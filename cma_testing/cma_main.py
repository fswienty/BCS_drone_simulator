import numpy as np
import matplotlib.pyplot as plt
from error_calculator import ErrorCalculator
import cma

# AGENT TRAJ DIM

START_VEL = np.array([[0,0,0],[0,0,0],[0,0,0]])
START_POS = np.array([[4,0,0],[0,4,0],[0,0,4]])
GOAL_VEL = np.array([[0,0,0],[0,0,0],[0,0,0]])
GOAL_POS = np.array([[-4,0,0],[0,-4,0],[0,0,-4]])

TIMESTEP = 1
MAX_JERK = 1
AGENTS = GOAL_VEL.shape[0]
TRAJ_LEN = 10
DIM = GOAL_VEL.shape[1]

num_opt_vars = AGENTS * TRAJ_LEN * DIM # the amount of variables to be optimized via cma
error_calc = ErrorCalculator(TIMESTEP, TRAJ_LEN, START_VEL, START_POS, GOAL_VEL, GOAL_POS)


options = cma.CMAOptions()
options.set('ftarget', 1e-1)
options.set('bounds', [-MAX_JERK, MAX_JERK])
# es = cma.CMAEvolutionStrategy(num_opt_vars * [0], 0.5, options)
# es.opts.set('opt', value) # use this for chaning options while running
# es.optimize(error_calc.get_error)
# xbest = es.result[0]
xbest = cma.fmin2(error_calc.get_error, num_opt_vars * [0], 0.5, options)[0]

print("\n### FINAL ERROR #############################################")
print(error_calc.get_error(xbest))
print("\n### FINAL JERK TRAJECTORY #############################################")
print(error_calc.jerk_traj)
print("\n### FINAL ACC TRAJECTORY #############################################")
print(error_calc.acc_traj)
print("\n### FINAL VEL TRAJECTORY #############################################")
print(error_calc.vel_traj)
print("\n### FINAL POS TRAJECTORY #############################################")
print(error_calc.pos_traj)

np.save("jerk_traj.npy", error_calc.jerk_traj)
np.save("acc_traj.npy", error_calc.acc_traj)
np.save("vel_traj.npy", error_calc.vel_traj)
np.save("pos_traj.npy", error_calc.pos_traj)

