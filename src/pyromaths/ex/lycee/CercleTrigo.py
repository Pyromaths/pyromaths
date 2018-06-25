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
from builtins import str
from builtins import range
import random
from math import cos, sin, radians, pi
# from pyromaths.outils.decimaux import decimaux
from pyromaths.outils.Arithmetique import pgcd
from pyromaths.ex import LegacyExercise

div180 = [[1,180],[2,90],[3,60],[4,45],[5,36],[6,30],[9,20],[10,18],[12,15]]

# Radians représentés en fait par des fractions

def deg2rad(n):
    """Effectue la conversion de degrés entre 0 et 360° vers radians."""
    p = pgcd(n,180)
    return [n // p,180 // p]

def simprad(liste):
    """Simplifie la fraction d'un angle en radians. Le paramètre est une liste d'entiers, pour représenter une fraction."""
    p = pgcd(liste[0],liste[1])
    return [f // p for f in liste]

def rad2deg(liste):
    """Effectue la conversion de radians entre 0 et 2pi vers degrés. Le paramètre est une liste d'entiers, pour représenter une fraction."""
    return liste[0]*180/liste[1] # Attention résultat entier, donc faux si liste[1] ne divise pas 180

def rad2tex(liste):
    """Prépare l'écriture de radians en latex."""
    if liste[0]==0:
        frac =  "$0$"
    elif liste[0]==liste[1]:
        frac = "$\\pi$"
    elif liste[0]==-liste[1]:
        frac = "$-\\pi$"
    elif liste[0]==1:
        frac = "$\\dfrac{\\pi}{"+str(liste[1])+"}$"
    elif liste[0]==-1:
        frac = "$\\dfrac{-\\pi}{"+str(liste[1])+"}$"
    elif liste[1]==-1: # Probablement inutile
        frac = "$"+str(-liste[0])+"\\pi$"
    elif liste[1]==1:
        frac = "$"+str(liste[0])+"\\pi$"
    else:
        frac = "$\\dfrac{"+str(liste[0])+"\\pi}{"+str(liste[1])+"}$"
    return frac

def mes_princ(liste):
    """Calcule la mesure principale d'un angle en radians ( entre -pi et pi )."""
    num = liste[0] % (2*liste[1])
    if num > liste[1]:
        num -= 2*liste[1]
    return simprad([num,liste[1]])

def mes_02pi(liste):
    """Calcule la mesure d'un angle en radians dans l'intervalle [0,2pi]."""
    num = liste[0] % (2*liste[1])
    return [num,liste[1]]

def cercle_trigo(code=0,*args):
    """Dessine le cercle trigonométrique avec un nombre indéfini d'angles en degrés ou radians, en codant ou non les angles."""
    figure = """\\psset{xunit=3cm,yunit=3cm,dotstyle=+}
    \\begin{pspicture}(-1.4,-1.4)(1.4,1.4)
    \\psframe(-1.4,-1.4)(1.4,1.4)
    \\psaxes[linewidth=0.5pt,Dx=2,Dy=2]{->}(0,0)(-1.1,-1.1)(1.1,1.1)
    \\pscircle[linecolor=gray](0,0){3}
    \\definecolor{grisclair}{gray}{0.20}
    \\colorlet{bleuclair}{blue!40!white}\n"""
    idx = 0
    if not code:
        for a in range(11):
            if (a+1) / 6 not in [0.5,1,1.5]:
                figure += "\\psline[linecolor=LightSkyBlue,linestyle=dashed](0,0)("+str(round(cos((a+1)*pi/6),2))+","+str(round(sin((a+1)*pi/6),2))+")\n"
        for a in range(9):
            if (a+1) / 5 not in [0.5,1,1.5]:
                figure += "\\psline[linecolor=LightSlateGray,linestyle=dashed](0,0)("+str(round(cos((a+1)*pi/5),2))+","+str(round(sin((a+1)*pi/5),2))+")\n"
        for a in range(4):
            figure += "\\psline[linecolor=LightGreen,linestyle=dashed](0,0)("+str(round(cos((2*a+1)*pi/4),2))+","+str(round(sin((2*a+1)*pi/4),2))+")\n"
    for f in args:
        if isinstance(f,list): # mesure en radians
            rad = simprad(f)
        else: # mesure en degrés
            rad = simprad(deg2rad(f))
        f = rad[0]*pi/rad[1] # Le dénominateur ne devrait pas être nul...
        frac = rad2tex(rad)

        figure += "\\psline[linecolor=red,linestyle=dashed](0,0)("+str(round(cos(f),2))+","+str(round(sin(f),2))+")\n"
        if code:
            figure += "\\rput("+str(round(1.25*cos(f),2))+","+str(round(1.25*sin(f),2))+"){"+frac+"}\n"
        else:
            figure += "\\rput("+str(round(1.25*cos(f),2))+","+str(round(1.25*sin(f),2))+"){$M_"+str(idx)+"$}\n"
            idx += 1
    figure += r"""\uput[dl](0,0){$O$}
    \uput[dr](1,0){$I$}
    \uput[ul](0,1){$J$}"""
    figure += "\n\\end{pspicture}"
    return figure

def findrad(itv=1, neg=0, denom_simple=1):
    """Génère un angle en radians sous certaines conditions :
    itv ( intervalle ): 0 ( quelconque ), 1 ( mesure principale ), 2 ( entre 0 et 2 pi )
    neg : 0 ( positif ), 1 ( négatif )
    denom_simple : 0 ( quelconque ), 1 ( simple, càd 1, 2, 3, 4, 5, ou 6 ), 2 ( diviseur de 180 )"""

    global div180

    if denom_simple==1:
        denom = random.randint(2,6)
    elif denom_simple == 0:
        denom = random.randint(2,30)
    else:
        random.shuffle(div180)
        random.shuffle(div180[0])
        denom = div180[0][0]

    if itv == 1:
        sgn = (-1)**(random.randint(1,2))
        num = sgn * random.randint(1,denom) # pas grave si -pi sort
    elif itv == 2:
        num = random.randint(1,2*denom)
    else:
        numliste = [random.randint(2*denom, 120),random.randint(-2*denom, -denom)]
        random.shuffle(numliste)
        num = numliste[0]

    if (neg and (num > 0)) or ((not neg) and (num < 0)):
        num = -num

    return [num,denom] # FIX Simplifier ?

def _cercle_trigonometrique():
    """Exercice de la fiche."""

    exo = ["\\exercice"]
    cor = ["\\exercice*"]

    mes_deg = [] # Question 1
    while len(mes_deg)<5:
        tmp = random.randint(0,360) # FIX trop complexes parfois
        if tmp not in mes_deg:
            mes_deg.append(tmp)
    mes_deg_tex = [_(u"$%s\\degres$") %(d) for d in mes_deg]

    radq2 = [] # Question 2
    while len(radq2)<5:
        tmp = findrad(2,0,2) # Dénominateur est un diviseur de 180
        if tmp not in radq2:
            radq2.append(tmp)

    radq3 = [] # Question 3
    while len(radq3)<5:
        while len(radq3)<4:
            tmp = findrad(0,0,0)
            if tmp not in radq3:
                radq3.append(tmp)
        tmp = findrad(0,1,0) # dernier négatif
        if tmp not in radq3:
            radq3.append(tmp)

    radq4 = [] # Question 4
    while len(radq4)<4:
        tmp = mes_princ(findrad(0,0,1))
        if tmp not in radq4:
            radq4.append(tmp)

    radq5 = [] # Question 5
    radq5_princ = []
    while len(radq5)<4:
        while len(radq5)<2:
            tmp = findrad(1,0,1)
            tmp_princ = mes_princ(tmp)
            if tmp_princ not in radq5_princ:
                radq5.append(tmp)
                radq5_princ.append(tmp_princ)
        while len(radq5)<3:
            tmp = findrad(1,1,1) # avant-dernier négatif
            tmp_princ = mes_princ(tmp)
            if tmp_princ not in radq5_princ:
                radq5.append(tmp)
                radq5_princ.append(tmp_princ)
        tmp = findrad(0,0,1) # dernier non principal
        tmp_princ = mes_princ(tmp)
        if tmp_princ not in radq5_princ:
            radq5.append(tmp)

    mes_rad = radq2 + radq3 + radq4 + radq5
    mes_rad_tex = [rad2tex(r)for r in mes_rad]

    mes_deg_en_rad = [deg2rad(d) for d in mes_deg]
    mes_deg_en_rad_tex = [rad2tex(r) for r in mes_deg_en_rad]

    exo.append(u"\\begin{enumerate}")
    exo.append(_(u"\\item Convertir les cinq mesures suivantes en radians : %s, %s, %s, %s et %s.") %(tuple(mes_deg_tex)))
    exo.append(_(u"\\item Convertir les cinq mesures suivantes en degrés : %s, %s, %s, %s et %s~rad.") %(tuple(mes_rad_tex[0:5])))
    exo.append(_(u"\\item Déterminer les mesures principales des angles suivants en radians : %s, %s, %s, %s et %s~rad.") %(tuple(mes_rad_tex[5:10])))
    exo.append(_(u"\\item Des angles ont été placés sur le cercle trigonométrique ci-dessous, représentés en rouge par les points $M_0$, $M_1$, $M_2$ et $M_3$. Lire leurs mesures principales en radians"))
    exo.append(_(u"( les lignes vertes, grises et bleues représentent des angles multiples de $\\dfrac{\\pi}{3}$, de $\\dfrac{\\pi}{4}$ et de $\\dfrac{\\pi}{5}$ ).\\par"))
    exo.append(cercle_trigo(0,radq4[0],radq4[1],radq4[2],radq4[3]))
    exo.append(_(u"\\item Placer les angles suivants sur le cercle trigonométrique : %s, %s, %s et %s~rad.\\par") %(tuple(mes_rad_tex[14:])))
    exo.append(cercle_trigo())
    exo.append(u"\\end{enumerate}\\par")

    cor.append(u"\\begin{enumerate}")
    cor.append(_(u"\\item Convertir les cinq mesures suivantes en radians : %s, %s, %s, %s et %s.\\par") %(tuple(mes_deg_tex)))

    cor.append(_(u"La conversion est en fait une simple règle de proportionnalité : il faut multiplier par $\\dfrac{\\pi}{180}$.\\par"))
    cor.append(_(u"Par exemple pour la première mesure, on obtient avec simplification : $"+str(mes_deg[0])+"\\times\\dfrac{\\pi}{180}$ = ")+mes_deg_en_rad_tex[0]+"~rad.\\par")
    cor.append(_(u"De même pour les autres mesures, on trouve alors respectivement : %s~rad, %s~rad, %s~rad, %s~rad et %s~rad.") %(tuple(mes_deg_en_rad_tex)))

    cor.append(_(u"\\item Convertir les cinq mesures suivantes en degrés : %s, %s, %s, %s et %s~rad.\\par") %(tuple(mes_rad_tex[0:5])))

    cor.append(_(u"On effectue alors la proportionnalité inverse : il faut multiplier par $\\dfrac{180}{\\pi}$.\\par"))
    cor.append(_(u"Après simplification, voici les résultats : %s\\degres, %s\\degres, %s\\degres, %s\\degres et %s\\degres.") %(tuple([rad2deg(r) for r in radq2])))

    cor.append(_(u"\\item Déterminer les mesures principales des angles suivants en radians : %s, %s, %s, %s et %s~rad.\\par") %(tuple(mes_rad_tex[5:10])))

    rep = mes_princ(radq3[0])
    nb_tours = (radq3[0][0]-rep[0]) // (2*radq3[0][1])

    cor.append(_(u"Une mesure d'angle en radians est définie modulo $2\\pi$, c'est-à-dire que l'ajout ou la suppression d'un tour ( qui vaut $2\\pi$ ou 360\\degres ) ne change pas un angle.\\par"))
    cor.append(_(u"Concrètement, avec le premier angle de la question, on remarque que :\\par"))
    cor.append(rad2tex(radq3[0])[:-1]+"\\equiv"+rad2tex(rep)[1:-1]+"+"+rad2tex([2*nb_tours*rep[1],rep[1]])[1:-1]+"\\equiv"+rad2tex(rep)[1:-1]+"+"+rad2tex([2*nb_tours,1])[1:-1]+"\\equiv"+rad2tex(rep)[1:-1]+u"~(2\\pi)$.\\par")
    cor.append(_(u"De même pour les autres mesures, on trouve alors respectivement : %s~rad, %s~rad, %s~rad, %s~rad et %s~rad.") %(tuple([rad2tex(mes_princ(r)) for r in radq3])))

    cor.append(_(u"\\item Des angles ont été placés sur le cercle trigonométrique ci-dessous, représentés en rouge par les points $M_0$, $M_1$, $M_2$ et $M_3$. Lire leurs mesures principales en radians"))
    cor.append(_(u"( les lignes vertes, grises et bleues représentent des angles multiples de $\\dfrac{\\pi}{3}$, de $\\dfrac{\\pi}{4}$ et de $\\dfrac{\\pi}{5}$ ).\\par"))

    cor.append(_(u"Les réponses sont directement données sur le cercle trigonométrique ci-dessous :\\par"))
    cor.append(cercle_trigo(1,mes_princ(radq4[0]),mes_princ(radq4[1]),mes_princ(radq4[2]),mes_princ(radq4[3])))
    cor.append(u"\\par")
    cor.append(_(u"Les points $M_0$, $M_1$, $M_2$ et $M_3$ définissent alors respectivement les angles %s, %s, %s et %s~rad.") %(tuple(mes_rad_tex[10:14])))
    cor.append(_(u"\\item Placer les angles suivants sur le cercle trigonométrique : %s, %s, %s et %s~rad.\\par") %(tuple(mes_rad_tex[14:])))

    cor.append(_(u"Les réponses sont directement données sur le cercle trigonométrique ci-dessous :\\par"))
    cor.append(cercle_trigo(1,radq5[0],radq5[1],radq5[2],radq5[3]))
    cor.append(u"\\par")
    cor.append(_(u"Ajoutons une simple remarque pour la dernière mesure, qui n'est pas principale : il faut effectuer en premier lieu une simplification, comme à la question 3. On obtient alors :\\par"))
    cor.append(rad2tex(radq5[3])[:-1]+"\\equiv"+rad2tex(mes_princ(radq5[3]))[1:-1]+"~(2\\pi)$.")
    cor.append(u"\\end{enumerate}\\par")

    return exo, cor

class cercle_trigonometrique(LegacyExercise):
    """Cercle trigonométrique"""

    tags = ["Seconde"]
    function = _cercle_trigonometrique
