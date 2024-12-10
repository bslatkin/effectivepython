/*
 * Copyright 2014-2024 Brett Slatkin, Pearson Education Inc.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

#include "my_extension.h"

PyObject *dot_product(PyObject *self, PyObject *args)
{
    PyObject *left, *right;
    if (!PyArg_ParseTuple(args, "OO", &left, &right)) {
        return NULL;
    }
    if (!PyList_Check(left) || !PyList_Check(right)) {
        PyErr_SetString(PyExc_TypeError, "Both arguments must be lists");
        return NULL;
    }

    Py_ssize_t left_length = PyList_Size(left);
    Py_ssize_t right_length = PyList_Size(right);
    if (left_length == -1 || right_length == -1) {
        return NULL;
    }
    if (left_length != right_length) {
        PyErr_SetString(PyExc_ValueError, "Lists must be the same length");
        return NULL;
    }

    double result = 0;

    for (Py_ssize_t i = 0; i < left_length; i++) {
        PyObject *left_item = PyList_GET_ITEM(left, i);
        PyObject *right_item = PyList_GET_ITEM(right, i);

        double left_double = PyFloat_AsDouble(left_item);
        double right_double = PyFloat_AsDouble(right_item);
        if (PyErr_Occurred()) {
            return NULL;
        }

        result += left_double * right_double;
    }

    return PyFloat_FromDouble(result);
}
