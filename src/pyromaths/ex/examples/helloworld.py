import random

from pyromaths import ex

class HelloWorld(ex.TexExercise):
    """Exemple d'exercice"""

    # Supprimer le tiret bas _ pour « activer » l'exercice.

    tags = ["exemple"]

    def tex_statement(self):
        return ['\\exercice', 'Hello, world!']

    def tex_answer(self):
        return ['\\exercice*', _('Hello, world corrigé!')]

class RandomHelloWorld(ex.TexExercise):
    """Exemple RandomHelloWorld"""

    tags = ["exemple"]

    def __init__(self):
        self.times = random.randint(2, 10)

    def tex_statement(self):
        return ['\\exercice', '%u times hello, World!' % self.times]

    def tex_answer(self):
        return ['\\exercice*', '%u times goodbye, World!' % self.times]
