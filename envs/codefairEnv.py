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

    obs_n    = list()
    reward_n = list()
    done_n   = list()
    info_n   = {'n': []}

    self.has_virus = False
    self.step_index = 0
    
    self.action_space = spaces.Discrete(self.action_length)
    self.observation_space = spaces.Discrete(self.state_length)

    # For rendering
    self.rendering_memory = []

  def get_target(self, direction):
    delta_x = [0, 0, -1, 1]
    delta_y = [-1, 1, 0, 0]
    return  self.link_position[0] + delta_x[direction],self.link_position[1] + delta_y[direction]

  def is_move_correct(self, action):
    if (action == 0 or action == 1):
      # moving 
      target_x, target_y = self.get_target(action)
      return (0 <= target_x < self.nrow) and (0 <= target_y < self.ncol)
    elif (action == 2):
      # virus
      return True
    elif (action == 3):
      # isolated
      return True
    return False

  def encode_link_position(self):
    # return link position between 0 and 225
    return self.link_position[0] * self.ncol + self.link_position[1]

  def move_link(self, target_x, target_y):
    self.map[target_x][target_y] = 2
    self.map[self.link_position[0]][self.link_position[1]] = 0
    self.link_position[0], self.link_position[1] = target_x, target_y

  def map_to_string(self):
    s = ''
    for row in self.map:
      for x in row:
        s += str(x)

    return s

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