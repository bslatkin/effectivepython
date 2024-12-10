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
    my_dict = {}
    my_dict["does_not_exist"]
except:
    logging.exception('Expected')
else:
    assert False


print("Example 2")
my_dict = {}
try:
    my_dict["does_not_exist"]
except KeyError:
    print("Could not find key!")


print("Example 3")
try:
    class MissingError(Exception):
        pass
    
    try:
        my_dict["does_not_exist"]    # Raises first exception
    except KeyError:
        raise MissingError("Oops!")  # Raises second exception
except:
    logging.exception('Expected')
else:
    assert False


print("Example 4")
try:
    try:
        my_dict["does_not_exist"]
    except KeyError:
        raise MissingError("Oops!")
except MissingError as e:
    print("Second:", repr(e))
    print("First: ", repr(e.__context__))


print("Example 5")
def lookup(my_key):
    try:
        return my_dict[my_key]
    except KeyError:
        raise MissingError


print("Example 6")
my_dict["my key 1"] = 123
print(lookup("my key 1"))


print("Example 7")
try:
    print(lookup("my key 2"))
except:
    logging.exception('Expected')
else:
    assert False


print("Example 8")
def contact_server(my_key):
    print(f"Looking up {my_key!r} in server")
    return "my value 2"

def lookup(my_key):
    try:
        return my_dict[my_key]
    except KeyError:
        result = contact_server(my_key)
        my_dict[my_key] = result  # Fill the local cache
        return result


print("Example 9")
print("Call 1")
print("Result:", lookup("my key 2"))
print("Call 2")
print("Result:", lookup("my key 2"))


print("Example 10")
class ServerMissingKeyError(Exception):
    pass

def contact_server(my_key):
    print(f"Looking up {my_key!r} in server")
    raise ServerMissingKeyError


print("Example 11")
try:
    print(lookup("my key 3"))
except:
    logging.exception('Expected')
else:
    assert False


print("Example 12")
def lookup(my_key):
    try:
        return my_dict[my_key]
    except KeyError:
        try:
            result = contact_server(my_key)
        except ServerMissingKeyError:
            raise MissingError        # Convert the server error
        else:
            my_dict[my_key] = result  # Fill the local cache
            return result


print("Example 13")
try:
    print(lookup("my key 4"))
except:
    logging.exception('Expected')
else:
    assert False


print("Example 14")
def lookup_explicit(my_key):
    try:
        return my_dict[my_key]
    except KeyError as e:              # Changed
        try:
            result = contact_server(my_key)
        except ServerMissingKeyError:
            raise MissingError from e  # Changed
        else:
            my_dict[my_key] = result
            return result


print("Example 15")
try:
    print(lookup_explicit("my key 5"))
except:
    logging.exception('Expected')
else:
    assert False


print("Example 16")
try:
    lookup_explicit("my key 6")
except Exception as e:
    print("Exception:", repr(e))
    print("Context:  ", repr(e.__context__))
    print("Cause:    ", repr(e.__cause__))
    print("Suppress: ", repr(e.__suppress_context__))


print("Example 17")
import traceback

try:
    lookup("my key 7")
except Exception as e:
    stack = traceback.extract_tb(e.__traceback__)
    for frame in stack:
        print(frame.line)


print("Example 18")
def get_cause(exc):
    if exc.__cause__ is not None:
        return exc.__cause__
    elif not exc.__suppress_context__:
        return exc.__context__
    else:
        return None


print("Example 19")
try:
    lookup("my key 8")
except Exception as e:
    while e is not None:
        stack = traceback.extract_tb(e.__traceback__)
        for i, frame in enumerate(stack, 1):
            print(i, frame.line)
        e = get_cause(e)
        if e:
            print("Caused by")


print("Example 20")
def contact_server(key):
    raise ServerMissingKeyError from None  # Suppress


print("Example 21")
try:
    print(lookup("my key 9"))
except:
    logging.exception('Expected')
else:
    assert False
