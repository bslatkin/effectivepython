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
class Request:
    def __init__(self, body):
        self.body = body
        self.response = None

def do_work(data):
    assert False, data

def handle(request):
    try:
        do_work(request.body)
    except BaseException as e:
        print(repr(e))
        request.response = 400  # Bad request error


print("Example 2")
request = Request("My message")
handle(request)


print("Example 3")
import traceback

def handle2(request):
    try:
        do_work(request.body)
    except BaseException as e:
        traceback.print_tb(e.__traceback__)  # Changed
        print(repr(e))
        request.response = 400

request = Request("My message 2")
handle2(request)


print("Example 4")
def handle3(request):
    try:
        do_work(request.body)
    except BaseException as e:
        stack = traceback.extract_tb(e.__traceback__)
        for frame in stack:
            print(frame.name)
        print(repr(e))
        request.response = 400

request = Request("My message 3")
handle3(request)


print("Example 5")
import json

def log_if_error(file_path, target, *args, **kwargs):
    try:
        target(*args, **kwargs)
    except BaseException as e:
        stack = traceback.extract_tb(e.__traceback__)
        stack_without_wrapper = stack[1:]
        trace_dict = dict(
            stack=[item.name for item in stack_without_wrapper],
            error_type=type(e).__name__,
            error_message=str(e),
        )
        json_data = json.dumps(trace_dict)

        with open(file_path, "a") as f:
            f.write(json_data)
            f.write("\n")


print("Example 6")
log_if_error("my_log.jsonl", do_work, "First error")
log_if_error("my_log.jsonl", do_work, "Second error")

with open("my_log.jsonl") as f:
    for line in f:
        print(line, end="")
