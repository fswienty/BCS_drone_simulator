import sys
import os
from math import pi, sin, cos
from direct.showbase.ShowBase import ShowBase
from drone import Drone
#from test import Test
from camera_controller import CameraController
# pylint: disable=no-name-in-module
from panda3d.core import Filename
from panda3d.core import DirectionalLight
from panda3d.core import AntialiasAttrib
from panda3d.core import Vec3
from panda3d.core import Vec4
from panda3d.bullet import BulletWorld
from panda3d.bullet import BulletPlaneShape
from panda3d.bullet import BulletBoxShape
from panda3d.bullet import BulletSphereShape
from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletDebugNode

class Main(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)

        self.setFrameRateMeter(True)
        self.accept('escape', sys.exit)
        self.isPaused = True
        self.accept('space', self.togglePause)
        self.render.setAntialias(AntialiasAttrib.MAuto)
        self.cameraController = CameraController(self)
        self.roomSize = Vec3(3.40, 4.56, 2.56) # the dimensions of the bcs drone lab in m
        # setup model directory
        self.modelDir = os.path.abspath(sys.path[0]) # Get the location of the 'py' file I'm running:
        self.modelDir = Filename.from_os_specific(self.modelDir).getFullpath() + "/models" # Convert that to panda's unix-style notation.
        # setup scene
        self.initBullet()
        self.spawnRoom()
        self.spawnLights()
        self.spawnDrones()


    def initBullet(self):
        self.world = BulletWorld()
        self.world.setGravity(Vec3(0, 0, 0))

        node = BulletRigidBodyNode("Ground") # derived from PandaNode
        node.addShape(BulletPlaneShape(Vec3(0, 0, 1), 0))
        np = self.render.attachNewNode(node)
        np.setPos(0, 0, 0)
        self.world.attachRigidBody(node)
        
        debugNode = BulletDebugNode("Debug")
        debugNode.showWireframe(True)
        debugNode.showConstraints(True)
        debugNode.showBoundingBoxes(False)
        debugNode.showNormals(True)
        debugNP = self.render.attachNewNode(debugNode)
        debugNP.show()
        self.world.setDebugNode(debugNP.node())


    def spawnDrones(self):
        self.drones = []
        self.drones.append(Drone(Vec3(0, 0, 4), self))
        self.drones.append(Drone(Vec3(2, 3, 2), self))
        self.drones.append(Drone(Vec3(4, 1, 1), self))
        self.drones.append(Drone(Vec3(2, 2, 1), self))
        self.drones.append(Drone(Vec3(1, 1, 1), self))
        self.drones.append(Drone(Vec3(0, 2, 1), self))


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


    def updateDronesTask(self, task):
        #print("##############")
        for drone in self.drones:
            drone.update()
        return task.cont


    def updatePhysicsTask(self, task):
        dt = self.taskMgr.globalClock.getDt()
        self.world.doPhysics(dt)
        return task.cont


    def togglePause(self):
        if self.isPaused == True:
            self.isPaused = False
            self.taskMgr.add(self.updateDronesTask, "UpdateDrones")
            self.taskMgr.add(self.updatePhysicsTask, "UpdatePhysics")
        else:
            self.isPaused = True
            self.taskMgr.remove("UpdateDrones")
            self.taskMgr.remove("UpdatePhysics")


app = Main()
app.run()