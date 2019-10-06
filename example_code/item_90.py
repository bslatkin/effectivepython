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
try:
    def subtract(a, b):
        return a - b
    
    subtract(10, '5')
except:
    logging.exception('Expected')
else:
    assert False


# Example 3
try:
    def concat(a, b):
        return a + b
    
    concat('first', b'second')
except:
    logging.exception('Expected')
else:
    assert False


# Example 5
class Counter:
    def __init__(self):
        self.value = 0

    def add(self, offset):
        value += offset

    def get(self) -> int:
        self.value


# Example 6
try:
    counter = Counter()
    counter.add(5)
except:
    logging.exception('Expected')
else:
    assert False


# Example 7
try:
    counter = Counter()
    found = counter.get()
    assert found == 0, found
except:
    logging.exception('Expected')
else:
    assert False


# Example 9
try:
    def combine(func, values):
        assert len(values) > 0
    
        result = values[0]
        for next_value in values[1:]:
            result = func(result, next_value)
    
        return result
    
    def add(x, y):
        return x + y
    
    inputs = [1, 2, 3, 4j]
    result = combine(add, inputs)
    assert result == 10, result  # Fails
except:
    logging.exception('Expected')
else:
    assert False


# Example 11
try:
    def get_or_default(value, default): 
        if value is not None:
            return value
        return value
    
    found = get_or_default(3, 5)
    assert found == 3
    
    found = get_or_default(None, 5)
    assert found == 5, found  # Fails
except:
    logging.exception('Expected')
else:
    assert False


# Example 13
class FirstClass:
    def __init__(self, value):
        self.value = value

class SecondClass:
    def __init__(self, value):
        self.value = value

second = SecondClass(5)
first = FirstClass(second)

del FirstClass
del SecondClass


# Example 15
try:
    class FirstClass:
        def __init__(self, value: SecondClass) -> None:  # Breaks
            self.value = value
    
    class SecondClass:
        def __init__(self, value: int) -> None:
            self.value = value
    
    second = SecondClass(5)
    first = FirstClass(second)
except:
    logging.exception('Expected')
else:
    assert False


# Example 16
class FirstClass:
    def __init__(self, value: 'SecondClass') -> None:  # OK
        self.value = value

class SecondClass:
    def __init__(self, value: int) -> None:
        self.value = value

second = SecondClass(5)
first = FirstClass(second)
