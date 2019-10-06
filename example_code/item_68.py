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
class GameState:
    def __init__(self):
        self.level = 0
        self.lives = 4


# Example 2
state = GameState()
state.level += 1  # Player beat a level
state.lives -= 1  # Player had to try again

print(state.__dict__)


# Example 3
import pickle

state_path = 'game_state.bin'
with open(state_path, 'wb') as f:
    pickle.dump(state, f)


# Example 4
with open(state_path, 'rb') as f:
    state_after = pickle.load(f)

print(state_after.__dict__)


# Example 5
class GameState:
    def __init__(self):
        self.level = 0
        self.lives = 4
        self.points = 0  # New field


# Example 6
state = GameState()
serialized = pickle.dumps(state)
state_after = pickle.loads(serialized)
print(state_after.__dict__)


# Example 7
with open(state_path, 'rb') as f:
    state_after = pickle.load(f)

print(state_after.__dict__)


# Example 8
assert isinstance(state_after, GameState)


# Example 9
class GameState:
    def __init__(self, level=0, lives=4, points=0):
        self.level = level
        self.lives = lives
        self.points = points


# Example 10
def pickle_game_state(game_state):
    kwargs = game_state.__dict__
    return unpickle_game_state, (kwargs,)


# Example 11
def unpickle_game_state(kwargs):
    return GameState(**kwargs)


# Example 12
import copyreg

copyreg.pickle(GameState, pickle_game_state)


# Example 13
state = GameState()
state.points += 1000
serialized = pickle.dumps(state)
state_after = pickle.loads(serialized)
print(state_after.__dict__)


# Example 14
class GameState:
    def __init__(self, level=0, lives=4, points=0, magic=5):
        self.level = level
        self.lives = lives
        self.points = points
        self.magic = magic  # New field


# Example 15
print('Before:', state.__dict__)
state_after = pickle.loads(serialized)
print('After: ', state_after.__dict__)


# Example 16
class GameState:
    def __init__(self, level=0, points=0, magic=5):
        self.level = level
        self.points = points
        self.magic = magic


# Example 17
try:
    pickle.loads(serialized)
except:
    logging.exception('Expected')
else:
    assert False


# Example 18
def pickle_game_state(game_state):
    kwargs = game_state.__dict__
    kwargs['version'] = 2
    return unpickle_game_state, (kwargs,)


# Example 19
def unpickle_game_state(kwargs):
    version = kwargs.pop('version', 1)
    if version == 1:
        del kwargs['lives']
    return GameState(**kwargs)


# Example 20
copyreg.pickle(GameState, pickle_game_state)
print('Before:', state.__dict__)
state_after = pickle.loads(serialized)
print('After: ', state_after.__dict__)


# Example 21
copyreg.dispatch_table.clear()
state = GameState()
serialized = pickle.dumps(state)
del GameState
class BetterGameState:
    def __init__(self, level=0, points=0, magic=5):
        self.level = level
        self.points = points
        self.magic = magic


# Example 22
try:
    pickle.loads(serialized)
except:
    logging.exception('Expected')
else:
    assert False


# Example 23
print(serialized)


# Example 24
copyreg.pickle(BetterGameState, pickle_game_state)


# Example 25
state = BetterGameState()
serialized = pickle.dumps(state)
print(serialized)
