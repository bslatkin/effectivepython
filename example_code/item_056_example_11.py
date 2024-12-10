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



print("Example 11")
# Check types in this file with: python3 -m mypy <path>

from dataclasses import dataclass

@dataclass(frozen=True)
class DataclassImmutablePoint:
    name: str
    x: float
    y: float

origin = DataclassImmutablePoint("origin", 0, 0)
origin.x = -3
