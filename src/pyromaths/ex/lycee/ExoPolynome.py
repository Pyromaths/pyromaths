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

from random import randrange
from pyromaths.classes.Polynome import Polynome, TeX, RacineDegre2
from pyromaths.classes.Racine import simplifie_racine
from pyromaths.outils.Priorites3 import priorites
from pyromaths.outils.Polynomes import poly_racines_entieres, poly_racines_fractionnaires, poly_racines_quelconques, poly_id_remarquables, poly_degre3_racines_entieres, TeX_division, poly_degre3_racines_fractionnaires, randint
# from pyromaths.outils.decimaux import decimaux
from pyromaths.outils.Affichage import pTeX, radicalTeX, fTeX
from pyromaths.outils.Arithmetique import pgcd
from math import sqrt



def exo_racines_degre2():
    '''exercice recherche de racines second degré'''

    exo = ["\\exercice"]
    cor = ["\\exercice*"]
    # intervalle pour les racines entières ou fractionnaire
    rac_min = -10
    rac_max = 10
    # denominateur maximmum pour les racines fractionnaires
    denom_max = 12
    # Valeurs absolues maximales des coefficients d'un polynôme quelconque
    abs_a = 1
    abs_b = 10
    abs_c = 10
    # X est le polynome P=x pour faciliter la construction des polynômes,
    inconnues = ['x', 'y', 'z', 't']
#     nom_poly = ['P', 'Q', 'R', 'S']

    exo.append(_(u"Résoudre les équations suivantes :"))
    cor.append(_(u"Résoudre les équations suivantes :"))
    exo.append("\\begin{enumerate}")
    cor.append("\\begin{enumerate}")


    # Racines entières
    nomP = 'P'
    var = inconnues[randrange(4)]
    X = Polynome({1:1}, var)
    P = poly_racines_entieres(rac_min, rac_max, X)

    exo.append("\\item $%s=0$\\par" % (P(var)))
    cor.append("\\item $%s=0$\\par" % (P(var)))
    cor = redaction_racines(P, nomP, var, cor)

    # Racines fractionnaires
    nomP = 'P'
    var = inconnues[randrange(4)]
    X = Polynome({1:1}, var)
    P = poly_racines_fractionnaires(rac_min, rac_max, denom_max, X)

    exo.append("\\item $%s=0$\\par" % (P(var)))
    cor.append("\\item $%s=0$\\par" % (P(var)))
    cor = redaction_racines(P, nomP, var, cor)

    # Racines quelconques
    nomP = 'P'
    var = inconnues[randrange(4)]
    X = Polynome({1:1}, var)
    P = poly_racines_quelconques(abs_a, abs_b, abs_c, X)

    exo.append("\\item $%s=0$\\par" % (P(var)))
    cor.append("\\item $%s=0$\\par" % (P(var)))
    redaction_racines(P, nomP, var, cor)

    exo.append("\\end{enumerate}")
    cor.append("\\end{enumerate}")
    return exo, cor

exo_racines_degre2.description = _(u'Équations 2° degré')
exo_racines_degre2.level = _(u'1.1èreS')


def exo_factorisation_degre2():
    '''exercice recherche de racines second degré'''

    exo = ["\\exercice"]
    cor = ["\\exercice*"]
    # intervalle pour les racines entières ou fractionnaire
    rac_min = -10
    rac_max = 10

    # X est le polynome P(x)=x pour faciliter la construction des polynômes,
    inconnues = ['x', 'y', 'z', 't']
    nom_poly = ['P', 'Q', 'R', 'S']

    exo.append(_(u"Factoriser les polynômes suivants :"))
    # cor=[]u"Factoriser les polynômes suivants :"]
    exo.append("\\begin{enumerate}")
    cor.append("\\begin{enumerate}")

####identites remarquables

    nomP = nom_poly[randrange(4)]
    var = inconnues[randrange(4)]
    X = Polynome({1:1}, var)
    P, sgns = poly_id_remarquables(rac_min, rac_max, X)  # sgns=-2,0 ou 2
    exo.append(_(u"\\item Factoriser  $%s(%s)=%s$ à l'aide d'une identité remarquable.") % (nomP, var, P(var)))
    cor.append(_("\\item Factoriser $%s(%s)=%s$") % (nomP, var, P(var)))

    factorisation, dummy = factorise_identites_remarquables(P, sgns, var, racines=True)

    factorise = "$$%s" % P
    for i in range(len(factorisation)):
        factorise += "=" + factorisation[i]
    cor.append(factorise + "$$")

####Racines entières
    nomP = nom_poly[randrange(4)]
    var = inconnues[randrange(4)]
    X = Polynome({1:1}, var)
    P = poly_racines_entieres(rac_min, rac_max, X)

    exo.append("\\item $%s(%s)=%s$" % (nomP, var, P(var)))
    cor.append(_("\\item Factoriser $%s(%s)=%s$\\par") % (nomP, var, P(var)))
    exo, cor = redaction_factorisation(P, nomP, exo, cor)

####Racines fractionnaires
    nomP = nom_poly[randrange(4)]
    var = inconnues[randrange(4)]
    X = Polynome({1:1}, var)
    # denominateur maximmum pour les racines fractionnaires
    denom_max = 12
    P = poly_racines_fractionnaires(rac_min, rac_max, denom_max, X)

    exo.append("\\item $%s(%s)=%s$" % (nomP, var, P(var)))
    cor.append(_("\\item Factoriser $%s(%s)=%s$\\par") % (nomP, var, P(var)))
    exo, cor = redaction_factorisation(P, nomP, exo, cor)


####Racines quelconques
    nomP = nom_poly[randrange(4)]
    var = inconnues[randrange(4)]
    X = Polynome({1:1}, var)
    # Valeurs absolues maximales des coefficients d'un polynôme quelconque
    abs_a = 1
    abs_b = 10
    abs_c = 10
    P = poly_racines_quelconques(abs_a, abs_b, abs_c, X)

    exo.append("\\item $%s(%s)=%s$" % (nomP, var, P(var)))
    cor.append(_("\\item Factoriser $%s(%s)=%s$\\par") % (nomP, var, P(var)))
    exo, cor = redaction_factorisation(P, nomP, exo, cor)

    exo.append("\\end{enumerate}")
    cor.append("\\end{enumerate}")
    return exo, cor

exo_factorisation_degre2.description = _(u'Factorisations 2° degré')
exo_factorisation_degre2.level = _(u'1.1èreS')


def exo_factorisation_degre3():
    '''exercice de factorisation degre3'''

    # intervalle pour les racines entières ou fractionnaire
    rac_min = -10
    rac_max = 10
    # denominateur maximmum pour les racines fractionnaires
    denom1 = 12
    # Valeurs absolues maximales des coefficients d'un polynôme quelconque
#     abs_a = 1
#     abs_b = 10
#     abs_c = 10
    # X est le polynome P=x pour faciliter la construction des polynômes, TODO : changer  l'inconnue
#     inconnues = ['x', 'y', 'z', 't']
#     nom_poly = ['P', 'Q', 'R', 'S']
    exo = ["\\exercice",
        "\\begin{enumerate}"]
    cor = ["\\exercice*",
         "\\begin{enumerate}"]

    X = Polynome({1:1}, var="x")
    racines_quelconques = [i for i in range(-10, 11)]
    E = poly_degre3_racines_entieres(rac_min, rac_max, X, racines=racines_quelconques)
    exo, cor = factorisation_degre3(E, "E", exo, cor, racines=racines_quelconques)
    F = poly_degre3_racines_fractionnaires(rac_min, rac_max, denom1, X)
    exo, cor = factorisation_degre3(F, "F", exo, cor)

    exo.append("\\end{enumerate}")
    cor.append("\\end{enumerate}")
    return exo, cor

exo_factorisation_degre3.description = _(u'Factorisations degré 3')
exo_factorisation_degre3.level = _(u'1.1èreS')


def exo_tableau_de_signe():
    # intervalle pour les racines entières ou fractionnaire
    rac_min = -10
    rac_max = 10
    # denominateur maximmum pour les racines fractionnaires
    denom1 = 12
    # Valeurs absolues maximales des coefficients d'un polynôme quelconque
    abs_a = 1
    abs_b = 10
    abs_c = 10
    # X est le polynome P=x pour faciliter la construction des polynômes, TODO : changer  l'inconnue
#     inconnues = ['x', 'y', 'z', 't']
#     nom_poly = ['P', 'Q', 'R', 'S']
    borneinf = -5  # float("-inf")
    bornesup = 5  # float("inf")
    var = "x"
    X = Polynome({1:1}, var=var)
    Poly = [poly_racines_entieres(rac_min, rac_max, X),
          poly_racines_fractionnaires(rac_min, rac_max, denom1, X),
          poly_racines_quelconques(abs_a, abs_b, abs_c, X)]
    intervalles = [[0, 5], [-5, 5], [float("-inf"), float("inf")]]
    exo = ["\\exercice",
        "\\begin{enumerate}"]
    cor = ["\\exercice*",
         "\\begin{enumerate}"]
    nomP = "P"
    for i in range(len(Poly)):
        P = Poly[i]
        borneinf, bornesup = intervalles[i]
        if borneinf == float("-inf") and bornesup == float("inf"):
            TeXintervalle = "\\mathbb R"
        else:
            if borneinf != float("-inf"):
                TeXintervalle = "["
            else:
                TeXintervalle = "]"
            TeXintervalle += "%s~;~%s" % (TeX(borneinf), TeX(bornesup))
            if bornesup == float("inf"):
                TeXintervalle += "["
            else:
                TeXintervalle += "]"
        exo.append(_(u"\\item Étudier le signe du polynôme $%s=%s$ sur $I=%s$.") % (nomP, P, TeXintervalle))
        cor.append(_(u"\\item Étudier le signe du polynôme $%s=%s$ sur $I=%s$.\\par") % (nomP, P, TeXintervalle))

        delta, dummy, racines, dummy, dummy = factorisation_degre2(P, factorisation=False)
        redaction_racines(P, nomP, var, cor)
        tableau_de_signe(P, nomP, delta, racines, cor, borneinf, bornesup, detail=False)
    exo.append("\\end{enumerate}")
    cor.append("\\end{enumerate}")
    return exo, cor

exo_tableau_de_signe.description = _(u'Étude de signe')
exo_tableau_de_signe.level = _(u'1.1èreS')


def exo_variation():

    exo = ["\\exercice",
         "\\begin{enumerate}"]
    cor = ["\\exercice*",
         "\\begin{enumerate}"]
    quest1, cor1 = quest_fonctions_rationnelles()
    quest2, cor2 = quest_variation_degre3(borneinf=-10, bornesup=10)

    exo += quest1 + quest2
    cor += cor1 + cor2

    exo.append("\\end{enumerate}")
    cor.append("\\end{enumerate}")
    return exo, cor

exo_variation.description = _(u"Sens de variations")
exo_variation.level = [_(u"1.1èreS"), _(u"0.Term STMG")]


def exo_variation_lim():
    """Étude de fonctions avec calculs de limites"""
    exo = ["\\exercice",
         "\\begin{enumerate}"]
    cor = ["\\exercice*",
         "\\begin{enumerate}"]
    quest3, cor3 = quest_variation_degre3(borneinf=float("-inf"), bornesup=float("+inf"))
    quest4, cor4 = quest_fonctions_rationnelles_sur_R()
    exo += quest3 + quest4
    cor += cor3 + cor4

    exo.append("\\end{enumerate}")
    cor.append("\\end{enumerate}")
    return exo, cor

exo_variation_lim.description = _(u"Étude de fonctions")
exo_variation_lim.level = _(u"0.Term S")

def quest_fonctions_rationnelles():
    from pyromaths.classes.Fractions import Fraction
    from pyromaths.outils import Priorites3

    nomf = ['f', 'g', 'h', 'k'][randrange(4)]
    var = ['t', 'x'][randrange(2)]
    X = Polynome({1:1}, var)
    # intervalle pour les racines entières ou fractionnaire

    rac_min = -9
    rac_max = 9
    b1 = b2 = a1 = a2 = 0
    while b1 == 0 or b2 == 0 or a1 == 0 or a2 == 0:
        b1 = randint(rac_min, rac_max)
        b2 = randint(rac_min, rac_max)
        a1 = randint(-5, 5)
        a2 = randint(-5, 5)
    P = a1 * X + b1
    Q = a2 * X + b2

    borneinf = -10
    bornesup = 10
    racine = eval(Priorites3.priorites("-%r/%r" % (Q[0], Q[1]))[-1][0])
    # Je veux que f soit définie et dérivable sur I=Intervalle
    if (racine >= borneinf) and (racine <= bornesup):
        if (racine - borneinf) < (bornesup - racine):
            Intervalle = [int(round(racine)) + 1, bornesup]
        else:
            Intervalle = [borneinf, int(round(racine)) - 1]
    else:
        Intervalle = [borneinf, bornesup]

    # dérivée
    numerateur = "%s\\times%s-%s\\times%s" % (P.derive().TeX(parenthese=True), Q.TeX(parenthese=True),
                                          P.TeX(parenthese=True), Q.derive().TeX(parenthese=True))
    numerateur_simplifie = (P.derive() * Q - P * Q.derive()).simplifie()
    denominateur = u"%s^2" % (Q.TeX(parenthese=True))
    f_derivee = "\\dfrac{%s}{%s}" % (numerateur, denominateur)
    f_derivee_simplifiee = "\\dfrac{%s}{%s}" % (numerateur_simplifie, denominateur)
    VI = eval(priorites('-%r*Fraction(1)/%r' % (Q[0], Q[1]))[-1][0])
    if isinstance(VI, (Fraction, RacineDegre2)): VI = VI.simplifie()
    exo = [_(u"\\item On considère la fonction $%s$ définie sur $I=[%s~;~%s]$ par $%s(%s)=\dfrac{%s}{%s}$.") % (nomf, Intervalle[0], Intervalle[1], nomf, var, P, Q),
         "\\begin{enumerate}"]
    cor = [_(u"\\item On considère la fonction $%s$ définie sur $I=[%s~;~%s]$ par $%s(%s)=\dfrac{%s}{%s}$.") % (nomf, Intervalle[0], Intervalle[1], nomf, var, P, Q),
         "\\begin{enumerate}"]

    exo.append(_(u"\\item Justifier que $%s$ est définie et dérivable sur $I$.") % (nomf))
    cor.append(_(u"\\item Justifier que $%s$ est définie et dérivable sur $I$.") % (nomf))
    cor.append(_(u" Pour déterminer la valeur interdite, on doit résoudre $%s=0$.") % (Q(var)))
    cor.append("\\begin{align*}")
    cor.append("%s&=0\\\\" % Q)
    cor.append("%s&=%s" % ((Q - Q[0]), TeX(-Q[0])))
    cor.append("\\\\")
    if Q[1] != 1:
        x0 = eval(priorites('-%r*Fraction(1)/%r' % (Q[0], Q[1]))[-1][0])
        if isinstance(x0, (Fraction, RacineDegre2)):
            x1 = x0.simplifie()
        else:
            x1 = x0
        cor.append("%s&=%s" % (var, Fraction(-Q[0], Q[1])))
        cor.append("\\\\")
        if isinstance(x0, (Fraction, RacineDegre2)) and (not isinstance(x1, (Fraction, RacineDegre2)) or x0.d != x1.d):
            cor.append("%s&=%s" % (var, TeX(x1)))
            cor.append("\\\\")
    cor.pop(-1)
    cor.append("\\end{align*}")
    cor.append(_(u"Or $%s$ n'est pas dans l'intervalle $[%s~;~%s]$ et comme $%s$ est un quotient de polynômes, alors $%s$ est définie et dérivable sur $I$.") % \
               (TeX(VI), Intervalle[0], Intervalle[1], nomf, nomf))
    exo.append(_(u"\\item Déterminer $%s'(%s)$ pour tout $%s\in[%s~;~%s]$.") % \
          (nomf, var, var, Intervalle[0], Intervalle[1]))
    cor.append(_(u"\\item Déterminer $%s'(%s)$ pour tout $%s\in[%s~;~%s]$.") % \
          (nomf, var, var, Intervalle[0], Intervalle[1]))
    cor.append(u"$$%s'(%s)=%s=%s$$" % (nomf, var, f_derivee, f_derivee_simplifiee))
    exo.append(_(u"\\item En déduire le sens de variations de $%s$ sur $I$.") % (nomf))
    cor.append(_(u"\\item En déduire le sens de variations de $%s$ sur $I$.\\par") % (nomf))
    if numerateur_simplifie.degre_max == 0:
        cor.append(_(u" Comme $%s$ est un carré, il est toujours positif.\\\\") % (denominateur))
        f_xmin = eval(priorites('%r*Fraction(1)/%r' % (P(Intervalle[0]), Q(Intervalle[0])))[-1][0])
        f_xmax = eval(priorites('%r*Fraction(1)/%r' % (P(Intervalle[1]), Q(Intervalle[1])))[-1][0])
        if isinstance(f_xmin, (Fraction, RacineDegre2)): f_xmin = f_xmin.simplifie()
        if isinstance(f_xmax, (Fraction, RacineDegre2)): f_xmax = f_xmax.simplifie()
        f_xmin = TeX(f_xmin)
        f_xmax = TeX(f_xmax)
        if numerateur_simplifie[0] < 0:
            cor.append(_(u" De plus, $%s<0$ donc pour tout $%s$ de $I$, $%s'(%s)<0$. Ainsi, on obtient \\par") % \
                  (numerateur_simplifie[0], var, nomf, var))
            cor.append("\\begin{tikzpicture}\n\\tkzTabInit[espcl=2.5]")
            cor.append("{$%s$ /1, $%s'\\,(x)$/1, $%s\\,(x)$/1.5}" % (var, nomf, nomf))
            cor.append("{$%s$,$%s$}" % (TeX(Intervalle[0]), TeX(Intervalle[1])))
            cor.append("\\tkzTabLine{,-,}")
            cor.append("\\tkzTabVar{+/$%s$/, -/$%s$/}" % (f_xmin, f_xmax))
            cor.append(r'\end{tikzpicture}\par')
            #===================================================================
            # cor.append("$$\\tabvar{")
            # cor.append("\\tx{%s}&\\tx{%s}&&\\tx{%s}\\cr" % (var, TeX(Intervalle[0]), TeX(Intervalle[1])))
            # cor.append("\\tx{%s'(%s)}&&\\tx{-}&&\\cr" % (nomf, var))
            # cor.append("\\tx{%s}&\\txh{%s}&\\fd&\\txb{%s}\\cr" % (nomf, f_xmin, f_xmax))
            # cor.append("}$$")
            #===================================================================
        else:
            cor.append(_(u" De plus, $%s>0$ donc pour tout $%s$ de $I$, $%s'(%s)>0$.\\par") % \
                  (numerateur_simplifie[0], var, nomf, var))
            cor.append("\\begin{tikzpicture}\n\\tkzTabInit[espcl=2.5]")
            cor.append("{$%s$ /1, $%s'\\,(x)$/1, $%s\\,(x)$/1.5}" % (var, nomf, nomf))
            cor.append("{$%s$,$%s$}" % (TeX(Intervalle[0]), TeX(Intervalle[1])))
            cor.append("\\tkzTabLine{,+,}")
            cor.append("\\tkzTabVar{-/$%s$/, +/$%s$/}" % (f_xmin, f_xmax))
            cor.append(r'\end{tikzpicture}\par')
            #===================================================================
            # cor.append("$$\\tabvar{")
            # cor.append("\\tx{%s}&\\tx{%s}&&\\tx{%s}\\cr" % (var, TeX(Intervalle[0]), TeX(Intervalle[1])))
            # cor.append("\\tx{%s'(%s)}&&\\tx{+}&&\\cr" % (nomf, var))
            # cor.append("\\tx{%s}&\\txb{%s}&\\fm&\\txh{%s}\\cr" % (nomf, f_xmin, f_xmax))
            # cor.append("}$$")
            #===================================================================
    else:
        cor.append(_(u" Je ne sais pas faire avec un tel numérateur $%s$.") % (numerateur_simplifie))
    exo.append("\\end{enumerate}")
    cor.append("\\end{enumerate}")
    return exo, cor

def quest_fonctions_rationnelles_sur_R():
    from pyromaths.classes.Fractions import Fraction

    nomf = ['f', 'g', 'h', 'k'][randrange(4)]
    var = ['t', 'x'][randrange(2)]
    X = Polynome({1:1}, var)
    # intervalle pour les racines entières ou fractionnaire

    rac_min = -9
    rac_max = 9
    b1 = b2 = a1 = a2 = 0
    while b1 == 0 or b2 == 0 or a1 == 0 or a2 == 0 or a1 * (-float(b2) / a1) + b1 == 0 or (a1 * b2 / a2 - b1) == 0:
        # (a1*b2/a2 - b1)==0 on teste que la racine de Q n'annule pas P donc on ne peut pas simplifier
        b1 = randint(rac_min, rac_max)
        b2 = randint(rac_min, rac_max)
        a1 = randint(-5, 5)
        a2 = randint(-5, 5)
    P = a1 * X + b1
    Q = a2 * X + b2

    borneinf = float("-inf")
    bornesup = float("+inf")
    Intervalle = [borneinf, bornesup]
#     TeXintervalle = "\\mathbb R"

    # dérivée
    numerateur = "%s\\times%s-%s\\times%s" % (P.derive().TeX(parenthese=True), Q.TeX(parenthese=True),
                                          P.TeX(parenthese=True), Q.derive().TeX(parenthese=True))
    numerateur_simplifie = (P.derive() * Q - P * Q.derive()).simplifie()
    # VI = (-Q[0] * Fraction(1) / Q[1]).simplifie()
    #===========================================================================
    # print "A simplifier : ", priorites('-%r*Fraction(1)/%r' % (Q[0], Q[1]))[-1][0]
    #===========================================================================
    VI = eval(priorites('-%r*Fraction(1)/%r' % (Q[0], Q[1]))[-1][0])
    if isinstance(VI, (Fraction, RacineDegre2)): VI.simplifie()
    denominateur = u"%s^2" % (Q.TeX(parenthese=True))
    f_derivee = "\\dfrac{%s}{%s}" % (numerateur, denominateur)
    f_derivee_simplifiee = "\\dfrac{%s}{%s}" % (numerateur_simplifie, denominateur)

    exo = [_(u"\\item On considère la fonction $%s$ définie  par $%s(%s)=\\dfrac{%s}{%s}$.") % (nomf, nomf, var, P, Q),
         "\\begin{enumerate}"]
    cor = [_(u"\\item On considère la fonction $%s$ définie  par $%s(%s)=\\dfrac{%s}{%s}$.") % (nomf, nomf, var, P, Q),
         "\\begin{enumerate}"]

    exo.append(_(u"\\item Déterminer l'ensemble de définition $\\mathcal{D}_{%s}$ de $%s$.") % (nomf, nomf))
    cor.append(_(u"\\item Déterminer l'ensemble de définition $\\mathcal{D}_{%s}$ de $%s$.\par") % (nomf, nomf))
    cor.append(_(u" La fonction rationnelle $%s$ est définie et dérivable en $%s$ si $%s\\neq0$.") % (nomf, var, Q(var)))
    cor.append("\\begin{align*}\n\
            %s&=0\\\\\n\
            %s&=%s\\\\\n\
            %s&=%s\\\\\n\
            %s&=%s\n\
            \\end{align*}" % (Q, (Q - Q[0]), TeX(-Q[0]), var, TeX(-Q[0] * Fraction(1) / Q[1]), var, TeX(VI)))
    cor.append(_(u"On en déduit que $\\mathcal{D}_{%s}=\\mathcal{D'}_{%s}=]-\\infty~;~%s[\cup]%s~;~+\\infty[$.") % \
          (nomf, nomf, TeX(VI), TeX(VI)))
    exo.append(_(u"\\item Déterminer $%s'(%s)$ pour tout $%s\in\\mathcal{D'}_{%s}$.") % \
          (nomf, var, var, nomf))
    cor.append(_(u"\\item Déterminer $%s'(%s)$ pour tout $%s\in\\mathcal{D'}_{%s}$.") % \
          (nomf, var, var, nomf))
    cor.append(u"$$%s'(%s)=%s=%s$$" % (nomf, var, f_derivee, f_derivee_simplifiee))
    exo.append(_(u"\\item Déterminer les limites de $%s$ aux bornes de $\\mathcal{D}_{%s}$.") % (nomf, nomf))
    cor.append(_(u"\\item Déterminer les limites de $%s$ aux bornes de $\\mathcal{D}_{%s}$.") % (nomf, nomf))
    #===========================================================================
    # limite = P[1] / Q[1]
    #===========================================================================
    limite = eval(priorites('-%r*Fraction(1)/%r' % (P[1], Q[1]))[-1][0])
    if isinstance(limite, (Fraction, RacineDegre2)):
        limite_simple = limite.simplifie()
    else:
        limite_simple = limite

    cor.append("$$\\lim_{%s\\to -\\infty}\\dfrac{%s}{%s}= " % (var, P, Q))

    cor.append("\\lim_{%s\\to -\\infty}\\dfrac{%s%s}{%s%s} = %s" % (var, coeffTeX(P[1]), var, coeffTeX(Q[1]), var, limite))
    if isinstance(limite, (int, float)) or (isinstance(limite_simple, (Fraction, RacineDegre2)) and limite.n == limite_simple.n):
        cor.append("$$")
    else:
        cor.append("= %s $$" % (TeX(limite_simple)))
    cor.append("$$\\lim_{%s\\to +\\infty}\\dfrac{%s}{%s}= " % (var, P, Q))
    cor.append("\\lim_{%s\\to +\\infty}\\dfrac{%s%s}{%s%s} = %s" % (var, coeffTeX(P[1]), var, coeffTeX(Q[1]), var, limite))
    if isinstance(limite, (int, float)) or (isinstance(limite_simple, (Fraction, RacineDegre2)) and limite.n == limite_simple.n):
        cor.append("$$")
    else:
        cor.append("= %s $$" % (TeX(limite_simple)))
    cor.append("Pour $%s=%s$, on a $%s=%s" % (var, TeX(VI), P, TeX(P(VI))))
    if P(VI) < 0:
        limites = ["-\\infty", "+\\infty"]
        cor.append("<0$.\\\\")
    elif P(VI) > 0:
        limites = ["+\\infty", "-\\infty"]
        cor.append(">0$.\\\\")
    else:cor.append("$.\\\\")
        # Impossible car on test (a1*b2/a2 - b1)!=0

    VIplus = "\\substack{%s\\to %s\\\\%s>%s}" % (var, fTeX(VI), var, fTeX(VI))
    VImoins = "\\substack{%s\\to %s\\\\%s<%s}" % (var, fTeX(VI), var, fTeX(VI))
    if Q[1] < 0:
        cor.append(_("De plus, $%s>0$ si $%s<%s$") % (Q, var, TeX(VI)))
        cor.append(_("et  $%s<0$ si $%s>%s$.\\\\") % (Q, var, TeX(VI)))
    else:
        cor.append(_("De plus, $%s<0$ si $%s<%s$") % (Q, var, TeX(VI)))
        cor.append(_("et  $%s>0$ si $%s>%s$.\\\\") % (Q, var, TeX(VI)))

    cor.append(u"$$\\lim_{%s}\\dfrac{%s}{%s}=%s $$" % (VImoins, P, Q, limites[0]))
    cor.append(u"$$\\lim_{%s}\\dfrac{%s}{%s}=%s $$" % (VIplus, P, Q, limites[1]))



    exo.append(_(u"\\item Dresser le tableau de variations de $%s$ sur $\\mathcal{D}_{%s}$.") % (nomf, nomf))
    cor.append(_(u"\\item Dresser le tableau de variations de $%s$ sur $\\mathcal{D}_{%s}$.\\par") % (nomf, nomf))
    if numerateur_simplifie.degre_max == 0:
        cor.append(_(u" Comme $%s$ est un carré, il est toujours positif.\\\\") % (denominateur))
        f_xmin = eval(priorites('-%r*Fraction(1)/%r' % (P[1], Q[1]))[-1][0])
        if isinstance(f_xmin, (Fraction, RacineDegre2)):
            f_xmin = f_xmin.simplifie()
        f_xmax = f_xmin
        if numerateur_simplifie[0] < 0:
            cor.append(_(u" De plus, $%s<0$ donc pour tout $%s$ de $I$, $%s'(%s)<0$. Ainsi, on obtient \\par") % \
                  (numerateur_simplifie[0], var, nomf, var))
            cor.append("\\begin{tikzpicture}\n\\tkzTabInit[espcl=2.5]")
            cor.append("{$%s$ /1, $%s'\\,(x)$/1, $%s\\,(x)$/1.5}" % (var, nomf, nomf))
            cor.append("{$%s$,$%s$,$%s$}" % (TeX(Intervalle[0]), TeX(VI), TeX(Intervalle[1])))
            cor.append("\\tkzTabLine{,-,d,-}")
            cor.append("\\tkzTabVar{+/$%s$ / ,-D+/ $-\\infty$ /$+\infty$, -/$%s$/}" % (f_xmin, f_xmax))
            cor.append(r'\end{tikzpicture}\par')
            #===================================================================
            # cor.append("$$\\tabvar{")
            # cor.append("\\tx{%s}&\\tx{%s}&&&\\tx{%s}&&&\\tx{%s}\\cr" % (var, TeX(Intervalle[0]), TeX(VI), TeX(Intervalle[1])))
            # cor.append("\\tx{%s'(%s)}&&\\tx{-}&&\\dbt &&\\tx{-}&\\cr" % (nomf, var))
            # cor.append("\\tx{%s}&\\txh{%s}&\\fd&\\txb{-\\infty}&\\dbt&\\txh{+\\infty}&\\fd&\\txb{%s}\\cr" % (nomf, f_xmin, f_xmax))
            # cor.append("}$$")
            #===================================================================
        else:
            cor.append(_(u" De plus, $%s>0$ donc pour tout $%s$ de $I$, $%s'(%s)>0$. \\par") % \
                  (numerateur_simplifie[0], var, nomf, var))
            cor.append("\\begin{tikzpicture}\n\\tkzTabInit[espcl=2.5]")
            cor.append("{$%s$ /1, $%s'\\,(x)$/1, $%s\\,(x)$/1.5}" % (var, nomf, nomf))
            cor.append("{$%s$,$%s$,$%s$}" % (TeX(Intervalle[0]), TeX(VI), TeX(Intervalle[1])))
            cor.append("\\tkzTabLine{,+,d,+}")
            cor.append("\\tkzTabVar{-/$-\\infty$ / ,+D-/ $%s$ /$%s$, +/$+\\infty$/}" % (f_xmin, f_xmax))
            cor.append(r'\end{tikzpicture}\par')
            #===================================================================
            # cor.append("$$\\tabvar{")
            # cor.append("\\tx{%s}&\\tx{%s}&&&\\tx{%s}&&&\\tx{%s}\\cr" % (var, TeX(Intervalle[0]), TeX(VI), TeX(Intervalle[1])))
            # cor.append("\\tx{%s'(%s)}&&\\tx{+}&&\\dbt&&\\tx{+}&\\cr" % (nomf, var))
            # cor.append("\\tx{%s}&\\txb{%s}&\\fm&\\txh{+\\infty}&\\dbt&\\txb{-\\infty}&\\fm&\\txh{%s}\\cr" % (nomf, f_xmin, f_xmax))
            # cor.append("}$$")
            #===================================================================
    else:
        cor.append(_(u" Je ne sais pas faire avec un tel numérateur $%s$.") % (numerateur_simplifie))
    exo.append("\\end{enumerate}")
    cor.append("\\end{enumerate}")
    return exo, cor

def coeffTeX(a):
        if a == 1:return ""
        if a == -1:return "-"
        return a

def quest_variation_degre3(borneinf=float("-inf"), bornesup=float("+inf")):
    '''Question qui propose l'étude du sens de variation d'un polynôme de degré 3'''
#     Intervalle = [borneinf, bornesup]
    if borneinf == float("-inf") and bornesup == float("+inf"):
        TeX_intervalle = "\\mathbb R"
    else:
        TeX_intervalle = "\\left[%s~;~%s\\right]" % (TeX(borneinf), TeX(bornesup))
    # intervalle pour les racines entières ou fractionnaire
    a = 3 * randint(1, 3)
    rac_min = -9
    rac_max = 9
    # denominateur maximmum pour les racines fractionnaires
#     denom_max = denom1 = 12
    # Valeurs absolues maximales des coefficients d'un polynôme quelconque
#     abs_a = 6
#     abs_b = 10
    abs_c = 10
    # X est le polynome P=x pour faciliter la construction des polynômes,
#     inconnues = ['x', 'y', 'z', 't']
#     nom_poly = ['P', 'Q', 'R', 'S']
    var = "x"
    X = Polynome({1:1}, var=var)
    nomP = ["f", "g", "h", "k", "p", "q"][randrange(6)]
    Pprime = poly_racines_entieres(rac_min, rac_max, X, a1=a)
    P = Pprime.primitive() + randint(-abs_c, abs_c)
    P = P.simplifie()
    exo = [_(u"\\item Étudier le sens de variations de $%s$ définie par $%s(x)=%s$ sur $%s$.") % (nomP, nomP, P(var), TeX_intervalle)]
    cor = [_(u"\\item Étudier le sens de variations de $%s$ définie par $%s(x)=%s$ sur $%s$.") % (nomP, nomP, P(var), TeX_intervalle)]

    cor.append("\\par $%s'(x)=%s$\\\\" % (nomP, Pprime(var)))
    cor.append(_(u"Je dois étudier le signe de $%s'(%s)$ qui est un polynôme du second degré.\\par") % (nomP, var))

    delta, simplrac, racines, str_racines, factorisation = factorisation_degre2(Pprime, factorisation=False)
    # cor=redaction_factorisation(Pprime,nomP+"'",exo=[],cor=cor)[1]
    # cor.pop(-5)
    redaction_racines(Pprime, nomP + "'", var, cor)
    str_variables, str_signes, str_valeurs, signes, ligne_valeurs = tableau_de_signe(Pprime, nomP + "'", delta, racines, cor, borneinf, bornesup, detail=True)

    # cor.append(tab_signe)


    if (delta <= 0 and P[3] < 0):
        cor += _(u"Donc la fonction polynômiale $%s$ est décroissante sur $%s$.") % (nomP, TeX_intervalle)
    elif (delta <= 0 and P[3] > 0):
        cor.append(_(u"Donc la fonction polynômiale $%s$ est croissante sur $%s$.") % (nomP, TeX_intervalle))
    else:
        cor.append(_("On obtient ainsi le tableau de variation de $%s$.\\par") % nomP)
#         [x1, x2] = racines
        # macro=[["txb","txh"],["fm","fd"]]
        cor.append("\\begin{tikzpicture}\n\\tkzTabInit[espcl=2.5]")
        cor.append(str_variables[:-1] + ', $%s\\,(x)$/1.5}' % nomP)
        cor.append(str_valeurs)
        cor.append(str_signes)
        var_de_P = "\\tkzTabVar{%s/$%s$, " % (["-", "+"]["-" == signes[0]], TeX(P(ligne_valeurs[0])))  # +/$%s$/, -/$%s$/}" % (f_xmin, f_xmax))
        #=======================================================================
        # var_de_P = "\\tx{%s}& \\%s{\\rnode{neu0}{%s}}&&" % (nomP, ["txb", "txh"]["-" == signes[0]], TeX(P(ligne_valeurs[0])))
        #=======================================================================
        compteur = 0
        for i in range(0, len(signes) - 1):
            if signes[i] == '+':
                if 0 and signes[i + 1] == "+":
                    var_de_P += "&&"
                else:
                    compteur += 1
                    var_de_P += "+/$%s$/, " % TeX(P(ligne_valeurs[i + 1]))
                    #===========================================================
                    # var_de_P += "\\txh{\\rnode{neu%s}{%s}}&&" % (compteur, TeX(P(ligne_valeurs[i + 1])))
                    #===========================================================
            else:
                if 0 and signes[i + 1] == "-":
                    var_de_P += "&&"
                else:
                    compteur += 1
                    var_de_P += "-/$%s$/, " % TeX(P(ligne_valeurs[i + 1]))
                    #===========================================================
                    # var_de_P += "\\txb{\\rnode{neu%s}{%s}}&&" % (compteur, TeX(P(ligne_valeurs[i + 1])))
                    #===========================================================
        compteur += 1
        if signes[-1] == "+":
            var_de_P += "+/$%s$/} " % TeX(P(ligne_valeurs[-1]))
            #===================================================================
            # var_de_P += "\\txh{\\rnode{neu%s}{%s}}\\cr" % (compteur, TeX(P(ligne_valeurs[-1])))
            #===================================================================
        else:
            var_de_P += "-/$%s$/} " % TeX(P(ligne_valeurs[-1]))
            #===================================================================
            # var_de_P += "\\txb{\\rnode{neu%s}{%s}}\\cr" % (compteur, TeX(P(ligne_valeurs[-1])))
            #===================================================================

        cor.append(var_de_P)
        #=======================================================================
        # cor.append("$$ \\tabvar{\n %s\n %s\n %s}$$" % \
        #            (str_valeurs, str_signes, var_de_P))
        #=======================================================================
        #=======================================================================
        # for i in range(1, compteur + 1):
        #     cor.append("\\ncline[nodesep=0.15,linewidth=0.5pt]{->}{neu%s}{neu%s}" % (i - 1, i))
        #=======================================================================
        cor.append(r'\end{tikzpicture}\par')

        if borneinf == float("-inf"):
            cor.append(u"$$\\lim_{%s\\to %s} %s= \\lim_{%s\\to %s} %s%s^3=%s $$  " % (var, "-\\infty", P, var, "-\\infty", P[3], var, TeX(P(float("-inf")))))
        if bornesup == float("+inf"):
            cor.append(u"$$\\lim_{%s\\to %s} %s= \\lim_{%s\\to %s} %s%s^3=%s  $$ " % (var, "+\\infty", P, var, "+\\infty", P[3], var, TeX(P(float("inf")))))
    return exo, cor


                ###############################################
                #                                             #
                #   Fonctions étudiant les polynômes          #
                #                                             #
                ###############################################

def tableau_de_signe(P, nomP, delta, racines, cor, borneinf=float("-inf"), bornesup=float("+inf"), detail=False):
    '''Étudie le signe d'un polynôme de degré2'''
    ''' ne fonctionne pas si on a pas borneinf < x1< x2 <bornesup'''
    '''detail=True permet de récupérer la dernière ligne avec le signe de P'''
    var = P.var
    signe_moinsa, signe_a = [('+', '-'), ('-', '+')][P[2] > 0]  # Ca donne bien ce qu'on veut...
    signes = []
    str_variables = "{$%s$/1, $%s\\,(x)$/1}" % (var, nomP)
    if delta < 0:
        cor.append(_("Comme $\\Delta <0$, $%s(%s)$ ne s'annule pas et est toujours du signe de $a$") % (nomP, var))
        cor.append(_("Ainsi "))
        str_valeurs = "{$%s$,$%s$}" % (TeX(borneinf), TeX(bornesup))
        str_signes = "\\tkzTabLine{,%s}" % signe_a
        # str_valeurs = "\\tx{%s}&\\tx{%s}&& \\tx{%s}\\cr" % (var, TeX(borneinf), TeX(bornesup))
        # str_signe = "\\tx{%s(%s)}&&\\tx{%s}&\\cr" % (nomP, var, signe_a)
        signes = [signe_a]
        ligne_valeurs = [borneinf, bornesup]
    elif delta == 0:
        cor.append(_("Comme $\\Delta =0$, $%s(%s)$ s'annule une seule fois pour $%s_0=%s$ et est toujours du signe de $a$.\\par") % (nomP, var, var, racines[0]))
        if racines[0] < borneinf or racines[0] > bornesup:
            if borneinf != float("-inf"):
                intervalle = "["
            else:
                intervalle = "]"
            intervalle += "%s~;~%s" % (TeX(borneinf), TeX(bornesup))
            if bornesup == float("inf"):
                intervalle += "["
            else:
                intervalle += "]"
            cor.append(_("Or $%s$ n'est pas dans l'intervalle $%s$ donc ") % (TeX(racines[0]), intervalle))
            ligne_valeurs = [borneinf, bornesup]

            str_valeurs = "{$%s$,$%s$}" % (TeX(borneinf), TeX(bornesup))
            str_signes = "\\tkzTabLine{,%s}" % signe_a
#===============================================================================
#             str_valeurs = "\\tx{%s}&\\tx{%s}&& \\tx{%s}\\cr" % (var, TeX(borneinf), TeX(bornesup))
#
#             str_signe = "\\tx{%s(%s)}&&\\tx{%s}&\\cr" % (nomP, var, signe_a)
#===============================================================================
            signes = [signe_a]
        else:

            ligne_valeurs = [borneinf, racines[0], bornesup]
            str_valeurs = "{$%s$,$%s$,$%s$}" % (TeX(borneinf), TeX(racines[0]), TeX(bornesup))
            str_signes = "\\tkzTabLine{,%s,0,%s}" % (signe_a, signe_a)
            #===================================================================
            # str_valeurs = "\\tx{%s}&\\tx{%s}&& \\tx{%s}&& \\tx{%s}\\cr" % (var, TeX(borneinf), TeX(racines[0]), TeX(bornesup))
            # str_signe = "\\tx{%s(%s)}&&\\tx{%s}&\\tx{0}&\\tx{%s}&\\cr" % (nomP, var, signe_a, signe_a)
            #===================================================================
            signes = [signe_a, signe_a]
    elif delta > 0:
        [x1, x2] = racines
        cor.append(_("Comme $\\Delta >0$, $%s(%s)$ est du signe de $-a$ entre les racines.") % (nomP, var))
        compare = [(x1 <= borneinf) + (x2 <= borneinf), (x2 >= bornesup) + (x1 >= bornesup)]
        # x_x1=x_x2=sign_x1=sign_x2=""
        if compare != [0, 0]:
            if borneinf != float("-inf"):
                intervalle = "["
            else:
                intervalle = "]"
            intervalle += "%s~;~%s" % (TeX(borneinf), TeX(bornesup))
            if bornesup == float("inf"):
                intervalle += "["
            else:
                intervalle += "]"

        ligne_valeurs = [borneinf]
        if compare[0] >= 1 or compare[1] == 2:
            x_x1 = sign_x1 = ""
        else:
            x_x1 = "$%s$," % (TeX(x1))
            ligne_valeurs += [x1]
            sign_x1 = ",%s,0" % (signe_a)
            signes += [signe_a]

        if 2 in compare:
            entreracines = ",%s" % (signe_a)
            signes += [signe_a]
        else:
            entreracines = ",%s" % (signe_moinsa)
            signes += [signe_moinsa]

        if compare[1] >= 1 or compare[0] == 2:
            x_x2 = sign_x2 = ""
        else:
            x_x2 = "$%s$," % (TeX(x2))
            ligne_valeurs += [x2]
            sign_x2 = ",0,%s" % (signe_a)
            signes += [signe_a]
        ligne_valeurs += [bornesup]
        # Ne rien dire si une racine est égale à une borne
        compare = [compare[0] - (x1 == borneinf) - (x2 == borneinf), compare[1] - (x1 == bornesup) - (x2 == bornesup)]

        if sum(compare) == 2 :
            # les deux racines sont à supprimer
            cor.append(_("\\par Or $%s$ et $%s$ ne sont pas dans $%s$.") % (TeX(x1), TeX(x2), intervalle))

        elif compare[0] == 1:
            cor.append(_("\\par Or $%s$ n'est pas dans $%s$.") % (TeX(x1), intervalle))
        elif compare[1] == 1:
            cor.append(_("\\par Or $%s$ n'est pas dans $%s$.") % (TeX(x2), intervalle))
        cor.append("Ainsi \\par")

        str_valeurs = "{$%s$, %s %s $%s$}" % (TeX(borneinf), x_x1, x_x2, TeX(bornesup))
        str_signes = "\\tkzTabLine{%s%s%s}" % (sign_x1, entreracines, sign_x2)

#===============================================================================
#         str_valeurs = "\\tx{%s}& \\tx{%s}& %s %s & \\tx{%s}\\cr" % (var, TeX(borneinf), x_x1, x_x2, TeX(bornesup))
#
#         str_signe = "\\tx{%s(%s)}&%s %s %s&\\cr" % (nomP, var, sign_x1, entreracines, sign_x2)
#===============================================================================

    cor.append("\\begin{tikzpicture}\n\\tkzTabInit[espcl=2.5]")
    cor.append(str_variables)
    cor.append(str_valeurs)
    cor.append(str_signes)
    cor.append(r'\end{tikzpicture}\par')
    #===========================================================================
    # cor.append("$$\\tabvar{")
    # cor.append(str_valeurs)
    # cor.append("%s}$$" % (str_signe))
    #===========================================================================
    if detail:
        return str_variables, str_signes, str_valeurs, signes, ligne_valeurs

def factorise_identites_remarquables(pol1, sgns, var='', racines=True):
    '''Factorise un polynomes grâce aux identités remarquables'''
    from pyromaths.classes.Fractions import Fraction
    if var == '':
        var = pol1.var
    X = Polynome({1:1}, var)
    a1 = pgcd(int(pol1[0]), pgcd(int(pol1[1]), int(pol1[2])))  # du signe de a=pol1[2]
    if a1 != 1 or a1 != -1:
        pol2 = pol1 / a1
    else:
        pol2 = pol1
    # coeff=coeff/int(math.sqrt(a1))
    # pol2=(cx)^2 ±2× cx × b + b^2
    # pol2[2]=c^2
    # pol2[1]=2× cx × b
    # pol2[0] = b^2
    c = int(sqrt(pol2[2]))  # problème d'arrondi ?

    factorisation = []
    if a1 != 1:
        pol_temp = (pol1 / a1).simplifie()
        pol_temp.var = var
        factorisation.append("%s \\times\\big[ %s \\big]" % (TeX(a1), pol_temp))
        facteur2 = "%s\\times \\big[" % (TeX(a1))
    else:
        facteur2 = ""
    if c != 1:
        facteur2 += u"(%s %s)^2" % (TeX(c), var)
    else:
        facteur2 += u"%s^2" % var
    if sgns:
        if sgns == -2:  # -2 => (a-b)²
            facteur2 += "-2 \\times "
        else:  # +2 => (a+b)²
            facteur2 += "+2 \\times "
        if c == 1:
            facteur2 += var
        else:
            facteur2 += TeX(c) + var
        b = int(sqrt(pol2[0]))
        facteur2 += " \\times %s +" % (TeX(b))
    else:
        # a²-b²
        facteur2 += "-"
        b = int(sqrt(-(pol2[0])))
    facteur2 += u"%s^2" % (TeX(b))
    if a1 != 1:
        facteur2 += "\\big]"
    factorisation.append(facteur2)
    facteur3 = ""
    if a1 != 1:
        facteur3 += TeX(a1)
    sgns = sgns / 2
    if sgns:  # (cx-b)² ou (cx+b)²
        liste_racines = [Fraction(-(sgns)) * b / c]
        facteur3 += "{(%s)}^2" % (c * X + sgns * b)
    else:  # (cx-b)(cx+b)
        liste_racines = [Fraction(-1) * b / c, Fraction(1) * b / c]
        facteur3 += "(%s)(%s)" % (c * X + b, c * X - b)
    factorisation.append(facteur3)
    if racines:
        return factorisation, liste_racines
    return factorisation

def racines_degre2(P):
    """renvoie les racines d'un polynôme de degré 2"""
    from pyromaths.classes.Fractions import Fraction
    delta = int(P[1] ** 2 - 4 * P[2] * P[0])
    if delta == 0:
        x0 = eval(priorites('Fraction(-1, 2)*%r/%r' % (P[1], P[2]))[-1][0])
        if isinstance(x0, (Fraction, RacineDegre2)):
            liste_racines = [x0.simplifie()]
        else:
            liste_racines = [x0]
        liste_str_racines = ["\\dfrac{-%s}{2\\times %s}" % (pTeX(P[1]), pTeX(P[2]))]
        simplrac = [False]
    elif delta > 0:
        simplrac, strx1, x1, strx2, x2 = listeracines(P[2], P[1], delta, parentheses=False)
        liste_racines = [x1, x2]
        liste_str_racines = [strx1, strx2]
    else:
        simplrac = [False]
        liste_racines = liste_str_racines = []
    return delta, simplrac, liste_racines, liste_str_racines
    # delta
    # simplrac[0] est True si racine de Delta se simplifie, alors simplrac[1] est la racine de delta simplifiée
    # liste_racines donne la liste des racines sous la forme simplifiée, sous forme numérique si possible
    # liste_str_racine est la liste des racines au format TeX, non simplifié.

def listeracines(a, b, delta, parentheses=False):
    '''renvoie racsimple,simplifie,formule_x1,x_1,formule_x2,x2'''
    '''avec x_1<x_2
       si parenthese=True, renvoie deux booleens
          parenthesex1=True signifie qu'il faut mettre des parenthese autour de x1
       On suppose delta >0
       simplrac est True si racine de delta se simplifie'''
    a = int(a)
    b = int(b)
#     parenthesex1 = parenthesex2 = True  # par défaut
    # simplrac=True
    strx1 = "\\dfrac{-%s-\\sqrt{%s}}{2\\times %s}" % (pTeX(b), TeX(delta), pTeX(a))
    strx2 = "\\dfrac{-%s+\\sqrt{%s}}{2\\times %s}" % (pTeX(b), TeX(delta), pTeX(a))
    # #on a strx1<strx2
    coeff, radicande = simplifie_racine(delta)

    # x1,x2 simplifiés ont une écriture fractionnaire donc
    parenthesex1 = parenthesex2 = False
    if coeff == 1:  # delta n'a pas de facteur carré, on ne peut rien simplifier
        rac_delta = radicalTeX(delta)
        simplrac = [False]
    else:
        if radicande == 1:
            rac_delta = TeX(coeff)
        else:
            rac_delta = TeX(coeff) + radicalTeX(radicande)
        simplrac = [True, rac_delta]
    x1 = RacineDegre2(-b, 2 * a, -1, delta)
    x2 = RacineDegre2(-b, 2 * a, 1, delta)
    if b == 0:
        parenthesex1 = (coeff * a > 0)
        parenthesex2 = (coeff * a < 0)
    if a < 0:
        strx1, strx2, x1, x2, parenthesex1, parenthesex2 = strx2, strx1, x2, x1, parenthesex2, parenthesex1
    if parentheses:
        return simplrac, strx1, x1, strx2, x2, parenthesex1, parenthesex2
    else:
        return simplrac, strx1, x1, strx2, x2
        # simplrac[0] est True si racine de Delta se simplifie, alors simplrac[1] est la racine de delta simplifiée

def factorisation_degre2(P, factorisation=True):
    # x1=x2=0
    from pyromaths.classes.Fractions import Fraction

    var = P.var
    X = Polynome({1:1}, var)
    delta = int(eval(priorites('%r**2-4*%r*%r' % (P[1], P[2], P[0]))[-1][0]))
    if delta < 0:
        factorisation = []
        str_racines = []
        racines = []
        simplrac = [False]
    elif delta == 0:
        x0 = eval(priorites('Fraction(-1, 2)*%r/%r' % (P[1], P[2]))[-1][0])
        simplrac = [False]
        if isinstance(x0, (Fraction, RacineDegre2)):
            racines = [x0.simplifie()]
        else:
            racines = [x0]
        str_racines = ["\\dfrac{-%s}{2\\times %s}" % (pTeX(P[1]), pTeX(P[2]))]


        P0 = "%s-%s" % (var, pTeX(racines[0]))
        factorisation = [[P0, P0]]  # non simplifiée

        if 0 > racines[0]:
            P0 = X - racines[0]
            factorisation.append([P0, P0])
    else:  # delta>0
        simplrac, strx1, x1, strx2, x2 = listeracines(P[2], P[1], delta)
        if isinstance(x1, RacineDegre2):
            x1 = x1.simplifie()
            x2 = x2.simplifie()
        racines = [x1, x2]
        str_racines = [strx1, strx2]
        P1 = "%s-%s" % (var, pTeX(x1))
        P2 = "%s-%s" % (var, pTeX(x2))
        factorisation = [[P1, P2]]  # non simplifiée
        # Peut-on simplifier les parenthèses ?
        if x1.radicande == 0 and (x1.numerateur < 0 or x2.numerateur < 0):
            P1 = (X - x1)(var)
            P2 = (X - x2)(var)
            factorisation.append([P1, P2])
    return delta, simplrac, racines, str_racines, factorisation


def factorisation_degre3(E, nomE, exo=[], cor=[], racines=[0, 1, -1, 2, -2]):
    '''Factorise un polynôme de degré 3 avec une racine évidente'''
    var = E.var
    X = Polynome({1:1}, var)
    exo.append(_("\\item Soit $%s =%s $") % (nomE, E))
    cor.append(_("\\item Soit $%s=%s $)") % (nomE, E))
    exo.append("\\begin{enumerate}")
    cor.append("\\begin{enumerate}")
    for x0 in racines:
        if E(x0) == 0:
            break
    if x0 in [-2, -1, 0, 1, 2]:
        exo.append(_(u"\\item Vérifier si $%s $ possède une racine évidente.") % (nomE))
    else:
        exo.append(_(u"\\item Vérifier que $%s$ est une racine de $%s$.") % (TeX(x0), nomE))
    exo.append(_("\\item Factoriser $%s $.") % (nomE))
    cor.append("\\item ")

    if x0 == 0:
        degre_facteur = min(E.puiss)
        # degre_facteur=1
        E2 = (E / (X ** degre_facteur))[0]
        if degre_facteur == 1:
            cor.append(_("On remarque que $%s$ peut se factoriser par $%s$ et $%s=%s\\left(%s\\right)$") % (nomE, var, nomE, var, E2))
        elif degre_facteur == 2:
            cor.append(_(u"On remarque que $%s$ peut se factoriser par $%s^2$ et $%s=%s^2\\left(%s\\right)$")\
            % (nomE, E.var, nomE, E.var, E2))
            exo.append("\\end{enumerate}")
            cor.append("\\end{enumerate}")
            return exo, cor
    else:
        cor.append(_("Comme $%s(%s)=0$, on peut diviser $%s$ par $%s$") % (nomE, TeX(x0), nomE, X - x0))
        cor.append(TeX_division(E, (X - x0)) + "")
        E2, reste = E / (X - x0)
    cor.append(_("\\item On doit maintenant factoriser le polynome $%s_2=%s$\\\\") % (nomE, E2))
    delta, simplrac, racines, str_racines, factorisation = factorisation_degre2(E2, factorisation=True)
    cor = redaction_factorisation(E2, nomP=nomE + "_2", exo=[], cor=cor)[1]
    cor.append("\\par")
    cor.append(_("On en conclue donc que $%s=") % (nomE))
#     final = 0
    if x0 == 0:
        P0 = E.var
    else:
        P0 = "\\left(%s\\right)" % (X - x0)
    if E[3] == -1:
        cor.append("-")
    elif E[3] != 1:
        cor.append(TeX(E[3]))
    if delta < 0:
        # P1 = factorisation[-1][0]
        E_factorise = "%s\\times%s$" % (P0, E2)
    elif delta == 0:
        P1 = factorisation[-1][0]
        E_factorise = "%s\\times{\\left(%s\\right)}^2$" % (P0, P1)
    else:
        P1 = factorisation[-1][0]
        P2 = factorisation[-1][1]
        E_factorise = "%s\\left(%s\\right)\\left(%s\\right)$" % (P0, P1, P2)
    cor.append(E_factorise)

    exo.append("\\end{enumerate}")
    cor.append("\\end{enumerate}")
    return exo, cor


#----------------- redaction ---------------------------------------------------------

def redaction_factorisation(P, nomP="P", exo=[], cor=[]):
    var = P.var
    delta, simpl_delta, racines, str_racines, factorisation = factorisation_degre2(P)
    redaction_racines(P, nomP, var, cor)

    # factorisation
    if delta < 0:
        cor.append(_(u"On ne peut pas factoriser $%s(%s)$.") % (nomP, var))
    elif delta == 0:
        cor.append(_(u"On peut donc écrire "))
        ligne_factorisation = "$$%s(%s)" % (nomP, var)
        for etape in factorisation:
            ligne_factorisation += " = "
            if P[2] != 1:
                ligne_factorisation += "%s \\times " % (TeX(P[2]))

            ligne_factorisation += "{\\left(%s\\right)}^2" % (etape[0])
        ligne_factorisation += "$$"
        cor.append(ligne_factorisation)
    else:
        cor.append(_(u"On peut donc écrire "))
        ligne_factorisation = "$$%s(%s)" % (nomP, var)
        for etape in factorisation:
            ligne_factorisation += " = "
            if P[2] != 1:
                ligne_factorisation += "%s \\times " % (TeX(P[2]))
            if len(etape) == 1:
                ligne_factorisation += etape[0]
            else:
                ligne_factorisation += "\\left(%s\\right)\left(%s\\right)" % (etape[0], etape[1])
        ligne_factorisation += "$$"
        cor.append(ligne_factorisation)
    return exo, cor

def redaction_racines(P, nomP, var, cor=[]):
    delta, simpl_delta, liste_racines, liste_str_racines = racines_degre2(P)
    ligne_delta = _(u"Je calcule $\\Delta=%s^2-4\\times %s\\times %s=%s$") % (pTeX(P[1]), pTeX(P[2]), pTeX(P[0]), TeX(delta))
    if simpl_delta[0]:
        ligne_delta += _(" et $%s=%s$.\\par") % (radicalTeX(delta), simpl_delta[1])
    else:
        ligne_delta += ".\\par"
    cor.append(ligne_delta)
    if delta < 0:
        cor.append(_("Comme $\\Delta <0$, $%s(%s)$ n'a pas de racines.") % (nomP, var))
    elif delta == 0:
        cor.append(_("Comme $\\Delta=0$, $%s(%s)$ a une seule racine $%s_0=%s=%s$.\\par") % (nomP, var, var, liste_str_racines[0], TeX(liste_racines[0])))
    else:  # delta>0
        [x1, x2] = liste_racines
        cor.append(_("Comme $\\Delta>0$, $%s(%s)$ a deux racines :") % (nomP, var))
        if isinstance(x1, RacineDegre2):
#             simplification1 = simplification2 = ""
            x1, detail1 = x1.simplifie(True)
            x2, detail2 = x2.simplifie(True)
            max_len = max(len(detail1), len(detail2))
            cor.append("\\begin{align*}")
            cor.append("%s &= %s  &%s &= %s" % \
                       (liste_str_racines[0], liste_racines[0], liste_str_racines[1], liste_racines[1]))
            cor.append("\\\\")
            for i in range(0, max_len):
                if i < len(detail1):
                    cor.append("&= %s&" % (detail1[i]))
                else:
                    cor.append("&&")
                if i < len(detail2):
                    cor.append("&= %s" % (detail2[i]))
                else:
                    cor.append("& ")
                cor.append("\\\\")
            cor.pop(-1)
            cor.append("\\end{align*}")
            cor.append(_("Les racines de $%s$ sont $%s_1=%s$ et $%s_2=%s$.\\par") % (nomP, var, x1, var, x2))
        else:
            [strx1, strx2] = liste_str_racines
            cor.append(_("Les racines de $%s$ sont $%s_1=%s=%s$ et $%s_2=%s=%s$.") % (nomP, var, strx1, x1, var, strx2, x2))

    return cor
