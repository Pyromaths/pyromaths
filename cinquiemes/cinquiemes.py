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

import priorites
import symetrie
import fractions
import reperage
from outils import tex_entete
from pyro_classes import WriteFiles
import os.path

def write(f, exos):
    f.write("\n")
    f.writelines(x + "\n" for x in exos[0])

def main(exo,f0, f1):
    modules = (priorites.main, symetrie.main, fractions.fractions_egales,
               fractions.sommes_fractions, fractions.produits_fractions,reperage.main)
    write(f0, modules[exo]())
    write(f1, modules[exo]())


	    