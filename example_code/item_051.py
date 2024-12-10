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
class RGB:
    def __init__(self, red, green, blue):
        self.red = red
        self.green = green
        self.blue = blue


print("Example 2")
class BadRGB:
    def __init__(self, green, red, blue):  # Bad: Order swapped
        self.red = red
        self.green = green
        self.bloe = blue                   # Bad: Typo


print("Example 3")
from dataclasses import dataclass

@dataclass
class DataclassRGB:
    red: int
    green: int
    blue: int


print("Example 6")
from typing import Any

@dataclass
class DataclassRGB:
    red: Any
    green: Any
    blue: Any


print("Example 7")
color1 = RGB(red=1, green=2, blue=3)
color2 = RGB(1, 2, 3)
color3 = RGB(1, 2, blue=3)
print(color1.__dict__)
print(color2.__dict__)
print(color3.__dict__)


print("Example 8")
class RGB:
    def __init__(self, *, red, green, blue):  # Changed
        self.red = red
        self.green = green
        self.blue = blue


print("Example 9")
color4 = RGB(red=1, green=2, blue=3)


print("Example 10")
try:
    RGB(1, 2, 3)
except:
    logging.exception('Expected')
else:
    assert False


print("Example 11")
@dataclass(kw_only=True)
class DataclassRGB:
    red: int
    green: int
    blue: int


print("Example 12")
color5 = DataclassRGB(red=1, green=2, blue=3)
print(color5)


print("Example 13")
try:
    DataclassRGB(1, 2, 3)
except:
    logging.exception('Expected')
else:
    assert False


print("Example 14")
class RGBA:
    def __init__(self, *, red, green, blue, alpha=1.0):
        self.red = red
        self.green = green
        self.blue = blue
        self.alpha = alpha


print("Example 15")
color1 = RGBA(red=1, green=2, blue=3)
print(
    color1.red,
    color1.green,
    color1.blue,
    color1.alpha,
)


print("Example 16")
@dataclass(kw_only=True)
class DataclassRGBA:
    red: int
    green: int
    blue: int
    alpha: int = 1.0


print("Example 17")
color2 = DataclassRGBA(red=1, green=2, blue=3)
print(color2)


print("Example 18")
class BadContainer:
    def __init__(self, *, value=[]):
        self.value = value

obj1 = BadContainer()
obj2 = BadContainer()
obj1.value.append(1)
print(obj2.value)  # Should be empty, but isn't


print("Example 19")
class MyContainer:
    def __init__(self, *, value=None):
        if value is None:
            value = []  # Create when not supplied
        self.value = value


print("Example 20")
obj1 = MyContainer()
obj2 = MyContainer()
obj1.value.append(1)
assert obj1.value == [1]
assert obj2.value == []


print("Example 21")
from dataclasses import field

@dataclass
class DataclassContainer:
    value: list = field(default_factory=list)


print("Example 22")
obj1 = DataclassContainer()
obj2 = DataclassContainer()
obj1.value.append(1)
assert obj1.value == [1]
assert obj2.value == []


print("Example 23")
color1 = RGB(red=1, green=2, blue=3)
print(color1)


print("Example 24")
class RGB:
    def __init__(self, *, red, green, blue):
        self.red = red
        self.green = green
        self.blue = blue


    def __repr__(self):
        return (
            f"{type(self).__module__}"
            f".{type(self).__name__}("
            f"red={self.red!r}, "
            f"green={self.green!r}, "
            f"blue={self.blue!r})"
        )


print("Example 25")
color1 = RGB(red=1, green=2, blue=3)
print(color1)


print("Example 26")
color2 = DataclassRGB(red=1, green=2, blue=3)
print(color2)


print("Example 27")
class RGB:
    def __init__(self, red, green, blue):
        self.red = red
        self.green = green
        self.blue = blue


    def _astuple(self):
        return (self.red, self.green, self.blue)


print("Example 28")
color1 = RGB(1, 2, 3)
print(color1._astuple())


print("Example 29")
color2 = RGB(*color1._astuple())
print(color2.red, color2.green, color2.blue)


print("Example 30")
@dataclass
class DataclassRGB:
    red: int
    green: int
    blue: int

from dataclasses import astuple

color3 = DataclassRGB(1, 2, 3)
print(astuple(color3))


print("Example 31")
class RGB:
    def __init__(self, red, green, blue):
        self.red = red
        self.green = green
        self.blue = blue

    def __repr__(self):
        return (
            f"{type(self).__module__}"
            f".{type(self).__name__}("
            f"red={self.red!r}, "
            f"green={self.green!r}, "
            f"blue={self.blue!r})"
        )


    def _asdict(self):
        return dict(
            red=self.red,
            green=self.green,
            blue=self.blue,
        )


print("Example 32")
import json

color1 = RGB(red=1, green=2, blue=3)
data = json.dumps(color1._asdict())
print(data)


print("Example 33")
color2 = RGB(**color1._asdict())
print(color2)


print("Example 34")
from dataclasses import asdict

color3 = DataclassRGB(red=1, green=2, blue=3)
print(asdict(color3))


print("Example 35")
color1 = RGB(1, 2, 3)
color2 = RGB(1, 2, 3)
print(color1 == color2)


print("Example 36")
assert color1 == color1
assert color1 is color1
assert color1 != color2
assert color1 is not color2


print("Example 37")
class RGB:
    def __init__(self, red, green, blue):
        self.red = red
        self.green = green
        self.blue = blue

    def __repr__(self):
        return (
            f"{type(self).__module__}"
            f".{type(self).__name__}("
            f"red={self.red!r}, "
            f"green={self.green!r}, "
            f"blue={self.blue!r})"
        )

    def _astuple(self):
        return (self.red, self.green, self.blue)


    def __eq__(self, other):
        return (
            type(self) == type(other)
            and self._astuple() == other._astuple()
        )


print("Example 38")
color1 = RGB(1, 2, 3)
color2 = RGB(1, 2, 3)
color3 = RGB(5, 6, 7)
assert color1 == color1
assert color1 == color2
assert color1 is not color2
assert color1 != color3


print("Example 39")
color4 = DataclassRGB(1, 2, 3)
color5 = DataclassRGB(1, 2, 3)
color6 = DataclassRGB(5, 6, 7)
assert color4 == color4
assert color4 == color5
assert color4 is not color5
assert color4 != color6


print("Example 40")
class Planet:
    def __init__(self, distance, size):
        self.distance = distance
        self.size = size

    def __repr__(self):
        return (
            f"{type(self).__module__}"
            f"{type(self).__name__}("
            f"distance={self.distance}, "
            f"size={self.size})"
        )


print("Example 41")
try:
    far = Planet(10, 5)
    near = Planet(1, 2)
    data = [far, near]
    data.sort()
except:
    logging.exception('Expected')
else:
    assert False


print("Example 42")
class Planet:
    def __init__(self, distance, size):
        self.distance = distance
        self.size = size

    def __repr__(self):
        return (
            f"{type(self).__module__}"
            f"{type(self).__name__}("
            f"distance={self.distance}, "
            f"size={self.size})"
        )


    def _astuple(self):
        return (self.distance, self.size)

    def __eq__(self, other):
        return (
            type(self) == type(other)
            and self._astuple() == other._astuple()
        )

    def __lt__(self, other):
        if type(self) != type(other):
            return NotImplemented
        return self._astuple() < other._astuple()

    def __le__(self, other):
        if type(self) != type(other):
            return NotImplemented
        return self._astuple() <= other._astuple()

    def __gt__(self, other):
        if type(self) != type(other):
            return NotImplemented
        return self._astuple() > other._astuple()

    def __ge__(self, other):
        if type(self) != type(other):
            return NotImplemented
        return self._astuple() >= other._astuple()


# Verify that NotImplemented works correctly
try:
    Planet(5, 10) > 8
except TypeError:
    pass
else:
    assert False


print("Example 43")
far = Planet(10, 2)
near = Planet(1, 5)
data = [far, near]
data.sort()
print(data)


print("Example 44")
@dataclass(order=True)
class DataclassPlanet:
    distance: float
    size: float


print("Example 45")
far2 = DataclassPlanet(10, 2)
near2 = DataclassPlanet(1, 5)
assert far2 > near2
assert near2 < far2
