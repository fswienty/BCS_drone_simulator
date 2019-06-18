import cflib.crtp
# pylint: disable=no-name-in-module
from panda3d.core import Vec3

def scanAndReset():
    # Initiate the low level drivers
    cflib.crtp.init_drivers(enable_debug_driver=False)
    print('Scanning interfaces for Crazyflies...')
    available = cflib.crtp.scan_interfaces()
    a = cflib.crtp.get_interfaces_status()
    # TODO reset estimator and get position in parallel
    print('Crazyflies found:')
    for i in available:
        print(i[0])
        print(available)
        print(a)

    posAddressList = []
    for i in available:
        posAddressList.append(["iPosition", "iUri"])

    posAddressList = [[Vec3(0,0,.3), "radio://0/80/2M/E7E7E7E7E0"], [Vec3(1,0,.3), "radio://0/80/2M/E7E7E7E7E1"]]

    return posAddressList