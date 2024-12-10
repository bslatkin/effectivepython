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
try:
    search_key = "red"
    my_dict = {"red": 1, "blue": 2, "green": 3}
    
    for key in my_dict:
        if key == "blue":
            my_dict["yellow"] = 4  # Causes error
except:
    logging.exception('Expected')
else:
    assert False


print("Example 2")
try:
    my_dict = {"red": 1, "blue": 2, "green": 3}
    for key in my_dict:
        if key == "blue":
            del my_dict["green"]  # Causes error
except:
    logging.exception('Expected')
else:
    assert False


print("Example 3")
my_dict = {"red": 1, "blue": 2, "green": 3}
for key in my_dict:
    if key == "blue":
        my_dict["green"] = 4  # Okay
print(my_dict)


print("Example 4")
try:
    my_set = {"red", "blue", "green"}
    
    for color in my_set:
        if color == "blue":
            my_set.add("yellow")  # Causes error
except:
    logging.exception('Expected')
else:
    assert False


print("Example 5")
my_set = {"red", "blue", "green"}
for color in my_set:
    if color == "blue":
        my_set.add("green")  # Okay

print(my_set)


print("Example 6")
my_list = [1, 2, 3]

for number in my_list:
    print(number)
    if number == 2:
        my_list[0] = -1  # Okay

print(my_list)


print("Example 7")
my_list = [1, 2, 3]
bad_count = 0

for number in my_list:
    print(number)
    if number == 2:
        my_list.insert(0, 4)  # Causes error
    # Break out of the infinite loop
    bad_count += 1
    if bad_count > 5:
        print("...")
        break


print("Example 8")
my_list = [1, 2, 3]

for number in my_list:
    print(number)
    if number == 2:
        my_list.append(4)  # Okay this time

print(my_list)


print("Example 9")
my_dict = {"red": 1, "blue": 2, "green": 3}

keys_copy = list(my_dict.keys())  # Copy
for key in keys_copy:             # Iterate over copy
    if key == "blue":
        my_dict["green"] = 4      # Modify original dict

print(my_dict)


print("Example 10")
my_list = [1, 2, 3]

list_copy = list(my_list)     # Copy
for number in list_copy:      # Iterate over copy
    print(number)
    if number == 2:
        my_list.insert(0, 4)  # Inserts in original list

print(my_list)


print("Example 11")
my_set = {"red", "blue", "green"}

set_copy = set(my_set)        # Copy
for color in set_copy:        # Iterate over copy
    if color == "blue":
        my_set.add("yellow")  # Add to original set

print(my_set)


print("Example 12")
my_dict = {"red": 1, "blue": 2, "green": 3}
modifications = {}

for key in my_dict:
    if key == "blue":
        modifications["green"] = 4  # Add to staging

my_dict.update(modifications)       # Merge modifications
print(my_dict)


print("Example 13")
my_dict = {"red": 1, "blue": 2, "green": 3}
modifications = {}

for key in my_dict:
    if key == "blue":
        modifications["green"] = 4
    value = my_dict[key]
    if value == 4:                   # This condition is never true
        modifications["yellow"] = 5

my_dict.update(modifications)        # Merge modifications
print(my_dict)


print("Example 14")
my_dict = {"red": 1, "blue": 2, "green": 3}
modifications = {}

for key in my_dict:
    if key == "blue":
        modifications["green"] = 4
    value = my_dict[key]
    other_value = modifications.get(key)  # Check cache
    if value == 4 or other_value == 4:
        modifications["yellow"] = 5

my_dict.update(modifications)             # Merge modifications
print(my_dict)
