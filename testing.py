import os, sys
import time
from math import sin, cos
import numpy as np


a = [3,6,1]
b = [1,2,3]

for _ in range(0, 20):
    print(time.clock(), time.perf_counter(), time.process_time())
    time.sleep(.1)