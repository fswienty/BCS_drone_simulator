import random
import time
from drone import Drone
import cflib.crtp
# pylint: disable=no-name-in-module
from panda3d.core import Vec3
from direct.showbase import DirectObject
#import numpy as np


class DroneManager(DirectObject.DirectObject):
    
    def __init__(self, base):
        self.base = base
        #self.roomSize = Vec3(3.40, 4.56, 2.56) # the dimensions of the bcs drone lab in meters
        self.roomSize = Vec3(2, 3, 1.5) # confined dimensions because the room and drone coordinated dont match up yet

        self.drones = {}
        Drone(self, "drone1", Vec3(0, 0, .3), uri="radio://0/80/2M/E7E7E7E7E1")
        Drone(self, "drone2", Vec3(1, 1, .3))
        Drone(self, "drone3", Vec3(-1, -1, .3))
        Drone(self, "drone4", Vec3(1, -1, .3))
        # Drone(self, "drone5", self.getRandomRoomCoordinate())
        # Drone(self, "drone6", self.getRandomRoomCoordinate())
        # Drone(self, "drone7", self.getRandomRoomCoordinate())

        self.base.taskMgr.doMethodLater(0, self.updateDronesTask, "UpdateDrones")

        self.isStarted = False
        self.isUpdating = False
        self.accept('1', self.startAll)
        self.accept('2', self.toggleUpdateDrones)
        self.accept('3', self.returnToWaitingPosition)
        self.accept('4', self.landAll)


    def startAll(self):
        print("starting all")
        self.isStarted = True
        for drone in self.drones.values():
            pos = drone.getPos()
            drone.setTarget(target=Vec3(pos[0], pos[1], 1))

    
    def landAll(self):
        print("landing all")
        self.isStarted = False
        for drone in self.drones.values():
            pos = drone.getPos()
            drone.setTarget(target=Vec3(pos[0], pos[1], 0.3))



    def toggleUpdateDrones(self):
        if self.isUpdating == False:
            if self.isStarted == False:
                print("drones are not started yet")
                return
            self.isUpdating = True
            for drone in self.drones.values():
                drone.setTarget(random=True)
        else:
            self.isUpdating = False
            for drone in self.drones.values():
                drone.setTarget(target=drone.getPos())


    def returnToWaitingPosition(self):
        if self.isUpdating == True:
            for drone in self.drones.values():
                drone.returnToWaitingPosition()


    def updateDronesTask(self, task):
        for drone in self.drones.values():
            drone.update()
        return task.cont


    def getRandomRoomCoordinate(self) -> Vec3:
        newX = random.uniform(-self.roomSize.x/2, self.roomSize.x/2)
        newY = random.uniform(-self.roomSize.y/2, self.roomSize.y/2)
        newZ = random.uniform(0+0.3, self.roomSize.z)
        return Vec3(newX, newY, newZ)  


    def getDrone(self, name: str) -> Drone:
        return self.drones.get(name)

    def getAllPositions(self):
        lst = []
        for drone in self.drones.values():
            pos = drone.getPos()
            lst.append([pos.x, pos.y, pos.z])
        return lst