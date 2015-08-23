#!/usr/bin/python
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

"""Test of exercises.

This module gather tests from all exercises. Running:

    python -m unittest discover

does just as expected.
"""

import codecs
import glob
import logging
import os
import random
import shutil
import tempfile
import unittest

import pyromaths
from pyromaths.outils import System

# Logging configuration
logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger()

def load_tests(*__args, **__kwargs):
    """Return an `unittest.TestSuite` containing tests from all exercises."""
    tests = TestPerformer()
    return tests.as_unittest_suite([
        (exo, tests.get_tested_seeds(exo))
        for exo in tests.iter_id()
        ])

class TestException(Exception):
    """Generic exception for this module."""
    pass

class ExerciseNotFound(TestException):
    """Name of exercise cannot be found in known exercises."""

    def __init__(self, exercise):
        super(ExerciseNotFound, self).__init__()
        self.exercise = exercise

    def __str__(self):
        return "Exercise '{}' not found.".format(self.exercise)

def test_path(dirlevel, name, seed, choice):
    """Return the path of file containing expected test result."""
    return os.path.join(
        pyromaths.Values.data_dir(),
        'ex',
        dirlevel,
        'tests',
        "%s.%s.%s" % (name, seed, choice)
        )

class TestExercise(object):
    """Test of an exercise"""

    def __init__(self, exercise, seed):
        self.exercise = exercise
        self.seed = seed

    def show(self):
        """Compile exercise, and display its result."""
        self.compile(openpdf=1)

    def get_exercise(self):
        """Return an instanciated exercise."""
        random.seed(self.seed)
        return self.exercise()

    def compile(self, openpdf=0, movefile=False, pipe=None):
        """Compile exercise"""
        tempdir = tempfile.mkdtemp()

        old_dir = os.path.abspath(os.getcwd())
        System.creation({
            'creer_pdf': True,
            'creer_unpdf': True,
            'titre': u"Fiche de révisions",
            'corrige': True,
            'niveau': "test",
            'nom_fichier': u'test.tex',
            'chemin_fichier': tempdir,
            'fiche_exo': os.path.join(tempdir, 'exercises.tex'),
            'fiche_cor': os.path.join(tempdir, 'exercises-corrige.tex'),
            'datadir': pyromaths.Values.data_dir(),
            'configdir': pyromaths.Values.configdir(),
            'modele': 'pyromaths.tex',
            'liste_exos': [self.get_exercise()],
            'les_fiches': pyromaths.Values.lesfiches(),
            'openpdf': openpdf,
            'pipe': pipe,
        })
        os.chdir(old_dir)

        if movefile:
            destname = "{}-{}.pdf".format(
                self.exercise.id(),
                self.seed,
                )
            shutil.move(
                os.path.join(tempdir, 'exercises.pdf'),
                destname,
            )
        else:
            destname = os.path.join(tempdir, 'exercises.pdf')

        return destname

    def test_path(self, name):
        """Return the path of the file containing expected results."""
        return test_path(
            self.exercise.dirlevel,
            self.exercise.name(),
            self.seed,
            name,
            )

    def write(self):
        """Write expected test results."""
        exo = self.get_exercise()
        with codecs.open(self.test_path("statement"), "w", "utf8") as statement:
            statement.write(u"\n".join(exo.tex_statement()))
        with codecs.open(self.test_path("answer"), "w", "utf8") as answer:
            answer.write(u"\n".join(exo.tex_answer()))

    def read(self, choice):
        """Read expected test result."""
        with codecs.open(self.test_path(choice), "r", "utf8") as file:
            return file.read()

    def remove(self):
        """Remove test"""
        os.remove(self.test_path("statement"))
        os.remove(self.test_path("answer"))

    def changed(self):
        """Return `True` iff exercise has changed."""
        exo = self.get_exercise()
        if "\n".join(exo.tex_statement()) != self.read('statement'):
            return True
        if "\n".join(exo.tex_answer()) != self.read('answer'):
            return True
        return False

class UnittestExercise(unittest.TestCase):
    """Test an exercise, with a particular seed."""

    def __init__(self, test):
        super(UnittestExercise, self).__init__()
        self.test = test

    def runTest(self):
        """Perform test"""
        exo = self.test.get_exercise()

        self.assertListEqual(
            exo.tex_statement(),
            self.test.read('statement').split("\n"),
            )

        self.assertListEqual(
            exo.tex_answer(),
            self.test.read('answer').split("\n"),
            )

class TestPerformer(object):
    """Perform tests over every exercises"""

    def __init__(self):
        self.exercises = {}
        levels = pyromaths.ex.load_levels()
        for level in levels:
            for exercise in levels[level]:
                self.exercises[exercise.id()] = exercise

    def iter_id(self):
        """Iterate over exercise ids."""
        return self.exercises.keys()

    def get(self, exercise, seed):
        """Return the `TestExercise` object corresponding to the arguments."""
        if exercise not in self.exercises:
            raise KeyError(exercise)
        return TestExercise(self.exercises[exercise], seed)

    def get_tested_seeds(self, exercise):
        """Return seeds that are tested for this exercise"""
        if exercise not in self.exercises:
            raise ExerciseNotFound(exercise)
        statement_seeds = [
            os.path.basename(path).split(".")[1]
            for path in glob.glob(test_path(
                self.exercises[exercise].dirlevel,
                self.exercises[exercise].name(),
                '*',
                'statement'
                ))
            ]
        for seed in statement_seeds:
            if os.path.exists(test_path(
                    self.exercises[exercise].dirlevel,
                    self.exercises[exercise].name(),
                    seed,
                    'answer',
                )):
                yield int(seed)

    def iter_missing(self):
        """Iterate over exercises that are not tested."""
        for exercise in self.exercises:
            if not list(self.get_tested_seeds(exercise)):
                yield exercise

    def as_unittest_suite(self, exercises):
        """Return the tests, as a `unittest.TestSuite`."""
        suite = unittest.TestSuite()
        for exercise, seeds in exercises:
            for seed in seeds:
                suite.addTest(UnittestExercise(self.get(exercise, seed)))
        return suite
