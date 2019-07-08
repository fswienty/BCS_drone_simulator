import random


def velocity(jerks: list, v0: float, t: float) -> float:
    k = len(jerks)
    summation = 0
    for i in range(0, k):
        summation += ((k - i) + 0.5) * jerks[i]
    v = v0 + t**2 * summation
    return v


def velocityGrad(jerks: list, t: float) -> list:
    gradV = []
    k = len(jerks)
    for i in range(0, k):
        gradV.append(t**2 * (k - i + 0.5))
    return gradV


def position(jerks: list, p0: float, v0: float, t: float) -> float:
    k = len(jerks)
    summation = 0
    for i in range(0, k):
        summation += ((k - i)**2 + (k - i) + 0.33333) * jerks[i]
    p = p0 + (k + 1) * v0 + 0.5 * t**3 * summation
    return p


def positionGrad(jerks: list, t: float) -> list:
    gradP = []
    k = len(jerks)
    for i in range(0, k):
        gradP.append(0.5 * t**3 * ((k - i)**2 + (k - i) + 0.33333))
    return gradP


def cost(jerks: list, ptarget, vtarget, p0, v0, t) -> float:
    velResult = velocity(jerks, v0, t)
    posResult = position(jerks, p0, v0, t)
    print("Vel: {0} Pos: {1}".format(velResult, posResult))
    cost = (vtarget - velResult)**2 + (ptarget - posResult)**2
    return cost


INITIAL_VEL = 0
INITIAL_POS = 0
TARGET_POS = 2
TARGET_VEL = 0
TIMESTEP = 0.5
LENGTH = 10
OPTIMIZATION_STEPS = 20
jerks = []
for i in range(0, LENGTH):
    rand = random.gauss(0, 1)
    jerks.append(rand)

print("initial inputs: ", jerks)
print(cost(jerks, TARGET_POS, TARGET_VEL, INITIAL_POS, INITIAL_VEL, TIMESTEP))
# optimization here
for i in range(0, OPTIMIZATION_STEPS):
    pass

# velResult = velocity(jerks, INITIAL_VEL, TIMESTEP)
# posResult = position(jerks, INITIAL_POS, INITIAL_VEL, TIMESTEP)
# velGradResult = velocityGrad(jerks, TIMESTEP)
# posGradResult = positionGrad(jerks, TIMESTEP)
# print("Vel: {0} Pos: {1} VelGrad: {2} PosGrad: {3}".format(velResult, posResult, velGradResult, posGradResult))
# print("Vel: {0} Pos: {1}".format(velResult, posResult))
