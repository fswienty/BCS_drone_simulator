import numpy as np
import matplotlib.pyplot as plt



### start and end values ###
START_VELOCITY = np.array([[0,0]])
START_POSITION = np.array([[0,0]])

END_VELOCITY = np.array([[0,0]])
END_POSITION = np.array([[10,10]])

DIM = 2 # dimensions the robots can traverse


timestep = 1
trajectory_length = 10

jerk_traj = np.array([[0,0]])
acc_traj = np.array([[0,0]])
vel_traj = START_VELOCITY
pos_traj = START_POSITION

# jerk_traj = np.array([[0,0]])
# jerk_traj = np.append(jerk_traj, 6 * np.random.rand(trajectory_length, DIM) - 3, axis=0)
jerk_traj = 6 * np.random.rand(trajectory_length, DIM) - 3
acc_traj = np.zeros([trajectory_length, DIM])
vel_traj = np.zeros([trajectory_length, DIM])
pos_traj = np.zeros([trajectory_length, DIM])

end_vel = 0
end_pos = 0

def integrate():
    for i in range(0, trajectory_length - 1):
        acc_traj[i+1] = acc_traj[i] + (timestep * jerk_traj[i])
        vel_traj[i+1] = vel_traj[i] + (timestep * acc_traj[i]) + (0.5 * timestep**2 * jerk_traj[i])
        pos_traj[i+1] = pos_traj[i] + (timestep * vel_traj[i]) + (0.5 * timestep**2 * acc_traj[i]) + (0.1666 * timestep**3 * jerk_traj[i])
    global end_vel
    end_vel = vel_traj[trajectory_length - 1]
    #global end_pos = pos_traj[trajectory_length - 1]

integrate()
print(end_vel, end_pos)

print("jerk_trajectory:\n", jerk_traj, "\n")
print("acc_trajectory:\n", acc_traj, "\n")
print("vel_trajectory:\n", vel_traj, "\n")
print("pos_trajectory:\n", pos_traj, "\n")

# x = jerk_traj[:,0]
# y = jerk_traj[:,1]
# plt.plot(x,y)
# plt.show()

# x = acc_traj[:,0]
# y = acc_traj[:,1]
# plt.plot(x,y)
# plt.show()

# x = vel_traj[:,0]
# y = vel_traj[:,1]
# plt.plot(x,y)
# plt.show()

# x = pos_traj[:,0]
# y = pos_traj[:,1]
# plt.plot(x,y)
# plt.show()

#acc_traj = np.append(acc_traj, acc_traj[1] + (timestep * jerk_traj[1]), axis=0)