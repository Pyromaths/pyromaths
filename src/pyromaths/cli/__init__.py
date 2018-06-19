# -*- coding: utf-8 -*-
#
# Copyright (C) 2016 -- Louis Paternault (spalax@gresille.org)
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301 USA

"""Generic stuff for pyromaths command line interface"""
from __future__ import unicode_literals

import argparse

class PyromathsException(Exception):
    """Generic exception for this module."""
    pass

def exercise_argument(string=""):
    """Return the exercises matching ``string``.

    :param str string: a string, option of one of `testexo` commands.
    :rtype: dict
    :return: A dictionary with exercises as keys, and sets of integers (seeds)
    as values.
    """
    splitted = string.split(":")
    if len(splitted) == 1:
        name = string
        seeds = []
    elif len(splitted) == 2:
        name, seeds = string.split(":")
        try:
            seeds = [int(seed) for seed in seeds.split(",")]
        except ValueError:
            raise argparse.ArgumentTypeError("Seeds must be a comma separated list of integers.")
    else:
        raise argparse.ArgumentTypeError("Seeds must be a comma separated list of integers.")

    return (name, seeds)

