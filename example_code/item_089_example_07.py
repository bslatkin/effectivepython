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



print("Example 7")
import gc
import sys

def broken_generator():
    try:
        yield 70
        yield 80
    except BaseException as e:
        print("Broken handler", type(e), e)
        raise RuntimeError("Broken")

it = broken_generator()
print("Before")
print(next(it))
print("After")
sys.stdout.flush()
del it
gc.collect()
print("Still going")