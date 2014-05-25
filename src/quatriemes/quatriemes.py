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

from . import puissances, developpements, calcul_mental, fractions, geometrie
from . import litteral

def write(f0, f1, exos):
    f0.write("\n")
    f1.write("\n")
    f0.writelines(x + "\n" for x in exos[0])
    f1.writelines(x + "\n" for x in exos[1])

def main(exo, f0, f1):
    modules = (
        calcul_mental.main,
        fractions.exo_sommes_fractions,
        fractions.exo_produits_fractions,
        fractions.exo_priorites_fractions,
        litteral.reduire,
        litteral.reduire_expressions, 
        puissances.tex_proprietes,
        puissances.tex_proprietes_neg,
        puissances.ecr_sc,
        puissances.exo_puissances,
        developpements.exo_distributivite,
        developpements.exo_double_distributivite,
        geometrie.exo_pythagore,
        geometrie.exo_reciproque_pythagore,
        geometrie.exo_triangle_cercle,
        geometrie.exo_thales,
        geometrie.exo_trigo,
        )
    write(f0, f1, modules[exo]())

