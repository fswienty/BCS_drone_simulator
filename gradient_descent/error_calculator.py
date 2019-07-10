import numpy as np
from jax import grad
# import matplotlib.pyplot as plt


class ErrorCalculator():

    timestep = 0
    agents = 0
    traj_len = 0
    min_dist = 0
    dim = 0

    start_vel = 0
    start_pos = 0
    goal_vel = 0
    goal_pos = 0

    jerk_traj = 0
    acc_traj = 0
    vel_traj = 0
    pos_traj = 0


    def __init__(self, timestep, traj_len, min_dist, start_vel, start_pos, goal_vel, goal_pos):
        self.timestep = timestep
        self.agents = goal_vel.shape[0]
        self.traj_len = traj_len
        self.min_dist = min_dist
        self.dim = goal_vel.shape[1]
        self.start_vel = start_vel
        self.start_pos = start_pos
        self.goal_vel = goal_vel
        self.goal_pos = goal_pos


    def _integrate(self):
        self.acc_traj = np.zeros([self.agents, self.traj_len, self.dim])
        self.vel_traj = np.zeros([self.agents, self.traj_len, self.dim])
        self.pos_traj = np.zeros([self.agents, self.traj_len, self.dim])
        self.vel_traj[:, 0, :] = self.start_vel
        self.pos_traj[:, 0, :] = self.start_pos
        for i in range(0, self.traj_len - 1):
            self.acc_traj[:, i + 1, :] = self.acc_traj[:, i, :] + (self.timestep * self.jerk_traj[:, i, :])
            self.vel_traj[:, i + 1, :] = self.vel_traj[:, i, :] + (self.timestep * self.acc_traj[:, i, :]) + (0.5 * self.timestep**2 * self.jerk_traj[:, i, :])
            self.pos_traj[:, i + 1, :] = self.pos_traj[:, i, :] + (self.timestep * self.vel_traj[:, i, :]) + (0.5 * self.timestep**2 * self.acc_traj[:, i, :]) + (0.1666 * self.timestep**3 * self.jerk_traj[:, i, :])


    def _checkCollisions(self):
        cols = 0
        for ag1 in range(0, self.agents):
            # pos_ag1 = self.pos_traj[ag1, :, :]
            for ag2 in range(ag1 + 1, self.agents):
                # pos_ag2 = self.pos_traj[ag2, :, :]
                # pos_diff = pos_ag1 - pos_ag2
                pos_diff = self.pos_traj[ag1, :, :] - self.pos_traj[ag2, :, :]
                for step in range(0, self.traj_len):
                    dist = np.linalg.norm(pos_diff[step])
                    if dist < self.min_dist:
                        cols += 1 - (1 / self.min_dist) * dist
        return cols


    def getError(self, jerk_traj):
        self.jerk_traj = np.asarray(jerk_traj).reshape(self.agents, self.traj_len, self.dim)
        self._integrate()
        error = 0
        vel_error = np.linalg.norm(self.goal_vel - self.vel_traj[:, -1, :])
        pos_error = np.linalg.norm(self.goal_pos - self.pos_traj[:, -1, :])
        error += vel_error
        error += pos_error
        error += self._checkCollisions()
        return error


START_VEL = np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]])
START_POS = np.array([[4, 0, 0], [-4, 0, 0], [0, 0, 0], [0, 0, 4], [-3, -3, 0]])
GOAL_VEL = np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]])
GOAL_POS = np.array([[-4, 0, 0], [4, 0, 0], [0, 0, 0], [0, 0, -4], [3, 3, 0]])

TIMESTEP = 1
MAX_JERK = 1
AGENTS = GOAL_VEL.shape[0]
TRAJ_LEN = 10
MIN_DIST = 2
DIM = GOAL_VEL.shape[1]

calc = ErrorCalculator(TIMESTEP, TRAJ_LEN, MIN_DIST, START_VEL, START_POS, GOAL_VEL, GOAL_POS)

jerks = np.zeros([AGENTS, TRAJ_LEN, DIM])

error = calc.getError(jerks)

errorAutogradFun = grad(calc.getError)
errorGrad = errorAutogradFun(jerks)

print(error)
print(errorGrad)