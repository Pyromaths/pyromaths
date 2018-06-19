# -*- coding: utf-8 -*-
#
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

from past.utils import old_div
import decimal
import random

from pyromaths.ex import Jinja2Exercice
from pyromaths.outils.jinja2 import facteur, matrice

# Liste des coefficients de la diagonale de la matrice de transition qui
# donnent des états stables dont la valeur exacte a au plus trois décimales.
CANDIDATS = [
        [.45, .30],
        [.50, .25],
        [.55, .20],
        [.55, .25],
        [.60, .15],
        [.65, .10],
        [.70, .05],
        [.70, .10],
        [.70, .50],
        [.70, .55],
        [.75, .45],
        [.80, .40],
        [.80, .70],
        [.85, .40],
        [.85, .55],
        [.85, .65],
        [.85, .75],
        [.90, .30],
        [.95, .55],
        [.95, .65],
        [.95, .80],
        [.95, .85],
        ]


class EtatStableSysteme2(Jinja2Exercice):

    description = u"Recherche d'état stable (avec un système)"
    level = u"0.Term ES"

    def __init__(self):
        super(EtatStableSysteme2, self).__init__()

        ab = random.choice(CANDIDATS)
        random.shuffle(ab)
        self.context = {
            "a": ab[0],
            "b": ab[1],
            }

    @property
    def environment(self):
        environment = super(EtatStableSysteme2, self).environment
        environment.filters.update({
            'facteur': facteur,
            })
        return environment

class InterpolationMatrices(Jinja2Exercice):
    # Plus ou moins inspiré du sujet de bac ES Amérique du Nord, juin 2015.

    description = u"Interpolation polynomiale en utilisant des matrices"
    level = u"0.Term ES"

    def __init__(self):
        super(InterpolationMatrices, self).__init__()

        X = [None, None, None]
        while len(set(X)) != 3:
            X = sorted([
                random.randint(2, 9),
                random.randint(2, 9),
                random.randint(2, 9),
                ])

        a = b = c = 0
        while True:
            a = decimal.Decimal(random.choice([1, -1]) * random.randint(2, 19))
            b = decimal.Decimal(random.choice([1, -1]) * random.randint(2, 19))
            c = decimal.Decimal(random.choice([1, -1]) * random.randint(2, 19))

            if len(set([a, b, c])) != 3:
                continue
            if 10 in (abs(a), abs(b), abs(c)):
                continue
            break

        if random.randint(0, 1) == 1:
            a = old_div(a, 10)
            b = old_div(b, 10)
            c = old_div(c, 10)

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
        environment = super(InterpolationMatrices, self).environment
        environment.filters.update({
            'facteur': facteur,
            'matrice': matrice,
            'zip': zip,
            })
        return environment
