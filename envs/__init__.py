from QlearningAgent.envs.codefairEnv import CodefairEnv
from gym.envs.registration import register

register(
  id='CodefairEnv-v0',
  entry_point='gym_alttp_gridworld.envs:CodefairEnv',
)
