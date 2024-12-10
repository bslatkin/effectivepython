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
def normalize(numbers):
    total = sum(numbers)
    result = []
    for value in numbers:
        percent = 100 * value / total
        result.append(percent)
    return result


print("Example 2")
visits = [15, 35, 80]
percentages = normalize(visits)
print(percentages)
assert sum(percentages) == 100.0


print("Example 3")
path = "my_numbers.txt"
with open(path, "w") as f:
    for i in (15, 35, 80):
        f.write(f"{i}\n")

def read_visits(data_path):
    with open(data_path) as f:
        for line in f:
            yield int(line)


print("Example 4")
it = read_visits("my_numbers.txt")
percentages = normalize(it)
print(percentages)


print("Example 5")
it = read_visits("my_numbers.txt")
print(list(it))
print(list(it))  # Already exhausted


print("Example 6")
def normalize_copy(numbers):
    numbers_copy = list(numbers)  # Copy the iterator
    total = sum(numbers_copy)
    result = []
    for value in numbers_copy:
        percent = 100 * value / total
        result.append(percent)
    return result


print("Example 7")
it = read_visits("my_numbers.txt")
percentages = normalize_copy(it)
print(percentages)
assert sum(percentages) == 100.0


print("Example 8")
def normalize_func(get_iter):
    total = sum(get_iter())   # New iterator
    result = []
    for value in get_iter():  # New iterator
        percent = 100 * value / total
        result.append(percent)
    return result


print("Example 9")
path = "my_numbers.txt"
percentages = normalize_func(lambda: read_visits(path))
print(percentages)
assert sum(percentages) == 100.0


print("Example 10")
class ReadVisits:
    def __init__(self, data_path):
        self.data_path = data_path

    def __iter__(self):
        with open(self.data_path) as f:
            for line in f:
                yield int(line)


print("Example 11")
visits = ReadVisits(path)
percentages = normalize(visits)  # Changed
print(percentages)
assert sum(percentages) == 100.0


print("Example 12")
def normalize_defensive(numbers):
    if iter(numbers) is numbers:  # An iterator -- bad!
        raise TypeError("Must supply a container")
    total = sum(numbers)
    result = []
    for value in numbers:
        percent = 100 * value / total
        result.append(percent)
    return result


visits = [15, 35, 80]
normalize_defensive(visits)  # No error

it = iter(visits)
try:
    normalize_defensive(it)
except TypeError:
    pass
else:
    assert False


print("Example 13")
from collections.abc import Iterator

def normalize_defensive(numbers):
    if isinstance(numbers, Iterator):  # Another way to check
        raise TypeError("Must supply a container")
    total = sum(numbers)
    result = []
    for value in numbers:
        percent = 100 * value / total
        result.append(percent)
    return result


visits = [15, 35, 80]
normalize_defensive(visits)  # No error

it = iter(visits)
try:
    normalize_defensive(it)
except TypeError:
    pass
else:
    assert False


print("Example 14")
visits_list = [15, 35, 80]
list_percentages = normalize_defensive(visits_list)

visits_obj = ReadVisits(path)
obj_percentages = normalize_defensive(visits_obj)

assert list_percentages == obj_percentages
assert sum(percentages) == 100.0


print("Example 15")
try:
    visits = [15, 35, 80]
    it = iter(visits)
    normalize_defensive(it)
except:
    logging.exception('Expected')
else:
    assert False
