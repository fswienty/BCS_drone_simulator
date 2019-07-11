# import random
# import math
# from autograd import grad
import numpy as np


class Functions():

    # AGENT TRAJLEN DIM

    positions = 0

    # def __init__(self, timestep, trajLen, min_dist, start_vel, start_pos, goal_vel, goal_pos):
    #     self.timestep = timestep
    #     self.agents = goal_vel.shape[0]
    #     self.trajLen = trajLen
    #     self.min_dist = min_dist
    #     self.dim = goal_vel.shape[1]
    #     self.start_vel = start_vel
    #     self.start_pos = start_pos
    #     self.goal_vel = goal_vel
    #     self.goal_pos = goal_pos


    def calculatePositions(self, jerks, startVel, startPos, t):
        trajLen = len(jerks)
        summation = 0
        p = np.zeros([trajLen])
        for k in range(0, trajLen - 1):
            summation = 0
            for i in range(0, k + 1):
                summation += ((k - i)**2 + (k - i) + .3333) * jerks[i]
            p[k + 1] = (startPos + (k + 1) * t * startVel + 0.5 * t**3 * summation)
        self.positions = p


    # def positionGrad(self, jerks, t):
    #     gradP = []
    #     k = len(jerks)
    #     for i in range(0, k):
    #         gradP.append(0.5 * t**3 * ((k - i)**2 + (k - i) + 0.33333))
    #     return gradP


    def cost(self, jerks, startVel, startPos, targetVel, targetPos, t):
        self.calculatePositions(jerks, startVel, startPos, t)
        cost = 0
        # cost = (vtarget - velResult)**2 + (ptarget - posResult)**2
        return cost


    # def costGrad(self, jerks, targetVel, targetPos, startVel, startPos, t):
    #     velResult = velocity(jerks, v0, t)
    #     posResult = position(jerks, p0, v0, t)
    #     velGrad = velocityGrad(jerks, t)
    #     posGrad = positionGrad(jerks, t)
    #     costGrad = []
    #     for i in range(0, len(jerks)):
    #         costGrad.append(2 * (vtarget - velResult) * velGrad[i] + 2 * (ptarget - posResult) * posGrad[i])
    #     return costGrad


TIMESTEP = 0.5
INPUT_LENGTH = 10
STEPS = 2000
STEPSIZE = 0.0001

START_VEL = np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]])
START_POS = np.array([[4, 0, 0], [-4, 0, 0], [0, 0, 0], [0, 0, 4], [-3, -3, 0]])
TARGET_VEL = np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]])
TARGET_POS = np.array([[-4, 0, 0], [4, 0, 0], [0, 0, 0], [0, 0, -4], [3, 3, 0]])

jerks = []
# jerks = np.array([4.0, -7.0, -4.0, 9.0, 1.0, -1.0, 5.0, 3.0, 5.0, 2.0, 0.0, 4.0, 4.0, -9.0, 0.0, 8.0, 5.0, -3.0, 2.0, -3.0, 6.0, -5.0, 3.0])
jerks = np.array([4.0, -7.0, -4.0])

fun = Functions()
fun.calculatePositions(jerks, START_VEL, START_POS, TIMESTEP)
print(fun.positions)
