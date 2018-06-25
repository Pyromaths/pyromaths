# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from pyromaths import ex

class _HelloWorld(ex.TexExercise):
    """Exemple d'exercice"""

    # Supprimer le tiret bas _ pour « activer » l'exercice.

    tags = ["exemple"]

    def tex_statement(self):
        return ['\\exercice', 'Hello, world!']

    def tex_answer(self):
        return ['\\exercice*', _('Hello, world corrigé!')]
