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
class Point:
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y


print("Example 2")
def distance(left, right):
    return ((left.x - right.x) ** 2 + (left.y - right.y) ** 2) ** 0.5

origin1 = Point("source", 0, 0)
point1 = Point("destination", 3, 4)
print(distance(origin1, point1))


print("Example 3")
def bad_distance(left, right):
    left.x = -3
    return distance(left, right)


print("Example 4")
print(bad_distance(origin1, point1))
print(origin1.x)


print("Example 5")
class ImmutablePoint:
    def __init__(self, name, x, y):
        self.__dict__.update(name=name, x=x, y=y)

    def __setattr__(self, key, value):
        raise AttributeError("Immutable object: set not allowed")

    def __delattr__(self, key):
        raise AttributeError("Immutable object: del not allowed")


# Verify del is also prevented
try:
    point = ImmutablePoint("foo", 5, 10)
    del point.x
except AttributeError as e:
    assert str(e) == "Immutable object: del not allowed"
else:
    assert False


print("Example 6")
origin2 = ImmutablePoint("source", 0, 0)
assert distance(origin2, point1) == 5


print("Example 7")
try:
    bad_distance(origin2, point1)
except:
    logging.exception('Expected')
else:
    assert False


print("Example 8")
from dataclasses import dataclass

@dataclass(frozen=True)
class DataclassImmutablePoint:
    name: str
    x: float
    y: float


print("Example 9")
origin3 = DataclassImmutablePoint("origin", 0, 0)
assert distance(origin3, point1) == 5


print("Example 10")
try:
    bad_distance(origin3, point1)
except:
    logging.exception('Expected')
else:
    assert False


print("Example 13")
from typing import Any, Final, Never

class ImmutablePoint:
    name: Final[str]
    x: Final[int]
    y: Final[int]

    def __init__(self, name: str, x: int, y: int) -> None:
        self.name = name
        self.x = x
        self.y = y

    def __setattr__(self, key: str, value: Any) -> None:
        if key in self.__annotations__ and key not in dir(self):
            # Allow the very first assignment to happen
            super().__setattr__(key, value)
        else:
            raise AttributeError("Immutable object: set not allowed")

    def __delattr__(self, key: str) -> Never:
        raise AttributeError("Immutable object: del not allowed")

# Verify set is also prevented
try:
    point = ImmutablePoint("foo", 5, 10)
    point.x = -3
except AttributeError as e:
    assert str(e) == "Immutable object: set not allowed"
else:
    assert False

# Verify del is also prevented
try:
    point = ImmutablePoint("foo", 5, 10)
    del point.x
except AttributeError as e:
    assert str(e) == "Immutable object: del not allowed"
else:
    assert False


print("Example 14")
def translate(point, delta_x, delta_y):
    point.x += delta_x
    point.y += delta_y


print("Example 15")
try:
    point1 = ImmutablePoint("destination", 5, 3)
    translate(point1, 10, 20)
except:
    logging.exception('Expected')
else:
    assert False


print("Example 16")
def translate_copy(point, delta_x, delta_y):
    return ImmutablePoint(
        name=point.name,
        x=point.x + delta_x,
        y=point.y + delta_y,
    )


point1 = ImmutablePoint("destination", 5, 3)
point2 = translate_copy(point1, 10, 20)
assert point1.x == 5 and point1.y == 3
assert point2.x == 15 and point2.y == 23


print("Example 17")
class ImmutablePoint:
    def __init__(self, name, x, y):
        self.__dict__.update(name=name, x=x, y=y)

    def __setattr__(self, key, value):
        raise AttributeError("Immutable object: set not allowed")

    def __delattr__(self, key):
        raise AttributeError("Immutable object: del not allowed")


    def _replace(self, **overrides):
        fields = dict(
            name=self.name,
            x=self.x,
            y=self.y,
        )
        fields.update(overrides)
        cls = type(self)
        return cls(**fields)


print("Example 18")
def translate_replace(point, delta_x, delta_y):
    return point._replace(  # Changed
        x=point.x + delta_x,
        y=point.y + delta_y,
    )


point3 = ImmutablePoint("destination", 5, 3)
point4 = translate_replace(point3, 10, 20)
assert point3.x == 5 and point3.y == 3
assert point4.x == 15 and point4.y == 23


print("Example 19")
import dataclasses

def translate_dataclass(point, delta_x, delta_y):
    return dataclasses.replace(  # Changed
        point,
        x=point.x + delta_x,
        y=point.y + delta_y,
    )


point5 = DataclassImmutablePoint("destination", 5, 3)
point6 = translate_dataclass(point5, 10, 20)
assert point5.x == 5 and point5.y == 3
assert point6.x == 15 and point6.y == 23


print("Example 20")
my_dict = {}
my_dict["a"] = 123
my_dict["a"] = 456
print(my_dict)


print("Example 21")
my_set = set()
my_set.add("b")
my_set.add("b")
print(my_set)


print("Example 22")
class Point:
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y

point1 = Point("A", 5, 10)
point2 = Point("B", -7, 4)
charges = {
    point1: 1.5,
    point2: 3.5,
}


print("Example 23")
print(charges[point1])


print("Example 24")
try:
    point3 = Point("A", 5, 10)
    assert point1.x == point3.x
    assert point1.y == point3.y
    charges[point3]
except:
    logging.exception('Expected')
else:
    assert False


print("Example 25")
assert point1 != point3


print("Example 26")
class Point:
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y


    def __eq__(self, other):
        return (
            type(self) == type(other)
            and self.name == other.name
            and self.x == other.x
            and self.y == other.y
        )


print("Example 27")
point4 = Point("A", 5, 10)
point5 = Point("A", 5, 10)
assert point4 == point5


print("Example 28")
try:
    other_charges = {
        point4: 1.5,
    }
    other_charges[point5]
except:
    logging.exception('Expected')
else:
    assert False


print("Example 29")
class Point:
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y

    def __eq__(self, other):
        return (
            type(self) == type(other)
            and self.name == other.name
            and self.x == other.x
            and self.y == other.y
        )


    def __hash__(self):
        return hash((self.name, self.x, self.y))


print("Example 30")
point6 = Point("A", 5, 10)
point7 = Point("A", 5, 10)

more_charges = {
    point6: 1.5,
}
value = more_charges[point7]
assert value == 1.5


print("Example 31")
point8 = DataclassImmutablePoint("A", 5, 10)
point9 = DataclassImmutablePoint("A", 5, 10)

easy_charges = {
    point8: 1.5,
}
assert easy_charges[point9] == 1.5


print("Example 32")
my_set = {point8, point9}
assert my_set == {point8}
