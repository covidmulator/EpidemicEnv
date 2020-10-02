from typing import Tuple
import gym
import numpy as np
from gym import spaces
from random import choice

# encoding for q table
EMPTY = 0
COMMON = 2
VIRUS = 1
ISOLATION = 3

MAPS = {
  "agent_map": [
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
  ],
  "reward_map": [
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
  ],
}

class EpidemicMultiEnv(gym.Env):
  def __init__(self, agent_num: int = 2) -> None:
    agent_map = MAPS["agent_map"]

    self.agent_num = agent_num
    self.agent_map = agent_map = np.array(agent_map).astype(int)
    self.nrow, self.ncol = agent_map.shape
    self.reward_range = (-1, 1)
    
    self.action_length = 4
    self.state_length = 4 * 2 * 2

    self.state_arr = [0 for _ in range(agent_num)]
    self.position_arr = self.get_position(agent_num)

    self.action_space = spaces.Discrete(self.action_length)
    self.observation_space = spaces.Discrete(self.state_length)

    self.step_index = 0
    self.steps_since_start = 0

  def get_position(self, agent_num: int = 2) -> list:
    num_x = list(range(0, 16))
    num_y = list(range(0, 16))
    position = []

    for i in range(agent_num):
      position.append((num_x.pop(num_x.index(choice(num_x))), num_y.pop(num_y.index(choice(num_y)))))

    return position

  def get_target(self, direction: int, index: int) -> int:
    delta_x = [0, 0, -1, 1]
    delta_y = [-1, 1, 0, 0]
    return  self.position_arr[index][0] + delta_x[direction], self.position_arr[index][1] + delta_y[direction]

  def is_virus_around(self, index: int) -> bool:
    result = False

    if(self.position_arrp[index][0] + -1, self.position_arr[index][1]):
      result = True
    elif(self.position_arr[index][0] + -1, self.position_arr[index][1]):
      result = True
    elif(self.position_arr[index][0], self.position_arr[index][1] + -1):
      result = True
    elif(self.position_arr[index][0], self.position_arr[index][1] + 1):
      result = True

    return result

  def is_move_correct(self, action: int) -> bool:
    if (0 < action < 4):
      # moving 
      target_x, target_y = self.get_target(action)
      return (0 <= target_x < self.nrow - 1) and (0 <= target_y < self.ncol - 1)

    return False

  def encode_state(self, index: int) -> int:
    has_virus = self.state_arr[index] == VIRUS
    return has_virus * 4 * (15 ** 2) * 4 * 2 * 2

  def encode_agent_position(self, index: int) -> int:
    return self.position_arr[index][0] * self.ncol + self.position_arr[index][0]

  def move_link(self, x: int, y: int, index: int) -> None:
    self.agent_map[x][y] = 1
    self.agent_map[self.position_arr[index][0]][self.position_arr[index][1]] = 0
    self.position_arr[index] = x, y

  def move(self, direction: int, index: int) -> Tuple[float, bool]:
    target_x, target_y = self.get_target(direction, index)
    object_in_direction = int(self.agent_map[target_x][target_y])

    reward_return = 0

    if (object_in_direction == EMPTY):
      self.move_link(target_x,target_y)
      reward_return = .1
    if (object_in_direction == VIRUS):
      self.move_link(target_x,target_y)
      self.has_virus = True
      reward_return = -.1
    if (object_in_direction == ISOLATION and self.has_virus):
      self.has_virus = False
      reward_return = .1
    
    return (reward_return, False)

  def step(self, action: int, index: int) -> Tuple[int, float, bool, dict]:
    if (self.is_move_correct(action)):
      r, d = self.move(action)
    else:
      r, d = -1, False

    # After x steps, end of episode
    self.steps_since_start += 1
    self.has_bow_of_light = (self.steps_since_start >= 100)
    if (self.steps_since_start == 200):
      d = True
      self.steps_since_start = 0

    return (self.encode_state(index), r, d, {})

  def reset(self) -> int:
    agent_map = MAPS["agent_map"]
    self.agent_map = agent_map = np.array(agent_map).astype(int)

    self.state_arr = [0 for _ in range(self.agent_num)]
    self.position_arr = self.get_position(self.agent_num)
    states = [self.encode_state(i) for i in range(self.agent_num+1)]
    return states