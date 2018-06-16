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

"""Exercice de seconde : Chapitre Second degré."""

import random

from pyromaths.ex import Jinja2Exercice
from pyromaths.outils.jinja2 import facteur

def signe(nombre):
    """Renvoit une chaîne contenant le signe de l'argument."""
    if nombre < 0:
        return "-"
    return "+"

class BilanTrinomeSansDiscriminant(Jinja2Exercice):

    description = u"Bilan sur les trinômes"
    level = u"2.Seconde"

    def __init__(self):
        super(BilanTrinomeSansDiscriminant, self).__init__()

        while True:
            a = float(random.choice([-1, 1]) * random.choice([0.5, 2]))
            x1 = float(random.choice([-1, 1]) * random.randint(2, 15))
            x2 = float(random.choice([-1, 1]) * random.randint(2, 15))

            b = -a * (x1 + x2)
            c = a * x1 * x2

            alpha = -b/(2*a)
            beta = a * (alpha**2) + b * alpha + c

            if alpha == 0 or beta == 0:
                continue
            if b == 0 or c == 0:
                continue
            if beta == c:
                continue

            break

        self.context = {
            "a": a,
            "b": b,
            "c": c,
            "x1": x1,
            "x2": x2,
            "alpha": alpha,
            "absalpha": abs(alpha), # Valeur absolue de alpha
            "signealpha": alpha/abs(alpha), # Signe de alpha (qui est non nul)
            "beta": beta,
            }

    @property
    def environment(self):
        environment = super(BilanTrinomeSansDiscriminant, self).environment
        environment.filters.update({
            'facteur': facteur,
            'min': min,
            'max': max,
            'abs': abs,
            'signe': signe,
            })
        return environment
