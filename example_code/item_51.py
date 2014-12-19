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
try:
    def determine_weight(volume, density):
        if density <= 0:
            raise ValueError('Density must be positive')
    
    determine_weight(1, 0)
except:
    logging.exception('Expected')
else:
    assert False


# Example 2
# my_module.py
class Error(Exception):
    """Base-class for all exceptions raised by this module."""

class InvalidDensityError(Error):
    """There was a problem with a provided density value."""


# Example 3
class my_module(object):
    Error = Error
    InvalidDensityError = InvalidDensityError

    @staticmethod
    def determine_weight(volume, density):
        if density <= 0:
            raise InvalidDensityError('Density must be positive')
try:
    weight = my_module.determine_weight(1, -1)
    assert False
except my_module.Error as e:
    logging.error('Unexpected error: %s', e)


# Example 4
weight = 5
try:
    weight = my_module.determine_weight(1, -1)
    assert False
except my_module.InvalidDensityError:
    weight = 0
except my_module.Error as e:
    logging.error('Bug in the calling code: %s', e)

assert weight == 0


# Example 5
weight = 5
try:
    weight = my_module.determine_weight(1, -1)
    assert False
except my_module.InvalidDensityError:
    weight = 0
except my_module.Error as e:
    logging.error('Bug in the calling code: %s', e)
except Exception as e:
    logging.error('Bug in the API code: %s', e)
    raise

assert weight == 0


# Example 6
# my_module.py
class NegativeDensityError(InvalidDensityError):
    """A provided density value was negative."""

def determine_weight(volume, density):
    if density < 0:
        raise NegativeDensityError


# Example 7
try:
    my_module.NegativeDensityError = NegativeDensityError
    my_module.determine_weight = determine_weight
    try:
        weight = my_module.determine_weight(1, -1)
        assert False
    except my_module.NegativeDensityError as e:
        raise ValueError('Must supply non-negative density') from e
    except my_module.InvalidDensityError:
        weight = 0
    except my_module.Error as e:
        logging.error('Bug in the calling code: %s', e)
    except Exception as e:
        logging.error('Bug in the API code: %s', e)
        raise
except:
    logging.exception('Expected')
else:
    assert False


# Example 8
# my_module.py
class WeightError(Error):
    """Base-class for weight calculation errors."""

class VolumeError(Error):
    """Base-class for volume calculation errors."""

class DensityError(Error):
    """Base-class for density calculation errors."""
