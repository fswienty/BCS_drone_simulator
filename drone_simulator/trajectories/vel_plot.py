import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider  # , Button, RadioButtons
from mpl_toolkits.mplot3d import Axes3D

traj = np.load(sys.path[0] + "/vel_traj.npy")
agents = traj.shape[0]
timesteps = traj.shape[1]

speed = np.zeros([agents, timesteps])
speed = np.sqrt(traj[:, :, 0]**2 + traj[:, :, 1]**2 + traj[:, :, 2]**2)

plt.xlabel('Timestep')
plt.ylabel('Speed (a.u.)')

plt.plot(speed[0])
plt.plot(speed[1])

SAVE = False
if SAVE:
    plt.savefig(sys.path[0] + "/force.pdf", dpi=None, facecolor='w', edgecolor='w',
                orientation='portrait', papertype=None, format=None,
                transparent=False, bbox_inches='tight', pad_inches=.1,
                frameon=None, metadata=None)
else:
    plt.show()
