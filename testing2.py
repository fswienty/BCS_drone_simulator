import os
import time
import random
 
from multiprocessing import Process
 
class Drone():
    
    def __init__(self, name):
        self.name = name


    def connect(self):
        print("connecting {}".format(self.name))
        time.sleep(random.uniform(0,3))
        print("{} finished connecting".format(self.name))
 

if __name__ == '__main__':

    procs = []
    droneList = (Drone("0"), Drone("1"))

    # proc = Process(target=doubler, args=(number,))
    # procs.append(proc)
    for drone in droneList:
        proc = Process(target=drone.connect)
        procs.append(proc)
        proc.start()
 
    for proc in procs:
        proc.join()

    print("All Done!")