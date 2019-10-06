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

import math

def squared_error(point, mean):
    err = point - mean
    return err ** 2

def compute_variance(data):
    mean = sum(data) / len(data)
    err_2_sum = sum(squared_error(x, mean) for x in data)
    variance = err_2_sum / (len(data) - 1)
    return variance

def compute_stddev(data):
    variance = compute_variance(data)
    return math.sqrt(variance)
