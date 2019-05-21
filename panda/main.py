import sys,os
from math import pi, sin, cos
from direct.showbase.ShowBase import ShowBase
#from direct.actor.Actor import Actor
#from direct.interval.IntervalGlobal import Sequence
#from panda3d.core import Point3 
# pylint: disable=no-name-in-module
from panda3d.core import Filename
from panda3d.core import DirectionalLight
from panda3d.core import AntialiasAttrib
#from panda3d.core import MouseButton
#from panda3d.core import KeyboardButton
#from panda3d.core import WindowProperties
from panda3d.core import Vec3
from panda3d.core import Vec4
from camera_controller import CameraController
from panda3d.bullet import BulletWorld
from panda3d.bullet import BulletPlaneShape
from panda3d.bullet import BulletBoxShape
from panda3d.bullet import BulletSphereShape
from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletDebugNode

class Main(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)

        # setup model directory
        self.modelDir = os.path.abspath(sys.path[0]) # Get the location of the 'py' file I'm running:
        self.modelDir = Filename.from_os_specific(self.modelDir).getFullpath() + "/models" # Convert that to panda's unix-style notation.
        # setup scene
        self.initRoom()
        self.initLights()
        self.initBullet()
        self.render.setAntialias(AntialiasAttrib.MAuto)
        self.cameraController = CameraController(self)

        #add some drones
        drone = self.loader.loadModel(self.modelDir + "/drones/drone1.egg")
        drone.reparentTo(self.render)

        self.physicsDrone = None

        #self.messenger.toggleVerbose() # show all events # self is base
        self.taskMgr.add(self.spinDroneTask, "SpinDroneTask", extraArgs=[drone], appendTask=True)


    def initBullet(self):
        self.world = BulletWorld()
        self.world.setGravity(Vec3(0, 0, -9.81))

        shape = BulletPlaneShape(Vec3(0, 0, 1), 1)
        node = BulletRigidBodyNode('Ground') # derived from PandaNode
        node.addShape(shape)
        np = self.render.attachNewNode(node)
        np.setPos(0, 0, 0)
        self.world.attachRigidBody(node)

        shape = BulletSphereShape(0.3)
        node = BulletRigidBodyNode('Sphere')
        node.setMass(1.0)
        node.addShape(shape)
        self.physicsDrone = self.render.attachNewNode(node)
        self.physicsDrone.setPos(0, 0, 2)
        self.world.attachRigidBody(node)
        model = self.loader.loadModel(self.modelDir + "/drones/drone1.egg")
        model.flattenLight()
        model.reparentTo(np)

        debugNode = BulletDebugNode('Debug')
        debugNode.showWireframe(True)
        debugNode.showConstraints(True)
        debugNode.showBoundingBoxes(False)
        debugNode.showNormals(True)
        debugNP = self.render.attachNewNode(debugNode)
        debugNP.show()
        self.world.setDebugNode(debugNP.node())

        self.taskMgr.add(self.physicsUpdate, "PhysicsUpdate")


    def physicsUpdate(self, task):
        dt = self.taskMgr.globalClock.getDt()
        self.world.doPhysics(dt)
        return task.cont


    def initRoom(self):
        self.roomModel = self.loader.loadModel(self.modelDir + "/room_test/room_test.egg")
        self.roomModel.setPos(0, 0, 1)
        self.roomModel.reparentTo(self.render)


    def initLights(self):
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
        

    # Define a procedure to move the drone.
    def spinDroneTask(self, drone, task):
        angleDegrees = task.time * 100.0
        angleRadians = angleDegrees * (pi / 180.0)
        drone.setPos(2 * sin(angleRadians), -2.0 * cos(angleRadians), 1)
        drone.setHpr(angleDegrees, -30, 0)
        return task.cont 
        

app = Main()
app.run()