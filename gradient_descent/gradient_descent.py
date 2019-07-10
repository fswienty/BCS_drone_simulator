import random
import math
from autograd import grad
import numpy as np


def velocity(jerks, v0, t):
    k = len(jerks)
    summation = 0
    for i in range(0, k):
        summation += ((k - i) + 0.5) * jerks[i]
    v = v0 + t**2 * summation
    return v


def velocityGrad(jerks, t):
    gradV = []
    k = len(jerks)
    for i in range(0, k):
        gradV.append(t**2 * (k - i + 0.5))
    return gradV


def position(jerks, p0, v0, t):
    k = len(jerks)
    summation = 0
    for i in range(0, k):
        summation += ((k - i)**2 + (k - i) + 0.33333) * jerks[i]
    p = p0 + (k + 1) * t * v0 + 0.5 * t**3 * summation
    return p


def positionGrad(jerks, t):
    gradP = []
    k = len(jerks)
    for i in range(0, k):
        gradP.append(0.5 * t**3 * ((k - i)**2 + (k - i) + 0.33333))
    return gradP


def cost(jerks, ptarget, vtarget, p0, v0, t):
    velResult = velocity(jerks, v0, t)
    posResult = position(jerks, p0, v0, t)
    cost = (vtarget - velResult)**2 + (ptarget - posResult)**2
    return cost


def costGrad(jerks, ptarget, vtarget, p0, v0, t):
    velResult = velocity(jerks, v0, t)
    posResult = position(jerks, p0, v0, t)
    velGrad = velocityGrad(jerks, t)
    posGrad = positionGrad(jerks, t)
    costGrad = []
    for i in range(0, len(jerks)):
        costGrad.append(2 * (vtarget - velResult) * velGrad[i] + 2 * (ptarget - posResult) * posGrad[i])
    return costGrad


INITIAL_VEL = 0
INITIAL_POS = 0
TARGET_POS = 2
TARGET_VEL = 0
TIMESTEP = 0.5
INPUT_LENGTH = 10
STEPS = 2000
STEPSIZE = 0.0001
jerks = []
#jerks = np.array([4.0, -7.0, -4.0, 9.0, 1.0, -1.0, 5.0, 3.0, 5.0, 2.0, 0.0, 4.0, 4.0, -9.0, 0.0, 8.0, 5.0, -3.0, 2.0, -3.0, 6.0, -5.0, 3.0])
jerks = np.array([4.0, -7.0, -4.0])

# for i in range(0, INPUT_LENGTH):
#     rand = random.gauss(0, 1)
#     jerks.append(rand)


# optimization here
# for i in range(0, STEPS):
#     c = cost(jerks, TARGET_POS, TARGET_VEL, INITIAL_POS, INITIAL_VEL, TIMESTEP)
#     gradient = costGrad(jerks, TARGET_POS, TARGET_VEL, INITIAL_POS, INITIAL_VEL, TIMESTEP)
#     # print("current cost = {} current grad = {}".format(c, grad))

#     endPos = position(jerks, INITIAL_POS, INITIAL_VEL, TIMESTEP)
#     endVel = velocity(jerks, INITIAL_VEL, TIMESTEP)
#     print("Iteration {}: current cost = {} endPos = {} endVel = {}".format(i, c, endPos, endVel))
#     currentStep = STEPSIZE
#     for j in range(0, len(jerks)):
#         jerks[j] += currentStep * gradient[j]


c = cost(jerks, TARGET_POS, TARGET_VEL, INITIAL_POS, INITIAL_VEL, TIMESTEP)
gradient = costGrad(jerks, TARGET_POS, TARGET_VEL, INITIAL_POS, INITIAL_VEL, TIMESTEP)
costAutograd = grad(cost)
autogradient = costAutograd(jerks, TARGET_POS, TARGET_VEL, INITIAL_POS, INITIAL_VEL, TIMESTEP)

print(c, gradient, autogradient)
