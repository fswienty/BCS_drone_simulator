import numpy as np

x = np.array([[[1,2,3],[4,5,6],[7,8,9],[10,11,12]],[[13,14,15],[16,17,18],[19,20,21],[22,23,24]]], ndmin=3)
y = np.array([[5,5,5],[6,6,6],[7,7,7],[8,8,8]], ndmin=2)

start_pos = np.array([[1,0,0],[-2,-2,-2],[0,3,0]])
pos = np.load("pos_traj.npy")
pos[:,0,:] = start_pos
print(pos)




