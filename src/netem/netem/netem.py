#!/usr/bin/env python3
#
# Copyright 2020 James Pace
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import subprocess
import psutil

class netem():
    def __init__(self, interface, debug=False):
        self._interface = interface
        self._debug = debug

    def _run(self, command):
        if self._debug:
            print("Command: " + command)
        else:
            subprocess.run(command)

    def clear(self):
        command = f"tc qdisc del dev {self._interface} root"
        self._run(command)

    def delay(self, time, std_dev):
        command = (f"tc qdisc change dev {self._interface} root netem delay "
                   f"{time}ms {std_dev}ms distribution normal")
        self._run(command)

    def packet_loss(self, percent):
        command = (f"tc qdisc change dev {self._interface} root netem loss "
                   f"{percent}%")
        self._run(command)

    def limit(self, bandwidth_kbit):
        command = (f"tc qdisc add dev {self._interface} root tbf rate "
                   f"{bandwidth_kbit}kbit burst 1600 limit 3000")
        self._run(command)
