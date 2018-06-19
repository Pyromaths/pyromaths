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

from __future__ import division
from __future__ import unicode_literals
from builtins import str
from builtins import range
from past.utils import old_div
from pyromaths.outils.Arithmetique import pgcd, valeur_alea
from pyromaths.outils.Affichage import decimaux, tex_coef
from random import choice, randrange
import string


def tex_proprietes_val(exp_max, nb_max, typeexo):
    """
    Renvoie des valeurs pour l'exercice sur les propriétés des puissances
    @param exp_max: valeur maximale pour les exposants
    @type exp_max: Integer
    @param nb_max: Valeur maximale pour les nombres
    @type nb_max: integer
    @param typeexo: 0 : 2 exposants et 1 nombre ; 1 : 1 exposant et 2 nombres
    @type typeexo: integer
    """

    if typeexo:
        while 1:
            nb1 = randrange(2, nb_max)
            nb2 = randrange(2, nb_max)
            exp1 = randrange(2, exp_max)
            exp2 = exp1
            if nb1 != nb2:
                break
    else:
        while 1:
            nb1 = randrange(2, nb_max)
            nb2 = nb1
            exp1 = randrange(2, exp_max)
            exp2 = randrange(2, exp_max)
            if exp1 != exp2:
                break
    return (nb1, exp1, nb2, exp2)


def tex_proprietes():
    exo = ["\\exercice",
           u"Compléter par un nombre de la forme $a^n$ avec $a$ et $n$ entiers :",
           "\\begin{multicols}{4}", "  \\noindent%",
           "  \\begin{enumerate}"]
    cor = ["\\exercice*",
           u"Compléter par un nombre de la forme $a^n$ avec $a$ et $n$ entiers :",
           "\\begin{multicols}{4}", "  \\noindent%",
           "  \\begin{enumerate}"]
    lexos = [0, 1, 2, 3, 0, 1, 2, 3]

    # 0: a^n*a^p ; 1: (a^n)^p ; 2:a^n/a^p ; 3: a^n*b^n

    for dummy in range(len(lexos)):
        j = lexos.pop(randrange(len(lexos)))
        if j == 3:
            lval = tex_proprietes_val(12, 12, 1)
            exo.append("\\item $%s^{%s} \\times %s^{%s} = \\dotfill$" % 
                       lval)
            cor.append("\\item $%s^{%s}\\times%s^{%s}=" % lval)
            cor.append("%s^{%s}$" % (lval[0] * lval[2], lval[1]))
        else:
            lval = tex_proprietes_val(12, 12, 0)
            if j == 0:
                exo.append("\\item $%s^{%s}\\times%s^{%s}=\\dotfill$" % 
                           lval)
                cor.append("\\item $%s^{%s}\\times%s^{%s}=" % lval)
                cor.append("%s^{%s}$" % (lval[0], lval[1] + lval[3]))
            elif j == 1:
                exo.append("\\item $(%s^{%s})^{%s}=\\dotfill$" % (lval[0],
                           lval[1], lval[3]))
                cor.append("\\item $(%s^{%s})^{%s}=" % (lval[0],
                           lval[1], lval[3]))
                cor.append("%s^{%s}$" % (lval[0], lval[1] * lval[3]))
            elif j == 2:
                while lval[1] - lval[3] < 3:
                    lval = tex_proprietes_val(12, 12, 0)
                exo.append("\\item $\\dfrac{%s^{%s}}{%s^{%s}}=\\dotfill$" % 
                           lval)
                cor.append("\\item $\\dfrac{%s^{%s}}{%s^{%s}}=" % 
                           lval)
                cor.append("%s^{%s}$" % (lval[0], lval[1] - lval[3]))
    exo.append("\\end{enumerate}")
    exo.append("\\end{multicols}\n")
    cor.append("\\end{enumerate}")
    cor.append("\\end{multicols}\n")
    return (exo, cor)

tex_proprietes.description = u'Propriétés sur les puissances'


# ----PROPRIETES AVEC 10


def tex_proprietes_neg_val(exp_max, nb_max, typeexo):
    """
    Renvoie des valeurs pour l'exercice sur les propriétés des puissances
    @param exp_max: valeur maximale pour les exposants
    @type exp_max: Integer
    @param nb_max: Valeur maximale pour les nombres
    @type nb_max: integer
    @param typeexo: 0 : 2 exposants et 1 nombre ; 1 : 1 exposant et 2 nombres
    @type typeexo: integer
    """

    if typeexo:
        while 1:
            nb1 = randrange(2, nb_max)
            nb2 = randrange(2, nb_max)
            exp1 = randrange(2, exp_max)
            exp2 = exp1
            if nb1 != nb2:
                break
    else:
        while 1:
            nb1 = randrange(2, nb_max)
            nb2 = nb1
            exp1 = randrange(2, exp_max)
            exp2 = randrange(2, exp_max)
            if exp1 != exp2:
                break
    return (nb1, exp1, nb2, exp2)


def tex_proprietes_neg():
    exo = ["\\exercice",
           u"Écrire sous la forme d'une puissance de 10 puis donner l'écriture",
           u" décimale de ces nombres :", "\\begin{multicols}{2}",
           "  \\noindent%", "  \\begin{enumerate}"]
    cor = ["\\exercice*",
           u"Écrire sous la forme d'une puissance de 10 puis donner l'écriture",
           u" décimale de ces nombres :", "\\begin{multicols}{2}",
           "  \\noindent%", "  \\begin{enumerate}"]
    lexos = [0, 1, 2, 3, 0, 1, 2, 3]

    # 0: a^n*a^p ; 1: (a^n)^p ; 2:a^n/a^p

    for dummy in range(len(lexos)):
        lexp = [randrange(-6, 6) for dummy in range(2)]
        j = lexos.pop(randrange(len(lexos)))

        # FIXME : À finir

        if j == 0:
            while abs(lexp[0] + lexp[1]) > 10:
                lexp = [randrange(-6, 6) for dummy in range(2)]
            exo.append("\\item $10^{%s} \\times 10^{%s} = \\dotfill$" % 
                       tuple(lexp))
            cor.append("\\item $10^{%s}\\times 10^{%s}=" % tuple(lexp))
            cor.append("10^{%s+%s}=" % (lexp[0], tex_coef(lexp[1],
                       '', bpn=1)))
            cor.append("10^{%s}=%s$" % (lexp[0] + lexp[1],
                       decimaux(10 ** (lexp[0] + lexp[1]), 1)))
        elif j == 1:
            while abs(lexp[0] * lexp[1]) > 10:
                lexp = [randrange(-6, 6) for dummy in range(2)]
            exo.append("\\item $(10^{%s})^{%s}=\\dotfill$" % (lexp[0],
                       lexp[1]))
            cor.append("\\item $(10^{%s})^{%s}=" % tuple(lexp))
            cor.append("10^{%s \\times %s}=" % (lexp[0], tex_coef(lexp[1],
                       '', bpn=1)))
            cor.append("10^{%s}=%s$" % (lexp[0] * lexp[1],
                       decimaux(10 ** (lexp[0] * lexp[1]), 1)))
        elif j == 2:
            while abs(lexp[0] - lexp[1]) > 10:
                lexp = [randrange(-6, 6) for dummy in range(2)]
            exo.append("\\item $\\dfrac{10^{%s}}{10^{%s}}=\\dotfill$" % 
                       tuple(lexp))
            cor.append("\\item $\\dfrac{10^{%s}}{10^{%s}}=" % tuple(lexp))
            cor.append("10^{%s-%s}=" % (lexp[0], tex_coef(lexp[1],
                       '', bpn=1)))
            cor.append("10^{%s}=%s$" % (lexp[0] - lexp[1],
                       decimaux(10 ** (lexp[0] - lexp[1]), 1)))
    exo.append("\\end{enumerate}")
    exo.append("\\end{multicols}\n")
    cor.append("\\end{enumerate}")
    cor.append("\\end{multicols}\n")
    return (exo, cor)

tex_proprietes_neg.description = u'Propriétés sur les puissances de 10'


#------------------------------------------------------------------------------
#  Écritures scientifiques
#------------------------------------------------------------------------------


def val_sc():
    while True:
        a = randrange(10) * 1000 + randrange(10) + randrange(10) * 10 ** \
            (randrange(2) + 1)
        a = a * 10 ** randrange(-9, 6)

        # a=randrange(1,9999)*10**randrange(-9,6)

        if a >= 10 or (a < 1 and a > 0) :
            break
    return a


def ecr_sc():
    from math import log10, floor
    exo = ["\\exercice", u"Compléter par le nombre qui convient :",
           "\\begin{multicols}{3}", "  \\noindent%",
           "  \\begin{enumerate}"]
    cor = ["\\exercice*",
           u"Compléter par le nombre qui convient :",
           "\\begin{multicols}{3}", "  \\noindent%",
           "  \\begin{enumerate}"]
    for dummy in range(6):
        a = val_sc()
        exp = int(floor(log10(a)))
        a_sc = old_div((a * 1.), 10 ** exp)
        s_a = decimaux(a, 1)
        s_a_sc = decimaux(a_sc, 1)
        if randrange(2):  # forme : a=a_sc*...
            exo.append("\\item $%s=%s\\times\\dotfill$" % (s_a,
                       s_a_sc))
            cor.append("\\item $%s=%s\\times\\mathbf{10^{%s}}$" % (s_a,
                       s_a_sc, decimaux(exp, 1)))
        else:
            # forme : a_sc*...=a
            exo.append("\\item $%s\\times\\dotfill=%s$" % (s_a_sc,
                       s_a))
            cor.append("\\item $%s\\times\\mathbf{10^{%s}}=%s$" % (s_a_sc,
                       decimaux(exp, 1), s_a))
    exo.append("\\end{enumerate}")
    exo.append("\\end{multicols}\n")
    cor.append("\\end{enumerate}")
    cor.append("\\end{multicols}\n")
    return (exo, cor)

ecr_sc.description = u'Écritures scientifiques'


# ------------------- PUISSANCES de 10 -------------------


def exo_puissances():
    from math import floor, log10
    sd = string.maketrans('.', ',')  # convertit les . en , (separateur decimal)
    exo = ["\\exercice",
           u"Calculer les expressions suivantes et donner l'écriture scientifique du résultat.",
           "\\begin{multicols}{2}", "  \\noindent%"]
    cor = ["\\exercice*",
           u"Calculer les expressions suivantes et donner l'écriture scientifique du résultat.",
           "\\begin{multicols}{2}", "  \\noindent%"]
    valeurs = valeurs_puissances()
    i = randrange(2)
    exo.append("\\[ \\thenocalcul = %s \\]" % tex_puissances_0(valeurs[i]).translate(sd))
    cor.append("\\[ \\thenocalcul = %s \\]" % tex_puissances_0(valeurs[i]).translate(sd))
    cor.append("\\[ \\thenocalcul = %s \\]" % tex_puissances_1(valeurs[i]).translate(sd))
    cor.append("\\[ \\thenocalcul = %s \\]" % tex_puissances_2(valeurs[i]).translate(sd))
    if int(floor(log10(old_div(((valeurs[i][0] * valeurs[i][1]) * 1.), valeurs[i][2])))) != \
        0:
        cor.append("\\[ \\thenocalcul = %s \\]" % tex_puissances_3(valeurs[i]).translate(sd))
    cor.append("\\[ \\boxed{\\thenocalcul = %s} \\]" % 
               tex_puissances_4(valeurs[i]).translate(sd))
    exo.append("\\columnbreak\\stepcounter{nocalcul}%")
    cor.append("\\columnbreak\\stepcounter{nocalcul}%")
    exo.append("\\[ \\thenocalcul = %s \\]" % tex_puissances_0(valeurs[1 - 
               i]).translate(sd))
    cor.append("\\[ \\thenocalcul = %s \\]" % tex_puissances_0(valeurs[1 - 
               i]).translate(sd))
    cor.append("\\[ \\thenocalcul = %s \\]" % tex_puissances_1(valeurs[1 - 
               i]).translate(sd))
    cor.append("\\[ \\thenocalcul = %s \\]" % tex_puissances_2(valeurs[1 - 
               i]).translate(sd))
    if int(floor(log10(old_div(((valeurs[1 - i][0] * valeurs[1 - i][1]) * 1.), 
           valeurs[1 - i][2])))) != 0:
        cor.append("\\[ \\thenocalcul = %s \\]" % tex_puissances_3(valeurs[1 - 
                   i]).translate(sd))
        cor.append("\\[ \\boxed{\\thenocalcul = %s} \\]" % 
                   tex_puissances_4(valeurs[1 - i]).translate(sd))
    exo.append("\\end{multicols}\n")
    cor.append("\\end{multicols}\n")
    return (exo, cor)

exo_puissances.description = u'Puissances de 10'


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
        if old_div(((a[0] * a[1]) * 1.), a[2]) == old_div((a[0] * a[1]), a[2]):
            if a[5] * a[6] < 0:
                return '\\nombre{%s} \\times 10^{%s-(%s)}' % \
                    verifie_type((old_div((a[0] * a[1]), a[2]), a[3] + a[4], a[5] * 
                                 a[6]))
            else:
                return '\\nombre{%s} \\times 10^{%s-%s}' % verifie_type((old_div((a[0] * 
                        a[1]), a[2]), a[3] + a[4], a[5] * a[6]))
        else:
            if a[5] * a[6] < 0:
                return '\\nombre{%s} \\times 10^{%s-(%s)}' % \
                    verifie_type((old_div(((a[0] * a[1]) * 1.), a[2]), a[3] + a[4],
                                 a[5] * a[6]))
            else:
                return '\\nombre{%s} \\times 10^{%s-%s}' % verifie_type((old_div(((a[0] * 
                        a[1]) * 1.), a[2]), a[3] + a[4], a[5] * a[6]))


def tex_puissances_3(a):
    from math import floor, log10
    b = int(floor(log10(old_div(((a[0] * a[1]) * 1.), a[2]))))
    if isinstance(a, tuple) and b != 0:
        return '\\nombre{%s}  \\times 10^{%s} \\times 10^{%s}' % \
            verifie_type((old_div((old_div(((a[0] * a[1]) * 1.), a[2])), 10 ** b), b, (a[3] + 
                         a[4]) - a[5] * a[6]))


def tex_puissances_4(a):
    from math import floor, log10
    b = int(floor(log10(old_div(((a[0] * a[1]) * 1.), a[2]))))
    if isinstance(a, tuple):
        return '\\nombre{%s}  \\times 10^{%s}' % verifie_type((old_div((old_div(((a[0] * 
                a[1]) * 1.), a[2])), 10 ** b), (b + a[3] + a[4]) - a[5] * 
                a[6]))


def verifie_type(a):  # verifie si des nombres reels dans le tuple a sont en fait des nombres entiers et change leur type
    liste = []
    for i in range(len(a)):
        if str(a[i]).endswith('.0'):
            liste.append(int(a[i] + .1))
        else:
            liste.append(a[i])
    return tuple(liste)


def valeurs_puissances():  # renvoie un tuple contenant les valeurs pour les deux exercices sur les puissances
    from math import floor, log10
    (maxi, emax) = (10, 2)
    while True:
        (b1, b2) = (valeur_alea(2, maxi), valeur_alea(2, maxi))
        (b1, b2) = (old_div(b1, pgcd(b1, b2)), old_div(b2, pgcd(b1, b2)))
        if b1 != 1 and b2 != 1:
            break
    while True:
        (n1, n2) = ((b1 * valeur_alea(2, maxi)) * 10 ** randrange(-emax,
                    emax), (b2 * valeur_alea(2, maxi)) * 10 ** randrange(-emax,
                    emax))
        n3 = ((b1 * b2) * choice((2, 4, 5, 8))) * 10 ** randrange(-emax,
                emax)
        if int(floor(log10(old_div(((n1 * n2) * 1.), n3)))) != 0 and n1 != 1 and \
            n2 != 1 and n3 != 1:
            break
    (e1, e2, e3, e4) = (valeur_alea(-10, 10), valeur_alea(-10, 10),
                        valeur_alea(2, 10), valeur_alea(2, 5))
    a = verifie_type((n1, n2, n3, e1, e2, e3, e4))
    while True:
        (b1, b2) = (valeur_alea(2, maxi), valeur_alea(2, maxi))
        (b1, b2) = (old_div(b1, pgcd(b1, b2)), old_div(b2, pgcd(b1, b2)))
        if b1 != 1 and b2 != 1:
            break
    (n1, n2) = ((b1 * valeur_alea(2, maxi)) * 10 ** randrange(-emax, emax + 
                1), (b2 * valeur_alea(2, maxi)) * 10 ** randrange(-emax,
                emax + 1))
    n3 = ((b1 * b2) * choice((1, 2, 4, 5, 8))) * 10 ** randrange(-emax,
            emax + 1)
    (e1, e2, e3, e4) = (valeur_alea(-10, 10), valeur_alea(-10, 10),
                        valeur_alea(-10, -2), valeur_alea(2, 5))
    b = verifie_type((n1, n2, n3, e1, e2, e3, e4))
    return (a, b)
