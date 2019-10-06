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
import subprocess
# Enable these lines to make this example work on Windows
# import os
# os.environ['COMSPEC'] = 'powershell'

result = subprocess.run(
    ['echo', 'Hello from the child!'],
    capture_output=True,
    # Enable this line to make this example work on Windows
    # shell=True,
    encoding='utf-8')

result.check_returncode()  # No exception means it exited cleanly
print(result.stdout)


# Example 2
# Use this line instead to make this example work on Windows
# proc = subprocess.Popen(['sleep', '1'], shell=True)
proc = subprocess.Popen(['sleep', '1'])
while proc.poll() is None:
    print('Working...')
    # Some time-consuming work here
    import time
    time.sleep(0.3)

print('Exit status', proc.poll())


# Example 3
import time

start = time.time()
sleep_procs = []
for _ in range(10):
    # Use this line instead to make this example work on Windows
    # proc = subprocess.Popen(['sleep', '1'], shell=True)
    proc = subprocess.Popen(['sleep', '1'])
    sleep_procs.append(proc)


# Example 4
for proc in sleep_procs:
    proc.communicate()

end = time.time()
delta = end - start
print(f'Finished in {delta:.3} seconds')


# Example 5
import os
# On Windows, after installing OpenSSL, you may need to
# alias it in your PowerShell path with a command like:
# $env:path = $env:path + ";C:\Program Files\OpenSSL-Win64\bin"

def run_encrypt(data):
    env = os.environ.copy()
    env['password'] = 'zf7ShyBhZOraQDdE/FiZpm/m/8f9X+M1'
    proc = subprocess.Popen(
        ['openssl', 'enc', '-des3', '-pass', 'env:password'],
        env=env,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE)
    proc.stdin.write(data)
    proc.stdin.flush()  # Ensure that the child gets input
    return proc


# Example 6
procs = []
for _ in range(3):
    data = os.urandom(10)
    proc = run_encrypt(data)
    procs.append(proc)


# Example 7
for proc in procs:
    out, _ = proc.communicate()
    print(out[-10:])


# Example 8
def run_hash(input_stdin):
    return subprocess.Popen(
        ['openssl', 'dgst', '-whirlpool', '-binary'],
        stdin=input_stdin,
        stdout=subprocess.PIPE)


# Example 9
encrypt_procs = []
hash_procs = []
for _ in range(3):
    data = os.urandom(100)

    encrypt_proc = run_encrypt(data)
    encrypt_procs.append(encrypt_proc)

    hash_proc = run_hash(encrypt_proc.stdout)
    hash_procs.append(hash_proc)

    # Ensure that the child consumes the input stream and
    # the communicate() method doesn't inadvertently steal
    # input from the child. Also lets SIGPIPE propagate to
    # the upstream process if the downstream process dies.
    encrypt_proc.stdout.close()
    encrypt_proc.stdout = None


# Example 10
for proc in encrypt_procs:
    proc.communicate()
    assert proc.returncode == 0

for proc in hash_procs:
    out, _ = proc.communicate()
    print(out[-10:])
    assert proc.returncode == 0


# Example 11
# Use this line instead to make this example work on Windows
# proc = subprocess.Popen(['sleep', '10'], shell=True)
proc = subprocess.Popen(['sleep', '10'])
try:
    proc.communicate(timeout=0.1)
except subprocess.TimeoutExpired:
    proc.terminate()
    proc.wait()

print('Exit status', proc.poll())
