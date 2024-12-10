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
import csv


with open("packages.csv", "w") as f:
    f.write(
        """\
Sydney,truck,25
Melbourne,boat,6
Brisbane,plane,12
Perth,road train,90
Adelaide,truck,17
"""
    )


with open("packages.csv") as f:
    for row in csv.reader(f):
        print(row)
print("...")


print("Example 2")
class Delivery:
    def __init__(self, destination, method, weight):
        self.destination = destination
        self.method = method
        self.weight = weight

    @classmethod
    def from_row(cls, row):
        return cls(row[0], row[1], row[2])


print("Example 3")
row1 = ["Sydney", "truck", "25"]
obj1 = Delivery.from_row(row1)
print(obj1.__dict__)


print("Example 4")
class RowMapper:
    fields = ()  # Must be in CSV column order

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if key not in type(self).fields:
                raise TypeError(f"Invalid field: {key}")
            setattr(self, key, value)

    @classmethod
    def from_row(cls, row):
        if len(row) != len(cls.fields):
            raise ValueError("Wrong number of fields")
        kwargs = dict(pair for pair in zip(cls.fields, row))
        return cls(**kwargs)


print("Example 5")
class DeliveryMapper(RowMapper):
    fields = ("destination", "method", "weight")


try:
    DeliveryMapper.from_row([1, 2, 3, 4])
except ValueError as e:
    assert str(e) == "Wrong number of fields"

try:
    DeliveryMapper(bad=1)
except TypeError as e:
    assert str(e) == "Invalid field: bad"


obj2 = DeliveryMapper.from_row(row1)
assert obj2.destination == "Sydney"
assert obj2.method == "truck"
assert obj2.weight == "25"


print("Example 6")
class MovingMapper(RowMapper):
    fields = ("source", "destination", "square_feet")


print("Example 7")
class BetterMovingMapper:
    source = ...
    destination = ...
    square_feet = ...


print("Example 8")
class BetterRowMapper(RowMapper):
    def __init_subclass__(cls):
        fields = []
        for key, value in cls.__dict__.items():
            if value is Ellipsis:
                fields.append(key)
        cls.fields = tuple(fields)


print("Example 9")
class BetterDeliveryMapper(BetterRowMapper):
    destination = ...
    method = ...
    weight = ...


try:
    DeliveryMapper.from_row([1, 2, 3, 4])
except ValueError as e:
    assert str(e) == "Wrong number of fields"

try:
    BetterDeliveryMapper(bad=1)
except TypeError as e:
    assert str(e) == "Invalid field: bad"


obj3 = BetterDeliveryMapper.from_row(row1)
assert obj3.destination == "Sydney"
assert obj3.method == "truck"
assert obj3.weight == "25"


print("Example 10")
class ReorderedDeliveryMapper(BetterRowMapper):
    method = ...
    weight = ...
    destination = ...  # Moved

row4 = ["road train", "90", "Perth"]  # Different order
obj4 = ReorderedDeliveryMapper.from_row(row4)
print(obj4.__dict__)


print("Example 11")
class Field:
    def __init__(self):
        self.internal_name = None

    def __set_name__(self, owner, column_name):
        self.internal_name = "_" + column_name

    def __get__(self, instance, instance_type):
        if instance is None:
            return self
        return getattr(instance, self.internal_name, "")

    def __set__(self, instance, value):
        adjusted_value = self.convert(value)
        setattr(instance, self.internal_name, adjusted_value)

    def convert(self, value):
        raise NotImplementedError


print("Example 12")
class StringField(Field):
    def convert(self, value):
        if not isinstance(value, str):
            raise ValueError
        return value

class FloatField(Field):
    def convert(self, value):
        return float(value)


print("Example 13")
class DescriptorRowMapper(RowMapper):
    def __init_subclass__(cls):
        fields = []
        for key, value in cls.__dict__.items():
            if isinstance(value, Field):  # Changed
                fields.append(key)
        cls.fields = tuple(fields)

try:
    DescriptorRowMapper.from_row([1, 2, 3, 4])
except ValueError as e:
    assert str(e) == "Wrong number of fields"

try:
    DescriptorRowMapper(bad=1)
except TypeError as e:
    assert str(e) == "Invalid field: bad"


print("Example 14")
class ConvertingDeliveryMapper(DescriptorRowMapper):
    destination = StringField()
    method = StringField()
    weight = FloatField()

obj5 = ConvertingDeliveryMapper.from_row(row1)
assert obj5.destination == "Sydney"
assert obj5.method == "truck"
assert obj5.weight == 25.0  # Number, not string


print("Example 15")
class HypotheticalWorkflow:
    def start_engine(self):
        pass

    def release_brake(self):
        pass

    def run(self):
        # Runs `start_engine` then `release_brake`
        pass


print("Example 16")
def step(func):
    func._is_step = True
    return func


print("Example 17")
class Workflow:
    def __init_subclass__(cls):
        steps = []
        for key, value in cls.__dict__.items():
            if callable(value) and hasattr(value, "_is_step"):
                steps.append(key)
        cls.steps = tuple(steps)


print("Example 18")
    def run(self):
        for step_name in type(self).steps:
            func = getattr(self, step_name)
            func()


print("Example 19")
class MyWorkflow(Workflow):
    @step
    def start_engine(self):
        print("Engine is on!")

    def my_helper_function(self):
        raise RuntimeError("Should not be called")

    @step
    def release_brake(self):
        print("Brake is off!")


print("Example 20")
workflow = MyWorkflow()
workflow.run()
print("...")
