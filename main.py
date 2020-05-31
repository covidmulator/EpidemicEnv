import numpy as np
import os
import random
import gym
import envs

if __name__ == "__main__":
  env = gym.make('EpidemicEnv-v0')

  reward = 0

  Q = np.zeros([env.observation_space.n, env.action_space.n])
  lr = .8
  y = .95
  epsilon = .9
  num_episodes = 1000

  for i in range(num_episodes):
    s = env.reset()
    rAll = 0
    d = False
    j = 0

    while j < num_episodes:
      env.render()
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
    if i == 999:
      env.browser_rendering(0, (i + 1), i)
    os.system('cls' if os.name == 'nt' else 'clear')
    print("num_episodes: ", i, "\nreward: ", int(rAll))
