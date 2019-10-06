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
def timecode_to_index(video_id, timecode):
    return 1234
    # Returns the byte offset in the video data

def request_chunk(video_id, byte_offset, size):
    pass
    # Returns size bytes of video_id's data from the offset

video_id = ...
timecode = '01:09:14:28'
byte_offset = timecode_to_index(video_id, timecode)
size = 20 * 1024 * 1024
video_data = request_chunk(video_id, byte_offset, size)


# Example 2
class NullSocket:
    def __init__(self):
        self.handle = open(os.devnull, 'wb')

    def send(self, data):
        self.handle.write(data)

socket = ...             # socket connection to client
video_data = ...         # bytes containing data for video_id
byte_offset = ...        # Requested starting position
size = 20 * 1024 * 1024  # Requested chunk size
import os

socket = NullSocket()
video_data = 100 * os.urandom(1024 * 1024)
byte_offset = 1234

chunk = video_data[byte_offset:byte_offset + size]
socket.send(chunk)


# Example 3
import timeit

def run_test():
    chunk = video_data[byte_offset:byte_offset + size]
    # Call socket.send(chunk), but ignoring for benchmark

result = timeit.timeit(
    stmt='run_test()',
    globals=globals(),
    number=100) / 100

print(f'{result:0.9f} seconds')


# Example 4
data = b'shave and a haircut, two bits'
view = memoryview(data)
chunk = view[12:19]
print(chunk)
print('Size:           ', chunk.nbytes)
print('Data in view:   ', chunk.tobytes())
print('Underlying data:', chunk.obj)


# Example 5
video_view = memoryview(video_data)

def run_test():
    chunk = video_view[byte_offset:byte_offset + size]
    # Call socket.send(chunk), but ignoring for benchmark

result = timeit.timeit(
    stmt='run_test()',
    globals=globals(),
    number=100) / 100

print(f'{result:0.9f} seconds')


# Example 6
class FakeSocket:

    def recv(self, size):
        return video_view[byte_offset:byte_offset+size]

    def recv_into(self, buffer):
        source_data = video_view[byte_offset:byte_offset+size]
        buffer[:] = source_data

socket = ...        # socket connection to the client
video_cache = ...   # Cache of incoming video stream
byte_offset = ...   # Incoming buffer position
size = 1024 * 1024  # Incoming chunk size
socket = FakeSocket()
video_cache = video_data[:]
byte_offset = 1234

chunk = socket.recv(size)
video_view = memoryview(video_cache)
before = video_view[:byte_offset]
after = video_view[byte_offset + size:]
new_cache = b''.join([before, chunk, after])


# Example 7
def run_test():
    chunk = socket.recv(size)
    before = video_view[:byte_offset]
    after = video_view[byte_offset + size:]
    new_cache = b''.join([before, chunk, after])

result = timeit.timeit(
    stmt='run_test()',
    globals=globals(),
    number=100) / 100

print(f'{result:0.9f} seconds')


# Example 8
try:
    my_bytes = b'hello'
    my_bytes[0] = b'\x79'
except:
    logging.exception('Expected')
else:
    assert False


# Example 9
my_array = bytearray(b'hello')
my_array[0] = 0x79
print(my_array)


# Example 10
my_array = bytearray(b'row, row, row your boat')
my_view = memoryview(my_array)
write_view = my_view[3:13]
write_view[:] = b'-10 bytes-'
print(my_array)


# Example 11
video_array = bytearray(video_cache)
write_view = memoryview(video_array)
chunk = write_view[byte_offset:byte_offset + size]
socket.recv_into(chunk)


# Example 12
def run_test():
    chunk = write_view[byte_offset:byte_offset + size]
    socket.recv_into(chunk)

result = timeit.timeit(
    stmt='run_test()',
    globals=globals(),
    number=100) / 100

print(f'{result:0.9f} seconds')
