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
'''
Créé le 9 déc. 2013

.. sectionauthor:: Jérôme Ortais <jerome.ortais@pyromaths.org>
'''
from random import shuffle
if __name__ == '__main__':
    pass

def choix_points():
    """**choix_points**\ ()

    Renvoie un tuple contenant 5 coordonnées sous forme de tuple telles que
    les abscisses et ordonnées sont paires, distinctes, comprises entre -4 et 4,
    une abscisse n'est jamais égale à une ordonnée et la coordonnée (b, a) n'est
    pas listée si la coordonnée (a, b) existe.

    >>> from pyromaths.ex.troisiemes import notion_de_fonction
    >>> notion_de_fonction.choix_points()  # doctest: +SKIP
    ((-4, -2), (-2, 0), (0, 4), (2, -4), (4, 2))

    :rtype: tuple

    """
    abscisse = [i for i in range(5)]
    refaire = True
    while refaire:
        ordonnee = [i for i in range(5)]
        shuffle(ordonnee)
        refaire = False
        for i in range(5):
            if i == ordonnee[i] or ordonnee[ordonnee[i]] == i :
                refaire = True
                break
    return tuple([(abscisse[i] * 2 - 4, ordonnee[i] * 2 - 4) for i in range(5)])

def Lagrange(points):
    """**Lagrange**\ (*points*)
    Renvoie le polynôme d'interpolation de Lagrange pour les points de coordonnées *points*

    Est prévue pour être utilisé avec :py:func:`choix_points`

    Associé à  :py:func:`pyromaths.outils.Priorites3.priorites`, permet d'obtenir sa version réduite.

    Associé à  :py:func:`pyromaths.outils.Priorites3.plotify`, permet d'obtenir sa version utilisable avec psplot.

    >>> from pyromaths.ex.troisiemes import notion_de_fonction
    >>> p = notion_de_fonction.Lagrange(((-4, -2), (-2, 0), (0,4), (2,-4), (4,2)))

    >>> from pyromaths.outils import Priorites3
    >>> Priorites3.priorites(p)[-1]
    ['Polynome([[Fraction(5, 48), 4], [Fraction(1, 8), 3], [Fraction(-23, 12), 2], [Fraction(-3, 2), 1], [Fraction(4, 1), 0]], "x", 0)']
    >>> Priorites3.plotify(Priorites3.priorites(p)[-1])
    '5/48*x^4+1/8*x^3-23/12*x^2-3/2*x^1+4/1'
    """
    PIL = []
    for i in range(len(points)):
        if points[i][1]:
            PIL.append('Fraction(%s, ' % points[i][1])
            produit = []
            for j in  range(len(points)):
                if j != i: produit.append(repr(points[i][0] - points[j][0]))
            produit = repr(eval("*".join(produit)))
            PIL[i] += produit + ")*"
            produit = []
            for j in  range(len(points)):
                if j != i and points[j][0] > 0: produit.append("Polynome(\"x-%s\", details = 0)" % points[j][0])
                elif j != i and points[j][0] < 0: produit.append("Polynome(\"x+%s\", details = 0)" % -points[j][0])
                elif j != i and points[j][0] == 0: produit.append("Polynome(\"x\", details = 0)")
            produit = "*".join(produit)
            PIL[i] += produit
        else:
            PIL.append('0')
    return "+".join(PIL)
