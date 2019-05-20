import sys,os
from math import pi, sin, cos
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
#from direct.actor.Actor import Actor
#from direct.interval.IntervalGlobal import Sequence
#from panda3d.core import Point3 
# pylint: disable=no-name-in-module
from panda3d.core import Filename
from panda3d.core import DirectionalLight
from panda3d.core import AntialiasAttrib
from panda3d.core import MouseButton
from panda3d.core import KeyboardButton
from panda3d.core import WindowProperties
from panda3d.core import VBase4
from panda3d.core import LVector3f
from panda3d.core import LVecBase3f
from camera_controller import CameraController

class Main(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)

        # setup model directory
        self.modelDir = os.path.abspath(sys.path[0]) # Get the location of the 'py' file I'm running:
        self.modelDir = Filename.from_os_specific(self.modelDir).getFullpath() + "/models" # Convert that to panda's unix-style notation.
        # setup scene
        self.addRoom()
        self.addLights()
        self.render.setAntialias(AntialiasAttrib.MAuto)
        self.cameraController = CameraController(self)

        #add some drones
        self.drone = self.loader.loadModel(self.modelDir + "/drones/drone1.egg")
        self.drone.reparentTo(self.render)

        #self.messenger.toggleVerbose() # show all events # self is base
        self.taskMgr.add(self.spinDroneTask, "SpinDroneTask")


    def addRoom(self):
        self.roomModel = self.loader.loadModel(self.modelDir + "/room_test/room_test.egg")
        self.roomModel.reparentTo(self.render)


    def addLights(self):
        for i in range(0,3):
            dlight = DirectionalLight("light")
            dlnp = self.render.attachNewNode(dlight) # directional light node path
            dlnp.setHpr((120 * i) + 1, -30, 0)
            self.render.setLight(dlnp)
        dlight = DirectionalLight("light")
        dlight.setColor(VBase4(0.2, 0.2, 0.2, 0.2))
        dlnp = self.render.attachNewNode(dlight) # directional light node path
        dlnp.setHpr(1, 30, 0)
        self.render.setLight(dlnp)


    # Define a procedure to move the drone.
    def spinDroneTask(self, task):
        angleDegrees = task.time * 100.0
        angleRadians = angleDegrees * (pi / 180.0)
        self.drone.setPos(2 * sin(angleRadians), -2.0 * cos(angleRadians), 1)
        self.drone.setHpr(angleDegrees, -30, 0)
        return Task.cont 
        
app = Main()
app.run()