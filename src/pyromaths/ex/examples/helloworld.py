import random

from pyromaths import ex

class _HelloWorld(ex.TexExercise):
    """Exemple d'exercice"""

    # Supprimer le tiret bas _ pour « activer » l'exercice.

    tags = ["exemple"]

    def tex_statement(self):
        return r"""
            \exercice
            Hello, world!
            """

    def tex_answer(self):
        return r"""
            \exercice*
            Hello, world corrigé !
            """

class _RandomHelloWorld(ex.TexExercise):
    """Exemple RandomHelloWorld"""

    tags = ["exemple"]

    def __init__(self):
        self.times = random.randint(2, 10)

    def tex_statement(self):
        return r"""
            \exercice
            {} times hello, World!
            """.format(self.times)

    def tex_answer(self):
        return r"""
            \exercice*
            {} times goodbye, World!
            """.format(self.times)
