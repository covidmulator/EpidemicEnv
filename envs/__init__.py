from envs.EpidemicEnv import EpidemicEnv
from envs.EpidemicMultiEnv import EpidemicMultiEnv
from gym.envs.registration import register

register(
  id='EpidemicEnv-v0',
  entry_point='envs:EpidemicEnv',
  max_episode_steps=100,
)

register(
  id='EpidemicMultiEnv-v0',
  entry_point='envs:EpidemicMultiEnv',
  max_episode_steps=100,
  kwargs={"agent_num": 15}
)