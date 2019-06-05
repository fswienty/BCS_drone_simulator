# -*- coding: utf-8 -*-
#
#     ||          ____  _ __
#  +------+      / __ )(_) /_______________ _____  ___
#  | 0xBC |     / __  / / __/ ___/ ___/ __ `/_  / / _ \
#  +------+    / /_/ / / /_/ /__/ /  / /_/ / / /_/  __/
#   ||  ||    /_____/_/\__/\___/_/   \__,_/ /___/\___/
#
#  Copyright (C) 2019 Bitcraze AB
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
Uploads the coordinates in bs_position.txt (must be located in the same directory as this python file) to the crazyflie with the specified address.
"""
import logging
import time
import os
import sys
import re

import cflib.crtp  # noqa
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.mem import LighthouseBsGeometry
from cflib.crazyflie.mem import MemoryElement
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
# Only output errors from the logging framework

logging.basicConfig(level=logging.ERROR)

class WriteMem:
    def __init__(self, uri, bs1, bs2):
        self.data_written = False
        self.got_data = False

        with SyncCrazyflie(uri, cf=Crazyflie(rw_cache='./cache')) as scf:
            mems = scf.cf.mem.get_mems(MemoryElement.TYPE_LH)

            count = len(mems)
            if count != 1:
                raise Exception('Unexpected nr of memories found:', count)

            # WRITE
            mems[0].geometry_data = [bs1, bs2]

            print('Writing data')
            mems[0].write_data(self._data_written)

            while not self.data_written:
                time.sleep(1)

            # READ
            print('Requesting data')
            mems[0].update(self._data_updated)

            while not self.got_data:
                time.sleep(1)


    def _data_written(self, mem, addr):
        self.data_written = True
        print('Data written')

    def _data_updated(self, mem):
        mem.dump()
        self.got_data = True


if __name__ == '__main__':
    # URI to the Crazyflie to connect to
    uri = 'radio://0/80/2M/E7E7E7E7E0'

    # Initialize the low-level drivers (don't list the debug drivers)
    cflib.crtp.init_drivers(enable_debug_driver=False)

    with open(os.path.join(sys.path[0], "bs_position.txt"), encoding="utf-8") as f:
        text = f.read()
    match = re.findall(r'-?\d.\d+', text)
    numberList = [float(i) for i in match]

    bs1 = LighthouseBsGeometry()
    bs1.origin = numberList[0:3]
    bs1.rotation_matrix = [numberList[3:6], numberList[6:9], numberList[9:12]]
    bs2 = LighthouseBsGeometry()
    bs2.origin = numberList[12:15]
    bs2.rotation_matrix = [numberList[15:18], numberList[18:21], numberList[21:24]]

    WriteMem(uri, bs1, bs2)
