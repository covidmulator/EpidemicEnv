
# INPUTS
# 그리드월드 좌표내에 존재하는 에이전트를 검사할지 말지 
# 감염자 또는 확인되지 않은 사람들을 격리할지 말지
# 해당 에이전트 또는 전 에이전트에 대해 이동 제한을 확률적으로 높은 빈도로 제한할지 낮은 빈도로 제한할지

from EpidemicEnv.main import d


class Agent:
  def __init__(self, need_test=False, need_isolate=False, restrictions=False, position=[3, 2]):
    self.need_test = need_test # 그리드월드 좌표내에 존재하는 에이전트를 검사할지 말지 
    self.need_isolate = need_isolate # 감염자 또는 확인되지 않은 사람들을 격리할지 말지
    self.restrictions = restrictions # 해당 에이전트 또는 전 에이전트에 대해 이동 제한을 확률적으로 높은 빈도로 제한할지 낮은 빈도로 제한할지

    self.agent_position = position # 에이전트 포지션

    self.has_virus = False # 바이러스 유무

  def get_target(self, direction):
    delta_x = [0, 0, -1, 1]
    delta_y = [-1, 1, 0, 0]

    return  self.agent_position[0] + delta_x[direction], self.agent_position[1] + delta_y[direction]

  def is_virus_around(self):
    result = False

    if(self.agent_position[0] + -1, self.agent_position[1]):
      result = True
    elif(self.agent_position[0] + -1, self.agent_position[1]):
      result = True
    elif(self.agent_position[0], self.agent_position[1] + -1):
      result = True
    elif(self.agent_position[0], self.agent_position[1] + 1):
      result = True

    return result

  def is_move_correct(self, action):
    if (0 < action < 4):
      # moving 
      target_x, target_y = self.get_target(action)
      return (0 <= target_x < self.nrow - 1) and (0 <= target_y < self.ncol - 1)
    # elif (action == 2):
    #   # virus
    #   return True
    # elif (action == 3):
    #   # isolated
    #   return True
    return False

  def encode_state(self):
    return self.has_virus * 4 * (15 ** 2) * 4 * 2 * 2

  def move_link(self, target_x, target_y):
    self.map[target_x][target_y] = 2
    self.map[self.agent_position[0]][self.agent_position[1]] = 0
    self.agent_position[0], self.agent_position[1] = target_x, target_y
    