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
from urllib.parse import parse_qs
my_values = parse_qs('red=5&blue=0&green=',
                     keep_blank_values=True)
print(repr(my_values))


# Example 2
print('Red:     ', my_values.get('red'))
print('Green:   ', my_values.get('green'))
print('Opacity: ', my_values.get('opacity'))


# Example 3
# For query string 'red=5&blue=0&green='
red = my_values.get('red', [''])[0] or 0
green = my_values.get('green', [''])[0] or 0
opacity = my_values.get('opacity', [''])[0] or 0
print('Red:     %r' % red)
print('Green:   %r' % green)
print('Opacity: %r' % opacity)


# Example 4
red = int(my_values.get('red', [''])[0] or 0)
green = int(my_values.get('green', [''])[0] or 0)
opacity = int(my_values.get('opacity', [''])[0] or 0)
print('Red:     %r' % red)
print('Green:   %r' % green)
print('Opacity: %r' % opacity)


# Example 5
red = my_values.get('red', [''])
red = int(red[0]) if red[0] else 0
green = my_values.get('green', [''])
green = int(green[0]) if green[0] else 0
opacity = my_values.get('opacity', [''])
opacity = int(opacity[0]) if opacity[0] else 0
print('Red:     %r' % red)
print('Green:   %r' % green)
print('Opacity: %r' % opacity)


# Example 6
green = my_values.get('green', [''])
if green[0]:
    green = int(green[0])
else:
    green = 0
print('Green:   %r' % green)


# Example 7
def get_first_int(values, key, default=0):
    found = values.get(key, [''])
    if found[0]:
        found = int(found[0])
    else:
        found = default
    return found


# Example 8
green = get_first_int(my_values, 'green')
print('Green:   %r' % green)
