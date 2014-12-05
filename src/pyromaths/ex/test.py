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
import logging
import random
import shutil
import tempfile
import textwrap
import unittest

import pyromaths
from pyromaths import ex
from pyromaths.outils import System

# Logging configuration
logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger()


class ActionCancelAll(Exception):
    """Cancel an action by user input."""
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

    @property
    def _testfile_name(self):
        """Return the name of the file holding test results."""
        return "{}.prt".format(os.path.join(*(
            pyromaths.__path__
            + [".."]
            + self.name.split('.')
            )))

    def read_testfile(self):
        """Read test files of exercises."""
        if os.access(self._testfile_name, os.R_OK):
            if os.stat(self._testfile_name)[6] != 0: # File is not empty
                with codecs.open(self._testfile_name, "r", "utf8") as testfile:
                    for exercise, seeds in json.loads(testfile.read()).items():
                        for seed in seeds:
                            self[exercise].add_seed(int(seed), seeds[seed])

    def write_testfile(self):
        """Write test files of exercises"""
        with codecs.open(self._testfile_name, "w", "utf8") as testfile:
            json.dump(
                self.dictionary(),
                testfile,
                ensure_ascii=False,
                sort_keys=True,
                indent=4,
                )

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

    def dictionary(self):
        """Return a ``dict`` version of ``self``, suitable for json encoding.
        """
        return dict([
            (name, exercise.dictionary())
            for name, exercise
            in self.exercises.items()
            ])

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

    def add_seed(self, seed, expected=None):
        """Add a test with a particular seed.

        :param dict expected: The expected result, as a dictionray with keys
            ``tex_statement`` and ``tex_answer``. If omitted, a
            :class:`WIPTestSeed` is used, which does not inherit from
            :class:`unittest.TestCase`, and represent a test which is being
            produced: its expected output is not known yet.
        """
        if expected:
            self.seeds[int(seed)] = create_exercise_test_case(
                self.exercise,
                seed,
                expected,
                )
        else:
            self.seeds[int(seed)] = WIPTestSeed(
                self.exercise,
                seed,
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
        LOGGER.info("Creating test for {}[{}]".format(self.exercise, seed))
        self.add_seed(seed)
        self[seed].show()
        if ask_confirm("Is the test valid"):
            self.add_seed(seed, self[seed].generate())

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

    def dictionary(self):
        """Return a ``dict`` version of ``self``, suitable for json encoding."""
        return dict([
            (seed, test.dictionary())
            for seed, test in self.seeds.items()
            if isinstance(test, unittest.TestCase)
            ])

def ask_confirm(message):
    """Ask a confirmation for some message.

    :rtype bool:
    :return: True iff user agreed (answered ``y``), False if user did not
        (answered ``n``).
    :raises ActionCancelAll: if user cancelled, for all casess.
    """
    while True:
        try:
            answer = raw_input("{} (y/n/c/?) [?]? ".format(message))
        except KeyboardInterrupt:
            answer = 'c'
        except EOFError:
            answer = 'c'
        if answer == 'y':
            return True
        elif answer == 'n':
            return False
        elif answer == 'c':
            print
            LOGGER.warning("Cancelling… Changes were not saved.")
            raise ActionCancelAll()
        print textwrap.dedent("""
            [y]es: accept.
            [n]o: reject.
            [c]ancel: just this case.
            [C]ancel: all cases (and lose changes made so far).
            """)

class WIPTestSeed(Test):
    """Test in progress: expected output is not known yet."""

    _tempdir = None

    def __init__(self, exercise, seed):
        super(WIPTestSeed, self).__init__()

        self.seed = seed
        random.seed(seed)

        self.exercise = exercise
        self.exercise_instance = exercise()

    @property
    def tempdir(self, *args, **kwargs):
        """Return a temporary directory for this file, creating it if necessary

        This directory will be removed when ``self`` is deleted.
        """
        if self._tempdir is None:
            self._tempdir = tempfile.mkdtemp(*args, **kwargs)
        return self._tempdir

    def __del__(self):
        if self._tempdir is not None:
            shutil.rmtree(self._tempdir)
        if hasattr(super(WIPTestSeed, self), "__del__"):
            super(WIPTestSeed, self).__del__()

    def compile(self, openpdf=0, movefile=False):
        """Compile exercise (an produce a PDF file).

        :rvalue: string
        :returns: The path of the compiled file.
        """
        random.seed(self.seed)

        old_dir = os.path.abspath(os.getcwd())
        System.creation({
            'creer_pdf': True,
            'creer_unpdf': True,
            'titre': u"Fiche de révisions",
            'corrige': True,
            'niveau': "test",
            'nom_fichier': u'test.tex',
            'chemin_fichier': self.tempdir,
            'fiche_exo': os.path.join(self.tempdir, 'exercices.tex'),
            'fiche_cor': os.path.join(self.tempdir, 'exercices-corrige.tex'),
            'datadir': pyromaths.Values.data_dir(),
            'configdir': pyromaths.Values.configdir(),
            'modele': 'pyromaths.tex',
            'liste_exos': [self.exercise_instance],
            'les_fiches': pyromaths.Values.LESFICHES,
            'openpdf': openpdf,
        })
        os.chdir(old_dir)

        if movefile:
            destname = "{}.{}-{}.pdf".format(
                self.exercise.__module__,
                self.exercise.__name__,
                self.seed,
                )
            shutil.move(
                os.path.join(self.tempdir, 'exercices.pdf'),
                destname,
            )
        else:
            destname = os.path.join(self.tempdir, 'exercices.pdf')

        return destname

    def show(self):
        """Display exercise (compiling it before).

        The corresponding PDF is displayed in a PDF viewer.
        """
        self.compile(openpdf=1)

    def generate(self):
        """Return the expected statement and answer, as a dictionary.
        """
        return {
            "tex_statement": self.exercise_instance.tex_statement(),
            "tex_answer": self.exercise_instance.tex_answer(),
            }

def create_exercise_test_case(exercise, seed, expected):
    """Return the `unittest.TestCase` for an exercise.

    :param TexExercise exercise: Exercise to test.
    :param int seed: Random seed to use to test exercise.
    :param dict expected: Expected output for the exercises.
    """
    class _TestSeed(WIPTestSeed, unittest.TestCase):
        """Test an exercise, with a particular seed."""

        longMessage = True

        def __init__(self, seed):
            super(_TestSeed, self).__init__(exercise, seed)

        def runTest(self):
            """Perform test"""
            self.assertListEqual(
                self.exercise_instance.tex_statement(),
                expected['tex_statement'],
                )

            self.assertListEqual(
                self.exercise_instance.tex_answer(),
                expected['tex_answer'],
                )

        @staticmethod
        def dictionary():
            """Return a ``dict`` version of ``self``, for json encoding."""
            return expected

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
    testrunner = unittest.TextTestRunner()
    return testrunner.run(unittest.TestSuite([test])).wasSuccessful()

def load_tests(*__args, **__kwargs):
    """Return an `unittest.TestSuite` containing tests from all exercises."""
    suite = unittest.TestSuite()
    tests = create_test_suite()
    for test in tests.iter_tests():
        suite.addTest(test)
    return suite
