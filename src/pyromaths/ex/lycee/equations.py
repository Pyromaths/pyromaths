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
from __builtin__ import str
'''
Created on 1 janv. 2015

@author: jerome
'''
from pyromaths import ex
from random import randrange
from math import sqrt
from pyromaths.ex.troisiemes import notion_de_fonction
from pyromaths.outils import Priorites3
from pyromaths.classes.PolynomesCollege import Polynome
from pyromaths.classes.Fractions import Fraction

if __name__ == '__main__':
    from pyromaths.ex.troisiemes import notion_de_fonction
    from pyromaths.outils import Priorites3

    pass

def racines(p, lracines):
    """ Trouve les 2 racines manquantes d'un polynôme de degré 5 connaissant 3 des racines
    """
    q = Polynome(p)
    for r in lracines:
        q = q // Polynome("x-%s" % r)
    delta = q[1][0] ** 2 - 4 * q[0][0] * q[2][0]
    d = float(eval(Priorites3.priorites(delta)[-1][0]))
    return (-float(q[1][0]) + sqrt(d)) / 2 / float(q[0][0]), (-float(q[1][0]) - sqrt(d)) / 2 / float(q[0][0])

class EquationGraphique(ex.TexExercise):
    # description = _(u'Résolution graphique d\'équations')
    # level = _(u"2.Seconde")

    def __init__(self):
        """
        l1, l2 et l3 sont les abscisses remarquables,
        y1, y2 et y3 sont les ordonnées correspondantes

        l1 contient trois abscisses de même ordonnée
        l2 contient deux abscisses de même ordonnée
        l3 contient 2 abscisses séparées d'un dixième (un extremum local j'espère) de même ordonnée
        """
        End = False
        while End == False:
            encore = True
            while encore:
                l1 = [a for a in range(-6, 7)]
                for dummy in range(10):
                    l1.pop(randrange(len(l1)))
                if l1[2] - l1[1] > 3 and l1[1] - l1[0] > 3: encore = False
            pos = randrange(2)
            l2 = randrange(1, 4) / 2.
            l2 = [l1[pos] + l2, l1[pos + 1] - l2]
            l3 = [(l1[(pos + 1) % 2] + l1[(pos + 1) % 2 + 1]) / 2.]
            l1.extend(l2)
            l1.extend(l3)
            y = [randrange(2) * (-1) ** randrange(2), randrange(3, 5) * (-1) ** randrange(2)]
            # if randrange(2): y[0], y[2] = y[2], y[0]
            #=======================================================================
            # y = [y[1], y[1], y[1], y[0], y[0], y[2], y[2]]
            #=======================================================================
            y = [y[1], y[1], y[1], y[0], y[0], y[0]]
            self.points = list([(l1[i], y[i]) for i in range(6)])
            p = notion_de_fonction.Lagrange(self.points)
            self.polynome = eval(Priorites3.priorites(p)[-1][0])
            End = True
            for val in range(13):
                #===============================================================
                # try:
                #     ordonnee = eval(self.polynome(val - 6))
                # except:
                #     print repr(self.polynome), val - 6
                # if isinstance(ordonnee, str):
                #     ordonnee = eval(Priorites3.priorites(ordonnee)[-1][0])
                #===============================================================
                try:
                    ordonnee = eval(Priorites3.priorites(self.polynome(val - 6))[-1][0])
                except IndexError:
                    ordonnee = eval(self.polynome(val - 6))
                if ordonnee > 5 or ordonnee < -5:
                    End = False
                    break

    def tex_statement(self):
        exo = [r'\exercice']
        exo.extend([r"\psset{unit=5mm, algebraic, dotsize=4pt 4}", r"\begin{pspicture*}(-6.2,-5.2)(6.2,5.2)"])
        exo.append(r"\psgrid[subgriddiv=1, gridwidth=.6pt,subgridcolor=lightgray, gridlabels=0pt]")
        exo.append(r"\psaxes[linewidth=1.2pt,]{->}(0,0)(-6.2,-5.2)(6.2,5.2)")
        exo.append(r"\psplot[plotpoints=200, linewidth=1.5pt, linecolor=DarkRed]{-6}{6}{%s}" % Priorites3.plotify(repr(self.polynome)))
        exo.append(r"\psdots %s" % " ".join([str(val) for val in self.points]))
        exo.append(r"\end{pspicture*}")
        #=======================================================================
        # print racines(self.polynome, [self.points[i][0] for i in range(3)])
        # print racines(self.polynome, [self.points[i][0] for i in range(3, 6)])
        #=======================================================================
        return exo
