#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright Louis Paternault 2018
#
# This file is part of Pyromaths.
#
# Pyromaths is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Pyromaths is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero Public License for more details.
#
# You should have received a copy of the GNU Affero Public License
# along with Pyromaths.  If not, see <http://www.gnu.org/licenses/>.

import os
import runpy
import sys

sys.path.insert(0, os.path.realpath(os.path.join(os.path.abspath(os.path.dirname(__file__)), os.pardir, "src")))

if __name__ == "__main__":
    runpy.run_module("pyromaths.cli", run_name="__main__")
