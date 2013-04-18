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

import random

#
# ------------------- PGCD -------------------


def tex_trouve_diviseur(a):  # trouve si les nombres dans le tuple a sont divisible par 10, 2, 5, 9 ou 3 (dans cet ordre)
    if a[0] % 10 == 0 and a[1] % 10 == 0:
        return '\\nombre{' + str(a[0]) + '} et \\nombre{' + str(a[1]) + \
            u'} se terminent tous les deux par zéro donc ils sont divisibles par 10.\\par\n' + \
            '\\nombre{' + str(a[0]) + '} et \\nombre{' + str(a[1]) + \
            '} ne sont donc pas premiers entre eux'
    elif a[0] % 2 == 0 and a[1] % 2 == 0:
        return '\\nombre{' + str(a[0]) + '} et \\nombre{' + str(a[1]) + \
            '} sont deux nombres pairs donc ils sont divisibles par 2.\\par\n' + \
            '\\nombre{' + str(a[0]) + '} et \\nombre{' + str(a[1]) + \
            '} ne sont donc pas premiers entre eux'
    elif a[0] % 5 == 0 and a[1] % 5 == 0:
        return '\\nombre{' + str(a[0]) + '} et \\nombre{' + str(a[1]) + \
            u'} se terminent tous les deux par zéro ou cinq donc ils sont divisibles par 5.\\par\n' + \
            '\\nombre{' + str(a[0]) + '} et \\nombre{' + str(a[1]) + \
            '} ne sont donc pas premiers entre eux'
    elif a[0] % 9 == 0 and a[1] % 9 == 0:
        return 'La somme des chiffres de \\nombre{' + str(a[0]) + \
            '} et celle de \\nombre{' + str(a[1]) + \
            '} sont divisibles par neuf donc ils sont divisibles par 9.\\par\n' + \
            '\\nombre{' + str(a[0]) + '} et \\nombre{' + str(a[1]) + \
            '} ne sont donc pas premiers entre eux'
    elif a[0] % 3 == 0 and a[1] % 3 == 0:
        return 'La somme des chiffres de \\nombre{' + str(a[0]) + \
            '} et celle de \\nombre{' + str(a[1]) + \
            '} sont divisibles par trois donc ils sont divisibles par 3.\\par\n' + \
            '\\nombre{' + str(a[0]) + '} et \\nombre{' + str(a[1]) + \
            '} ne sont donc pas premiers entre eux'


def valeurs_pgcd():  # creer un tuple contenant les deux nombres dont on cherche le pgcd
    reste = random.choice((2, 3, 5, 9, 10)) * random.choice((7, 11, 13,
            17, 19, 23, 31))
    diviseur = reste * random.randrange(1, 10)
    for i in range(random.randrange(2, 5)):
        (diviseur, reste) = (diviseur * random.randrange(1, 10) + reste,
                             diviseur)
    return (diviseur, reste)


def algo_euclide(a):  # renvoi une liste contenant (dividende,diviseur,quotient,reste) pour chaque etape
    liste = []
    if a[0] > a[1]:
        (dividende, diviseur) = (a[0], a[1])
    else:
        (dividende, diviseur) = (a[1], a[0])
    (quotient, reste) = (dividende // diviseur, dividende % diviseur)
    liste.append((dividende, diviseur, quotient, reste))
    while reste != 0:
        (dividende, diviseur) = (diviseur, reste)
        (quotient, reste) = (dividende // diviseur, dividende % diviseur)
        liste.append((dividende, diviseur, quotient, reste))
    return liste


def simplifie_fraction_pgcd(l):  # renvoie le nombre par lequel on peut simplifier la fraction et la fraction simplifiée
    (pgcd, n0, d0) = (l[len(l) - 1][1], l[0][0], l[0][1])
    (n1, d1) = (l[0][0] // pgcd, l[0][1] // pgcd)
    return (n0, d0, n0, pgcd, d0, pgcd, n1, d1)


def tex_algo_euclide(l):  # renvoie l'ecriture au format tex de l'algorithme d'Euclide
    lignes = []
    for i in range(len(l)):
        lignes.append('\\nombre{%s}=\\nombre{%s}\\times\\nombre{%s}+\\nombre{%s}' %
                      l[i])
    lignes.append('\\fbox{Donc le \\textsc{pgcd} de \\nombre{%s} et \\nombre{%s} est %s}.\n' %
                  (l[0][0], l[0][1], l[len(l) - 1][1]))
    return lignes


def tex_simplifie_fraction_pgcd(a):  # renvoie l'ecriture au format tex de la simplification de la fraction
    return '''\\begin{align*}
\\cfrac{\\nombre{%s}}{\\nombre{%s}} &= \\cfrac{\\nombre{%s}\\div%s}{\\nombre{%s}\\div%s}\\\\\n      &= \\boxed{\\cfrac{\\nombre{%s}}{\\nombre{%s}}}
\\end{align*}''' % a

def tex_pgcd():
    nombres = valeurs_pgcd()
    exo = ['\\exercice']
    exo.append('\\begin{enumerate}')
    exo.append('\\item Les nombres \\nombre{%s} et \\nombre{%s} sont-ils premiers entre eux ?  ' % nombres)
    exo.append('\\item Calculer le plus grand commun diviseur (\\textsc{pgcd}) de \\nombre{%s} et \\nombre{%s}.' % nombres)
    exo.append(u'\\item Simplifier la fraction $\\cfrac{\\nombre{%s}}{\\nombre{%s}}$ pour la rendre irréductible en indiquant la méthode.\n' % nombres)
    exo.append('\\end{enumerate}')
    cor = ['\\exercice*']
    cor.append('\\begin{enumerate}')
    cor.append('\\item Les nombres \\nombre{%s} et \\nombre{%s} sont-ils premiers entre eux ?\\par ' % nombres)
    cor.append(tex_trouve_diviseur(nombres))
    cor.append('\\item Calculer le plus grand commun diviseur (\\textsc{pgcd}) de \\nombre{%s} et \\nombre{%s}.\\par' % nombres)
    cor.append('On calcule le \\textsc{pgcd} des nombres \\nombre{%s} et \\nombre{%s} en utilisant l\'algorithme d\'Euclide.' % nombres)
    l = algo_euclide(nombres)
    tex_liste = tex_algo_euclide(l)
    for i in range(len(l)):
        cor.append(u'\\[ %s' % tex_liste[i] + '\\] ')
    cor.append(tex_liste[len(l)])
    cor.append(u'\\item Simplifier la fraction $\\cfrac{\\nombre{%s}}{\\nombre{%s}}$ pour la rendre irréductible en indiquant la méthode.' % nombres)
    cor.append(tex_simplifie_fraction_pgcd(simplifie_fraction_pgcd(l)))
    cor.append('\\end{enumerate}')
    return (exo, cor)
