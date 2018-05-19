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
import gettext
import glob
import logging
import os
import random
import shutil
import tempfile
import unittest

# Quick and dirty definition of `_` as the identity function
gettext.install('pyromaths', unicode=1)

import pyromaths
from pyromaths.outils import System
from pyromaths.cli import PyromathsException

# Logging configuration
logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger()

def load_tests(*__args, **__kwargs):
    """Return an `unittest.TestSuite` containing tests from all exercises."""
    tests = TestPerformer()
    return tests.as_unittest_suite([
        (exo, tests.get_tested_seeds(exo))
        for exo in tests.iter_names()
        ])

class ExerciseNotFound(PyromathsException):
    """Name of exercise cannot be found in known exercises."""

    def __init__(self, exercise):
        super(ExerciseNotFound, self).__init__()
        self.exercise = exercise

    def __str__(self):
        return "Exercise '{}' not found.".format(self.exercise)

def test_path(name, seed, choice):
    """Return the path of file containing expected test result."""
    return os.path.join(
        pyromaths.Values.data_dir(),
        'ex',
        'tests',
        "%s.%s.%s" % (name, seed, choice)
        )

def generate(exercise_list, openpdf=False, destname=None, pipe=None):
    """Generate exercise list as a pdf, and return the resulting pdf name.

    :param openpdf: Open pdf at the end of compilation.
    :param str destname: Destination name (use ``None`` to use the default name).
    :param list pipe: List of commands executed on the tex file before compilation.
    """
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
        'liste_exos': exercise_list,
        'les_fiches': pyromaths.Values.lesfiches(),
        'openpdf': openpdf,
        'pipe': pipe,
    })
    os.chdir(old_dir)

    if destname:
        shutil.move(
            os.path.join(tempdir, 'exercises.pdf'),
            destname,
        )
    else:
        destname = os.path.join(tempdir, 'exercises.pdf')

    return destname

class TestExercise(object):
    """Test of an exercise"""

    def __init__(self, exercise, seed):
        self.exercise = exercise
        self.seed = seed

    def show(self):
        """Generate exercise, and display its result."""
        self.generate(openpdf=1)

    def get_exercise(self):
        """Return an instanciated exercise."""
        random.seed(self.seed)
        return self.exercise()

    def generate(self, openpdf=0):
        """Generate exercise"""
        return generate([self.get_exercise()], openpdf=openpdf)

    def test_path(self, name):
        """Return the path of the file containing expected results."""
        return test_path(
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
        with codecs.open(self.test_path(choice), "r", "utf8") as result:
            return result.read()

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

    maxDiff = None

    def __init__(self, exercise=None):
        super(UnittestExercise, self).__init__()
        self.exercise = exercise

    def shortDescription(self):
        if self.exercise is None:
            return super(UnittestExercise, self).shortDescription()
        else:
            return self.exercise.exercise.name()

    def runTest(self):
        """Perform test"""
        exo = self.exercise.get_exercise()

        self.assertEqual(
            u"\n".join(exo.tex_statement()),
            self.exercise.read('statement'),
            )

        self.assertEqual(
            u"\n".join(exo.tex_answer()),
            self.exercise.read('answer'),
            )

class TestPerformer(object):
    """Perform tests over every exercises"""

    def __init__(self):
        self.exercises = {}
        levels = pyromaths.ex.load_levels()
        for level in levels:
            for exercise in levels[level]:
                self.exercises[exercise.name()] = exercise

    def iter_names(self):
        """Iterate over exercise names."""
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
                self.exercises[exercise].name(),
                '*',
                'statement'
                ))
            ]
        for seed in statement_seeds:
            if os.path.exists(test_path(
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
                suite.addTest(UnittestExercise(exercise=self.get(exercise, seed)))
        return suite
