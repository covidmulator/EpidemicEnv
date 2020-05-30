import numpy as np
import os
import random
import gym
import gym_alttp_gridworld

if __name__ == "__main__":
  env = gym.make('Environment-v0')

  reward = 0

  Q = np.zeros([env.ov])