#!/usr/bin/env python3
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
# Pyromaths : Initiation au calcul littéral
#----------------------------------------------------------------------
from __future__ import unicode_literals
from builtins import chr
from builtins import range
from pyromaths.outils.Priorites3 import texify, priorites, splitting
from random import randrange, shuffle
from pyromaths.ex import LegacyExercise

def valeurs_reduire():
    """Travail sur les bases du calcul littéral en quatrième"""
    var = "atxy"
    var = var[randrange(len(var))]
    op = "+*-*"[randrange(4)]
    if op == "*":
        deg1 = randrange(3)
        if deg1 == 2: deg2 = 0
        elif deg1 == 1: deg2 = randrange(2)
        else: deg2 = randrange(1, 3)
    else:
        deg1 = randrange(1, 3)
        deg2 = [i for i in range(3)]
        deg2.extend([deg1] * 7)
        shuffle(deg2)
        deg2 = deg2.pop(randrange(len(deg2)))
    a1, a2 = 0, 0
    while not a1 or not a2:
        a1 = randrange(-10, 11)
        a2 = randrange(-10, 11)
    p1 = "Polynome(\"%s%s^%s\", details=3)" % (a1, var, deg1)
    p2 = "Polynome(\"%s%s^%s\", details=3)" % (a2, var, deg2)
    return p1 + op + p2

def _reduire():
    """Travail sur les bases du calcul littéral en quatrième"""
    exo = ["\\exercice", u"Réduire, si possible, les expressions suivantes :",
           "\\begin{multicols}{3}\\noindent", "  \\begin{enumerate}"]
    cor = ["\\exercice*", u"Réduire, si possible, les expressions suivantes :",
           "\\begin{multicols}{3}\\noindent", "  \\begin{enumerate}"]
    for dummy in range(9):
        a = valeurs_reduire()
        solve = [a]
        exo.append("\\item $\\thenocalcul = " + texify(solve)[0] + "$")
        cor.append("\\item $\\thenocalcul = " + texify(solve)[0] + "$")
        solve = priorites(a)
        solve.insert(0, a)
        solve = texify(solve)
        if len(solve) > 1:
            for e in solve[1:]:
                cor.append("\\[\\thenocalcul = " + e + "\\]")
        exo.append("\\stepcounter{nocalcul}")
        cor.append("\\stepcounter{nocalcul}")
    exo.extend(["  \\end{enumerate}", "\\end{multicols}"])
    cor.extend(["  \\end{enumerate}", "\\end{multicols}"])
    return (exo, cor)

class reduire(LegacyExercise):
    """Bases du calcul littéral"""

    tags = ["quatrième"]
    function = _reduire

def _distributivite():
    """Crée un exercice permettant de s'entrainer sur la distributivité
    """
    lcalc, expr = [], []
    for i in range(2):
        tmp = ['Polynome([[%s, 1]], details=3)' % randrange(2, 10), 'Polynome([[%s, 0]], details=3)' % randrange(2, 10)]
        shuffle(tmp)
        lcalc.append(["*".join(tmp)])
        lcalc[i].extend(priorites(lcalc[i][0]))
        lcalc[i][0] = splitting(lcalc[i][0])
        expr.append(texify(lcalc[i]))
    tmp = [0, 1, 2]
    for i in range(2, 5):
        k = 'Polynome([[%s, 0]], details=3)' % randrange(2, 11)
        if i > 1:
            a = valeurs_reduire_somme(2)
        else:
            sgn = (-1) ** randrange(2)
            a = [[sgn, 1] for dummy2 in range(randrange(2, 5))]
            a.append([randrange(1, 11) * (-1) ** randrange(2), 0])
            a = 'Polynome(%s, var=\'x\', details=3)' % a
        exp = tmp.pop(randrange(len(tmp)))
        if exp != 2:
            b = 'Polynome([[%s, %s]], details=3)' % (randrange(1, 11) * (-1) ** randrange(3), exp)
        else:
            b = valeurs_reduire_somme(2)

        lpoly = [a, k]
        shuffle(lpoly)
        if randrange(2):lpoly.insert(0, b)
        else:lpoly.append(b)
        if b == lpoly[0]:
            lcalc.append(['%s+%s*%s' % (lpoly[0], lpoly[1], lpoly[2])])
        else:
            lcalc.append(['%s*%s+%s' % (lpoly[0], lpoly[1], lpoly[2])])
        lcalc[i].extend(priorites(lcalc[i][0]))
        lcalc[i][0] = splitting(lcalc[i][0])
        expr.append(texify(lcalc[i]))
    exo = ["\\exercice", u"Développer et réduire chacune des expressions littérales suivantes :"]
    exo.append("\\begin{multicols}{2}")
    cor = ["\\exercice*", u"Développer et réduire chacune des expressions littérales suivantes :"]
    cor.append("\\begin{multicols}{2}")

    for i in range(len(lcalc)):
        cor.append('\\\\\n'.join(['$%s=%s$' % (chr(i + 65), expr[i][j]) for j in range(len(expr[i]) - 1)]))
        cor.append('\\\\')
        cor.append('\\fbox{$%s=%s$}\\\\\n' % (chr(i + 65), expr[i][-1]))
    exo.append('\\\\\n'.join(['$%s=%s$' % (chr(i + 65), expr[i][0]) for i in range(len(expr))]))
    exo.append("\\end{multicols}")
    cor.append("\\end{multicols}")
    return exo, cor

class distributivite(LegacyExercise):
    """Distributivité"""

    tags = ["quatrième"]
    function = _distributivite

def _double_distributivite():
    """Crée un exercice permettant de s'entrainer sur la double distributivité
    """
    lcalc, expr = [], []
    for i in range(2):
        tmp = ['Polynome([[%s, 1]], details=3)' % ([1, randrange(2, 10)][i]), 'Polynome([[%s, 1]], details=3)' % randrange(2, 10)]
        shuffle(tmp)
        lcalc.append(["*".join(tmp)])
        lcalc[i].extend(priorites(lcalc[i][0]))
        lcalc[i][0] = splitting(lcalc[i][0])
        expr.append(texify(lcalc[i]))
    tmp = [0, 1, 2]
    for i in range(2, 5):
        a = valeurs_reduire_somme(2)
        b = valeurs_reduire_somme(2)
        exp = tmp.pop(randrange(len(tmp)))
        if exp != 1:
            c = 'Polynome([[%s, %s]], details=3)' % (randrange(1, 11) * (-1) ** randrange(3), exp)
        else:
            c = valeurs_reduire_somme(2)
        lpoly = [a, b]
        if randrange(2): lpoly.insert(0, c)
        else: lpoly.append(c)
        if c == lpoly[0]:
            lcalc.append(['%s+%s*%s' % (lpoly[0], lpoly[1], lpoly[2])])
        else:
            lcalc.append(['%s*%s+%s' % (lpoly[0], lpoly[1], lpoly[2])])
        lcalc[i].extend(priorites(lcalc[i][0]))
        lcalc[i][0] = splitting(lcalc[i][0])
        expr.append(texify(lcalc[i]))
    exo = ["\\exercice", u"Développer et réduire chacune des expressions littérales suivantes :"]
    exo.append("\\begin{multicols}{2}")
    cor = ["\\exercice*", u"Développer et réduire chacune des expressions littérales suivantes :"]
    cor.append("\\begin{multicols}{2}")
    for i in range(len(lcalc)):
        if i == 2: cor.append("\\end{multicols}")
        cor.append('\\\\\n'.join(['$%s=%s$' % (chr(i + 65), expr[i][j]) for j in range(len(expr[i]) - 1)]))
        cor.append('\\\\')
        cor.append('\\fbox{$%s=%s$}\\\\\n' % (chr(i + 65), expr[i][-1]))
    exo.append('\\\\\n'.join(['$%s=%s$' % (chr(i + 65), expr[i][0]) for i in range(len(expr))]))
    exo.append("\\end{multicols}")
    return exo, cor

class double_distributivite(LegacyExercise):
    """Double distributivité"""

    tags = ["quatrième"]
    function = _double_distributivite

def _soustraction():
    """Réduction d'expressions du type 5a+3-(5+a)
    """
    lcalc, expr = [], []
    sgn = ['-', '-', '-', '-', '+', '+']
    for i in range(len(sgn)):
        a = valeurs_reduire_somme(2)
        b = 'Polynome([[%s,0]], var=\'x\', details=3)' % (randrange(2, 11) * (-1) ** randrange(2))
        c = 'Polynome([[%s,1]], var=\'x\', details=3)' % (randrange(2, 11) * (-1) ** randrange(2))
        poly = [a, b, c]
        shuffle(poly)
        signe = sgn.pop(randrange(len(sgn)))
        poly.insert(poly.index(a), signe)
        if signe == '+':
            poly.insert(poly.index(a), '(')
            poly.insert(poly.index(a) + 1, ')')
        poly.insert(poly.index(b), '+')
        poly.insert(poly.index(c), '+')
        if poly[0] == '+': del poly[0]
        lcalc.append(["".join(poly)])
        lcalc[i].extend(priorites(lcalc[i][0]))
        lcalc[i][0] = splitting(lcalc[i][0])
        expr.append(texify(lcalc[i]))
    exo = ["\\exercice", u"Réduire chacune des expressions littérales suivantes :"]
    exo.append("\\begin{multicols}{2}")
    cor = ["\\exercice*", u"Réduire chacune des expressions littérales suivantes :"]
    cor.append("\\begin{multicols}{2}")
    for i in range(len(lcalc)):
        cor.append('\\\\\n'.join(['$%s=%s$' % (chr(i + 65), expr[i][j]) for j in range(len(expr[i]) - 1)]))
        cor.append('\\\\')
        cor.append('\\fbox{$%s=%s$}\\\\\n' % (chr(i + 65), expr[i][-1]))
    exo.append('\\\\\n'.join(['$%s=%s$' % (chr(i + 65), expr[i][0]) for i in range(len(expr))]))
    exo.append("\\end{multicols}")
    cor.append("\\end{multicols}")
    return exo, cor

class soustraction(LegacyExercise):
    """Soustraire une expression entre parenthèses"""

    tags = ["quatrième"]
    function = _soustraction

def valeurs_reduire_somme(nbval=4):
    """Réduire une somme de quatre monômes de degrés 0 et 1"""
    var = "x"
    #===========================================================================
    # var = var[randrange(len(var))]
    #===========================================================================
    l = [[randrange(1, 11) * (-1) ** randrange(2), (i + 1) % 2] for i in range(nbval)]
    return "Polynome(%s, var=\"%s\", details=3)" % (l, var)

def _exo_comptable():
    """Exercice tiré de l'excellent ouvrage Des maths ensemble et pour chacun quatrième
    """
    exo = ["\\exercice", u"Le principe est le suivant : l'extrémité de chaque flèche indique la somme de la ligne ou de la colonne correspondante. Compléter, sachant que $x$ représente un nombre quelconque et que le contenu des deux cases grises doit être le même.\\par"]
    cor = ["\\exercice*", u"Le principe est le suivant : l'extrémité de chaque flèche indique la somme de la ligne ou de la colonne correspondante. Compléter, sachant que $x$ représente un nombre quelconque et que le contenu des deux cases grises doit être le même.\\par"]
    lexo = [valeurs_reduire_somme(2) for dummy in range(8)]
    lcalc = [["%s+%s" % (lexo[4], lexo[0])], ["%s+%s" % (lexo[5], lexo[1])], ["%s+%s" % (lexo[6], lexo[2])], ["%s+%s" % (lexo[7], lexo[3])], \
             ["%s+%s+%s+%s" % tuple(lexo[0:4])], [ "%s+%s+%s+%s" % tuple(lexo[4:])]]
    for i in range(6):
        sol = priorites(lcalc[i][0])
        lcalc[i].extend(["".join(sol[j]) for j in range(len(sol))])
    lcalc.append(["%s+%s+%s+%s" % (lcalc[0][-1], lcalc[1][-1], lcalc[2][-1], lcalc[3][-1])])
    lcalc.append(["%s+%s" % (lcalc[4][-1], lcalc[5][-1])])
    for i in range(6, 8):
        sol = priorites(lcalc[i][0])
        lcalc[i].extend(["".join(sol[j]) for j in range(len(sol))])
    for i in range(8):
        for j in range(len(lcalc[i])):
            lcalc[i][j] = splitting(lcalc[i][j])
    expr = [texify(lcalc[i]) for i in range(8)]
    # expr = [texify([splitting(lexo[i])]) for i in range(8)]
    txt = []
    # txt.append(r"\psset{xunit=1.1cm,yunit=1.5cm}")
    txt.append(r"\begin{center}")
    txt.append(r"\begin{pspicture}(16,6)")
    txt.append(r"\psframe[fillstyle=solid,fillcolor=Gray](0,0)(2,1)")
    txt.append(r"\psframe[fillstyle=solid,fillcolor=Gray](14,5)(16,6)")
    txt.append(r"\psframe(14,2)(16,3)")
    txt.append(r"\psframe(14,3)(16,4)")
    txt.append(r"\multido{\i=4+2}{4}{")
    txt.append(r"\rput(\i,0){\psframe(0,0)(2,1)\psline[linewidth=2pt]{<-}(1,1.2)(1,1.8)}")
    txt.append(r"\rput(\i,2){\psframe(0,0)(2,1)}")
    txt.append(r"\rput(\i,3){\psframe(0,0)(2,1)}}")
    txt.append(r"\psline[linewidth=2pt]{<-}(2.2,.5)(3.8,.5)")
    txt.append(r"\psline[linewidth=2pt]{->}(12.2,2.5)(13.8,2.5)")
    txt.append(r"\psline[linewidth=2pt]{->}(12.2,3.5)(13.8,3.5)")
    txt.append(r"\psline[linewidth=2pt]{<-}(15,4.8)(15,4.2)")
    txt.append(r"\rput(5,2.5){$%s$}" % texify([splitting(lexo[0])])[0])
    txt.append(r"\rput(7,2.5){$%s$}" % texify([splitting(lexo[1])])[0])
    txt.append(r"\rput(9,2.5){$%s$}" % texify([splitting(lexo[2])])[0])
    txt.append(r"\rput(11,2.5){$%s$}" % texify([splitting(lexo[3])])[0])
    txt.append(r"\rput(5,3.5){$%s$}" % texify([splitting(lexo[4])])[0])
    txt.append(r"\rput(7,3.5){$%s$}" % texify([splitting(lexo[5])])[0])
    txt.append(r"\rput(9,3.5){$%s$}" % texify([splitting(lexo[6])])[0])
    txt.append(r"\rput(11,3.5){$%s$}" % texify([splitting(lexo[7])])[0])
    exo.extend(txt)
    txt.append(r"\rput(5,.5){$%s$}" % expr[0][-1])
    txt.append(r"\rput(7,.5){$%s$}" % expr[1][-1])
    txt.append(r"\rput(9,.5){$%s$}" % expr[2][-1])
    txt.append(r"\rput(11,.5){$%s$}" % expr[3][-1])
    txt.append(r"\rput(15,2.5){$%s$}" % expr[4][-1])
    txt.append(r"\rput(15,3.5){$%s$}" % expr[5][-1])
    txt.append(r"\rput(1,.5){$%s$}" % expr[6][-1])
    txt.append(r"\rput(15,5.5){$%s$}" % expr[7][-1])
    cor.extend(txt)
    exo.append("\\end{pspicture}\n\\end{center}")
    cor.append("\\end{pspicture}\n\\end{center}")
    cor.append(u"\\subsubsection*{Ligne du bas :}")
    cor.append(u"\\begin{multicols}{4}")
    for i in range(4):
        cor.append('\\\\\n'.join(['$%s=%s$' % (chr(i + 65), expr[i][j]) for j in range(len(expr[i]) - 1)]))
        cor.append('\\\\')
        cor.append('\\fbox{$%s=%s$}\\\\\n' % (chr(i + 65), expr[i][-1]))
    cor.append(u"\\end{multicols}")
    cor.append(u"\\subsubsection*{Colonne de droite :}")
    cor.append(u"\\begin{multicols}{2}")
    for i in range(4, 6):
        cor.append('\\\\\n'.join(['$%s=%s$' % (chr(i + 65), expr[i][j]) for j in range(len(expr[i]) - 1)]))
        cor.append('\\\\')
        cor.append('\\fbox{$%s=%s$}\\\\\n' % (chr(i + 65), expr[i][-1]))
    cor.append(u"\\end{multicols}")
    cor.append(u"\\subsubsection*{Cases grises :}")
    cor.append(u"\\begin{multicols}{2}")
    for i in range(6, 8):
        cor.append('\\\\\n'.join(['$%s=%s$' % (chr(i + 65), expr[i][j]) for j in range(len(expr[i]) - 1)]))
        cor.append('\\\\')
        cor.append('\\fbox{$%s=%s$}\\\\\n' % (chr(i + 65), expr[i][-1]))
    cor.append(u"\\end{multicols}")

    return exo, cor

class exo_comptable(LegacyExercise):
    """Réduire des expressions littérales"""

    tags = ["quatrième"]
    function = _exo_comptable

#===============================================================================
#
# def reduire_expressions():
#     """Fait double emploi avec l'exercice du comptable"""
#     """Travail sur les bases du calcul littéral en quatrième"""
#     exo = ["\\exercice", u"Réduire les expressions littérales suivantes :",
#            "\\begin{multicols}{2}"]
#     cor = ["\\exercice*", u"Réduire les expressions littérales suivantes :",
#            "\\begin{multicols}{2}"]
#     lexo = [valeurs_reduire_somme() for dummy in range(4)]
#     expr = [texify([splitting(lexo[i])]) for i in range(4)]
#     for i in range(4):
#         expr[i].extend(texify(priorites(lexo[i])))
#         exo.append('\\\\\n$%s=%s$' % (chr(i + 65), expr[i][0]))
#         cor.append('\\\\\n'.join(['$%s=%s$' % (chr(i + 65), expr[i][j]) for j in range(len(expr[i]) - 1)]))
#         cor.append('\\\\')
#         cor.append('\\fbox{$%s=%s$}\\\\\n' % (chr(i + 65), expr[i][-1]))
#     exo.append("\\end{multicols}")
#     cor.append("\\end{multicols}")
#     return exo, cor
#
# # eduire_expressions.description = u'Réduire des expressions littérales'
#===============================================================================
