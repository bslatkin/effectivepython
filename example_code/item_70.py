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
def insertion_sort(data):
    result = []
    for value in data:
        insert_value(result, value)
    return result


# Example 2
def insert_value(array, value):
    for i, existing in enumerate(array):
        if existing > value:
            array.insert(i, value)
            return
    array.append(value)


# Example 3
from random import randint

max_size = 10**4
data = [randint(0, max_size) for _ in range(max_size)]
test = lambda: insertion_sort(data)


# Example 4
from cProfile import Profile

profiler = Profile()
profiler.runcall(test)


# Example 5
from pstats import Stats

stats = Stats(profiler)
stats = Stats(profiler, stream=STDOUT)
stats.strip_dirs()
stats.sort_stats('cumulative')
stats.print_stats()


# Example 6
from bisect import bisect_left

def insert_value(array, value):
    i = bisect_left(array, value)
    array.insert(i, value)


# Example 7
profiler = Profile()
profiler.runcall(test)
stats = Stats(profiler, stream=STDOUT)
stats.strip_dirs()
stats.sort_stats('cumulative')
stats.print_stats()


# Example 8
def my_utility(a, b):
    c = 1
    for i in range(100):
        c += a * b

def first_func():
    for _ in range(1000):
        my_utility(4, 5)

def second_func():
    for _ in range(10):
        my_utility(1, 3)

def my_program():
    for _ in range(20):
        first_func()
        second_func()


# Example 9
profiler = Profile()
profiler.runcall(my_program)
stats = Stats(profiler, stream=STDOUT)
stats.strip_dirs()
stats.sort_stats('cumulative')
stats.print_stats()


# Example 10
stats = Stats(profiler, stream=STDOUT)
stats.strip_dirs()
stats.sort_stats('cumulative')
stats.print_callers()
