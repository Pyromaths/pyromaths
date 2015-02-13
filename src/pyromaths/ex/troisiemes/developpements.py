#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Pyromaths
# Un programme en Python qui permet de créer des fiches d'exercices types de
# mathématiques niveau collège ainsi que leur corrigé en LaTeX.
# Copyright (C) 2014 -- Jérôme Ortais (jerome.ortais@pyromaths.org)
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
from random import randrange, shuffle
from pyromaths.classes.Fractions import Fraction
from pyromaths.outils import Priorites3
from pyromaths.outils.Arithmetique import pgcd


def id_rem():
    """Génère un exercice de développement des 3 identités remarquables avec une situation piège.
    Dans un premier temps, on n'utilise que des nombres entiers, puis des fractions, puis l'opposé 
    d'une expression littérale.
    """

    l = [randrange(1, 11) for dummy in range(14)]
    while pgcd(l[8], l[9]) != 1 or pgcd(l[10], l[11]) != 1 or (l[9] == 1 and l[11] == 1):
        # On crée deux rationnels irréductibles non tous deux entiers.
        l = [randrange(1, 11) for dummy in range(14)]
    lpoly = [id_rem1(l[0], l[1]), id_rem2(l[2], l[3]), id_rem3(l[4], l[5]), id_rem4(l[6], l[7])]
    shuffle(lpoly)
    lid = [id_rem1, id_rem2, id_rem3, id_rem4]
    lpoly2 = [lid.pop(randrange(4))(Fraction(l[8], l[9]), Fraction(l[10], l[11]))]
    lpoly2.append('-' + lid.pop(randrange(3))(l[12], l[13]))
    shuffle(lpoly2)
    lpoly.extend(lpoly2)
    expr = [Priorites3.texify([Priorites3.splitting(lpoly[i])]) for i in range(6)]
    exo = ["\\exercice", u"Développer chacune des expressions littérales suivantes :"]
    exo.append("\\begin{multicols}{2}")
    exo.append('\\\\\n'.join(['$%s=%s$' % (chr(i + 65), expr[i][0]) for i in range(6)]))
    exo.append("\\end{multicols}")
    cor = ["\\exercice*", u"Développer chacune des expressions littérales suivantes :"]
    cor.append("\\begin{multicols}{2}")
    for i in range(6):
        dev = Priorites3.texify(Priorites3.priorites(lpoly[i]))
        dev.insert(0, expr[i][0])
        cor.append('\\\\\n'.join(['$%s=%s$' % (chr(i + 65), dev[j]) for j in range(len(dev) - 1)]))
        cor.append('\\\\')
        cor.append('\\fbox{$%s=%s$}\\\\\n' % (chr(i + 65), dev[-1]))
    cor.append("\\end{multicols}")

    return exo, cor

def id_rem1(a, b, details=2):
    """Construit un Polynome de la forme (ax+b)^2
    Renvoie une chaine"""
    return 'Polynome([[%r, 1], [%r, 0]], details=%s)**2' % (a, b, details)
def id_rem2(a, b, details=2):
    """Construit un Polynome de la forme (ax-b)^2
    Renvoie une chaine"""
    return 'Polynome([[%r, 1], [%r, 0]], details=%s)**2' % (a, -b, details)
def id_rem3(a, b, details=2):
    """Construit un Polynome de la forme (ax+b)(ax-b) ou (ax-b)(ax+b)
    Renvoie une chaine"""
    sgn = randrange(2)
    return 'Polynome([[%r, 1], [%r, 0]], details=%s) * Polynome([[%r, 1], [%r, 0]], details=%s)' % (a, (-1) ** sgn * b, details, a, (-1) ** (sgn + 1) * b, details)
def id_rem4(a, b, details=2):
    """Construit un Polynome de la forme (ax+b)(bx-a) ou (ax-b)(bx+a)
    Renvoie une chaine"""
    sgn = randrange(2)
    return 'Polynome([[%r, 1], [%r, 0]], details=%s) * Polynome([[%r, 1], [%r, 0]], details=%s)' % (a, (-1) ** sgn * b, details, b, (-1) ** (sgn + 1) * a, details)


id_rem.description = u'Identités remarquables'
