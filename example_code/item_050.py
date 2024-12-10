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
class NodeAlt:
    def evaluate(self):
        raise NotImplementedError

    def pretty(self):
        raise NotImplementedError

class IntegerNodeAlt(NodeAlt):
    def __init__(self, value):
        self.value = value

    def evaluate(self):
        return self.value

    def pretty(self):
        return repr(self.value)

class AddNodeAlt(NodeAlt):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def evaluate(self):
        left = self.left.evaluate()
        right = self.right.evaluate()
        return left + right

    def pretty(self):
        left_str = self.left.pretty()
        right_str = self.right.pretty()
        return f"({left_str} + {right_str})"


class MultiplyNodeAlt(NodeAlt):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def evaluate(self):
        left = self.left.evaluate()
        right = self.right.evaluate()
        return left + right

    def pretty(self):
        left_str = self.left.pretty()
        right_str = self.right.pretty()
        return f"({left_str} * {right_str})"


print("Example 2")
tree = MultiplyNodeAlt(
    AddNodeAlt(IntegerNodeAlt(3), IntegerNodeAlt(5)),
    AddNodeAlt(IntegerNodeAlt(4), IntegerNodeAlt(7)),
)
print(tree.evaluate())
print(tree.pretty())


print("Example 3")
class NodeAlt2:
    def evaluate(self):
        raise NotImplementedError

    def pretty(self):
        raise NotImplementedError

    def solve(self):
        raise NotImplementedError

    def error_check(self):
        raise NotImplementedError

    def derivative(self):
        raise NotImplementedError

    # And 20 more methods...


print("Example 4")
import functools

@functools.singledispatch
def my_print(value):
    raise NotImplementedError


print("Example 5")
@my_print.register(int)
def _(value):
    print("Integer!", value)

@my_print.register(float)
def _(value):
    print("Float!", value)


print("Example 6")
my_print(20)
my_print(1.23)


print("Example 7")
@functools.singledispatch
def my_evaluate(node):
    raise NotImplementedError


print("Example 8")
class Integer:
    def __init__(self, value):
        self.value = value

@my_evaluate.register(Integer)
def _(node):
    return node.value


print("Example 9")
class Add:
    def __init__(self, left, right):
        self.left = left
        self.right = right

@my_evaluate.register(Add)
def _(node):
    left = my_evaluate(node.left)
    right = my_evaluate(node.right)
    return left + right

class Multiply:
    def __init__(self, left, right):
        self.left = left
        self.right = right

@my_evaluate.register(Multiply)
def _(node):
    left = my_evaluate(node.left)
    right = my_evaluate(node.right)
    return left * right


print("Example 10")
tree = Multiply(
    Add(Integer(3), Integer(5)),
    Add(Integer(4), Integer(7)),
)
result = my_evaluate(tree)
print(result)


print("Example 11")
@functools.singledispatch
def my_pretty(node):
    raise NotImplementedError

@my_pretty.register(Integer)
def _(node):
    return repr(node.value)

@my_pretty.register(Add)
def _(node):
    left_str = my_pretty(node.left)
    right_str = my_pretty(node.right)
    return f"({left_str} + {right_str})"

@my_pretty.register(Multiply)
def _(node):
    left_str = my_pretty(node.left)
    right_str = my_pretty(node.right)
    return f"({left_str} * {right_str})"


print("Example 12")
print(my_pretty(tree))


print("Example 13")
class PositiveInteger(Integer):
    pass

print(my_pretty(PositiveInteger(1234)))


print("Example 14")
try:
    class Float:
        def __init__(self, value):
            self.value = value
    
    
    print(my_pretty(Float(5.678)))
except:
    logging.exception('Expected')
else:
    assert False
