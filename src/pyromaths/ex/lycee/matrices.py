# Pyromaths
#
# Un programme en Python qui permet de créer des fiches d'exercices types de
# mathématiques niveau collège ainsi que leur corrigé en LaTeX.
#
# Copyright (C) 2018 -- Louis Paternault (spalax@gresille.org)
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
#

"""Exercice de Terminale ES, spécialité : Déterminer un état stable en utilisant un système."""
from __future__ import division
from __future__ import unicode_literals

from decimal import Decimal
import random

from pyromaths.ex import Jinja2Exercise
from pyromaths.outils.jinja2 import facteur, matrice

# Liste des coefficients de la diagonale de la matrice de transition qui
# donnent des états stables dont la valeur exacte a au plus trois décimales.
CANDIDATS = [
        [".45", ".3 "],
        [".5 ", ".25"],
        [".55", ".2 "],
        [".55", ".25"],
        [".6 ", ".15"],
        [".65", ".1 "],
        [".7 ", ".05"],
        [".7 ", ".1 "],
        [".7 ", ".5 "],
        [".7 ", ".55"],
        [".75", ".45"],
        [".8 ", ".4 "],
        [".8 ", ".7 "],
        [".85", ".4 "],
        [".85", ".55"],
        [".85", ".65"],
        [".85", ".75"],
        [".9 ", ".3 "],
        [".95", ".55"],
        [".95", ".65"],
        [".95", ".8 "],
        [".95", ".85"],
        ]


class EtatStableSysteme2(Jinja2Exercise):
    """Recherche d'état stable (avec un système)"""

    tags = ["Term ES"]

    def __init__(self):
        super().__init__()

        ab = random.choice(CANDIDATS)
        random.shuffle(ab)
        self.context = {
            "a": Decimal(ab[0]),
            "b": Decimal(ab[1]),
            }

    @property
    def environment(self):
        environment = super().environment
        environment.filters.update({
            'facteur': facteur,
            })
        return environment

class InterpolationMatrices(Jinja2Exercise):
    """Interpolation polynomiale en utilisant des matrices"""
    # Plus ou moins inspiré du sujet de bac ES Amérique du Nord, juin 2015.

    tags = ["Term ES"]

    def __init__(self):
        super().__init__()

        X = [None, None, None]
        while len(set(X)) != 3:
            X = sorted([
                random.randint(2, 9),
                random.randint(2, 9),
                random.randint(2, 9),
                ])

        a = b = c = 0
        while True:
            a = Decimal(random.choice([1, -1]) * random.randint(2, 19))
            b = Decimal(random.choice([1, -1]) * random.randint(2, 19))
            c = Decimal(random.choice([1, -1]) * random.randint(2, 19))

            if len(set([a, b, c])) != 3:
                continue
            if 10 in (abs(a), abs(b), abs(c)):
                continue
            break

        if random.randint(0, 1) == 1:
            a = a //  10
            b = b //  10
            c = c //  10

        M = [
            [X[0]**2, X[0], 1],
            [X[1]**2, X[1], 1],
            [X[2]**2, X[2], 1],
            ]
        Y = [
            a * X[0]**2 + b * X[0] + c,
            a * X[1]**2 + b * X[1] + c,
            a * X[2]**2 + b * X[2] + c,
            ]

        self.context = {
            "X": X,
            "Y": Y,
            "A": [a, b, c],
            "M": M,
            "x": random.randint(10, 19),
            }

    @property
    def environment(self):
        environment = super().environment
        environment.filters.update({
            'facteur': facteur,
            'matrice': matrice,
            'zip': zip,
            })
        return environment
