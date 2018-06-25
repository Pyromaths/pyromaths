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

from __future__ import division
from __future__ import unicode_literals

import math
from builtins import range
from builtins import str
from random import choice, randrange

from pyromaths.outils.Arithmetique import pgcd, valeur_alea


#
# ------------------- PUISSANCES -------------------


def tex_puissances_0(a):
    if isinstance(a, tuple):
        return '\\cfrac{\\nombre{%s} \\times 10^{%s} \\times \\nombre{%s} \\times 10^{%s}}{\\nombre{%s} \\times \\big( 10^{%s} \\big) ^%s}' % \
               (a[0], a[3], a[1], a[4], a[2], a[5], a[6])


def tex_puissances_1(a):
    if isinstance(a, tuple):
        if a[4] < 0:
            return '\\cfrac{\\nombre{%s} \\times \\nombre{%s}}{\\nombre{%s}} \\times \\cfrac{10^{%s+(%s)}}{10^{%s \\times %s}}' % \
                   (a[0], a[1], a[2], a[3], a[4], a[5], a[6])
        else:
            return '\\cfrac{\\nombre{%s} \\times \\nombre{%s}}{\\nombre{%s}} \\times \\cfrac{10^{%s+%s}}{10^{%s \\times %s}}' % \
                   (a[0], a[1], a[2], a[3], a[4], a[5], a[6])


def tex_puissances_2(a):
    if isinstance(a, tuple):
        if a[0] * a[1] / a[2] == a[0] * a[1] // a[2]:
            if a[5] * a[6] < 0:
                return '\\nombre{%s} \\times 10^{%s-(%s)}' % \
                       verifie_type((a[0] * a[1] // a[2], a[3] + a[4], a[5] * a[6]))
            else:
                return '\\nombre{%s} \\times 10^{%s-%s}' % verifie_type((a[0] * a[1] // a[2], a[3] + a[4], a[5] * a[6]))
        else:
            if a[5] * a[6] < 0:
                return '\\nombre{%s} \\times 10^{%s-(%s)}' % \
                       verifie_type((a[0] * a[1] / a[2], a[3] + a[4], a[5] * a[6]))
            else:
                return '\\nombre{%s} \\times 10^{%s-%s}' % verifie_type((a[0] * a[1] / a[2], a[3] + a[4], a[5] * a[6]))


def tex_puissances_3(a):
    from math import floor, log10
    b = int(floor(log10(a[0] * a[1] / a[2])))
    if isinstance(a, tuple) and b != 0:
        return '\\nombre{%s}  \\times 10^{%s} \\times 10^{%s}' % \
               verifie_type((a[0] * a[1] / a[2] / 10 ** b, b, (a[3] + a[4]) - a[5] * a[6]))


def tex_puissances_4(a):
    from math import floor, log10
    b = int(floor(log10(a[0] * a[1] / a[2])))
    if isinstance(a, tuple):
        return '\\nombre{%s}  \\times 10^{%s}' % verifie_type(
            (a[0] * a[1] / a[2] / 10 ** b, (b + a[3] + a[4]) - a[5] * a[6]))


def verifie_type(
        a):  # verifie si des nombres reels dans le tuple a sont en fait des nombres entiers et change leur type
    list = []
    for i in range(len(a)):
        if str(a[i]).endswith('.0'):
            list.append(int(a[i] + .1))
        else:
            list.append(a[i])
    return tuple(list)


def valeurs_puissances():  # renvoie un tuple contenant les valeurs pour les deux exercices sur les puissances
    from math import floor, log10
    (maxi, emax) = (10, 2)
    while True:
        (b1, b2) = (valeur_alea(2, maxi), valeur_alea(2, maxi))
        (b1, b2) = (b1 // pgcd(b1, b2), b2 // pgcd(b1, b2))
        if b1 != 1 and b2 != 1:
            break
    while True:
        (n1, n2) = ((b1 * valeur_alea(2, maxi)) * 10 ** randrange(-emax, emax),
                    (b2 * valeur_alea(2, maxi)) * 10 ** randrange(-emax, emax))
        n3 = ((b1 * b2) * choice((2, 4, 5, 8))) * 10 ** randrange(-emax, emax)
        if int(floor(log10(n1 * n2 / n3))) != 0 and n1 != 1 and n2 != 1 and n3 != 1:
            break
    (e1, e2, e3, e4) = (valeur_alea(-10, 10), valeur_alea(-10, 10), valeur_alea(2, 10), valeur_alea(2, 5))
    a = verifie_type((n1, n2, n3, e1, e2, e3, e4))
    while True:
        (b1, b2) = (valeur_alea(2, maxi), valeur_alea(2, maxi))
        (b1, b2) = (b1 // pgcd(b1, b2), b2 // pgcd(b1, b2))
        if b1 != 1 and b2 != 1:
            break
    (n1, n2) = ((b1 * valeur_alea(2, maxi)) * 10 ** randrange(-emax, emax + 1),
                (b2 * valeur_alea(2, maxi)) * 10 ** randrange(-emax, emax + 1))
    n3 = ((b1 * b2) * choice((1, 2, 4, 5, 8))) * 10 ** randrange(-emax, emax + 1)
    (e1, e2, e3, e4) = (valeur_alea(-10, 10), valeur_alea(-10, 10), valeur_alea(-10, -2), valeur_alea(2, 5))
    b = verifie_type((n1, n2, n3, e1, e2, e3, e4))
    return a, b


def tex_puissances():
    sd = str.maketrans('.', ',')  # convertit les . en , (separateur decimal)
    valeurs = valeurs_puissances()
    i = randrange(2)
    exo = ['\\exercice''', u"Calculer les expressions suivantes et donner l'écriture scientifique du résultat."]
    exo.append('\\begin{multicols}{2}\\noindent')
    cor = ['\\exercice*''', u"Calculer les expressions suivantes et donner l'écriture scientifique du résultat."]
    cor.append('\\begin{multicols}{2}\\noindent')
    exo.append(u'\\[ \\thenocalcul = ' + tex_puissances_0(valeurs[i]).translate(sd) + '\\] ')
    cor.append(u'\\[ \\thenocalcul = ' + tex_puissances_0(valeurs[i]).translate(sd) + '\\] ')
    cor.append(u'\\[ \\thenocalcul = ' + tex_puissances_1(valeurs[i]).translate(sd) + '\\] ')
    cor.append(u'\\[ \\thenocalcul = ' + tex_puissances_2(valeurs[i]).translate(sd) + '\\] ')
    if int(math.floor(math.log10(valeurs[i][0] * valeurs[i][1] / valeurs[i][2]))) != 0:
        cor.append(u'\\[ \\thenocalcul = ' + tex_puissances_3(valeurs[i]).translate(sd) + '\\] ')
    cor.append(u'\\[ \\boxed{\\thenocalcul = ' + tex_puissances_4(valeurs[i]).translate(sd) + '} \\] ')
    exo.append('\\columnbreak\\stepcounter{nocalcul}%')
    cor.append('\\columnbreak\\stepcounter{nocalcul}%')
    exo.append(u'\\[ \\thenocalcul = ' + tex_puissances_0(valeurs[1 - i]).translate(sd) + '\\] ')
    cor.append(u'\\[ \\thenocalcul = ' + tex_puissances_0(valeurs[1 - i]).translate(sd) + '\\] ')
    cor.append(u'\\[ \\thenocalcul = ' + tex_puissances_1(valeurs[1 - i]).translate(sd) + '\\] ')
    cor.append(u'\\[ \\thenocalcul = ' + tex_puissances_2(valeurs[1 - i]).translate(sd) + '\\] ')
    if int(math.floor(math.log10(valeurs[1 - i][0] * valeurs[1 - i][1] / valeurs[1 - i][2]))) != 0:
        cor.append(u'\\[ \\thenocalcul = ' + tex_puissances_3(valeurs[1 - i]).translate(sd) + '\\] ')
    cor.append(u'\\[ \\boxed{\\thenocalcul = ' + tex_puissances_4(valeurs[1 - i]).translate(sd) + '} \\] ')
    exo.append('\\end{multicols}')
    cor.append('\\end{multicols}')
    return exo, cor


tex_puissances.description = u'Puissances'
