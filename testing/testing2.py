import os
import sys
import time
import random
import numpy as np
import matplotlib.pyplot as plt
import glob
import ntpath


def test(k):
    trajLen = 10
    posGrad = np.zeros([2, trajLen, 3])
    for i in range(0, k):
        posGrad[:, i, :] = (k - i)
    for i in range(k, trajLen):
        posGrad[:, i, :] = 0
    return posGrad


t9 = test(9)
t3 = test(3)


tmp = np.zeros([2, 10, 3])
for i in range(0, 10):
    tmp[:, i, :] += t3[:, 0, :] * t9[:, i, :]

print(tmp)
