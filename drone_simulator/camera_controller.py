from direct.showbase import DirectObject
from panda3d.core import KeyboardButton
from panda3d.core import WindowProperties
from panda3d.core import Vec3


class CameraController(DirectObject.DirectObject):

    def __init__(self, base):
        self.base = base
        self.base.disableMouse()
        self.camera = base.camera
        self.cameraControlActive = False
        self.accept("mouse3", self.activateCameraControl)
        self.accept("mouse3-up", self.deactivateCameraControl)
        self.camera.setPos(-5, 0, 2)
        self.camera.lookAt(0, 0, 1)
        base.camLens.setFov(90)
        base.camLens.setNear(.1)


    # def toggleCameraControl(self):
    #     props = WindowProperties()
    #     if self.cameraControlActive:
    #         self.cameraControlActive = False
    #         props.setCursorHidden(False)
    #         self.base.win.requestProperties(props)
    #         self.base.taskMgr.remove("CameraControlTask")
    #     else:
    #         self.cameraControlActive = True
    #         props.setCursorHidden(True)
    #         self.base.win.requestProperties(props)
    #         windowSizeX = self.base.win.getProperties().getXSize()
    #         windowSizeY = self.base.win.getProperties().getYSize()
    #         self.base.taskMgr.add(self.cameraControlTask, "CameraControlTask", extraArgs=[windowSizeX, windowSizeY], appendTask=True)


    def activateCameraControl(self):
        props = WindowProperties()
        self.cameraControlActive = True
        props.setCursorHidden(True)
        self.base.win.requestProperties(props)
        windowSizeX = self.base.win.getProperties().getXSize()
        windowSizeY = self.base.win.getProperties().getYSize()
        self.base.taskMgr.add(self.cameraControlTask, "CameraControlTask", extraArgs=[windowSizeX, windowSizeY], appendTask=True)


    def deactivateCameraControl(self):
        props = WindowProperties()
        self.cameraControlActive = False
        props.setCursorHidden(False)
        self.base.win.requestProperties(props)
        self.base.taskMgr.remove("CameraControlTask")



    def cameraControlTask(self, windowSizeX, windowSizeY, task):
        mw = self.base.mouseWatcherNode
        curPos = self.camera.getPos()
        curHpr = self.camera.getHpr()
        forward = self.camera.getQuat().getForward()
        right = self.camera.getQuat().getRight()
        up = self.camera.getQuat().getUp()
        moveSpeed = .05
        rotSpeed = 20

        if mw.hasMouse():
            deltaX = rotSpeed * (mw.getMouseX() + 2 * int(windowSizeX / 2) / windowSizeX - 1)  # don't ask
            deltaY = rotSpeed * (mw.getMouseY() + 2 * int(windowSizeY / 2) / windowSizeY - 1)
            self.base.win.movePointer(0, int(windowSizeX / 2), int(windowSizeY / 2))
            self.camera.setHpr(curHpr.getX() - deltaX, curHpr.getY() + deltaY, 0)

        deltaPos = Vec3(0, 0, 0)
        if mw.isButtonDown(KeyboardButton.asciiKey(bytes('w', 'utf-8'))):
            deltaPos += forward
        if mw.isButtonDown(KeyboardButton.asciiKey(bytes('s', 'utf-8'))):
            deltaPos -= forward
        if mw.isButtonDown(KeyboardButton.asciiKey(bytes('d', 'utf-8'))):
            deltaPos += right
        if mw.isButtonDown(KeyboardButton.asciiKey(bytes('a', 'utf-8'))):
            deltaPos -= right
        if mw.isButtonDown(KeyboardButton.asciiKey(bytes('e', 'utf-8'))):
            deltaPos += up
        if mw.isButtonDown(KeyboardButton.asciiKey(bytes('q', 'utf-8'))):
            deltaPos -= up
        deltaPos.normalize()
        deltaPos *= moveSpeed
        self.camera.setPos(curPos + deltaPos)

        return task.cont
