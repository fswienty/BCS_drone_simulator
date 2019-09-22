import os
import sys
import time
import random
import numpy as np
import matplotlib.pyplot as plt
import glob
import ntpath
import math


traj = np.load(sys.path[0] + "/vel_traj.npy")
agents = traj.shape[0]
timesteps = traj.shape[1]

speed = np.zeros([agents, timesteps])

# for i in range(0, timesteps):
#     sqSum = traj[:, i, 0]**2 + traj[:, i, 1]**2 + traj[:, i, 2]**2
#     speed[i] = np.sqrt(sqSum)

speed = np.sqrt(traj[:, :, 0]**2 + traj[:, :, 1]**2 + traj[:, :, 2]**2)

plt.plot(speed[0])
plt.plot(speed[1])
plt.show()