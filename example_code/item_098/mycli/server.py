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

# server.py
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/adjust", methods=["GET", "POST"])
def do_adjust():
    if request.method == "POST":
        the_file = request.files["the_file"]
        brightness = request.form["brightness"]
        contrast = request.form["contrast"]
        import adjust   # Dynamic import

        return adjust.do_adjust(the_file, brightness, contrast)
    else:
        return render_template("adjust.html")

@app.route("/enhance", methods=["GET", "POST"])
def do_enhance():
    if request.method == "POST":
        the_file = request.files["the_file"]
        amount = request.form["amount"]
        import enhance  # Dynamic import

        return enhance.do_enhance(the_file, amount)
    else:
        return render_template("enhance.html")
