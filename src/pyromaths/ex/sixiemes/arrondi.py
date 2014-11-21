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
from random import randint, shuffle
import textwrap

from pyromaths import ex
from pyromaths.outils.Affichage import decimaux

precision = [u'au millième', u'au centième', u'au dixième', u'à l\'unité',
             u'à la dizaine', u'à la centaine', 'au millier',
             u'à la dizaine de milliers']

supinf = ['', u' par défaut', u' par excès']

class ArrondirNombreDecimal(ex.TexExercise):
    """ Exercice d'arrondis avec les encadrements. """

    description = u'Arrondir des nombres décimaux'

    def __init__(self):
        hasard = [valide_hasard() for dummy in range(4)]
        choix = [(i, j) for i in range(7)  for j in range(3)]
        shuffle(choix)
        self.choix_precision = [choix[i][0] for i in range(4)]
        self.choix_supinf = [choix[i][1] for i in range(4)]
    # FIXME
        # Arrondir n'est pas synonyme de valeur approchée
        # Valeur approchée par excès 
        # Valeur approchée par défaut 
        # Arrondi = la « meilleure » valeur approchée
        # et ne paraît employé ici correctement
        self.nombres = [(hasard[0]) / (10 ** (-self.choix_precision[0] + 4)),
                (hasard[1]) / (10 ** (-self.choix_precision[1] + 4)),
                (hasard[2]) / (10 ** (-self.choix_precision[2] + 4)),
                (hasard[3]) / (10 ** (-self.choix_precision[3] + 4))]

    def tex_statement(self):
        exo = ["\\exercice", '\\begin{enumerate}']
        for k in range(4):
            exo.append("\\item Arrondir " + decimaux(self.nombres[k]) + " " + 
                    precision[self.choix_precision[k]] + supinf[self.choix_supinf[k]] + 
                    '.')
        exo.append("\\end{enumerate}")
        return exo

    def tex_answer(self):
        cor = ["\\exercice*", '\\begin{enumerate}']
        for k in range(4):
            arrondi = round(self.nombres[k], -self.choix_precision[k] + 3)
            if (arrondi > self.nombres[k]):
                defaut = arrondi - 10 ** (self.choix_precision[k] - 3)
                exc = arrondi
            if (arrondi <= self.nombres[k]):
                defaut = arrondi
                exc = arrondi + 10 ** (self.choix_precision[k] - 3)
            if (self.choix_supinf[k] == 0):
                solution = arrondi
            elif (self.choix_supinf[k] == 1):
                solution = defaut
            elif (self.choix_supinf[k] == 2):
                solution = exc
            cor.append('\\item L\'encadrement de ' + decimaux(self.nombres[k]) + ' ' + 
                    precision[self.choix_precision[k]] + ' est :\\par')
            cor.append(decimaux(defaut) + ' < ' + decimaux(self.nombres[k]) + ' < ' + 
                    decimaux(exc) + '\\par')
            cor.append(u'On en déduit que son arrondi ' + 
                    precision[self.choix_precision[k]] + ' ' + supinf[self.choix_supinf[k]] + 
                    ' est : ' + decimaux(solution) + '.')
        cor.append("\\end{enumerate}")
        return cor

    tests = {
        0: {
            'tex_statement': textwrap.dedent(ur"""
                \exercice
                \begin{enumerate}
                \item Arrondir 845\,987 à la dizaine par défaut.
                \item Arrondir 4\,263,73 au dixième par défaut.
                \item Arrondir 51,616\,4 au millième par défaut.
                \item Arrondir 78,596\,3 au millième.
                \end{enumerate}
                """),
            'tex_answer': textwrap.dedent(ur"""
                \exercice*
                \begin{enumerate}
                \item L'encadrement de 845\,987 à la dizaine est :\par
                845\,980 < 845\,987 < 845\,990\par
                On en déduit que son arrondi à la dizaine  par défaut est : 845\,980.
                \item L'encadrement de 4\,263,73 au dixième est :\par
                4\,263,7 < 4\,263,73 < 4\,263,8\par
                On en déduit que son arrondi au dixième  par défaut est : 4\,263,7.
                \item L'encadrement de 51,616\,4 au millième est :\par
                51,616 < 51,616\,4 < 51,617\par
                On en déduit que son arrondi au millième  par défaut est : 51,616.
                \item L'encadrement de 78,596\,3 au millième est :\par
                78,596 < 78,596\,3 < 78,597\par
                On en déduit que son arrondi au millième  est : 78,596.
                \end{enumerate}
                """),
            }
        }

def valide_hasard():
    """renvoie un nombre float non multiple de 10000"""
    nbre, unite = randint(1000, 100000), randint(1, 9)
    return float(nbre) * 10 + unite
