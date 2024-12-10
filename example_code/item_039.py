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
import math
import functools

def log_sum(log_total, value):
    log_value = math.log(value)
    return log_total + log_value

result = functools.reduce(log_sum, [10, 20, 40], 0)
print(math.exp(result))


print("Example 2")
def log_sum_alt(value, log_total):  # Changed
    log_value = math.log(value)
    return log_total + log_value


print("Example 3")
result = functools.reduce(
    lambda total, value: log_sum_alt(value, total),  # Reordered
    [10, 20, 40],
    0,
)
print(math.exp(result))


print("Example 4")
def log_sum_for_reduce(total, value):
    return log_sum_alt(value, total)

result = functools.reduce(
    log_sum_for_reduce,
    [10, 20, 40],
    0,
)
print(math.exp(result))


print("Example 5")
def logn_sum(base, logn_total, value):  # New first parameter
    logn_value = math.log(value, base)
    return logn_total + logn_value


print("Example 6")
result = functools.reduce(
    lambda total, value: logn_sum(10, total, value),  # Changed
    [10, 20, 40],
    0,
)
print(math.pow(10, result))


print("Example 7")
result = functools.reduce(
    functools.partial(logn_sum, 10),  # Changed
    [10, 20, 40],
    0,
)
print(math.pow(10, result))


print("Example 8")
def logn_sum_last(logn_total, value, *, base=10):  # New last parameter
    logn_value = math.log(value, base)
    return logn_total + logn_value


print("Example 9")
import math

log_sum_e = functools.partial(logn_sum_last, base=math.e)  # Pinned `base`
print(log_sum_e(3, math.e**10))


print("Example 10")
log_sum_e_alt = lambda *a, base=math.e, **kw: logn_sum_last(*a, base=base, **kw)
print(log_sum_e_alt(3, math.e**10))


print("Example 11")
print(log_sum_e.args, log_sum_e.keywords, log_sum_e.func)
