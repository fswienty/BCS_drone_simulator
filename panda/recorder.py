import os
import sys
import numpy as np
from drones.drone import Drone
# pylint: disable=no-name-in-module
from panda3d.core import Vec3

class DroneRecorder:
    
    # timestep, drone, axis
    def __init__(self, droneManager):
        self.droneManager = droneManager
        # timestep, drone, axis
        self.recordingLst = []
        #self.recording = np.array([])    


    def recordDronesTask(self, task):
        task.delayTime = 0.5
        #tt = np.load("trajectories/pos_traj.npy")
        #np.save("trajectories/jerk_traj.npy", error_calc.jerk_traj)
        self.recordingLst.append(self.droneManager.getAllPositions())
        #print("####################")
        #print(np.asarray(self.recordingLst))
        return task.again

    def save(self):
        np.save(os.path.join(sys.path[0], "trajectories/traj.npy"), np.asarray(self.recordingLst))
