import sys
import os

from camera_controller import CameraController
from drone_manager import DroneManager
from recorder import DroneRecorder

from direct.showbase.ShowBase import ShowBase
from panda3d.core import Filename
from panda3d.core import DirectionalLight
from panda3d.core import AntialiasAttrib
from panda3d.core import Vec3
from panda3d.core import Vec4
from panda3d.core import WindowProperties
from panda3d.bullet import BulletWorld
from panda3d.bullet import BulletPlaneShape
from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletDebugNode


class DroneSimulator(ShowBase):
    """The main class of this project. Execute this to start the drone simulation."""

    def __init__(self, droneList):
        ShowBase.__init__(self)

        # set resolution
        wp = WindowProperties()
        # wp.setSize(2000, 1500)
        wp.setSize(1200, 900)
        # wp.setSize(1000, 750)
        self.win.requestProperties(wp)

        self.setFrameRateMeter(True)
        self.render.setAntialias(AntialiasAttrib.MAuto)
        self.cameraController = CameraController(self)

        # setup model directory
        self.modelDir = os.path.abspath(sys.path[0])  # Get the location of the 'py' file I'm running:
        self.modelDir = Filename.from_os_specific(self.modelDir).getFullpath() + "/models"  # Convert that to panda's unix-style notation.

        self.initScene()
        self.initBullet()

        self.droneManager = DroneManager(self, droneList)
        self.droneRecorder = DroneRecorder(self.droneManager)


    def initScene(self):
        """Adds the room 3d model and some lights to the scene"""
        # add room
        roomModel = self.loader.loadModel(self.modelDir + "/room_test/room_test.egg")
        roomModel.reparentTo(self.render)

        # add lights
        for i in range(0, 3):
            dlight = DirectionalLight("light")
            dlnp = self.render.attachNewNode(dlight)  # directional light node path
            dlnp.setHpr((120 * i) + 1, -30, 0)
            self.render.setLight(dlnp)
        dlight = DirectionalLight("light")
        dlight.setColor(Vec4(0.2, 0.2, 0.2, 0.2))
        dlnp = self.render.attachNewNode(dlight)  # directional light node path
        dlnp.setHpr(1, 30, 0)
        self.render.setLight(dlnp)


    def initBullet(self):
        """Initializes the Bullet physics engine, also adds the updatePhysicsTask to the task manager."""
        self.world = BulletWorld()
        self.world.setGravity(Vec3(0, 0, 0))

        # add ground
        node = BulletRigidBodyNode("Ground")  # derived from PandaNode
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


    def updatePhysicsTask(self, task):
        dt = self.taskMgr.globalClock.getDt()
        self.world.doPhysics(dt)
        return task.cont


if __name__ == "__main__":
    # add drones you want to spawn to the droneList, with an initial position and a uri of real drone if applicable
    # if the drone should not be able to connect, put -1 as uri
    droneList = []
    droneList.append([Vec3(0, 0, .3), 'radio://0/80/2M/E7E7E7E7E0'])
    droneList.append([Vec3(1, 1, .3), 'radio://0/80/2M/E7E7E7E7E1'])
    droneList.append([Vec3(1, -1, .3), 'radio://0/80/2M/E7E7E7E7E2'])
    droneList.append([Vec3(-1, 1, .3), 'radio://0/80/2M/E7E7E7E7E3'])
    droneList.append([Vec3(-1, -1, .3), 'radio://0/80/2M/E7E7E7E7E4'])
    droneList.append([Vec3(.5, -1, .3), 'radio://0/80/2M/E7E7E7E7E5'])

    # droneList.append([Vec3(0, 0, .3), 'radio://0/80/2M/E7E7E7E7E0'])

    app = DroneSimulator(droneList)
    app.run()
