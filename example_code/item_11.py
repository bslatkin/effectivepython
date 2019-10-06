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
a = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
print('Middle two:  ', a[3:5])
print('All but ends:', a[1:7])


# Example 2
assert a[:5] == a[0:5]


# Example 3
assert a[5:] == a[5:len(a)]


# Example 4
print(a[:])
print(a[:5])
print(a[:-1])
print(a[4:])
print(a[-3:])
print(a[2:5])
print(a[2:-1])
print(a[-3:-1])


# Example 5
a[:]      # ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
a[:5]     # ['a', 'b', 'c', 'd', 'e']
a[:-1]    # ['a', 'b', 'c', 'd', 'e', 'f', 'g']
a[4:]     #                     ['e', 'f', 'g', 'h']
a[-3:]    #                          ['f', 'g', 'h']
a[2:5]    #           ['c', 'd', 'e']
a[2:-1]   #           ['c', 'd', 'e', 'f', 'g']
a[-3:-1]  #                          ['f', 'g']


# Example 6
first_twenty_items = a[:20]
last_twenty_items = a[-20:]


# Example 7
try:
    a[20]
except:
    logging.exception('Expected')
else:
    assert False


# Example 8
b = a[3:]
print('Before:   ', b)
b[1] = 99
print('After:    ', b)
print('No change:', a)


# Example 9
print('Before ', a)
a[2:7] = [99, 22, 14]
print('After  ', a)


# Example 10
print('Before ', a)
a[2:3] = [47, 11]
print('After  ', a)


# Example 11
b = a[:]
assert b == a and b is not a


# Example 12
b = a
print('Before a', a)
print('Before b', b)
a[:] = [101, 102, 103]
assert a is b             # Still the same list object
print('After a ', a)      # Now has different contents
print('After b ', b)      # Same list, so same contents as a
