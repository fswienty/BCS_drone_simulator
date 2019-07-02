import os
import ntpath
import numpy as np

from direct.gui.DirectGui import DirectScrolledFrame
from direct.gui.DirectGui import DirectButton


def loadFormationSelectionFrame(manager):
    """Loads all formations files in the same directory as this .py file and builds a UI element with buttons for each formation.
        Formations are .csv files where the nth line is the position of the nth drone."""
    manager = manager

    formations = []  # a list of formations, which are lists consisting of the name and the positions as a numpy array
    # load all .txt files in the formations folder
    directory = os.path.dirname(os.path.abspath(__file__))  # the directory this.py file is in, which also contains the formation files
    for file in os.listdir(directory):
        if file.endswith(".csv"):
            path = os.path.join(directory, file)
            formations.append(_loadFormation(path))

    # size and position of the buttons and the scrollable frame
    buttonSize = (-8, 8, -.2, .8)
    buttonDistance = 0.15
    scrolledFrame = DirectScrolledFrame(
        frameColor=(.2, .2, .2, 1),
        canvasSize=(-.7, .7, -buttonDistance * len(formations), 0),
        frameSize=(-.9, .9, -.5, .5),
        pos=(.8, 0, -.7),
        scale=.5
    )
    canvas = scrolledFrame.getCanvas()

    # add a button for each formation
    for i in range(0, len(formations)):
        button = DirectButton(text=formations[i][0], scale=.1, frameSize=buttonSize, command=manager.applyFormation, extraArgs=[formations[i]])
        button.reparentTo(canvas)
        button.setPos(0.15, 0, -(i + 0.75) * buttonDistance)

    print("{} formations found and loaded.".format(len(formations)))


def _loadFormation(path: str) -> (np.array, int):
    """Loads the formation file at the specified path and returns a list containing its name and the drone positions as a numpy array"""
    name = ntpath.basename(path)
    name = os.path.splitext(name)[0]
    drones = _getRowCount(path)
    arr = np.loadtxt(path, delimiter=",")
    arr = arr.reshape((drones, 3))
    return [name, arr]


def _getRowCount(path):
    with open(path) as f:
        for i, _ in enumerate(f):
            pass
    return i + 1
