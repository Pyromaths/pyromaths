#!/usr/bin/env python3

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
from __future__ import unicode_literals
from builtins import chr
from builtins import range
from random import randrange, shuffle
from pyromaths.outils import Priorites3
from pyromaths.classes.PolynomesCollege import factoriser

def factorisation():
    """Génère un exercice de factorisation utilisant les identités remarquables ou
    la distributivité
    """
    l = [randrange(1, 11) for dummy in range(21)]
    diff = [True, False, False]
    shuffle(diff)
    exo = [id_rem1, id_rem2]
    lexo = [exo[randrange(2)](l[0], l[1])]
    lexo.append(id_rem3(l[2], l[3]))
    lexo.append(id_rem3bis(l[4], l[5], l[6]))
    lexo.append(facteur_commun1(l[7:13], diff=diff.pop()))
    shuffle(lexo)
    exo = [facteur_commun2, facteur_commun3]
    shuffle(exo)
    lexo.append(exo[0](l[13:17], diff=diff.pop()))
    lexo.append(exo[1](l[17:21], diff=diff.pop()))

    exo = ["\\exercice", u"Factoriser chacune des expressions littérales suivantes :"]
    exo.append("\\begin{multicols}{2}")
    cor = ["\\exercice*", u"Factoriser chacune des expressions littérales suivantes :"]
    cor.append("\\begin{multicols}{2}")
    for i in range(len(lexo)):
        p = [lexo[i]]
        while True:
            fact = factoriser(p[-1])
            if fact:
                p.append(fact)
            else: break
        p = Priorites3.texify([Priorites3.splitting(p[j]) for j in range(len(p))])
        cor.append('\\\\\n'.join(['$%s=%s$' % (chr(i + 65), p[j]) for j in range(len(p) - 1)]))
        cor.append('\\\\')
        cor.append('\\fbox{$%s=%s$}\\\\\n' % (chr(i + 65), p[-1]))
    exo.append('\\\\\n'.join(['$%s=%s$' % (chr(i + 65), Priorites3.texify([Priorites3.splitting(lexo[i])])[0]) for i in range(len(lexo))]))
    exo.append("\\end{multicols}")
    cor.append("\\end{multicols}")
    return exo, cor

def id_rem1(a, b, details=1):
    """Construit un Polynome de la forme ax^2+2abx+b^2
    Renvoie une chaine"""
    return 'Polynome([[%r, 2], [%r, 1], [%r, 0]], details=%s)' % (a ** 2, 2 * a * b, b ** 2, details)
def id_rem2(a, b, details=1):
    """Construit un Polynome de la forme ax^2-2abx+b^2
    Renvoie une chaine"""
    return 'Polynome([[%r, 2], [%r, 1], [%r, 0]], details=%s)' % (a ** 2, -2 * a * b, b ** 2, details)
def id_rem3(a, b, details=1):
    """Construit un Polynome de la forme a^2x^2-b^2
    Renvoie une chaine"""
    sgn = randrange(2)
    return 'Polynome([[%r, 2], [%r, 0]], details=%s)' % (a ** 2 * (-1) ** sgn, b ** 2 * (-1) ** (sgn + 1), details)
def id_rem3bis(a, b, c, details=1):
    """Construit un Polynome de la forme (ax+b)^2-c^2
    Renvoie une chaine"""
    sgn = randrange(2)
    lpolynomes = ['Polynome([[%r, 1], [%r, 0]], details=%s)**2' % (a * (-1) ** randrange(3), b * (-1) ** randrange(3), details)]
    lpolynomes.append('Polynome([[%r, %r]], details=%s)' % (c ** 2, 2 * randrange(2), details))
    shuffle(lpolynomes)
    lop = ['+', '-']
    shuffle(lop)
    poly = ''
    for i in range(2):
        if i != 0 or lop[0] == '-': poly += lop[i]
        poly += lpolynomes[i]
    return poly
def facteur_commun1(lcoeff, details=1, diff=False):
    """Construit une somme de la forme (ax+b)(cx+d)+(ax+b)(ex+f)
    Si diff, alors (ax+b)(cx+d)-(ax+b)(ex+f)
    lcoeff est une liste de décimaux de longueur 6
    Renvoie une chaine"""
    lpolynomes = ['Polynome([[%r, 1], [%r, 0]], details=%s)' % (lcoeff[2 * i] * (-1) ** randrange(3), lcoeff[2 * i + 1] * (-1) ** randrange(3), details) for i in range(3)]
    lpolynomes.insert(randrange(2, 4), lpolynomes[randrange(2)])
    lop = [0, '*', '+', '*']
    if diff: lop[randrange(2) * 2] = '-'
    poly = ''
    for i in range(4):
        if lop[i]: poly += lop[i]
        poly += lpolynomes[i]
    return poly
def facteur_commun2(lcoeff, details=1, diff=False):
    """Construit une somme de la forme (ax+b)(cx+d)+(ax+b)
    si diff, (ax+b)(cx+d)-(ax+b) ou -(ax+b)(cx+d)+(ax+b)
    lcoeff est une liste de décimaux de longueur 4
    Renvoie une chaine"""
    lpolynomes = ['Polynome([[%r, 1], [%r, 0]], details=%s)' % (lcoeff[2 * i], lcoeff[2 * i + 1] * (-1) ** randrange(3), details) for i in range(2)]
    a = lpolynomes[0]
    shuffle(lpolynomes)
    lop = [ '*', '+']
    if diff: lop[1] = '+-'[randrange(2)]
    shuffle(lop)
    if lop[0] == '*':
        lpolynomes.append(a)
    else:
        lpolynomes.insert(0, a)
    if diff and lop.count('-') == 0: lop.insert(0, '-')
    else: lop.insert(0, 0)
    poly = ''
    for i in range(3):
        if lop[i]: poly += lop[i]
        poly += lpolynomes[i]
    return poly
def facteur_commun3(lcoeff, details=1, diff=False):
    """Construit une somme de la forme (ax+b)(cx+d)+(ax+b)**2
    lcoeff est une liste de décimaux de longueur 4
    Renvoie une chaine"""
    lpolynomes = ['Polynome([[%r, 1], [%r, 0]], details=%s)' % (lcoeff[2 * i] * (-1) ** randrange(3), lcoeff[2 * i + 1] * (-1) ** randrange(3), details) for i in range(2)]
    a = lpolynomes[0]
    shuffle(lpolynomes)
    lop = [ '*', '+']
    if diff: lop[1] = '+-'[randrange(2)]
    shuffle(lop)
    if lop[0] == '*':
        lpolynomes.append(a + '**2')
    else:
        lpolynomes.insert(0, a + '**2')
    if diff and lop.count('-') == 0: lop.insert(0, '-')
    else: lop.insert(0, 0)
    poly = ''
    for i in range(3):
        if lop[i]: poly += lop[i]
        poly += lpolynomes[i]
    return poly

factorisation.description = u'Factorisations'
