import sys,os
from math import pi, sin, cos
from direct.showbase.ShowBase import ShowBase
# pylint: disable=no-name-in-module
from panda3d.core import Filename
from panda3d.core import DirectionalLight
from panda3d.core import AntialiasAttrib
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

        self.setFrameRateMeter(True)
        self.accept('escape', sys.exit)
        # setup model directory
        self.modelDir = os.path.abspath(sys.path[0]) # Get the location of the 'py' file I'm running:
        self.modelDir = Filename.from_os_specific(self.modelDir).getFullpath() + "/models" # Convert that to panda's unix-style notation.
        # setup scene
        self.initRoom()
        self.initLights()
        self.initBullet()
        self.render.setAntialias(AntialiasAttrib.MAuto)
        self.cameraController = CameraController(self)


    def initBullet(self):
        self.world = BulletWorld()
        self.world.setGravity(Vec3(0, 0, 0))

        node = BulletRigidBodyNode('Ground') # derived from PandaNode
        node.addShape(BulletPlaneShape(Vec3(0, 0, 1), 1))
        np = self.render.attachNewNode(node)
        np.setPos(0, 0, 0)
        self.world.attachRigidBody(node)

        self.physicsDrone = BulletRigidBodyNode('Sphere') # derived from PandaNode
        self.physicsDrone.setMass(1.0) # type: BulletRigidBodyNode # body is now dynamic
        self.physicsDrone.addShape(BulletSphereShape(0.3))
        self.physicsDroneNP = self.render.attachNewNode(self.physicsDrone)
        self.physicsDroneNP.setPos(0, 0, 4)
        self.world.attachRigidBody(self.physicsDrone)
        model = self.loader.loadModel(self.modelDir + "/drones/drone1.egg")
        model.reparentTo(self.physicsDroneNP)
        self.physicsDrone.applyCentralForce(Vec3(0, 0, -130))
        self.physicsDrone.setLinearDamping(0.8)   
        self.taskMgr.add(self.addForceToPointTask, "AddForceToPointTask", extraArgs=[self.physicsDrone], appendTask=True)

        debugNode = BulletDebugNode('Debug')
        debugNode.showWireframe(True)
        debugNode.showConstraints(True)
        debugNode.showBoundingBoxes(False)
        debugNode.showNormals(True)
        debugNP = self.render.attachNewNode(debugNode)
        debugNP.show()
        self.world.setDebugNode(debugNP.node())

        self.taskMgr.add(self.physicsUpdate, "PhysicsUpdate")
        

    def addForceToPointTask(self, pd, task):
        target = Vec3(2, -6, 2)
        pos = self.physicsDroneNP.getPos()
        dist = (target - pos)
        if(dist.lengthSquared() > 5**2):
            force = dist.normalized()
        else:
            force = dist / 5
        pd.applyCentralForce(force * 5)
        #rint(pos, force.length())
        return task.cont


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


app = Main()
app.run()