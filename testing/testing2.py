import os
import sys
import time
import random
import numpy as np
import matplotlib.pyplot as plt
import glob
import ntpath
import math


def circleCoordinates(amount, radius, angleOffset):
    coordinateArray = np.zeros([amount, 3])
    angleStep = 360 / amount
    for i in range(0, amount):
        currRad = math.radians(i * angleStep + angleOffset)
        coordinateArray[i] = np.array([radius * math.cos(currRad), radius * math.sin(currRad), 1])
    return coordinateArray


arr = circleCoordinates(10, 1, 0)
for pos in arr:
    print("{}, {}, {}".format(pos[0], pos[1], pos[2]))
