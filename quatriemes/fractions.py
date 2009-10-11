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

import outils.Arithmetique
from fonctions_globales import OperateurPrioritaire, Affichage
import random
from pyro_classes import Fractions


def sommes_fractions_4e(op, level):
    '''Choisit des valeurs aléatoires pour effectuer une somme ou une différence
    de fractions en fonction du niveau de difficulté souhaité (de 1 à 4) et renvoie
    l'énoncé et le corrigé au format TeX

    @param op: '+' ou '-'
    @param level: niveau de difficulté :
                  1- Fractions positives et dénominateur de l'une multiple de l'autre
                  2- Fractions positives et dénominateurs non multiples
                  3- Fractions avec des nombres relatifs
                  4- Fractions avec des nombres relatifs et résultats simplifiable
    '''

    while True:
        (n1, d1, n2, d2) = (2, 2, 2, 2)
#        import pdb; pdb.set_trace()
        while True:
            if level == 1:
                n1 = random.randrange(1, 16)
                d1 = random.randrange(1, 9)
                n2 = random.randrange(1, 16)
                d2 = d1*random.randrange(2, 11)
                if random.randrange(2):
                    d1, d2 = d2, d1
            elif level == 2:
                n1 = outils.Arithmetique.valeur_alea(1, 16)
                d1 = outils.Arithmetique.valeur_alea(1, 40)
                n2 = outils.Arithmetique.valeur_alea(1, 16)
                d2 = outils.Arithmetique.valeur_alea(1, 40)
            else:
                while True:
                    neg=[(-1,1)[random.randrange(2)] for x in range(4)]
                    if neg[0]<0 or neg[1]<0 or neg[2]<0 or neg[3]<0:
                        break
                n1 = random.randrange(1, 16)*neg[0]
                d1 = random.randrange(1, 40)*neg[1]
                n2 = random.randrange(1, 16)*neg[2]
                d2 = random.randrange(1, 40)*neg[3]
            fr1 = Fractions(n1, d1)
            fr2 = Fractions(n2, d2)
            if outils.Arithmetique.pgcd(fr1.n, fr1.d) == 1 and \
                outils.Arithmetique.pgcd(fr2.n, fr2.d) == 1 and \
                (level == 1 or (outils.Arithmetique.pgcd(fr1.d, fr2.d) != abs(fr1.d) \
                                and outils.Arithmetique.pgcd(fr1.d, fr2.d) != abs(fr2.d))):
                if op == "+":
                    simplifiable = abs(fr1.d * fr2.d) != \
                                        abs(Fractions.simplifie(fr1 + fr2).d)
                else:
                    simplifiable = abs(fr1.d * fr2.d) != \
                                        abs(Fractions.simplifie(fr1 - fr2).d)
                if level == 1 or (simplifiable and level == 4) or \
                                            (not simplifiable and level < 4):
                    break

        l = [fr1, op, fr2]
        (cor, res, niveau) = OperateurPrioritaire(l, 4, solution=[])
        if niveau >= 4:
            break
    fr1 = Fractions(n1, d1)
    fr2 = Fractions(n2, d2)
    return ([fr1, op, fr2], cor, res)

def produits_fractions_4e(op, level):
    '''Choisit des valeurs aléatoires pour effectuer un produit ou un quotient de
    fractions en fonction du niveau de difficulté souhaité (de 1 à 4) et renvoie
    l'énoncé et le corrigé au format TeX

    @param op: '*' ou '/'
    @param level: niveau de difficulté :
                  1- Fractions positives non décomposables
                  2- Fractions avec des nombres relatifs non décomposables
                  3- Fractions positives à décomposer
                  4- Fractions avec des nombres relatifs à décomposer
    '''

    while True:
        (n1, d1, n2, d2) = (2, 2, 2, 2)
        while True:
            n1=d1=n2=d2=a=b=2
            if level == 3 or level == 4:
                while outils.Arithmetique.pgcd(a,b)>1:
                    a=random.randrange(2,11)
                    b=random.randrange(2,11)
            else:
                a, b = 1, 1
            if op == "*":
                if level == 1 or level == 3:
                    while outils.Arithmetique.pgcd(n1*a,d1*b)>1:
                        n1=random.randrange(1,11)
                        d1=random.randrange(2,11)
                    while outils.Arithmetique.pgcd(n2*b,d2*a)>1:
                        n2=random.randrange(1,11)
                        d2=random.randrange(2,11)
                elif level == 2 or level == 4:
                    while True:
                        neg=[(-1,-1,1)[random.randrange(3)] for x in range(4)]
                        if neg[0]<0 or neg[1]<0 or neg[2]<0 or neg[3]<0:
                            break
                    while outils.Arithmetique.pgcd(n1*a,d1*b)>1:
                        n1=random.randrange(1,11)*neg[0]
                        d1=random.randrange(2,11)*neg[1]
                    while outils.Arithmetique.pgcd(n2*b,d2*a)>1:
                        n2=random.randrange(1,11)*neg[2]
                        d2=random.randrange(2,11)*neg[3]
                fr1 = Fractions(n1*a, d1*b)
                fr2 = Fractions(n2*b, d2*a)
                simplifiable = abs(fr1.d * fr2.d) != Fractions.simplifie(fr1 *
                                                                         fr2).d
            else:
                if level == 1 or level == 3:
                    while outils.Arithmetique.pgcd(n1*a,d1*b)>1:
                        n1=random.randrange(1,11)
                        d1=random.randrange(2,11)
                    while outils.Arithmetique.pgcd(n2*a,d2*b)>1:
                        n2=random.randrange(1,11)
                        d2=random.randrange(2,11)
                else:
                    while outils.Arithmetique.pgcd(n1*a,d1*b)>1:
                        n1=random.randrange(-11,11)
                        d1=random.randrange(2,11)*(-1,1)[random.randrange(2)]
                    while outils.Arithmetique.pgcd(n2*a,d2*b)>1:
                        n2=random.randrange(-11,11)
                        d2=random.randrange(2,11)*(-1,1)[random.randrange(2)]
                fr1 = Fractions(n1*a, d1*b)
                fr2 = Fractions(n2*a, d2*b)
                simplifiable = abs(fr1.d * fr2.n) != \
                                            Fractions.simplifie(fr1 / fr2).d
            if (simplifiable and level>2) or (not simplifiable and level<=2):
                break
        l = [fr1, op, fr2]

        (cor, res, niveau) = OperateurPrioritaire(l, 4, solution=[])
        if niveau >= 4:
            break
    return (l, cor, res)


def valeurs_priorites_fractions(nb, entier=1):  # renvoie les 2 listes contenant les opérateurs et les opérandes.
    listoperateurs = [
        "+",
        "*",
        "-",
        "/",
        '(',
        '(',
        '(',
        '(',
        ')',
        ')',
        ')',
        ')',
        ]
    loperateurs = []
    loperandes = []
    i = 0  #nombre d'opérateurs créés
    p = 0  #nombre de parenthèses ouvertes
    cpt = 0  #compteur pour éviter que le programme ne boucle.
    while i < nb - 1:
        cpt = cpt + 1
        if cpt > 10:  #On recommence
            (cpt, i, p, loperateurs) = (0, 0, 0, [])
        if p:
            if loperateurs[-1] == '(':  # On n'écrit pas 2 parenthèses à suivre
                operateur = listoperateurs[random.randrange(4)]
            else:
                operateur = listoperateurs[random.randrange(12)]
        elif loperateurs == []:

            # On ne commence pas par une parenthèse

            operateur = listoperateurs[random.randrange(4)]
        else:
            operateur = listoperateurs[random.randrange(8)]
        if nb > 3:
            test = ('-*/').find(operateur) >= 0 and loperateurs.count(operateur) < \
                1 or operateur == "+" and loperateurs.count(operateur) < \
                2
        else:
            test = ('-*/+').find(operateur) >= 0 and loperateurs.count(operateur) < \
                1
        if test:

            #On n'accepte pas plus de 1 produit, différence, quotient et de 2 sommes ou parenthèses par calcul.

            if i == 0 or loperateurs[-1] != '(' or ('*/').find(operateur) < \
                0:  #pas de * ou / dans une parenthèse.
                i = i + 1
                loperateurs.append(operateur)
        elif operateur == '(' and (')+').find(loperateurs[-1]) < 0:

            #Il ne peut y avoir de ( après une ) ou après un +

            p = p + 1
            loperateurs.append(operateur)
        elif operateur == ')':
            p = p - 1
            loperateurs.append(operateur)
    while p > 0:
        loperateurs.append(')')
        p = p - 1
    loperandes = []
    for i in range(nb):
        (n, d) = (2, 2)
        while outils.Arithmetique.pgcd(n, d) != 1 or abs(d) == 1:
            n = outils.Arithmetique.valeur_alea(-16, 16)
            d = -outils.Arithmetique.valeur_alea(-40, 40)
        loperandes.append(Fractions(n, d))
    exercice = [loperandes[0]]
    i = 1
    j = 0
    while i < len(loperandes) or j < len(loperateurs):
        if j < len(loperateurs):
            exercice.append(loperateurs[j])
            j = j + 1
        while j < len(loperateurs) and (loperateurs[j] == '(' or
                loperateurs[j - 1] == ')'):
            exercice.append(loperateurs[j])
            j = j + 1
        if i < len(loperandes):
            exercice.append(loperandes[i])
            i = i + 1
    return exercice


def exo_sommes_fractions():
    exo = ["\\exercice",
           u"Effectuer les calculs suivants et donner le résultat sous la forme d'une fraction simplifiée :",
           "\\begin{multicols}{4}", "  \\noindent%"]
    cor = ["\\exercice*",
           u"Effectuer les calculs suivants et donner le résultat sous la forme d'une fraction simplifiée :",
           "\\begin{multicols}{4}", "  \\noindent%"]
    op = ["+", "-","+", "-","+", "-","+", "-"]
    for i in range(8):
        if i%2:
            (l, sol, res) = sommes_fractions_4e(op.pop(0), i//2+1)
        else:
            (l, sol, res) = sommes_fractions_4e(op.pop(random.randrange(2)),
                                                i//2+1)
        exo.append("  \\[\\thenocalcul = %s\\]" % Affichage(l))
        cor.append("  \\[\\thenocalcul = %s\\]" % Affichage(l))
        for l in sol:
            if l == sol[-1]:
                cor.append("  \\[\\boxed{\\thenocalcul = %s}\\]" % l)
            else:
                cor.append("  \\[\\thenocalcul = %s\\]" % l)
        exo.append("  \\stepcounter{nocalcul}%")
        cor.append("  \\stepcounter{nocalcul}%")
    exo.append("\\end{multicols}\n")
    cor.append("\\end{multicols}\n")
    return (exo, cor)


def exo_produits_fractions():
    exo = ["\\exercice",
           u"Effectuer les calculs suivants et donner le résultat sous la forme d'une fraction simplifiée :",
           "\\begin{multicols}{4}", "  \\noindent%"]
    cor = ["\\exercice*",
           u"Effectuer les calculs suivants et donner le résultat sous la forme d'une fraction simplifiée :",
           "\\begin{multicols}{4}", "  \\noindent%"]
    op = ["*", "/","*", "/","*", "/","*", "/"]
    for i in range(8):
        if i%2:
            (l, sol, res) = produits_fractions_4e(op.pop(0), i//2+1)
        else:
            (l, sol, res) = produits_fractions_4e(op.pop(random.randrange(2)), i//2+1)
        exo.append("  \\[\\thenocalcul = %s\\]" % Affichage(l))
        cor.append("  \\[\\thenocalcul = %s\\]" % Affichage(l))
        for l in sol:
            if l == sol[-1]:
                cor.append("  \\[\\boxed{\\thenocalcul = %s}\\]" % l)
            else:
                cor.append("  \\[\\thenocalcul = %s\\]" % l)
        exo.append("  \\stepcounter{nocalcul}%")
        cor.append("  \\stepcounter{nocalcul}%")
    exo.append("\\end{multicols}\n")
    cor.append("\\end{multicols}\n")
    return (exo, cor)


def exo_priorites_fractions():
    exo = ["\\exercice",
           u"Effectuer les calculs suivants et donner le résultat sous la forme d'une fraction simplifiée :",
           "\\begin{multicols}{3}", "  \\noindent%"]
    cor = ["\\exercice*",
           u"Effectuer les calculs suivants et donner le résultat sous la forme d'une fraction simplifiée :",
           "\\begin{multicols}{3}", "  \\noindent%"]
    for i in range(6):
        while True:
            l = valeurs_priorites_fractions(3)
            (sol, res, niveau) = OperateurPrioritaire(l, 4, solution=[])
            if niveau >= 4:
                break
        exo.append("  \\[\\thenocalcul = %s\\]" % Affichage(l))
        cor.append("  \\[\\thenocalcul = %s\\]" % Affichage(l))
        for l in sol:
            if l == sol[-1]:
                cor.append("  \\[\\boxed{\\thenocalcul = %s}\\]" % l)
            else:
                cor.append("  \\[\\thenocalcul = %s\\]" % l)
        exo.append("  \\stepcounter{nocalcul}%")
        cor.append("  \\stepcounter{nocalcul}%")
    exo.append("\\end{multicols}\n")
    cor.append("\\end{multicols}\n")
    return (exo, cor)

exo_sommes_fractions()
