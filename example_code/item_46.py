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
from collections import deque
fifo = deque()
fifo.append(1)      # Producer
fifo.append(2)
fifo.append(3)
x = fifo.popleft()  # Consumer
print(x)


# Example 2
a = {}
a['foo'] = 1
a['bar'] = 2
from random import randint

# Randomly populate 'b' to cause hash conflicts
while True:
    z = randint(99, 1013)
    b = {}
    for i in range(z):
        b[i] = i
    b['foo'] = 1
    b['bar'] = 2
    for i in range(z):
        del b[i]
    if str(b) != str(a):
        break

print(a)
print(b)
print('Equal?', a == b)


# Example 3
from collections import OrderedDict
a = OrderedDict()
a['foo'] = 1
a['bar'] = 2

b = OrderedDict()
b['foo'] = 'red'
b['bar'] = 'blue'

for value1, value2 in zip(a.values(), b.values()):
    print(value1, value2)


# Example 4
stats = {}
key = 'my_counter'
if key not in stats:
    stats[key] = 0
stats[key] += 1
print(stats)


# Example 5
from collections import defaultdict
stats = defaultdict(int)
stats['my_counter'] += 1
print(dict(stats))


# Example 6
from heapq import *
a = []
heappush(a, 5)
heappush(a, 3)
heappush(a, 7)
heappush(a, 4)


# Example 7
print(heappop(a), heappop(a), heappop(a), heappop(a))


# Example 8
a = []
heappush(a, 5)
heappush(a, 3)
heappush(a, 7)
heappush(a, 4)
assert a[0] == nsmallest(1, a)[0] == 3


# Example 9
print('Before:', a)
a.sort()
print('After: ', a)


# Example 10
x = list(range(10**6))
i = x.index(991234)
print(i)


# Example 11
from bisect import bisect_left
i = bisect_left(x, 991234)
print(i)


# Example 12
from timeit import timeit
print(timeit(
    'a.index(len(a)-1)',
    'a = list(range(100))',
    number=1000))
print(timeit(
    'bisect_left(a, len(a)-1)',
    'from bisect import bisect_left;'
    'a = list(range(10**6))',
    number=1000))
