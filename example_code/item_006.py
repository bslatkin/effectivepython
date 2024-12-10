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
first = (1, 2, 3)


print("Example 2")
second = (1, 2, 3,)
second_wrapped = (
    1,
    2,
    3,  # Optional comma
)


print("Example 3")
third = 1, 2, 3


print("Example 4")
fourth = 1, 2, 3,


print("Example 5")
assert first == second == third == fourth


print("Example 6")
empty = ()


print("Example 7")
single_with = (1,)
single_without = (1)
assert single_with != single_without
assert single_with[0] == single_without


print("Example 8")
single_parens = (1,)
single_no_parens = 1,
assert single_parens == single_no_parens


print("Example 9")
def calculate_refund(a, b, c):
    return 123_000_000

def get_order_value(a, b):
    pass

def get_tax(a, b):
    pass

def adjust_discount(a):
    return 1

import types
user = types.SimpleNamespace(address='Fake address')
order = types.SimpleNamespace(
    id='my order',
    dest='my destination')
to_refund = calculate_refund(
    get_order_value(user, order.id),
    get_tax(user.address, order.dest),
    adjust_discount(user) + 0.1),


print("Example 10")
print(type(to_refund))


print("Example 11")
to_refund2 = calculate_refund(
    get_order_value(user, order.id),
    get_tax(user.address, order.dest),
    adjust_discount(user) + 0.1,
)  # No trailing comma
print(type(to_refund2))


print("Example 12")
value_a = 1,    # No parentheses, right
list_b = [1,]   # No parentheses, wrong
list_c = [(1,)] # Parentheses, right
print('A:', value_a)
print('B:', list_b)
print('C:', list_c)


print("Example 13")
def get_coupon_codes(user):
    return [['DEAL20']]

(a1,), = get_coupon_codes(user)
(a2,) = get_coupon_codes(user)
(a3), = get_coupon_codes(user)
(a4) = get_coupon_codes(user)
a5, = get_coupon_codes(user)
a6 = get_coupon_codes(user)

assert a1 not in (a2, a3, a4, a5, a6)
assert a2 == a3 == a5
assert a4 == a6
