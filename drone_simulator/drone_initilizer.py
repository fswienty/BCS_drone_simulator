import sys
import time
import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.log import LogConfig
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.crazyflie.syncLogger import SyncLogger
# pylint: disable=no-name-in-module
from panda3d.core import Vec3


class SimpleDrone():
    
    def __init__(self, address):
        self.pos = Vec3(0, 0, 0)
        self.address = address


    def wait_for_position_estimator(self, scf):
        print('Waiting for estimator to find position...')

        log_config = LogConfig(name='Kalman Variance', period_in_ms=500)
        log_config.add_variable('kalman.varPX', 'float')
        log_config.add_variable('kalman.varPY', 'float')
        log_config.add_variable('kalman.varPZ', 'float')

        var_y_history = [1000] * 10
        var_x_history = [1000] * 10
        var_z_history = [1000] * 10

        threshold = 0.001

        with SyncLogger(scf, log_config) as logger:
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


    def reset_estimator(self, scf):
        cf = scf.cf
        cf.param.set_value('kalman.resetEstimation', '1')
        time.sleep(0.1)
        cf.param.set_value('kalman.resetEstimation', '0')

        self.wait_for_position_estimator(scf)


    def position_callback(self, timestamp, data, logconf):
        x = data['kalman.stateX']
        y = data['kalman.stateY']
        z = data['kalman.stateZ']
        # x = data['lighthouse.x']
        # y = data['lighthouse.y']
        # z = data['lighthouse.z']
        self.pos = Vec3(x, y, z)
        # print('pos: ({}, {}, {})'.format(x, y, z))


    def start_position_printing(self, scf):
        log_conf = LogConfig(name='Position', period_in_ms=100)
        log_conf.add_variable('kalman.stateX', 'float')
        log_conf.add_variable('kalman.stateY', 'float')
        log_conf.add_variable('kalman.stateZ', 'float')
        # log_conf.add_variable('lighthouse.x', 'float')
        # log_conf.add_variable('lighthouse.y', 'float')
        # log_conf.add_variable('lighthouse.z', 'float')

        scf.cf.log.add_config(log_conf)
        log_conf.data_received_cb.add_callback(self.position_callback)
        log_conf.start()

    def initDrone(self, posAddressList):
        print("Resetting and locating ", self.address)
        scf = SyncCrazyflie(self.address, cf=Crazyflie(rw_cache='./cache'))
        scf.open_link()
        self.reset_estimator(scf)
        self.start_position_printing(scf)
        time.sleep(0.2)
        self.pos
        posAddressList.append([self.pos, self.address])
        print("added", [self.pos, self.address])
        scf.close_link()



def resetAndLocate(addressList: list):

    if addressList == []:
        return []

    cflib.crtp.init_drivers(enable_debug_driver=False)
    drones = []
    for i in range(0, len(addressList)):
        drones.append(SimpleDrone(addressList[i]))

    posAddressList = []
    for drone in drones:
        drone.initDrone(posAddressList)


    # posAddressList = []
    # for i in available:
    #     posAddressList.append(["iPosition", "iUri"])

    # posAddressList = [[Vec3(0,0,.3), "radio://0/80/2M/E7E7E7E7E0"], [Vec3(1,0,.3), "radio://0/80/2M/E7E7E7E7E1"]]

    return posAddressList


if __name__ == "__main__":
    addressList = []
    addressList.append('radio://0/80/2M/E7E7E7E7E0')
    # addresses.append('radio://0/80/2M/E7E7E7E7E1')
    addressList.append('radio://0/80/2M/E7E7E7E7E2')
    # addresses.append('radio://0/80/2M/E7E7E7E7E3')
    #addressList.append('radio://0/80/2M/E7E7E7E7E4')
    print(resetAndLocate(addressList))
