# -*- coding: utf-8 -*-
import random
import textwrap

from pyromaths import ex

class RandomHelloWorld(ex.TexExercise):

    # Un-comment to show this exercise:
#    description = u'Exemple RandomHelloWorld'

    def __init__(self):
        self.times = random.randint(2, 10)

    def tex_statement(self):
        return ['\\exercice', '%u times hello, World!' % self.times]

    def tex_answer(self):
        return ['\\exercice*', '%u times goodbye, World!' % self.times]

    tests = {
            0: {
                'tex_statement': """Here comes the expected output of tex_statement() with random seed 0.""",
                'tex_statement': """Here comes the expected output of tex_answer() with random seed 0.""",
                },
            }
