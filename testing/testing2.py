import os
import sys
import time
import random
import numpy as np
import matplotlib.pyplot as plt
import glob
import ntpath


npTest = np.ones([4, 2, 3])
path = os.path.join(sys.path[0], "trajectories")
print(path)
np.save(path + "/npTest.npy", npTest)
