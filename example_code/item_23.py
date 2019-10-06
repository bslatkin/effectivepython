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
def remainder(number, divisor):
    return number % divisor

assert remainder(20, 7) == 6


# Example 2
remainder(20, 7)
remainder(20, divisor=7)
remainder(number=20, divisor=7)
remainder(divisor=7, number=20)


# Example 3
try:
    # This will not compile
    source = """remainder(number=20, 7)"""
    eval(source)
except:
    logging.exception('Expected')
else:
    assert False


# Example 4
try:
    remainder(20, number=7)
except:
    logging.exception('Expected')
else:
    assert False


# Example 5
my_kwargs = {
	'number': 20,
	'divisor': 7,
}
assert remainder(**my_kwargs) == 6


# Example 6
my_kwargs = {
	'divisor': 7,
}
assert remainder(number=20, **my_kwargs) == 6


# Example 7
my_kwargs = {
	'number': 20,
}
other_kwargs = {
	'divisor': 7,
}
assert remainder(**my_kwargs, **other_kwargs) == 6


# Example 8
def print_parameters(**kwargs):
    for key, value in kwargs.items():
        print(f'{key} = {value}')

print_parameters(alpha=1.5, beta=9, gamma=4)


# Example 9
def flow_rate(weight_diff, time_diff):
    return weight_diff / time_diff

weight_diff = 0.5
time_diff = 3
flow = flow_rate(weight_diff, time_diff)
print(f'{flow:.3} kg per second')


# Example 10
def flow_rate(weight_diff, time_diff, period):
    return (weight_diff / time_diff) * period


# Example 11
flow_per_second = flow_rate(weight_diff, time_diff, 1)


# Example 12
def flow_rate(weight_diff, time_diff, period=1):
    return (weight_diff / time_diff) * period


# Example 13
flow_per_second = flow_rate(weight_diff, time_diff)
flow_per_hour = flow_rate(weight_diff, time_diff, period=3600)
print(flow_per_second)
print(flow_per_hour)


# Example 14
def flow_rate(weight_diff, time_diff,
              period=1, units_per_kg=1):
    return ((weight_diff * units_per_kg) / time_diff) * period


# Example 15
pounds_per_hour = flow_rate(weight_diff, time_diff,
                            period=3600, units_per_kg=2.2)
print(pounds_per_hour)


# Example 16
pounds_per_hour = flow_rate(weight_diff, time_diff, 3600, 2.2)
print(pounds_per_hour)
