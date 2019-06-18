import numpy as np
import os, sys
import re

def loadFormationList(name: str):
    #with open(os.path.join(sys.path[0], name)) as file:
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), name)) as file:
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

    arr = np.loadtxt(os.path.join(sys.path[0], name))
    arr = arr.reshape((positions, drones, 3))

    return arr

def loadFormation(name: str) -> (np.array, int):
    drones = _file_len(name)
    #arr = np.loadtxt(os.path.join(sys.path[0], name))
    arr = np.loadtxt(os.path.join(os.path.dirname(os.path.abspath(__file__)), name))
    arr = arr.reshape((drones, 3))
    return (arr, drones)

def _file_len(name):
    # with open(os.path.join(sys.path[0], name)) as f:
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), name)) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

class FormationLoader():

    def __init__(self, name: str):
        #self.name = name
        (self.array, self.drones) = loadFormation("{}.txt".format(name))

