import numpy as np
import os, sys
import re

def loadFormationList(name: str):
    with open(os.path.join(sys.path[0], name), "r") as file:
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

#print(loadPositionList("positions.txt"))
loadFormationList("positions.txt")
