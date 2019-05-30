import random
from drone import Drone
# pylint: disable=no-name-in-module
from panda3d.core import Vec3

class DroneManager:
    
    def __init__(self, base):
        self.base = base
        self.drones = {}


    def spawnDrones(self):
        self.drones["1"] = Drone("1", Vec3(0, -2, 2), self, printDebugInfo=True)
        self.drones["2"] = Drone("2", Vec3(0, 2, 2), self)

        self.drones.get("1").setTarget(Vec3(0, 2, 2))
        self.drones.get("2").setTarget(Vec3(0, -2, 2))


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