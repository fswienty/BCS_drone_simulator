import os
import numpy as np
import ntpath

# pylint: disable=no-name-in-module
from panda3d.core import Vec3
from direct.gui.DirectGui import DirectScrolledFrame
from direct.gui.DirectGui import DirectButton

class FormationUiElement:

    def __init__(self, manager):
        self.manager = manager
        self.formations = [] # a list of formations, which are lists consisting of the name, the amount of drones, and the positions as a numpy array

        directory = os.path.dirname(os.path.abspath(__file__))
        for file in os.listdir(directory):
            if file.endswith(".txt"):
                path = os.path.join(directory, file)
                self.formations.append(self.loadFormation(path))

        buttonSize = (-8, 8, -.2, .8)
        buttonDistance = 0.15

        scrolledFrame = DirectScrolledFrame(frameColor=(.2, .2, .2, 1), canvasSize = (-.7,.7,-buttonDistance * len(self.formations),0), frameSize = (-.9,.9,-.5,.5), pos=(.8, 0, -.7), scale=.5) 
        #scrolledFrame.setPos(.5, .5, 0)
        canvas = scrolledFrame.getCanvas()

        for i in range(0, len(self.formations)):
            buttonRandomTargets = DirectButton(text = self.formations[i][0], scale=.1, frameSize=buttonSize, command=manager.applyFormation, extraArgs=[self.formations[i]])
            buttonRandomTargets.reparentTo(canvas)
            buttonRandomTargets.setPos(Vec3(0.15, 0, -(i + 0.75) * buttonDistance))

        print("{} formations found and loaded.".format(len(self.formations)))

    def loadFormation(self, path: str) -> (np.array, int):
        name = ntpath.basename(path)
        name = os.path.splitext(name)[0]
        drones = self._getRowCount(path)
        #arr = np.loadtxt(path, delimiter=",")
        arr = np.loadtxt(path)
        arr = arr.reshape((drones, 3))
        print(name)
        return [name, arr]

    def _getRowCount(self, path):
        with open(path) as f:
            for i, _ in enumerate(f):
                pass
        return i + 1

    def dummy(self):
        print("dummymethod")