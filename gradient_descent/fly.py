# -*- coding: utf-8 -*-
#
#     ||          ____  _ __
#  +------+      / __ )(_) /_______________ _____  ___
#  | 0xBC |     / __  / / __/ ___/ ___/ __ `/_  / / _ \
#  +------+    / /_/ / / /_/ /__/ /  / /_/ / / /_/  __/
#   ||  ||    /_____/_/\__/\___/_/   \__,_/ /___/\___/
#
#  Copyright (C) 2017-2018 Bitcraze AB
#
#  Crazyflie Nano Quadcopter Client
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA  02110-1301, USA.
"""
Version of the AutonomousSequence.py example connecting to 10 Crazyflies.
The Crazyflies go straight up, hover a while and land but the code is fairly
generic and each Crazyflie has its own sequence of setpoints that it files
to.
"""
import sys
import time
import numpy as np

import cflib.crtp
from cflib.crazyflie.log import LogConfig
from cflib.crazyflie.swarm import CachedCfFactory
from cflib.crazyflie.swarm import Swarm
from cflib.crazyflie.syncLogger import SyncLogger

# Change uris and sequences according to your setup
URI1 = 'radio://0/80/2M/E7E7E7E7E0'
URI2 = 'radio://0/80/2M/E7E7E7E7E1'
URI3 = 'radio://0/80/2M/E7E7E7E7E2'
URI4 = 'radio://0/80/2M/E7E7E7E7E3'
URI5 = 'radio://0/80/2M/E7E7E7E7E4'
URI6 = 'radio://0/80/2M/E7E7E7E7E5'
URI7 = 'radio://0/80/2M/E7E7E7E7E6'
URI8 = 'radio://0/80/2M/E7E7E7E7E7'
URI9 = 'radio://0/80/2M/E7E7E7E7E8'
URI10 = 'radio://0/80/2M/E7E7E7E7E9'

# how long each setpoint broadcast before switching to the next
timePerSetpoint = 0.2

traj = np.load(sys.path[0] + "/trajectories/pos_traj.npy")
# agents = traj.shape[0]
# timesteps = traj.shape[1]

sequence1 = traj[0]
sequence2 = traj[1]
# sequence3 = traj[2]
# sequence4 = traj[3]
# sequence5 = traj[4]
# sequence6 = traj[5]
# sequence7 = traj[6]
# sequence8 = traj[7]
# sequence9 = traj[8]
# sequence10 = traj[9]

seq_args = {
    URI1: [sequence1],
    URI2: [sequence2]
    # URI3: [sequence3],
    # URI4: [sequence4],
    # URI5: [sequence5],
    # URI6: [sequence6],
    # URI7: [sequence7],
    # URI8: [sequence8],
    # URI9: [sequence9],
    # URI10: [sequence10],
}

# List of URIs, comment the one you do not want to fly
uris = {
    URI1,
    URI2
    # URI3,
    # URI4,
    # URI5,
    # URI6,
    # URI7,
    # URI8,
    # URI9,
    # URI10
}


def wait_for_position_estimator(scf):
    print('Waiting for estimator to find position...')

    log_config = LogConfig(name='Kalman Variance', period_in_ms=500)
    log_config.add_variable('kalman.varPX', 'float')
    log_config.add_variable('kalman.varPY', 'float')
    log_config.add_variable('kalman.varPZ', 'float')

    var_y_history = [1000] * 10
    var_x_history = [1000] * 10
    var_z_history = [1000] * 10

    threshold = 0.001

    with SyncLogger(scf, log_config) as logger:
        for log_entry in logger:
            data = log_entry[1]

            var_x_history.append(data['kalman.varPX'])
            var_x_history.pop(0)
            var_y_history.append(data['kalman.varPY'])
            var_y_history.pop(0)
            var_z_history.append(data['kalman.varPZ'])
            var_z_history.pop(0)

            min_x = min(var_x_history)
            max_x = max(var_x_history)
            min_y = min(var_y_history)
            max_y = max(var_y_history)
            min_z = min(var_z_history)
            max_z = max(var_z_history)

            # print("{} {} {}".
            #       format(max_x - min_x, max_y - min_y, max_z - min_z))

            if (max_x - min_x) < threshold and (
                    max_y - min_y) < threshold and (
                    max_z - min_z) < threshold:
                break


def wait_for_param_download(scf):
    while not scf.cf.param.is_updated:
        time.sleep(1.0)
    print('Parameters downloaded for', scf.cf.link_uri)


def reset_estimator(scf):
    cf = scf.cf
    cf.param.set_value('kalman.resetEstimation', '1')
    time.sleep(0.1)
    cf.param.set_value('kalman.resetEstimation', '0')

    wait_for_position_estimator(cf)


def take_off(cf, position):
    # take_off_time = 1.0
    # sleep_time = 0.1
    # steps = int(take_off_time / sleep_time)
    # vz = position[2] / take_off_time

    # print(vz)

    # for _ in range(steps):
    #     cf.commander.send_velocity_world_setpoint(0, 0, vz, 0)
    #     time.sleep(sleep_time)

    # make sure the drone is at the starting position of the trajectory
    # hopfefully you put them on the ground in a way that they dont crash on their way there
    for _ in range(30):
        cf.commander.send_position_setpoint(position[0], position[1], position[2], 0)
        time.sleep(0.1)


def land(cf, position):
    # landing_time = 1.0
    # sleep_time = 0.1
    # steps = int(landing_time / sleep_time)
    # vz = -position[2] / landing_time

    # print(vz)

    # for _ in range(steps):
    #     cf.commander.send_velocity_world_setpoint(0, 0, vz, 0)
    #     time.sleep(sleep_time)

    for _ in range(20):
        cf.commander.send_position_setpoint(position[0], position[1], 0.25, 0)
        time.sleep(0.1)

    cf.commander.send_stop_setpoint()
    # Make sure that the last packet leaves before the link is closed
    # since the message queue is not flushed before closing
    time.sleep(0.1)


def run_sequence(scf, sequence):
    try:
        cf = scf.cf

        take_off(cf, sequence[0])

        # fly the trajectory
        print("forwards!")
        for position in sequence:
            # print('Setting position {}'.format(position))
            end_time = time.time() + timePerSetpoint
            while time.time() < end_time:
                cf.commander.send_position_setpoint(position[0], position[1], position[2], 0)
                time.sleep(0.1)

        for _ in range(20):
            position = sequence[-1]
            cf.commander.send_position_setpoint(position[0], position[1], position[2], 0)
            time.sleep(0.1)

        # fly the trajectory backwards
        print("backwards!")
        for position in reversed(sequence):
            # print('Setting position {}'.format(position))
            end_time = time.time() + timePerSetpoint
            while time.time() < end_time:
                cf.commander.send_position_setpoint(position[0], position[1], position[2], 0)
                time.sleep(0.1)

        land(cf, sequence[0])
    except Exception as e:
        print(e)


if __name__ == '__main__':
    # logging.basicConfig(level=logging.DEBUG)
    cflib.crtp.init_drivers(enable_debug_driver=False)

    factory = CachedCfFactory(rw_cache='./cache')
    with Swarm(uris, factory=factory) as swarm:
        # If the copters are started in their correct positions this is
        # probably not needed. The Kalman filter will have time to converge
        # any way since it takes a while to start them all up and connect. We
        # keep the code here to illustrate how to do it.
        swarm.parallel(reset_estimator)

        # The current values of all parameters are downloaded as a part of the
        # connections sequence. Since we have 10 copters this is clogging up
        # communication and we have to wait for it to finish before we start
        # flying.
        print('Waiting for parameters to be downloaded...')
        swarm.parallel(wait_for_param_download)

        swarm.parallel(run_sequence, args_dict=seq_args)
