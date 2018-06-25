#!/usr/bin/env python3

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

from __future__ import unicode_literals
from builtins import range
from pyromaths.outils import Arithmetique
import random
from pyromaths.outils.Affichage import tex_coef
from pyromaths.ex import LegacyExercise

# carres=[2,3,5,6,7,10,11,13,15,17,19]

carres = [2, 3, 5, 6, 7, 10]  # ,11,13,15,17,19]


def exoaRb0(exo, cor, v):
    a = (tex_coef(v[0], '\\sqrt{%s}' % (v[6] * v[3] ** 2)), tex_coef(v[1],
         '\\sqrt{%s}' % (v[6] * v[4] ** 2), bplus=1), tex_coef(v[2],
         '\\sqrt{%s}' % (v[6] * v[5] ** 2), bplus=1))
    exo.append(u'\\[ \\thenocalcul = ' + '%s%s%s' % a + '\\] ')
    cor.append(u'\\[ \\thenocalcul = ' + '%s%s%s' % a + '\\] ')
    a = (tex_coef(v[0], '\\sqrt{%s}' % v[3] ** 2), v[6], tex_coef(v[1],
         '\\sqrt{%s}' % v[4] ** 2, bplus=1), v[6], tex_coef(v[2],
         '\\sqrt{%s}' % v[5] ** 2, bplus=1), v[6])
    cor.append(u'\\[ \\thenocalcul = ' +
                     '%s\\times\\sqrt{%s}%s\\times\\sqrt{%s}%s\\times\\sqrt{%s}' %
                     a + '\\] ')
    a = (
        tex_coef(v[0], ''),
        v[3],
        v[6],
        tex_coef(v[1], '', bplus=1),
        v[4],
        v[6],
        tex_coef(v[2], '', bplus=1),
        v[5],
        v[6],
        )
    cor.append(u'\\[ \\thenocalcul = ' +
                     '%s\\times%s\\times\\sqrt{%s}%s\\times%s\\times\\sqrt{%s}%s\\times%s\\times\\sqrt{%s}' %
                     a + '\\] ')
    a = (tex_coef(v[0] * v[3], '\\sqrt{%s}' % v[6]), tex_coef(v[1] * v[4],
         '\\sqrt{%s}' % v[6], bplus=1), tex_coef(v[2] * v[5],
         '\\sqrt{%s}' % v[6], bplus=1))
    cor.append(u'\\[ \\thenocalcul = ' + '%s%s%s' % a + '\\] ')
    del a
    cor.append(u'\\[ \\boxed{\\thenocalcul = ' + '%s' % tex_coef(v[0] * v[3] + v[1] * v[4] + v[2] *
                     v[5], '\\sqrt{%s}' % v[6]) + '} \\] ')


def valeurs_aRb0(pyromax):  # renvoie (coef0, coef1, coef2, carre0, carre1, carre2, b)
    a = carres
    l = [Arithmetique.valeur_alea(-pyromax, pyromax) for dummy in range(3)]
    while True:
        t = [random.randrange(2, pyromax) for dummy in range(3)]
        if pyromax < 4 or t[0] != t[1] and t[0] != t[2] and t[1] != t[2]:
            break
    l.extend(t)
    l.append(a[random.randrange(len(a))])
    return tuple(l)


def exoaRb1(exo, cor, v):
    a = (v[3] * v[0] ** 2, v[3] * v[1] ** 2, v[3] * v[2] ** 2)
    exo.append(u'\\[ \\thenocalcul = ' + '\\sqrt{%s}\\times\\sqrt{%s}\\times\\sqrt{%s}' %
                     a + '\\] ')
    cor.append(u'\\[ \\thenocalcul = ' + '\\sqrt{%s}\\times\\sqrt{%s}\\times\\sqrt{%s}' %
                     a + '\\] ')
    a = (v[0] ** 2, v[3], v[1] ** 2, v[3], v[2] ** 2, v[3])
    cor.append(u'\\[ \\thenocalcul = ' +
                     '\\sqrt{%s}\\times\\sqrt{%s}\\times\\sqrt{%s}\\times\\sqrt{%s}\\times\\sqrt{%s}\\times\\sqrt{%s}' %
                     a + '\\] ')
    a = (v[0], v[3], v[1], v[3], v[2], v[3])
    cor.append(u'\\[ \\thenocalcul = ' +
                     '%s\\times\\sqrt{%s}\\times%s\\times\\sqrt{%s}\\times%s\\times\\sqrt{%s}' %
                     a + '\\] ')
    a = ((v[0] * v[1]) * v[2], v[3], v[3])
    cor.append(u'\\[ \\thenocalcul = ' +
                     '%s\\times\\left(\\sqrt{%s}\\right)^2\\times\\sqrt{%s}' %
                     a + '\\] ')
    a = ((v[0] * v[1]) * v[2], v[3], v[3])
    cor.append(u'\\[ \\thenocalcul = ' + '%s\\times%s\\times\\sqrt{%s}' % a + '\\] ')
    del a
    cor.append(u'\\[ \\boxed{\\thenocalcul = ' + '%s' % tex_coef(((v[0] * v[1]) * v[2]) * v[3],
                     '\\sqrt{%s}' % v[3]) + '} \\] ')


def valeurs_aRb1(pyromax):  # renvoie (coef0, coef1, coef2, carre0, carre1, carre2, b)
    a = carres
    while True:
        l = [random.randrange(2, pyromax) for dummy in range(3)]
        if pyromax < 4 or l[0] != l[1] and l[0] != l[2] and l[1] != l[2]:
            break
    l.append(a[random.randrange(len(a))])
    return tuple(l)


def valeurs_aPbRc(pyromax):  # renvoie (coef0, coef1, coef2, carre0, carre1, carre2, b)
    while True:
        a = carres[random.randrange(len(carres))]
        b = carres[random.randrange(len(carres))]
        if a != b and Arithmetique.pgcd(a, b) != min(a, b):
            break
    while True:
        c = random.randrange(2, pyromax)
        d = Arithmetique.valeur_alea(-pyromax, pyromax)
        if c != d:
            break
    return (c, a, d, b)


def exo_aPbRc(exo, cor, v):
    a = (tex_coef(v[0], '\\sqrt{%s}' % v[1]), tex_coef(v[2],
         '\\sqrt{%s}' % v[3], bplus=1))
    exo.append(u'\\[ \\thenocalcul = ' + '\\left( %s%s \\right)^2' % a + '\\] ')
    cor.append(u'\\[ \\thenocalcul = ' + '\\left( %s%s \\right)^2' % a + '\\] ')
    if v[2] > 0:
        sgn = '+'
    else:
        sgn = '-'
    a = (tex_coef(v[0], '\\sqrt{%s}' % v[1], bpc=1), sgn, tex_coef(v[0],
         '\\sqrt{%s}' % v[1]), tex_coef(abs(v[2]), '\\sqrt{%s}' % v[3]),
         tex_coef(abs(v[2]), '\\sqrt{%s}' % v[3], bpc=1))
    cor.append(u'\\[ \\thenocalcul = ' + '%s^2%s2\\times%s\\times%s+%s^2' % a + '\\] ')
    a = (v[0] ** 2, v[1], tex_coef((2 * v[0]) * v[2], '\\sqrt{%s}' % (v[1] *
         v[3]), bplus=1), v[2] ** 2, v[3])
    cor.append(u'\\[ \\thenocalcul = ' + '%s\\times %s %s+%s\\times %s' % a + '\\] ')
    a = (v[0] ** 2 * v[1] + v[2] ** 2 * v[3], tex_coef((2 * v[0]) * v[2],
         '\\sqrt{%s}' % (v[1] * v[3]), bplus=1))
    cor.append(u'\\[ \\boxed{\\thenocalcul = ' + '%s%s' % a + '} \\] ')


def valeurs_entier0(pyromax):  # renvoie (coef0, coef1, coef2, carre0, carre1, carre2, b)
    a = carres[random.randrange(len(carres))]
    while True:
        b = random.randrange(2, pyromax)
        c = Arithmetique.valeur_alea(-pyromax, pyromax)
        if b != c and abs(c) != 1:
            break
    return (b, c, a)


def exo_entier0(exo, cor, v):
    a = (v[0], tex_coef(v[1], '\\sqrt{%s}' % v[2], bplus=1), v[0],
         tex_coef(-v[1], '\\sqrt{%s}' % v[2], bplus=1))
    exo.append(u'\\[ \\thenocalcul = ' + '\\left( %s%s \\right)\\left( %s%s \\right)' %
                     a + '\\] ')
    cor.append(u'\\[ \\thenocalcul = ' + '\\left( %s%s \\right)\\left( %s%s \\right)' %
                     a + '\\] ')
    a = (tex_coef(v[0], '', bpc=1), tex_coef(abs(v[1]), '\\sqrt{%s}' % v[2],
         bpc=1))
    cor.append(u'\\[ \\thenocalcul = ' + '%s^2-%s^2' % a + '\\] ')
    a = (v[0] ** 2, v[1] ** 2, v[2])
    cor.append(u'\\[ \\thenocalcul = ' + '%s-%s\\times %s' % a + '\\] ')
    cor.append(u'\\[ \\boxed{\\thenocalcul = ' + '%s' % (v[0] ** 2 - v[1] ** 2 * v[2]) + '} \\] ')


def valeurs_entier1(pyromax):  # renvoie (coef0, coef1, coef2, carre0, carre1, carre2, b)
    a = carres[random.randrange(len(carres))]
    while True:
        v0 = random.randrange(2, pyromax)
        v1 = random.randrange(2, pyromax)
        b0 = random.randrange(2, pyromax)
        b1 = random.randrange(2, pyromax)
        a0 = (b1 * v0) * v1
        a1 = v1 * b0
        if b0 < b1 and Arithmetique.pgcd(a0, a1) != a1:
            break
    return (a0, b0, a1, b1, a)


def exo_entier1(exo, cor, v):
    a = (tex_coef(v[0], '\\sqrt{%s}' % (v[1] ** 2 * v[4])), tex_coef(v[2],
         '\\sqrt{%s}' % (v[3] ** 2 * v[4])))
    exo.append(u'\\[ \\thenocalcul = ' + '\\frac{%s}{%s}' % a + '\\] ')
    cor.append(u'\\[ \\thenocalcul = ' + '\\frac{%s}{%s}' % a + '\\] ')
    a = (v[0], v[1] ** 2, v[4], v[2], v[3] ** 2, v[4])
    cor.append(u'\\[ \\thenocalcul = ' +
                     '\\frac{%s\\times\\sqrt{%s}\\times\\cancel{\\sqrt{%s}}}{%s\\times\\sqrt{%s}\\times\\cancel{\\sqrt{%s}}}' %
                     a + '\\] ')
    cor.append(u'\\[ \\thenocalcul = ' + '\\frac{%s\\times %s}{%s\\times %s}' % v[0:4] + '\\] ')
    cor.append(u'\\[ \\boxed{\\thenocalcul = ' + '%s' % (((v[0] * v[1]) // v[2]) // v[3]) + '} \\] ')

def _tex_racines():
    exo = ['\\exercice']
    exo.append('\\begin{enumerate}')
    exo.append(u'\\item Calculer les expressions suivantes et donner le résultat sous la forme $a\\,\\sqrt{b}$ avec $a$ et $b$ entiers, $b$ le plus petit possible.')
    exo.append('\\begin{multicols}{2}\\noindent')
    cor = ['\\exercice*']
    cor.append('\\begin{enumerate}')
    cor.append(u'\\item Calculer les expressions suivantes et donner le résultat sous la forme $a\\,\\sqrt{b}$ avec $a$ et $b$ entiers, $b$ le plus petit possible.')
    mymax = 5
    cor.append('\\begin{multicols}{2}\\noindent')
    valeurs = valeurs_aRb0(mymax)
    exoaRb0(exo, cor, valeurs)
    exo.append('\\columnbreak\\stepcounter{nocalcul}%')
    cor.append('\\columnbreak\\stepcounter{nocalcul}%')
    valeurs = valeurs_aRb1(mymax)
    exoaRb1(exo, cor, valeurs)
    exo.append('\\end{multicols}\\vspace{-3ex}')
    cor.append('\\end{multicols}')
    exo.append(u'\\item Calculer les expressions suivantes et donner le résultat sous la forme $a+b\\,\\sqrt{c}$ avec $a$, $b$ et $c$ entiers.')
    exo.append('''\\stepcounter{nocalcul}%
    \\begin{multicols}{2}\\noindent''')
    cor.append(u'\\item Calculer les expressions suivantes et donner le résultat sous la forme $a+b\\,\\sqrt{c}$ avec $a$, $b$ et $c$ entiers.')
    cor.append('''\\stepcounter{nocalcul}%
    \\begin{multicols}{2}\\noindent''')
    valeurs = valeurs_aPbRc(mymax)
    exo_aPbRc(exo, cor, valeurs)
    exo.append('\\columnbreak\\stepcounter{nocalcul}%')
    cor.append('\\columnbreak\\stepcounter{nocalcul}%')
    valeurs = valeurs_aPbRc(mymax)
    exo_aPbRc(exo, cor, valeurs)
    exo.append('\\end{multicols}\\vspace{-3ex}')
    cor.append('\\end{multicols}')
    exo.append(u"\\item Calculer les expressions suivantes et donner le résultat sous la forme d'un nombre entier.\n")
    exo.append('''\\stepcounter{nocalcul}%
    \\begin{multicols}{2}\\noindent''')
    cor.append(u"\\item Calculer les expressions suivantes et donner le résultat sous la forme d'un nombre entier.\n")
    cor.append('''\\stepcounter{nocalcul}%
    \\begin{multicols}{2}\\noindent''')
    valeurs = valeurs_entier0(mymax)
    exo_entier0(exo, cor, valeurs)
    exo.append('\\columnbreak\\stepcounter{nocalcul}%')
    cor.append('\\columnbreak\\stepcounter{nocalcul}%')
    valeurs = valeurs_entier1(mymax)
    exo_entier1(exo, cor, valeurs)
    exo.append('\\end{multicols}\\vspace{-3ex}')
    exo.append('\\end{enumerate}')
    cor.append('\\end{multicols}')
    cor.append('\\end{enumerate}')
    return (exo, cor)

class tex_racines(LegacyExercise):
    """Racines carrées"""

    tags = ["Troisième"]
    function = _tex_racines
