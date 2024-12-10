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
try:
    list_a = [1, 2, 3]
    assert list_a, "a empty"
    list_b = []
    assert list_b, "b empty"  # Raises
except:
    logging.exception('Expected')
else:
    assert False


print("Example 2")
try:
    class EmptyError(Exception):
        pass
    
    list_c = []
    if not list_c:
        raise EmptyError("c empty")
except:
    logging.exception('Expected')
else:
    assert False


print("Example 3")
try:
    raise EmptyError("From raise statement")
except EmptyError as e:
    print(f"Caught: {e}")


print("Example 4")
try:
    assert False, "From assert statement"
except AssertionError as e:
    print(f"Caught: {e}")


print("Example 5")
class RatingError(Exception):
    pass

class Rating:
    def __init__(self, max_rating):
        if not (max_rating > 0):
            raise RatingError("Invalid max_rating")
        self.max_rating = max_rating
        self.ratings = []

    def rate(self, rating):
        if not (0 < rating <= self.max_rating):
            raise RatingError("Invalid rating")
        self.ratings.append(rating)


print("Example 6")
try:
    movie = Rating(5)
    movie.rate(5)
    movie.rate(7)  # Raises
except:
    logging.exception('Expected')
else:
    assert False


print("Example 7")
class RatingInternal:
    def __init__(self, max_rating):
        assert max_rating > 0, f"Invalid {max_rating=}"
        self.max_rating = max_rating
        self.ratings = []

    def rate(self, rating):
        assert 0 < rating <= self.max_rating, f"Invalid {rating=}"
        self.ratings.append(rating)


print("Example 8")
try:
    movie = RatingInternal(5)
    movie.rate(5)
    movie.rate(7)  # Raises
except:
    logging.exception('Expected')
else:
    assert False
