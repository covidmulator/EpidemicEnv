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
COMMON = 2
VIRUS = 1
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

class EpidemicEnv(gym.Env):
  def __init__(self, map_key="15x15"):
    map = MAPS[map_key]

    self.map = map = np.array(map).astype(int)
    self.nrow, self.ncol = nrow, ncol = map.shape
    self.reward_range = (-1, 1)

    self.action_length = 4
    self.state_length = 4 * 2 * 2 # 상하좌우, 코로나인지 일반인인지, 목적지에 도착했는지, 

    self.agent_position = [3,2]


    # for multi agent
    obs_n    = list()
    reward_n = list()
    done_n   = list()
    info_n   = {'n': []}

    self.has_virus = False
    self.step_index = 0
    
    self.action_space = spaces.Discrete(self.action_length)
    self.observation_space = spaces.Discrete(self.state_length)

    self.steps_since_start = 0

    # For rendering
    self.rendering_memory = []

  def get_target(self, direction):
    delta_x = [0, 0, -1, 1]
    delta_y = [-1, 1, 0, 0]
    return  self.agent_position[0] + delta_x[direction], self.agent_position[1] + delta_y[direction]

  def is_virus_around(self):
    result = False

    if(self.agent_position[0] + -1, self.agent_position[1]):
      result = True
    elif(self.agent_position[0] + -1, self.agent_position[1]):
      result = True
    elif(self.agent_position[0], self.agent_position[1] + -1):
      result = True
    elif(self.agent_position[0], self.agent_position[1] + 1):
      result = True

    return result

  def is_move_correct(self, action):
    if (0 < action < 4):
      # moving 
      target_x, target_y = self.get_target(action)
      return (0 <= target_x < self.nrow - 1) and (0 <= target_y < self.ncol - 1)
    # elif (action == 2):
    #   # virus
    #   return True
    # elif (action == 3):
    #   # isolated
    #   return True
    return False

  def encode_state(self):
    return self.has_virus * 4 * (15 ** 2) * 4 * 2 * 2

  def encode_agent_position(self):
    # return link position between 0 and 225
    return self.agent_position[0] * self.ncol + self.agent_position[1]

  def move_link(self, target_x, target_y):
    self.map[target_x][target_y] = 2
    self.map[self.agent_position[0]][self.agent_position[1]] = 0
    self.agent_position[0], self.agent_position[1] = target_x, target_y

  def map_to_string(self):
    s = ''
    for row in self.map:
      for x in row:
        s += str(x)

    return s

  def render(self):
    self.rendering_memory.append(self.map_to_string())
    return 0

  def browser_rendering(self, begin, end, nb_episodes=0):
    copy('./includes/template.js', './server/codefair.js')
    copy('./includes/index.html', './server/index.html')
    with open('./server/codefair.js', "a+") as f:
      if (nb_episodes > 0):
        print("  log('<h3>Number of episodes since beginning: " + str(nb_episodes) + "</h3>');", file=f)
      for i in range(begin, end):
        print("  if (counter == " + str(i - begin) + ") print_map('" + self.rendering_memory[i] + "');", file=f)
      print("}", file=f)
    webbrowser.open('file:///' + os.path.realpath('./server/index.html'), autoraise=False)

  def move(self, direction):
    target_x, target_y = self.get_target(direction)
    object_in_direction = int(self.map[target_x][target_y])

    reward_return = 0;

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

    return reward_return, False

  def step(self, a):
    is_virus_around
    if (self.is_move_correct(a)):
      r, d = self.move(a)
    else:
      r, d = -1, False

    # After x steps, end of episode
    self.steps_since_start += 1
    self.has_bow_of_light = (self.steps_since_start >= 100)
    if (self.steps_since_start == 200):
      d = True
      self.steps_since_start = 0

    return (self.encode_state(), r, d, {})

  def reset(self):
    map = MAPS["15x15"]
    self.map = map = np.array(map).astype(int)
    self.agent_position = [3,2]
    self.has_virus = False
    return self.encode_state()