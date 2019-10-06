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
ALIVE = '*'
EMPTY = '-'


# Example 2
class Grid:
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.rows = []
        for _ in range(self.height):
            self.rows.append([EMPTY] * self.width)

    def get(self, y, x):
        return self.rows[y % self.height][x % self.width]

    def set(self, y, x, state):
        self.rows[y % self.height][x % self.width] = state

    def __str__(self):
        output = ''
        for row in self.rows:
            for cell in row:
                output += cell
            output += '\n'
        return output


# Example 3
grid = Grid(5, 9)
grid.set(0, 3, ALIVE)
grid.set(1, 4, ALIVE)
grid.set(2, 2, ALIVE)
grid.set(2, 3, ALIVE)
grid.set(2, 4, ALIVE)
print(grid)


# Example 4
def count_neighbors(y, x, get):
    n_ = get(y - 1, x + 0)  # North
    ne = get(y - 1, x + 1)  # Northeast
    e_ = get(y + 0, x + 1)  # East
    se = get(y + 1, x + 1)  # Southeast
    s_ = get(y + 1, x + 0)  # South
    sw = get(y + 1, x - 1)  # Southwest
    w_ = get(y + 0, x - 1)  # West
    nw = get(y - 1, x - 1)  # Northwest
    neighbor_states = [n_, ne, e_, se, s_, sw, w_, nw]
    count = 0
    for state in neighbor_states:
        if state == ALIVE:
            count += 1
    return count

alive = {(9, 5), (9, 6)}
seen = set()

def fake_get(y, x):
    position = (y, x)
    seen.add(position)
    return ALIVE if position in alive else EMPTY

count = count_neighbors(10, 5, fake_get)
assert count == 2

expected_seen = {
    (9, 5),  (9, 6),  (10, 6), (11, 6),
    (11, 5), (11, 4), (10, 4), (9, 4)
}
assert seen == expected_seen


# Example 5
def game_logic(state, neighbors):
    if state == ALIVE:
        if neighbors < 2:
            return EMPTY     # Die: Too few
        elif neighbors > 3:
            return EMPTY     # Die: Too many
    else:
        if neighbors == 3:
            return ALIVE     # Regenerate
    return state

assert game_logic(ALIVE, 0) == EMPTY
assert game_logic(ALIVE, 1) == EMPTY
assert game_logic(ALIVE, 2) == ALIVE
assert game_logic(ALIVE, 3) == ALIVE
assert game_logic(ALIVE, 4) == EMPTY
assert game_logic(EMPTY, 0) == EMPTY
assert game_logic(EMPTY, 1) == EMPTY
assert game_logic(EMPTY, 2) == EMPTY
assert game_logic(EMPTY, 3) == ALIVE
assert game_logic(EMPTY, 4) == EMPTY


# Example 6
def step_cell(y, x, get, set):
    state = get(y, x)
    neighbors = count_neighbors(y, x, get)
    next_state = game_logic(state, neighbors)
    set(y, x, next_state)

alive = {(10, 5), (9, 5), (9, 6)}
new_state = None

def fake_get(y, x):
    return ALIVE if (y, x) in alive else EMPTY

def fake_set(y, x, state):
    global new_state
    new_state = state

# Stay alive
step_cell(10, 5, fake_get, fake_set)
assert new_state == ALIVE

# Stay dead
alive.remove((10, 5))
step_cell(10, 5, fake_get, fake_set)
assert new_state == EMPTY

# Regenerate
alive.add((10, 6))
step_cell(10, 5, fake_get, fake_set)
assert new_state == ALIVE


# Example 7
def simulate(grid):
    next_grid = Grid(grid.height, grid.width)
    for y in range(grid.height):
        for x in range(grid.width):
            step_cell(y, x, grid.get, next_grid.set)
    return next_grid


# Example 8
class ColumnPrinter:
    def __init__(self):
        self.columns = []

    def append(self, data):
        self.columns.append(data)

    def __str__(self):
        row_count = 1
        for data in self.columns:
            row_count = max(
                row_count, len(data.splitlines()) + 1)

        rows = [''] * row_count
        for j in range(row_count):
            for i, data in enumerate(self.columns):
                line = data.splitlines()[max(0, j - 1)]
                if j == 0:
                    padding = ' ' * (len(line) // 2)
                    rows[j] += padding + str(i) + padding
                else:
                    rows[j] += line

                if (i + 1) < len(self.columns):
                    rows[j] += ' | '

        return '\n'.join(rows)

columns = ColumnPrinter()
for i in range(5):
    columns.append(str(grid))
    grid = simulate(grid)

print(columns)


# Example 9
def game_logic(state, neighbors):
    # Do some blocking input/output in here:
    data = my_socket.recv(100)
