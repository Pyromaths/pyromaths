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

import outils
import random
from .developpements import tex_coef

#carres=[2,3,5,6,7,10,11,13,15,17,19]

carres = [2, 3, 5, 6, 7, 10]  #,11,13,15,17,19]


def exoaRb0(f0, f1, v):
    a = (tex_coef(v[0], '\\sqrt{%s}' % (v[6] * v[3] ** 2)), tex_coef(v[1],
         '\\sqrt{%s}' % (v[6] * v[4] ** 2), bplus=1), tex_coef(v[2],
         '\\sqrt{%s}' % (v[6] * v[5] ** 2), bplus=1))
    outils.ecrit_tex(f0, '%s%s%s' % a, tabs=3)
    outils.ecrit_tex(f1, '%s%s%s' % a, tabs=3)
    a = (tex_coef(v[0], '\\sqrt{%s}' % v[3] ** 2), v[6], tex_coef(v[1],
         '\\sqrt{%s}' % v[4] ** 2, bplus=1), v[6], tex_coef(v[2],
         '\\sqrt{%s}' % v[5] ** 2, bplus=1), v[6])
    outils.ecrit_tex(f1,
                     '%s\\times\\sqrt{%s}%s\\times\\sqrt{%s}%s\\times\\sqrt{%s}' %
                     a, tabs=3)
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
    outils.ecrit_tex(f1,
                     '%s\\times%s\\times\\sqrt{%s}%s\\times%s\\times\\sqrt{%s}%s\\times%s\\times\\sqrt{%s}' %
                     a, tabs=3)
    a = (tex_coef(v[0] * v[3], '\\sqrt{%s}' % v[6]), tex_coef(v[1] * v[4],
         '\\sqrt{%s}' % v[6], bplus=1), tex_coef(v[2] * v[5],
         '\\sqrt{%s}' % v[6], bplus=1))
    outils.ecrit_tex(f1, '%s%s%s' % a, tabs=3)
    del a
    outils.ecrit_tex(f1, '%s' % tex_coef(v[0] * v[3] + v[1] * v[4] + v[2] *
                     v[5], '\\sqrt{%s}' % v[6]), cadre=1, tabs=3)


def valeurs_aRb0(pyromax):  # renvoie (coef0, coef1, coef2, carre0, carre1, carre2, b)
    a = carres
    l = [outils.valeur_alea(-pyromax, pyromax) for i in range(3)]
    while True:
        t = [random.randrange(2, pyromax) for i in range(3)]
        if pyromax < 4 or t[0] != t[1] and t[0] != t[2] and t[1] != t[2]:
            break
    l.extend(t)
    l.append(a[random.randrange(len(a))])
    return tuple(l)


def exoaRb1(f0, f1, v):
    a = (v[3] * v[0] ** 2, v[3] * v[1] ** 2, v[3] * v[2] ** 2)
    outils.ecrit_tex(f0, '\\sqrt{%s}\\times\\sqrt{%s}\\times\\sqrt{%s}' %
                     a, tabs=3)
    outils.ecrit_tex(f1, '\\sqrt{%s}\\times\\sqrt{%s}\\times\\sqrt{%s}' %
                     a, tabs=3)
    a = (v[0] ** 2, v[3], v[1] ** 2, v[3], v[2] ** 2, v[3])
    outils.ecrit_tex(f1,
                     '\\sqrt{%s}\\times\\sqrt{%s}\\times\\sqrt{%s}\\times\\sqrt{%s}\\times\\sqrt{%s}\\times\\sqrt{%s}' %
                     a, tabs=3)
    a = (v[0], v[3], v[1], v[3], v[2], v[3])
    outils.ecrit_tex(f1,
                     '%s\\times\\sqrt{%s}\\times%s\\times\\sqrt{%s}\\times%s\\times\\sqrt{%s}' %
                     a, tabs=3)
    a = ((v[0] * v[1]) * v[2], v[3], v[3])
    outils.ecrit_tex(f1,
                     '%s\\times\\left(\\sqrt{%s}\\right)^2\\times\\sqrt{%s}' %
                     a, tabs=3)
    a = ((v[0] * v[1]) * v[2], v[3], v[3])
    outils.ecrit_tex(f1, '%s\\times%s\\times\\sqrt{%s}' % a, tabs=3)
    del a
    outils.ecrit_tex(f1, '%s' % tex_coef(((v[0] * v[1]) * v[2]) * v[3],
                     '\\sqrt{%s}' % v[3]), cadre=1, tabs=3)


def valeurs_aRb1(pyromax):  # renvoie (coef0, coef1, coef2, carre0, carre1, carre2, b)
    a = carres
    while True:
        l = [random.randrange(2, pyromax) for i in range(3)]
        if pyromax < 4 or l[0] != l[1] and l[0] != l[2] and l[1] != l[2]:
            break
    l.append(a[random.randrange(len(a))])
    return tuple(l)


def valeurs_aPbRc(pyromax):  # renvoie (coef0, coef1, coef2, carre0, carre1, carre2, b)
    while True:
        a = carres[random.randrange(len(carres))]
        b = carres[random.randrange(len(carres))]
        if a != b and outils.pgcd(a, b) != min(a, b):
            break
    while True:
        c = random.randrange(2, pyromax)
        d = outils.valeur_alea(-pyromax, pyromax)
        if c != d:
            break
    return (c, a, d, b)


def exo_aPbRc(f0, f1, v):
    a = (tex_coef(v[0], '\\sqrt{%s}' % v[1]), tex_coef(v[2],
         '\\sqrt{%s}' % v[3], bplus=1))
    outils.ecrit_tex(f0, '\\left( %s%s \\right)^2' % a, tabs=3)
    outils.ecrit_tex(f1, '\\left( %s%s \\right)^2' % a, tabs=3)
    if v[2] > 0:
        sgn = '+'
    else:
        sgn = '-'
    a = (tex_coef(v[0], '\\sqrt{%s}' % v[1], bpc=1), sgn, tex_coef(v[0],
         '\\sqrt{%s}' % v[1]), tex_coef(abs(v[2]), '\\sqrt{%s}' % v[3]),
         tex_coef(abs(v[2]), '\\sqrt{%s}' % v[3], bpc=1))
    outils.ecrit_tex(f1, '%s^2%s2\\times%s\\times%s+%s^2' % a, tabs=3)
    a = (v[0] ** 2, v[1], tex_coef((2 * v[0]) * v[2], '\\sqrt{%s}' % (v[1] *
         v[3]), bplus=1), v[2] ** 2, v[3])
    outils.ecrit_tex(f1, '%s\\times %s %s+%s\\times %s' % a, tabs=3)
    a = (v[0] ** 2 * v[1] + v[2] ** 2 * v[3], tex_coef((2 * v[0]) * v[2],
         '\\sqrt{%s}' % (v[1] * v[3]), bplus=1))
    outils.ecrit_tex(f1, '%s%s' % a, cadre=1, tabs=3)


def valeurs_entier0(pyromax):  # renvoie (coef0, coef1, coef2, carre0, carre1, carre2, b)
    a = carres[random.randrange(len(carres))]
    while True:
        b = random.randrange(2, pyromax)
        c = outils.valeur_alea(-pyromax, pyromax)
        if b != c and abs(c) != 1:
            break
    return (b, c, a)


def exo_entier0(f0, f1, v):
    a = (v[0], tex_coef(v[1], '\\sqrt{%s}' % v[2], bplus=1), v[0],
         tex_coef(-v[1], '\\sqrt{%s}' % v[2], bplus=1))
    outils.ecrit_tex(f0, '\\left( %s%s \\right)\\left( %s%s \\right)' %
                     a, tabs=3)
    outils.ecrit_tex(f1, '\\left( %s%s \\right)\\left( %s%s \\right)' %
                     a, tabs=3)
    a = (tex_coef(v[0], '', bpc=1), tex_coef(abs(v[1]), '\\sqrt{%s}' % v[2],
         bpc=1))
    outils.ecrit_tex(f1, '%s^2-%s^2' % a, tabs=3)
    a = (v[0] ** 2, v[1] ** 2, v[2])
    outils.ecrit_tex(f1, '%s-%s\\times %s' % a, tabs=3)
    outils.ecrit_tex(f1, '%s' % (v[0] ** 2 - v[1] ** 2 * v[2]), cadre=1,
                     tabs=3)


def valeurs_entier1(pyromax):  # renvoie (coef0, coef1, coef2, carre0, carre1, carre2, b)
    a = carres[random.randrange(len(carres))]
    while True:
        v0 = random.randrange(2, pyromax)
        v1 = random.randrange(2, pyromax)
        b0 = random.randrange(2, pyromax)
        b1 = random.randrange(2, pyromax)
        a0 = (b1 * v0) * v1
        a1 = v1 * b0
        if b0 < b1 and outils.pgcd(a0, a1) != a1:
            break
    return (a0, b0, a1, b1, a)


def exo_entier1(f0, f1, v):
    a = (tex_coef(v[0], '\\sqrt{%s}' % (v[1] ** 2 * v[4])), tex_coef(v[2],
         '\\sqrt{%s}' % (v[3] ** 2 * v[4])))
    outils.ecrit_tex(f0, '\\frac{%s}{%s}' % a, tabs=3)
    outils.ecrit_tex(f1, '\\frac{%s}{%s}' % a, tabs=3)
    a = (v[0], v[1] ** 2, v[4], v[2], v[3] ** 2, v[4])
    outils.ecrit_tex(f1,
                     '\\frac{%s\\times\\sqrt{%s}\\times\\cancel{\\sqrt{%s}}}{%s\\times\\sqrt{%s}\\times\\cancel{\\sqrt{%s}}}' %
                     a, tabs=3)
    outils.ecrit_tex(f1, '\\frac{%s\\times %s}{%s\\times %s}' % v[0:4],
                     tabs=3)
    outils.ecrit_tex(f1, '%s' % (((v[0] * v[1]) // v[2]) // v[3]), cadre=1,
                     tabs=3)
