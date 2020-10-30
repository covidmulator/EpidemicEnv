from envs.EpidemicEnv import EpidemicEnv
from envs.EpidemicMultiEnv import EpidemicMultiEnv
from gym.envs.registration import register
import numpy as np

register(
  id='EpidemicEnv-v0',
  entry_point='envs:EpidemicEnv',
  max_episode_steps=100,
)

r = [
  np.load("./data/seocho.npy"),
  np.load("./data/daechi.npy"),
  np.load("./data/dogok.npy"),
  np.load("./data/yangjae.npy"),
  np.load("./data/sunreung.npy"),
  np.load("./data/nambu.npy")
]

register(
  id='EpidemicMultiEnv-v0',
  entry_point='envs:EpidemicMultiEnv',
  max_episode_steps=100,
  kwargs={
    "env_config": {"agent_num": 15, "population": r}
  }
)