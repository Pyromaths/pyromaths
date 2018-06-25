#!/usr/bin/env python3

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

"""Pyromaths exercise regression tests

To display help:

> python3 -m pyromaths.cli.test --help
"""
from __future__ import unicode_literals

from builtins import input
import argparse
import gettext
import logging
import sys
import unittest

# Quick and dirty definition of `_` as the identity function
gettext.install('pyromaths')

from pyromaths.cli import exercise_argument, PyromathsException
from pyromaths.ex.test import TestPerformer

# Logging configuration
logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger()

VERSION = "0.1.0"

def ask_confirm(message):
    """Ask a confirmation for some message.

    :rtype bool:
    :return: True iff user agreed (answered ``y``), False if user did not
        (answered ``n``).
    """
    while True:
        try:
            answer = input("{} (y/n) [n]? ".format(message))
        except EOFError:
            answer = 'n'
        if answer == 'y':
            return True
        elif answer == 'n':
            return False

def argument_parser():
    """Return an argument parser"""
    parser = argparse.ArgumentParser(
        prog="pyromaths-cli test",
        )
    parser.add_argument(
        '-v', '--version',
        action='version',
        version='%(prog)s {version}'.format(version=VERSION),
        )
    subparsers = parser.add_subparsers(title='Commands', dest='command')
    subparsers.required = True
    subparsers.dest = 'command'

    # Create
    create = subparsers.add_parser(
        'create',
        help='Create test given in argument.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        )
    create.add_argument(
        "exercise",
        metavar='EXERCISE[:SEED[,SEED]]',
        nargs='+', type=exercise_argument,
        help='Exercises to test.'
        )

    # Missing
    missing = subparsers.add_parser( # pylint: disable=unused-variable
        'missing',
        help='Create missing tests.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        )

    # Remove
    remove = subparsers.add_parser(
        'remove',
        help='Remove a test',
        )
    remove.add_argument(
        "exercise",
        metavar='EXERCISE[:SEED[,SEED]]',
        nargs='+', type=exercise_argument, default=None,
        help='Exercises to remove.',
        )

    # Update
    update = subparsers.add_parser(
        'update',
        help=(
            "Perform tests given in argument. "
            "Update tests that have changed."
            ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        )
    update.add_argument(
        "exercise",
        metavar='EXERCISE[:SEED[,SEED]]',
        nargs='*', type=exercise_argument, default=None,
        help='Exercises to test. If empty, all exercises are tested.'
        )

    # Check
    check = subparsers.add_parser(
        'check',
        help=(
            "Test exercises (equivalent to `python3 -m unittest discover`, "
            "for exercises only)."
            ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        )
    check.add_argument(
        "exercise",
        metavar='EXERCISE[:SEED[,SEED]]',
        nargs='*', type=exercise_argument, default=None,
        help='Exercises to check. If empty, all exercises are checked.'
        )

    return parser

def do_create(options):
    """Action for command line 'create'."""
    tests = TestPerformer()

    for exercise, seeds in options.exercise:
        if not seeds:
            seeds = [0]
        for seed in seeds:
            test = tests.get(exercise, seed)
            test.show()
            if ask_confirm("Is the test valid?"):
                test.write()

def do_missing(options): # pylint: disable=unused-argument
    """Action for command line 'missing'."""
    tests = TestPerformer()

    for exercise in tests.iter_missing():
        test = tests.get(exercise, 0)
        test.show()
        if ask_confirm("Is the test valid?"):
            test.write()

def do_remove(options):
    """Action for command line 'remove'."""
    tests = TestPerformer()

    for exercise, seeds in options.exercise:
        if not seeds:
            seeds = tests.get_tested_seeds(exercise)
        for seed in seeds:
            if ask_confirm("Remove test {}:{}?".format(exercise, seed)):
                tests.get(exercise, seed).remove()

def get_exercise_list_or_all(tests, exercise_option):
    """Return list of exercises provided by user, or every exercise.

    - If user provided an exercise list, return a list of tuples `(exercise,
      seeds)`.
    - If user did not, return a list of tuples `(exercise, seeds)` for all
      tests found in the data directory.
    """
    if exercise_option:
        exercise_list = []
        for exercise, seeds in exercise_option:
            if seeds:
                exercise_list.append((exercise, seeds))
            else:
                exercise_list.append((exercise, tests.get_tested_seeds(exercise)))
    else:
        exercise_list = [
            (exo, tests.get_tested_seeds(exo))
            for exo in tests.iter_names()
            ]

    return exercise_list

def do_update(options):
    """Action for command line 'update'."""
    tests = TestPerformer()

    for exercise, seeds in get_exercise_list_or_all(tests, options.exercise):
        for seed in seeds:
            test = tests.get(exercise, seed)
            if test.changed():
                test.show()
                test.print_diff()
                if ask_confirm("Is the test valid?"):
                    test.write()

def do_check(options):
    """Run the tests"""
    tests = TestPerformer()

    unittest.TextTestRunner(verbosity=2).run(
        tests.as_unittest_suite(
            get_exercise_list_or_all(tests, options.exercise)
            )
        )

COMMANDS = {
    "check": do_check,
    "create": do_create,
    "missing": do_missing,
    "remove": do_remove,
    "update": do_update,
    }

def main(argv=None):
    """Main function"""
    if argv is None:
        argv = sys.argv[1:]
    options = argument_parser().parse_args(argv)

    try:
        COMMANDS[options.command](options)
    except PyromathsException as error:
        logging.error(error)
        sys.exit(1)

if __name__ == "__main__":
    main()
