# pylint: disable=no-name-in-module
from direct.showbase import DirectObject
#from direct.task import Task
from panda3d.core import MouseButton
from panda3d.core import KeyboardButton
from panda3d.core import WindowProperties
from panda3d.core import Vec3

class CameraController(DirectObject.DirectObject):

    def __init__(self, base):
        self.base = base
        self.base.disableMouse()
        self.camera = base.camera
        self.cameraControlActive = False
        self.accept("t", self.toggleCameraControl)
        self.camera.setPos(0, -20, 3)


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
            windowSizeX = self.base.win.getProperties().getXSize()
            windowSizeY = self.base.win.getProperties().getYSize()
            self.base.taskMgr.add(self.cameraControlTask, "CameraControlTask", extraArgs=[windowSizeX, windowSizeY], appendTask=True)


    def cameraControlTask(self, windowSizeX, windowSizeY, task):        
        mw = self.base.mouseWatcherNode
        curPos = self.camera.getPos()
        curHpr = self.camera.getHpr()
        forward = self.camera.getQuat().getForward()
        right = self.camera.getQuat().getRight()
        up = self.camera.getQuat().getUp()
        moveSpeed = .1
        rotSpeed = 20

        if mw.hasMouse():
            #deltaX = rotSpeed * mw.getMouseX()
            #deltaY = rotSpeed * mw.getMouseY()
            deltaX = rotSpeed * (mw.getMouseX() + 2 * int(windowSizeX / 2) / windowSizeX - 1) # dont ask
            deltaY = rotSpeed * (mw.getMouseY() + 2 * int(windowSizeY / 2) / windowSizeY - 1)
            self.base.win.movePointer(0, int(windowSizeX / 2), int(windowSizeY / 2))
            self.camera.setHpr(curHpr.getX() - deltaX, curHpr.getY() + deltaY, 0)

        deltaPos = Vec3(0, 0, 0)
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
      
        return task.cont