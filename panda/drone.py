import random
from random import uniform
# pylint: disable=no-name-in-module
from panda3d.core import Vec3
from panda3d.core import Loader
from panda3d.core import BitMask32
from panda3d.bullet import BulletSphereShape
from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletGhostNode

class Drone:

    def __init__(self, position: Vec3, base, printDebugInfo=False):
        self.base = base

        self.rigidBody = BulletRigidBodyNode("RigidSphere") # derived from PandaNode
        self.rigidBody.setMass(1.0) # body is now dynamic
        self.rigidBody.addShape(BulletSphereShape(0.1))
        self.rigidBody.setLinearSleepThreshold(0)
        self.rigidBody.setFriction(0)
        self.rigidBodyNP = base.render.attachNewNode(self.rigidBody)
        self.rigidBodyNP.setPos(position)
        self.rigidBodyNP.setCollideMask(BitMask32.bit(1))
        
        self.ghost = BulletGhostNode("GhostSphere")
        self.ghost.addShape(BulletSphereShape(0.3))
        self.ghostNP = base.render.attachNewNode(self.ghost)
        self.ghostNP.setPos(position)
        self.ghostNP.setCollideMask(BitMask32.bit(2))


        base.world.attach(self.rigidBody)
        base.world.attach(self.ghost)
        model = base.loader.loadModel(base.modelDir + "/drones/drone1.egg")
        model.setScale(0.3)
        model.reparentTo(self.rigidBodyNP)

        self.target = position
        self.rigidBody.setLinearDamping(0.8)

        self.printDebugInfo = printDebugInfo
        if self.printDebugInfo == True:
            model = base.loader.loadModel(base.modelDir + "/drones/drone1.egg")
            model.setPos(0, 0, .2)
            model.reparentTo(self.rigidBodyNP)


    def setTarget(self, target: Vec3 = Vec3(0, 0, 0), random=False):
        if random == False:
            self.target = target
        else:
            self.target = self._getRandomRoomCoordinate()
        

    def _getRandomRoomCoordinate(self) -> Vec3:
        newX = uniform(-self.base.roomSize.x/2, self.base.roomSize.x/2)
        newY = uniform(-self.base.roomSize.y/2, self.base.roomSize.y/2)
        newZ = uniform(0, self.base.roomSize.z)
        return Vec3(newX, newY, newZ)        


    def update(self):
        self._updateForce()
        self._updateGhost()
        self._checkCompletion()


    def _updateForce(self):
        dist = (self.target - self.rigidBodyNP.getPos())
        if(dist.lengthSquared() > 5**2):
            force = dist.normalized()
        else:
            force = dist / 5
        self.rigidBody.applyCentralForce(force * 5)


    def _updateGhost(self):
        self.ghostNP.setPos(self.rigidBodyNP.getPos())
        if self.printDebugInfo == True: 
            print(self.ghost.getNumOverlappingNodes())
            for node in self.ghost.getOverlappingNodes():
                print(node)


    def _checkCompletion(self):
        diff = self.getPos() - self.target
        if diff.lengthSquared() < 0.2**2:
            self.setTarget(random=True)

    
    def getPos(self) -> Vec3:
        return self.rigidBodyNP.getPos()

    def getVel(self) -> Vec3:
        return self.rigidBody.getLinearVelocity()