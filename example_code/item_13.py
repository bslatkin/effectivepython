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
try:
    car_ages = [0, 9, 4, 8, 7, 20, 19, 1, 6, 15]
    car_ages_descending = sorted(car_ages, reverse=True)
    oldest, second_oldest = car_ages_descending
except:
    logging.exception('Expected')
else:
    assert False


# Example 2
oldest = car_ages_descending[0]
second_oldest = car_ages_descending[1]
others = car_ages_descending[2:]
print(oldest, second_oldest, others)


# Example 3
oldest, second_oldest, *others = car_ages_descending
print(oldest, second_oldest, others)


# Example 4
oldest, *others, youngest = car_ages_descending
print(oldest, youngest, others)

*others, second_youngest, youngest = car_ages_descending
print(youngest, second_youngest, others)


# Example 5
try:
    # This will not compile
    source = """*others = car_ages_descending"""
    eval(source)
except:
    logging.exception('Expected')
else:
    assert False


# Example 6
try:
    # This will not compile
    source = """first, *middle, *second_middle, last = [1, 2, 3, 4]"""
    eval(source)
except:
    logging.exception('Expected')
else:
    assert False


# Example 7
car_inventory = {
	'Downtown': ('Silver Shadow', 'Pinto', 'DMC'),
	'Airport': ('Skyline', 'Viper', 'Gremlin', 'Nova'),
}

((loc1, (best1, *rest1)),
 (loc2, (best2, *rest2))) = car_inventory.items()

print(f'Best at {loc1} is {best1}, {len(rest1)} others')
print(f'Best at {loc2} is {best2}, {len(rest2)} others')


# Example 8
short_list = [1, 2]
first, second, *rest = short_list
print(first, second, rest)


# Example 9
it = iter(range(1, 3))
first, second = it
print(f'{first} and {second}')


# Example 10
def generate_csv():
	yield ('Date', 'Make' , 'Model', 'Year', 'Price')
	for i in range(100):
		yield ('2019-03-25', 'Honda', 'Fit' , '2010', '$3400')
		yield ('2019-03-26', 'Ford', 'F150' , '2008', '$2400')


# Example 11
all_csv_rows = list(generate_csv())
header = all_csv_rows[0]
rows = all_csv_rows[1:]
print('CSV Header:', header)
print('Row count: ', len(rows))


# Example 12
it = generate_csv()
header, *rows = it
print('CSV Header:', header)
print('Row count: ', len(rows))
