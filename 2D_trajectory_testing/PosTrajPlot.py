from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

TRAJ_LOCATION = Path("C:/Users/Florian_Swienty/Misc/dev/csharptest/csharptest/bin/Debug/netcoreapp2.1/traj.txt")

traj_xyz = np.loadtxt(TRAJ_LOCATION, delimiter=",")
traj_x = traj_xyz[0]
traj_y = traj_xyz[1]
traj_z = traj_xyz[2]

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

#ax.scatter(traj_x, traj_y, traj_z)
ax.plot(traj_x, traj_y, traj_z)
plt.show()