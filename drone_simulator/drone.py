import random
import re
import time

import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.log import LogConfig
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.crazyflie.syncLogger import SyncLogger
from cflib.crazyflie.commander import Commander

# pylint: disable=no-name-in-module
from panda3d.core import Vec3
from panda3d.core import Loader
from panda3d.core import BitMask32
from panda3d.core import LineSegs
from panda3d.bullet import BulletSphereShape
from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletGhostNode

class Drone:

    # RIGIDBODYMASS = 1
    # RIGIDBODYRADIUS = 0.1
    # GHOSTRADIUS = 0.5

    # NAVIGATIONFORCE = .5
    # AVOIDANCEFORCE = 5
    # FORCEFALLOFFDISTANCE = .5
    # LINEARDAMPING = .9

    RIGIDBODYMASS = 1
    RIGIDBODYRADIUS = 0.1
    GHOSTRADIUS = 0.3

    NAVIGATIONFORCE = 1
    AVOIDANCEFORCE = 25
    FORCEFALLOFFDISTANCE = .5
    LINEARDAMPING = 0.95

    def __init__(self, manager, name: str, position: Vec3, uri="drone address", printDebugInfo=False):

        self.base = manager.base
        self.manager = manager
        self.name = name
        self.manager.drones[self.name] = self # put the drone into the drone manager's dictionary
        
        self.canConnect = False # true if the virtual drone is linked to a real drone
        self.isConnected = False # wether to connection to a real drone is currently active
        self.uri = uri
        if self.uri != "drone address":
            self.canConnect = True

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
        self.waitingPosition = Vec3(position[0], position[1], 1)
        
        self.printDebugInfo = printDebugInfo
        if self.printDebugInfo == True: # put a second drone model on top of drone that outputs debug stuff
            model = self.base.loader.loadModel(self.base.modelDir + "/drones/drone1.egg")
            model.setPos(0, 0, .2)
            model.reparentTo(self.rigidBodyNP)

        # initialize line renderers
        self.targetLineNP = self.base.render.attachNewNode(LineSegs().create())
        self.velocityLineNP = self.base.render.attachNewNode(LineSegs().create())


    # connect to a real drone with the uri
    def connect(self):
        print(self.name, "@", self.uri, "connecting")
        self.isConnected = True
        self.scf = SyncCrazyflie(self.uri, cf=Crazyflie(rw_cache='./cache'))
        self.scf.open_link()
        self.reset_estimator()


    def sendPosition(self):
        #print("sending position")
        cf = self.scf.cf
        cf.param.set_value('flightmode.posSet', '1')
        pos = self.getPos()
        # print('Setting position {} | {} | {}'.format(pos[0], pos[1], pos[2]))
        cf.commander.send_position_setpoint(pos[0], pos[1], pos[2], 0)


    def disconnect(self):
        print(self.name, "@", self.uri, "disconnecting")
        self.isConnected = False
        cf = self.scf.cf
        cf.commander.send_stop_setpoint()
        time.sleep(0.1)
        self.scf.close_link()


    def returnToWaitingPosition(self):
        self.setTarget(self.waitingPosition)


    def update(self):
        self._updateForce()
        self._updateGhost()
        self._handleCollisions()

        if self.isConnected:
            self.sendPosition()

        self._drawTargetLine()
        self._drawVelocityLine()

        self._printDebugInfo()


    def _updateGhost(self):
        self.ghostNP.setPos(self.getPos())


    def _updateForce(self):
        dist = (self.target - self.getPos())
        if(dist.length() > self.FORCEFALLOFFDISTANCE):
            force = dist.normalized() * self.NAVIGATIONFORCE
        else:
            force = dist * self.NAVIGATIONFORCE / self.FORCEFALLOFFDISTANCE
        velMult = self.getVel().length() + .1
        velMult = velMult
        self._addForce(force * 3)


    def _handleCollisions(self):
        for node in self.ghost.getOverlappingNodes():
            if node.name.startswith("drone"):
                other = self.manager.getDrone(node.name)
                dist = other.getPos() - self.getPos()
                if dist.length() < 0.2:
                    print("BONK")
                distMult = max([0, 2 * self.GHOSTRADIUS - dist.length()])
                distMult = distMult
                # velMult = other.getVel().length() + self.getVel().length() + 1
                velMult = self.getVel().length()
                velMult = velMult + .5
                self._addForce(-dist.normalized() * distMult * velMult * self.AVOIDANCEFORCE)


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


    def wait_for_position_estimator(self):
        print('Waiting for estimator to find position...')

        log_config = LogConfig(name='Kalman Variance', period_in_ms=500)
        log_config.add_variable('kalman.varPX', 'float')
        log_config.add_variable('kalman.varPY', 'float')
        log_config.add_variable('kalman.varPZ', 'float')

        var_y_history = [1000] * 10
        var_x_history = [1000] * 10
        var_z_history = [1000] * 10

        threshold = 0.001

        with SyncLogger(self.scf, log_config) as logger:
            for log_entry in logger:
                data = log_entry[1]

                var_x_history.append(data['kalman.varPX'])
                var_x_history.pop(0)
                var_y_history.append(data['kalman.varPY'])
                var_y_history.pop(0)
                var_z_history.append(data['kalman.varPZ'])
                var_z_history.pop(0)

                min_x = min(var_x_history)
                max_x = max(var_x_history)
                min_y = min(var_y_history)
                max_y = max(var_y_history)
                min_z = min(var_z_history)
                max_z = max(var_z_history)

                # print("{} {} {}".
                #       format(max_x - min_x, max_y - min_y, max_z - min_z))

                if (max_x - min_x) < threshold and (
                        max_y - min_y) < threshold and (
                        max_z - min_z) < threshold:
                    break


    def reset_estimator(self):
        cf = self.scf.cf
        cf.param.set_value('kalman.resetEstimation', '1')
        time.sleep(0.1)
        cf.param.set_value('kalman.resetEstimation', '0')

        self.wait_for_position_estimator()