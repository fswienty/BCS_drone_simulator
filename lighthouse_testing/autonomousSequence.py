# -*- coding: utf-8 -*-
#
#     ||          ____  _ __
#  +------+      / __ )(_) /_______________ _____  ___
#  | 0xBC |     / __  / / __/ ___/ ___/ __ `/_  / / _ \
#  +------+    / /_/ / / /_/ /__/ /  / /_/ / / /_/  __/
#   ||  ||    /_____/_/\__/\___/_/   \__,_/ /___/\___/
#
#  Copyright (C) 2016 Bitcraze AB
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
Simple example that connects to one crazyflie (check the address at the top
and update it to your crazyflie address) and send a sequence of setpoints,
one every 5 seconds.

This example is intended to work with the Loco Positioning System in TWR TOA
mode. It aims at documenting how to set the Crazyflie in position control mode
and how to send setpoints.
"""
import time
from math import sin, cos

import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.log import LogConfig
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.crazyflie.syncLogger import SyncLogger
from cflib.crazyflie.commander import Commander

# URI to the Crazyflie to connect to
uri = 'radio://0/80/2M/E7E7E7E7E1'

# Change the sequence according to your setup
#             x    y    z  YAW
sequence = [
    (0, 0, .5, 0),
    (-1.1, -1.6, 1, 0),
    (1.1, -1.6, 1, 0),
    (1.1, 1.6, 1, 0),
    (-1.1, 1.6, 1, 0),
    (-1.1, -1.6, 1, 0),
    (0, 0, .5, 0),
    (0, 0, .2, 0),
]

yawstuff = [
    (0, 0, .5, 0),
    (0, 0, .5, 90),
    (0, 0, .5, 180),
    (0, 0, .5, 270),
    (0, 0, .5, 360),
    (0, 0, .5, 0),
    (0, 0, .2, 0)
]

start = [
    (0, 0, .7, 0)
]

land = [
    (0, 0, .5, 0),
    (0, 0, .2, 0)
]


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


def reset_estimator(scf):
    cf = scf.cf
    cf.param.set_value('kalman.resetEstimation', '1')
    time.sleep(0.1)
    cf.param.set_value('kalman.resetEstimation', '0')

    wait_for_position_estimator(cf)


def position_callback(timestamp, data, logconf):
    x = data['kalman.stateX']
    y = data['kalman.stateY']
    z = data['kalman.stateZ']
    #print('pos: ({}, {}, {})'.format(x, y, z))
    #print('pos: ({}, {})'.format(x, y))


def start_position_printing(scf):
    log_conf = LogConfig(name='Position', period_in_ms=200)
    log_conf.add_variable('kalman.stateX', 'float')
    log_conf.add_variable('kalman.stateY', 'float')
    log_conf.add_variable('kalman.stateZ', 'float')

    scf.cf.log.add_config(log_conf)
    log_conf.data_received_cb.add_callback(position_callback)
    log_conf.start()


def run_sequence(scf, sequence):
    cf = scf.cf

    cf.param.set_value('flightmode.posSet', '1')

    for position in sequence:
        print('Setting position {}'.format(position))
        for _ in range(15):
            cf.commander.send_position_setpoint(position[0], position[1],  position[2], position[3])
            time.sleep(0.1)    

    # for position in start:
    #     #print('Setting position {}'.format(position))
    #     for _ in range(10):
    #         cf.commander.send_position_setpoint(position[0], position[1], position[2], position[3])
    #         time.sleep(0.2)  

    # for i in range(0, 50):
    #     t = time.perf_counter() * 3
    #     x = sin(t) * .5
    #     y = cos(t) * .5
    #     cf.commander.send_position_setpoint(x, y, .7, 0)
    #     #print('pos: ({}, {})'.format(x, y))
    #     time.sleep(0.2)

    # for position in land:
    #     #print('Setting position {}'.format(position))
    #     for _ in range(10):
    #         cf.commander.send_position_setpoint(position[0], position[1], position[2], position[3])
    #         time.sleep(0.2)           

    cf.commander.send_stop_setpoint()
    # Make sure that the last packet leaves before the link is closed
    # since the message queue is not flushed before closing
    time.sleep(0.1)


if __name__ == '__main__':
    cflib.crtp.init_drivers(enable_debug_driver=False)

    with SyncCrazyflie(uri, cf=Crazyflie(rw_cache='./cache')) as scf:
        reset_estimator(scf)
        start_position_printing(scf)
        run_sequence(scf, yawstuff)
