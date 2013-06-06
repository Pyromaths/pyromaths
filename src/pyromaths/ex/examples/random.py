# -*- coding: utf-8 -*-
import random
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
