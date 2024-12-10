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

# my_extension_test.py
import unittest
import my_extension

class MyExtensionTest(unittest.TestCase):

    def test_empty(self):
        result = my_extension.dot_product([], [])
        self.assertAlmostEqual(0, result)

    def test_positive_result(self):
        result = my_extension.dot_product(
            [3, 4, 5],
            [-1, 9, -2.5],
        )
        self.assertAlmostEqual(20.5, result)

    def test_zero_result(self):
        result = my_extension.dot_product(
            [0, 0, 0],
            [1, 1, 1],
        )
        self.assertAlmostEqual(0, result)

    def test_negative_result(self):
        result = my_extension.dot_product(
            [-1, -1, -1],
            [1, 1, 1],
        )
        self.assertAlmostEqual(-3, result)

    def test_not_lists(self):
        with self.assertRaises(TypeError) as context:
            my_extension.dot_product((1, 2), [3, 4])
        self.assertEqual(
            "Both arguments must be lists", str(context.exception)
        )

        with self.assertRaises(TypeError) as context:
            my_extension.dot_product([1, 2], (3, 4))
        self.assertEqual(
            "Both arguments must be lists", str(context.exception)
        )

    def test_mismatched_size(self):
        with self.assertRaises(ValueError) as context:
            my_extension.dot_product([1], [2, 3])
        self.assertEqual(
            "Lists must be the same length", str(context.exception)
        )

        with self.assertRaises(ValueError) as context:
            my_extension.dot_product([1, 2], [3])
        self.assertEqual(
            "Lists must be the same length", str(context.exception)
        )

    def test_not_floatable(self):
        with self.assertRaises(TypeError) as context:
            my_extension.dot_product(["bad"], [1])
        self.assertEqual(
            "must be real number, not str", str(context.exception)
        )


if __name__ == "__main__":
    unittest.main()
