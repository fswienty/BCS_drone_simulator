import random
import time
from multiprocessing import Process
from drone import Drone
import cflib.crtp
# pylint: disable=no-name-in-module
from panda3d.core import Vec3
from direct.showbase import DirectObject
from direct.gui.DirectGui import DirectButton
from direct.gui.DirectGui import DirectFrame
from formations.formation_loader import FormationLoader

class DroneManager(DirectObject.DirectObject):
    
    def __init__(self, base):
        self.base = base
        #self.roomSize = Vec3(3.40, 4.56, 2.56) # the dimensions of the bcs drone lab in meters
        self.roomSize = Vec3(1.5, 2, 1.3) # confined dimensions because the room and drone coordinated dont match up yet
        self.initDrones()
        self.initFormations()
        self.initUI()


    def initDrones(self):
        self.isStarted = False
        self.isConnected = False
        self.drones = {}

        self.loadDrone("drone0", Vec3(0, 0, .3), uri="radio://0/80/2M/E7E7E7E7E0")
        self.loadDrone("drone1", Vec3(1, 1, .3), uri="radio://0/80/2M/E7E7E7E7E1")
        self.loadDrone("drone2", Vec3(1, -1, .3), uri="radio://0/80/2M/E7E7E7E7E2")
        # self.loadDrone("drone3", Vec3(-1, 1, .3), uri="radio://0/80/2M/E7E7E7E7E3")
        self.loadDrone("drone4", Vec3(-1, -1, .3), uri="radio://0/80/2M/E7E7E7E7E4")

        self.base.taskMgr.add(self.updateDronesTask, "UpdateDrones")


    def initFormations(self):
        self.formations = {}
    
        self.loadFormation("square")
        self.loadFormation("square_inv")
        self.loadFormation("line")
        self.loadFormation("upright_square")

        self.accept('1', self.applyFormation, extraArgs=["square"])
        self.accept('2', self.applyFormation, extraArgs=["square_inv"])
        self.accept('3', self.applyFormation, extraArgs=["line"])
        self.accept('4', self.applyFormation, extraArgs=["upright_square"])


    def initUI(self):
        buttonSize = (-4, 4, -.2, .8)
        buttonDistance = 0.15

        frame = DirectFrame(frameColor=(.2, .2, .2, 1), frameSize=(-.5, .5, -.7, .1), pos=(-.9, 0, -.6), scale=.5)

        self.buttonStartLand = DirectButton(text = "Start", scale=.1, frameSize=buttonSize, command=self.startLandAll)
        self.buttonStartLand.reparentTo(frame)

        self.buttonRandomTargets = DirectButton(text = "Random Target", scale=.1, frameSize=buttonSize, command=self.setRandomTargets)
        self.buttonRandomTargets.reparentTo(frame)
        self.buttonRandomTargets.setPos(Vec3(0,0,-1*buttonDistance))

        self.buttonStop = DirectButton(text = "Stop", scale=.1, frameSize=buttonSize, command=self.stopAll)
        self.buttonStop.reparentTo(frame)
        self.buttonStop.setPos(Vec3(0,0,-2*buttonDistance))

        self.buttonReturn = DirectButton(text = "Return", scale=.1, frameSize=buttonSize, command=self.returnToWaitingPosition)
        self.buttonReturn.reparentTo(frame)
        self.buttonReturn.setPos(Vec3(0,0,-3*buttonDistance))

        self.buttonToggleConnection = DirectButton(text = "Connect", scale=.1, frameSize=buttonSize, command=self.toggleConnections)
        self.buttonToggleConnection.reparentTo(frame)
        self.buttonToggleConnection.setPos(Vec3(0,0,-4*buttonDistance))


    def startLandAll(self):
        if self.isStarted == False:
            self.isStarted = True
            self.buttonStartLand["text"] = "Land"
            print("starting all")
            for drone in self.drones.values():
                pos = drone.getPos()
                drone.setTarget(target=Vec3(pos[0], pos[1], .7))
        else:
            self.isStarted = False
            self.buttonStartLand["text"] = "Start"
            print("landing all")
            for drone in self.drones.values():
                pos = drone.getPos()
                drone.setTarget(target=Vec3(pos[0], pos[1], .2))


    def returnToWaitingPosition(self):
        if self.isStarted == False:
            print("can't return to waiting position, drones are not started")
            return
        print("returning to waiting positions")
        for drone in self.drones.values():
            drone.returnToWaitingPosition()


    def setRandomTargets(self):
        if self.isStarted == False:
            print("can't set random targets, drones are not started")
            return
        print("setting random targets")
        for drone in self.drones.values():
            drone.setTarget(random=True)


    def stopAll(self):
        if self.isStarted == False:
            print("can't stop drones, drones are not started")
            return
        print("stopping drones")
        for drone in self.drones.values():
            drone.setTarget(target=drone.getPos())


    def toggleConnections(self):
        #connect drones
        if self.isConnected == False:
            self.isConnected = True
            self.buttonToggleConnection["text"] = "Disconnect"
            print("initializing drivers")
            cflib.crtp.init_drivers(enable_debug_driver=False)
            print("connecting drones")
            for drone in self.drones.values():
                drone.connect()
        #disconnect drones
        else:
            self.isConnected = False
            self.buttonToggleConnection["text"] = "Connect"
            print("disconnecting drones")
            for drone in self.drones.values():
                if drone.isConnected:
                    drone.disconnect()           


    def loadFormation(self, name):
        self.formations[name] = FormationLoader(name)


    def applyFormation(self, name: str):
        if self.formations[name].drones != self.drones.__len__():
            print("Amount of drones in simulation is not equal to amount of drones required for formation")
            return
        if self.isStarted == False:
            print("Can't apply formation, drones are not started")
            return
        droneList = list(self.drones.values())
        formation = self.formations[name].array
        for i in range(0, self.drones.__len__()):
            droneList[i].setTarget(Vec3(formation[i,0], formation[i,1], formation[i,2]))
            

    def updateDronesTask(self, task):
        for drone in self.drones.values():
            drone.update()
        return task.cont


    def getRandomRoomCoordinate(self) -> Vec3:
        newX = random.uniform(-self.roomSize.x/2, self.roomSize.x/2)
        newY = random.uniform(-self.roomSize.y/2, self.roomSize.y/2)
        newZ = random.uniform(0+0.3, self.roomSize.z)
        return Vec3(newX, newY, newZ)  


    def loadDrone(self, name: str, position: Vec3, uri="drone address", printDebugInfo=False):
        self.drones[name] = Drone(self, name, position, uri=uri, printDebugInfo=printDebugInfo)


    def getDrone(self, name: str) -> Drone:
        return self.drones.get(name)


    def getAllPositions(self):
        lst = []
        for drone in self.drones.values():
            pos = drone.getPos()
            lst.append([pos.x, pos.y, pos.z])
        return lst