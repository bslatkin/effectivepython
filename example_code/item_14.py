#!/usr/bin/env PYTHONHASHSEED=1234 python3

# Copyright 2014-2019 Brett Slatkin, Pearson Education Inc.
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

# Reproduce book environment
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


# Example 1
numbers = [93, 86, 11, 68, 70]
numbers.sort()
print(numbers)


# Example 2
class Tool:
    def __init__(self, name, weight):
        self.name = name
        self.weight = weight

    def __repr__(self):
        return f'Tool({self.name!r}, {self.weight})'

tools = [
    Tool('level', 3.5),
    Tool('hammer', 1.25),
    Tool('screwdriver', 0.5),
    Tool('chisel', 0.25),
]


# Example 3
try:
    tools.sort()
except:
    logging.exception('Expected')
else:
    assert False


# Example 4
print('Unsorted:', repr(tools))
tools.sort(key=lambda x: x.name)
print('\nSorted:  ', tools)


# Example 5
tools.sort(key=lambda x: x.weight)
print('By weight:', tools)


# Example 6
places = ['home', 'work', 'New York', 'Paris']
places.sort()
print('Case sensitive:  ', places)
places.sort(key=lambda x: x.lower())
print('Case insensitive:', places)


# Example 7
power_tools = [
    Tool('drill', 4),
    Tool('circular saw', 5),
    Tool('jackhammer', 40),
    Tool('sander', 4),
]


# Example 8
saw = (5, 'circular saw')
jackhammer = (40, 'jackhammer')
assert not (jackhammer < saw)  # Matches expectations


# Example 9
drill = (4, 'drill')
sander = (4, 'sander')
assert drill[0] == sander[0]  # Same weight
assert drill[1] < sander[1]   # Alphabetically less
assert drill < sander         # Thus, drill comes first


# Example 10
power_tools.sort(key=lambda x: (x.weight, x.name))
print(power_tools)


# Example 11
power_tools.sort(key=lambda x: (x.weight, x.name),
                 reverse=True)  # Makes all criteria descending
print(power_tools)


# Example 12
power_tools.sort(key=lambda x: (-x.weight, x.name))
print(power_tools)


# Example 13
try:
    power_tools.sort(key=lambda x: (x.weight, -x.name),
                     reverse=True)
except:
    logging.exception('Expected')
else:
    assert False


# Example 14
power_tools.sort(key=lambda x: x.name)   # Name ascending

power_tools.sort(key=lambda x: x.weight, # Weight descending
                 reverse=True)

print(power_tools)


# Example 15
power_tools.sort(key=lambda x: x.name)
print(power_tools)


# Example 16
power_tools.sort(key=lambda x: x.weight,
                 reverse=True)
print(power_tools)
