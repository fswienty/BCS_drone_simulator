import numpy as np
# pylint: disable=no-name-in-module
from panda3d.core import Vec3

class Matrix:

    def __init__(self, *args, **kwargs):
        self.T = np.array([[2.32, 0.37, 0.01, -1.15],[-0.24, 3.6, -0.02, -1.7],[-0.02, 0.05, 1.2, 0.16],[0, 0, 0, 1]])

    def transform(self, vector: Vec3) -> Vec3:
        vec = np.array([vector.x, vector.y, vector.z, 1])
        result = self.T.dot(vec)
        return Vec3(result[0], result[1], result[2])

mat = Matrix()
print("[0, 0, 0]->", mat.transform(Vec3(0,0,0)))
print("[1, 0, 0]->", mat.transform(Vec3(1,0,0)))
print("[0, 1, 0]->", mat.transform(Vec3(0,1,0)))
print("[0, 0, 1]->", mat.transform(Vec3(0,0,1)))
print("[1, 1, 0]->", mat.transform(Vec3(1,1,0)))
print("[1, 0, 1]->", mat.transform(Vec3(1,0,1)))
print("[0, 1, 1]->", mat.transform(Vec3(0,1,1)))
print("[1, 1, 1]->", mat.transform(Vec3(1,1,1)))

print("center floor->", mat.transform(Vec3(0.5,0.5,0)))
print("center air->", mat.transform(Vec3(0.5,0.5,1)))