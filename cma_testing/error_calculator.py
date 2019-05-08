import numpy as np
import matplotlib.pyplot as plt

class ErrorCalculator():

    timestep = 0
    agents = 0
    traj_len = 0
    dim = 0

    goal_vel = 0
    goal_pos = 0

    jerk_traj = 0
    acc_traj = 0
    vel_traj = 0
    pos_traj = 0

    def __init__(self, timestep, traj_len, goal_vel, goal_pos):
        self.timestep = timestep
        self.agents = goal_vel.shape[0]
        self.traj_len = traj_len
        self.dim = goal_vel.shape[1]
        self.goal_vel = goal_vel
        self.goal_pos = goal_pos
        
    #todo apply initial vel and pos
    def _integrate(self):
        self.acc_traj = np.zeros([self.agents, self.traj_len, self.dim])
        self.vel_traj = np.zeros([self.agents, self.traj_len, self.dim])
        self.pos_traj = np.zeros([self.agents, self.traj_len, self.dim])
        for i in range(0, self.traj_len - 1):
            self.acc_traj[:,i+1,:] = self.acc_traj[:,i,:] + (self.timestep * self.jerk_traj[:,i,:])
            self.vel_traj[:,i+1,:] = self.vel_traj[:,i,:] + (self.timestep * self.acc_traj[:,i,:]) + (0.5 * self.timestep**2 * self.jerk_traj[:,i,:])
            self.pos_traj[:,i+1,:] = self.pos_traj[:,i,:] + (self.timestep * self.vel_traj[:,i,:]) + (0.5 * self.timestep**2 * self.acc_traj[:,i,:]) + (0.1666 * self.timestep**3 * self.jerk_traj[:,i,:])  

    def get_error(self, jerk_traj):
        self.jerk_traj = np.asarray(jerk_traj).reshape(self.agents, self.traj_len, self.dim)
        self._integrate()
        # end_vel = self.vel_traj[:,-1,:]
        # end_pos = self.pos_traj[:,-1,:]
        vel_error = np.linalg.norm(self.goal_vel - self.vel_traj[:,-1,:])
        pos_error = np.linalg.norm(self.goal_pos - self.pos_traj[:,-1,:])
        return vel_error + pos_error
