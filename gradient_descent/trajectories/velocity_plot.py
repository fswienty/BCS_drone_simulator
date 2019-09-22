import sys
import numpy as np
import matplotlib.pyplot as plt
# from matplotlib.widgets import Slider  # , Button, RadioButtons
# from mpl_toolkits.mplot3d import Axes3D

traj = np.load(sys.path[0] + "/pos_traj.npy")
agents = traj.shape[0]
timesteps = traj.shape[1]

test = traj[0, :, :]
plt.plot(test)

plt.show()
