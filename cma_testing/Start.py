import numpy as np
import matplotlib.pyplot as plt
import TrajectoryError
import cma

# AGENT TRAJ DIM

START_VEL = np.array([[0,0,0]])
START_POS = np.array([[0,0,0]])
GOAL_VEL = np.array([[0,0,0]])
GOAL_POS = np.array([[4,4,4]])

TIMESTEP = 1
NUM_AGENTS = GOAL_VEL.shape[0]
NUM_TRAJ = 10
NUM_DIM= GOAL_VEL.shape[1]

error = TrajectoryError.TrajectoryError(TIMESTEP, NUM_TRAJ, GOAL_VEL, GOAL_POS)


# es = cma.CMAEvolutionStrategy((NUM_AGENTS*NUM_TRAJ*NUM_DIM) * [0], 0.5)
# es.optimize(error.get_error)
# #es.result_pretty()
# print("\n")
# xbest = es.result[0]
# error.integrate(xbest)
# print(error.vel_traj)
# print(error.pos_traj)

