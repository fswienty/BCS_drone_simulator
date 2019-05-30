import random
# pylint: disable=no-name-in-module
from panda3d.core import Vec3
from panda3d.core import Loader
from panda3d.core import BitMask32
from panda3d.bullet import BulletSphereShape
from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletGhostNode

class Drone:

    def __init__(self, name: str, position: Vec3, manager, printDebugInfo=False):
        self.name = name
        self.base = manager.base
        self.manager = manager

        self.rigidBody = BulletRigidBodyNode("RigidSphere") # derived from PandaNode
        self.rigidBody.setMass(1.0) # body is now dynamic
        self.rigidBody.addShape(BulletSphereShape(0.1))
        self.rigidBody.setLinearSleepThreshold(0)
        self.rigidBody.setFriction(0)
        self.rigidBodyNP = self.base.render.attachNewNode(self.rigidBody)
        self.rigidBodyNP.setPos(position)
        self.rigidBodyNP.setCollideMask(BitMask32.bit(1))

        self.ghost = BulletGhostNode(self.name) # give drone the same identifier as the drone has in the dict
        self.ghost.addShape(BulletSphereShape(0.5))
        self.ghostNP = self.base.render.attachNewNode(self.ghost)
        self.ghostNP.setPos(position)
        self.ghostNP.setCollideMask(BitMask32.bit(2))

        self.ghost.ls


        self.base.world.attach(self.rigidBody)
        self.base.world.attach(self.ghost)
        model = self.base.loader.loadModel(self.base.modelDir + "/drones/drone1.egg")
        model.setScale(0.3)
        model.reparentTo(self.rigidBodyNP)

        self.target = position
        self.rigidBody.setLinearDamping(0.8)

        self.printDebugInfo = printDebugInfo
        if self.printDebugInfo == True: # put a second drone model on top of drone that outputs debug stuff
            model = self.base.loader.loadModel(self.base.modelDir + "/drones/drone1.egg")
            model.setPos(0, 0, .2)
            model.reparentTo(self.rigidBodyNP)


    def setTarget(self, target: Vec3 = Vec3(0, 0, 0), random=False):
        if random == False:
            self.target = target
        else:
            self.target = self.manager.getRandomRoomCoordinate()
        

    def update(self):
        self._updateForce()
        self._updateGhost()
        self._checkCompletion()


    def _updateForce(self):
        dist = (self.target - self.getPos())
        if(dist.length() > 5):
            force = dist.normalized()
        else:
            force = dist / 5
        self.rigidBody.applyCentralForce(force * 5)


    def addForce(self, force: Vec3):
        self.rigidBody.applyCentralForce(force)


    def _updateGhost(self):
        self.ghostNP.setPos(self.rigidBodyNP.getPos())
        if self.printDebugInfo == True: 
            print("Drone", self.name, " Amount of overlapping nodes: ", self.ghost.getNumOverlappingNodes())
            for node in self.ghost.getOverlappingNodes():
                print(node.name)
                self.manager.getDrone(node.name).addForce(Vec3(0,0,10))


    def _checkCompletion(self):
        diff = self.getPos() - self.target
        if diff.length() < 0.2:
            self.setTarget(random=True)

    
    def getPos(self) -> Vec3:
        return self.rigidBodyNP.getPos()

    def getVel(self) -> Vec3:
        return self.rigidBody.getLinearVelocity()