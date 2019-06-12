import numpy as np
import os, sys
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons
from mpl_toolkits.mplot3d import Axes3D

tt = np.load(os.path.join(sys.path[0], "traj.npy"))
agents = tt.shape[1]
traj_len = tt.shape[0]

fig = plt.figure()
ax = fig.add_subplot(111, aspect='equal', projection='3d')
plt.subplots_adjust(bottom=0.25) # make room for the slider

ax_step = plt.axes([0.25, 0.1, 0.65, 0.03])
s_step = Slider(ax_step, 'timestep', 1, traj_len, valinit=1, valstep=1)

def update(val):
    step = int(s_step.val)
    ax.clear()
    ax.set_xlim3d(-2, 2)
    ax.set_ylim3d(-2, 2)
    ax.set_zlim3d(0, 2)
    #ax.set_aspect('equal')
    for i in range(0, agents):
        trail = max(0, step-10)
        #ax.plot3D(tt[0:step,i,0], tt[0:step,i,1], tt[0:step,i,2])
        ax.plot3D(tt[trail:step,i,0], tt[trail:step,i,1], tt[trail:step,i,2])
        ax.scatter(tt[step-1,i,0], tt[step-1,i,1], tt[step-1,i,2])
    fig.canvas.draw_idle()

s_step.on_changed(update)

update(1) #run update once to set axes range
plt.show()