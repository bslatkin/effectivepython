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
class Integer:
    def __init__(self, value):
        self.value = value

class Add:
    def __init__(self, left, right):
        self.left = left
        self.right = right

class Multiply:
    def __init__(self, left, right):
        self.left = left
        self.right = right


print("Example 2")
tree = Add(
    Integer(2),
    Integer(9),
)


print("Example 3")
def evaluate(node):
    if isinstance(node, Integer):
        return node.value
    elif isinstance(node, Add):
        return evaluate(node.left) + evaluate(node.right)
    elif isinstance(node, Multiply):
        return evaluate(node.left) * evaluate(node.right)
    else:
        raise NotImplementedError


print("Example 4")
print(evaluate(tree))


print("Example 5")
tree = Multiply(
    Add(Integer(3), Integer(5)),
    Add(Integer(4), Integer(7)),
)
print(evaluate(tree))


print("Example 6")
class Node:
    def evaluate(self):
        raise NotImplementedError


print("Example 7")
class IntegerNode(Node):
    def __init__(self, value):
        self.value = value

    def evaluate(self):
        return self.value


print("Example 8")
class AddNode(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def evaluate(self):
        left = self.left.evaluate()
        right = self.right.evaluate()
        return left + right

class MultiplyNode(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def evaluate(self):
        left = self.left.evaluate()
        right = self.right.evaluate()
        return left * right


print("Example 9")
tree = MultiplyNode(
    AddNode(IntegerNode(3), IntegerNode(5)),
    AddNode(IntegerNode(4), IntegerNode(7)),
)
print(tree.evaluate())


print("Example 10")
class NodeAlt:
    def evaluate(self):
        raise NotImplementedError

    def pretty(self):
        raise NotImplementedError


print("Example 11")
class IntegerNodeAlt(NodeAlt):
    def __init__(self, value):
        self.value = value

    def evaluate(self):
        return self.value


    def pretty(self):
        return repr(self.value)


print("Example 12")
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


print("Example 13")
tree = MultiplyNodeAlt(
    AddNodeAlt(IntegerNodeAlt(3), IntegerNodeAlt(5)),
    AddNodeAlt(IntegerNodeAlt(4), IntegerNodeAlt(7)),
)
print(tree.pretty())
