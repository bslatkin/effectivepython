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

# my_extension2_test.py
import unittest
import my_extension2

class MyExtension2Test(unittest.TestCase):

    def test_decimals(self):
        import decimal

        a = [decimal.Decimal(1), decimal.Decimal(2)]
        b = [decimal.Decimal(3), decimal.Decimal(4)]
        result = my_extension2.dot_product(a, b)
        self.assertEqual(11, result)

    def test_not_lists(self):
        result1 = my_extension2.dot_product(
            (1, 2),
            [3, 4],
        )
        result2 = my_extension2.dot_product(
            [1, 2],
            (3, 4),
        )
        result3 = my_extension2.dot_product(
            range(1, 3),
            range(3, 5),
        )
        self.assertAlmostEqual(11, result1)
        self.assertAlmostEqual(11, result2)
        self.assertAlmostEqual(11, result3)

    def test_empty(self):
        result = my_extension2.dot_product([], [])
        self.assertAlmostEqual(0, result)

    def test_positive_result(self):
        result = my_extension2.dot_product(
            [3, 4, 5],
            [-1, 9, -2.5],
        )
        self.assertAlmostEqual(20.5, result)

    def test_zero_result(self):
        result = my_extension2.dot_product(
            [0, 0, 0],
            [1, 1, 1],
        )
        self.assertAlmostEqual(0, result)

    def test_negative_result(self):
        result = my_extension2.dot_product(
            [-1, -1, -1],
            [1, 1, 1],
        )
        self.assertAlmostEqual(-3, result)

    def test_mismatched_size(self):
        with self.assertRaises(ValueError) as context:
            my_extension2.dot_product([1], [2, 3])
        self.assertEqual(
            "Arguments had unequal length", str(context.exception)
        )

        with self.assertRaises(ValueError) as context:
            my_extension2.dot_product([1, 2], [3])
        self.assertEqual(
            "Arguments had unequal length", str(context.exception)
        )

    def test_not_floatable(self):
        with self.assertRaises(TypeError) as context:
            my_extension2.dot_product(["bad"], [1])
        self.assertEqual(
            "unsupported operand type(s) for +: 'int' and 'str'",
            str(context.exception),
        )


if __name__ == "__main__":
    unittest.main()
