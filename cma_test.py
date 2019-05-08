import numpy as np
import matplotlib.pyplot as plt
import cma

def function(x):
    x = np.asarray(x)
    return x[0]**2 + (x[1]-304)**2

es = cma.CMAEvolutionStrategy(2 * [0], 0.5)
print(es.opts.defaults())

