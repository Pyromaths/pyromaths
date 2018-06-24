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
from __future__ import division
from __future__ import unicode_literals
from builtins import str
from builtins import range
from random import randrange

def genere_points(xmin, xmax, ymin, ymax, simple=False):

    if simple:  # génère 3 intervalles de variations /\/ ou \/\
        if randrange(1):
            variation = [0, 1, 0]
        else:
            variation = [1, 0, 1]
        longueur = xmax - xmin
        hauteur = ymax - ymin
        x_variation = [xmin]
        x_variation.append(x_variation[0] + randrange(int(0.25 * longueur), int(0.4 * longueur)))
        x_variation.append(x_variation[1] + randrange(int(0.25 * longueur), int(0.4 * longueur)))
        x_variation.append(xmax)
        liste_points = [(x_variation[0], randrange(ymin + (1 - variation[0]) * int(0.4 * hauteur), ymax - variation[0] * int(0.4 * hauteur)))]
        for i in [1, 2, 3]:
            if variation[i - 1]:
                liste_points.append((x_variation[i], randrange(liste_points[i - 1][1], ymax)))
            else:
                liste_points.append((x_variation[i], randrange(ymin, liste_points[i - 1][1])))
    else:
        liste_points = [(xmin, 0)]
        for i in range(10):
            liste_points.append((liste_points[i][0] + randrange(2, 5), randrange(ymin, ymax)))
    return liste_points

def bezier(simple=False, xmin=-15, xmax=15, ymin=-12, ymax=12):
    liste_points = genere_points(simple=simple, xmin=xmin, xmax=xmax, ymin=ymin, ymax=ymax)
    variation = []
    largeur = liste_points[-1][0] - liste_points[0][0]
    points = [liste_points[0]]
    for i in range(1, len(liste_points)):
        if liste_points[i - 1][1] < liste_points[i][1]:
            points.append(liste_points[i])
        elif liste_points[i - 1][1] > liste_points[i][1]:
            points.append(liste_points[i])
    deltaxx = 0.3 * (points[1][0] - points[0][0])
    nderiv = (points[1][1] - points[0][1]) / (points[1][0] - points[0][0])
    apres = [(points[0][0] + 0.5, points[0][1] + deltaxx * nderiv)]
    avant = []
    if points[0][1] < points[1][1]:
        variation += '+'
    else:
        variation += '-'
    x_variation = [points[0][0]]
    y_variation = [points[0][1]]

    for i in range(1, len(points) - 1):
        if (points[i][1] <= points[i - 1][1] and points[i][1] <= points[i + 1][1]):
            nderiv = 0
            x_variation.append(points[i][0])
            y_variation.append(points[i][1])
            variation += '+'
        elif (points[i][1] >= points[i - 1][1] and points[i][1] >= points[i + 1][1]):
            nderiv = 0
            x_variation.append(points[i][0])
            y_variation.append(points[i][1])
            variation += '-'
        else:
            nderiv = (points[i - 1][1] - points[i + 1][1]) / (points[i - 1][0] - points[i + 1][0])
        deltax = 0.3 * (points[i - 1][0] - points[i][0])
        deltaxx = 0.3 * (points[i + 1][0] - points[i][0])
        avant.append((points[i][0] + deltax, points[i][1] + deltax * nderiv))
        apres.append((points[i][0] + deltaxx, points[i][1] + deltaxx * nderiv))
    avant.append((points[len(points) - 1][0] - 0.5, points[len(points) - 1][1] - 0))
    string = str(points[0])
    for i in range(len(points) - 1):
        string += str(apres[i]) + str(avant[i]) + str(points[i + 1])
    textbezier = "\\input{tabvar}\n\
                \psset{unit=" + str(14 / largeur) + "cm}\n\
                \\begin{pspicture}"
    textbezier += "(" + str(xmin) + "," + str(ymin) + ")(" + str(liste_points[-1][0]) + "," + str(ymax) + ")\n"
    textbezier += "\psgrid[subgriddiv=0,griddots=10,gridlabels=0pt]\n\
                \psaxes[linewidth=1pt,%\n\
                ticks=none,%\n\
                %labels=none\n\
                Dx=2\n\
                ]{->}(0,0)"
    textbezier += "(" + str(xmin) + "," + str(ymin) + ")(" + str(liste_points[-1][0]) + "," + str(ymax) + ")\n"
    impression = textbezier + "\psbezier" + string + "\n" + "\\end{pspicture}\n\\vspace{2cm}\n\n"
    impression += "\\begin{tikzpicture}\n\\tkzTabInit[espcl=1]\n{$x$ / .5,$f'\\,(x)$ / .5}\n"
    impression += "{$" + "$,$".join([str(i) for i in x_variation]) + "$}\n"
    impression += "\\tkzTabLine{," + ",".join(y_variation) + "}\n\end{tikzpicture}\n"
#===============================================================================
# {$x$ / 1,$g(x)$ / 1}%
# {$0$,$1$,$2$}%
# \tkzTabLine{d,+,0,-,d}
# \end{tikzpicture}"
#===============================================================================
    impression += "$$\n\
                \\tabvar{%\n\
                \\tx{x}&\\tx{" + str(x_variation[0]) + "}"
    for i in range(1, len(x_variation)):
        impression += "&& \\tx{" + str(x_variation[i]) + "}"
    impression += "&& \\tx{" + str(points[-1][0]) + "}\\cr\n"
    impression += "\\tx{f(x)}"
    for i in range(len(variation)):
        if variation[i] == '+':
            impression += "&\\txb{" + str(y_variation[i]) + "}&\\fm"
        else:
            impression += "&\\txh{" + str(y_variation[i]) + "}&\\fd"
    if variation[-1] == '+':
        impression += "&\\txh{" + str(points[-1][1]) + "}"
    else:
        impression += "&\\txb{" + str(points[-1][1]) + "}"
    return impression + "\\cr\n}$$\n\n"


def tab_var(fonc, Intervalle=["-\\infty", "+\\infty"]):
    from pyromaths.classes.Polynome import Polynome
    if isinstance(fonc, Polynome):
        return tab_var_poly(fonc, Intervalle[0], Intervalle[1])
    else:
        return _("Je ne sais pas étudier les variations de cette fonction.")

def tab_var_poly(P, borneinf="-\\infty" , bornesup=u"+\\infty"):
    Intervalle = [borneinf, bornesup]
    # print"borneinf=",borneinf
    tab_var = "\\input{tabvar}\n"
    tab_var += "$$\\tabvar{%\n"
    if P.deg == 0:
        tab_var += tabvar_x(Intervalle, P.var)
        Cste = str(P(0))
        tab_var += "\\tx{f(" + P.var + ")}&\\tx{" + Cste + "}&\\fhm&\\tx{" + Cste + "}\\cr\n"
        return tab_var + "}$$\n"
    elif P.deg == 1:
        tab_var += tabvar_x(Intervalle, P.var)
        if P.dictio[1] > 0:
            tab_var += "\\tx{f(" + P.var + ")}& &\\fm& \\cr\n"
        else:
            tab_var += "\\tx{f(" + P.var + ")}& &\\fd&\\cr\n"
        return tab_var + "}$$\n"
    elif P.deg == 2:
        alpha = -P.dictio[1] //  (2 * P.dictio[2])
        extremum = P(alpha)
        if (borneinf == "-\\infty" or Intervalle[0] < alpha) and\
           (Intervalle[1] == "+\\infty" or Intervalle[1] > alpha):
            listex = [Intervalle[0], alpha, Intervalle[1]]
            if P.dictio[0] > 0:
                tab_var_y = "\\tx{f(" + P.var + ")}& &\\fd&\\txb{" + nombre_TeX(extremum) + "}&\\fm&\\cr\n"
            else:
                tab_var_y = "\\tx{f(" + P.var + ")}& &\\fm&\\txh{" + nombre_TeX(extremum) + "}&\\fd&\\cr\n"
        else:
            listex = Intervalle
            if P.dictio > 0:
                if not(borneinf == "-\\infty") and Intervalle[0] > alpha:
                    tab_var_y = "\\tx{f(" + P.var + ")}& &\\fm& \\cr\n"
                else:
                    tab_var_y = "\\tx{f(" + P.var + ")}& &\\fd&\\cr\n"
            else:
                if not(borneinf == "-\\infty") and Intervalle[0] > alpha:
                    tab_var_y = "\\tx{f(" + P.var + ")}& &\\fd&\\cr\n"
                else:
                    tab_var_y = "\\tx{f(" + P.var + ")}& &\\fm& \\cr\n"
        tab_var += tabvar_x(listex, P.var)
        tab_var += tab_var_y
        return tab_var + "}$$\n"
    elif P.deg == 3:
        return _(u"attends un peu pour le degré 3")
        # #Les fonctions développées pour les équations du second degré doivent aider
    else:
        return _(u"Degré trop élevé")
            # #Cas particulier où P' a une racine évidente, ou polynome bicarré


def tabvar_x(listex, var):
    '''imprime la premiere ligne du tabvar'''
    var_x = "\\tx{" + var + "}&\\tx{" + nombre_TeX(listex[0]) + "}"
    for i in range(1, len(listex)):
        var_x += "&&\\tx{" + nombre_TeX(listex[i]) + "}"
    return var_x + "\\cr\n"

def nombre_TeX(nombre):  # A remplacer par sepmillier
    from pyromaths.classes.Fractions import Fraction
    if type(nombre) in [type(int), type(float)]:
        return str(nombre)
    elif isinstance(nombre, Fraction):
        if nombre.denominateur == 1:
            return nombre_TeX(nombre.numerateur)
        else:
            return "\\dfrac{" + str(nombre.numerateur) + "}{" + str(nombre.denominateur) + "}"
    else:
        return str(nombre)
