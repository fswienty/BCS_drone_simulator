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
        coordinateArray[i] = np.array([math.cos(currRad), math.sin(currRad), 0])
    return coordinateArray


print(circleCoordinates(4, 1, 45))
