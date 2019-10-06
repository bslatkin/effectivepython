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

from unittest import TestCase, main

def sum_squares(values):
    cumulative = 0
    for value in values:
        cumulative += value ** 2
        yield cumulative

class HelperTestCase(TestCase):
    def verify_complex_case(self, values, expected):
        expect_it = iter(expected)
        found_it = iter(sum_squares(values))
        test_it = zip(expect_it, found_it)

        for i, (expect, found) in enumerate(test_it):
            self.assertEqual(
                expect,
                found,
                f'Index {i} is wrong')

        # Verify both generators are exhausted
        try:
            next(expect_it)
        except StopIteration:
            pass
        else:
            self.fail('Expected longer than found')

        try:
            next(found_it)
        except StopIteration:
            pass
        else:
            self.fail('Found longer than expected')

    def test_wrong_lengths(self):
        values = [1.1, 2.2, 3.3]
        expected = [
            1.1**2,
        ]
        self.verify_complex_case(values, expected)

    def test_wrong_results(self):
        values = [1.1, 2.2, 3.3]
        expected = [
            1.1**2,
            1.1**2 + 2.2**2,
            1.1**2 + 2.2**2 + 3.3**2 + 4.4**2,
        ]
        self.verify_complex_case(values, expected)

if __name__ == '__main__':
    main()
