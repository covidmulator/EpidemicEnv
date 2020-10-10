import numpy as np
import os
import random
import gym
import envs

if __name__ == "__main__":  
  env = gym.make('EpidemicMultiEnv-v0')
  
  agent_num = env.env.agent_num

  reward_arr = [0 for _ in range(agent_num)]
  reward_all_arr = [0 for _ in range(agent_num)]
  Q = np.zeros([env.observation_space.n, env.action_space.n])
  Q_arr = [np.zeros([env.observation_space.n, env.action_space.n]) for _ in range(agent_num)]

  lr = .8
  y = .95
  epsilon = .9
  num_episodes = 1000

  for i in range(num_episodes):
    s = env.reset() # error
    rAll = 0
    d = False
    j = 0

    while j < num_episodes:
      actions = list()
      j += 1
      # Choose an action by epsilon-greedy (with noise) picking from Q table
      for _ in range(agent_num):
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
    print(f'num_episodes: {i} \nreward: {reward_all_arr}\nagent: \n{env.env.agent_matrix}')
