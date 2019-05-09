import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

tt = np.load("pos_traj.npy")

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

for i in range(0, tt.shape[0]):
    ax.plot3D(tt[i,:,0], tt[i,:,1], tt[i,:,2])
    ax.scatter(tt[i,:,0], tt[i,:,1], tt[i,:,2])

plt.show()