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
def dot_product(a, b):
    result = 0
    for i, j in zip(a, b):
        result += i * j
    return result

print(dot_product([1, 2], [3, 4]))


print("Example 2")
import ctypes

library_path = ...

import pathlib

run_py = pathlib.Path(__file__)
library_path = run_py.parent / "item_095" / "my_library" / "my_library.lib"

my_library = ctypes.cdll.LoadLibrary(library_path)


print("Example 3")
print(my_library.dot_product)


print("Example 4")
my_library.dot_product.restype = ctypes.c_double

vector_ptr = ctypes.POINTER(ctypes.c_double)
my_library.dot_product.argtypes = (
    ctypes.c_int,
    vector_ptr,
    vector_ptr,
)


print("Example 5")
size = 3
vector3 = ctypes.c_double * size
a = vector3(1.0, 2.5, 3.5)
b = vector3(-7, 4, -12.1)


print("Example 6")
result = my_library.dot_product(
    3,
    ctypes.cast(a, vector_ptr),
    ctypes.cast(b, vector_ptr),
)
print(result)


print("Example 7")
def dot_product(a, b):
    size = len(a)
    assert len(b) == size
    a_vector = vector3(*a)
    b_vector = vector3(*b)
    result = my_library.dot_product(size, a_vector, b_vector)
    return result

result = dot_product([1.0, 2.5, 3.5], [-7, 4, -12.1])
print(result)


print("Example 8")
from unittest import TestCase

class MyLibraryTest(TestCase):

    def test_dot_product(self):
        vector3 = ctypes.c_double * size
        a = vector3(1.0, 2.5, 3.5)
        b = vector3(-7, 4, -12.1)
        vector_ptr = ctypes.POINTER(ctypes.c_double)
        result = my_library.dot_product(
            3,
            ctypes.cast(a, vector_ptr),
            ctypes.cast(b, vector_ptr),
        )
        self.assertAlmostEqual(-39.35, result)

import unittest

suite = unittest.defaultTestLoader.loadTestsFromTestCase(
    MyLibraryTest
)
# suite.debug()
unittest.TextTestRunner(stream=STDOUT).run(suite)
