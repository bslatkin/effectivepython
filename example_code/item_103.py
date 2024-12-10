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
class Email:
    def __init__(self, sender, receiver, message):
        self.sender = sender
        self.receiver = receiver
        self.message = message


print("Example 2")
def get_emails():
    yield Email("foo@example.com", "bar@example.com", "hello1")
    yield Email("baz@example.com", "banana@example.com", "hello2")
    yield None
    yield Email("meep@example.com", "butter@example.com", "hello3")
    yield Email("stuff@example.com", "avocado@example.com", "hello4")
    yield None
    yield Email("thingy@example.com", "orange@example.com", "hello5")
    yield Email("roger@example.com", "bob@example.com", "hello6")
    yield None
    yield Email("peanut@example.com", "alice@example.com", "hello7")
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

    print(f"Produced email: {email.message}")
    return email


print("Example 3")
def produce_emails(queue):
    while True:
        try:
            email = try_receive_email()
        except NoEmailError:
            return
        else:
            queue.append(email)  # Producer


print("Example 4")
def consume_one_email(queue):
    if not queue:
        return
    email = queue.pop(0)  # Consumer
    # Index the message for long-term archival
    print(f"Consumed email: {email.message}")


print("Example 5")
def loop(queue, keep_running):
    while keep_running():
        produce_emails(queue)
        consume_one_email(queue)


def make_test_end():
    count = list(range(10))

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


print("Example 6")
import timeit

def list_append_benchmark(count):
    def run(queue):
        for i in range(count):
            queue.append(i)

    return timeit.timeit(
        setup="queue = []",
        stmt="run(queue)",
        globals=locals(),
        number=1,
    )


print("Example 7")
for i in range(1, 6):
    count = i * 1_000_000
    delay = list_append_benchmark(count)
    print(f"Count {count:>5,} takes: {delay*1e3:>6.2f}ms")


print("Example 8")
def list_pop_benchmark(count):
    def prepare():
        return list(range(count))

    def run(queue):
        while queue:
            queue.pop(0)

    return timeit.timeit(
        setup="queue = prepare()",
        stmt="run(queue)",
        globals=locals(),
        number=1,
    )


print("Example 9")
for i in range(1, 6):
    count = i * 10_000
    delay = list_pop_benchmark(count)
    print(f"Count {count:>5,} takes: {delay*1e3:>6.2f}ms")


print("Example 10")
import collections

def consume_one_email(queue):
    if not queue:
        return
    email = queue.popleft()  # Consumer
    # Process the email message
    print(f"Consumed email: {email.message}")

def my_end_func():
    pass

my_end_func = make_test_end()
EMAIL_IT = get_emails()
loop(collections.deque(), my_end_func)


print("Example 11")
def deque_append_benchmark(count):
    def prepare():
        return collections.deque()

    def run(queue):
        for i in range(count):
            queue.append(i)

    return timeit.timeit(
        setup="queue = prepare()",
        stmt="run(queue)",
        globals=locals(),
        number=1,
    )

for i in range(1, 6):
    count = i * 100_000
    delay = deque_append_benchmark(count)
    print(f"Count {count:>5,} takes: {delay*1e3:>6.2f}ms")


print("Example 12")
def dequeue_popleft_benchmark(count):
    def prepare():
        return collections.deque(range(count))

    def run(queue):
        while queue:
            queue.popleft()

    return timeit.timeit(
        setup="queue = prepare()",
        stmt="run(queue)",
        globals=locals(),
        number=1,
    )

for i in range(1, 6):
    count = i * 100_000
    delay = dequeue_popleft_benchmark(count)
    print(f"Count {count:>5,} takes: {delay*1e3:>6.2f}ms")
