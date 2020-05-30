import gym
import numpy as np
from gym import utils, Env, spaces
from shutil import copy
import os
import webbrowser
import time
import random

# encoding for q table
EMPTY = 0
COMMON = 1
VIRUS = 2
ISOLATION = 3

MAPS = {
  "15x15": [
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
}

class codefairEnv(gym.Env):
  def __init__(self, map_key="15x15"):
    map = MAPS[map_key]

    self.map = map = np.array(map).astype(int)
    self.nrow, self.ncol = nrow, ncol = map.shape
    self.reward_range = (-1, 1)

    self.action_length = 4
    self.state_length = 4 * 2 * 2 # 상하좌우, 코로나인지 일반인인지, 목적지에 도착했는지, 

    self.action_space = spaces.Discrete(self.action_length)
    self.observation_space = spaces.Discrete(self.state_length)

    # For rendering
    self.rendering_memory = []

  def get_target(self, direction):
    delta_x = [0, 0, -1, 1]
    delta_y = [-1, 1, 0, 0]
    return  self.link_position[0] + delta_x[direction],self.link_position[1] + delta_y[direction]

  def is_move_correct(self, action):
    if (action == 0): 
      # moving 
      target_x, target_y = self.get_target(action)
      return (0 <= target_x < self.nrow) and (0 <= target_y < self.ncol)
    elif (action == 1 or action == 2):
      # i.e. shooting an arrow
      return True
    return False

  def encode_link_position(self):
    return self.link_position[0] * self.ncol + self.link_position[1]

  def encode_blocks(self):
    encoding = 0
    factor = 1
    block_positions = [         [0,1],        [0,3],        [0,5],
                        [1,0],  [1,1],        [1,3], [1,4], [1,5],
                                [2,1],
                        [3,0],  [3,1]                             ]
    for position in block_positions:
      if self.map[position[0]][position[1]] in [SHOPKEEPER, ICE]:
        encoding += factor
      factor *= 2
    return encoding

  def render(self):
    self.memory_for_rendering.append(self.map_to_string())
    return 0

  def browser_rendering(self, begin, end, nb_episodes=0):
    copy('./includes/template.js', '../server/codefair.js')
    copy('./includes/index.html', '../server/index.html')
    with open('../server/codefair.js', "a+") as f:
      if (nb_episodes > 0):
        print(" log('<h3>Number of episodes since beginning: " + str(nb_episodes) + "</h3>');", file=f)
      for i in range(begin, end):
        print("if (counter == " + str(i - begin) + ") print_map('" + self.memory_for_rendering[i] + "');", file=f)
        print("\n}", file=f)
    webbrowser.open('file:///' + os.path.realpath('./includes/index.html'), autoraise=False)