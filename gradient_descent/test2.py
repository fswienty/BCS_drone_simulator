import autograd.numpy as np
from autograd import grad


def myFun(inp):
    return np.sum(np.square(inp))


inp = np.array([2., 7., -2.])
gradMyFun = grad(myFun)


print(myFun(inp))
print(gradMyFun(inp))
