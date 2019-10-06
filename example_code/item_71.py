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
class Email:
    def __init__(self, sender, receiver, message):
        self.sender = sender
        self.receiver = receiver
        self.message = message


# Example 2
def get_emails():
    yield Email('foo@example.com', 'bar@example.com', 'hello1')
    yield Email('baz@example.com', 'banana@example.com', 'hello2')
    yield None
    yield Email('meep@example.com', 'butter@example.com', 'hello3')
    yield Email('stuff@example.com', 'avocado@example.com', 'hello4')
    yield None
    yield Email('thingy@example.com', 'orange@example.com', 'hello5')
    yield Email('roger@example.com', 'bob@example.com', 'hello6')
    yield None
    yield Email('peanut@example.com', 'alice@example.com', 'hello7')
    yield None

EMAIL_IT = get_emails()

class NoEmailError(Exception):
    pass

def try_receive_email():
    # Returns an Email instance or raises NoEmailError
    try:
        email = next(EMAIL_IT)
    except StopIteration:
        email = None

    if not email:
        raise NoEmailError

    print(f'Produced email: {email.message}')
    return email


# Example 3
def produce_emails(queue):
    while True:
        try:
            email = try_receive_email()
        except NoEmailError:
            return
        else:
            queue.append(email)  # Producer


# Example 4
def consume_one_email(queue):
    if not queue:
        return
    email = queue.pop(0)  # Consumer
    # Index the message for long-term archival
    print(f'Consumed email: {email.message}')


# Example 5
def loop(queue, keep_running):
    while keep_running():
        produce_emails(queue)
        consume_one_email(queue)

def make_test_end():
    count=list(range(10))

    def func():
        if count:
            count.pop()
            return True
        return False

    return func


def my_end_func():
    pass

my_end_func = make_test_end()
loop([], my_end_func)


# Example 6
import timeit

def print_results(count, tests):
    avg_iteration = sum(tests) / len(tests)
    print(f'Count {count:>5,} takes {avg_iteration:.6f}s')
    return count, avg_iteration

def list_append_benchmark(count):
    def run(queue):
        for i in range(count):
            queue.append(i)

    tests = timeit.repeat(
        setup='queue = []',
        stmt='run(queue)',
        globals=locals(),
        repeat=1000,
        number=1)

    return print_results(count, tests)


# Example 7
def print_delta(before, after):
    before_count, before_time = before
    after_count, after_time = after
    growth = 1 + (after_count - before_count) / before_count
    slowdown = 1 + (after_time - before_time) / before_time
    print(f'{growth:>4.1f}x data size, {slowdown:>4.1f}x time')

baseline = list_append_benchmark(500)
for count in (1_000, 2_000, 3_000, 4_000, 5_000):
    print()
    comparison = list_append_benchmark(count)
    print_delta(baseline, comparison)


# Example 8
def list_pop_benchmark(count):
    def prepare():
        return list(range(count))

    def run(queue):
        while queue:
            queue.pop(0)

    tests = timeit.repeat(
        setup='queue = prepare()',
        stmt='run(queue)',
        globals=locals(),
        repeat=1000,
        number=1)

    return print_results(count, tests)


# Example 9
baseline = list_pop_benchmark(500)
for count in (1_000, 2_000, 3_000, 4_000, 5_000):
    print()
    comparison = list_pop_benchmark(count)
    print_delta(baseline, comparison)


# Example 10
import collections

def consume_one_email(queue):
    if not queue:
        return
    email = queue.popleft()  # Consumer
    # Process the email message
    print(f'Consumed email: {email.message}')

def my_end_func():
    pass

my_end_func = make_test_end()
EMAIL_IT = get_emails()
loop(collections.deque(), my_end_func)


# Example 11
def deque_append_benchmark(count):
    def prepare():
        return collections.deque()

    def run(queue):
        for i in range(count):
            queue.append(i)

    tests = timeit.repeat(
        setup='queue = prepare()',
        stmt='run(queue)',
        globals=locals(),
        repeat=1000,
        number=1)
    return print_results(count, tests)

baseline = deque_append_benchmark(500)
for count in (1_000, 2_000, 3_000, 4_000, 5_000):
    print()
    comparison = deque_append_benchmark(count)
    print_delta(baseline, comparison)


# Example 12
def dequeue_popleft_benchmark(count):
    def prepare():
        return collections.deque(range(count))

    def run(queue):
        while queue:
            queue.popleft()

    tests = timeit.repeat(
        setup='queue = prepare()',
        stmt='run(queue)',
        globals=locals(),
        repeat=1000,
        number=1)

    return print_results(count, tests)

baseline = dequeue_popleft_benchmark(500)
for count in (1_000, 2_000, 3_000, 4_000, 5_000):
    print()
    comparison = dequeue_popleft_benchmark(count)
    print_delta(baseline, comparison)
