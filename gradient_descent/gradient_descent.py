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
        cost += np.sum(self.wVel * (self.velocities[:, -1, :] - targetVel)**2)  # add target velocity error
        cost += np.sum(self.wPos * (self.positions[:, -1, :] - targetPos)**2)  # add target position error
        for ag1 in range(0, agents):
            for ag2 in range(ag1 + 1, agents):
                posDiff = self.positions[ag1, :, :] - self.positions[ag2, :, :]
                for step in range(0, trajLen):
                    dist = np.linalg.norm(posDiff[step, :])
                    if dist < self.collDist:
                        cost += self.wCol * (1 - dist / self.collDist)**2
        return cost


    def costGrad(self, jerks, startVel, startPos, targetVel, targetPos, t):
        agents = jerks.shape[0]
        trajLen = jerks.shape[1]
        dim = jerks.shape[2]
        costGrad = np.zeros([agents, trajLen, dim])

        # gradient due to difference between target and actual end velcity/position
        endVelGrad = self.velocityGrad(jerks, trajLen, t)
        endPosGrad = self.positionGrad(jerks, trajLen, t)
        for i in range(0, trajLen):
            costGrad[:, i, :] += self.wVel * 2 * (self.velocities[:, -1, :] - targetVel) * endVelGrad[:, i, :]
            costGrad[:, i, :] += self.wPos * 2 * (self.positions[:, -1, :] - targetPos) * endPosGrad[:, i, :]

        # gradient due to drone-drone collisions
        for ag1 in range(0, agents):
            for ag2 in range(ag1 + 1, agents):
                posDiff = self.positions[ag1, :, :] - self.positions[ag2, :, :]
                for step in range(0, trajLen):
                    dist = np.linalg.norm(posDiff[step, :])
                    if dist < self.collDist:
                        positionGrad = self.positionGrad(jerks, step, t)
                        grad = self.wCol * 2 * (1 - posDiff[step, :] / self.collDist) * (positionGrad[ag2, :, :]) / self.collDist
                        costGrad[ag1, :, :] += grad
                        costGrad[ag2, :, :] -= grad

        return costGrad

    def costGradBlind(self, jerks, startVel, startPos, targetVel, targetPos, t):
        agents = jerks.shape[0]
        trajLen = jerks.shape[1]
        dim = jerks.shape[2]
        costGrad = np.zeros([agents, trajLen, dim])

        # gradient due to difference between target and actual end velcity/position
        endVelGrad = self.velocityGrad(jerks, trajLen, t)
        endPosGrad = self.positionGrad(jerks, trajLen, t)
        for i in range(0, trajLen):
            costGrad[:, i, :] += self.wVel * 2 * (self.velocities[:, -1, :] - targetVel) * endVelGrad[:, i, :]
            costGrad[:, i, :] += self.wPos * 2 * (self.positions[:, -1, :] - targetPos) * endPosGrad[:, i, :]

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
# STARTVEL = np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]])
# STARTPOS = np.array([[4, 0, 0], [-4, 0, 0], [0, 0, 0], [0, 0, 4], [-3, -3, 0]])
# TARGETVEL = np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]])
# TARGETPOS = np.array([[-4, 0, 0], [4, 0, 0], [0, 0, 0], [0, 0, -4], [3, 3, 0]])
STARTVEL = np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]])
STARTPOS = np.array([[4, 0, 0], [-4, 0, 0], [0, 4, 0], [0, -4, 0], [0, 0, 4], [0, 0, -4]])
TARGETVEL = np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]])
TARGETPOS = np.array([[-4, 0, 0], [4, 0, 0], [0, -4, 0], [0, 4, 0], [0, 0, -4], [0, 0, 4]])
AGENTS = STARTVEL.shape[0]
TRAJLEN = 20
DIM = STARTVEL.shape[1]

TIMESTEP = 0.5
MAXJERK = 2
STEPS = 1000
STEPSIZE = 0.00005

# AGENT TRAJLEN DIM
# jerks = randomJerk(AGENTS, TRAJLEN, 1)
jerks = np.zeros([AGENTS, TRAJLEN, DIM])

fun = Functions(5, 1, 5, 2)

# find initial solutions that don't consider collisions
lastGradient = np.zeros([AGENTS, TRAJLEN, DIM])
for i in range(0, int(STEPS / 5)):
    cost = fun.cost(jerks, STARTVEL, STARTPOS, TARGETVEL, TARGETPOS, TIMESTEP)
    gradient = fun.costGradBlind(jerks, STARTVEL, STARTPOS, TARGETVEL, TARGETPOS, TIMESTEP)
    print("Pre iteration {} cost = {}".format(i, cost))
    gradient += 0.9 * lastGradient
    lastGradient = gradient
    jerks -= STEPSIZE * gradient
    jerks = np.clip(jerks, -MAXJERK, MAXJERK)

# refinde solutions with collisions
lastGradient = np.zeros([AGENTS, TRAJLEN, DIM])
for i in range(0, STEPS):
    cost = fun.cost(jerks, STARTVEL, STARTPOS, TARGETVEL, TARGETPOS, TIMESTEP)
    gradient = fun.costGrad(jerks, STARTVEL, STARTPOS, TARGETVEL, TARGETPOS, TIMESTEP)
    print("Iteration {} cost = {}".format(i, cost))
    gradient += 0.9 * lastGradient
    lastGradient = gradient
    jerks -= STEPSIZE * gradient
    jerks = np.clip(jerks, -MAXJERK, MAXJERK)


print("### FINAL VELOCITY DIFFERENCE ###")
print(TARGETVEL - fun.velocities[:, -1, :])
print("### FINAL POSITIONS DIFFERENCE ###")
print(TARGETPOS - fun.positions[:, -1, :])

# np.save(sys.path[0] + "/trajectories/vel_traj.npy", fun.velocities)
np.save(sys.path[0] + "/trajectories/pos_traj.npy", fun.positions)
