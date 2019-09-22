import sys
import numpy as np
import matplotlib.pyplot as plt

# 100 iterations time data, 20 runs, mean and std
# x = [2, 5, 10, 15, 20, 25, 30]
# y = [0.18860795497894287, 0.3348004221916199, 0.9326541304588318, 2.094514548778534, 3.6826900005340577, 6.042745387554168, 8.273628222942353]
# std = [0.007281478635805068, 0.014803962214698242, 0.024386522496844164, 0.04608182124647058, 0.1923647729981805, 0.20194796700484924, 0.14046157984210636]

# circle swaps time data
x = [2, 3, 4, 5, 6]
y = [0.2696045398712158, 0.3316895246505737, 0.46469435691833494, 1.0863147258758545, 2.5175641059875487]
std = [0.012899517381508185, 0.013873055261522143, 0.007741864388553333, 0.025682008564961487, 0.02503523303876185]

fig, ax = plt.subplots()
ax.bar(x, y,
       yerr=std,
       align='center',
       alpha=0.5,
       ecolor='black',
       capsize=10)

ax.set_xlabel('Number of quadcopters on circle')
ax.set_ylabel('Time until solution is found (s)')
ax.set_xticks(x)
ax.yaxis.grid(True)

SAVE = True
if SAVE:
    plt.savefig(sys.path[0] + "/opt_time.pdf", dpi=None, facecolor='w', edgecolor='w',
                orientation='portrait', papertype=None, format=None,
                transparent=False, bbox_inches='tight', pad_inches=0,
                frameon=None, metadata=None)
else:
    plt.show()
