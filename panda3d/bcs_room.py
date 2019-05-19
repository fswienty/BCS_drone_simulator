import sys,os
from math import pi, sin, cos
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
#from direct.actor.Actor import Actor
#from direct.interval.IntervalGlobal import Sequence
#from panda3d.core import Point3 # pylint: disable=no-name-in-module
from panda3d.core import Filename
from panda3d.core import DirectionalLight
from panda3d.core import AntialiasAttrib

class BcsTest(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)

        # setup model directory
        # Get the location of the 'py' file I'm running:
        self.modelDir = os.path.abspath(sys.path[0])
        # Convert that to panda's unix-style notation.
        self.modelDir = Filename.from_os_specific(self.modelDir).getFullpath() + "/models"

        self.addRoom()
        self.addLights()

        self.render.setAntialias(AntialiasAttrib.MAuto)

        
        #self.messenger.toggleVerbose() # show all events # self is base
        # Add the procedure to the task manager.
        #self.taskMgr.add(self.spinCameraTask, "SpinCameraTask")

    # Define a procedure to move the camera.
    def spinCameraTask(self, task):
        angleDegrees = task.time * 16.0
        angleRadians = angleDegrees * (pi / 180.0)
        self.camera.setPos(20 * sin(angleRadians), -20.0 * cos(angleRadians), 10)
        self.camera.setHpr(angleDegrees, -30, 0)
        return Task.cont

    def addRoom(self):
        self.roomModel = self.loader.loadModel(self.modelDir + "/room_test/room_test.egg")
        self.roomModel.reparentTo(self.render)

    def addLights(self):
        for i in range(0,3):
            dlight = DirectionalLight("light")
            dlnp = self.render.attachNewNode(dlight) # directional light node path
            dlnp.setHpr((120 * i)+1, -30, 0)
            self.render.setLight(dlnp)


app = BcsTest()
app.run()