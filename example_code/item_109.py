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
class Toaster:
    def __init__(self, timer):
        self.timer = timer
        self.doneness = 3
        self.hot = False

    def _get_duration(self):
        return max(0.1, min(120, self.doneness * 10))

    def push_down(self):
        if self.hot:
            return

        self.hot = True
        self.timer.countdown(self._get_duration(), self.pop_up)

    def pop_up(self):
        print("Pop!")  # Release the spring
        self.hot = False
        self.timer.end()


print("Example 2")
import threading

class ReusableTimer:
    def __init__(self):
        self.timer = None

    def countdown(self, duration, callback):
        self.end()
        self.timer = threading.Timer(duration, callback)
        self.timer.start()

    def end(self):
        if self.timer:
            self.timer.cancel()


print("Example 3")
toaster = Toaster(ReusableTimer())
print("Initially hot:  ", toaster.hot)
toaster.doneness = 5
toaster.doneness = 0
toaster.push_down()
print("After push down:", toaster.hot)

# Time passes
toaster.timer.timer.join()
print("After time:     ", toaster.hot)


print("Example 4")
from unittest import TestCase
from unittest.mock import Mock

class ToasterUnitTest(TestCase):

    def test_start(self):
        timer = Mock(spec=ReusableTimer)
        toaster = Toaster(timer)
        toaster.push_down()
        self.assertTrue(toaster.hot)
        timer.countdown.assert_called_once_with(30, toaster.pop_up)

    def test_end(self):
        timer = Mock(spec=ReusableTimer)
        toaster = Toaster(timer)
        toaster.hot = True
        toaster.pop_up()
        self.assertFalse(toaster.hot)
        timer.end.assert_called_once()

import unittest

suite = unittest.defaultTestLoader.loadTestsFromTestCase(
    ToasterUnitTest
)
# suite.debug()
unittest.TextTestRunner(stream=STDOUT).run(suite)


print("Example 5")
from unittest import mock

class ReusableTimerUnitTest(TestCase):

    def test_countdown(self):
        my_func = lambda: None
        with mock.patch("threading.Timer"):
            timer = ReusableTimer()
            timer.countdown(0.1, my_func)
            threading.Timer.assert_called_once_with(0.1, my_func)
            timer.timer.start.assert_called_once()

    def test_end(self):
        my_func = lambda: None
        with mock.patch("threading.Timer"):
            timer = ReusableTimer()
            timer.countdown(0.1, my_func)
            timer.end()
            timer.timer.cancel.assert_called_once()

import unittest

suite = unittest.defaultTestLoader.loadTestsFromTestCase(
    ReusableTimerUnitTest
)
# suite.debug()
unittest.TextTestRunner(stream=STDOUT).run(suite)


print("Example 6")
class ToasterIntegrationTest(TestCase):

    def setUp(self):
        self.timer = ReusableTimer()
        self.toaster = Toaster(self.timer)
        self.toaster.doneness = 0

    def test_wait_finish(self):
        self.assertFalse(self.toaster.hot)
        self.toaster.push_down()
        self.assertTrue(self.toaster.hot)
        self.timer.timer.join()
        self.assertFalse(self.toaster.hot)

    def test_cancel_early(self):
        self.assertFalse(self.toaster.hot)
        self.toaster.push_down()
        self.assertTrue(self.toaster.hot)
        self.toaster.pop_up()
        self.assertFalse(self.toaster.hot)

import unittest

suite = unittest.defaultTestLoader.loadTestsFromTestCase(
    ToasterIntegrationTest
)
# suite.debug()
unittest.TextTestRunner(stream=STDOUT).run(suite)


print("Example 7")
class DonenessUnitTest(TestCase):
    def setUp(self):
        self.toaster = Toaster(ReusableTimer())

    def test_min(self):
        self.toaster.doneness = 0
        self.assertEqual(0.1, self.toaster._get_duration())

    def test_max(self):
        self.toaster.doneness = 1000
        self.assertEqual(120, self.toaster._get_duration())

import unittest

suite = unittest.defaultTestLoader.loadTestsFromTestCase(
    DonenessUnitTest
)
# suite.debug()
unittest.TextTestRunner(stream=STDOUT).run(suite)
