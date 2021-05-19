#!/usr/bin/env PYTHONHASHSEED=1234 python3

# Copyright 2014-2019 Brett Slatkin, Pearson Education Inc.
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

# Reproduce book environment
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


# Example 1
from datetime import datetime, timedelta

class Bucket:
    def __init__(self, period):
        self.period_delta = timedelta(seconds=period)
        self.reset_time = datetime.now()
        self.quota = 0

    def __repr__(self):
        return f'Bucket(quota={self.quota})'

bucket = Bucket(60)
print(bucket)


# Example 2
def fill(bucket, amount):
    now = datetime.now()
    if (now - bucket.reset_time) > bucket.period_delta:
        bucket.quota = 0
        bucket.reset_time = now
    bucket.quota += amount


# Example 3
def deduct(bucket, amount):
    now = datetime.now()
    if (now - bucket.reset_time) > bucket.period_delta:
        return False  # Bucket hasn't been filled this period
    if bucket.quota - amount < 0:
        return False  # Bucket was filled, but not enough
    bucket.quota -= amount
    return True       # Bucket had enough, quota consumed


# Example 4
bucket = Bucket(60)
fill(bucket, 100)
print(bucket)


# Example 5
if deduct(bucket, 99):
    print('Had 99 quota')
else:
    print('Not enough for 99 quota')
print(bucket)


# Example 6
if deduct(bucket, 3):
    print('Had 3 quota')
else:
    print('Not enough for 3 quota')
print(bucket)


# Example 7
class NewBucket:
    def __init__(self, period):
        self.period_delta = timedelta(seconds=period)
        self.reset_time = datetime.now()
        self.max_quota = 0
        self.quota_consumed = 0

    def __repr__(self):
        return (f'NewBucket(max_quota={self.max_quota}, '
                f'quota_consumed={self.quota_consumed})')


# Example 8
    @property
    def quota(self):
        return self.max_quota - self.quota_consumed


# Example 9
    @quota.setter
    def quota(self, amount):
        delta = self.max_quota - amount
        if amount == 0:
            # Quota being reset for a new period
            self.quota_consumed = 0
            self.max_quota = 0
        elif delta < 0:
            # Quota being filled during the period
            self.max_quota = amount + self.quota_consumed
        else:
            # Quota being consumed during the period
            self.quota_consumed = delta


# Example 10
bucket = NewBucket(60)
print('Initial', bucket)
fill(bucket, 100)
print('Filled', bucket)

if deduct(bucket, 99):
    print('Had 99 quota')
else:
    print('Not enough for 99 quota')

print('Now', bucket)

if deduct(bucket, 3):
    print('Had 3 quota')
else:
    print('Not enough for 3 quota')

print('Still', bucket)


# Example 11
bucket = NewBucket(6000)
assert bucket.max_quota == 0
assert bucket.quota_consumed == 0
assert bucket.quota == 0

fill(bucket, 100)
assert bucket.max_quota == 100
assert bucket.quota_consumed == 0
assert bucket.quota == 100

assert deduct(bucket, 10)
assert bucket.max_quota == 100
assert bucket.quota_consumed == 10
assert bucket.quota == 90

assert deduct(bucket, 20)
assert bucket.max_quota == 100
assert bucket.quota_consumed == 30
assert bucket.quota == 70

fill(bucket, 50)
assert bucket.max_quota == 150
assert bucket.quota_consumed == 30
assert bucket.quota == 120

assert deduct(bucket, 40)
assert bucket.max_quota == 150
assert bucket.quota_consumed == 70
assert bucket.quota == 80

assert not deduct(bucket, 81)
assert bucket.max_quota == 150
assert bucket.quota_consumed == 70
assert bucket.quota == 80

bucket.reset_time += bucket.period_delta - timedelta(1)
assert bucket.quota == 80
assert not deduct(bucket, 79)

fill(bucket, 1)
assert bucket.quota == 1
