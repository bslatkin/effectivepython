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
def load_data(path):
    open(path).read()

def analyze_data(data):
    return "my summary"

def run_report(path):
    data = load_data(path)
    summary = analyze(data)
    return summary


print("Example 2")
try:
    summary = run_report("pizza_data-2024-01-28.csv")
    print(summary)
except:
    logging.exception('Expected')
else:
    assert False


print("Example 3")
try:
    summary = run_report("pizza_data.csv")
except FileNotFoundError:
    print("Transient file error")
else:
    print(summary)


print("Example 4")
try:
    summary = run_report("pizza_data.csv")
except Exception:  # Changed
    print("Transient report issue")
else:
    print(summary)


print("Example 5")
try:
    def load_data(path):
        pass
    
    run_report("my_data.csv")
except:
    logging.exception('Expected')
else:
    assert False


print("Example 6")
try:
    summary = run_report("my_data.csv")
except Exception as e:
    print("Fail:", type(e), e)
else:
    print(summary)
