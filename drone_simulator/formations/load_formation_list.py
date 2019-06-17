import numpy as np
import os, sys
import re

def loadFormationList(fname: str):
    #with open(os.path.join(sys.path[0], fname)) as file:
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), fname)) as file:
        text = file.read()
        # parse the number of drones
        drones = re.search(r'\# Drones = \d+', text)
        drones = re.search(r'\d+', drones.group())
        drones = int(drones.group())
        # parse the number of positions
        positions = re.search(r'\# Positions = \d+', text)
        positions = re.search(r'\d+', positions.group())
        positions = int(positions.group())
        arr2 = np.fromstring(text)
        print(arr2)

    arr = np.loadtxt(os.path.join(sys.path[0], fname))
    arr = arr.reshape((positions, drones, 3))

    return arr

def loadFormation(fname: str):
    drones = _file_len(fname)
    #arr = np.loadtxt(os.path.join(sys.path[0], fname))
    arr = np.loadtxt(os.path.join(os.path.dirname(os.path.abspath(__file__)), fname))
    arr = arr.reshape((drones, 3))
    return arr

def _file_len(fname):
    # with open(os.path.join(sys.path[0], fname)) as f:
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), fname)) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

#print(loadFormation("line.txt"))

