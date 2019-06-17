import numpy as np
import os, sys

arr = np.loadtxt(os.path.join(sys.path[0], "positions.txt"))
print(arr.shape)
print(arr)
print(arr.reshape((2,5,3)))