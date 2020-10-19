import numpy as np
from sklearn.preprocessing import MinMaxScaler

reward_matrix = [np.load("./data/서초.npy"), np.load("./data/대치.npy"), np.load("./data/선릉.npy"), np.load("./data/남부터미널.npy"), np.load("./data/양재.npy"), np.load("./data/도곡.npy")]

scaler = MinMaxScaler(feature_range=(-1, 1))
scaler.fit(reward_matrix)
reward_matrix = scaler.transform(reward_matrix)

print(reward_matrix)