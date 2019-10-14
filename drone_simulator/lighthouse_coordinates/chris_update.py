import sys
import openvr
 
import logging
import time
 
import cflib.crtp  # noqa
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.mem import LighthouseBsGeometry
from cflib.crazyflie.mem import MemoryElement
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
 
# Only output errors from the logging framework
logging.basicConfig(level=logging.ERROR)
 
CENTER_AROUND_CONTROLLER = False
 
 
def getBsPos():
    """
    Get the position of the base stations.
 
    2019-10-02 Code for getting the base station positions taken from:
    https://github.com/bitcraze/crazyflie-firmware/blob/master/tools/lighthouse/get_bs_position.py
    """
 
    print("Opening OpenVR")
    vr = openvr.init(openvr.VRApplication_Other)
 
    print("OpenVR Opened")
    devices = {}
    poses = vr.getDeviceToAbsoluteTrackingPose(openvr.TrackingUniverseStanding, 0,
                                               openvr.k_unMaxTrackedDeviceCount)
 
    if CENTER_AROUND_CONTROLLER:
        offset = None
        # Acquire offset
        for i in range(openvr.k_unMaxTrackedDeviceCount):
            if poses[i].bPoseIsValid:
                device_class = vr.getTrackedDeviceClass(i)
                if device_class == openvr.TrackedDeviceClass_Controller or \
                        device_class == openvr.TrackedDeviceClass_GenericTracker:
                    pose = poses[i].mDeviceToAbsoluteTracking
                    offset = [pose[0][3], pose[1][3], pose[2][3]]
                    break
 
        if offset is None:
            print("Controller not found, place controller at the origin of the space")
            openvr.shutdown()
            sys.exit(1)
    else:
        offset = [0, 0, 0]
 
    print("Origin: {}", offset)
 
    print("-------------------------------")
 
    bs_poses = [None, None]
 
    for i in range(openvr.k_unMaxTrackedDeviceCount):
        if poses[i].bPoseIsValid:
            device_class = vr.getTrackedDeviceClass(i)
            if (device_class == openvr.TrackedDeviceClass_TrackingReference):
 
                mode = vr.getStringTrackedDeviceProperty(i, openvr.Prop_ModeLabel_String)
                try:
                    mode = mode.decode("utf-8")
                except:
                    # likely already decoded
                    pass
 
                pose = poses[i].mDeviceToAbsoluteTracking
 
                # Mode 'B' is master
                if mode == 'B':
                    bs_poses[0] = pose
                elif mode == 'A' or mode == 'C':
                    bs_poses[1] = pose
                else:
                    print("Base station with mode {} detected.".format(mode))
                    print("This script can only work with base station V1 (mode A, B or C). Exiting.")
                    sys.exit(1)
 
    for pose in bs_poses:
        if pose is None:
            continue
 
        position = [pose[0][3] - offset[0], pose[1][3] - offset[1], pose[2][3] - offset[2]]
        rotation = [pose[0][:3], pose[1][:3], pose[2][:3]]
 
        print("{.origin = {", end='')
        for i in position:
            print("{:0.6f}, ".format(i), end='')
 
        print("}, .mat = {", end='')
 
        for i in rotation:
            print("{", end='')
            for j in i:
                print("{:0.6f}, ".format(j), end='')
            print("}, ", end='')
 
        print("}},")
 
    openvr.shutdown()
    return bs_poses, offset
 
 
class WriteMem:
    """
    Write the base station positions to a drone.
 
 
    2019-10-02 Code for updating the drones taken from:
    https://github.com/bitcraze/crazyflie-lib-python/blob/master/examples/lighthouse/write-geometry-mem.py
    """
    def __init__(self, uri, bs1, bs2):
        self.data_written = False
 
        with SyncCrazyflie(uri, cf=Crazyflie(rw_cache='./cache')) as scf:
            mems = scf.cf.mem.get_mems(MemoryElement.TYPE_LH)
 
            count = len(mems)
            if count != 1:
                raise Exception('Unexpected nr of memories found:', count)
 
            mems[0].geometry_data = [bs1, bs2]
 
            print('Writing data')
            mems[0].write_data(self._data_written)
 
            while not self.data_written:
                time.sleep(1)
 
    def _data_written(self, mem, addr):
        self.data_written = True
        print('Data written')
 
 
if __name__ == "__main__":
    print("Let's go!")
    print("First, let's get the positions of the base stations")
    print("___________________________________________________")
    bsPoses, offset = getBsPos()
    print("___________________________________________________")
    if len(bsPoses) is not 2 or bsPoses[0] is None or bsPoses[1] is None:
        print("Well, something went wrong, sorry")
        print("Number of returned base station positions: %d" % len(bsPoses))
        for i in range(len(bsPoses)):
            print("Type of pose %d is: %s" % (i, type(bsPoses[i])))
        print("Is SteamVR running? If not, that might just be the problem")
        exit(1)
 
    # formatting the positions
    bs1 = LighthouseBsGeometry()
    pose1 = bsPoses[0]
    bs1.origin = [pose1[0][3] - offset[0], pose1[1][3] - offset[1], pose1[2][3] - offset[2]]
    bs1.rotation_matrix = [pose1[0][:3], pose1[1][:3], pose1[2][:3]]
 
    bs2 = LighthouseBsGeometry()
    pose2 = bsPoses[1]
    bs2.origin = [pose2[0][3] - offset[0], pose2[1][3] - offset[1], pose2[2][3] - offset[2]]
    bs2.rotation_matrix = [pose2[0][:3], pose2[1][:3], pose2[2][:3]]
 
    # initialize the low-level drivers (don't list the debug drivers)
    cflib.crtp.init_drivers(enable_debug_driver=False)
 
    print("Now, let's scan for available drones")
    available = cflib.crtp.scan_interfaces()
    if len(available) == 0:
        print("Sorry, no drones found. Did you plug in the receiver and turned the drones on?")
        exit(1)
    print("%d drones found, which are:" %len(available))
    for i in available:
        print(i[0])
 
    # write to the drones
    for i in available:
        print("Now writing to drone %s" % i[0])
        uri = i[0]
        WriteMem(uri, bs1, bs2)
 
    print("All done, bye!")
    exit(0)