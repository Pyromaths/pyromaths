# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from pyromaths import ex

class HelloWorld(ex.TexExercise):

    # Un-comment to show this exercise:
#    description = u'Exemple HelloWorld'

    def tex_statement(self):
        return ['\\exercice', 'Hello, world!']

    def tex_answer(self):
        return ['\\exercice*', _('Hello, world corrigé!')]
