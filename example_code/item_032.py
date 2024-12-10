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
def careful_divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return None


assert careful_divide(4, 2) == 2
assert careful_divide(0, 1) == 0
assert careful_divide(3, 6) == 0.5
assert careful_divide(1, 0) == None


print("Example 2")
x, y = 1, 0
result = careful_divide(x, y)
if result is None:
    print("Invalid inputs")
else:
    print(f"Result is {result:.1f}")


print("Example 3")
x, y = 0, 5
result = careful_divide(x, y)
if not result:               # Changed
    print("Invalid inputs")  # This runs! But shouldn't
else:
    assert False


print("Example 4")
def careful_divide(a, b):
    try:
        return True, a / b
    except ZeroDivisionError:
        return False, None


assert careful_divide(4, 2) == (True, 2)
assert careful_divide(0, 1) == (True, 0)
assert careful_divide(3, 6) == (True, 0.5)
assert careful_divide(1, 0) == (False, None)


print("Example 5")
x, y = 5, 0
success, result = careful_divide(x, y)
if not success:
    print("Invalid inputs")


print("Example 6")
x, y = 5, 0
_, result = careful_divide(x, y)
if not result:
    print("Invalid inputs")


print("Example 7")
def careful_divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        raise ValueError("Invalid inputs")  # Changed


print("Example 8")
x, y = 5, 2
try:
    result = careful_divide(x, y)
except ValueError:
    print("Invalid inputs")
else:
    print(f"Result is {result:.1f}")
