import sys
import random
import numpy as np
# import math
# from autograd import grad


class CostFunctions():

    positions = 0
    velocities = 0

    wVel = 0
    wPos = 0
    wCol = 0
    collDist = 0

    def __init__(self, wVel, wPos, wCol, collDist, agents, trajLen, dim, startVel, startPos, targetVel, targetPos, timestep):
        self.wVel = wVel
        self.wPos = wPos
        self.wCol = wCol
        self.collDist = collDist

        self.agents = agents
        self.trajLen = trajLen
        self.dim = dim
        self.startVel = startVel
        self.startPos = startPos
        self.targetVel = targetVel
        self.targetPos = targetPos
        self.t = timestep


    def _calculateTrajectories(self, jerks):
        positionSummation = 0
        v = np.zeros([self.agents, self.trajLen, self.dim])
        p = np.zeros([self.agents, self.trajLen, self.dim])
        v[:, 0, :] = self.startVel
        p[:, 0, :] = self.startPos
        for k in range(0, self.trajLen - 1):
            velocitySummation = 0
            positionSummation = 0
            for i in range(0, k + 1):
                velocitySummation += ((k - i) + 0.5) * jerks[:, i, :]
                positionSummation += ((k - i)**2 + (k - i) + 0.3333) * jerks[:, i, :]
            v[:, k + 1, :] = self.startVel + self.t**2 * velocitySummation
            p[:, k + 1, :] = self.startPos + (k + 1) * self.t * self.startVel + 0.5 * self.t**3 * positionSummation
        self.velocities = v
        self.positions = p


    def _velocityGrad(self, jerks, k):
        velGrad = np.zeros([self.agents, self.trajLen, self.dim])
        for i in range(0, k):
            velGrad[:, i, :] = self.t**2 * ((k - i) + 0.5)
        for i in range(k, self.trajLen):
            velGrad[:, i, :] = 0
        return velGrad


    def _positionGrad(self, jerks, k):
        posGrad = np.zeros([self.agents, self.trajLen, self.dim])
        for i in range(0, k):
            posGrad[:, i, :] = 0.5 * self.t**3 * ((k - i)**2 + (k - i) + 0.3333)
        for i in range(k, self.trajLen):
            posGrad[:, i, :] = 0
        return posGrad


    def cost(self, jerks):
        self._calculateTrajectories(jerks)
        cost = 0
        cost += np.sum(self.wVel * (self.velocities[:, -1, :] - self.targetVel)**2)  # add target velocity cost
        cost += np.sum(self.wPos * (self.positions[:, -1, :] - self.targetPos)**2)  # add target position cost

        # add drone-drone collision cost
        for ag1 in range(0, self.agents):
            for ag2 in range(ag1 + 1, self.agents):
                posDiff = self.positions[ag1, :, :] - self.positions[ag2, :, :]
                for step in range(0, self.trajLen):
                    dist = np.linalg.norm(posDiff[step, :])
                    if dist < self.collDist:
                        cost += self.wCol * (1 - dist / self.collDist)**2
        return cost


    def costGrad(self, jerks):
        costGrad = np.zeros([self.agents, self.trajLen, self.dim])

        # gradient due to difference between target and actual end velcity/position
        endVelGrad = self._velocityGrad(jerks, self.trajLen)
        endPosGrad = self._positionGrad(jerks, self.trajLen)
        for i in range(0, self.trajLen):
            costGrad[:, i, :] += self.wVel * 2 * (self.velocities[:, -1, :] - self.targetVel) * endVelGrad[:, i, :]
            costGrad[:, i, :] += self.wPos * 2 * (self.positions[:, -1, :] - self.targetPos) * endPosGrad[:, i, :]

        # gradient due to drone-drone collisions
        for ag1 in range(0, self.agents):
            for ag2 in range(ag1 + 1, self.agents):
                posDiff = self.positions[ag1, :, :] - self.positions[ag2, :, :]
                for step in range(0, self.trajLen):
                    dist = np.linalg.norm(posDiff[step, :])
                    if dist < self.collDist:
                        positionGrad = self._positionGrad(jerks, step)
                        grad = self.wCol * 2 * (1 - posDiff[step, :] / self.collDist) * (positionGrad[ag2, :, :]) / self.collDist
                        costGrad[ag1, :, :] += grad
                        costGrad[ag2, :, :] -= grad

        return costGrad


    def costGradBlind(self, jerks):
        costGrad = np.zeros([self.agents, self.trajLen, self.dim])

        # gradient due to difference between target and actual end velcity/position
        endVelGrad = self._velocityGrad(jerks, self.trajLen)
        endPosGrad = self._positionGrad(jerks, self.trajLen)
        for i in range(0, self.trajLen):
            costGrad[:, i, :] += self.wVel * 2 * (self.velocities[:, -1, :] - self.targetVel) * endVelGrad[:, i, :]
            costGrad[:, i, :] += self.wPos * 2 * (self.positions[:, -1, :] - self.targetPos) * endPosGrad[:, i, :]

        return costGrad


# def momentumGradientDescent(costFunction, gradientFunction, problemDefinition: ProblemDefinition, initialJerks=0):
#     pd = problemDefinition
#     parameters = 0
#     if initialJerks != 0:
#         parameters = initialJerks
#     lastGradient = np.zeros([pd.agents, pd.trajLen, pd.dim])
#     for i in range(0, pd.steps):
#         cost = costFun.cost(parameters, pd.startVel, pd.startPos, pd.targetVel, pd.targetPos, pd.timestep)
#         gradient = costFun.costGrad(parameters, pd.startVel, pd.startPos, pd.targetVel, pd.targetPos, pd.timestep)
#         print("Iteration {} Cost = {}".format(i, cost))
#         gradient += 0.9 * lastGradient
#         lastGradient = gradient
#         parameters -= STEPSIZE * gradient
#         parameters = np.clip(parameters, -MAXJERK, MAXJERK)
#     return parameters


# AGENT DIM
# STARTVEL = np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]])
# STARTPOS = np.array([[4, 0, 0], [-4, 0, 0], [0, 0, 0], [0, 0, 4], [-3, -3, 0]])
# TARGETVEL = np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]])
# TARGETPOS = np.array([[-4, 0, 0], [4, 0, 0], [0, 0, 0], [0, 0, -4], [3, 3, 0]])
# STARTVEL = np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]])
# STARTPOS = np.array([[4, 0, 0], [-4, 0, 0], [0, 4, 0], [0, -4, 0], [0, 0, 4], [0, 0, -4]])
# TARGETVEL = np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]])
# TARGETPOS = np.array([[-4, 0, 0], [4, 0, 0], [0, -4, 0], [0, 4, 0], [0, 0, -4], [0, 0, 4]])
STARTVEL = np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]])
STARTPOS = np.array([[4, 0, 0], [-4, 0, 0], [0, 4, 0], [0, -4, 0], [0, 0, 4], [0, 0, -4]])
TARGETVEL = np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]])
TARGETPOS = np.array([[-4, 0, 0], [4, 0, 0], [0, -4, 0], [0, 4, 0], [0, 0, -4], [0, 0, 4]])
AGENTS = STARTVEL.shape[0]
TRAJLEN = 20
DIM = STARTVEL.shape[1]

TIMESTEP = 0.5
MAXJERK = 2
COLLDIST = 2
PRESTEPS = 200  # amount of steps for the initial gradient descend without collisions
STEPS = 700  # amount of steps for the final gradient descent with collisions
STEPSIZE = 0.00005

# AGENT TRAJLEN DIM
# jerks = randomJerk(AGENTS, TRAJLEN, 1)
jerks = np.zeros([AGENTS, TRAJLEN, DIM])

costFun = CostFunctions(5, 1, 5, COLLDIST, AGENTS, TRAJLEN, DIM, STARTVEL, STARTPOS, TARGETVEL, TARGETPOS, TIMESTEP)

# find initial solutions that don't consider collisions
lastGradient = np.zeros([AGENTS, TRAJLEN, DIM])
for i in range(0, PRESTEPS):
    cost = costFun.cost(jerks)
    gradient = costFun.costGradBlind(jerks,)
    print("Pre iteration {} cost = {}".format(i, cost))
    gradient += 0.9 * lastGradient
    lastGradient = gradient
    jerks -= STEPSIZE * gradient
    jerks = np.clip(jerks, -MAXJERK, MAXJERK)

# refinde solutions with collisions
lastGradient = np.zeros([AGENTS, TRAJLEN, DIM])
for i in range(0, STEPS):
    cost = costFun.cost(jerks)
    gradient = costFun.costGrad(jerks)
    print("Iteration {} cost = {}".format(i, cost))
    gradient += 0.9 * lastGradient
    lastGradient = gradient
    jerks -= STEPSIZE * gradient
    jerks = np.clip(jerks, -MAXJERK, MAXJERK)


print("### FINAL VELOCITY DIFFERENCE ###")
print(TARGETVEL - costFun.velocities[:, -1, :])
print("### FINAL POSITIONS DIFFERENCE ###")
print(TARGETPOS - costFun.positions[:, -1, :])

# np.save(sys.path[0] + "/trajectories/vel_traj.npy", fun.velocities)
np.save(sys.path[0] + "/trajectories/pos_traj.npy", costFun.positions)


# def randomJerk(agents, trajLen, maxJerk):
#     jerks = np.zeros([agents, trajLen, 3])
#     for i in range(0, agents):
#         tmp = np.zeros([trajLen, 3])
#         for j in range(0, trajLen):
#             tmp[j] = [random.uniform(-maxJerk, maxJerk), random.uniform(-maxJerk, maxJerk), random.uniform(-maxJerk, maxJerk)]
#         jerks[i] = tmp
#     return jerks
