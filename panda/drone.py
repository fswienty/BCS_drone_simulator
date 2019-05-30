import random
# pylint: disable=no-name-in-module
from panda3d.core import Vec3
from panda3d.core import Loader
from panda3d.core import BitMask32
from panda3d.bullet import BulletSphereShape
from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletGhostNode

class Drone:

    MASS = 1.0
    RIGIDBODYRADIUS = 0.1
    GHOSTRADIUS = 0.5
    LINEARDAMPING = 0.8

    def __init__(self, name: str, position: Vec3, manager, printDebugInfo=False):
        self.name = name
        self.base = manager.base
        self.manager = manager

        self.rigidBody = BulletRigidBodyNode("RigidSphere") # derived from PandaNode
        self.rigidBody.setMass(self.MASS) # body is now dynamic
        self.rigidBody.addShape(BulletSphereShape(self.RIGIDBODYRADIUS))
        self.rigidBody.setLinearSleepThreshold(0)
        self.rigidBody.setFriction(0)
        self.rigidBodyNP = self.base.render.attachNewNode(self.rigidBody)
        self.rigidBodyNP.setPos(position)
        self.rigidBodyNP.setCollideMask(BitMask32.bit(1))

        self.ghost = BulletGhostNode(self.name) # give drone the same identifier as the drone has in the dict
        self.ghost.addShape(BulletSphereShape(self.GHOSTRADIUS))
        self.ghostNP = self.base.render.attachNewNode(self.ghost)
        self.ghostNP.setPos(position)
        self.ghostNP.setCollideMask(BitMask32.bit(2))

        self.base.world.attach(self.rigidBody)
        self.base.world.attach(self.ghost)
        model = self.base.loader.loadModel(self.base.modelDir + "/drones/drone1.egg")
        model.setScale(0.3)
        model.reparentTo(self.rigidBodyNP)

        self.target = position
        self.rigidBody.setLinearDamping(self.LINEARDAMPING)

        self.printDebugInfo = printDebugInfo
        if self.printDebugInfo == True: # put a second drone model on top of drone that outputs debug stuff
            model = self.base.loader.loadModel(self.base.modelDir + "/drones/drone1.egg")
            model.setPos(0, 0, .2)
            model.reparentTo(self.rigidBodyNP)


    def update(self):
        self._updateForce()
        self._updateGhost()
        self._checkCompletion()
        self._handleCollisions()

        self._printDebugInfo()


    def _updateForce(self):
        dist = (self.target - self.getPos())
        if(dist.length() > 5):
            force = dist.normalized()
        else:
            force = dist / 5
        self.addForce(force * 5)


    def _updateGhost(self):
        self.ghostNP.setPos(self.getPos())


    def _handleCollisions(self):
        for node in self.ghost.getOverlappingNodes():
            other = self.manager.getDrone(node.name)
            
            direction = other.getPos() - self.getPos()
            mult = max([0, 2 * self.GHOSTRADIUS - direction.length()])
            other.addForce(direction.normalized() * mult * 5)


    def _checkCompletion(self):
        diff = self.getPos() - self.target
        if diff.length() < 0.2:
            self.setTarget(random=True)


    def _printDebugInfo(self):
        if self.printDebugInfo == True: 
            print("Drone", self.name, " Amount of overlapping nodes: ", self.ghost.getNumOverlappingNodes())
            for node in self.ghost.getOverlappingNodes():
                other = self.manager.getDrone(node.name)
                direction = other.getPos() - self.getPos()
                mult = max([0, 2 * self.GHOSTRADIUS - direction.length()])
                force = direction.normalized() * mult * 20


    def setTarget(self, target: Vec3 = Vec3(0, 0, 0), random=False):
        if random == False:
            self.target = target
        else:
            self.target = self.manager.getRandomRoomCoordinate()
    

    def addForce(self, force: Vec3):
        self.rigidBody.applyCentralForce(force)

    
    def getPos(self) -> Vec3:
        return self.rigidBodyNP.getPos()

    def getVel(self) -> Vec3:
        return self.rigidBody.getLinearVelocity()