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
from panda3d.core import MouseButton
from panda3d.core import KeyboardButton
from panda3d.core import WindowProperties
from panda3d.core import VBase4
from panda3d.core import LVector3f
from panda3d.core import LVecBase3f
#from panda3d.core import CSDefault

class BcsTest(ShowBase):

    cameraControlActive = False

    def __init__(self):
        ShowBase.__init__(self)

        # setup model directory
        self.modelDir = os.path.abspath(sys.path[0]) # Get the location of the 'py' file I'm running:
        self.modelDir = Filename.from_os_specific(self.modelDir).getFullpath() + "/models" # Convert that to panda's unix-style notation.
        # setup scene
        self.addRoom()
        self.addLights()
        self.render.setAntialias(AntialiasAttrib.MAuto)

        # setup control scheme
        self.disableMouse()
        self.accept("t", self.toggleCameraControl)

        #self.messenger.toggleVerbose() # show all events # self is base

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
            dlnp.setHpr((120 * i) + 1, -30, 0)
            self.render.setLight(dlnp)
        dlight = DirectionalLight("light")
        dlight.setColor(VBase4(0.2, 0.2, 0.2, 0.2))
        dlnp = self.render.attachNewNode(dlight) # directional light node path
        dlnp.setHpr(1, 30, 0)
        self.render.setLight(dlnp)

    def toggleCameraControl(self):
        if self.cameraControlActive:
            self.cameraControlActive = False
            props = WindowProperties()
            props.setCursorHidden(False)
            self.win.requestProperties(props)
            self.taskMgr.remove("CameraControlTask")
        else:
            self.cameraControlActive = True
            props = WindowProperties()
            props.setCursorHidden(True)
            self.win.requestProperties(props)
            self.taskMgr.add(self.cameraControlTask, "CameraControlTask")

    def cameraControlTask(self, task):
        mw = self.mouseWatcherNode
        curPos = self.camera.getPos()
        curHpr = self.camera.getHpr()
        #forward = self.camera.getRelativeVector(self.render, LVecBase3f(0,0,1))
        forward = self.camera.getQuat().getForward()
        right = self.camera.getQuat().getRight()
        up = self.camera.getQuat().getUp()
        moveSpeed = .1
        rotSpeed = 20

        if mw.hasMouse():
            deltaX = rotSpeed * mw.getMouseX()
            deltaY = rotSpeed * mw.getMouseY()
            props = self.win.getProperties()
            self.win.movePointer(0, int(props.getXSize() / 2), int(props.getYSize() / 2))
            self.camera.setHpr(curHpr.getX() - deltaX, curHpr.getY() + deltaY, 0)

        deltaPos = LVector3f(0, 0, 0)
        if mw.isButtonDown(KeyboardButton.asciiKey(bytes('w','utf-8'))):
            deltaPos += forward * moveSpeed
        if mw.isButtonDown(KeyboardButton.asciiKey(bytes('s','utf-8'))):
            deltaPos -= forward * moveSpeed
        if mw.isButtonDown(KeyboardButton.asciiKey(bytes('d','utf-8'))):
            deltaPos += right * moveSpeed
        if mw.isButtonDown(KeyboardButton.asciiKey(bytes('a','utf-8'))):
            deltaPos -= right * moveSpeed
        if mw.isButtonDown(KeyboardButton.asciiKey(bytes('q','utf-8'))):
            deltaPos += up * moveSpeed
        if mw.isButtonDown(KeyboardButton.asciiKey(bytes('e','utf-8'))):
            deltaPos -= up * moveSpeed
        self.camera.setPos(curPos + deltaPos)

        return Task.cont
        
        


app = BcsTest()
app.run()