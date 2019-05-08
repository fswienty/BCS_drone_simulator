import numpy as np
import matplotlib.pyplot as plt
import TrajectoryError
import cma

# AGENT TRAJ DIM

# START_VEL = np.array([[0,0,0]])
# START_POS = np.array([[0,0,0]])
GOAL_VEL = np.array([[0,0,0],[0,0,0]])
GOAL_POS = np.array([[4,4,4],[-2,-2,-2]])

TIMESTEP = 1
NUM_AGENTS = GOAL_VEL.shape[0]
NUM_TRAJ = 10
NUM_DIM = GOAL_VEL.shape[1]

num_opt_vars = NUM_AGENTS*NUM_TRAJ*NUM_DIM # the amount of variables to be optimized via cma

error_calc = TrajectoryError.ErrorCalculator(TIMESTEP, NUM_TRAJ, GOAL_VEL, GOAL_POS)

# options = cma.CMAOptions()
# options.set('tolfun', 1e-3)
es = cma.CMAEvolutionStrategy(num_opt_vars * [0], 0.5)
es.opts.set('tolfun', 1e-1)
es.optimize(error_calc.get_error)
print("\n### es.result_pretty() #############################################")
es.result_pretty()
xbest = es.result[0]
# print("\n### JERK TRAJECTORY RESULT #############################################")
# print(xbest.reshape(NUM_AGENTS, NUM_TRAJ, NUM_DIM))

err = error_calc.get_error(xbest)
print("\n### FINAL ERROR #############################################")
print(err)
print("\n### FINAL JERK TRAJECTORY #############################################")
print(error_calc.jerk_traj)
print("\n### FINAL ACC TRAJECTORY #############################################")
print(error_calc.acc_traj)
print("\n### FINAL VEL TRAJECTORY #############################################")
print(error_calc.vel_traj)
print("\n### FINAL POS TRAJECTORY #############################################")
print(error_calc.pos_traj)

