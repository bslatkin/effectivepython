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
from functools import wraps

def trace_func(func):
    if hasattr(func, "tracing"):  # Only decorate once
        return func

    @wraps(func)
    def wrapper(*args, **kwargs):
        args_repr = repr(args)
        kwargs_repr = repr(kwargs)
        result = None
        try:
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            result = e
            raise
        finally:
            print(
                f"{func.__name__}"
                f"({args_repr}, {kwargs_repr}) -> "
                f"{result!r}"
            )

    wrapper.tracing = True
    return wrapper


print("Example 2")
class TraceDict(dict):
    @trace_func
    def __init__(self, *args, **kwargs):
        return super().__init__(*args, **kwargs)

    @trace_func
    def __setitem__(self, *args, **kwargs):
        return super().__setitem__(*args, **kwargs)

    @trace_func
    def __getitem__(self, *args, **kwargs):
        return super().__getitem__(*args, **kwargs)


print("Example 3")
trace_dict = TraceDict([("hi", 1)])
trace_dict["there"] = 2
trace_dict["hi"]
try:
    trace_dict["does not exist"]
except KeyError:
    pass  # Expected
else:
    assert False


print("Example 4")
import types

TRACE_TYPES = (
    types.MethodType,
    types.FunctionType,
    types.BuiltinFunctionType,
    types.BuiltinMethodType,
    types.MethodDescriptorType,
    types.ClassMethodDescriptorType,
    types.WrapperDescriptorType,
)

IGNORE_METHODS = (
    "__repr__",
    "__str__",
)

class TraceMeta(type):
    def __new__(meta, name, bases, class_dict):
        klass = super().__new__(meta, name, bases, class_dict)

        for key in dir(klass):
            if key in IGNORE_METHODS:
                continue

            value = getattr(klass, key)
            if not isinstance(value, TRACE_TYPES):
                continue

            wrapped = trace_func(value)
            setattr(klass, key, wrapped)

        return klass


print("Example 5")
class TraceDict(dict, metaclass=TraceMeta):
    pass

trace_dict = TraceDict([("hi", 1)])
trace_dict["there"] = 2
trace_dict["hi"]
try:
    trace_dict["does not exist"]
except KeyError:
    pass  # Expected
else:
    assert False


print("Example 6")
try:
    class OtherMeta(type):
        pass
    
    class SimpleDict(dict, metaclass=OtherMeta):
        pass
    
    class ChildTraceDict(SimpleDict, metaclass=TraceMeta):
        pass
except:
    logging.exception('Expected')
else:
    assert False


print("Example 7")
class TraceMeta(type):
    def __new__(meta, name, bases, class_dict):
        klass = super().__new__(meta, name, bases, class_dict)

        for key in dir(klass):
            if key in IGNORE_METHODS:
                continue

            value = getattr(klass, key)
            if not isinstance(value, TRACE_TYPES):
                continue

            wrapped = trace_func(value)
            setattr(klass, key, wrapped)

        return klass


class OtherMeta(TraceMeta):
    pass

class SimpleDict(dict, metaclass=OtherMeta):
    pass

class ChildTraceDict(SimpleDict, metaclass=TraceMeta):
    pass

trace_dict = ChildTraceDict([("hi", 1)])
trace_dict["there"] = 2
trace_dict["hi"]
try:
    trace_dict["does not exist"]
except KeyError:
    pass  # Expected
else:
    assert False


print("Example 8")
def my_class_decorator(klass):
    klass.extra_param = "hello"
    return klass

@my_class_decorator
class MyClass:
    pass

print(MyClass)
print(MyClass.extra_param)


print("Example 9")
def trace(klass):
    for key in dir(klass):
        if key in IGNORE_METHODS:
            continue

        value = getattr(klass, key)
        if not isinstance(value, TRACE_TYPES):
            continue

        wrapped = trace_func(value)
        setattr(klass, key, wrapped)

    return klass


print("Example 10")
@trace
class DecoratedTraceDict(dict):
    pass

trace_dict = DecoratedTraceDict([("hi", 1)])
trace_dict["there"] = 2
trace_dict["hi"]
try:
    trace_dict["does not exist"]
except KeyError:
    pass  # Expected
else:
    assert False


print("Example 11")
class OtherMeta(type):
    pass

@trace
class HasMetaTraceDict(dict, metaclass=OtherMeta):
    pass

trace_dict = HasMetaTraceDict([("hi", 1)])
trace_dict["there"] = 2
trace_dict["hi"]
try:
    trace_dict["does not exist"]
except KeyError:
    pass  # Expected
else:
    assert False
