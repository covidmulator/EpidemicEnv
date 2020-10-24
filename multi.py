import os
import random
import gym
import envs
import numpy as np

if __name__ == "__main__":  
  population = [
    np.load("./data/서초.npy"),
    np.load("./data/대치.npy"),
    np.load("./data/선릉.npy"),
    np.load("./data/남부터미널.npy"),
    np.load("./data/양재.npy"),
    np.load("./data/도곡.npy")
  ]

  # 서초: (2,9)
  # 대치: (11,4)
  # 도곡:(9,4)
  # 양재:(7,4)
  # 선릉:(9,9)
  # 남부터미널: (3,4)

  env = gym.make('EpidemicMultiEnv-v0')
  env.env.__init__(100, population)

  agent_num = env.env.agent_num

  reward_arr = [0 for _ in range(agent_num)]
  reward_all_arr = [0 for _ in range(agent_num)]
  Q = np.zeros([env.observation_space.n, env.action_space.n])
  Q_arr = [Q for _ in range(agent_num)]

  lr = .8
  y = .95
  epsilon = .9
  num_episodes = 300

  for i in range(num_episodes):
    s = env.reset()
    rAll = 0
    d = False
    j = 0

    while j < num_episodes:
      actions = list()
      j += 1
      # Choose an action by epsilon-greedy (with noise) picking from Q table
      for k in range(agent_num):
        if (random.random() < (epsilon / np.log(i+2))):
          a = random.randint(0, env.action_space.n - 1)
        else:
          a = np.argmax(Q[s,:] + np.random.randn(1,env.action_space.n)*(1./(i+1)))
        
        actions.append(a)

      # Get new state and reward from environment
      s1, r, d, _ = env.step(actions)
      # Update Q-Table with new knowledge
      for index in range(agent_num):
        Q_sa = Q_arr[index][s[index], actions[index]]
        Q_arr[index][s[index], actions[index]] = Q_sa + lr * (r[index] + y * np.max(Q_arr[index][s1[index], :]) - Q_sa)
        reward_all_arr[index] += r[index]
        s[index] = s1[index]

      os.system('cls' if os.name == 'nt' else 'clear')
      print(f'num_episodes: {i}') # 기본 정보
      print('서초\t\t대치\t선릉\n남부터미널\t양재\t도곡')
      for i in range(15):
        print(f'{env.env.agent_matrix[0][i]}\t{env.env.agent_matrix[1][i]}\t{env.env.agent_matrix[2][i]}')
      print("")
      for i in range(15):
        print(f'{env.env.agent_matrix[3][i]}\t{env.env.agent_matrix[4][i]}\t{env.env.agent_matrix[5][i]}')
