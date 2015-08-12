import unittest

import pyromaths

class UniqueName(unittest.TestCase):

    def test_uniquename(self):
        """Check that in each level, exercice names are unique"""

        levels = pyromaths.ex.load_levels()
        for level in levels:
            names = []
            for exercice in levels[level]:
                if issubclass(exercice, pyromaths.ex.LegacyExercise):
                    names.append(exercice.function[0].__name__)
                else:
                    names.append(exercice.__name__)
            self.assertEqual(len(names), len(set(names)))
