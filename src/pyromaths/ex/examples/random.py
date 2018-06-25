# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
# -*- coding: utf-8 -*-
import random
import textwrap

from pyromaths import ex

class _RandomHelloWorld(ex.TexExercise):
    """Exemple RandomHelloWorld"""

    tags = ["exemple"]

    def __init__(self):
        self.times = random.randint(2, 10)

    def tex_statement(self):
        return ['\\exercice', '%u times hello, World!' % self.times]

    def tex_answer(self):
        return ['\\exercice*', '%u times goodbye, World!' % self.times]
