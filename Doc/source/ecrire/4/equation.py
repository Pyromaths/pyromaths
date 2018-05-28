# -*- coding: utf-8 -*-
#
# Pyromaths
#
# Un programme en Python qui permet de créer des fiches d'exercices types de
# mathématiques niveau collège ainsi que leur corrigé en LaTeX.
#
# Copyright (C) 2018 -- Jérôme Ortais (jerome.ortais@pyromaths.org)
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

"""Équations du premier degré"""

import random

from pyromaths.ex import Jinja2Exercice
from pyromaths.outils.decimaux import decimaux, suppr0

class EquationPremierDegre(Jinja2Exercice):

    description = u"Résolution d'équations du premier degré à coefficients entiers."
    level = u'3.Troisième'

    def __init__(self):
        super(EquationPremierDegre, self).__init__()

        self.context = {
            "a": random.choice([1, -1]) * (random.choice(range(1, 10))),
            "b": random.choice([1, -1]) * (random.choice(range(1, 10))),
            "c": random.choice([1, -1]) * (random.choice(range(1, 10))),
            "d": random.choice([1, -1]) * (random.choice(range(1, 10))),
            }

    @property
    def environment(self):
        environment = super(EquationPremierDegre, self).environment
        environment.filters.update({
            'decimaux': decimaux,
            'suppr0': suppr0,
            })
        return environment
