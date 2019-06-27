import os
import time
import random
import numpy as np
import matplotlib.pyplot as plt
import glob
import ntpath


from direct.gui.DirectGui import DirectScrolledFrame
from direct.gui.DirectGui import DirectButton
from panda3d.core import Vec3
import direct.directbase.DirectStart
 
class Formation():

    def __init__(self, path: str):
        (self.array, self.drones, self.name) = self._loadFormation(path)

    def _loadFormation(self, path: str) -> (np.array, int):
        drones = self._getRowCount(path)
        arr = np.loadtxt(path)
        arr = arr.reshape((drones, 3))    
        ntpath.basename("a/b/c")
        return (arr, drones, name)

    def _getRowCount(self, name):
        with open(path) as f:
            for i, _ in enumerate(f):
                pass
        return i + 1

    def getFormation(self):
        

def lul(bla):
    print(bla)

formations = []
directory = os.path.join(os.path.dirname(os.path.abspath(__file__)))
for file in os.listdir(directory):
    if file.endswith(".txt"):
        path = os.path.join(directory, file)
        formations.append(Formation._loadFormation(path))
        print("{} @ {}".format(file, path))

print(len(formations))
buttonSize = (-4, 4, -.2, .8)
buttonDistance = 0.15

scrolledFrame = DirectScrolledFrame(canvasSize = (-.4,.4,-buttonDistance*10,0), frameSize = (-.5,.5,-.5,.5)) 
scrolledFrame.setPos(0, 0, 0)
canvas = scrolledFrame.getCanvas()

for i in range(0, len(formations)):
    buttonRandomTargets = DirectButton(text = formations[i], scale=.1, frameSize=buttonSize, command=lul, extraArgs=["benis"])
    buttonRandomTargets.reparentTo(canvas)
    buttonRandomTargets.setPos(Vec3(0,0,-(i+.5)*buttonDistance))
 

run()