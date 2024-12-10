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

### Start book environment setup
import random
random.seed(1234)

import logging
from pprint import pprint
from sys import stdout as STDOUT

# Write all output to a temporary directory
import atexit
import gc
import io
import os
import tempfile

TEST_DIR = tempfile.TemporaryDirectory()
atexit.register(TEST_DIR.cleanup)

# Make sure Windows processes exit cleanly
OLD_CWD = os.getcwd()
atexit.register(lambda: os.chdir(OLD_CWD))
os.chdir(TEST_DIR.name)

def close_open_files():
    everything = gc.get_objects()
    for obj in everything:
        if isinstance(obj, io.IOBase):
            obj.close()

atexit.register(close_open_files)
### End book environment setup


print("Example 1")
try:
    def do_processing():
        raise KeyboardInterrupt
    
    def main(argv):
        while True:
            try:
                do_processing()  # Interrupted
            except Exception as e:
                print("Error:", type(e), e)
    
        return 0
    
    if __name__ == "__main__":
        sys.exit(main(sys.argv))
    else:
        main(["foo.csv"])
except:
    logging.exception('Expected')
else:
    assert False


print("Example 2")
try:
    with open("my_data.csv", "w") as f:
        f.write("file exists")
    
    def do_processing(handle):
        raise KeyboardInterrupt
    
    def main(argv):
        data_path = argv[1]
        handle = open(data_path, "w+")
    
        while True:
            try:
                do_processing(handle)
            except Exception as e:
                print("Error:", type(e), e)
            except BaseException:
                print("Cleaning up interrupt")
                handle.flush()
                handle.close()
                return 1
    
        return 0
    
    if __name__ == "__main__":
        sys.exit(main(sys.argv))
    else:
        main(["ignore", "foo.csv"])
except:
    logging.exception('Expected')
else:
    assert False


print("Example 3")
try:
    def do_processing(handle):
        raise KeyboardInterrupt
    
    def main(argv):
        data_path = argv[1]
        handle = open(data_path, "w+")
    
        try:
            while True:
                try:
                    do_processing(handle)
                except Exception as e:
                    print("Error:", type(e), e)
        finally:
            print("Cleaning up finally")  # Always runs
            handle.flush()
            handle.close()
    
    if __name__ == "__main__":
        sys.exit(main(sys.argv))
    else:
        main(["ignore", "foo.csv"])
except:
    logging.exception('Expected')
else:
    assert False


print("Example 4")
try:
    def do_processing():
        raise KeyboardInterrupt
    
    def input(prompt):
        print(f"{prompt}y")
        return "y"
    
    def main(argv):
        while True:
            try:
                do_processing()
            except Exception as e:
                print("Error:", type(e), e)
            except KeyboardInterrupt:
                found = input("Terminate? [y/n]: ")
                if found == "y":
                    raise  # Propagate the error
    
    if __name__ == "__main__":
        sys.exit(main(sys.argv))
    else:
        main(["ignore", "foo.csv"])
    
    del input
except:
    logging.exception('Expected')
else:
    assert False


print("Example 5")
import functools

def log(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
        except Exception as e:
            result = e
            raise
        finally:
            print(
                f"Called {func.__name__}"
                f"(*{args!r}, **{kwargs!r}) "
                f"got {result!r}"
            )

    return wrapper


print("Example 6")
try:
    @log
    def my_func(x):
        x / 0
    
    my_func(123)
except:
    logging.exception('Expected')
else:
    assert False


print("Example 7")
try:
    @log
    def other_func(x):
        if x > 0:
            sys.exit(1)
    
    other_func(456)
except:
    logging.exception('Expected')
else:
    assert False


print("Example 8")
def fixed_log(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
        except BaseException as e:  # Fixed
            result = e
            raise
        finally:
            print(
                f"Called {func.__name__}"
                f"(*{args!r}, **{kwargs!r}) "
                f"got {result!r}"
            )

    return wrapper


print("Example 9")
try:
    @fixed_log
    def other_func(x):
        if x > 0:
            sys.exit(1)
    
    other_func(456)
except:
    logging.exception('Expected')
else:
    assert False
