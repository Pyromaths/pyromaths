# -*- coding: utf-8 -*-
#
# Pyromaths
#
# Un programme en Python qui permet de créer des fiches d'exercices types de
# mathématiques niveau collège ainsi que leur corrigé en LaTeX.
#
# Copyright (C) 2018 -- Louis Paternault (spalax+python@gresille.org)
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
from pyromaths.outils.jinja2 import facteur

class EquationPremierDegre61(Jinja2Exercice):

    description = u"Résolution d'équations du premier degré à coefficients entiers."
    level = u'3.Troisième'

    def __init__(self):
        super(EquationPremierDegre61, self).__init__()

        a = random.choice([1, -1]) * random.randint(2, 9)
        b = random.choice([1, -1]) * random.randint(2, 9)
        c = random.choice([1, -1]) * random.randint(2, 9)
        d = random.choice([1, -1]) * random.randint(2, 9)

        calculs = [
                r"{a}x{b:+d} &= {c}x{d:+d}\\".format(a=a, b=b, c=c, d=d),
                r"{a}x{c:+d}x &= {d}{b:+d}\\".format(a=a, b=-b, c=-c, d=d),
            ]
        if a-c == 0:
            calculs.append(r"0 &= {}\\".format(d-b))
            if d == b:
                conclusion = u"Puisque $0=0$ est toujours vrai, alors l'équation a une infinité de solutions : tous les nombres réels sont des solutions."
            else:
                conclusion = u"Puisque $0={}$ est toujours faux, alors l'équation n'a aucune solution.".format(d-b)
        elif a-c == -1:
            calculs.append(r"-x &= {}\\".format(d-b))
            calculs.append(r"(-1)\times -x&= (-1)\times {}\\".format(d-b))
            calculs.append(r"x&={}\\".format(b-d))
            conclusion = r"L'unique solution est $x = {}$.".format(b-d)
        elif a-c == 1:
            calculs.append(r"x &= {}\\".format(d-b))
            conclusion = r"L'unique solution est $x = {}$.".format(d-b)
        else:
            calculs.append(r"{}x &= {}\\".format(a-c, d-b))
            calculs.append(r"x&=\frac{{ {} }}{{ {} }}\\".format(d-b, a-c))
            solution = facteur(float(d-b)/float(a-c), "2")
            if 100*(float(d-b)/float(a-c)) == int(100 * float(d-b)/float(a-c)):
                calculs.append(r"x&={}\\".format(solution))
                conclusion = r"L'unique solution est $x = {}$.".format(solution)
            else:
                calculs.append(r"x&\simeq{}\\".format(solution))
                conclusion = r"L'unique solution est $x \simeq {}$.".format(solution)
        self.context = {
            "a": a,
            "b": b,
            "c": c,
            "d": d,
            "calculs": calculs,
            "conclusion": conclusion,
            }
