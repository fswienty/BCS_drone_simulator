import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider  # , Button, RadioButtons
from mpl_toolkits.mplot3d import Axes3D

tt = np.load(sys.path[0] + "/trajectories/pos_traj.npy")
agents = tt.shape[0]
traj_len = tt.shape[1]

print("Showing {2}D trajectories of {0} agents with {1} timesteps".format(tt.shape[0], tt.shape[1], tt.shape[2]))

fig = plt.figure()
ax = fig.add_subplot(111, aspect='equal', projection='3d')
plt.subplots_adjust(bottom=0.25)  # make room for the slider

ax_step = plt.axes([0.25, 0.1, 0.65, 0.03])
s_step = Slider(ax_step, 'timestep', 1, traj_len, valinit=1, valstep=1)

plotRange = 4


def update(val):
    step = int(s_step.val)
    ax.clear()
    ax.set_xlim3d(-plotRange, plotRange)
    ax.set_ylim3d(-plotRange, plotRange)
    ax.set_zlim3d(-plotRange, plotRange)
    # ax.set_aspect('equal')
    for i in range(0, agents):
        ax.plot3D(tt[i, 0:step, 0], tt[i, 0:step, 1], tt[i, 0:step, 2])
        ax.scatter(tt[i, 0:step, 0], tt[i, 0:step, 1], tt[i, 0:step, 2])
    fig.canvas.draw_idle()


s_step.on_changed(update)

update(1)  # run update once to set axes range
plt.show()
