#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Pyromaths
# Un programme en Python qui permet de créer des fiches d'exercices types de
# mathématiques niveau collège ainsi que leur corrigé en LaTeX.
# Copyright (C) 2006 -- Jérôme Ortais (jerome.ortais@pyromaths.org)
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

import quatriemes.puissances, quatriemes.developpements
import quatriemes.calcul_mental, quatriemes.fractions
import quatriemes.geometrie

def write(f0, f1, exos):
    f0.write("\n")
    f1.write("\n")
    f0.writelines(x + "\n" for x in exos[0])
    f1.writelines(x + "\n" for x in exos[1])

def main(exo, f0, f1):
    modules = (
        quatriemes.calcul_mental.main,
        quatriemes.fractions.exo_sommes_fractions,
        quatriemes.fractions.exo_produits_fractions,
        quatriemes.fractions.exo_priorites_fractions,
        quatriemes.puissances.tex_proprietes,
        quatriemes.puissances.tex_proprietes_neg,
        quatriemes.puissances.ecr_sc,
        quatriemes.puissances.exo_puissances,
        quatriemes.developpements.exo_distributivite,
        quatriemes.developpements.exo_double_distributivite,
        quatriemes.geometrie.exo_pythagore,
        quatriemes.geometrie.exo_reciproque_pythagore,
        quatriemes.geometrie.exo_triangle_cercle,
        quatriemes.geometrie.exo_thales,
        quatriemes.geometrie.exo_trigo,
        )
    write(f0, f1, modules[exo]())

