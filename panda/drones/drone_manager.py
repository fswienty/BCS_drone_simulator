import random
from drones.drone import Drone
# pylint: disable=no-name-in-module
from panda3d.core import Vec3
import numpy as np

class DroneManager:
    
    def __init__(self, base):
        self.base = base
        self.drones = {}
        Drone(self, "drone1", Vec3(0, 0, 1), uri="radio://0/80/2M/E7E7E7E7E1")
        Drone(self, "drone2", self.getRandomRoomCoordinate())
        Drone(self, "drone3", self.getRandomRoomCoordinate())
        Drone(self, "drone4", self.getRandomRoomCoordinate())
        Drone(self, "drone5", self.getRandomRoomCoordinate())
        Drone(self, "drone6", self.getRandomRoomCoordinate())
        Drone(self, "drone7", self.getRandomRoomCoordinate())


    def updateDronesTask(self, task):
        for drone in self.drones.values():
            drone.update()
        return task.cont


    def getRandomRoomCoordinate(self) -> Vec3:
        newX = random.uniform(-self.base.roomSize.x/2, self.base.roomSize.x/2)
        newY = random.uniform(-self.base.roomSize.y/2, self.base.roomSize.y/2)
        newZ = random.uniform(0, self.base.roomSize.z)
        return Vec3(newX, newY, newZ)  


    def getDrone(self, name: str) -> Drone:
        return self.drones.get(name)

    def getAllPositions(self):
        lst = []
        for drone in self.drones.values():
            pos = drone.getPos()
            lst.append([pos.x, pos.y, pos.z])
        return lst