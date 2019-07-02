import os
import sys
import numpy as np

from direct.showbase import DirectObject


class DroneRecorder(DirectObject.DirectObject):

    # timestep, drone, axis
    def __init__(self, droneManager):
        self.droneManager = droneManager
        # timestep, drone, axis
        self.recordingLst = []
        self.isRecording = False
        self.accept('m', self.save)
        self.accept('space', self.toggleRecording)


    def recordDronesTask(self, task):
        task.delayTime = 0.3
        #tt = np.load("trajectories/pos_traj.npy")
        #np.save("trajectories/jerk_traj.npy", error_calc.jerk_traj)
        self.recordingLst.append(self.droneManager.getAllPositions())
        #print("####################")
        #print(np.asarray(self.recordingLst))
        print("recording")
        return task.again


    def save(self):
        np.save(os.path.join(sys.path[0], "trajectories/traj.npy"), np.asarray(self.recordingLst))
        print("recording saved")


    def toggleRecording(self):
        if not self.isRecording:
            self.isRecording = True
            self.droneManager.base.taskMgr.doMethodLater(0, self.recordDronesTask, "RecordDrones")
        else:
            self.isRecording = False
            self.droneManager.base.taskMgr.remove("RecordDrones")
