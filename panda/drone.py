import random
import re
# pylint: disable=no-name-in-module
from panda3d.core import Vec3
from panda3d.core import Loader
from panda3d.core import BitMask32
from panda3d.core import LineSegs
from panda3d.bullet import BulletSphereShape
from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletGhostNode

class Drone:

    RIGIDBODYMASS = 1.0
    RIGIDBODYRADIUS = 0.1
    GHOSTRADIUS = 0.5

    MAXFORCE = .5
    FORCEFALLOFFDISTANCE = .5
    LINEARDAMPING = 0.9

    def __init__(self, manager, name: str, position: Vec3, printDebugInfo=False):
        self.name = name
        self.base = manager.base
        self.manager = manager

        # add the rigidbody to the drone, which has a mass and linear damping
        self.rigidBody = BulletRigidBodyNode("RigidSphere") # derived from PandaNode
        self.rigidBody.setMass(self.RIGIDBODYMASS) # body is now dynamic
        self.rigidBody.addShape(BulletSphereShape(self.RIGIDBODYRADIUS))
        self.rigidBody.setLinearSleepThreshold(0)
        self.rigidBody.setFriction(0)
        self.rigidBody.setLinearDamping(self.LINEARDAMPING)
        self.rigidBodyNP = self.base.render.attachNewNode(self.rigidBody)
        self.rigidBodyNP.setPos(position)
        self.rigidBodyNP.setCollideMask(BitMask32.bit(1))

        # add the ghost to the drone which acts as a sensor for nearby drones
        self.ghost = BulletGhostNode(self.name) # give drone the same identifier that the drone has in the dict
        self.ghost.addShape(BulletSphereShape(self.GHOSTRADIUS))
        self.ghostNP = self.base.render.attachNewNode(self.ghost)
        self.ghostNP.setPos(position)
        self.ghostNP.setCollideMask(BitMask32.bit(2))

        # add a 3d model to the drone to be able to see it in the 3d scene
        self.base.world.attach(self.rigidBody)
        self.base.world.attach(self.ghost)
        model = self.base.loader.loadModel(self.base.modelDir + "/drones/drone1.egg")
        model.setScale(0.3)
        model.reparentTo(self.rigidBodyNP)

        self.target = position
        

        self.printDebugInfo = printDebugInfo
        if self.printDebugInfo == True: # put a second drone model on top of drone that outputs debug stuff
            model = self.base.loader.loadModel(self.base.modelDir + "/drones/drone1.egg")
            model.setPos(0, 0, .2)
            model.reparentTo(self.rigidBodyNP)

        # initialize line renderers
        self.targetLineNP = self.base.render.attachNewNode(LineSegs().create())
        self.velocityLineNP = self.base.render.attachNewNode(LineSegs().create())


    def update(self):
        self._updateForce()
        self._updateGhost()
        self._checkCompletion()
        self._handleCollisions()

        self._printDebugInfo()
        self._drawTargetLine()
        self._drawVelocityLine()


    def _updateForce(self):
        dist = (self.target - self.getPos())
        if(dist.length() > self.FORCEFALLOFFDISTANCE):
            force = dist.normalized() * self.MAXFORCE
        else:
            force = dist * self.MAXFORCE / self.FORCEFALLOFFDISTANCE
        velMult = self.getVel().length() + .1
        velMult = velMult
        self._addForce(force * 3)


    def _updateGhost(self):
        self.ghostNP.setPos(self.getPos())


    def _handleCollisions(self):
        for node in self.ghost.getOverlappingNodes():
            if node.name.startswith("drone"):
                other = self.manager.getDrone(node.name)
                
                dist = other.getPos() - self.getPos()
                if dist.length() < 0.3:
                    print("BONK")
                distMult = max([0, 2 * self.GHOSTRADIUS - dist.length()])
                distMult = distMult**2
                # velMult = other.getVel().length() + self.getVel().length() + 1
                velMult = self.getVel().length()
                velMult = velMult**2 + 1
                self._addForce(-dist.normalized() * distMult * velMult * 5)


    def _checkCompletion(self):
        diff = self.getPos() - self.target
        if diff.length() < 0.2:
            self.setTarget(random=True)


    def _printDebugInfo(self):
        if self.printDebugInfo == True: 
            print("Drone", self.name, " Amount of overlapping nodes: ", self.ghost.getNumOverlappingNodes())
            for node in self.ghost.getOverlappingNodes():
                print(node)


    def setTarget(self, target: Vec3 = Vec3(0, 0, 0), random=False):
        if random == False:
            self.target = target
        else:
            self.target = self.manager.getRandomRoomCoordinate()
    

    def _addForce(self, force: Vec3):
        self.rigidBody.applyCentralForce(force)

    
    def getPos(self) -> Vec3:
        return self.rigidBodyNP.getPos()


    def getVel(self) -> Vec3:
        return self.rigidBody.getLinearVelocity()


    def _drawTargetLine(self):
        self.targetLineNP.removeNode()
        ls = LineSegs()
        #ls.setThickness(1)
        ls.setColor(1.0, 0.0, 0.0, 1.0)
        ls.moveTo(self.getPos())
        ls.drawTo(self.target)
        node = ls.create()
        self.targetLineNP = self.base.render.attachNewNode(node)

    
    def _drawVelocityLine(self):
        self.velocityLineNP.removeNode()
        ls = LineSegs()
        #ls.setThickness(1)
        ls.setColor(0.0, 0.0, 1.0, 1.0)
        ls.moveTo(self.getPos())
        ls.drawTo(self.getPos() + self.getVel())
        node = ls.create()
        self.velocityLineNP = self.base.render.attachNewNode(node)        
