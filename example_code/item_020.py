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
for i in range(3):
    print(f"Inside {i=}")
print(f"After  {i=}")


print("Example 2")
categories = ["Hydrogen", "Uranium", "Iron", "Other"]
for i, name in enumerate(categories):
    if name == "Iron":
        break
print(i)


print("Example 3")
for i, name in enumerate(categories):
    if name == "Lithium":
        break
print(i)


print("Example 4")
try:
    del i
    categories = []
    for i, name in enumerate(categories):
        if name == "Lithium":
            break
    print(i)
except:
    logging.exception('Expected')
else:
    assert False


print("Example 5")
try:
    my_numbers = [37, 13, 128, 21]
    found = [i for i in my_numbers if i % 2 == 0]
    print(i)  # Always raises
except:
    logging.exception('Expected')
else:
    assert False
