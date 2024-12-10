#!/usr/bin/env PYTHONHASHSEED=1234 python3

# Copyright 2014-2024 Brett Slatkin, Pearson Education Inc.
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

### Start book environment setup
import random
random.seed(1234)

import logging
from pprint import pprint
from sys import stdout as STDOUT

# Write all output to a temporary directory
import atexit
import gc
import io
import os
import tempfile

TEST_DIR = tempfile.TemporaryDirectory()
atexit.register(TEST_DIR.cleanup)

# Make sure Windows processes exit cleanly
OLD_CWD = os.getcwd()
atexit.register(lambda: os.chdir(OLD_CWD))
os.chdir(TEST_DIR.name)

def close_open_files():
    everything = gc.get_objects()
    for obj in everything:
        if isinstance(obj, io.IOBase):
            obj.close()

atexit.register(close_open_files)
### End book environment setup


print("Example 1")
counter = 0

def read_sensor(sensor_index):
    # Returns sensor data or raises an exception
    # Nothing actually happens here, but this is where
    # the blocking I/O would go.
    pass

def get_offset(data):
    # Always returns 1 or greater
    return 1

def worker(sensor_index, how_many):
    global counter
    # I have a barrier in here so the workers synchronize
    # when they start counting, otherwise it's hard to get a race
    # because the overhead of starting a thread is high.
    BARRIER.wait()
    for _ in range(how_many):
        data = read_sensor(sensor_index)
        # Note that the value passed to += must be a function call or other
        # non-trivial expression in order to cause the CPython eval loop to
        # check whether it should release the GIL. This is a side-effect of
        # an optimization. See https://github.com/python/cpython/commit/4958f5d69dd2bf86866c43491caf72f774ddec97 for details.
        counter += get_offset(data)


print("Example 2")
from threading import Thread

how_many = 10**6
sensor_count = 4

from threading import Barrier

BARRIER = Barrier(sensor_count)

threads = []
for i in range(sensor_count):
    thread = Thread(target=worker, args=(i, how_many))
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()

expected = how_many * sensor_count
print(f"Counter should be {expected}, got {counter}")


print("Example 3")
data = None
counter += get_offset(data)


print("Example 4")
value = counter
delta = get_offset(data)
result = value + delta
counter = result


print("Example 5")
data_a = None
data_b = None
# Running in Thread A
value_a = counter
delta_a = get_offset(data_a)
# Context switch to Thread B
value_b = counter
delta_b = get_offset(data_b)
result_b = value_b + delta_b
counter = result_b
# Context switch back to Thread A
result_a = value_a + delta_a
counter = result_a


print("Example 6")
from threading import Lock

counter = 0
counter_lock = Lock()

def locking_worker(sensor_index, how_many):
    global counter
    BARRIER.wait()
    for _ in range(how_many):
        data = read_sensor(sensor_index)
        with counter_lock:                  # Added
            counter += get_offset(data)


print("Example 7")
BARRIER = Barrier(sensor_count)

for i in range(sensor_count):
    thread = Thread(target=locking_worker, args=(i, how_many))
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()

expected = how_many * sensor_count
print(f"Counter should be {expected}, got {counter}")
