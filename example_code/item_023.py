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
import random

def flip_coin():
    if random.randint(0, 1) == 0:
        return "Heads"
    else:
        return "Tails"

def flip_is_heads():
    return flip_coin() == "Heads"


print("Example 2")
flips = [flip_is_heads() for _ in range(20)]
all_heads = False not in flips
assert not all_heads  # Very unlikely to be True


print("Example 3")
all_heads = True
for _ in range(100):
    if not flip_is_heads():
        all_heads = False
        break
assert not all_heads  # Very unlikely to be True


print("Example 4")
print("All truthy:")
print(all([1, 2, 3]))
print(1 and 2 and 3)

print("One falsey:")
print(all([1, 0, 3]))
print(1 and 0 and 3)


print("Example 5")
all_heads = all(flip_is_heads() for _ in range(20))
assert not all_heads


print("Example 6")
all_heads = all([flip_is_heads() for _ in range(20)])  # Wrong
assert not all_heads


print("Example 7")
def repeated_is_heads(count):
    for _ in range(count):
        yield flip_is_heads()  # Generator

all_heads = all(repeated_is_heads(20))
assert not all_heads


print("Example 8")
def flip_is_tails():
    return flip_coin() == "Tails"


print("Example 9")
print("All falsey:")
print(any([0, False, None]))
print(0 or False or None)

print("One truthy:")
print(any([None, 3, 0]))
print(None or 3 or 0)


print("Example 10")
all_heads = not any(flip_is_tails() for _ in range(20))
assert not all_heads


print("Example 11")
def repeated_is_tails(count):
    for _ in range(count):
        yield flip_is_tails()

all_heads = not any(repeated_is_tails(20))
assert not all_heads


print("Example 12")
for a in (True, False):
    for b in (True, False):
        assert any([a, b]) == (not all([not a, not b]))
        assert all([a, b]) == (not any([not a, not b]))
