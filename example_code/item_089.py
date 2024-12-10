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
def my_func():
    try:
        return 123
    finally:
        print("Finally my_func")

print("Before")
print(my_func())
print("After")


print("Example 2")
def my_generator():
    try:
        yield 10
        yield 20
        yield 30
    finally:
        print("Finally my_generator")

print("Before")

for i in my_generator():
    print(i)

print("After")


print("Example 3")
it = my_generator()
print("Before")
print(next(it))
print(next(it))
print("After")


print("Example 4")
import gc

del it
gc.collect()


print("Example 5")
def catching_generator():
    try:
        yield 40
        yield 50
        yield 60
    except BaseException as e:  # Catches GeneratorExit
        print("Catching handler", type(e), e)
        raise


print("Example 6")
it = catching_generator()
print("Before")
print(next(it))
print(next(it))
print("After")
del it
gc.collect()


print("Example 8")
with open("my_file.txt", "w") as f:
    for _ in range(20):
        f.write("a" * random.randint(0, 100))
        f.write("\n")

def lengths_path(path):
    try:
        with open(path) as handle:
            for i, line in enumerate(handle):
                print(f"Line {i}")
                yield len(line.strip())
    finally:
        print("Finally lengths_path")


print("Example 9")
max_head = 0
it = lengths_path("my_file.txt")

for i, length in enumerate(it):
    if i == 5:
        break
    else:
        max_head = max(max_head, length)

print(max_head)


print("Example 10")
del it
gc.collect()


print("Example 11")
def lengths_handle(handle):
    try:
        for i, line in enumerate(handle):
            print(f"Line {i}")
            yield len(line.strip())
    finally:
        print("Finally lengths_handle")


print("Example 12")
max_head = 0

with open("my_file.txt") as handle:
    it = lengths_handle(handle)
    for i, length in enumerate(it):
        if i == 5:
            break
        else:
            max_head = max(max_head, length)

print(max_head)
print("Handle closed:", handle.closed)
