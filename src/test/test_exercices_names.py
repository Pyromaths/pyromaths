from __future__ import unicode_literals
import unittest

import pyromaths

class UniqueName(unittest.TestCase):

    def test_uniquename(self):
        """Check that in each level, exercice names are unique"""

        levels = pyromaths.ex.load_levels()
        for level in levels:
            names = [exo.name for exo in levels[level]]
        self.assertEqual(len(names), len(set(names)))
