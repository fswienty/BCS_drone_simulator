import os
import time
import random
import numpy as np
import matplotlib.pyplot as plt

xVals = np.arange(-1,2,.05)
print(xVals)
yVals = 0.5 * 0.5 * (np.tanh(4 * xVals - 3) + 1)
plt.plot(xVals, yVals)
plt.show()