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

from pyro_classes import Fractions
import random
import string
import outils


def fractions_egales():
    exo = ["\\exercice", "Compléter :", "\\begin{multicols}{4}",
           "  \\begin{enumerate}"]
    cor = ["\\exercice*", "Compléter :", "\\begin{multicols}{4}",
           "  \\begin{enumerate}"]
    for i in range(8):
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
        exo.append("    \\item $\\dfrac{%s}{%s}=\\dfrac{%s}{%s}$" %
                   tuple(enonce))
        if cas:
            cor.append("    \\item $\\dfrac{%s_{(\\times %s)}}{%s_{(\\times %s)}}=\\dfrac{%s}{%s}$" %
                       tuple(solution))
        else:
            cor.append("    \\item $\\dfrac{%s}{%s}=\\dfrac{%s_{(\\times %s)}}{%s_{(\\times %s)}}$" %
                       tuple(solution))
    exo.extend(["  \\end{enumerate}", "\end{multicols}\n"])
    cor.extend(["  \\end{enumerate}", "\end{multicols}\n"])
    return (exo, cor)


def sommes_fractions():
    exo = ["\\exercice",
           "Effectuer les calculs suivants et donner le résultat sous la forme d'une fraction simplifiée :",
           "\\begin{multicols}{4}", "  \\noindent"]
    cor = ["\\exercice*",
           "Effectuer les calculs suivants et donner le résultat sous la forme d'une fraction simplifiée :",
           "\\begin{multicols}{4}", "  \\noindent"]
    for i in range(8):
        if random.randrange(2):
            s = "+"
        else:
            s = "-"
        n = d = c = n2 = 2
        while outils.pgcd(n, d) > 1:
            n = random.randrange(1, 11)
            d = random.randrange(2, 11)
        while outils.pgcd(n2, d * c) > 1:
            c = random.randrange(2, 11)
            n2 = random.randrange(2, 11)
        fr1 = Fractions(n, d)
        fr2 = Fractions(n2, d * c)
        if s == "-" and (fr1 - fr2).n * (fr1 - fr2).d < 0 or s == "+" and \
            random.randrange(2):
            (fr1, fr2) = (fr2, fr1)
        exo.append("  \\[ \\thenocalcul = %s%s%s \\]" % (Fractions.TeX(fr1),
                   s, Fractions.TeX(fr2)))
        cor.append("  \\[ \\thenocalcul = %s%s%s \\]" % (Fractions.TeX(fr1),
                   s, Fractions.TeX(fr2)))
        if fr1.d < fr2.d:
            cor.append("  \\[ \\thenocalcul = %s%s%s \\]" % (Fractions.TeX(fr1,
                       coef=c), s, Fractions.TeX(fr2)))
        else:
            cor.append("  \\[ \\thenocalcul = %s%s%s \\]" % (Fractions.TeX(fr1),
                       s, Fractions.TeX(fr2, coef=c)))
        if s == "+":
            fr = fr1 + fr2
        else:
            fr = fr1 - fr2
        frs = Fractions.simplifie(fr)
        if frs.d != fr.d:
            cor.append("  \\[ \\thenocalcul = %s \\]" % Fractions.TeX(frs,
                       coef=fr.d // frs.d))
            cor.append("  \\[ \\boxed{\\thenocalcul = %s} \\]" %
                       Fractions.TeX(frs))
        else:
            cor.append("  \\[ \\boxed{\\thenocalcul = %s} \\]" %
                       Fractions.TeX(fr))
        exo.append("  \\stepcounter{nocalcul}%")
        cor.append("  \\stepcounter{nocalcul}%")
    exo.append("\end{multicols}\n")
    cor.append("\end{multicols}\n")
    return (exo, cor)


def produits_fractions():
    exo = ["\\exercice",
           "Effectuer les calculs suivants et donner le résultat sous la forme d'une fraction simplifiée :",
           "\\begin{multicols}{4}", "  \\noindent"]
    cor = ["\\exercice*",
           "Effectuer les calculs suivants et donner le résultat sous la forme d'une fraction simplifiée :",
           "\\begin{multicols}{4}", "  \\noindent"]
    for i in range(8):
        n1=d1=n2=d2=a=b=2
        while outils.pgcd(a,b)>1:
            a=random.randrange(1,11)
            b=random.randrange(2,11)
        while outils.pgcd(n1*a,d1*b)>1:
            n1=random.randrange(1,11)
            d1=random.randrange(2,11)
        while outils.pgcd(n2*b,d2*a)>1:
            n2=random.randrange(1,11)
            d2=random.randrange(2,11)

        fr1 = Fractions(n1*a, d1*b)
        fr2 = Fractions(n2*b, d2*a)
        exo.append("  \\[ \\thenocalcul = %s \\times %s \\]" % (Fractions.TeX(fr1),
                   Fractions.TeX(fr2)))
        cor.append("  \\[ \\thenocalcul = %s \\times %s \\]" % (Fractions.TeX(fr1),
                   Fractions.TeX(fr2)))
        fr1s = Fractions.simplifie(fr1)
        fr2s = Fractions.simplifie(fr2)
        if abs(fr1s.d) < abs(fr1.d) or abs(fr2s.d) < abs(fr2.d):
            cor.append("  \\[ \\thenocalcul = %s \\times %s \\]" % (Fractions.TeXSimplifie(fr1),
                       Fractions.TeXSimplifie(fr2)))
        fr = fr1s * fr2s
        frs = Fractions.simplifie(fr)
        if abs(frs.d) < abs(fr.d):
            cor.append("  \\[ \\thenocalcul = %s \\]" % Fractions.TeXProduit(fr1s,
                       fr2s))
        cor.append("  \\[ \\boxed{\\thenocalcul = %s} \\]" % Fractions.TeX(frs))
        exo.append("  \\stepcounter{nocalcul}%")
        cor.append("  \\stepcounter{nocalcul}%")
    exo.append("\end{multicols}\n")
    cor.append("\end{multicols}\n")
    return (exo, cor)


