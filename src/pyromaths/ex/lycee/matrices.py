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
import random

from pyromaths.outils.decimaux import decimaux
from pyromaths.ex import Jinja2Exercice

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
    level = u"0.TermES"

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
            'decimal': decimaux,
            })
        return environment
