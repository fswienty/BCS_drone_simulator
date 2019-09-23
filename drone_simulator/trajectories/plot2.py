import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider  # , Button, RadioButtons
from mpl_toolkits.mplot3d import Axes3D

traj = np.load(sys.path[0] + "/4circle_pos.npy")
agents = traj.shape[0]
timesteps = traj.shape[1]

print("Showing {2}D trajectories of {0} agents with {1} timesteps".format(traj.shape[0], traj.shape[1], traj.shape[2]))

fig = plt.figure()
# fig = plt.figure(figsize=(4, 35))
fig.subplots_adjust(bottom=.25, top=.75)
ax = fig.add_subplot(111, projection='3d')
# fig.subplots_adjust()


plotRange = 1

ax.set_xlim3d(-plotRange, plotRange)
ax.set_ylim3d(-plotRange, plotRange)
# ax.set_zlim3d(0, 2 * plotRange)
ax.set_zlim3d(.5, 1.5)
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')

ax.view_init(elev=32, azim=35)
fig.set_size_inches(10, 10)

# Turn off tick labels
# ax.set_xticklabels([])
# ax.set_yticklabels([])
# ax.set_zticklabels([])

step = timesteps - 1
for i in range(0, agents):
    trail = max(0, step - 999999)
    ax.plot3D(traj[i, trail:step + 1, 0], traj[i, trail:step + 1, 1], traj[i, trail:step + 1, 2])
    ax.scatter(traj[i, step, 0], traj[i, step, 1], traj[i, step, 2])

SAVE = True

if SAVE:
    plt.savefig(sys.path[0] + "/force.pdf", dpi=None, facecolor='w', edgecolor='w',
                orientation='portrait', papertype=None, format=None,
                transparent=False, bbox_inches='tight', pad_inches=.1,
                frameon=None, metadata=None)
else:
    plt.show()
