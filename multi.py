import os
import random
import gym
import envs
import numpy as np

if __name__ == "__main__":  
  population = [
    np.load("./data/서초.npy"),
    np.load("./data/대치.npy"),
    np.load("./data/도곡.npy"),
    np.load("./data/양재.npy"),
    np.load("./data/선릉.npy"),
    np.load("./data/남부터미널.npy")
  ]

  env = gym.make('EpidemicMultiEnv-v0')
  env.env.__init__(100, population)

  agent_num = env.env.agent_num

  num_episodes = 300


  r = [
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


  for i in range(num_episodes):
    s = env.reset()
    rAll = 0
    d = False
    j = 0

    while j < num_episodes:
      j += 1
      state, reward, dones = env.step(r)

      os.system('cls' if os.name == 'nt' else 'clear')
      print(f'num_episodes: {i}') # 기본 정보
      print("서초: (2,9)   # 대치: (11,4)   # 도곡:(9,4)   # 양재:(7,4)   # 선릉:(9,9)   # 남부터미널: (3,4)")
      print(f'{env.env.agent_matrix}')

      if False not in dones:
        break
