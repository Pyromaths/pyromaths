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
import unittest

from pyromaths import ex

def fullclassname(argument):
    """Return the full name of a python object.

    That is, return its module name followed by its class name.
    """
    return "{}.{}".format(
        argument.__module__,
        argument.__class__.__name__,
        )

def create_exercice_test_case(exercice, seed):
    """Return the `unittest.TestCase` for an exercise.

    :param TexExercise exercice: Exercise to test.
    :param int seed: Random seed to use to test exercise.
    """

    class _ExerciceTestCase(unittest.TestCase):
        """Test case for an exercise."""

        longMessage = True

        def runTest(self):
            self.assertMultiLineEqual(
                "\n".join(exercice.tex_statement()),
                exercice.tests[seed]['tex_statement'].strip(),
                )

            self.assertMultiLineEqual(
                "\n".join(exercice.tex_answer()),
                exercice.tests[seed]['tex_answer'].strip(),
                )

    return type(
        '{}.tests[{}]'.format(fullclassname(exercice), seed),
        (_ExerciceTestCase,),
        dict(_ExerciceTestCase.__dict__),
        )()

def create_named_test_suite(name):
    """Return an `unittest.TestSuite`, having name `name`."""

    class _NamedTestSuite(unittest.TestSuite):
        """Named `unittest.TestSuite`."""

        def shortDescription(self):
            return u"Testing {}".format(name)

        def id(self):
            return name

    return type(
        unidecode.unidecode(u'TestSuite({})'.format(name)),
        (_NamedTestSuite,),
        dict(_NamedTestSuite.__dict__)
        )()

def load_tests(*args, **kwargs):
    """Return an `unittest.TestSuite` containing tests from all exercises."""
    ex.load()
    suite = unittest.TestSuite()
    for level, exercices in ex.levels.iteritems():
        level_suite = create_named_test_suite(level)
        for exo in exercices:
            if hasattr(exo, 'tests'):
                exo_suite = create_named_test_suite(fullclassname(exo))
                for seed in exo.tests.keys():
                    random.seed(seed)
                    exo_suite.addTest(create_exercice_test_case(exo(), seed))
                level_suite.addTest(exo_suite)
        suite.addTest(level_suite)

    return suite

