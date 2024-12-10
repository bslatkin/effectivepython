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



print("Example 12")
# Check types in this file with: python -m mypy <path>

from typing import Any, Final, Never

class ImmutablePoint:
    name: Final[str]
    x: Final[int]
    y: Final[int]

    def __init__(self, name: str, x: int, y: int) -> None:
        self.name = name
        self.x = x
        self.y = y

    def __setattr__(self, key: str, value: Any) -> None:
        if key in self.__annotations__ and key not in dir(self):
            # Allow the very first assignment to happen
            super().__setattr__(key, value)
        else:
            raise AttributeError("Immutable object")

    def __delattr__(self, key: str) -> Never:
        raise AttributeError("Immutable object")


origin = ImmutablePoint("origin", 0, 0)
origin.x = -3
