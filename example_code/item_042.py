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
stock = {
    "nails": 125,
    "screws": 35,
    "wingnuts": 8,
    "washers": 24,
}

order = ["screws", "wingnuts", "clips"]

def get_batches(count, size):
    return count // size

result = {}
for name in order:
    count = stock.get(name, 0)
    batches = get_batches(count, 8)
    if batches:
        result[name] = batches

print(result)


print("Example 2")
found = {name: get_batches(stock.get(name, 0), 8)
         for name in order
         if get_batches(stock.get(name, 0), 8)}
print(found)


print("Example 3")
has_bug = {name: get_batches(stock.get(name, 0), 4)  # Wrong
           for name in order
           if get_batches(stock.get(name, 0), 8)}

print("Expected:", found)
print("Found:   ", has_bug)


print("Example 4")
found = {name: batches for name in order
         if (batches := get_batches(stock.get(name, 0), 8))}
assert found == {"screws": 4, "wingnuts": 1}, found


print("Example 5")
try:
    result = {name: (tenth := count // 10)
              for name, count in stock.items() if tenth > 0}
except:
    logging.exception('Expected')
else:
    assert False


print("Example 6")
result = {name: tenth for name, count in stock.items()
          if (tenth := count // 10) > 0}
print(result)


print("Example 7")
half = [(squared := last**2)
        for count in stock.values()
        if (last := count // 2) > 10]
print(f"Last item of {half} is {last} ** 2 = {squared}")


print("Example 8")
for count in stock.values():
    last = count // 2
    squared = last**2

print(f"{count} // 2 = {last}; {last} ** 2 = {squared}")


print("Example 9")
try:
    del count
    half = [count // 2 for count in stock.values()]
    print(half)   # Works
    print(count)  # Exception because loop variable didn't leak
except:
    logging.exception('Expected')
else:
    assert False


print("Example 10")
found = ((name, batches) for name in order
         if (batches := get_batches(stock.get(name, 0), 8)))
print(next(found))
print(next(found))
