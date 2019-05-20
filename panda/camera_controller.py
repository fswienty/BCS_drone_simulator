# pylint: disable=no-name-in-module
from direct.showbase import DirectObject
from direct.task import Task
from panda3d.core import MouseButton
from panda3d.core import KeyboardButton
from panda3d.core import WindowProperties
from panda3d.core import LVector3f

class CameraController(DirectObject.DirectObject):

    def __init__(self, base):
        self.base = base
        self.base.disableMouse()
        self.camera = base.camera
        self.cameraControlActive = False
        self.accept("t", self.toggleCameraControl)

        self.camera.setPos(0, -20, 2)
        self.windowSizeX = self.base.win.getProperties().getXSize()
        self.windowSizeY = self.base.win.getProperties().getYSize()


    def toggleCameraControl(self):
        props = WindowProperties()
        if self.cameraControlActive:
            self.cameraControlActive = False
            props.setCursorHidden(False)
            self.base.win.requestProperties(props)
            self.base.taskMgr.remove("CameraControlTask")
        else:
            self.cameraControlActive = True
            props.setCursorHidden(True)
            self.base.win.requestProperties(props)
            self.base.taskMgr.add(self.cameraControlTask, "CameraControlTask")

    # fix me
    def cameraControlTask(self, task):
        self.windowSizeX = self.base.win.getProperties().getXSize()
        self.windowSizeY = self.base.win.getProperties().getYSize()
        #self.windowSizeX -= self.windowSizeX % 2
        #self.windowSizeY -= self.windowSizeY % 2
        
        mw = self.base.mouseWatcherNode
        curPos = self.camera.getPos()
        curHpr = self.camera.getHpr()
        forward = self.camera.getQuat().getForward()
        right = self.camera.getQuat().getRight()
        up = self.camera.getQuat().getUp()
        moveSpeed = .1
        rotSpeed = 20

        if mw.hasMouse():
            deltaX = rotSpeed * mw.getMouseX()
            deltaY = rotSpeed * mw.getMouseY()
            self.base.win.movePointer(0, int(self.windowSizeX / 2), int(self.windowSizeY / 2)) # window size has to be a multiple of 2 or this causes trouble
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
        if mw.isButtonDown(KeyboardButton.asciiKey(bytes('e','utf-8'))):
            deltaPos += up * moveSpeed
        if mw.isButtonDown(KeyboardButton.asciiKey(bytes('q','utf-8'))):
            deltaPos -= up * moveSpeed
        self.camera.setPos(curPos + deltaPos)

        return Task.cont