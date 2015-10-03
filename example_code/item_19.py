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
def remainder(number, divisor):
    return number % divisor

assert remainder(20, 7) == 6


# Example 2
remainder(20, 7)
remainder(20, divisor=7)
remainder(number=20, divisor=7)
remainder(divisor=7, number=20)


# Example 3
try:
    # This will not compile
    source = """remainder(number=20, 7)"""
    eval(source)
except:
    logging.exception('Expected')
else:
    assert False


# Example 4
try:
    remainder(20, number=7)
except:
    logging.exception('Expected')
else:
    assert False


# Example 5
def flow_rate(weight_diff, time_diff):
    return weight_diff / time_diff

weight_diff = 0.5
time_diff = 3
flow = flow_rate(weight_diff, time_diff)
print('%.3f kg per second' % flow)
assert (flow - 0.16666666666666666) < 0.0001


# Example 6
def flow_rate(weight_diff, time_diff, period):
    return (weight_diff / time_diff) * period


# Example 7
flow_per_second = flow_rate(weight_diff, time_diff, 1)
assert (flow_per_second - 0.16666666666666666) < 0.0001


# Example 8
def flow_rate(weight_diff, time_diff, period=1):
    return (weight_diff / time_diff) * period


# Example 9
flow_per_second = flow_rate(weight_diff, time_diff)
assert (flow_per_second - 0.16666666666666666) < 0.0001
flow_per_hour = flow_rate(weight_diff, time_diff, period=3600)
assert flow_per_hour == 600.0


# Example 10
def flow_rate(weight_diff, time_diff,
              period=1, units_per_kg=1):
    return ((weight_diff * units_per_kg) / time_diff) * period


# Example 11
pounds_per_hour = flow_rate(weight_diff, time_diff,
                            period=3600, units_per_kg=2.2)
print(pounds_per_hour)
assert pounds_per_hour == 1320.0


# Example 12
pounds_per_hour = flow_rate(weight_diff, time_diff, 3600, 2.2)
print(pounds_per_hour)
assert pounds_per_hour == 1320.0
