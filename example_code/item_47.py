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
rate = 1.45
seconds = 3*60 + 42
cost = rate * seconds / 60
print(cost)


# Example 2
print(round(cost, 2))


# Example 3
rate = 0.05
seconds = 5
cost = rate * seconds / 60
print(cost)


# Example 4
print(round(cost, 2))


# Example 5
from decimal import Decimal
from decimal import ROUND_UP
rate = Decimal('1.45')
seconds = Decimal('222')  # 3*60 + 42
cost = rate * seconds / Decimal('60')
print(cost)


# Example 6
rounded = cost.quantize(Decimal('0.01'), rounding=ROUND_UP)
print(rounded)


# Example 7
rate = Decimal('0.05')
seconds = Decimal('5')
cost = rate * seconds / Decimal('60')
print(cost)


# Example 8
rounded = cost.quantize(Decimal('0.01'), rounding=ROUND_UP)
print(rounded)
