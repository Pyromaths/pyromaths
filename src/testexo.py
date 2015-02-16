#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Pyromaths exercise regression tests

To display help:

> testexo --help
"""

import argparse
import logging
import sys
import unittest

import pyromaths.ex.test

# Logging configuration
logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger()

VERSION = "0.1.0"

def match_exercise(path):
    """Return the exercises in `path`."""
    exercises = []
    for level in pyromaths.ex.levels:
        for exercise in pyromaths.ex.levels[level]:
            if pyromaths.ex.LegacyExercise in exercise.__bases__:
                continue
            if exercise.__module__.startswith(path):
                exercises.append(exercise)
    return exercises

def exercise_argument(string=""):
    """Return the exercises matching ``string``.

    :param str string: a string, option of one of `testexo` commands.
    :rtype: dict
    :return: A dictionary with exercises as keys, and sets of integers (seeds)
    as values.
    """
    splitted = string.split(":")
    if len(splitted) == 1:
        path = string
        seeds = []
    elif len(splitted) == 2:
        path, seeds = string.split(":")
        try:
            seeds = [int(seed) for seed in seeds.split(",")]
        except ValueError:
            raise argparse.ArgumentTypeError("TODO")
    else:
        raise argparse.ArgumentTypeError("TODO")

    if path.endswith(".py"):
        path = path[:-3]

    return dict([
        (exo, seeds) for exo in match_exercise(path.replace('/', '.'))
        ])

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
        help='Create test given in argument. If not, create missing tests.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        )
    create.add_argument(
        "exercise",
        metavar='EXERCISE[:SEED[,SEED]]',
        nargs='*', type=exercise_argument, default=None,
        help='Exercices to test. If empty, all exercises are tested.'
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
        help='Exercices to remove.',
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
        help='Exercices to test. If empty, all exercises are tested.'
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
        help='Exercices to compile. If empty, all exercises are compiled.'
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
        help='Exercices to check. If empty, all exercises are checked.'
        )

    return parser

def do_create(exercises, test_suite):
    """Action for command line 'create'."""
    for exo in exercises:
        if not exercises[exo]:
            seeds = set([0])
        else:
            seeds = exercises[exo]
        for seed in seeds:
            if not test_suite.has_test(exo, seed):
                test_suite.create_test(exo, seed)
    test_suite.write_testfiles()

def do_remove(exercises, test_suite):
    """Action for command line 'remove'."""
    for exo in exercises:
        if not exercises[exo]:
            seeds = test_suite.get_exercise(exo).seeds
        else:
            seeds = exercises[exo]
        for seed in list(seeds.keys()):
            if test_suite.has_test(exo, seed):
                test_suite.remove_test(exo, seed)
    test_suite.write_testfiles()

def do_update(exercises, test_suite):
    """Action for command line 'update'."""
    for exo in exercises:
        if not exercises[exo]:
            seeds = test_suite.get_exercise(exo).seeds
        else:
            seeds = exercises[exo]
        for seed in seeds:
            exo_instance = test_suite.get_exercise(exo)
            LOGGER.info(u"Testing exercise {}[{}]…".format(
                exo_instance.name,
                seed,
                ))
            if not pyromaths.ex.test.simple_runtest(
                    exo_instance[seed]
                ):
                test_suite.create_test(exo, seed)
    test_suite.write_testfiles()

def do_compile(exercises, test_suite):
    """Action for command line 'compile'."""
    for exo in exercises:
        if not exercises[exo]:
            seeds = test_suite.get_exercise(exo).seeds
        else:
            seeds = exercises[exo]
        exo_instance = test_suite.get_exercise(exo)
        if not exo_instance.seeds:
            exo_instance.add_seed(0)
        for seed in seeds:
            exo_instance[seed].compile(movefile=True)

def do_check(__exercises, test_suite):
    """Run the tests"""
    suite = unittest.TestSuite(list(test_suite.iter_tests()))
    unittest.TextTestRunner(verbosity=2).run(suite)

COMMANDS = {
    "check": do_check,
    "create": do_create,
    "remove": do_remove,
    "compile": do_compile,
    "update": do_update,
    }

def main():
    """Main function"""
    pyromaths.ex.load()
    options = argument_parser().parse_args(sys.argv[1:])
    test_suite = pyromaths.ex.test.create_test_suite()

    exercises = {}
    if not options.exercise:
        options.exercise = [exercise_argument()]
    for exo_option in options.exercise:
        for exo in exo_option:
            if exo not in exercises:
                exercises[exo] = set()
            exercises[exo] |= set(exo_option[exo])

    try:
        COMMANDS[options.command](exercises, test_suite)
    except pyromaths.ex.test.ActionCancelAll:
        sys.exit(1)

if __name__ == "__main__":
    main()
