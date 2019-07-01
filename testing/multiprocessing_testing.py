import os, sys
import time
from math import sin, cos
import numpy as np
import random
from multiprocessing import Process 

class Test():

    def __init__(self):
        #self.procs = []
        self.droneList = (Drone("0"), Drone("1"))


    def connectAll(self):
        procs = []
        for drone in self.droneList:
            proc = Process(target=drone.connect)
            procs.append(proc)
            proc.start()
        for proc in procs:
            proc.join()
        print("All connected!")


class Drone():
    
    def __init__(self, name):
        self.name = name


    def connect(self):
        print("connecting {}".format(self.name))
        time.sleep(random.uniform(0,3))
        print("{} finished connecting".format(self.name))


if __name__ ==  '__main__':
    test = Test()
    test.connectAll()
                   
                                                  
                                             
                                                                                
                                                                                
