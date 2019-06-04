import random
from drone import Drone
# pylint: disable=no-name-in-module
from panda3d.core import Vec3

class DroneManager:
    
    def __init__(self, base):
        self.base = base
        self.drones = {}
        self.spawnDrone("1", Vec3(0, -2, 2))
        self.spawnDrone("2", Vec3(0, 2, 2.2))
        self.spawnDrone("3", Vec3(1, -2, 2))
        self.spawnDrone("4", Vec3(1, 2, 2))
        self.spawnDrone("5", Vec3(-1, -2, 2))
        self.spawnDrone("6", Vec3(-1, 2, 2))
        self.spawnDrone("7", Vec3(1, 2, .5))
        self.spawnDrone("8", Vec3(-1, 2, .5))
        self.spawnDrone("9", Vec3(1, -2, .5))
        self.spawnDrone("10", Vec3(-1, -2, .5))

        # self.spawnDrone("1", Vec3(0, -2, 2), printDebugInfo=False)
        # self.spawnDrone("2", Vec3(0, 2, 2))
        # self.getDrone("1").setTarget(Vec3(0, 2, 2))
        # self.getDrone("2").setTarget(Vec3(0, -2, 2))


    def spawnDrone(self, name: str, position: Vec3, printDebugInfo=False):
        self.drones[name] = Drone(name, position, self, printDebugInfo=printDebugInfo)


    def updateDronesTask(self, task):
        for drone in self.drones.values():
            drone.update()
        return task.cont


    def handleCollisions(self): # currently implemented in drone class
        pass


    def getRandomRoomCoordinate(self) -> Vec3:
        newX = random.uniform(-self.base.roomSize.x/2, self.base.roomSize.x/2)
        newY = random.uniform(-self.base.roomSize.y/2, self.base.roomSize.y/2)
        newZ = random.uniform(0, self.base.roomSize.z)
        return Vec3(newX, newY, newZ)  

    
    def getDrone(self, name: str) -> Drone:
        return self.drones.get(name)