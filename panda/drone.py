# pylint: disable=no-name-in-module
from panda3d.core import Vec3
from main import Main
from panda3d.bullet import BulletSphereShape
from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletGhostNode


class Drone:

    def __init__(self, position: Vec3, base: Main):
        self.base = base

        self.target = position
        self.rigidBody = BulletRigidBodyNode("RigidSphere") # derived from PandaNode
        self.rigidBody.setMass(1.0) # type: BulletRigidBodyNode # body is now dynamic
        self.rigidBody.addShape(BulletSphereShape(0.3))
        self.ghost = BulletGhostNode("GhostSphere")
        self.rigidBodyNP = base.render.attachNewNode(self.rigidBody) # set pos on the nodepath
        self.rigidBodyNP.setPos(position)
        base.world.attachRigidBody(self.rigidBody)
        model = base.loader.loadModel(base.modelDir + "/drones/drone1.egg")
        model.reparentTo(self.rigidBodyNP)
        self.rigidBody.setLinearDamping(0.8)

    def setTarget(self, target: Vec3):
        self.target = target

    def updateForce(self):
        pass
    