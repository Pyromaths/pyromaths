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

import random
import unidecode
import json
import os
import textwrap
import codecs
import unittest

import pyromaths
from pyromaths import ex

def fullclassname(argument):
    """Return the full name of a python object.

    That is, return its module name followed by its class name.
    """
    return "{}.{}".format(
        argument.__module__,
        argument.__class__.__name__,
        )

class Test(object):
    pass

class TestPackage(Test):

    def __init__(self):
        super(TestPackage, self).__init__()
        self.modules = {}

    def read_testfiles(self):
        for module in self:
            self[module].read_testfile()

    def write_testfiles(self):
        for module in self:
            self[module].write_testfile()

    def add_exercise(self, exercise):
        self.add_module(exercise.__module__)
        self[exercise.__module__].add_exercise(exercise)

    def add_module(self, modulename):
        if modulename not in self:
            self.modules[modulename] = TestModule(modulename)

    def get_exercise(self, exercise):
        return self[exercise.__module__][exercise.__name__]

    def has_test(self, exercise, seed):
        if exercise.__module__ not in self:
            return False
        return self[exercise.__module__].has_test(exercise, seed)

    def create_test(self, exercise, seed):
        self.add_module(exercise.__module__)
        self[exercise.__module__].create_test(exercise, seed)

    def remove_test(self, exercise, seed):
        if exercise.__module__ not in self:
            return
        self[exercise.__module__].remove_test(exercise, seed)

    def __iter__(self):
        return iter(self.modules)

    def __getitem__(self, key):
        return self.modules[key]

    def iter_tests(self):
        for module in self:
            for test in self[module].iter_tests():
                yield test

class TestModule(Test):

    def __init__(self, name):
        super(TestModule, self).__init__()
        self.name = name
        self.exercises = {}

    def create_test(self, exercise, seed):
        self.add_exercise(exercise)
        self[exercise].create_test(seed)

    def remove_test(self, exercise, seed):
        if exercise.__name__ not in self:
            return
        self[exercise].remove_test(seed)

    def __getitem__(self, key):
        if isinstance(key, type):
            return self.exercises[key.__name__]
        return self.exercises[key]

    def has_test(self, exercise, seed):
        if exercise.__name__ not in self:
            return False
        return self[exercise].has_test(seed)

    def read_testfile(self):
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
        TODO(write)

    def add_exercise(self, exercise):
        if exercise.__name__ not in self:
            self.exercises[exercise.__name__] = TestExercise(exercise)

    def __iter__(self):
        return iter(self.exercises)

    def iter_tests(self):
        for exercise in self:
            for test in self[exercise].iter_tests():
                yield test

class TestExercise(Test):

    def __init__(self, exercise):
        super(TestExercise, self).__init__()
        self.exercise = exercise
        self.seeds = {}

    @property
    def name(self):
        return self.exercise._name__

    @property
    def fullname(self):
        return ".".join([
                self.exercise.__module__,
                self.exercise.__name__,
                ])

    def add_seed(self, seed, expected):
        if int(seed) not in self:
            self.seeds[int(seed)] = create_exercise_test_case(self.exercise, seed, expected)

    def remove_test(self, seed):
        if seed in self.seeds:
            if ask_confirm("Delete test {}[{}]".format(self.fullname, seed)):
                del self.seeds[seed]

    def create_test(self, seed):
        print("TODO Creating exo for {}[{}]".format(self.exercise, seed))
        if ask_confirm("Create"):
            TODO(WRITE)

    def has_test(self, seed):
        return seed in self

    def __iter__(self):
        return iter(self.seeds)

    def iter_tests(self):
        for seed in self:
            yield self[seed]

    def __getitem__(self, key):
        return self.seeds[key]

def ask_confirm(message):
    while True:
        answer = raw_input("{} (y/n/c/C/?) [?]? ".format(message))
        if answer == 'y':
            return True
        elif answer == 'n':
            return False
        elif answer == 'c':
            raise ActionAbort()
        elif answer == 'C':
            raise ActionAbortAll()
        print(textwrap.dedent("""
        [y]es: accept.
        [n]o: reject.
        [c]ancel: just this case.
        [C]ancel: all cases.
        """))

def create_exercise_test_case(exercise, seed, expected):
    """Return the `unittest.TestCase` for an exercise.

    :param TexExercise exercise: Exercise to test.
    :param int seed: Random seed to use to test exercise.
    :param dict expected: Expected output for the exercises.
    """
    random.seed(seed)
    exercise_instance = exercise()

    class _TestSeed(Test, unittest.TestCase):

        longMessage = True

        def __init__(self, seed):
            super(_TestSeed, self).__init__()
            self.seed = seed

        def runTest(self):
            self.assertListEqual(
                exercise_instance.tex_statement(),
                expected['tex_statement'],
                )

            self.assertListEqual(
                exercise_instance.tex_answer(),
                expected['tex_answer'],
                )

        def compile(self):
            TODO(compile)

        def show(self):
            TODO(show)

    return type(
        '{}.{}[{}]'.format(exercise.__module__, exercise.__name__, seed),
        (_TestSeed,),
        dict(_TestSeed.__dict__),
        )(seed)

def create_test_dictionary():
    ex.load()
    tests = TestPackage()
    for level, exercises in ex.levels.iteritems():
        for exo in exercises:
            if ex.__LegacyExercise in exo.__bases__:
                continue
            tests.add_exercise(exo)
    tests.read_testfiles()
    return tests

def simple_runtest(test):
    unittest.TextTestRunner().run(unittest.TestSuite([test]))

def load_tests(*args, **kwargs):
    """Return an `unittest.TestSuite` containing tests from all exercises."""
    suite = unittest.TestSuite()
    tests = create_test_dictionary()
    for test in tests.iter_tests():
        suite.addTest(test)
    return suite
