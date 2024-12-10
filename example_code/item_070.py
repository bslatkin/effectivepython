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
def download(item):
    return item

def resize(item):
    return item

def upload(item):
    return item


print("Example 2")
from collections import deque
from threading import Lock

class MyQueue:
    def __init__(self):
        self.items = deque()
        self.lock = Lock()


    print("Example 3")
    def put(self, item):
        with self.lock:
            self.items.append(item)


    print("Example 4")
    def get(self):
        with self.lock:
            return self.items.popleft()


print("Example 5")
from threading import Thread
import time

class Worker(Thread):
    def __init__(self, func, in_queue, out_queue):
        super().__init__()
        self.func = func
        self.in_queue = in_queue
        self.out_queue = out_queue
        self.polled_count = 0
        self.work_done = 0


    print("Example 6")
    def run(self):
        while True:
            self.polled_count += 1
            try:
                item = self.in_queue.get()
            except IndexError:
                time.sleep(0.01)  # No work to do
            except AttributeError:
                # The magic exit signal to make this easy to show in
                # example code, but don't use this in practice.
                return
            else:
                result = self.func(item)
                self.out_queue.put(result)
                self.work_done += 1


print("Example 7")
download_queue = MyQueue()
resize_queue = MyQueue()
upload_queue = MyQueue()
done_queue = MyQueue()
threads = [
    Worker(download, download_queue, resize_queue),
    Worker(resize, resize_queue, upload_queue),
    Worker(upload, upload_queue, done_queue),
]


print("Example 8")
for thread in threads:
    thread.start()

for _ in range(1000):
    download_queue.put(object())


print("Example 9")
while len(done_queue.items) < 1000:
    # Do something useful while waiting
    time.sleep(0.1)
# Stop all the threads by causing an exception in their
# run methods.
for thread in threads:
    thread.in_queue = None
    thread.join()


print("Example 10")
processed = len(done_queue.items)
polled = sum(t.polled_count for t in threads)
print(f"Processed {processed} items after " f"polling {polled} times")


print("Example 11")
from queue import Queue

my_queue = Queue()

def consumer():
    print("Consumer waiting")
    my_queue.get()  # Runs after put() below
    print("Consumer done")

thread = Thread(target=consumer)
thread.start()


print("Example 12")
print("Producer putting")
my_queue.put(object())  # Runs before get() above
print("Producer done")
thread.join()


print("Example 13")
my_queue = Queue(1)  # Buffer size of 1

def consumer():
    time.sleep(0.1)  # Wait
    my_queue.get()   # Runs second
    print("Consumer got 1")
    my_queue.get()   # Runs fourth
    print("Consumer got 2")
    print("Consumer done")

thread = Thread(target=consumer)
thread.start()


print("Example 14")
my_queue.put(object())  # Runs first
print("Producer put 1")
my_queue.put(object())  # Runs third
print("Producer put 2")
print("Producer done")
thread.join()


print("Example 15")
in_queue = Queue()

def consumer():
    print("Consumer waiting")
    work = in_queue.get()      # Runs second
    print("Consumer working")
    # Doing work
    print("Consumer done")
    in_queue.task_done()       # Runs third

thread = Thread(target=consumer)
thread.start()


print("Example 16")
print("Producer putting")
in_queue.put(object())     # Runs first
print("Producer waiting")
in_queue.join()            # Runs fourth
print("Producer done")
thread.join()


print("Example 17")
from queue import ShutDown

my_queue2 = Queue()

def consumer():
    while True:
        try:
            item = my_queue2.get()
        except ShutDown:
            print("Terminating!")
            return
        else:
            print("Got item", item)
            my_queue2.task_done()

thread = Thread(target=consumer)
my_queue2.put(1)
my_queue2.put(2)
my_queue2.put(3)
my_queue2.shutdown()

thread.start()

my_queue2.join()
thread.join()
print("Done")


print("Example 18")
class StoppableWorker(Thread):
    def __init__(self, func, in_queue, out_queue):
        super().__init__()
        self.func = func
        self.in_queue = in_queue
        self.out_queue = out_queue

    def run(self):
        while True:
            try:
                item = self.in_queue.get()
            except ShutDown:
                return
            else:
                result = self.func(item)
                self.out_queue.put(result)
                self.in_queue.task_done()


print("Example 19")
download_queue = Queue()
resize_queue = Queue(100)
upload_queue = Queue(100)
done_queue = Queue()

threads = [
    StoppableWorker(download, download_queue, resize_queue),
    StoppableWorker(resize, resize_queue, upload_queue),
    StoppableWorker(upload, upload_queue, done_queue),
]

for thread in threads:
    thread.start()


print("Example 20")
for _ in range(1000):
    download_queue.put(object())


print("Example 21")
download_queue.shutdown()
download_queue.join()

resize_queue.shutdown()
resize_queue.join()

upload_queue.shutdown()
upload_queue.join()


print("Example 22")
done_queue.shutdown()

counter = 0

while True:
    try:
        item = done_queue.get()
    except ShutDown:
        break
    else:
        # Process the item
        done_queue.task_done()
        counter += 1

done_queue.join()

for thread in threads:
    thread.join()

print(counter, "items finished")


print("Example 23")
def start_threads(count, *args):
    threads = [StoppableWorker(*args) for _ in range(count)]
    for thread in threads:
        thread.start()
    return threads

def drain_queue(input_queue):
    input_queue.shutdown()

    counter = 0

    while True:
        try:
            item = input_queue.get()
        except ShutDown:
            break
        else:
            input_queue.task_done()
            counter += 1

    input_queue.join()

    return counter


print("Example 24")
download_queue = Queue()
resize_queue = Queue(100)
upload_queue = Queue(100)
done_queue = Queue()

threads = (
    start_threads(3, download, download_queue, resize_queue)
    + start_threads(4, resize, resize_queue, upload_queue)
    + start_threads(5, upload, upload_queue, done_queue)
)


print("Example 25")
for _ in range(2000):
    download_queue.put(object())

download_queue.shutdown()
download_queue.join()

resize_queue.shutdown()
resize_queue.join()

upload_queue.shutdown()
upload_queue.join()

counter = drain_queue(done_queue)

for thread in threads:
    thread.join()

print(counter, "items finished")
