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

import random, math, string
#import outils.Arithmetique
import ExoPolynome

def tex_racines_degre2(f0,f1):
    f0.write('\\exercice\n')
    f1.write('\\exercice*\n')
    exo,cor=ExoPolynome.exo_racines_degre2()
    f0.write(exo)
    f1.write(cor)


def tex_factorisation(f0,f1):
    f0.write('\\exercice\n')
    f1.write('\\exercice*\n')
    exo,cor=ExoPolynome.Exo_factorisation()
    f0.write(exo)
    f1.write(cor)
    
def tex_factorisation_degre3(f0,f1):
    f0.write('\\exercice\n')
    f1.write('\\exercice*\n')
    exo,cor=ExoPolynome.Exo_factorisation_degre3()
    f0.write(exo)
    f1.write(cor)


def main(exo, f0, f1):
    modules = (
        tex_racines_degre2,
        tex_factorisation,
        tex_factorisation_degre3,
        )

    modules[exo](f0, f1)
