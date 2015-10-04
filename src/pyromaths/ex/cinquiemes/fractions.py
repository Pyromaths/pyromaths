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

# from pyromaths.classes.Fractions import Fraction  # Fractions de pyromaths
import random
from pyromaths.outils import Arithmetique
from pyromaths.outils.Priorites3 import texify, priorites


def fractions_egales():
    exo = ["\\exercice", _(u"Compléter :"), "\\begin{multicols}{4}",
           "  \\begin{enumerate}"]
    cor = ["\\exercice*", _(u"Compléter :"), "\\begin{multicols}{4}",
           "  \\begin{enumerate}"]
    for dummy in range(8):
        n = d = 1
        while n == d:
            n = random.randrange(1, 11)
            d = random.randrange(2, 11)
        c = random.randrange(2, 11)
        cas = random.randrange(2)
        if cas:
            enonce = [n, d, n * c, d * c]
            solution = [n, d, n * c, d * c]
        else:
            enonce = [n * c, d * c, n, d]
            solution = [n * c, d * c, n, d]
        trou = random.randrange(4)
        enonce[trou] = "\\ldots"
        solution[trou] = "\\mathbf{%s}" % solution[trou]
        if cas:
            solution.insert(2, c)
            solution.insert(1, c)
        else:
            solution.insert(4, c)
            solution.insert(3, c)
        exo.append("\\item $\\dfrac{%s}{%s}=\\dfrac{%s}{%s}$" %
                   tuple(enonce))
        if cas:
            cor.append("\\item $\\dfrac{%s_{(\\times %s)}}{%s_{(\\times %s)}}=\\dfrac{%s}{%s}$" %
                       tuple(solution))
        else:
            cor.append("\\item $\\dfrac{%s}{%s}=\\dfrac{%s_{(\\times %s)}}{%s_{(\\times %s)}}$" %
                       tuple(solution))
    exo.extend(["  \\end{enumerate}", "\end{multicols}\n"])
    cor.extend(["  \\end{enumerate}", "\end{multicols}\n"])
    return (exo, cor)

fractions_egales.description = u'Fractions égales'


def valeurs_somme():
    """Travail sur les sommes de fractions en cinquième"""
    l = []

    for dummy in range(2):
        op = "+-"[random.randrange(2)]
        n2, d2 = random.randrange(1, 11), random.randrange(2, 11)
        if op == "-" and 1 - n2 / d2 > 0:
            l.append(_('1 %s Fraction(%s, %s)') % (op, n2, d2))
        else:
            l.append(_('Fraction(%s, %s) %s 1') % (n2, d2, op))

    for dummy in range(2):
        op = "+-"[random.randrange(2)]
        n1 = random.randrange(2, 11)
        n2, d2 = random.randrange(1, 11), random.randrange(2, 11)
        if op == "-" and n1 - n2 / d2 > 0:
            l.append(_('%s %s Fraction(%s, %s)') % (n1, op, n2, d2))
        else:
            l.append(_('Fraction(%s, %s) %s %s') % (n2, d2, op, n1))

    op = "+-"[random.randrange(2)]
    n1 = random.randrange(1, 11)
    n2, d2 = random.randrange(1, 11), random.randrange(2, 11)
    if op == "-" and n1 - n2 > 0:
        l.append(_('Fraction(%s, %s) %s Fraction(%s, %s)') % (n1, d2, op, n2, d2))
    else:
        l.append(_('Fraction(%s, %s) %s Fraction(%s, %s)') % (n2, d2, op, n1, d2))

    for dummy in range(3):
        op = "+-"[random.randrange(2)]
        n1, d1 = random.randrange(1, 11), random.randrange(2, 11)
        n2, d2 = random.randrange(1, 11), random.randrange(2, 11) * d1
        if op == "-" and n1 / d1 - n2 / d2 > 0:
            l.append(_('Fraction(%s, %s) %s Fraction(%s, %s)') % (n1, d1, op, n2, d2))
        else:
            l.append(_('Fraction(%s, %s) %s Fraction(%s, %s)') % (n2, d2, op, n1, d1))

    random.shuffle(l)
    return l


def sommes_fractions():
    exo = [_("\\exercice"),
           _(u"Calculer en détaillant les étapes. Donner le résultat sous la forme d’une fraction la plus simple possible (ou d’un entier lorsque c’est possible)."),
           "\\begin{multicols}{4}", "  \\begin{enumerate}"]
    cor = [_("\\exercice*"),
           _(u"Calculer en détaillant les étapes. Donner le résultat sous la forme d’une fraction la plus simple possible (ou d’un entier lorsque c’est possible)."),
           "\\begin{multicols}{4}", "  \\begin{enumerate}"]
    lexo = valeurs_somme()
    for question in lexo:
        solve = [question]
        exo.append("\\item $\\thenocalcul = " + texify(solve)[0] + "$")
        cor.append("\\item $\\thenocalcul = " + texify(solve)[0] + "$")
        solve = priorites(question)
        solve = texify(solve)
        for e in solve:
            cor.append("\\[\\thenocalcul = " + e + "\\]")
        exo.append("\\stepcounter{nocalcul}")
        cor.append("\\stepcounter{nocalcul}")
    exo.extend(["  \\end{enumerate}", "\\end{multicols}"])
    cor.extend(["  \\end{enumerate}", "\\end{multicols}"])
    return (exo, cor)

sommes_fractions.description = _(u'Sommes de fractions')


def valeurs_produit():
    l = []

    for dummy in range(4):
        n1 = d1 = n2 = d2 = a = b = 2
        while Arithmetique.pgcd(a, b) > 1:
            a = random.randrange(1, 11)
            b = random.randrange(2, 11)
        while Arithmetique.pgcd(n1 * a, d1 * b) > 1:
            n1 = random.randrange(1, 11)
            d1 = random.randrange(2, 11)
        while Arithmetique.pgcd(n2 * b, d2 * a) > 1:
            n2 = random.randrange(1, 11)
            d2 = random.randrange(2, 11)

        l.append(_('Fraction(%s, %s)*Fraction(%s,%s)') % (n1 * a, d1 * b, n2 * b, d2 * a))

    return l

def produits_fractions():
    exo = ["\\exercice",
           _(u"Calculer en détaillant les étapes. Donner le résultat sous la forme d’une fraction la plus simple possible (ou d’un entier lorsque c’est possible)."),
           "\\begin{multicols}{4}", "  \\begin{enumerate}"]
    cor = ["\\exercice*",
           _(u"Calculer en détaillant les étapes. Donner le résultat sous la forme d’une fraction la plus simple possible (ou d’un entier lorsque c’est possible)."),
           "\\begin{multicols}{4}", "  \\begin{enumerate}"]
    lexo = valeurs_produit()
    for question in lexo:
        solve = [question]
        exo.append("\\item $\\thenocalcul = " + texify(solve)[0] + "$")
        cor.append("\\item $\\thenocalcul = " + texify(solve)[0] + "$")
        solve = priorites(question)
        solve = texify(solve)
        for e in solve:
            cor.append("\\[\\thenocalcul = " + e + "\\]")
        exo.append("\\stepcounter{nocalcul}")
        cor.append("\\stepcounter{nocalcul}")
    exo.extend(["  \\end{enumerate}", "\\end{multicols}"])
    cor.extend(["  \\end{enumerate}", "\\end{multicols}"])

    return (exo, cor)

produits_fractions.description = _(u'Produits de fractions')
