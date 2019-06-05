# Von Florian Swienty

import numpy as np

class CoordTransform:

    def __init__(self, *args, **kwargs):
        self.T = np.array([[2.32, 0.37, 0.01, -1.15],[-0.24, 3.6, -0.02, -1.7],[-0.02, 0.05, 1.2, 0.16],[0, 0, 0, 1]])


    def transformF2F(self, x, y, z):
        vec = np.array([x, y, z, 1])
        result = self.T.dot(vec)
        return result[0], result[1], result[2]