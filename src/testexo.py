#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2015 -- Louis Paternault (spalax@gresille.org)
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

> testexo --help
"""

import argparse
import logging
import sys
import unittest

from pyromaths.ex.test import TestPerformer, TestException

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
            answer = raw_input("{} (y/n) [n]? ".format(message))
        except EOFError:
            answer = 'n'
        if answer == 'y':
            return True
        elif answer == 'n':
            return False

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
            raise argparse.ArgumentTypeError("TODO")
    else:
        raise argparse.ArgumentTypeError("TODO")

    return (name, seeds)

def argument_parser():
    """Return an argument parser"""
    parser = argparse.ArgumentParser()
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
    missing = subparsers.add_parser(
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

    # Compile
    compile_parser = subparsers.add_parser(
        'compile',
        help='Compile some exercises.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        )
    compile_parser.add_argument(
        "exercise",
        metavar='EXERCISE[:SEED[,SEED]]',
        nargs='*', type=exercise_argument, default=None,
        help='Exercises to compile. If empty, all exercises are compiled.'
        )

    # Check
    check = subparsers.add_parser(
        'check',
        help=(
            "Test exercises (equivalent to `python -m unittest discover`, "
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

    # List exos
    lsexos = subparsers.add_parser(
        'lsexos',
        help=(
            "List available exercises. Each line of the output can be used as "
            "an argument to other commands."
            ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
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

def do_missing(__options):
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
            for exo in tests.iter_id()
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
                if ask_confirm("Is the test valid?"):
                    test.write()

def do_compile(options):
    """Action for command line 'compile'."""
    tests = TestPerformer()

    for exercise, seeds in options.exercise:
        if not seeds:
            seeds = [0]
        for seed in seeds:
            test = tests.get(exercise, seed)
            test.compile(movefile=True)

def do_check(options):
    """Run the tests"""
    tests = TestPerformer()

    unittest.TextTestRunner(verbosity=2).run(
        tests.as_unittest_suite(
            get_exercise_list_or_all(tests, options.exercise)
            )
        )

def do_lsexos(__options):
    """Perform the `lsexos` command."""
    tests = TestPerformer()
    for exo_id in tests.iter_id():
        print exo_id

COMMANDS = {
    "check": do_check,
    "compile": do_compile,
    "create": do_create,
    "lsexos": do_lsexos,
    "missing": do_missing,
    "remove": do_remove,
    "update": do_update,
    }

def main():
    """Main function"""
    options = argument_parser().parse_args(sys.argv[1:])

    try:
        COMMANDS[options.command](options)
    except TestException as error:
        logging.error(error)
        sys.exit(1)

if __name__ == "__main__":
    main()
