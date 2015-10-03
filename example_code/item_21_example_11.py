#!/usr/bin/env python2.7

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


# Example 11
def safe_division_d(number, divisor, **kwargs):
    ignore_overflow = kwargs.pop('ignore_overflow', False)
    ignore_zero_div = kwargs.pop('ignore_zero_division', False)
    if kwargs:
        raise TypeError('Unexpected **kwargs: %r' % kwargs)
    try:
        return number / divisor
    except OverflowError:
        if ignore_overflow:
            return 0
        else:
            raise
    except ZeroDivisionError:
        if ignore_zero_div:
            return float('inf')
        else:
            raise

assert safe_division_d(1.0, 10) == 0.1
assert safe_division_d(1.0, 0, ignore_zero_division=True) == float('inf')
assert safe_division_d(1.0, 10**500, ignore_overflow=True) == 0.0

# Example 12
try:
    safe_division_d(1.0, 0, False, True)
except:
    logging.exception('Expected')
else:
    assert False


# Example 13
try:
    safe_division_d(0.0, 0, unexpected=True)
except:
    logging.exception('Expected')
else:
    assert False
