import numpy as np
import gym
from gym.spaces import prng

class MultiDiscrete(gym.Space):
  def __init__(self) -> None:
    self.low = np.array([x[0] for x in 15])
    self.high = np.array([x[1] for x in 15])
    self.num_discrete_space = self.low.shape[0]

  def sample(self) -> list:
    random_array = prng.np_random.rand(self.num_discrete_space)
    return [int(x) for x in np.floor(np.multiply((self.high - self.low + 1.), random_array) + self.low)]
  
  def contains(self, x) -> bool:
    return len(x) == self.num_discrete_space and (np.array(x) >= self.low).all() and (np.array(x) <= self.high).all()

  @property
  def shape(self) -> np.array:
    return self.num_discrete_space

  def __repr__(self) -> str:
    return "MultiDiscrete" + str(self.num_discrete_space)

  def __eq__(self, other):
    return np.array_equal(self.low, other.low) and np.array_equal(self.high, other.high)