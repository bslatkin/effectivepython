#!/usr/bin/env python3

# Copyright 2014 Brett Slatkin, Pearson Education Inc.
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

# Preamble to mimick book environment
import logging
from pprint import pprint
from sys import stdout as STDOUT


# Example 1
def safe_division(number, divisor, ignore_overflow,
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
result = safe_division(1, 10**500, True, False)
print(result)
assert result == 0


# Example 3
result = safe_division(1, 0, False, True)
print(result)
assert result == float('inf')


# Example 4
def safe_division_b(number, divisor,
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


# Example 5
assert safe_division_b(1, 10**500, ignore_overflow=True) == 0
assert safe_division_b(1, 0, ignore_zero_division=True) == float('inf')


# Example 6
assert safe_division_b(1, 10**500, True, False) == 0


# Example 7
def safe_division_c(number, divisor, *,
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
    safe_division_c(1, 10**500, True, False)
except:
    logging.exception('Expected')
else:
    assert False


# Example 9
safe_division_c(1, 0, ignore_zero_division=True)  # No exception
try:
    safe_division_c(1, 0)
    assert False
except ZeroDivisionError:
    pass  # Expected
