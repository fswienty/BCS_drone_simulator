import sys
import random
import numpy as np
import math


class CostFunctions():

    positions = 0
    velocities = 0

    def __init__(self, wVel, wPos, wCol, minDist, agents, timesteps, dim, startVel, startPos, targetVel, targetPos, t):
        self.wVel = wVel
        self.wPos = wPos
        self.wCol = wCol
        self.minDist = minDist

        self.agents = agents
        self.timesteps = timesteps
        self.dim = dim
        self.startVel = startVel
        self.startPos = startPos
        self.targetVel = targetVel
        self.targetPos = targetPos
        self.t = t


    def _calculateTrajectories(self, jerks):
        positionSum = 0
        v = np.zeros([self.agents, self.timesteps, self.dim])
        p = np.zeros([self.agents, self.timesteps, self.dim])
        v[:, 0, :] = self.startVel
        p[:, 0, :] = self.startPos
        for k in range(0, self.timesteps - 1):
            velocitySum = 0
            positionSum = 0
            for i in range(0, k + 1):
                velocitySum += ((k - i) + 0.5) * jerks[:, i, :]
                positionSum += ((k - i)**2 + (k - i) + 0.3333) * jerks[:, i, :]
            v[:, k + 1, :] = self.startVel + self.t**2 * velocitySum
            p[:, k + 1, :] = self.startPos + (k + 1) * self.t * self.startVel + 0.5 * self.t**3 * positionSum
        self.velocities = v
        self.positions = p


    def _velocityGrad(self, jerks, k):
        velGrad = np.zeros([self.agents, self.timesteps, self.dim])
        for i in range(0, k):
            velGrad[:, i, :] = self.t**2 * ((k - i) + 0.5)
        for i in range(k, self.timesteps):
            velGrad[:, i, :] = 0
        return velGrad


    def _positionGrad(self, jerks, k):
        posGrad = np.zeros([self.agents, self.timesteps, self.dim])
        for i in range(0, k):
            posGrad[:, i, :] = 0.5 * self.t**3 * ((k - i)**2 + (k - i) + 0.3333)
        # for i in range(k, self.timesteps):
        #     posGrad[:, i, :] = 0
        return posGrad


    def cost(self, jerks):
        self._calculateTrajectories(jerks)
        cost = 0
        cost += np.sum(self.wVel * (self.velocities[:, -1, :] - self.targetVel)**2)  # add target velocity cost
        cost += np.sum(self.wPos * (self.positions[:, -1, :] - self.targetPos)**2)  # add target position cost

        # add drone-drone conflict cost
        for ag1 in range(0, self.agents):
            for ag2 in range(ag1 + 1, self.agents):
                posDiff = self.positions[ag1, :, :] - self.positions[ag2, :, :]
                for step in range(0, self.timesteps):
                    dist = np.linalg.norm(posDiff[step, :])
                    if dist < self.minDist:
                        cost += self.wCol * (1 - dist / self.minDist)**2

        return cost


    def gradient(self, jerks):
        costGrad = np.zeros([self.agents, self.timesteps, self.dim])

        # gradient due to difference between target and actual end velocity/position
        endVelGrad = self._velocityGrad(jerks, self.timesteps)
        endPosGrad = self._positionGrad(jerks, self.timesteps)
        for i in range(0, self.timesteps):
            costGrad[:, i, :] += self.wVel * 2 * (self.velocities[:, -1, :] - self.targetVel) * endVelGrad[:, i, :]
            costGrad[:, i, :] += self.wPos * 2 * (self.positions[:, -1, :] - self.targetPos) * endPosGrad[:, i, :]

        # gradient due to drone-drone conflicts
        for ag1 in range(0, self.agents):
            for ag2 in range(ag1 + 1, self.agents):
                posDiff = self.positions[ag1, :, :] - self.positions[ag2, :, :]
                for step in range(0, self.timesteps):
                    dist = np.linalg.norm(posDiff[step, :])
                    if dist < self.minDist:
                        positionGrad = self._positionGrad(jerks, step)
                        grad = self.wCol * 2 * (1 - posDiff[step, :] / self.minDist) * (positionGrad[ag2, :, :]) / self.minDist
                        costGrad[ag1, :, :] += grad
                        costGrad[ag2, :, :] -= grad

        return costGrad


    def gradientNoCollision(self, jerks):
        costGrad = np.zeros([self.agents, self.timesteps, self.dim])

        # gradient due to difference between target and actual end velcity/position
        endVelGrad = self._velocityGrad(jerks, self.timesteps)
        endPosGrad = self._positionGrad(jerks, self.timesteps)
        for i in range(0, self.timesteps):
            costGrad[:, i, :] += self.wVel * 2 * (self.velocities[:, -1, :] - self.targetVel) * endVelGrad[:, i, :]
            costGrad[:, i, :] += self.wPos * 2 * (self.positions[:, -1, :] - self.targetPos) * endPosGrad[:, i, :]

        return costGrad


def momentumGradientDescent(costFunction, costTarget, gradientFunction, initialParameters, parameterLimit, stepsize, maxSteps, momentum):
    parameters = initialParameters
    v = np.zeros(initialParameters.shape)
    for i in range(0, maxSteps):
        cost = costFunction(parameters)
        gradient = gradientFunction(parameters)
        print("Iteration {} Cost = {}".format(i, cost))

        if(cost < costTarget):
            print("stopping due to reaching cost target")
            return parameters

        v = momentum * v + stepsize * gradient
        parameters -= v
        parameters = np.clip(parameters, -parameterLimit, parameterLimit)

    print("stopping due to reaching step limit")
    return parameters


def adamGradientDescent(costFunction, costTarget, gradientFunction, initialParameters, parameterLimit, stepsize, maxSteps, beta1, beta2, eps):
    parameters = initialParameters
    m = np.zeros(initialParameters.shape)
    v = np.zeros(initialParameters.shape)
    for i in range(0, maxSteps):
        cost = costFunction(parameters)
        gradient = gradientFunction(parameters)
        print("Iteration {} Cost = {}".format(i, cost))

        if(cost < costTarget):
            print("stopping due to reaching cost target")
            return parameters

        curStepsize = stepsize / (1 + 0.01 * i)
        # curStepsize = stepsize

        m = beta1 * m + (1 - beta1) * gradient
        v = beta2 * v + (1 - beta2) * gradient**2
        mHat = m / (1 - beta1)
        vHat = v / (1 - beta2)
        parameters -= curStepsize / (np.sqrt(vHat) + eps) * mHat
        parameters = np.clip(parameters, -parameterLimit, parameterLimit)

    print("stopping due to reaching step limit")
    return parameters


# first position is at the center towards the window, then counter clockwise
def circleCoordinates(amount, radius, angleOffset):
    coordinateArray = np.zeros([amount, 3])
    angleStep = 360 / amount
    for i in range(0, amount):
        currRad = math.radians(i * angleStep + angleOffset)
        coordinateArray[i] = np.array([radius * math.cos(currRad), radius * math.sin(currRad), 1])
    return coordinateArray


# AGENT DIM
# "random"
# STARTVEL = np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]])
# STARTPOS = np.array([[4, 0, 0], [-4, 0, 0], [0, 0, 0], [0, 0, 4], [-3, -3, 0]])
# TARGETVEL = np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]])
# TARGETPOS = np.array([[-4, 0, 0], [4, 0, 0], [0, 0, 0], [0, 0, -4], [3, 3, 0]])

# 3 axis position swap
# STARTVEL = np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]])
# STARTPOS = np.array([[4, 0, 0], [-4, 0, 0], [0, 4, 0], [0, -4, 0], [0, 0, 4], [0, 0, -4], [0, 0, 0]])
# TARGETVEL = np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]])
# TARGETPOS = np.array([[-4, 0, 0], [4, 0, 0], [0, -4, 0], [0, 4, 0], [0, 0, -4], [0, 0, 4], [0, 0, 0]])

# pentagram
# STARTVEL = np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]])
# STARTPOS = np.array([[-2, -2, 0], [3, 1, 0], [-3, 1, 0], [2, -2, 0], [0, 4, 0]])
# TARGETVEL = np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]])
# TARGETPOS = np.array([[3, 1, 0], [-3, 1, 0], [2, -2, 0], [0, 4, 0], [-2, -2, 0]])

# line swap
# STARTVEL = np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]])
# STARTPOS = np.array([[3, -4, 0], [3, -2, 0], [3, 0, 0], [3, 2, 0], [3, 4, 0], [-3, -4, 0], [-3, -2, 0], [-3, 0, 0], [-3, 2, 0], [-3, 4, 0]])
# TARGETVEL = np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]])
# TARGETPOS = np.array([[-3, -4, 0], [-3, -2, 0], [-3, 0, 0], [-3, 2, 0], [-3, 4, 0], [3, -4, 0], [3, -2, 0], [3, 0, 0], [3, 2, 0], [3, 4, 0]])

# drone wall
# STARTVEL = np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]])
# STARTPOS = np.array([[-2, 0, -2], [-2, 0, 0], [-2, 0, 2], [0, 0, -2], [0, 0, 0], [0, 0, 2], [2, 0, -2], [2, 0, 0], [2, 0, 2], [0, -3, 0]])
# TARGETVEL = np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]])
# TARGETPOS = np.array([[-2, 0, -2], [-2, 0, 0], [-2, 0, 2], [0, 0, -2], [0, 0, 0], [0, 0, 2], [2, 0, -2], [2, 0, 0], [2, 0, 2], [0, 3, 0]])

# 3 axis swap
# STARTVEL = np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]])
# STARTPOS = np.array([[0, 0, .3], [0, 0, 1.3], [.5, 0, .8], [-.5, 0, .8], [0, .5, .8], [0, -.5, .8]])
# TARGETVEL = np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]])
# TARGETPOS = np.array([[0, 0, 1.3], [0, 0, 0.3], [-.5, 0, .8], [.5, 0, .8], [0, -.5, .8], [0, .5, .8]])


# circle swap
AGENTS = 6
STARTVEL = np.zeros([AGENTS, 3])
STARTPOS = circleCoordinates(AGENTS, 1, 0)
TARGETVEL = np.zeros([AGENTS, 3])
TARGETPOS = circleCoordinates(AGENTS, 1, 180)
print("initial distance: {}".format(np.linalg.norm(STARTPOS[0] - STARTPOS[1])))


AGENTS = STARTVEL.shape[0]
TIMESTEPS = 20
DIM = STARTVEL.shape[1]

TIMESTEP = .5
MAXJERK = 0.1

# weights for changing how much the final velocity error, the final position error and the drone-drone conflicts are considered
# try changing these if your results are bad
WVEL = 5
WPOS = 5
WCOL = .5

MINDIST = .6

costFun = CostFunctions(WVEL, WPOS, WCOL, MINDIST, AGENTS, TIMESTEPS, DIM, STARTVEL, STARTPOS, TARGETVEL, TARGETPOS, TIMESTEP)

# AGENT TIMESTEP DIM
jerks = np.zeros([AGENTS, TIMESTEPS, DIM])
# randomize jerks
# maxRandom = 0.05
# for i in range(0, AGENTS):
#     tmp = np.zeros([TIMESTEPS, 3])
#     for j in range(0, TIMESTEPS):
#         tmp[j] = [random.uniform(-maxRandom, maxRandom), random.uniform(-maxRandom, maxRandom), random.uniform(-maxRandom, maxRandom)]
#     jerks[i] = tmp

# COST TARGET GRAD INITIALPARAM PARAMLIMIT STEPSIZE MAXSTEPS MOMENTUM
# initialJerks = momentumGradientDescent(costFun.cost, 0, costFun.gradientNoCollision, jerks, MAXJERK, 0.0005, 50, 0.9)
# momentumGradientDescent(costFun.cost, 0.05, costFun.gradient, initialJerks, MAXJERK, 0.0005, 700, 0.9)

# COST TARGET GRAD INITIALPARAM PARAMLIMIT STEPSIZE MAXSTEPS BETA1 BETA2 EPSILON
initialResult = adamGradientDescent(costFun.cost, 0, costFun.gradientNoCollision, jerks, MAXJERK, 0.01, 50, 0.95, 0.99, 10**(-8))
result = adamGradientDescent(costFun.cost, 0.05, costFun.gradient, jerks, MAXJERK, 0.005, 4000, 0.95, 0.99, 10**(-8))

print("\n ##### RESULTS #####")
print("Highest final velocity difference:", np.max(np.linalg.norm(TARGETVEL - costFun.velocities[:, -1, :], axis=1)))
print("Highest final position difference:", np.max(np.linalg.norm(TARGETPOS - costFun.positions[:, -1, :], axis=1)))
smallestDistance = sys.float_info.max
smallestDistanceTimestep = -1
smallestDistanceAgent1 = -1
smallestDistanceAgent2 = -1
for ag1 in range(0, costFun.agents):
    for ag2 in range(ag1 + 1, costFun.agents):
        posDiff = costFun.positions[ag1, :, :] - costFun.positions[ag2, :, :]
        for step in range(0, costFun.timesteps):
            dist = np.linalg.norm(posDiff[step, :])
            if dist < smallestDistance:
                smallestDistance = dist
                smallestDistanceTimestep = step
                smallestDistanceAgent1 = ag1
                smallestDistanceAgent2 = ag2
print("Smallest distance: {0} at timestep {1} between agents {2} and {3}".format(smallestDistance, smallestDistanceTimestep, smallestDistanceAgent1, smallestDistanceAgent2), "\n")

# np.save(sys.path[0] + "/trajectories/vel_traj.npy", fun.velocities)
np.save(sys.path[0] + "/trajectories/pos_traj.npy", costFun.positions)
