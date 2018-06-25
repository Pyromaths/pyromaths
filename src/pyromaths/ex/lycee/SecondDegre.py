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

from builtins import range
from builtins import str
from functools import reduce
# from math import sqrt
from random import shuffle, randrange

from pyromaths import ex
from pyromaths.classes.Fractions import Fraction
from pyromaths.classes.SquareRoot import SquareRoot
from pyromaths.classes.PolynomesCollege import Polynome, factoriser
from pyromaths.outils import Priorites3
from pyromaths.outils.Arithmetique import carrerise, pgcd, valeur_alea

"""Exercice de seconde : Chapitre Second degré."""

import random

from pyromaths.ex import Jinja2Exercice
from pyromaths.outils.jinja2 import facteur

def signe(nombre):
    """Renvoit une chaîne contenant le signe de l'argument."""
    if nombre < 0:
        return "-"
    return "+"
dummy=SquareRoot([1,1]) # Pour que l'IDE sache que l'import de SquareRoot est obligatoire

class BilanTrinomeSansDiscriminant(Jinja2Exercice):
    description = u"Bilan sur les trinômes"
    level = "2.Seconde"

    def __init__(self):
        super(BilanTrinomeSansDiscriminant, self).__init__()

        while True:
            a = float(random.choice([-1, 1]) * random.choice([0.5, 2]))
            x1 = float(random.choice([-1, 1]) * random.randint(2, 15))
            x2 = float(random.choice([-1, 1]) * random.randint(2, 15))

            b = -a * (x1 + x2)
            c = a * x1 * x2

            alpha = -b // (2*a)
            beta = a * (alpha**2) + b * alpha + c

            if alpha == 0 or beta == 0:
                continue
            if b == 0 or c == 0:
                continue
            if beta == c:
                continue

            break

        self.context = {
            "a": a,
            "b": b,
            "c": c,
            "x1": x1,
            "x2": x2,
            "alpha": alpha,
            "absalpha": abs(alpha), # Valeur absolue de alpha
            "signealpha": alpha // abs(alpha), # Signe de alpha (qui est non nul)
            "beta": beta,
            }

    @property
    def environment(self):
        environment = super(BilanTrinomeSansDiscriminant, self).environment
        environment.filters.update({
            'facteur': facteur,
            'min': min,
            'max': max,
            'abs': abs,
            'signe': signe,
            })
        return environment

def creerPolydegre2(nb_racines=2, rac_radical=True, rac_quotient=False):
    if nb_racines == 2:
        redo = True
        while redo:
            a = randrange(1, 4) * (-1) ** randrange(2)
            alpha = randrange(1, 10) * (-1) ** randrange(2)
            beta = randrange(1, 10)
            gamma = [1, randrange(1, 6)][rac_radical]
            if rac_quotient:
                den = randrange(2, 6)
                while pgcd(alpha, den) != 1 or pgcd(beta, den) != 1:
                    den = randrange(2, 6)
                alpha = Fraction(alpha, den)
                beta = Fraction(beta, den)
            b = -2 * alpha * a
            c = a * (alpha ** 2 - gamma * beta ** 2)
            if abs(c) <= 10 and c != 0 and not factoriser(repr(Polynome([[a, 2], [b, 1], [c, 0]]))): redo = False
            if c.denominator != 1:
                c = 'Fraction(%s, %s)' % (c.numerator, c.denominator)
            else:
                c = c.numerator
            if b.denominator != 1:
                b = 'Fraction(%s, %s)' % (b.numerator, b.denominator)
            else:
                b = b.numerator
        return Polynome([[a, 2], [b, 1], [c, 0]])
    elif nb_racines == 1:
        a, b = valeur_alea(-9, 9), valeur_alea(-9, 9)
        return Polynome([[a ** 2, 2], [2 * a * b, 1], [b ** 2, 0]])
    else:
        pol = [[valeur_alea(-9, 9), 2 - dummy] for dummy in range(3)]
        while pol[1][0] ** 2 - 4 * pol[0][0] * pol[2][0] >= 0:
            pol = [[valeur_alea(-9, 9), 2 - dummy] for dummy in range(3)]
        return Polynome(pol)

class Sd1FormeCanonique(ex.TexExercise):

    description = _(u'Forme canonique')
    level = _("1.1reS")

    def __init__(self):
        m = [[1, 2], [2 * randrange(1, 10) * (-1) ** randrange(2), 1], [randrange(1, 10) * (-1) ** randrange(2), 0]]
        pol = [[['Polynome(%s, "x", details=0)' % m]]]
        pol[0].extend(self.resolution(m))
        m = [[1, 2], [(2 * randrange(1, 6) + 1) * (-1) ** randrange(2), 1], [randrange(1, 10) * (-1) ** randrange(2), 0]]
        pol.append([['Polynome(%s, "x", details=0)' % m]])
        pol[1].extend(self.resolution(m))
        a, b = randrange(1, 10), randrange(1, 10)
        m = [[a ** 2, 2], [2 * a * b * (-1) ** randrange(2), 1], [b ** 2, 0]]
        pol.append([['Polynome(%s, "x", details=0)' % m]])
        if m[1][0] < 0: pol[2].extend(self.id_rem(a, b, '-'))
        else: pol[2].extend(self.id_rem(a, b, '+'))
        m = [[randrange(2, 6) * (-1) ** randrange(2), 2], [randrange(1, 10) * (-1) ** randrange(2), 1], [randrange(1, 10) * (-1) ** randrange(2), 0]]
        pol.append([['Polynome(%s, "x", details=0)' % m]])
        fracb = Fraction(m[1][0], m[0][0]).simplifie()
#        if fracb.d == 1: fracb = fracb.n
        fracc = Fraction(m[2][0], m[0][0]).simplifie()
#        if fracc.d == 1: fracc = fracc.n
        pol[3].append(['%s' % m[0][0], '*', '(', 'Polynome(%s, "x", details=0)' % [[1, 2], [fracb, 1], [fracc, 0]], ')'])
        pol[3].extend(self.resolution([[1, 2], [fracb, 1], [fracc, 0]], ['%s' % m[0][0], '*', '('], [')']))
        shuffle(pol)
        self.exercice = pol

    def resolution(self, m, pre=[], post=[]):
        sgn = '+-'[m[1][0] < 0]
        if isinstance(m[1][0], Fraction):
            b = Priorites3.priorites(abs(m[1][0]) / 2)[-1][0]
        elif m[1][0] % 2:
            b = 'Fraction(%s, 2)' % abs(m[1][0])
        else:
            b = abs(m[1][0]) // 2
        fc = ['Polynome("%sx%s%s")' % (m[0][0], sgn, b), '**', '2']
        reste = ['-']
        if m[2][0] > 0 or isinstance(m[2][0], Fraction):
            reste.extend(Priorites3.splitting('%s**2+%r' % (b, m[2][0])))
        else:
            reste.extend(Priorites3.splitting('%s**2%r' % (b, m[2][0])))
        etapes = list(pre)
        etapes.extend(fc)
        etapes.extend(reste)
        etapes.extend(post)
        etapes = [etapes]
        for unreste in Priorites3.priorites(''.join(reste)):
            calcul = list(pre)
            calcul.extend(fc)
            if unreste[0][0] != '-':
                calcul.append('+')
            else:
                calcul.append('-')
                unreste[0] = unreste[0][1:]
            calcul.extend(unreste)
            calcul.extend(post)
            etapes.append(calcul)
        if isinstance(b, str):  # On supprime deux étapes trop détaillée UGLY
            # TODO: Corriger la classe Fractions pour qu'elle gère plusieurs niveaux de détails.
            etapes.pop(1)
            etapes.pop(1)
        if pre:
            calcul = pre[0:-1]
            calcul.extend(fc)
            fc = list(calcul)
            reste = Priorites3.priorites(''.join(reste))[-1]
            reste.extend(['*', pre[0]])
            for unreste in Priorites3.priorites(''.join(reste)):
                calcul = list(fc)
                if unreste[0][0] != '-':
                    calcul.append('+')
                else:
                    calcul.append('-')
                    unreste[0] = unreste[0][1:]
                calcul.extend(unreste)
                etapes.append(calcul)
        return etapes

    def id_rem(self, a, b, sgn):
        etapes = [['Polynome("%sx%s%s")' % (a, sgn, b), '**', '2']]
        if a != 1:
            etapes.append(['(', '%s' % a, '*', 'Polynome("x%sFraction(%s, %s)")' % (sgn, b, a), ')', '**', '2' ])
            frac = Fraction(b, a).simplifie()
            etapes.append(['%s' % (a ** 2), '*', 'Polynome("x%s%r")' % (sgn, frac), '**', '2'])
        return etapes

    def tex_statement(self):
        exo = [r'\exercice']
        exo.append(_(u'Donner la forme canonique des polynômes $P$ , $Q$ , $R$ et $S$ .'))
        exo.append(r'\begin{align*}')
        noms = [r'P\,(x) &= ', r'Q\,(x) &= ', r'R\,(x) &= ', r'S\,(x) &= ']
        exercice = list(self.exercice)
        sol = ''
        for i in range(len(exercice)):
            exercice[i][0] = Priorites3.texify(exercice[i][0])
            sol += noms[i] + exercice[i][0][0]
            if i < len(exercice) - 1: sol += r' & '
            else: sol += r' \\ '
        exo.append(sol)
        exo.append(r'\end{align*}')
        return exo

    def tex_answer(self):
        exo = [r'\exercice*']
        exo.append(_(u'Donner la forme canonique des polynômes $P$ , $Q$ , $R$ et $S$ .'))
        noms = [r'P\,(x) &= ', r'Q\,(x) &= ', r'R\,(x) &= ', r'S\,(x) &= ']
        exercice = list(self.exercice)
        for i in range(len(exercice)):
            exercice[i] = Priorites3.texify(exercice[i])
            exercice[i][0] = noms[i] + exercice[i][0]  # [0]
            for j in range(1, len(exercice[i]) - 1):
                exercice[i][j] = r' &= ' + exercice[i][j]
            exercice[i][-1] = r'\Aboxed{' + noms[i] + exercice[i][-1] + r'}'
        tri = []
        for i in range(len(exercice)):
            tri.append((i, len(exercice[i])))
        tri = sorted(tri, key=lambda nblgn: nblgn[1])
        if tri[0][0] < tri[1][0]:
            exercice[tri[0][0]].extend(exercice.pop(tri[1][0]))
        else:
            exercice[tri[1][0]].extend(exercice.pop(tri[0][0]))
        exo.append(r'\begin{align*}')
        for j in range(max(len(exercice[0]), len(exercice[1]), len(exercice[2]))):
            sol = ''
            for i in range(3):
                if j < len(exercice[i]):
                    sol += exercice[i][j]
                else:
                    sol += r'& '
                if i == 2:
                    sol += r'\\'
                else:
                    sol += r' & '
            exo.append(sol)
        exo.append(r'\end{align*}')
        return exo

class Sd2aRacines(ex.TexExercise):
    #TODO: ./utils/pyromaths-cli.py generate Sd2aRacines:1, 2 et 3 ne fonctionnent pas
    description = _(u'Racines d\'un polynôme de degré 2')
    level = _("1.1reS")
    def __init__(self):
        pol = [creerPolydegre2(nb_racines=2, rac_radical=True, rac_quotient=False)]
        pol.append(creerPolydegre2(nb_racines=1))
        a, b = valeur_alea(-9, 9), valeur_alea(-9, 9)
        pol.append([[a ** 2, 2], [-b ** 2, 0]])
        a, b = valeur_alea(-9, 9), valeur_alea(-9, 9)
        while a * b == -64:
            # sqrt{8} est trop long à décomposer en une demi-ligne
            a, b = valeur_alea(-9, 9), valeur_alea(-9, 9)
        pol.append([[a, 2], [b, 0]])
        a, b = valeur_alea(-9, 9), valeur_alea(-9, 9)
        pol.append([[a, 2], [b, 1]])
        pol.pop(randrange(1, len(pol)))
        pol.pop(randrange(1, len(pol)))
        shuffle(pol)
        for i in range(3):
            m = list(pol[i])
            shuffle(m)
            pol[i] = m
        self.exercice = pol

    def tex_statement(self):
        exo = [r'\exercice']
        exo.append(_(u'Déterminer les racines des polynômes :'))
        exo.append('\\begin{align*}')
        noms = [r'P\,(x) &= ', r'Q\,(x) &= ', r'R\,(x) &= ']
        r = ''
        for i in range(3):
            r += noms[i] + str(Polynome(self.exercice[i], 'x'))
            if i < 2: r += ' & '
        exo.append(r)
        exo.append('\\end{align*}')
        return exo

    def tex_answer(self):
        exo = [r'\exercice*']
        exo.append(_(u'Déterminer les racines des polynômes :\\par'))
        noms = [r'P\,(x) &= ', r'Q\,(x) &= ', r'R\,(x) &= ']
        r = ''
        question = [[], [], []]
        for i in range(3):
            p = []
            m = Polynome(list(self.exercice[i])).ordonne()
            if factoriser('%r' % Polynome(m)):
                p = [factoriser('%r' % Polynome(m))]
                while factoriser(p[-1]):
                    p.append(factoriser(p[-1]))
            if p and eval(Priorites3.splitting(p[-1])[0]).degre() > 0:
                tmp = Priorites3.texify([Priorites3.splitting(p[j]) for j in range(len(p))])
                question[i].append('{$\\! \\begin{aligned}')
                question[i].append(noms[i] + str(Polynome(m, 'x')) + r'\\')
                question[i].append('\\\\\n'.join(['&=%s' % (tmp[j]) for j in range(len(tmp))]))
                question[i].append(r'\end{aligned}$}\par')
                lp = Priorites3.splitting(p[-1])
                racines = []
                for e in lp:
                    if e[:9] == 'Polynome(':
                        e = eval(e)
                        if len(e) == 2:
                            racines.append(str(Fraction(-e[1][0], e[0][0]).simplifie()))
                        else:
                            racines.append('0')
                if len(racines) > 1:
                    question[i].append(_(u'\\underline{Les racines de $%s$ sont }\\fbox{$%s$}') % (noms[i].rstrip(r' &= '), '$}\\underline{ et }\\fbox{$'.join(racines)))
                elif len(racines) == 1:
                    question[i].append(_(u'\\underline{L\'unique racine de $%s$ est }\\fbox{$%s$}') % (noms[i].rstrip(r' &= '), racines[0]))
            elif len(m) == 2 and m[0][1] == 2 and m[1][1] == 0 and m[0][0] * m[1][0] > 0:
                question[i].append('$' + noms[i] + str(Polynome(m, 'x')) + r'$\par')
                question[i][-1] = question[i][-1].replace('&', '')
                if m[1][0] > 0: question[i].append('$' + noms[i][:7] + ' \\geqslant %r$' % m[1][0])
                else: question[i].append('$' + noms[i][:7] + ' \\leqslant %r$' % m[1][0])
                question[i].append(_(u'car un carré est toujours positif.\\par\n\\underline{$%s$ n\'a donc pas de racine.}') % (noms[i].rstrip(r' &= ')))
            else:
                question[i].append('$' + noms[i] + str(Polynome(m, 'x')) + r'\quad$')
                question[i][-1] = question[i][-1].replace('&', '')
                question[i].append(_(u'On calcule le discriminant de $%s$ avec $a=%s$, $b=%s$ et $c=%s$ :\\par\\medskip') % (noms[i].rstrip(r' &= '), m[0][0], m[1][0], m[2][0]))
                question[i].append(r'\begin{tabularx}{\linewidth}[t]{XXX}')
                question[i].append(r'{$\! \begin{aligned}')
                if m[1][0]>0:
                    sol = [[str(m[1][0]), '**', '2', '-', '4', '*', str(m[0][0]), '*', str(m[2][0])]]
                    sol.extend(Priorites3.priorites('%s**2-4*%s*%s' % (m[1][0], m[0][0], m[2][0])))
                else:
                    sol = [['(', str(m[1][0]), ')', '**', '2', '-', '4', '*', str(m[0][0]), '*', str(m[2][0])]]
                    sol.extend(Priorites3.priorites('(%s)**2-4*%s*%s' % (m[1][0], m[0][0], m[2][0])))
                solTeX = Priorites3.texify(sol)
                for s in solTeX:
                    question[i].append(u'\\Delta &= %s\\\\' % s)
                question[i].append(r'\end{aligned}$}')
                question[i].append(r'&')
                question[i].append(r'{$\! \begin{aligned}')
                delta = sol[-1][0]
                sol = [['Fraction(SquareRoot([[%s, None], [-1, %s]]),\'2*%s\')' % (-m[1][0], delta, m[0][0])]]
                sol.extend(Priorites3.priorites(sol[0][0]))
                sol = Priorites3.texify(sol)
                for s in sol:
                    question[i].append(u'x_1 &= %s\\\\' % s)
                racines = [sol[-1]]
                question[i].append(r'\end{aligned}$}')
                question[i].append(r'&')
                question[i].append(r'{$\! \begin{aligned}')
                sol = [['Fraction(SquareRoot([[%s, None], [1, %s]]),\'2*%s\')' % (-m[1][0], delta, m[0][0])]]
                sol.extend(Priorites3.priorites(sol[0][0]))
                sol = Priorites3.texify(sol)
                for s in sol:
                    question[i].append(u'x_2 &= %s\\\\' % s)
                racines.append(sol[-1])
                question[i].append(r'\end{aligned}$}')
                question[i].append(r'\end{tabularx}\par')
                question[i].append(_(u'\\underline{Les racines de $%s$ sont }\\fbox{$%s$}') % (noms[i].rstrip(r' &= '), _('$}\\underline{ et }\\fbox{$').join(racines)))
                if i == 1: question.append(question[1])
        if len(question) == 4:
            question.pop(1)
        if question[0][0][-6:] == r'\quad$':
            question[1].insert(0, r'\par\medskip\begin{tabularx}{\linewidth}[t]{XX}')
            question[2].insert(0, r'&')
            question[2].append(r'\end{tabularx}\par\medskip')
        else:
            question[0].insert(0, r'\begin{tabularx}{\linewidth}[t]{XX}')
            question[1].insert(0, r'&')
            question[1].append(r'\end{tabularx}\par\medskip')
        for i in range(3): exo.extend(question[i])
        return exo

class Sd2bEquations(ex.TexExercise):
    # description = u'Équations et polynômes de degré 2'
    level = _("1.1reS")
    def __init__(self):
        pol = [creerPolydegre2(nb_racines=2, rac_radical=False, rac_quotient=False)]
        pol.append(creerPolydegre2(nb_racines=1))
        a, b = valeur_alea(-9, 9), valeur_alea(-9, 9)
        pol.append([[a ** 2, 2], [-b ** 2, 0]])
        a, b = valeur_alea(-9, 9), valeur_alea(-9, 9)
        pol.append([[a, 2], [b, 1]])
        a, b = valeur_alea(-9, 9), valeur_alea(-9, 9)
        pol.append([[a, 2], [b, 0]])
        pol.pop(randrange(1, len(pol)))
        pol.pop(randrange(1, len(pol)))
        pol.pop(randrange(1, len(pol)))
        shuffle(pol)
        exercice = [pol]
        lval = [[[randrange(2, 10) * (-1) ** randrange(2), 1], [randrange(2, 10) * (-1) ** randrange(2), 0]] for dummy in range(3)]
        a, b, c = -lval[2][0][0] * lval[1][0][0], lval[0][0][0] - lval[2][0][0] * lval[1][1][0] - lval[2][1][0] * lval[1][0][0], lval[0][1][0] - lval[2][1][0] * lval[1][1][0]
        delta = b ** 2 - 4 * a * c
        while delta < 0 or carrerise(delta) != 1:
            lval = [[[randrange(2, 10) * (-1) ** randrange(2), 1], [randrange(2, 10) * (-1) ** randrange(2), 0]] for dummy in range(3)]
            a, b, c = -lval[2][0][0] * lval[1][0][0], lval[0][0][0] - lval[2][0][0] * lval[1][1][0] - lval[2][1][0] * lval[1][0][0], lval[0][1][0] - lval[2][1][0] * lval[1][1][0]
            delta = b ** 2 - 4 * a * c
        # print delta, Polynome([[a, 2], [b, 1], [c, 0]]), '\cfrac{%s}{%s}' % (-b - sqrt(delta), 2 * a), '\cfrac{%s}{%s}' % (-b + sqrt(delta), 2 * a)
        exercice.append(lval)
        shuffle(exercice)
        self.exercice = exercice

    def tex_statement(self):
        exo = [r'\exercice']
        exo.append(_(u'Résoudre les équations :'))
        exo.append('\\begin{align*}')
        for e in self.exercice:
            if len(e) == 2:
                exo.append(Priorites3.texify([[repr(Polynome(e[0])), '*', repr(Polynome(e[1]))]])[0] + ' &= 0 & ')
            else:
                exo.append(r'\cfrac{%s}{%s} &= %s & ' % (Polynome(e[0]), Polynome(e[1]), Polynome(e[2])))
        exo[-1] = exo[-1][:-3]  # Suppression du dernier  " &"
        exo.append('\\end{align*}')
        return exo

class Sd3aSigne(ex.TexExercise):
    # description = u'Signe d\'un polynôme de degré 2'
    level = _("1.1reS")
    def __init__(self):
        pol = [[valeur_alea(-9, 9), 2 - dummy] for dummy in range(3)]
        while pol[1][0] ** 2 - 4 * pol[0][0] * pol[2][0] >= 0:
            pol = [[valeur_alea(-9, 9), 2 - dummy] for dummy in range(3)]
        exercice = [list(pol)]

        val = [valeur_alea(-9, 9), valeur_alea(-9, 9)]
        val.append(Fraction(valeur_alea(-9, 9), val[0]))
        while val[2].d == 1:
            val = [valeur_alea(-9, 9), valeur_alea(-9, 9)]
            val.append(Fraction(valeur_alea(-9, 9), val[0]))
        sgn = -val[0] // abs(val[0])
        pol = [[val[0], 2], [(-val[0] * (val[1] * val[2].d + val[2].n)) // val[2].d, 1], [(val[0] * val[1] * val[2].n) // val[2].d, 0]]
        shuffle(pol)
        exercice.append([pol, val[1], val[2]])

        val = [sgn * valeur_alea(-9, 9), valeur_alea(-9, 9)]
        val.append(Fraction(valeur_alea(-9, 9), val[0]).simplifie())
        while isinstance(val[2], int) or val[2].d == 1:
            val = [sgn * valeur_alea(-9, 9), valeur_alea(-9, 9)]
            val.append(Fraction(valeur_alea(-9, 9), val[0]))
        pol = [[val[0], 2], [(-val[0] * (val[1] * val[2].d + val[2].n)) // val[2].d, 1], [(val[0] * val[1] * val[2].n) // val[2].d, 0]]
        shuffle(pol)
        exercice.append([pol, val[1], val[2]])

        self.exercice = exercice

    def tex_statement(self):
        exo = [r'\exercice']
        exo.append(r'\begin{enumerate}')
        exo.append(_(u'\\item Déterminer le signe du polynôme $P\\,(x) = %s$') % Polynome(self.exercice[0]))
        exo.append(_(u'\\item Le polynôme $Q\\,(x) = %s$ admet deux racines $%s$ et $%s\\,$. Dresser son tableau de signes.') \
            % (Polynome(self.exercice[1][0]), self.exercice[1][1], self.exercice[1][2]))
        exo.append(_(u'\\item Le polynôme $R\\,(x) = %s$ admet deux racines $%s$ et $%s\\,$. Dresser son tableau de signes.') \
            % (Polynome(self.exercice[2][0]), self.exercice[2][1], self.exercice[2][2]))
        exo.append('\\end{enumerate}')
        return exo

class Sd3bInequations(ex.TexExercise):
    # description = u'Inéquations et polynômes de degré 2'
    level = _("1.1reS")
    def __init__(self):
        pol = creerPolydegre2(nb_racines=2, rac_radical=False, rac_quotient=False).monomes
        pol2 = [[valeur_alea(-9, 9), 1], [valeur_alea(-9, 9), 0]]
        shuffle(pol)
        shuffle(pol2)
        p = [pol, pol2]
        shuffle(p)
        p.append(['<', '>', '\\leqslant{}', '\\geqslant{}'][randrange(4)])
        self.exercice = p

    def tex_statement(self):
        exo = [r'\exercice']
        exo.append(_(u'Résoudre l\'inéquation : $\qquad \\cfrac{%s}{%s} %s 0$') % (Polynome(self.exercice[0]),
                                                                                  Polynome(self.exercice[1]),
                                                                                  self.exercice[2]))
        return exo

class Sd4Factorisation(ex.TexExercise):
    # description = u'Racines et factorisation d\'un polynôme de degré 2'
    level = _("1.1reS")
    def __init__(self):
        val = [valeur_alea(-9, 9), valeur_alea(-9, 9)]
        val.append(Fraction(valeur_alea(-9, 9), val[0]))
        while val[2].d == 1:
            val = [valeur_alea(-9, 9), valeur_alea(-9, 9)]
            val.append(Fraction(valeur_alea(-9, 9), val[0]))

        pol = [[val[0], 2], [(-val[0] * (val[1] * val[2].d + val[2].n)) // val[2].d, 1], [(val[0] * val[1] * val[2].n) // val[2].d, 0]]
        shuffle(pol)
        exercice = [[list(pol), val[1], val[2]]]

        pol = [creerPolydegre2(nb_racines=0).monomes]
        pol.append(creerPolydegre2(nb_racines=1).monomes)
        a, b = valeur_alea(-9, 9), valeur_alea(-9, 9)
        sgn = [1, -1][randrange(2)]
        pol.append([[sgn * a ** 2, 2], [-sgn * b ** 2, 0]])
        a, b = valeur_alea(-9, 9), valeur_alea(-9, 9)
        pol.append([[a, 2], [b, 1]])
        a, b = valeur_alea(-9, 9), valeur_alea(-9, 9)
        while abs(pgcd(a, b)) != 1:
            a, b = valeur_alea(-9, 9), valeur_alea(-9, 9)
        pol.append([[a, 2], [b, 0]])
        pol.pop(randrange(1, len(pol)))
        pol.pop(randrange(1, len(pol)))
        pol.pop(randrange(1, len(pol)))
        shuffle(pol)
        exercice.append(pol)

        self.exercice = exercice

    def tex_statement(self):
        exo = [r'\exercice']
        exo.append(r'\begin{enumerate}')
        exo.append(_(u'\\item Le polynôme $\\quad P\\,(x) = %s \\quad$ admet deux racines $%s$ et $%s\\,$. Donner sa forme factorisée.\n') \
            % (Polynome(self.exercice[0][0]), self.exercice[0][1], self.exercice[0][2]))
        exo.append(_(u'\\item Factoriser si possible les polynômes $\quad Q\\,(x) = %s\\quad$ et $\\quad R\\,(x) = %s$.\n') % (Polynome(self.exercice[1][0]), Polynome(self.exercice[1][1])))
        exo.append(r'\end{enumerate}')

        return exo

class Sd5Caracteristiques(ex.TexExercise):
    # description = u'Caractéristiques d\'une parabole'
    level = _("1.1reS")
    def __init__(self):
        val = [valeur_alea(-9, 9), valeur_alea(-9, 9) , valeur_alea(-9, 9)]
        pol = Polynome([[val[0], 2], [(-val[0] * (val[1] + val[2])), 1], [(val[0] * val[1] * val[2]), 0]])
        while val[2] == val[1] or abs(val[0] * val[1] * val[2]) > 10 or abs(eval(pol((val[1] + val[2]) / 2))) > 10:
            val = [valeur_alea(-9, 9), valeur_alea(-9, 9) , valeur_alea(-9, 9)]
            pol = Polynome([[val[0], 2], [(-val[0] * (val[1] + val[2])), 1], [(val[0] * val[1] * val[2]), 0]])
        val = [[val[0], 2], [(-val[0] * (val[1] + val[2])), 1], [(val[0] * val[1] * val[2]), 0]]
        shuffle(val)
        lp = [Polynome(val)]

        val = [[valeur_alea(-9, 9), 2 - dummy] for dummy in range(3)]
        val[1][0] = valeur_alea(-9, 9) * val[0][0]
        pol = Polynome(val)
        while val[1][0] ** 2 - 4 * val[0][0] * val[2][0] >= 0 or abs(eval(pol(-val[1][0] / 2. / val[0][0]))) > 10:
            val = [[valeur_alea(-9, 9), 2 - dummy] for dummy in range(3)]
            val[1][0] = valeur_alea(-9, 9) * val[0][0]
            pol = Polynome(val)
        shuffle(val)
        pol = Polynome(val)
        lp.append(pol)
        shuffle(lp)

        self.exercice = lp

    def tex_statement(self):
        exo = [r'\exercice']
        exo.append(_(u'On donne les polynômes $\\quad p\\,(x) = %s \\quad$ et $\\quad Q\\,(x) = %s$.') % (self.exercice[0], self.exercice[1]))
        exo.append(r'\begin{enumerate}')
        exo.append(_(u'\\item Donner les caractéristiques de leurs courbes respectives (sommet, intersections avec les axes du repère).'))
        exo.append(_(u'\\item Tracer l’allure de ces deux courbes sur un même graphique.'))
        exo.append(r'\end{enumerate}')

        return exo

class Sd6Parametre(ex.TexExercise):
    # description = u'Polynôme paramétré de degré 2'
    level = _("1.1reS")
    def __init__(self):
        [a, b, c, d] = [randrange(-5, 6) for dummy in range(4)]
        while a == 0 or c == 0 or a ** 2 * d - a * b * c + c ** 2 < 0 or carrerise(a ** 2 * d - a * b * c + c ** 2) != 1:
            [a, b, c, d] = [randrange(-5, 6) for dummy in range(4)]
        p1 = str(Polynome([[a, 1], [b, 0]], "m"))
        p2 = str(Polynome([[c, 1], [d, 0]], "m"))
        pol = [Polynome([[1, 2], [p1, 1], [p2, 0]]), randrange(3)]
        exercice = [list(pol)]

        v = [randrange(-4, 5) for dummy in range(6)]
        while v[0] == 0 or v[2] == v[4] == 0 or reduce(lambda x, y: x * y, v) != 0 or v[2] == v[3] == 0 or v[4] == v[5] == 0:
            v = [randrange(-4, 5) for dummy in range(6)]
        lp = [str(Polynome([[v[2 * i] // pgcd(v[2 * i], v[2 * i + 1]), 1], [v[2 * i + 1] // pgcd(v[2 * i], v[2 * i + 1]), 0]], "a")) for i in range(3)]
        pol = Polynome([[lp[0], 2], [lp[1], 1], [lp[2], 0]])
        vi = Fraction(-v[1], v[0])
        racine = randrange(-4, 5)
        while racine == vi or racine == 0:
            racine = randrange(-4, 5)
        if vi.d == 1 : vi = str(vi.n)
        else: vi = str(vi)
        exercice.append([list(pol), vi, racine])
        self.exercice = exercice

    def tex_statement(self):
        exo = [r'\exercice']
        exo.append(r'\begin{enumerate}')
        exo.append(_(u'\\item On donne le polynôme $\\quad P\\,(x) = %s\\quad$ où $m$ est un réel.\\par') % self.exercice[0][0])
        # TODO: Affichage des paramètres et parenthèses
        exo.append(_(u'Quelles sont les valeurs de $m$ pour lesquelles $P$ %s ?\n') % [_('a une seule racine'), _('n\'a pas de racine'),
                _('a deux racines distinctes')][self.exercice[0][1]])
        # exo.append(u'\\par Solution : Polynôme en m : $%s$\\par\n' % (Polynome([[a ** 2, 2], [2 * a * b - 4 * c, 1], [b ** 2 - 4 * d, 0]], "m"))
        # exo.append( u'Solution : discriminant $\\Delta_m = %s$\\par\n' % (16 * (a ** 2 * d - a * b * c + c ** 2))
        exo.append(_(u'\\item Soit $a$ un réel différent de $%s$. On donne $Q\\,(x) = %s$.\\par\n') % (self.exercice[1][1], Polynome(self.exercice[1][0])))
        exo.append(_(u'Déterminer $a$ pour que $%s$ soit une racine de $Q$.\n') % self.exercice[1][2])
        exo.append(r'\end{enumerate}')

        return exo
