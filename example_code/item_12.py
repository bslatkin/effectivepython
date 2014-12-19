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
for i in range(3):
    print('Loop %d' % i)
else:
    print('Else block!')


# Example 2
for i in range(3):
    print('Loop %d' % i)
    if i == 1:
        break
else:
    print('Else block!')


# Example 3
for x in []:
    print('Never runs')
else:
    print('For Else block!')


# Example 4
while False:
    print('Never runs')
else:
    print('While Else block!')


# Example 5
a = 4
b = 9

for i in range(2, min(a, b) + 1):
    print('Testing', i)
    if a % i == 0 and b % i == 0:
        print('Not coprime')
        break
else:
    print('Coprime')


# Example 6
def coprime(a, b):
    for i in range(2, min(a, b) + 1):
        if a % i == 0 and b % i == 0:
            return False
    return True
print(coprime(4, 9))
print(coprime(3, 6))


# Example 7
def coprime2(a, b):
    is_coprime = True
    for i in range(2, min(a, b) + 1):
        if a % i == 0 and b % i == 0:
            is_coprime = False
            break
    return is_coprime
print(coprime2(4, 9))
print(coprime2(3, 6))
