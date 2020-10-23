import gym
import numpy as np
from gym import spaces
from sklearn.preprocessing import MinMaxScaler
from random import choice, randint
from typing import Dict, Tuple

# encoding for q table
# entity에 개개인의 값을 가지도록 만들면 좋을 듯
EMPTY = 0
COMMON = 2
VIRUS = 1
ISOLATION = 3

AGENT_MATRIX = [
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]

class EpidemicMultiEnv(gym.Env):
  def __init__(self, agent_num: int, reward_matrix: np.array) -> None:
    agent_matrix = AGENT_MATRIX

    self.agent_num = agent_num
    self.action_length = 4
    self.state_length = 4 * 2 * 2
    self.action_space = spaces.Discrete(self.action_length)
    self.observation_space = spaces.Discrete(self.state_length)
    self.rewards = self.min_max_norm(reward_matrix)

    self.agent_matrix = agent_matrix = [np.array(agent_matrix).astype(int) for _ in range(len(self.rewards))]
    self.nrow, self.ncol = nrow, ncol = self.agent_matrix[0].shape
    self.reward_range = (-1, 1)

    self.agents = self.get_position(len(self.rewards))
    self.has_virus = self.get_virus()

    self.episode = 0
    self.destinations = self.get_position(len(reward_matrix))

  def get_virus(self) -> list:
    virus_return = [False for _ in range(self.agent_num)]
    virus_return[randint(0, self.agent_num)] = True

    return virus_return

  def min_max_norm(self, lst: np.array) -> np.array:
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaler.fit(lst)
    reward_matrix = scaler.transform(lst)

    return reward_matrix

  def get_position(self, matrix_num: int) -> list:
    num_x = list(range(0, self.ncol))
    num_y = list(range(0, self.nrow))
    num_z = list(range(0, matrix_num))
    position_return = list()
    positions = list()
    
    for x in num_x:
      for y in num_y:
        for z in num_z:
          positions.append([x, y, z])

    for _ in range(self.agent_num):
      selected = choice(positions)
      position_return.append(selected)
      positions.pop(positions.index(selected))
    
    return position_return

  def get_target(self, direction: int, index: int) -> Tuple[int, int]:
    delta_x = [0, 0, -1, 1]
    delta_y = [-1, 1, 0, 0]
    agent_x = self.agents[index][0]
    agent_y = self.agents[index][1]
    return agent_x + delta_x[direction], agent_y + delta_y[direction]

  def is_virus_around(self, index: int) -> bool:
    result = False
    x = self.agents[index][0]
    y = self.agents[index][1]
    z = self.agents[index][2]

    for i in range(4):
      around = self.get_target(i, index)
      if(around == VIRUS):
        self.has_virus[self.agents.index(x, y, z)] = True
        result = True

    return result

  def is_move_correct(self, action: int, index: int) -> bool:
    if(0 < action < 4):
      agent_x, agent_y = self.get_target(action, index)
      return (0 <= agent_x < self.nrow - 1) and (0 <= agent_y < self.ncol - 1)
    
    return False
  
  def encode_state(self, index: int) -> int:
    return self.has_virus[index] * 4 * (15 ** 2) * 4 * 2 * 2

  def move_link(self, x: int, y: int, z: int, index: int, status: int) -> None:
    agent_x = self.agents[index][0]
    agent_y = self.agents[index][1]
    agent_z = self.agents[index][2]

    self.agent_matrix[z][x][y] = 2 # update agent matrix

    self.agent_matrix[agent_z][agent_x][agent_y] = 0
    self.agents[index][0] = x
    self.agents[index][1] = y
    self.agents[index][2] = z

  def move(self, direction: int, index: int) -> Tuple[float, bool]:
    agent_x = self.agents[index][0]
    agent_y = self.agents[index][1]
    z = self.agents[index][2]
    status = COMMON

    if(self.is_virus_around(index)):
      status = VIRUS

    if(agent_x == agent_y == 7): # 역에 있을때
      z = self.destinations[index][2] # 역을 통해 다른 지역 이동

    x, y = self.get_target(direction, index)

    reward = self.rewards[z][self.episode]
    object_in_direction = int(self.agent_matrix[z][x][y])

    reward_return = 0

    is_end = False

    if x == self.destinations[index][0] \
      and y == self.destinations[index][1] \
      and z == self.destinations[index][2]:
      is_end = True

    if object_in_direction == EMPTY:
      self.move_link(x, y, z, index, status)
      reward_return = .5
    elif object_in_direction == VIRUS:
      self.move_link(x, y, z, index, status)
      reward_return = -.1
    elif object_in_direction == COMMON:
      self.move_link(x, y, z, index, status)
      reward_return = -.1
    elif object_in_direction == ISOLATION:
      self.move_link(x, y, z, index, status)
      reward_return = -.1

    reward_return += reward
    
    return reward_return, is_end

  def step(self, actions) -> Tuple[list, list, list, Dict]:
    rewards = list()
    dones = list()
    encode_states = list()
    
    for i in range(self.agent_num):
      if (self.is_move_correct(actions[i], i)):
        r, d = self.move(actions[i], i)
      else:
        r, d = -1, False

      encode_states.append(self.encode_state(i))
      rewards.append(r)
      dones.append(d)

    return encode_states, rewards, dones, {}

  def reset(self) -> int:
    agent_matrix = AGENT_MATRIX

    self.agent_matrix = agent_matrix = [np.array(agent_matrix).astype(int) for _ in range(len(self.rewards))]

    self.episode += 1

    self.agents = self.get_position(len(self.rewards))
    states = [self.encode_state(i) for i in range(self.agent_num)]
    return states