import os
import sys
import time
import random
import numpy as np
import matplotlib.pyplot as plt
import glob
import ntpath
import math


#    x   y   z  time
sequence1 = [
    (1, 1, 1, 1.0),
    (2, 2, 2, 3.0),
    (3, 3, 3, 1.0),
]

traj = np.load(sys.path[0] + "/trajectories/pos_traj.npy")
agents = traj.shape[0]
timesteps = traj.shape[1]

mySeq = traj[0]

print(sequence1)
print(mySeq)

print("forwards!")
for position in sequence1:
    end_time = time.time() + 0.2
    while time.time() < end_time:
        print(position[0], position[1], position[2], 0)
        time.sleep(0.1)

print("backwards!")
for position in reversed(sequence1):
    end_time = time.time() + 0.2
    while time.time() < end_time:
        print(position[0], position[1], position[2], 0)
        time.sleep(0.1)
