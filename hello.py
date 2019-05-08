import numpy as np

x = np.array([[[1,2,3],[4,5,6],[7,8,9],[10,11,12]],[[13,14,15],[16,17,18],[19,20,21],[22,23,24]]], ndmin=3)
y = np.array([[5,5,5],[6,6,6],[7,7,7],[8,8,8]], ndmin=2)

print(x)

print(x.shape)

num_agents = x.shape[0]
num_traj = x.shape[1]
num_dim = x.shape[2]



x_flat = x.flatten()
x_rebuilt = x_flat.reshape(num_agents,num_traj,num_dim)
