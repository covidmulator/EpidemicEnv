from envs.EpidemicEnv import EpidemicEnv
from gym.envs.registration import register

register(
  id='EpidemicEnv-v0',
  entry_point='envs:EpidemicEnv',
  max_episode_steps=100,
)
