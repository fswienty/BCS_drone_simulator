import sys
import random
import numpy as np
# import math
# from autograd import grad



class Functions():

    positions = 0
    velocities = 0

    wVel = 0
    wPos = 0
    wCol = 0
    collDist = 0

    def __init__(self, wVel, wPos, wCol, collDist):
        self.wVel = wVel
        self.wPos = wPos
        self.wCol = wCol
        self.collDist = collDist


    def calculateTrajectory(self, jerks, startVel, startPos, t):
        agents = jerks.shape[0]
        trajLen = jerks.shape[1]
        dim = jerks.shape[2]
        positionSummation = 0
        v = np.zeros([agents, trajLen, dim])
        p = np.zeros([agents, trajLen, dim])
        v[:, 0, :] = startVel
        p[:, 0, :] = startPos
        for k in range(0, trajLen - 1):
            velocitySummation = 0
            positionSummation = 0
            for i in range(0, k + 1):
                velocitySummation += ((k - i) + 0.5) * jerks[:, i, :]
                positionSummation += ((k - i)**2 + (k - i) + 0.3333) * jerks[:, i, :]
            v[:, k + 1, :] = startVel + t**2 * velocitySummation
            p[:, k + 1, :] = startPos + (k + 1) * t * startVel + 0.5 * t**3 * positionSummation
        self.velocities = v
        self.positions = p


    def velocityGrad(self, jerks, k, t):
        agents = jerks.shape[0]
        trajLen = jerks.shape[1]
        dim = jerks.shape[2]
        velGrad = np.zeros([agents, trajLen, dim])
        for i in range(0, k):
            velGrad[:, i, :] = t**2 * ((k - i) + 0.5)
        for i in range(k, trajLen):
            velGrad[:, i, :] = 0
        return velGrad


    def positionGrad(self, jerks, k, t):
        agents = jerks.shape[0]
        trajLen = jerks.shape[1]
        dim = jerks.shape[2]
        posGrad = np.zeros([agents, trajLen, dim])
        for i in range(0, k):
            # posGrad.append(0.5 * t**3 * ((k - i)**2 + (k - i) + 0.3333))
            posGrad[:, i, :] = 0.5 * t**3 * ((k - i)**2 + (k - i) + 0.3333)
        for i in range(k, trajLen):
            posGrad[:, i, :] = 0
        return posGrad


    def cost(self, jerks, startVel, startPos, targetVel, targetPos, t):
        self.calculateTrajectory(jerks, startVel, startPos, t)
        agents = self.positions.shape[0]
        trajLen = self.positions.shape[1]
        # dim = self.positions.shape[2]
        cost = 0
        cost += np.sum(self.wVel * (targetVel - self.velocities[:, -1, :])**2)  # add target velocity error
        cost += np.sum(self.wPos * (targetPos - self.positions[:, -1, :])**2)  # add target position error
        for ag1 in range(0, agents):
            for ag2 in range(ag1 + 1, agents):
                posDiff = self.positions[ag1, :, :] - self.positions[ag2, :, :]
                # print("### {} vs {} ###".format(ag1, ag2))
                # print(posDiff)
                for step in range(0, trajLen):
                    dist = np.linalg.norm(posDiff[step])
                    if dist < self.collDist:
                        cost += self.wCol * (1 - dist / self.collDist)**2
        return cost


    def costGrad(self, jerks, startVel, startPos, targetVel, targetPos, t):
        agents = jerks.shape[0]
        trajLen = jerks.shape[1]
        dim = jerks.shape[2]
        endVelGrad = self.velocityGrad(jerks, trajLen, t)
        endPosGrad = self.positionGrad(jerks, trajLen, t)
        costGrad = np.zeros([agents, trajLen, dim])
        for i in range(0, trajLen):
            costGrad[:, i, :] += self.wVel * 2 * (targetVel - self.velocities[:, -1, :]) * endVelGrad[:, i, :]
            costGrad[:, i, :] += self.wPos * 2 * (targetPos - self.positions[:, -1, :]) * endPosGrad[:, i, :]
        # add code for collision gradient
        return costGrad


def randomJerk(agents, trajLen, maxJerk):
    jerks = np.zeros([agents, trajLen, 3])
    for i in range(0, agents):
        tmp = np.zeros([trajLen, 3])
        for j in range(0, trajLen):
            tmp[j] = [random.uniform(-maxJerk, maxJerk), random.uniform(-maxJerk, maxJerk), random.uniform(-maxJerk, maxJerk)]
        jerks[i] = tmp
    return jerks


# AGENT DIM
# START_VEL = np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]])
# START_POS = np.array([[4, 0, 0], [-4, 0, 0], [0, 0, 0], [0, 0, 4], [-3, -3, 0]])
# TARGET_VEL = np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]])
# TARGET_POS = np.array([[-4, 0, 0], [4, 0, 0], [0, 0, 0], [0, 0, -4], [3, 3, 0]])
START_VEL = np.array([[0, 0, 0], [0, 0, 0]])
START_POS = np.array([[4, 0, 0], [-4, 0, 0]])
TARGET_VEL = np.array([[0, 0, 0], [0, 0, 0]])
TARGET_POS = np.array([[-4, 0, 0], [4, 0, 0]])
AGENTS = START_VEL.shape[0]
TRAJLEN = 10
DIM = START_VEL.shape[1]

TIMESTEP = 1
STEPS = 400
STEPSIZE = 0.00005

# AGENT TRAJLEN DIM
# jerks = np.array([[[1, 0, 0]], [[2, 1, 0]], [[0, 0, 0]], [[0, 0, 0]], [[5, 0, -7]]])

fun = Functions(5, 1, 10, 2)
# randJerk = randomJerk(5, 10, 1)
# np.save(sys.path[0] + "/trajectories/jerk_traj2.npy", randJerk)
# jerks = np.load(sys.path[0] + "/trajectories/jerk_traj.npy")
jerks = np.zeros([AGENTS, TRAJLEN, DIM])

for i in range(0, STEPS):
    # agents = jerks.shape[0]
    # trajLen = jerks.shape[1]
    # dim = jerks.shape[2]
    cost = fun.cost(jerks, START_VEL, START_POS, TARGET_VEL, TARGET_POS, TIMESTEP)
    gradient = fun.costGrad(jerks, START_VEL, START_POS, TARGET_VEL, TARGET_POS, TIMESTEP)
    # print("current cost = {} current grad = {}".format(cost, gradient))
    print("ITERATION {} COST = {}".format(i, cost))
    jerks += STEPSIZE * gradient

print("### FINAL VELOCITIES ###")
print(fun.velocities[:, -1, :])
print("### FINAL POSITIONS ###")
print(fun.positions[:, -1, :])

# np.save(sys.path[0] + "/trajectories/vel_traj.npy", fun.velocities)
np.save(sys.path[0] + "/trajectories/pos_traj.npy", fun.positions)
