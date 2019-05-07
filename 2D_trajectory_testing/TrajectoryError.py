import numpy as np
import matplotlib.pyplot as plt

class TrajectoryError():

    timestep = 0
    traj_len = 0
    dim = 1

    goal_vel = 0
    goal_pos = 0

    jerk_traj = np.zeros([traj_len, dim])
    acc_traj = np.zeros([traj_len, dim])
    vel_traj = np.zeros([traj_len, dim])
    pos_traj = np.zeros([traj_len, dim])

    def __init__(self, timestep, traj_len, goal_vel, goal_pos, dim):
        self.timestep = timestep
        self.traj_len = traj_len
        self.goal_vel = goal_vel
        self.goal_pos = goal_pos
        self.dim = dim

    def integrate(self, jerk_traj):
        self.jerk_traj = jerk_traj
        self.acc_traj = np.zeros([self.traj_len, self.dim])
        self.vel_traj = np.zeros([self.traj_len, self.dim])
        self.pos_traj = np.zeros([self.traj_len, self.dim])
        for i in range(0, self.traj_len - 1):
            self.acc_traj[i+1] = self.acc_traj[i] + (self.timestep * self.jerk_traj[i])
            self.vel_traj[i+1] = self.vel_traj[i] + (self.timestep * self.acc_traj[i]) + (0.5 * self.timestep**2 * self.jerk_traj[i])
            self.pos_traj[i+1] = self.pos_traj[i] + (self.timestep * self.vel_traj[i]) + (0.5 * self.timestep**2 * self.acc_traj[i]) + (0.1666 * self.timestep**3 * self.jerk_traj[i])  

    def get_error(self, jerk_traj):
        self.integrate(jerk_traj)
        end_vel = self.vel_traj[self.traj_len - 1]
        end_pos = self.pos_traj[self.traj_len - 1]
        vel_error = np.linalg.norm(self.goal_vel - end_vel)
        pos_error = np.linalg.norm(self.goal_pos - end_pos)
        return vel_error + pos_error

# lul = TrajectoryError(1,10,0,5,1)
# lul.integrate(jerk_traj)
# print(lul.vel_traj)
# print(lul.pos_traj)