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
def safe_division(number, divisor,
                  ignore_overflow,
                  ignore_zero_division):
    try:
        return number / divisor
    except OverflowError:
        if ignore_overflow:
            return 0
        else:
            raise
    except ZeroDivisionError:
        if ignore_zero_division:
            return float('inf')
        else:
            raise


# Example 2
result = safe_division(1.0, 10**500, True, False)
print(result)


# Example 3
result = safe_division(1.0, 0, False, True)
print(result)


# Example 4
def safe_division_b(number, divisor,
                    ignore_overflow=False,        # Changed
                    ignore_zero_division=False):  # Changed
    try:
        return number / divisor
    except OverflowError:
        if ignore_overflow:
            return 0
        else:
            raise
    except ZeroDivisionError:
        if ignore_zero_division:
            return float('inf')
        else:
            raise


# Example 5
result = safe_division_b(1.0, 10**500, ignore_overflow=True)
print(result)

result = safe_division_b(1.0, 0, ignore_zero_division=True)
print(result)


# Example 6
assert safe_division_b(1.0, 10**500, True, False) == 0


# Example 7
def safe_division_c(number, divisor, *,  # Changed
                    ignore_overflow=False,
                    ignore_zero_division=False):
    try:
        return number / divisor
    except OverflowError:
        if ignore_overflow:
            return 0
        else:
            raise
    except ZeroDivisionError:
        if ignore_zero_division:
            return float('inf')
        else:
            raise


# Example 8
try:
    safe_division_c(1.0, 10**500, True, False)
except:
    logging.exception('Expected')
else:
    assert False


# Example 9
result = safe_division_c(1.0, 0, ignore_zero_division=True)
assert result == float('inf')

try:
    result = safe_division_c(1.0, 0)
except ZeroDivisionError:
    pass  # Expected
else:
    assert False


# Example 10
assert safe_division_c(number=2, divisor=5) == 0.4
assert safe_division_c(divisor=5, number=2) == 0.4
assert safe_division_c(2, divisor=5) == 0.4


# Example 11
def safe_division_c(numerator, denominator, *,  # Changed
                    ignore_overflow=False,
                    ignore_zero_division=False):
    try:
        return numerator / denominator
    except OverflowError:
        if ignore_overflow:
            return 0
        else:
            raise
    except ZeroDivisionError:
        if ignore_zero_division:
            return float('inf')
        else:
            raise


# Example 12
try:
    safe_division_c(number=2, divisor=5)
except:
    logging.exception('Expected')
else:
    assert False


# Example 13
def safe_division_d(numerator, denominator, /, *,  # Changed
                    ignore_overflow=False,
                    ignore_zero_division=False):
    try:
        return numerator / denominator
    except OverflowError:
        if ignore_overflow:
            return 0
        else:
            raise
    except ZeroDivisionError:
        if ignore_zero_division:
            return float('inf')
        else:
            raise


# Example 14
assert safe_division_d(2, 5) == 0.4


# Example 15
try:
    safe_division_d(numerator=2, denominator=5)
except:
    logging.exception('Expected')
else:
    assert False


# Example 16
def safe_division_e(numerator, denominator, /,
                    ndigits=10, *,                # Changed
                    ignore_overflow=False,
                    ignore_zero_division=False):
    try:
        fraction = numerator / denominator        # Changed
        return round(fraction, ndigits)           # Changed
    except OverflowError:
        if ignore_overflow:
            return 0
        else:
            raise
    except ZeroDivisionError:
        if ignore_zero_division:
            return float('inf')
        else:
            raise


# Example 17
result = safe_division_e(22, 7)
print(result)

result = safe_division_e(22, 7, 5)
print(result)

result = safe_division_e(22, 7, ndigits=2)
print(result)
