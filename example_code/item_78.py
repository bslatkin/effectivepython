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
class DatabaseConnection:
    def __init__(self, host, port):
        pass

class DatabaseConnectionError(Exception):
    pass

def get_animals(database, species):
    # Query the Database
    raise DatabaseConnectionError('Not connected')
    # Return a list of (name, last_mealtime) tuples


# Example 2
try:
    database = DatabaseConnection('localhost', '4444')
    
    get_animals(database, 'Meerkat')
except:
    logging.exception('Expected')
else:
    assert False


# Example 3
from datetime import datetime
from unittest.mock import Mock

mock = Mock(spec=get_animals)
expected = [
    ('Spot', datetime(2019, 6, 5, 11, 15)),
    ('Fluffy', datetime(2019, 6, 5, 12, 30)),
    ('Jojo', datetime(2019, 6, 5, 12, 45)),
]
mock.return_value = expected


# Example 4
try:
    mock.does_not_exist
except:
    logging.exception('Expected')
else:
    assert False


# Example 5
database = object()
result = mock(database, 'Meerkat')
assert result == expected


# Example 6
mock.assert_called_once_with(database, 'Meerkat')


# Example 7
try:
    mock.assert_called_once_with(database, 'Giraffe')
except:
    logging.exception('Expected')
else:
    assert False


# Example 8
from unittest.mock import ANY

mock = Mock(spec=get_animals)
mock('database 1', 'Rabbit')
mock('database 2', 'Bison')
mock('database 3', 'Meerkat')

mock.assert_called_with(ANY, 'Meerkat')


# Example 9
try:
    class MyError(Exception):
        pass
    
    mock = Mock(spec=get_animals)
    mock.side_effect = MyError('Whoops! Big problem')
    result = mock(database, 'Meerkat')
except:
    logging.exception('Expected')
else:
    assert False


# Example 10
def get_food_period(database, species):
    # Query the Database
    pass
    # Return a time delta

def feed_animal(database, name, when):
    # Write to the Database
    pass

def do_rounds(database, species):
    now = datetime.datetime.utcnow()
    feeding_timedelta = get_food_period(database, species)
    animals = get_animals(database, species)
    fed = 0

    for name, last_mealtime in animals:
        if (now - last_mealtime) > feeding_timedelta:
            feed_animal(database, name, now)
            fed += 1

    return fed


# Example 11
def do_rounds(database, species, *,
              now_func=datetime.utcnow,
              food_func=get_food_period,
              animals_func=get_animals,
              feed_func=feed_animal):
    now = now_func()
    feeding_timedelta = food_func(database, species)
    animals = animals_func(database, species)
    fed = 0

    for name, last_mealtime in animals:
        if (now - last_mealtime) > feeding_timedelta:
            feed_func(database, name, now)
            fed += 1

    return fed


# Example 12
from datetime import timedelta

now_func = Mock(spec=datetime.utcnow)
now_func.return_value = datetime(2019, 6, 5, 15, 45)

food_func = Mock(spec=get_food_period)
food_func.return_value = timedelta(hours=3)

animals_func = Mock(spec=get_animals)
animals_func.return_value = [
    ('Spot', datetime(2019, 6, 5, 11, 15)),
    ('Fluffy', datetime(2019, 6, 5, 12, 30)),
    ('Jojo', datetime(2019, 6, 5, 12, 45)),
]

feed_func = Mock(spec=feed_animal)


# Example 13
result = do_rounds(
    database,
    'Meerkat',
    now_func=now_func,
    food_func=food_func,
    animals_func=animals_func,
    feed_func=feed_func)

assert result == 2


# Example 14
from unittest.mock import call

food_func.assert_called_once_with(database, 'Meerkat')

animals_func.assert_called_once_with(database, 'Meerkat')

feed_func.assert_has_calls(
    [
        call(database, 'Spot', now_func.return_value),
        call(database, 'Fluffy', now_func.return_value),
    ],
    any_order=True)


# Example 15
from unittest.mock import patch

print('Outside patch:', get_animals)

with patch('__main__.get_animals'):
    print('Inside patch: ', get_animals)

print('Outside again:', get_animals)


# Example 16
try:
    fake_now = datetime(2019, 6, 5, 15, 45)
    
    with patch('datetime.datetime.utcnow'):
        datetime.utcnow.return_value = fake_now
except:
    logging.exception('Expected')
else:
    assert False


# Example 17
def get_do_rounds_time():
    return datetime.datetime.utcnow()

def do_rounds(database, species):
    now = get_do_rounds_time()

with patch('__main__.get_do_rounds_time'):
    pass


# Example 18
def do_rounds(database, species, *, utcnow=datetime.utcnow):
    now = utcnow()
    feeding_timedelta = get_food_period(database, species)
    animals = get_animals(database, species)
    fed = 0

    for name, last_mealtime in animals:
        if (now - last_mealtime) > feeding_timedelta:
            feed_func(database, name, now)
            fed += 1

    return fed


# Example 19
from unittest.mock import DEFAULT

with patch.multiple('__main__',
                    autospec=True,
                    get_food_period=DEFAULT,
                    get_animals=DEFAULT,
                    feed_animal=DEFAULT):
    now_func = Mock(spec=datetime.utcnow)
    now_func.return_value = datetime(2019, 6, 5, 15, 45)
    get_food_period.return_value = timedelta(hours=3)
    get_animals.return_value = [
        ('Spot', datetime(2019, 6, 5, 11, 15)),
        ('Fluffy', datetime(2019, 6, 5, 12, 30)),
        ('Jojo', datetime(2019, 6, 5, 12, 45))
    ]


# Example 20
    result = do_rounds(database, 'Meerkat', utcnow=now_func)
    assert result == 2

    food_func.assert_called_once_with(database, 'Meerkat')
    animals_func.assert_called_once_with(database, 'Meerkat')
    feed_func.assert_has_calls(
        [
            call(database, 'Spot', now_func.return_value),
            call(database, 'Fluffy', now_func.return_value),
        ],
        any_order=True)
