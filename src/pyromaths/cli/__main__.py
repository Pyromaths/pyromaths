#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2016-2018 -- Louis Paternault (spalax@gresille.org)
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

"""Pyromaths command line interface.

To display help:

> python -m pyromaths.cli --help
"""

import argparse
import gettext
import logging
import random
import sys

# Quick and dirty definition of `_` as the identity function
gettext.install('pyromaths', unicode=1)

from pyromaths.cli import exercise_argument, PyromathsException
from pyromaths.ex.test import TestPerformer, generate

# Logging configuration
logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger()

VERSION = "0.1.0"

def argument_parser():
    """Return an argument parser"""
    parser = argparse.ArgumentParser(
        prog='pyromaths-cli',
        )
    parser.add_argument(
        '-v', '--version',
        action='version',
        version='%(prog)s {version}'.format(version=VERSION),
        )
    subparsers = parser.add_subparsers(title='Commands', dest='command')
    subparsers.required = True
    subparsers.dest = 'command'

    # List exos
    ls = subparsers.add_parser( # pylint: disable=unused-variable
        'ls',
        help=(
            "List available exercises. Each line of the output can be used as "
            "an argument to other commands."
            ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        )
    ls.add_argument(
        "-v", "--verbose",
        help="Affiche davantage de détails.",
        action="store_true",
        )

    # Generate
    generate_parser = subparsers.add_parser(
        'generate',
        help='Generate some exercises.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        )
    generate_parser.add_argument(
        "exercise",
        metavar='EXERCISE[:SEED[,SEED]]',
        nargs='+', type=exercise_argument, default=None,
        help='Exercises to generate.'
        )
    generate_parser.add_argument(
        '-p', '--pipe',
        nargs=1,
        type=str,
        action='append',
        help=(
            "Commands to run on the LaTeX file before compiling. String '{}' "
            "is replaced by the file name; if not, it is appended at the end "
            "of the string."
            )
        )
    generate_parser.add_argument(
        '-o', '--output',
        type=str,
        default='exercice.pdf',
        help=(
            "Output filename. Default is 'exercice.pdf'."
            ),
        )

    # Test
    test = subparsers.add_parser(
        'test',
        help='Test exercices',
        )
    test.add_argument('args', nargs=argparse.REMAINDER)

    # GUI
    gui = subparsers.add_parser(
        'gui',
        help='Launch the pyromaths graphical user interface.',
        )
    gui.add_argument('args', nargs=argparse.REMAINDER)

    # Dummy
    dummy = subparsers.add_parser(
        'dummy',
        help='Generate a dummy LaTeX file.',
        )
    dummy.add_argument('args', nargs=argparse.REMAINDER)

    return parser

def do_test(options):
    """Action for command line 'test'."""
    from pyromaths.cli.test import __main__
    sys.exit(__main__.main(options.args))

def do_gui(options):
    """Action for command line 'gui'."""
    from pyromaths import pyromaths
    sys.argv = ["pyromaths"] + sys.argv[2:]
    pyromaths.main()

def do_dummy(options):
    """Action for command line 'dummy'."""
    from . import dummy
    dummy.main()

def do_generate(options):
    """Action for command line 'generate'."""
    tests = TestPerformer()

    if options.pipe is None:
        options.pipe = []
    else:
        options.pipe = [item[0] for item in options.pipe]

    exercise_list = []
    for exercise, seeds in options.exercise:
        if not seeds:
            seeds = [random.randint(0, sys.maxint)]
        for seed in seeds:
            exercise_list.append(tests.get(exercise, seed).get_exercise())

    generate(
        exercise_list,
        destname=options.output,
        pipe=options.pipe,
        )

def do_ls(options): # pylint: disable=unused-argument
    """Perform the `ls` command."""
    tests = TestPerformer()
    for name in sorted(tests.iter_names(), key=str.lower):
        if options.verbose:
            print(u"{}: {}".format(name, tests.exercises[name].description)) # pylint: disable=superfluous-parens
        else:
            print(name) # pylint: disable=superfluous-parens

COMMANDS = {
    "generate": do_generate,
    "ls": do_ls,
    "test": do_test,
    "gui": do_gui,
    "dummy": do_dummy,
    }

def main():
    """Main function"""
    options = argument_parser().parse_args(sys.argv[1:])

    try:
        COMMANDS[options.command](options)
    except PyromathsException as error:
        logging.error(error)
        sys.exit(1)

if __name__ == "__main__":
    main()
