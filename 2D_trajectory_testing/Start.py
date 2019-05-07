import numpy as np
import matplotlib.pyplot as plt
import TrajectoryError
import cma

START_VELOCITY = np.array([[0,0]])
START_POSITION = np.array([[0,0]])
GOAL_VELOCITY = np.array([[-3,-3]])
GOAL_POSITION = np.array([[4,4]])

DIM = 1 # dimensions the robots can traverse
TIMESTEP = 1
TRAJ_LEN = 10


error = TrajectoryError.TrajectoryError(TIMESTEP, TRAJ_LEN, GOAL_VELOCITY, GOAL_POSITION, DIM)

es = cma.CMAEvolutionStrategy(TRAJ_LEN * [0], 0.5)
es.optimize(error.get_error)
#es.result_pretty()
print("\n")
xbest = es.result[0]
error.integrate(xbest)
print(error.vel_traj)
print(error.pos_traj)

