# pylint: disable=no-name-in-module
import sys,os
from direct.showbase.ShowBase import ShowBase
from panda3d.core import Filename
from panda3d.core import Vec3
from panda3d.bullet import BulletWorld
from panda3d.bullet import BulletPlaneShape
from panda3d.bullet import BulletBoxShape
from panda3d.bullet import BulletSphereShape
from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletDebugNode
from direct.showbase.DirectObject import DirectObject

class BulletTest(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)

        # setup model directory
        self.modelDir = os.path.abspath(sys.path[0]) # Get the location of the 'py' file I'm running:
        self.modelDir = Filename.from_os_specific(self.modelDir).getFullpath() + "/models" # Convert that to panda's unix-style notation.

        self.cam.setPos(0, -10, 0)
        self.cam.lookAt(0, 0, 0)
        

        debugNode = BulletDebugNode('Debug')
        debugNode.showWireframe(True)
        debugNode.showConstraints(True)
        debugNode.showBoundingBoxes(False)
        debugNode.showNormals(True)
        debugNP = self.render.attachNewNode(debugNode)
        debugNP.show()
        # world
        self.world = BulletWorld()
        self.world.setGravity(Vec3(0, 0, -9.81))
        self.world.setDebugNode(debugNP.node())

        # create and add ground
        shape = BulletPlaneShape(Vec3(0, 0, 1), 1)
        node = BulletRigidBodyNode('Ground') # derived from PandaNode
        node.addShape(shape)
        np = self.render.attachNewNode(node)
        np.setPos(0, 0, -2)
        self.world.attachRigidBody(node)

        # create and add a box
        shape = BulletBoxShape(Vec3(0.5, 0.5, 0.5))
        shape = BulletSphereShape(0.3)
        node = BulletRigidBodyNode('Box')
        node.setMass(1.0)
        node.addShape(shape)
        np = self.render.attachNewNode(node)
        np.setPos(0, 0, 2)
        self.world.attachRigidBody(node)
        model = self.loader.loadModel(self.modelDir + "/drones/drone1.egg")
        model.flattenLight()
        model.reparentTo(np)

        self.taskMgr.add(self.physicsUpdate, "PhysicsUpdate")


    def physicsUpdate(self, task):
        dt = self.taskMgr.globalClock.getDt()
        self.world.doPhysics(dt)
        return task.cont

app = BulletTest()
app.run()