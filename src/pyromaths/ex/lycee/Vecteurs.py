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


# #- additions / soustractions de vecteurs ( difficulté : ne pas sortir du cadre )
# #- multiplication d'un vecteur par un réel +  add + sous ( difficulté : ne pas sortir du cadre )
# #- lire les coordonnées d'un vecteur
# #- placer un point B connaissant A et les coordonnées de vec{AB} : avec coordonnées ou i et j ( difficulté : ne pas sortir du cadre )
# #- calcul de norme
# #- simplifier des sommes
# #- problèmes de colinéarité

from __future__ import division
from __future__ import unicode_literals
from builtins import str
from pyromaths.classes.Vecteurs import randvect, Vecteur
from pyromaths.classes.Racine import simplifie_racine
import math
from random import randint, shuffle

def dist_bords(a, b):
    '''Calcule les distances minimales d'un point de coordonnées (a,b) aux bords du cadre, selon l'axe x et y.'''
    x = min(a, 18 - a)  # la largeur vaut 18
    y = min(b, 10 - b)  # la hauteur vaut 10
    return (x, y)

def pair(n):
    '''Retourne le plus petit entier pair strictement plus grand que n'''
    if (n % 2 == 0):
        return n + 2
    else:
        return n + 1

def AffNom(u, crd=0):
    '''Renvoie les coordonnées pour l'affichage du nom du vecteur u.'''
    if u.x == 0 and math.fabs(u.y) > 2:
        coord = (0, u.y // 2)
    elif u.x == 0:
        coord = (-0.5, u.y // 2)
    elif u.y == 0 and math.fabs(u.x) > 2:
        coord = (u.x // 2, 0)
    elif u.y == 0:
        coord = (u.x // 2, -0.5)
    elif math.fabs(u.x) + math.fabs(u.y) < 3:
        coord = (u.x / 2 + 0.5, u.y / 2 + 0.5)
    else:
        coord = (u.x // 2, u.y // 2)
    return str(coord[0]) + "," + str(coord[1])

def ChoixVecteur(u, v, w, x, y):
    listecoeff = [0.5, -0.5, -1, -2, 2, 3, -3]
    listevect = [(u, "u"), (v, "v"), (w, "w")]
    shuffle(listecoeff)
    shuffle(listevect)
    for vec in listevect:
        for coeff in listecoeff:
            if (0 <= x + coeff * vec[0].x <= 18) and (0 <= y + coeff * vec[0].y <= 10):
                return (coeff, coeff * vec[0], vec[1])



def repr_somme(u, v, u1, u2, cor, larg=0):
    '''Représente la somme des vecteurs u + v.'''

    a = u + v

    if (u.x * a.x >= 0):
        largeur = max(math.fabs(u.x), math.fabs(a.x))
        if (a.x > 0):
            departx = 0
        elif (a.x == 0):
            departx = -u.x / 2 + math.fabs(u.x) / 2
        else:
            departx = max(math.fabs(u.x), math.fabs(a.x))
    else:
        largeur = math.fabs(u.x) + math.fabs(a.x)
        if (u.x >= 0):
            departx = -a.x
        else:
            departx = -u.x
    if (u.y * a.y >= 0):
        hauteur = max(math.fabs(u.y), math.fabs(a.y))
        if (a.y > 0):
            departy = 0
        elif (a.y == 0):
            departy = -u.y / 2 + math.fabs(u.y) / 2
        else:
            departy = max(math.fabs(u.y), math.fabs(a.y))
    else:
        hauteur = math.fabs(u.y) + math.fabs(a.y)
        if (u.y >= 0):
            departy = -a.y
        else:
            departy = -u.y

    if int(larg) + largeur > 18:
        cor.append("\\par")  # Figure trop large avec la précédente, il faut passer à une nouvelle ligne.

    depart = "(" + str(departx) + "," + str(departy) + ")"
    largeur = str(pair(int(largeur)))
    hauteur = str(pair(int(hauteur)))

    cor.append(u"\\begin{pspicture*}(0,0)(" + largeur + "," + hauteur + ")")
    cor.append(u"\\psgrid[subgriddiv=2, gridlabels=0pt]")
    cor.append(u"\\psset{unit=10mm,arrowscale=2}")

    cor.append(u"\\rput" + depart + "{")
    cor.append(u"\\psline[linewidth=1pt, linecolor=DarkGreen]{|->}(0, 0)(" + str(u.x) + ", " + str(u.y) + ")")  # # Premier Vecteur
    cor.append(u"\\rput(" + AffNom(u) + ") \
          {\\psframebox[linecolor=white, fillcolor=white, fillstyle=solid]{\\textcolor{DarkGreen}{$\\overrightarrow{" + u1 + "}$}}}")

    cor.append(u"\\psline[linewidth=1pt, linecolor=DarkBlue]{|->}(" + str(u.x) + ", " + str(u.y) + ")(" + str(a.x) + ", " + str(a.y) + ")")  # # 2e Vecteur
    k = Vecteur(u.x + a.x, u.y + a.y)
    cor.append(u"\\rput(" + AffNom(k) + ") \
          {\psframebox[linecolor=white, fillcolor=white, fillstyle=solid]{\\textcolor{DarkBlue}{$\\overrightarrow{" + u2 + "}$}}}")
    if len(u2) > 1:
        sgn = "-"
    else:
        sgn = "+"
    cor.append(u"\\psline[linestyle=dashed, linewidth=1pt, linecolor=DarkRed]{|->}(0, 0)(" + str(a.x) + ", " + str(a.y) + ")")  # # Résultat de l'opération
    cor.append(u"\\rput(" + AffNom(a) + ") \
          {\psframebox[linecolor=white, fillcolor=white, fillstyle=solid]{\\textcolor{DarkRed}{$\\overrightarrow{" + u1 + "}" + sgn + "\\overrightarrow{" + u2[-1] + "}$}}}")

    cor.append(u"}")
    cor.append(u"\\end{pspicture*}")
    return largeur  # # récupérer la largeur pour éviter d'aligner des figures trop larges sur la feuille

def vecteurs_add():
    '''Exercice sur la définition des vecteurs et leurs sommes.'''
    t = None
    while not t:
    # Pour être sûr que l'exercice ait des solutions
        (u, posux, posuy) = randvect(0, 10)
        (v, posvx, posvy) = randvect(math.fabs(u.x) + 1, 10)
        (w, poswx, poswy) = randvect(math.fabs(v.x) + math.fabs(u.x) + 2, 10)

        # # Construction du point pour la question 2
        if 18 - poswx - max(w.x, 0) > 0:
            restes = (18 - poswx - max(w.x, 0), 10)
            pointy = randint(0, 10)
        elif poswy + min(w.y, 0) > 10 - poswy - max(w.y, 0):
            restes = (poswx + min(w.x, 0), poswy + min(w.y, 0))
            pointy = randint(0, restes[1])
        else:
            restes = (poswx + min(w.x, 0), 10 - poswy - max(w.y, 0))
            pointy = randint(10 - restes[1], 10)

        pointx = randint(18 - restes[0], 18)

        t = ChoixVecteur(u, v, w, pointx, pointy)

    exo = ["\\exercice"]
    cor = ["\\exercice*"]

    exo.append(u"\\begin{pspicture*}(0,0)(18,10)")
    exo.append(u"\\psgrid[subgriddiv=2, gridlabels=0pt]")
    exo.append(u"\\psset{unit=10mm,arrowscale=2}")

    cor.append(u"\\begin{pspicture*}(0,0)(18,10)")
    cor.append(u"\\psgrid[subgriddiv=2, gridlabels=0pt]")
    cor.append(u"\\psset{unit=10mm,arrowscale=2}")

    exo.append(u"\\psdot(" + str(pointx) + "," + str(pointy) + ")")

    if pointx < 18 and pointy < 10:
        nompoint = str(pointx + 0.5) + "," + str(pointy + 0.5)
    else:
        nompoint = str(pointx - 0.5) + "," + str(pointy - 0.5)

    exo.append(u"\\rput(" + nompoint + "){\\psframebox[linecolor=white, fillcolor=white, fillstyle=solid]{$A$}}")

    cor.append(u"\\psdot(" + str(pointx) + "," + str(pointy) + ")")
    cor.append(u"\\rput(" + nompoint + "){\\psframebox[linecolor=white, fillcolor=white, fillstyle=solid]{$A$}}")

    cor.append(u"\psline[linecolor=DarkBlue]{|->}(" + str(pointx) + "," + str(pointy) + ")(" + str(pointx + t[1].x) + ", " + str(pointy + t[1].y) + ")")

    bx = pointx + t[1].x
    by = pointy + t[1].y

    if bx < 18 and by < 10:
        nompoint = str(bx + 0.5) + "," + str(by + 0.5)
    else:
        nompoint = str(bx - 0.5) + "," + str(by - 0.5)

    cor.append(u"\\psdot(" + str(pointx + t[1].x) + "," + str(pointy + t[1].y) + ")")
    cor.append(u"\\rput(" + nompoint + "){\\psframebox[linecolor=white, fillcolor=white, fillstyle=solid]{$B$}}")

    for vec in [(u, posux, posuy, "u"), (v, posvx, posvy, "v"), (w, poswx, poswy, "w")]:
        exo.append(u"\\rput(" + str(vec[1]) + "," + str(vec[2]) + "){")
        exo.append(u"\psline{|->}(0, 0)(" + str(vec[0].x) + ", " + str(vec[0].y) + ")")

        exo.append(u"\\rput(" + AffNom(vec[0]) + ") \
                     {\\psframebox[linecolor=white, fillcolor=white, fillstyle=solid]{$\\overrightarrow{" + vec[3] + "}$}}")
        exo.append(u"}")
    exo.append(u"\\end{pspicture*}")


    for vec in [(u, posux, posuy, "u"), (v, posvx, posvy, "v"), (w, poswx, poswy, "w")]:
        if vec[0].y > 0:
            plus = 1
        else:
            plus = 0
        cor.append(u"\\rput(" + str(vec[1]) + "," + str(vec[2]) + "){")
        cor.append(u"\\psline{|->}(0, 0)(" + str(vec[0].x) + ", " + str(vec[0].y) + ")")
        cor.append(u"\\psline[linestyle=dashed,linecolor=DarkRed](0, 0)(" + str(vec[0].x) + ", 0)(" + str(vec[0].x) + "," + str(vec[0].y) + ")")
        cor.append(u"\\rput(" + AffNom(vec[0]) + "){\\psframebox[linecolor=white, fillcolor=white, \
                     fillstyle=solid]{$\\overrightarrow{" + vec[3] + "}\\ (" + str(vec[0].x) + ";" + str(vec[0].y) + ")$}}")
        cor.append(u"}")
    cor.append(u"\\end{pspicture*}")

    exo.append("\\par")
    cor.append("\\par")
    exo.append(_(u"On se place dans un repère orthonormé et on considère les vecteurs $\\overrightarrow{u}$, $\\overrightarrow{v}$, et $\\overrightarrow{w}$ ci-dessous."))
    cor.append(_(u"On se place dans un repère orthonormé et on considère les vecteurs $\\overrightarrow{u}$, $\\overrightarrow{v}$, et $\\overrightarrow{w}$ ci-dessous."))

    exo.append("\\begin{enumerate}")
    cor.append("\\begin{enumerate}")

    exo.append(_(u"\\item Lire les coordonnées de chacun des vecteurs $\\overrightarrow{u}$, $\\overrightarrow{v}$, et $\\overrightarrow{w}$."))
    cor.append(_(u"\\item Lire les coordonnées de chacun des vecteurs $\\overrightarrow{u}$, $\\overrightarrow{v}$, et $\\overrightarrow{w}$."))

    cor.append("\\par")
    cor.append(_(u"Un petit rappel : l'abscisse d'un vecteur est la différence d'abscisse entre le fin et le début du vecteur. \
                 Concernant le vecteur $\\overrightarrow{u}$, son abscisse est $" + str(u.x) + u"$. \
                 On lit également son ordonnée : $") + str(u.x) + _(u"$. \
                 Donc les coordonnées de $\\overrightarrow{u}$ sont $(") + str(u.x) + ", " + str(u.y) + _(u" )$. \
                 Des pointillés ont été ajoutés sur la figure pour faciliter la lecture des coordonnées."))
    cor.append(_(u"De même, les coordonnées de $\\overrightarrow{v}$ sont $(") + str(v.x) + ", " + str(v.y) + _(u" )$ \
                 et les coordonnées de $\\overrightarrow{w}$ sont $(") + str(w.x) + ", " + str(w.y) + " )$.")

    exo.append(_(u"\\item Placer un point B de sorte que le vecteur $\\overrightarrow{AB}$ soit égal à $") + str(t[0]) + " \\times \\overrightarrow{" + t[2] + "}$.")
    cor.append(_(u"\\item Placer un point B de sorte que le vecteur $\\overrightarrow{AB}$ soit égal à $") + str(t[0]) + " \\times \\overrightarrow{" + t[2] + "}$.")

    cor.append(u"\\par")
    cor.append(_(u"Le plus simple pour répondre à cette question est de calculer les coordonnées du vecteur $") + str(t[0]) + " \\times \\overrightarrow{" + str(t[2]) + "}$.")
    cor.append(_(u"Cela se fait en multipliant les coordonnées de $\\overrightarrow{") + str(t[2]) + "}$ par $" + str(t[0]) + _(u"$, ce qui donne comme résultat $(") + str(t[1].x) + ";" + str(t[1].y) + ")$.")
    cor.append(_(u"En partant du point A et en respectant ces coordonnées, on dessine un vecteur (en bleu sur la figure ci-dessus) qui indique l'emplacement du point B."))

    exo.append(_(u"\\item Calculer les normes de chacun des vecteurs $\\overrightarrow{u}$, $\\overrightarrow{v}$, et $\\overrightarrow{w}$."))
    cor.append(_(u"\\item Calculer les normes de chacun des vecteurs $\\overrightarrow{u}$, $\\overrightarrow{v}$, et $\\overrightarrow{w}$."))

    if u.x ** 2 + u.y ** 2 == simplifie_racine(u.x ** 2 + u.y ** 2)[1]:  # Cas où la simplification est la même, donc inutile d'écrire deux fois la même chose.
        Norm_u = "$"
    else:
        Norm_u = "=" + str(u.normeTex()) + "$"

    if v.x ** 2 + v.y ** 2 == simplifie_racine(v.x ** 2 + v.y ** 2)[1]:
        Norm_v = "$"
    else:
        Norm_v = "=" + str(v.normeTex()) + "$"

    if w.x ** 2 + w.y ** 2 == simplifie_racine(w.x ** 2 + w.y ** 2)[1]:
        Norm_w = "$"
    else:
        Norm_w = "=" + str(w.normeTex()) + "$"

    cor.append("\\par")
    cor.append(u"$\|\\overrightarrow{u}\|=\\sqrt{(" + str(u.x) + ")^2+(" + str(u.y) + ")^2}=\\sqrt{" + str(u.x ** 2) + " + " + str(u.y ** 2) + "}= \
                 \\sqrt{" + str(u.x ** 2 + u.y ** 2) + "}" + Norm_u + ".\\par")
    cor.append(_(u"De la même manière, on obtient :"))

    cor.append(u"$\|\\overrightarrow{v}\|=\\sqrt{(" + str(v.x) + ")^2+(" + str(v.y) + ")^2}=\\sqrt{" + str(v.x ** 2) + " + " + str(v.y ** 2) + "}= \
                 \\sqrt{" + str(v.x ** 2 + v.y ** 2) + "}" + Norm_v + " et \\par")
    cor.append(u"$\|\\overrightarrow{w}\|=\\sqrt{(" + str(w.x) + ")^2+(" + str(w.y) + ")^2}=\\sqrt{" + str(w.x ** 2) + " + " + str(w.y ** 2) + "}= \
                 \\sqrt{" + str(w.x ** 2 + w.y ** 2) + "}" + Norm_w + ".\\par")

    exo.append(_(u"\\item Dessiner des représentants des vecteurs $\\overrightarrow{u}+\\overrightarrow{v}$, $\\overrightarrow{u}-\\overrightarrow{v}$, $\\overrightarrow{u}-\\overrightarrow{w}$ \
                 et $\\overrightarrow{v}+\\overrightarrow{w}$."))
    cor.append(_(u"\\item Dessiner des représentants des vecteurs $\\overrightarrow{u}+\\overrightarrow{v}$, $\\overrightarrow{u}-\\overrightarrow{v}$, $\\overrightarrow{u}-\\overrightarrow{w}$ \
                 et $\\overrightarrow{v}+\\overrightarrow{w}$."))

    cor.append("\\par")
    cor.append(_(u"Pour dessiner les sommes ou différences de vecteurs, il faut les mettre \"bouts à bouts\", \
                 comme sur les figures qui suivent :\\par"))
    i = repr_somme(u, v, 'u', 'v', cor)
    repr_somme(u, -v, 'u', '-v', cor, i)
    cor.append("\\par")
    i = repr_somme(u, -w, 'u', '-w', cor)
    repr_somme(v, w, 'v', 'w', cor, i)

    exo.append("\\end{enumerate}")
    cor.append("\\end{enumerate}")

    return exo, cor

vecteurs_add.description = _(u"Vecteurs")
vecteurs_add.level = _(u"2.Seconde")
