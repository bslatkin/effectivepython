#!/usr/bin/env python3

# Copyright 2014 Brett Slatkin, Pearson Education Inc.
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

# Preamble to mimick book environment
import logging
from pprint import pprint
from sys import stdout as STDOUT


# Example 1
class GameState(object):
    def __init__(self):
        self.level = 0
        self.lives = 4


# Example 2
state = GameState()
state.level += 1  # Player beat a level
state.lives -= 1  # Player had to try again


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
class GameState(object):
    def __init__(self):
        self.level = 0
        self.lives = 4
        self.points = 0


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
class GameState(object):
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
class GameState(object):
    def __init__(self, level=0, lives=4, points=0, magic=5):
        self.level = level
        self.lives = lives
        self.points = points
        self.magic = magic


# Example 15
state_after = pickle.loads(serialized)
print(state_after.__dict__)


# Example 16
class GameState(object):
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
        kwargs.pop('lives')
    return GameState(**kwargs)


# Example 20
copyreg.pickle(GameState, pickle_game_state)
state_after = pickle.loads(serialized)
print(state_after.__dict__)


# Example 21
copyreg.dispatch_table.clear()
state = GameState()
serialized = pickle.dumps(state)
del GameState
class BetterGameState(object):
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
print(serialized[:25])


# Example 24
copyreg.pickle(BetterGameState, pickle_game_state)


# Example 25
state = BetterGameState()
serialized = pickle.dumps(state)
print(serialized[:35])
