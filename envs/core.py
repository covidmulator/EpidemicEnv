import numpy as np
import ray

class EntityState(object):
  def __init__(self) -> None:
    # physical position
    self.p_pos = None

class AgentState(EntityState):
  def __init__(self) -> None:
    super(AgentState, self).__init__()
    # communication utterance
    self.c = None

class Action(object):
  def __init__(self) -> None:
    # physical action
    self.u = None
    # communication action
    self.c = None

class Entity(object):
  def __init__(self) -> None:
    # name
    self.name = 'Epidemic Environment'
    # properties
    # self.size = 