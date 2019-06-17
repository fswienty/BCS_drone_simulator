import sys
import os
import time
from direct.showbase.ShowBase import ShowBase
from camera_controller import CameraController
from drone_manager import DroneManager
from recorder import DroneRecorder
# pylint: disable=no-name-in-module
from panda3d.core import Filename
from panda3d.core import DirectionalLight
from panda3d.core import AntialiasAttrib
from panda3d.core import Vec3
from panda3d.core import Vec4
from panda3d.core import WindowProperties
from panda3d.bullet import BulletWorld
from panda3d.bullet import BulletPlaneShape
from panda3d.bullet import BulletBoxShape
from panda3d.bullet import BulletSphereShape
from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletDebugNode

class DroneSimulator(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)

        # set resolution
        wp = WindowProperties()
        wp.setSize(1600, 1200)
        self.win.requestProperties(wp)

        self.setFrameRateMeter(True)
        # self.accept('escape', self.endApplication)
        self.isPaused = False
        #self.accept('space', self.togglePause)
        self.render.setAntialias(AntialiasAttrib.MAuto)
        self.cameraController = CameraController(self)
        
        # setup model directory
        self.modelDir = os.path.abspath(sys.path[0]) # Get the location of the 'py' file I'm running:
        self.modelDir = Filename.from_os_specific(self.modelDir).getFullpath() + "/models" # Convert that to panda's unix-style notation.

        # setup scene
        self.initBullet()
        self.spawnRoom()
        self.spawnLights()

        self.droneManager = DroneManager(self)
        self.droneRecorder = DroneRecorder(self.droneManager)
        self.accept('m', self.droneRecorder.save)


    def initBullet(self):
        self.world = BulletWorld()
        self.world.setGravity(Vec3(0, 0, 0))

        # add ground
        node = BulletRigidBodyNode("Ground") # derived from PandaNode
        node.addShape(BulletPlaneShape(Vec3(0, 0, 1), 0))
        np = self.render.attachNewNode(node)
        np.setPos(0, 0, 0)
        self.world.attachRigidBody(node)
        
        # add debug node
        debugNode = BulletDebugNode("Debug")
        debugNode.showWireframe(False)
        debugNode.showConstraints(True)
        debugNode.showBoundingBoxes(False)
        debugNode.showNormals(True)
        debugNP = self.render.attachNewNode(debugNode)
        debugNP.show()
        self.world.setDebugNode(debugNP.node())

        self.taskMgr.add(self.updatePhysicsTask, "UpdatePhysics")
        

    def spawnRoom(self):
        # room size: x=3.40m y=4.56m z=2.56m 
        roomModel = self.loader.loadModel(self.modelDir + "/room_test/room_test.egg")
        roomModel.reparentTo(self.render)


    def spawnLights(self):
        for i in range(0,3):
            dlight = DirectionalLight("light")
            dlnp = self.render.attachNewNode(dlight) # directional light node path
            dlnp.setHpr((120 * i) + 1, -30, 0)
            self.render.setLight(dlnp)
        dlight = DirectionalLight("light")
        dlight.setColor(Vec4(0.2, 0.2, 0.2, 0.2))
        dlnp = self.render.attachNewNode(dlight) # directional light node path
        dlnp.setHpr(1, 30, 0)
        self.render.setLight(dlnp)


    def updatePhysicsTask(self, task):
        dt = self.taskMgr.globalClock.getDt()
        self.world.doPhysics(dt)
        return task.cont


    def togglePause(self):
        if self.isPaused == True:
            self.isPaused = False
            # self.taskMgr.add(self.droneManager.updateDronesTask, "UpdateDrones")
            self.taskMgr.doMethodLater(0, self.droneRecorder.recordDronesTask, "RecordDrones")
            # self.taskMgr.add(self.updatePhysicsTask, "UpdatePhysics")
        else:
            self.isPaused = True
            # self.taskMgr.remove("UpdateDrones")
            self.taskMgr.remove("RecordDrones")
            # self.taskMgr.remove("UpdatePhysics")


    def endApplication(self):
        print("ending application")
        self.taskMgr.removeTasksMatching("*")
        self.destroy()
        sys.exit()

if __name__ == "__main__":
    app = DroneSimulator()
    app.run()