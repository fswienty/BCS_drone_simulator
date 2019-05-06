import numpy as np
import matplotlib.pyplot as plt
import Fitness
import cma

START_VELOCITY = np.array([[0,0]])
START_POSITION = np.array([[0,0]])

GOAL_VELOCITY = np.array([[0,0]])
GOAL_POSITION = np.array([[10,10]])

dim = 2 # dimensions the robots can traverse

timestep = 1
traj_len = 10
result = 0

fitness = Fitness.Fitness(timestep, traj_len, GOAL_VELOCITY, GOAL_POSITION)

jerk_traj = 6 * np.random.rand(traj_len, dim) - 3
result = fitness.get_fitness(jerk_traj)

print(result)

es = cma.CMAEvolutionStrategy(traj_len * [0], 0.5)
es.optimize(fitness.get_fitness)
es.result_pretty()