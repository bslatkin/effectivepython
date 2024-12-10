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
connection = ...

class RpcError(Exception):
    pass

def lookup_request(connection):
    raise RpcError("From lookup_request")

def close_connection(connection):
    print("Connection closed")

try:
    request = lookup_request(connection)
except RpcError:
    print("Encountered error!")
    close_connection(connection)


print("Example 2")
def lookup_request(connection):
    # No error raised
    return object()

def is_cached(connection, request):
    raise RpcError("From is_cached")

try:
    request = lookup_request(connection)
    if is_cached(connection, request):
        request = None
except RpcError:
    print("Encountered error!")
    close_connection(connection)


print("Example 3")
def is_closed(_):
    pass

if is_closed(connection):
    # Was the connection closed because of an error
    # in lookup_request or is_cached?
    pass


print("Example 4")
try:
    try:
        request = lookup_request(connection)
    except RpcError:
        close_connection(connection)
    else:
        if is_cached(connection, request):  # Moved
            request = None
except:
    logging.exception('Expected')
else:
    assert False
