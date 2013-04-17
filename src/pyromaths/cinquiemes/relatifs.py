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
#----------------------------------------------------------------------
# Pyromaths : Poser des opérations
#----------------------------------------------------------------------

from ..outils import Arithmetique
from ..outils.Affichage import TeX, tex_coef
import random


def choix_trou(nb1, nb2, tot, operateur, exo, cor):
    nbaleatoire = random.randrange(4)
    if nbaleatoire > 1:
        exo.append("\\item $%s %s %s = \\ldots\\ldots\\ldots$" % (nb1,
                   operateur, nb2))
        cor.append("\\item $%s %s %s = \\mathbf{%s}$" % (nb1,
                   operateur, nb2, tot))
    elif nbaleatoire > 0:
        exo.append("\\item $%s %s \\ldots\\ldots\\ldots = %s$" % (nb1,
                   operateur, tot))
        cor.append("\\item $%s %s \\mathbf{%s} = %s$" % (nb1,
                   operateur, nb2, tot))
    else:
        exo.append("\\item $\\ldots\\ldots\\ldots %s %s = %s$" % (operateur,
                   nb2, tot))
        cor.append("\\item $\\mathbf{%s} %s %s = %s$" % (nb1,
                   operateur, nb2, tot))


def plus(pyromax):
    (a, b) = (Arithmetique.valeur_alea(-pyromax, pyromax), Arithmetique.valeur_alea(-pyromax,
              pyromax))
    return (a, b)


def moins(pyromax):
    (a, b) = (Arithmetique.valeur_alea(-pyromax, pyromax), Arithmetique.valeur_alea(-pyromax,
              pyromax))
    return (a + b, a)

def plus_dec(pyromax):
    (a, b) = (Arithmetique.valeur_alea(-10*pyromax, 10*pyromax)/10.0, Arithmetique.valeur_alea(-10*pyromax, 10*pyromax)/10.0)
    return (a, b)


def moins_dec(pyromax):
    (a, b) = (Arithmetique.valeur_alea(-10*pyromax, 10*pyromax)/10.0, Arithmetique.valeur_alea(-10*pyromax, 10*pyromax)/10.0)
    return (a + b, a)




def main():
    exo = ["\\exercice", "Effectuer sans calculatrice :",
           "\\begin{multicols}{3}\\noindent", "  \\begin{enumerate}"]
    cor = ["\\exercice*", "Effectuer sans calculatrice :",
           "\\begin{multicols}{3}\\noindent", "  \\begin{enumerate}"]
    modules = (plus, moins, )
    modules_dec= (plus_dec, moins_dec, )
    calculs = [i for i in range(20)]
    random.shuffle(calculs)
    for j in range(4):
        (a, b) = modules[calculs[j] // 10](10)
        choix_trou(a, tex_coef(b, '', bpn=1), a + b, '+', exo,
                       cor)

    for j in range(4,14):
        (a, b) = modules[calculs[j] // 10](10)
        if calculs[j] // 10 == 0:
            choix_trou(a, tex_coef(b, '', bpn=1), a + b, '+', exo,
                       cor)
        if calculs[j] // 10 == 1:
            choix_trou(a, tex_coef(b, '', bpn=1), a - b, '-', exo,
                       cor)
    for j in range(14,20):
        (a, b) = modules_dec[calculs[j] // 10](10)
        if calculs[j] // 10 == 0:
            choix_trou(TeX(a), tex_coef(b, '', bpn=1), TeX(a + b), '+', exo,
                       cor)
        if calculs[j] // 10 == 1:
            choix_trou(TeX(a), tex_coef(b, '', bpn=1), TeX(a - b), '-', exo,
                       cor)
    exo.extend(["  \\end{enumerate}", "\\end{multicols}"])
    cor.extend(["  \\end{enumerate}", "\\end{multicols}"])
    return (exo, cor)
