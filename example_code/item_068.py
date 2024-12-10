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
def factorize(number):
    for i in range(1, number + 1):
        if number % i == 0:
            yield i


print("Example 2")
import time

numbers = [7775876, 6694411, 5038540, 5426782,
           9934740, 9168996, 5271226, 8288002,
           9403196, 6678888, 6776096, 9582542,
           7107467, 9633726, 5747908, 7613918]
start = time.perf_counter()

for number in numbers:
    list(factorize(number))

end = time.perf_counter()
delta = end - start
print(f"Took {delta:.3f} seconds")


print("Example 3")
from threading import Thread

class FactorizeThread(Thread):
    def __init__(self, number):
        super().__init__()
        self.number = number

    def run(self):
        self.factors = list(factorize(self.number))


print("Example 4")
start = time.perf_counter()

threads = []
for number in numbers:
    thread = FactorizeThread(number)
    thread.start()
    threads.append(thread)


print("Example 5")
for thread in threads:
    thread.join()

end = time.perf_counter()
delta = end - start
print(f"Took {delta:.3f} seconds")


print("Example 6")
import select
import socket

def slow_systemcall():
    select.select([socket.socket()], [], [], 0.1)


print("Example 7")
start = time.perf_counter()

for _ in range(5):
    slow_systemcall()

end = time.perf_counter()
delta = end - start
print(f"Took {delta:.3f} seconds")


print("Example 8")
start = time.perf_counter()

threads = []
for _ in range(5):
    thread = Thread(target=slow_systemcall)
    thread.start()
    threads.append(thread)


print("Example 9")
def compute_helicopter_location(index):
    pass

for i in range(5):
    compute_helicopter_location(i)

for thread in threads:
    thread.join()

end = time.perf_counter()
delta = end - start
print(f"Took {delta:.3f} seconds")
