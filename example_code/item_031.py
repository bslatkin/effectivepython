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
def get_stats(numbers):
    minimum = min(numbers)
    maximum = max(numbers)
    return minimum, maximum

lengths = [63, 73, 72, 60, 67, 66, 71, 61, 72, 70]

minimum, maximum = get_stats(lengths)  # Two return values

print(f"Min: {minimum}, Max: {maximum}")


print("Example 2")
first, second = 1, 2
assert first == 1
assert second == 2

def my_function():
    return 1, 2

first, second = my_function()
assert first == 1
assert second == 2


print("Example 3")
def get_avg_ratio(numbers):
    average = sum(numbers) / len(numbers)
    scaled = [x / average for x in numbers]
    scaled.sort(reverse=True)
    return scaled

longest, *middle, shortest = get_avg_ratio(lengths)

print(f"Longest:  {longest:>4.0%}")
print(f"Shortest: {shortest:>4.0%}")


print("Example 4")
def get_median(numbers):
    count = len(numbers)
    sorted_numbers = sorted(numbers)
    middle = count // 2
    if count % 2 == 0:
        lower = sorted_numbers[middle - 1]
        upper = sorted_numbers[middle]
        median = (lower + upper) / 2
    else:
        median = sorted_numbers[middle]
    return median

def get_stats_more(numbers):
    minimum = min(numbers)
    maximum = max(numbers)
    count = len(numbers)
    average = sum(numbers) / count
    median = get_median(numbers)
    return minimum, maximum, average, median, count

minimum, maximum, average, median, count = get_stats_more(lengths)

print(f"Min: {minimum}, Max: {maximum}")
print(f"Average: {average}, Median: {median}, Count {count}")

assert minimum == 60
assert maximum == 73
assert average == 67.5
assert median == 68.5
assert count == 10

# Verify odd count median
_, _, _, median, count = get_stats_more([1, 2, 3])
assert median == 2
assert count == 3


print("Example 5")
# Correct:
minimum, maximum, average, median, count = get_stats_more(lengths)

# Oops! Median and average swapped:
minimum, maximum, median, average, count = get_stats_more(lengths)


print("Example 6")
minimum, maximum, average, median, count = get_stats_more(
    lengths)

minimum, maximum, average, median, count = \
    get_stats_more(lengths)

(minimum, maximum, average,
 median, count) = get_stats_more(lengths)

(minimum, maximum, average, median, count
    ) = get_stats_more(lengths)


print("Example 7")
from dataclasses import dataclass

@dataclass
class Stats:
    minimum: float
    maximum: float
    average: float
    median: float
    count: int

def get_stats_obj(numbers):
    return Stats(
        minimum=min(numbers),
        maximum=max(numbers),
        count=len(numbers),
        average=sum(numbers) / count,
        median=get_median(numbers),
    )

result = get_stats_obj(lengths)
print(result)

assert result.minimum == 60
assert result.maximum == 73
assert result.average == 67.5
assert result.median == 68.5
assert result.count == 10

# Verify odd count median
result2 = get_stats_obj([1, 2, 3])
assert result2.median == 2
assert result2.count == 3
