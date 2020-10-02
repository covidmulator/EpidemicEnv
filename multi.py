import numpy as np
import os
import random
import gym

if __name__ == "__main__":
  agent_num = 15

  env = gym.make('EpidemicMultiEnv-v0')

  env.env.__init__(agent_num)

  reward = 0

  reward_arr = [0 for _ in range(agent_num)]
  Q_arr = [np.zeros([env.observation_space.n, env.action_space.n]) for _ in range(agent_num)]

  lr = .8
  y = .95
  epsilon = .9
  num_episodes = 1000

  print(Q_arr)

  for i in range(num_episodes):
    for i in range(agent_num):
      s = env.reset() # error
      rAll = 0
      d = False
      j = 0

      while j < num_episodes:
        j += 1
        # Choose an action by epsilon-greedy (with noise) picking from Q table
        if (random.random() < (epsilon / np.log(i+2))):
            a = random.randint(0, env.action_space.n - 1)
        else:
            a = np.argmax(Q[s,:] + np.random.randn(1,env.action_space.n)*(1./(i+1)))
        # Get new state and reward from environment
        s1,r,d,_ = env.step(a)
        # Update Q-Table with new knowledge
        s1 = int(s1)
        Q[s,a] = Q[s,a] + lr * (r + y * np.max(Q[s1,:]) - Q[s,a])
        rAll += r
        s = s1
        if d == True:
          break
      os.system('cls' if os.name == 'nt' else 'clear')
      print("num_episodes: ", i, "\nreward: ", int(rAll))
