



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


def eh(l: list):
    k = len(l)
    print("k =", k)
    for i in range(0, k):
        print(i)


TARGET_POS = 2
TARGET_VEL = 0
inputs = [1, .5, .3, .7, -1, -.4, .1]
