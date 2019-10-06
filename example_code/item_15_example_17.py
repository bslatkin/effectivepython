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



# Example 17
# Check types in this file with: python -m mypy <path>

from typing import Dict, MutableMapping

def populate_ranks(votes: Dict[str, int],
                   ranks: Dict[str, int]) -> None:
    names = list(votes.keys())
    names.sort(key=votes.get, reverse=True)
    for i, name in enumerate(names, 1):
        ranks[name] = i

def get_winner(ranks: Dict[str, int]) -> str:
    return next(iter(ranks))

from typing import Iterator, MutableMapping

class SortedDict(MutableMapping[str, int]):
    def __init__(self) -> None:
        self.data: Dict[str, int] = {}

    def __getitem__(self, key: str) -> int:
        return self.data[key]

    def __setitem__(self, key: str, value: int) -> None:
        self.data[key] = value

    def __delitem__(self, key: str) -> None:
        del self.data[key]

    def __iter__(self) -> Iterator[str]:
        keys = list(self.data.keys())
        keys.sort()
        for key in keys:
            yield key

    def __len__(self) -> int:
        return len(self.data)

votes = {
    'otter': 1281,
    'polar bear': 587,
    'fox': 863,
}

sorted_ranks = SortedDict()
populate_ranks(votes, sorted_ranks)
print(sorted_ranks.data)
winner = get_winner(sorted_ranks)
print(winner)
