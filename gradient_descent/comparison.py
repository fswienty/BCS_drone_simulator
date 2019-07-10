import numpy as np


class comp:

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

    def __init__(self, timestep, traj_len, min_dist, start_vel, start_pos):
        self.timestep = timestep
        self.traj_len = traj_len
        self.min_dist = min_dist
        self.start_vel = start_vel
        self.start_pos = start_pos


    def cma(self, jerk_traj):
        self.traj_len = len(jerk_traj)
        self.jerk_traj = jerk_traj
        self.acc_traj = np.zeros([self.traj_len])
        self.vel_traj = np.zeros([self.traj_len])
        self.pos_traj = np.zeros([self.traj_len])
        self.vel_traj[0] = self.start_vel
        self.pos_traj[0] = self.start_pos
        for i in range(0, self.traj_len - 1):
            self.acc_traj[i + 1] = self.acc_traj[i] + (self.timestep * self.jerk_traj[i])
            self.vel_traj[i + 1] = self.vel_traj[i] + (self.timestep * self.acc_traj[i]) + (0.5 * self.timestep**2 * self.jerk_traj[i])
            self.pos_traj[i + 1] = self.pos_traj[i] + (self.timestep * self.vel_traj[i]) + (0.5 * self.timestep**2 * self.acc_traj[i]) + (0.1666 * self.timestep**3 * self.jerk_traj[i])


def gradDesc(jerks, p0, v0, t):
    traj_len = len(jerks)
    summation = 0
    p = np.zeros([traj_len])
    for k in range(0, traj_len - 1):
        summation = 0
        for i in range(0, k + 1):
            summation += ((k - i)**2 + (k - i) + .3333) * jerks[i]
        p[k + 1] = p0 + (k + 1) * t * v0 + 0.5 * t**3 * summation
    return p


START_VEL = 0
START_POS = 0
# GOAL_VEL = np.array([[0, 0, 0]])
# GOAL_POS = np.array([[-4, 0, 0]])

TIMESTEP = 1
MAX_JERK = 1
TRAJ_LEN = 15
MIN_DIST = 2

jerk = np.array([2, 1, -6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

# comp = comp(TIMESTEP, TRAJ_LEN, MIN_DIST, START_VEL, START_POS)
# comp.cma(jerk)
# cmaResult = comp.pos_traj
gradResult = gradDesc(jerk, START_POS, START_VEL, TIMESTEP)

print(gradResult)
