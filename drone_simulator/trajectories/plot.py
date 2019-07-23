import numpy as np
import os
import sys
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons
from mpl_toolkits.mplot3d import Axes3D

traj = np.load(sys.path[0] + "/traj.npy")
agents = traj.shape[1]
traj_len = traj.shape[0]

print("Showing {2}D trajectories of {0} agents with {1} timesteps".format(traj.shape[0], traj.shape[1], traj.shape[2]))

fig = plt.figure()
ax = fig.add_subplot(111, aspect='equal', projection='3d')
plt.subplots_adjust(bottom=0.25)  # make room for the slider

ax_step = plt.axes([0.25, 0.1, 0.65, 0.03])
s_step = Slider(ax_step, 'timestep', 1, traj_len, valinit=1, valstep=1)

plotRange = 1


def update(val):
    step = int(s_step.val)
    ax.clear()
    ax.set_xlim3d(-plotRange, plotRange)
    ax.set_ylim3d(-plotRange, plotRange)
    ax.set_zlim3d(0, 2 * plotRange)
    for i in range(0, agents):
        trail = max(0, step - 5000)
        ax.plot3D(traj[trail:step, i, 0], traj[trail:step, i, 1], traj[trail:step, i, 2])
        ax.scatter(traj[step - 1, i, 0], traj[step - 1, i, 1], traj[step - 1, i, 2])
    fig.canvas.draw_idle()


s_step.on_changed(update)

update(1)  # run update once to set axes range
plt.show()