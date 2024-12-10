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
class Book:
    def __init__(self, title, due_date):
        self.title = title
        self.due_date = due_date


print("Example 2")
def add_book(queue, book):
    queue.append(book)
    queue.sort(key=lambda x: x.due_date, reverse=True)

queue = []
add_book(queue, Book("Don Quixote", "2019-06-07"))
add_book(queue, Book("Frankenstein", "2019-06-05"))
add_book(queue, Book("Les Misérables", "2019-06-08"))
add_book(queue, Book("War and Peace", "2019-06-03"))


print("Example 3")
class NoOverdueBooks(Exception):
    pass

def next_overdue_book(queue, now):
    if queue:
        book = queue[-1]
        if book.due_date < now:
            queue.pop()
            return book

    raise NoOverdueBooks


print("Example 4")
now = "2019-06-10"

found = next_overdue_book(queue, now)
print(found.due_date, found.title)

found = next_overdue_book(queue, now)
print(found.due_date, found.title)


print("Example 5")
def return_book(queue, book):
    queue.remove(book)

queue = []
book = Book("Treasure Island", "2019-06-04")

add_book(queue, book)
print("Before return:", [x.title for x in queue])

return_book(queue, book)
print("After return: ", [x.title for x in queue])


print("Example 6")
try:
    next_overdue_book(queue, now)
except NoOverdueBooks:
    pass          # Expected
else:
    assert False  # Doesn't happen


print("Example 7")
import random
import timeit

def list_overdue_benchmark(count):
    def prepare():
        to_add = list(range(count))
        random.shuffle(to_add)
        return [], to_add

    def run(queue, to_add):
        for i in to_add:
            queue.append(i)
            queue.sort(reverse=True)

        while queue:
            queue.pop()

    return timeit.timeit(
        setup="queue, to_add = prepare()",
        stmt=f"run(queue, to_add)",
        globals=locals(),
        number=1,
    )


print("Example 8")
for i in range(1, 6):
    count = i * 1_000
    delay = list_overdue_benchmark(count)
    print(f"Count {count:>5,} takes: {delay*1e3:>6.2f}ms")


print("Example 9")
def list_return_benchmark(count):
    def prepare():
        queue = list(range(count))
        random.shuffle(queue)

        to_return = list(range(count))
        random.shuffle(to_return)

        return queue, to_return

    def run(queue, to_return):
        for i in to_return:
            queue.remove(i)

    return timeit.timeit(
        setup="queue, to_return = prepare()",
        stmt=f"run(queue, to_return)",
        globals=locals(),
        number=1,
    )


print("Example 10")
for i in range(1, 6):
    count = i * 1_000
    delay = list_return_benchmark(count)
    print(f"Count {count:>5,} takes: {delay*1e3:>6.2f}ms")


print("Example 11")
from heapq import heappush

def add_book(queue, book):
    heappush(queue, book)


print("Example 12")
try:
    queue = []
    add_book(queue, Book("Little Women", "2019-06-05"))
    add_book(queue, Book("The Time Machine", "2019-05-30"))
except:
    logging.exception('Expected')
else:
    assert False


print("Example 13")
import functools

@functools.total_ordering
class Book:
    def __init__(self, title, due_date):
        self.title = title
        self.due_date = due_date

    def __lt__(self, other):
        return self.due_date < other.due_date


print("Example 14")
queue = []
add_book(queue, Book("Pride and Prejudice", "2019-06-01"))
add_book(queue, Book("The Time Machine", "2019-05-30"))
add_book(queue, Book("Crime and Punishment", "2019-06-06"))
add_book(queue, Book("Wuthering Heights", "2019-06-12"))
print([b.title for b in queue])


print("Example 15")
queue = [
    Book("Pride and Prejudice", "2019-06-01"),
    Book("The Time Machine", "2019-05-30"),
    Book("Crime and Punishment", "2019-06-06"),
    Book("Wuthering Heights", "2019-06-12"),
]
queue.sort()
print([b.title for b in queue])


print("Example 16")
from heapq import heapify

queue = [
    Book("Pride and Prejudice", "2019-06-01"),
    Book("The Time Machine", "2019-05-30"),
    Book("Crime and Punishment", "2019-06-06"),
    Book("Wuthering Heights", "2019-06-12"),
]
heapify(queue)
print([b.title for b in queue])


print("Example 17")
from heapq import heappop

def next_overdue_book(queue, now):
    if queue:
        book = queue[0]     # Most overdue first
        if book.due_date < now:
            heappop(queue)  # Remove the overdue book
            return book

    raise NoOverdueBooks


print("Example 18")
now = "2019-06-02"

book = next_overdue_book(queue, now)
print(book.due_date, book.title)

book = next_overdue_book(queue, now)
print(book.due_date, book.title)

try:
    next_overdue_book(queue, now)
except NoOverdueBooks:
    pass  # Expected
else:
    assert False  # Doesn't happen


print("Example 19")
def heap_overdue_benchmark(count):
    def prepare():
        to_add = list(range(count))
        random.shuffle(to_add)
        return [], to_add

    def run(queue, to_add):
        for i in to_add:
            heappush(queue, i)
        while queue:
            heappop(queue)

    return timeit.timeit(
        setup="queue, to_add = prepare()",
        stmt=f"run(queue, to_add)",
        globals=locals(),
        number=1,
    )


print("Example 20")
for i in range(1, 6):
    count = i * 10_000
    delay = heap_overdue_benchmark(count)
    print(f"Count {count:>5,} takes: {delay*1e3:>6.2f}ms")


print("Example 21")
@functools.total_ordering
class Book:
    def __init__(self, title, due_date):
        self.title = title
        self.due_date = due_date
        self.returned = False  # New field

    def __lt__(self, other):
        return self.due_date < other.due_date


print("Example 22")
def next_overdue_book(queue, now):
    while queue:
        book = queue[0]
        if book.returned:
            heappop(queue)
            continue

        if book.due_date < now:
            heappop(queue)
            return book

        break

    raise NoOverdueBooks


queue = []

book = Book("Pride and Prejudice", "2019-06-01")
add_book(queue, book)

book = Book("The Time Machine", "2019-05-30")
add_book(queue, book)
book.returned = True

book = Book("Crime and Punishment", "2019-06-06")
add_book(queue, book)
book.returned = True

book = Book("Wuthering Heights", "2019-06-12")
add_book(queue, book)

now = "2019-06-11"

book = next_overdue_book(queue, now)
assert book.title == "Pride and Prejudice"

try:
    next_overdue_book(queue, now)
except NoOverdueBooks:
    pass  # Expected
else:
    assert False  # Doesn't happen


print("Example 23")
def return_book(queue, book):
    book.returned = True


assert not book.returned
return_book(queue, book)
assert book.returned
