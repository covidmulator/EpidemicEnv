import gym
import numpy as np
from gym import spaces
from random import choice
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
REWARD_MATRIX = [
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
  def __init__(self, agent_num: int) -> None:
    reward_matrix = REWARD_MATRIX
    agent_matrix = AGENT_MATRIX

    self.agent_num = agent_num
    self.action_length = 4
    self.state_length = 4 * 2 * 2
    self.action_space = spaces.Discrete(self.action_length)
    self.observation_space = spaces.Discrete(self.state_length)
    
    self.reward_matrix = reward_matrix = np.array(reward_matrix).astype(int)
    self.agent_matrix = agent_matrix = np.array(agent_matrix).astype(int)
    self.nrow, self.ncol = nrow, ncol = self.reward_matrix.shape
    self.reward_range = (-1, 1)

    self.agents = self.get_position(agent_num)
    self.has_virus = [False for _ in range(agent_num)]

    self.steps_since_start = 0
    self.destination = (14, 14)

  def get_position(self, agent_num: int) -> list:
    num_x = list(range(0, 16))
    num_y = list(range(0, 16))
    position = list()

    for _ in range(agent_num):
      position.append([num_x.pop(num_x.index(choice(num_x))), num_y.pop(num_y.index(choice(num_y)))])
    
    return position

  def get_target(self, direction: int, index: int) -> Tuple[int, int]:
    delta_x = [0, 0, -1, 1]
    delta_y = [-1, 1, 0, 0]
    return self.agents[index][0] + delta_x[direction], self.agents[index][1] + delta_y[direction]

  def is_virus_around(self, index: int) -> bool:
    result = False

    if(self.agents[index][0] + -1, self.agents[index][1]):
      result = True
    elif(self.agents[index][0] + -1, self.agents[index][1]):
      result = True
    elif(self.agents[index][0], self.agents[index][1] + -1):
      result = True
    elif(self.agents[index][0], self.agents[index][1] + 1):
      result = True

    return result
  
  def is_move_correct(self, action: int, index: int) -> bool:
    if(0 < action < 4):
      target_x, target_y = self.get_target(action, index)
      return (0 <= target_x < self.nrow - 1) and (0 <= target_y < self.ncol - 1)
    
    return False
  
  def encode_state(self, index: int) -> int:
    return self.has_virus[index] * 4 * (15 ** 2) * 4 * 2 * 2

  def move_link(self, x: int, y: int, index: int) -> None:
    self.agent_matrix[x][y] = 2
    self.agent_matrix[self.agents[index][0]][self.agents[index][1]] = 0
    self.agents[index][0] = x
    self.agents[index][1] = y

  # def get_coord_state(self, x: int, y: int) -> int or False:
  #   for index, (agent_x, agent_y) in enumerate(self.agents):
  #     print(index)
  #     if agent_x == x and agent_y == y:
  #       return index

  #   return False

  def move(self, direction: int, index: int) -> Tuple[float, bool]:
    x, y = self.get_target(direction, index)
    object_in_direction = int(self.agent_matrix[x][y])

    reward_return = 0

    is_end = False

    if(x == self.destination[0] and y == self.destination[1]):
      is_end = True

    if(object_in_direction == EMPTY):
      self.move_link(x, y, index)
      reward_return = .2
    elif(object_in_direction == VIRUS):
      self.has_virus = True
      reward_return = -.1
    elif(object_in_direction == COMMON):
      pass
    elif(object_in_direction == ISOLATION): # 좌표의 에이전트 상태 확인하는 함수 필요 get_coord_state
      self.move_link(x, y, index)
      reward_return = -.1
    
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
    reward_matrix = REWARD_MATRIX
    agent_matrix = AGENT_MATRIX

    self.reward_matrix = reward_matrix = np.array(reward_matrix).astype(int)
    self.agent_matrix = agent_matrix = np.array(agent_matrix).astype(int)

    self.agents = self.get_position(self.agent_num)
    states = [self.encode_state(i) for i in range(self.agent_num)]
    return states