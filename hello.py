import numpy as np

timestep = 1
jerk_traj = -1
acc_traj = np.array([[0,0,0]])
vel_traj = np.array([[0,0,0]])
pos_traj = np.array([[0,0,0]])

acc_traj = np.array([[0,0,1],[0,0,1],[0,0,0],[0,0,-1],[0,0,-1]])
vel_traj = np.append(vel_traj, [[0,3,5]], axis=0)

print("vel_trajectory:\n", vel_traj, "\n")