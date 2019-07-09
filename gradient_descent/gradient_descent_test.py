import numpy as np
from autograd import grad


def costFun(x):
    sum = 0
    for i in range(0, len(x)):
        sum = sum + x[i]**2
    return sum



x = np.array([1.4, -9.1, 4.0])
STEPS = 100
STEPSIZE = 0.3
# for i in range(0, STEPS):
#     cost = costFun(x)
#     gradient = gradCostFun(x)
#     print("current cost = {} current grad = {}".format(cost, gradient))
#     for j in range(0, len(x)):
#         x[j] -= STEPSIZE * gradient[j]


costAutograd = grad(costFun)
print(costFun(x), costAutograd(x))
