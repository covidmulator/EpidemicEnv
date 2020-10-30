from ray import tune
import ray
from ray.rllib.agents import a3c


import gym
import numpy as np
from gym import spaces
from sklearn.preprocessing import MinMaxScaler
from random import choice, randint, random
from typing import List, Tuple

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
  def __init__(self, env_config):
    agent_matrix = AGENT_MATRIX
    reward_matrix = REWARD_MATRIX

    self.agent_num = env_config["agent_num"]
    self.action_length = 4
    self.state_length = 15 * 15
<<<<<<< HEAD
    self.action_space = spaces.Box(low=-1.0,high=4.0,shape=(15,15),dtype=np.float32),
    self.observation_space = spaces.Box(low=-1.0, high=4.0,shape=(15,15),dtype=np.float32)
=======
    self.action_space = spaces.Box(low=0.0, high=4.0, shape=(15, 15), dtype=np.float32)
    self.observation_space = spaces.Box(low=0.0, high=4.0, shape=(15, 15), dtype=np.float32)
>>>>>>> 6d0943a4bd9aa2d388a8750fd40d87ea3b77b7f6
    self.population = self.min_max_norm(env_config["population"])

    Q = np.zeros([15, 15])

    self.agent_matrix = agent_matrix = np.array(agent_matrix).astype(int)
    self.nrow, self.ncol = nrow, ncol = self.agent_matrix.shape
    self.reward_range = (-1, 1)

    self.agents = self.get_position()
    self.has_virus = self.get_virus()

    self.episode = 0
    self.destinations = self.get_position()
    
    self.steps = [0 for _ in range(env_config["agent_num"])]

    self.reward_matrix = self.get_reward_matrix(reward_matrix)

    self.Q_list = [Q for _ in range(env_config["agent_num"])]
    self.lr = .8
    self.y = .95
    self.epsilon = .9
    self.s = [self.encode_state(i) for i in range(self.agent_num)]

    self.reward_arr = [0 for _ in range(env_config["agent_num"])]
    self.reward_all_arr = [0 for _ in range(env_config["agent_num"])]


  def min_max_norm(self, lst: list) -> list:
    scaler = MinMaxScaler(feature_range=(-1, 1))
    scaler.fit(lst)
    lst_norm = scaler.transform(lst)

    return lst_norm

  def get_reward_matrix(self, matrix: list) -> list:
    matrix_result = matrix
    e = self.episode

    matrix_result[2][9] = self.population[0][e]
    matrix_result[11][4] = self.population[1][e]
    matrix_result[9][4] = self.population[2][e]
    matrix_result[7][4] = self.population[3][e]
    matrix_result[9][9] = self.population[4][e]
    matrix_result[3][4] = self.population[5][e]
    return matrix_result

  def get_position(self) -> list:
    num_x = list(range(0, self.ncol))
    num_y = list(range(0, self.nrow))
    positions = list()
    positions_return = list()

    for x in num_x:
      for y in num_y:
        positions.append([x, y])

    for _ in range(self.agent_num):
      selected = choice(positions)
      positions_return.append(selected)
      positions.pop(positions.index(selected))

    return positions_return

  def get_virus(self) -> list:
    index = randint(0, self.agent_num - 1)
    virus_return = [False for _ in range(self.agent_num)]
    virus_return[index] = True
    x, y = self.agents[index]
    self.agent_matrix[x][y] = VIRUS

    return virus_return

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

    for action in range(4):
      if(self.is_move_correct(action, index)):
        around_x, around_y = self.get_target(action, index)
      
        if(self.agent_matrix[around_x][around_y] == VIRUS):
          self.has_virus[self.agents.index([x, y])] = True
          result = True
  
    return result

  def is_move_correct(self, action: int, index: int) -> bool:
    if(0 < action < 4):
      agent_x, agent_y = self.get_target(action, index)
      return (0 <= agent_x < self.nrow - 1) and (0 <= agent_y < self.ncol - 1)
    
    return False

  def encode_state(self, index: int) -> int:
    x = self.agents[index][0]
    y = self.agents[index][1]

    return self.agent_matrix[x][y]

  def move_link(self, x: int, y: int, index: int, status: int) -> None:
    agent_x = self.agents[index][0]
    agent_y = self.agents[index][1]

    self.agent_matrix[x][y] = status

    self.agent_matrix[agent_x][agent_y] = 0
    self.agents[index][0] = x
    self.agents[index][1] = y

  def move(self, direction: int, index: int) -> Tuple[float, bool]:
    agent_x = self.agents[index][0]
    agent_y = self.agents[index][1]

    status = COMMON
    self.steps[index] += 1

    if self.is_virus_around(index):
      status = VIRUS
      self.steps[index] -= 1

    x, y = self.get_target(direction, index)

    object_in_direction = int(self.agent_matrix[x][y])

    reward_return = 0

    is_end = False

    if x == self.destinations[index][0] and y == self.destinations[index][1]:
      status = EMPTY
      is_end = True
    elif object_in_direction == EMPTY:
      self.move_link(x, y, index, status)
      reward_return = .5
    elif object_in_direction == VIRUS:
      self.move_link(x, y, index, status)
      reward_return = -.1
    elif object_in_direction == COMMON:
      self.move_link(x, y, index, status)
      reward_return = -.1
    elif object_in_direction == ISOLATION:
      self.move_link(x, y, index, status)
      reward_return = -.1

    reward_return += self.reward_matrix[agent_x][agent_y]
    
    
    return reward_return, is_end

  def choose_action(self):
    actions = list()
    for index in range(self.agent_num):
      if (random() < (self.epsilon / np.log(self.episode + 2))):
        a = randint(0, 15 - 1)
      else:
        a = np.argmax(self.Q_list[index][self.s,:][index] + np.random.randn(1, 15) * (1. / (self.episode + 1)))

      actions.append(a)

    return actions

  def action(self, actions) -> Tuple[list, list, list, dict]:
    rewards = list()
    encode_states = list()
    dones = list()
    
    for i in range(self.agent_num):
      if (self.is_move_correct(actions[i], i)):
        r, d = self.move(actions[i], i)
      else:
        r, d = -1, False

      encode_states.append(self.encode_state(i))
      rewards.append(r)
      dones.append(d)

    return encode_states, rewards, False in dones, {}

  def update_reward_matrix(self, matrix: list) -> None:
    for x, lst in enumerate(self.reward_matrix):
      for y in range(len(lst)):
        self.reward_matrix[x][y] += matrix[x][y]

  def step(self, matrix: list) -> Tuple[list, float, list, dict]:
    matrix = matrix[0]
    print(len(matrix))
    self.update_reward_matrix(matrix)

    actions = self.choose_action()
    s1, r, d, _ = self.action(actions)

    for index in range(self.agent_num):
      Q_sa = self.Q_list[index][self.s[index], actions[index]]
      self.Q_list[index][self.s[index], actions[index]] = Q_sa + self.lr * (r[index] + self.y * np.max(self.Q_list[index][s1[index], :]) - Q_sa)
      self.reward_all_arr[index] += r[index]
      self.s[index] = s1[index]

    return self.agent_matrix, np.mean(self.steps), d, {}

  def reset(self) -> List[int]:
    agent_matrix = AGENT_MATRIX
    reward_matrix = REWARD_MATRIX

    self.episode += 1

    self.agent_matrix = agent_matrix = np.array(agent_matrix).astype(int)
    self.reward_matrix = self.get_reward_matrix(reward_matrix)

    self.agents = self.get_position()
    self.has_virus = self.get_virus()

    self.destinations = self.get_position()

    states = [self.encode_state(i) for i in range(self.agent_num)]
    self.s = states

    return np.array(agent_matrix).astype(int)

if __name__ == "__main__":
  population = [
    np.load("./data/seocho.npy"),
    np.load("./data/daechi.npy"),
    np.load("./data/dogok.npy"),
    np.load("./data/yangjae.npy"),
    np.load("./data/sunreung.npy"),
    np.load("./data/nambu.npy")
  ]
<<<<<<< HEAD
  ray.init()
  trainer = a3c.A3CTrainer(env=EpidemicMultiEnv, config={
      "env_config": {'agent_num':200,'population':population},  # config to pass to env class
  })
=======
ray.init()
trainer = a3c.A3CTrainer(env=EpidemicMultiEnv, config={
    "env_config": {'agent_num':100, 'population':population},  # config to pass to env class
})
>>>>>>> 6d0943a4bd9aa2d388a8750fd40d87ea3b77b7f6

  while True:
    print(trainer.train())
