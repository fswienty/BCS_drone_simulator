import random

from drone import Drone
from formations.formation_ui_element import loadFormationSelectionFrame

import cflib.crtp

from panda3d.core import Vec3
from direct.showbase import DirectObject
from direct.gui.DirectGui import DirectButton
from direct.gui.DirectGui import DirectFrame


class DroneManager(DirectObject.DirectObject):

    def __init__(self, base, droneList):
        self.base = base
        # the actual dimensions of the bcs drone lab in meters
        # self.roomSize = Vec3(3.40, 4.56, 2.56)
        # confined dimensions because the room and drone coordinates dont match up yet.
        # Also, flying near the windows/close to walls/too high often makes the lps loose track
        self.roomSize = Vec3(1.5, 2, 1.3)
        self.initDrones(droneList)
        self.initUI()


    def initDrones(self, droneList):
        """Initializes the drones defined in droneList."""
        self.isStarted = False
        self.isConnected = False
        self.drones = {}  # this is the dictionary all drones are held in with their name as key

        if droneList == []:
            print("No drones to spawn")
        else:
            for i in range(0, len(droneList)):
                name = "drone{}".format(i)
                position = droneList[i][0]
                uri = droneList[i][1]
                self.drones[name] = Drone(self, name, position, uri=uri)

        self.base.taskMgr.add(self.updateDronesTask, "UpdateDrones")


    def initUI(self):
        # initialize drone control panel
        buttonSize = (-4, 4, -.2, .8)
        buttonDistance = 0.15

        frame = DirectFrame(frameColor=(.2, .2, .2, 1), frameSize=(-.5, .5, -.7, .1), pos=(-.9, 0, -.6), scale=.5)

        button = DirectButton(text="Start", scale=.1, frameSize=buttonSize, command=self.startLandAll)
        button["extraArgs"] = [button]
        button.reparentTo(frame)

        button = DirectButton(text="Random Target", scale=.1, frameSize=buttonSize, command=self.setRandomTargets)
        button.reparentTo(frame)
        button.setPos(Vec3(0, 0, -1 * buttonDistance))

        button = DirectButton(text="Stop", scale=.1, frameSize=buttonSize, command=self.stopAll)
        button.reparentTo(frame)
        button.setPos(Vec3(0, 0, -2 * buttonDistance))

        button = DirectButton(text="Return", scale=.1, frameSize=buttonSize, command=self.returnToWaitingPosition)
        button.reparentTo(frame)
        button.setPos(Vec3(0, 0, -3 * buttonDistance))

        button = DirectButton(text="Connect", scale=.1, frameSize=buttonSize, command=self.toggleConnections)
        button["extraArgs"] = [button]
        button.reparentTo(frame)
        button.setPos(Vec3(0, 0, -4 * buttonDistance))

        # initialize an UI element with all available formations
        loadFormationSelectionFrame(self)



    def startLandAll(self, button):
        if not self.isStarted:
            self.isStarted = True
            button["text"] = "Land"
            print("starting all")
            for drone in self.drones.values():
                pos = drone.getPos()
                drone.setTarget(target=Vec3(pos[0], pos[1], .7))
        else:
            self.isStarted = False
            button["text"] = "Start"
            print("landing all")
            for drone in self.drones.values():
                pos = drone.getPos()
                drone.setTarget(target=Vec3(pos[0], pos[1], .2))


    def returnToWaitingPosition(self):
        """Makes all drones hover above their starting position. Usefull to make the drones land just where they started."""
        if not self.isStarted:
            print("can't return to waiting position, drones are not started")
            return
        print("returning to waiting positions")
        for drone in self.drones.values():
            drone.setTarget(drone.waitingPosition)


    def setRandomTargets(self):
        """Set random targets for all drones."""
        if not self.isStarted:
            print("can't set random targets, drones are not started")
            return
        print("setting random targets")
        for drone in self.drones.values():
            drone.setRandomTarget()


    def stopAll(self):
        """Stops all drones and makes them hover where they are."""
        if not self.isStarted:
            print("can't stop drones, drones are not started")
            return
        print("stopping drones")
        for drone in self.drones.values():
            drone.setTarget(target=drone.getPos())


    def toggleConnections(self, button):
        """Connects/Disconnects the virtual drones to/from the real drones."""
        # connect drones
        if not self.isConnected:
            self.isConnected = True
            button["text"] = "Disconnect"
            print("initializing drivers")
            cflib.crtp.init_drivers(enable_debug_driver=False)
            print("connecting drones")
            for drone in self.drones.values():
                drone.connect()
        # disconnect drones
        else:
            self.isConnected = False
            button["text"] = "Connect"
            print("disconnecting drones")
            for drone in self.drones.values():
                if drone.isConnected:
                    drone.disconnect()


    def applyFormation(self, formation):
        """Applies the supplied formation to the drones."""
        if not self.isStarted:
            print("Can't apply formation, drones are not started")
            return

        name = formation[0]
        dronePositions = formation[1]
        requiredDrones = len(dronePositions)

        availableDrones = self.drones.__len__()
        maxNumber = availableDrones
        if requiredDrones > availableDrones:
            print("The formation contains more points than there are drones available")

        if requiredDrones < availableDrones:
            print("The formation contains less points than there are drones available, some drones will remain stationary")
            maxNumber = requiredDrones

        print("applying {} formation".format(name))
        droneList = list(self.drones.values())
        for i in range(0, maxNumber):
            droneList[i].setTarget(Vec3(dronePositions[i, 0], dronePositions[i, 1], dronePositions[i, 2]))


    def updateDronesTask(self, task):
        """Run the update methods of all drones."""
        for drone in self.drones.values():
            drone.update()
        return task.cont


    def getRandomRoomCoordinate(self) -> Vec3:
        """Returns random 3D coordinates withing the confines of the room."""
        newX = random.uniform(-self.roomSize.x / 2, self.roomSize.x / 2)
        newY = random.uniform(-self.roomSize.y / 2, self.roomSize.y / 2)
        newZ = random.uniform(0 + 0.3, self.roomSize.z)
        return Vec3(newX, newY, newZ)


    def getDrone(self, name: str) -> Drone:
        """Finds a drone by name, returns the drone object."""
        return self.drones.get(name)


    def getAllPositions(self):
        """Returns a list of the positions of all drones. Usefull when recording their paths for later."""
        lst = []
        for drone in self.drones.values():
            pos = drone.getPos()
            lst.append([pos.x, pos.y, pos.z])
        return lst
