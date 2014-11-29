#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Pyromaths
# Un programme en Python qui permet de créer des fiches d'exercices types de
# mathématiques niveau collège ainsi que leur corrigé en LaTeX.
# Copyright (C) 2006 -- Jérôme Ortais (jerome.ortais@pyromaths.org)
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

"""Test of exercises.

This module gather tests from all exercises. Running:

    python -m unittest discover

does just as expected.
"""

import codecs
import json
import os
import random
import textwrap
import unittest

import pyromaths
from pyromaths import ex

class ActionCancel(Exception):
    pass

class ActionCancelAll(Exception):
    pass

def fullclassname(argument):
    """Return the full name of a python object.

    That is, return its module name followed by its class name.
    """
    return "{}.{}".format(
        argument.__module__,
        argument.__class__.__name__,
        )

class Test(object):
    """Generic test class.

    All subclasses of this class are handle test creation, deletion,
    performance of tests of some exercises.
    """
    pass

class TestPackage(Test):
    """Test of a package"""

    def __init__(self):
        super(TestPackage, self).__init__()
        self.modules = {}

    def read_testfiles(self):
        """Read test files of exercises."""
        for module in self:
            self[module].read_testfile()

    def write_testfiles(self):
        """Write test files of exercises"""
        for module in self:
            self[module].write_testfile()

    def add_exercise(self, exercise):
        """Add an exercise to the test suite."""
        self.add_module(exercise.__module__)
        self[exercise.__module__].add_exercise(exercise)

    def add_module(self, modulename):
        """Create a sub module of this package."""
        if modulename not in self:
            self.modules[modulename] = TestModule(modulename)

    def get_exercise(self, exercise):
        """Return the :class:`TestExercise` instance corresponding to argument.
        """
        return self[exercise.__module__][exercise.__name__]

    def has_test(self, exercise, seed):
        """Return True iff there is a test to ``exercises`` with ``seed``."""
        if exercise.__module__ not in self:
            return False
        return self[exercise.__module__].has_test(exercise, seed)

    def create_test(self, exercise, seed):
        """Create a test to ``exercise`` with ``seed``.

        If such test already exists, it is replaced.
        """
        self.add_module(exercise.__module__)
        self[exercise.__module__].create_test(exercise, seed)

    def remove_test(self, exercise, seed):
        """Remove test of ``exercise`` with ``seed``"""
        if exercise.__module__ not in self:
            return
        self[exercise.__module__].remove_test(exercise, seed)

    def __iter__(self):
        return iter(self.modules)

    def __getitem__(self, key):
        return self.modules[key]

    def iter_tests(self):
        """Return an iterator over tests.

        The iterator iterates over :class:`unittest.TestCase` intances.
        """
        for module in self:
            for test in self[module].iter_tests():
                yield test

class TestModule(Test):
    """Test of exercises of a module."""

    def __init__(self, name):
        super(TestModule, self).__init__()
        self.name = name
        self.exercises = {}

    def create_test(self, exercise, seed):
        """Create a test to ``exercise`` with ``seed``.

        If such a test already exists, it is replaced.
        """
        self.add_exercise(exercise)
        self[exercise].create_test(seed)

    def remove_test(self, exercise, seed):
        """Remove test of ``exercise`` with ``seed``"""
        if exercise.__name__ not in self:
            return
        self[exercise].remove_test(seed)

    def __getitem__(self, key):
        if isinstance(key, type):
            return self.exercises[key.__name__]
        return self.exercises[key]

    def has_test(self, exercise, seed):
        """Return True iff there is a test to ``exercises`` with ``seed``."""
        if exercise.__name__ not in self:
            return False
        return self[exercise].has_test(seed)

    def read_testfile(self):
        """Read test files of exercises."""
        testfile_name = "{}.prt".format(os.path.join(*(
            pyromaths.__path__
            + [".."]
            + self.name.split('.')
            )))
        if os.access(testfile_name, os.R_OK):
            with codecs.open(testfile_name, "r", "utf8") as testfile:
                for exercise, seeds in json.loads(testfile.read()).items():
                    for seed in seeds:
                        self[exercise].add_seed(seed, seeds[seed])

    def write_testfile(self):
        """Write test files of exercises"""
        TODO(write)

    def add_exercise(self, exercise):
        """Add an exercise to the test suite."""
        if exercise.__name__ not in self:
            self.exercises[exercise.__name__] = TestExercise(exercise)

    def __iter__(self):
        return iter(self.exercises)

    def iter_tests(self):
        """Return an iterator over tests.

        The iterator iterates over :class:`unittest.TestCase` intances.
        """
        for exercise in self:
            for test in self[exercise].iter_tests():
                yield test

class TestExercise(Test):
    """Test of an exercise"""

    def __init__(self, exercise):
        super(TestExercise, self).__init__()
        self.exercise = exercise
        self.seeds = {}

    @property
    def name(self):
        """Name of the exercise.

        That is, name of the corresponding class.
        """
        return self.exercise.__name__

    @property
    def fullname(self):
        """Full name of the exercise.

        That is, module and name of the corresponding class.
        """
        return ".".join([
            self.exercise.__module__,
            self.exercise.__name__,
            ])

    def add_seed(self, seed, expected):
        """Add a test with a particular seed."""
        if int(seed) not in self:
            self.seeds[int(seed)] = create_exercise_test_case(
                self.exercise,
                seed,
                expected,
                )

    def remove_test(self, seed):
        """Remove the test with ``seed``.

        If no such test exists, silently return.
        """
        if seed in self.seeds:
            if ask_confirm("Delete test {}[{}]".format(self.fullname, seed)):
                del self.seeds[seed]

    def create_test(self, seed):
        """Create a test for ``seed``.

        If test already exists, replace it.
        """
        print "TODO Creating exo for {}[{}]".format(self.exercise, seed)
        try:
            if ask_confirm("Create"):
                TODO(WRITE)
        except ActionCancel:
            return

    def has_test(self, seed):
        """Return True iff there is a test for ``seed``."""
        return seed in self

    def __iter__(self):
        return iter(self.seeds)

    def iter_tests(self):
        """Return an iterator over tests.

        The iterator iterates over :class:`unittest.TestCase` intances.
        """
        for seed in self:
            yield self[seed]

    def __getitem__(self, key):
        return self.seeds[key]

def ask_confirm(message):
    """Ask a confirmation for some message.

    :rtype bool:
    :return: True iff user agreed (answered ``y``), False if user did not
        (answered ``n``).
    :raises ActionCancel: if user cancelled, for this case only.
    :raises ActionCancelAll: if user cancelled, for all casess.
    """
    while True:
        try:
            answer = raw_input("{} (y/n/c/C/?) [?]? ".format(message))
        except KeyboardInterrupt:
            answer = 'C'
        except EOFError:
            answer = 'C'
        if answer == 'y':
            return True
        elif answer == 'n':
            return False
        elif answer == 'c':
            raise ActionCancel()
        elif answer == 'C':
            print
            print "Cancelling… Changes were not saved."
            raise ActionCancelAll()
        print textwrap.dedent("""
            [y]es: accept.
            [n]o: reject.
            [c]ancel: just this case.
            [C]ancel: all cases (and lose changes made so far).
            """)

def create_exercise_test_case(exercise, seed, expected):
    """Return the `unittest.TestCase` for an exercise.

    :param TexExercise exercise: Exercise to test.
    :param int seed: Random seed to use to test exercise.
    :param dict expected: Expected output for the exercises.
    """
    random.seed(seed)
    exercise_instance = exercise()

    class _TestSeed(Test, unittest.TestCase):
        """Test an exercise, with a particular seed."""

        longMessage = True

        def __init__(self, seed):
            super(_TestSeed, self).__init__()
            self.seed = seed

        def runTest(self):
            """Perform test"""
            self.assertListEqual(
                exercise_instance.tex_statement(),
                expected['tex_statement'],
                )

            self.assertListEqual(
                exercise_instance.tex_answer(),
                expected['tex_answer'],
                )

        def compile(self):
            """Compile exercise (an produce a PDF file).

            :rvalue: string
            :returns: The path of the compiled file.
            """
            TODO(compile)

        def show(self):
            """Display exercise (compiling it before).

            The corresponding PDF is displayed in a PDF viewer.
            """
            TODO(show)

    return type(
        '{}.{}[{}]'.format(exercise.__module__, exercise.__name__, seed),
        (_TestSeed,),
        dict(_TestSeed.__dict__),
        )(seed)

def create_test_suite():
    """Gather all exercise tests in a :class:`TestPackage` intance."""
    ex.load()
    tests = TestPackage()
    for __level, exercises in ex.levels.iteritems():
        for exo in exercises:
            if ex.LegacyExercise in exo.__bases__:
                continue
            tests.add_exercise(exo)
    tests.read_testfiles()
    return tests

def simple_runtest(test):
    """Perform a single test, and return True iff it was successful."""
    return unittest.TextTestRunner().run(unittest.TestSuite([test])).wasSuccessful()

def load_tests(*args, **kwargs):
    """Return an `unittest.TestSuite` containing tests from all exercises."""
    suite = unittest.TestSuite()
    tests = create_test_suite()
    for test in tests.iter_tests():
        suite.addTest(test)
    return suite
