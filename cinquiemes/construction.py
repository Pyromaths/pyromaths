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
import outils.Geometrie as geo
import random,math
from outils.Affichage import decimaux
#trigo en degré
tan =lambda z:math.tan(math.radians(z))
cos =lambda z:math.cos(math.radians(z))
sin =lambda z:math.sin(math.radians(z))
def exo_triangle():
    
    exo=["\\exercice",
         "\\begin{enumerate}"]
    cor=["\\exercice*",
         "\\begin{enumerate}"]
    cor.append("\\definecolor{enonce}{rgb}{0.11,0.56,0.98}")
    cor.append("\\definecolor{calcul}{rgb}{0.13,0.54,0.13}")
    if True:#toutes les constructions en test
        exo,cor=quest_LAL(exo,cor)
        exo,cor=quest_ALA(exo,cor)
        exo,cor=quest_AAL(exo,cor)
        exo,cor=quest_isocele_angbase(exo,cor)
        exo,cor=quest_isocele_angprincipal(exo,cor)
        exo,cor=quest_rectangle_hypo_angle(exo,cor)
        exo,cor=quest_rectangle_hypo_cote(exo,cor)
    else:#Construction choisies au hasard
        questions=[quest_LAL,
                   quest_ALA,
                   quest_AAL,
                   quest_isocele_angbase,
                   quest_isocele_angprincipal,
                   quest_rectangle_hypo_cote,
                   quest_rectangle_hypo_angle]
        random.shuffle(questions)
        for i in range(4):
            exo,cor=question[i](exo,cor)
    exo.append("\\end{enumerate}")
    cor.append("\\end{enumerate}")
    return exo,cor


def quest_LAL(exo,cor):
    """on donne un angle et les longueurs de ses deux côtés"""
    """            angBAC et      AB=c et AC=b"""
    A,B,C=geo.choix_points(3)
    c=0.1*random.randint(40,70)#longueur AB
    b=0.1*random.randint(20,100)#longueur BC
    angBAC=3*random.randint(7,50)#BAC mesure entre 21° et 150°
    
    exo.append(u"\\item Trace un triangle $%s%s%s$ tel que $%s%s=\\unit[%s]{cm}$, $%s%s=\\unit[%s]{cm}$ et $\\widehat{%s%s%s}=%s\\degres$"
               %(A,B,C,A,B,decimaux(c),A,C,decimaux(b),B,A,C,angBAC))
    cor.append(u"\\item Trace un triangle $%s%s%s$ tel que $%s%s=\\unit[%s]{cm}$, $%s%s=\\unit[%s]{cm}$ et $\\widehat{%s%s%s}=%s\\degres$.\\par"
               %(A,B,C,A,B,decimaux(c),A,C,decimaux(b),B,A,C,angBAC))
    cor.append(u"\\begin{pspicture}(%s,%s)(%s,%s)"%(min(0,b*cos(angBAC))-0.4,-1,max(b,b*cos(angBAC))+0.4,b*sin(angBAC)+1))
    cor.append(u"\\pstTriangle(0,0){%s}(%s;%s){%s}(%s,0){%s}"%(A,b,angBAC,C,c,B))
    cor.append(u"\\color{enonce}\\pstMarkAngle[linecolor=enonce]{%s}{%s}{%s}{%s\\degres}"%(B,A,C,angBAC))
    cor.append(u"\\pstLineAB[nodesepB=-1]{%s}{%s}"%(A,C))
    cor.append(u"\\pstRotation[RotAngle=7,PointSymbol=none,PointName=none]{%s}{%s}[C_1]"%(A,C))
    cor.append(u"\\pstRotation[RotAngle=-7,PointSymbol=none,PointName=none]{%s}{%s}[C_2]"%(A,C))
    cor.append(u"\\pstArcOAB[linecolor=calcul]{%s}{C_2}{C_1}"%(A))
    cor.append(u"\\pyrLongueur(0,0)(%s,0){\\color{enonce}\\unit[%s]{cm}}"%(c,decimaux(c)))
    if angBAC<111:
        cor.append(u"\\pyrLongueurh(0,0)(%s;%s){\\color{enonce}\\unit[%s]{cm}}"%(b,angBAC,decimaux(b)))
    else:
        cor.append(u"\\pyrLongueur(%s;%s)(0,0){\\color{enonce}\\unit[%s]{cm}}"%(b,angBAC,decimaux(b)))
    cor.append(u"\\end{pspicture}")
    return exo,cor

def quest_ALA(exo,cor):
    """on donne deux angles et la longueur du côté commun"""
    """ angBAC et angABC et AB=c"""
    A,B,C=geo.choix_points(3)
    c=0.1*random.randint(40,70)#longueur AB
    angBAC=5*random.randint(4,12)
    angABC=5*random.randint(4,12)
    exo.append(u"\\item Trace un triangle $%s%s%s$ tel que $%s%s=\\unit[%s]{cm}$,  $\\widehat{%s%s%s}=%s\\degres$ et $\\widehat{%s%s%s}=%s\\degres$"
               %(A,B,C,A,B,decimaux(c),B,A,C,angBAC,A,B,C,angABC))
    cor.append(u"\\item Trace un triangle $%s%s%s$ tel que $%s%s=\\unit[%s]{cm}$,  $\\widehat{%s%s%s}=%s\\degres$ et $\\widehat{%s%s%s}=%s\\degres$\\par"
               %(A,B,C,A,B,decimaux(c),B,A,C,angBAC,A,B,C,angABC))
    x_C=(c*tan(angABC))/(tan(angABC)+tan(angBAC))
    y_C=x_C*tan(angBAC)
    cor.append(u"\\begin{pspicture}(-0.4,-1)(%s,%s)"%(c+1,y_C+1))
    cor.append(u"\\psset{MarkAngleRadius=0.6}")
    cor.append(u"\\pstTriangle(0,0){%s}(%s,0){%s}(%s,%s){%s}"%(A,c,B,x_C,y_C,C))
    cor.append(u"\\pstLineAB[nodesepB=-1]{%s}{%s}\\pstLineAB[nodesepB=-1]{%s}{%s}"%(A,C,B,C))
    cor.append(u"\\pyrLongueur(0,0)(%s,0){\\color{enonce}\\unit[%s]{cm}}"%(c,decimaux(c)))
    cor.append(u"\\color{enonce}\\pstMarkAngle[linecolor=enonce]{%s}{%s}{%s}{%s\\degres}"%(B,A,C,angBAC))
    cor.append(u"\\color{enonce}\\pstMarkAngle[linecolor=enonce]{%s}{%s}{%s}{%s\\degres}"%(C,B,A,angABC))
    cor.append(u"\\end{pspicture}")
    return exo,cor

def quest_AAL(exo,cor):
    """on donne deux angles et la longueur du côté commun"""
    """ angBAC et angACB et AB=c"""
    A,B,C=geo.choix_points(3)
    c=0.2*random.randint(20,50)#longueur AB
    angBAC=3*random.randint(10,24)#entre 30° et 72°
    angACB=3*random.randint(10,24)#entre 30° et 72°
    exo.append(u"\\item Trace un triangle $%s%s%s$ tel que $%s%s=\\unit[%s]{cm}$,  $\\widehat{%s%s%s}=%s\\degres$ et $\\widehat{%s%s%s}=%s\\degres$"
               %(A,B,C,A,B,c,B,A,C,angBAC,A,C,B,angACB))
    cor.append(u"\\item Trace un triangle $%s%s%s$ tel que $%s%s=\\unit[%s]{cm}$,  $\\widehat{%s%s%s}=%s\\degres$ et $\\widehat{%s%s%s}=%s\\degres$\\par"
               %(A,B,C,A,B,decimaux(c),B,A,C,angBAC,A,C,B,angACB))
    cor.append(u"On doit d'abord calculer la mesure de $\\widehat{%s%s%s}$.\\\\"
               %(A,B,C))
    angABC=180-angBAC-angACB
    cor.append(u"Or la somme des trois angles d'un triangle est égale à 180\\degres donc $\\widehat{%s%s%s}=180\\degres-%s\\degres-%s\\degres=%s\\degres$.\\par"
               %(A,B,C,angBAC,angACB,angABC))
    x_C=(c*tan(angABC))/(tan(angABC)+tan(angBAC))
    y_C=x_C*tan(angBAC)
    cor.append(u"\\begin{pspicture}(-1,-1)(%s,%s)"%(c+1,y_C+1))
    cor.append(u"\\psset{MarkAngleRadius=0.6}")
    cor.append(u"\\pstTriangle(0,0){%s}(%s,0){%s}(%s,%s){%s}"%(A,c,B,x_C,y_C,C))
    cor.append(u"\\pstLineAB[nodesepB=-1]{%s}{%s}\\pstLineAB[nodesepB=-1]{%s}{%s}"%(A,C,B,C))
    cor.append(u"\\pstMarkAngle[linecolor=calcul]{%s}{%s}{%s}{\\color{calcul}%s\\degres}"%(C,B,A,angABC))
    cor.append(u"\\color{enonce}\\pstMarkAngle[linecolor=enonce]{%s}{%s}{%s}{%s\\degres}"%(A,C,B,angACB))
    cor.append(u"\\pyrLongueur(0,0)(%s,0){\\color{enonce}\\unit[%s]{cm}}"%(c,decimaux(c)))
    cor.append(u"\\pstMarkAngle[linecolor=enonce]{%s}{%s}{%s}{%s\\degres}"%(B,A,C,angBAC))
    cor.append(u"\\end{pspicture}")
    return exo,cor

def quest_isocele_angbase(exo,cor):
    """on donne ABC isocele en C, AB=c et angBAC"""
    A,B,C=geo.choix_points(3)
    c=0.2*random.randint(20,37)#longueur AB
    angABC=angBAC=5*random.randint(4,12)
    exo.append(u"\\item Trace un triangle $%s%s%s$ isocèle en $%s$ tel que $%s%s=\\unit[%s]{cm}$,  $\\widehat{%s%s%s}=%s\\degres$."
               %(A,B,C,C,A,B,decimaux(c),B,A,C,angBAC))
    cor.append(u"\\item Trace un triangle $%s%s%s$ isocèle en $%s$ tel que $%s%s=\\unit[%s]{cm}$,  $\\widehat{%s%s%s}=%s\\degres$. \\par"
               %(A,B,C,C,A,B,decimaux(c),B,A,C,angBAC))
    cor.append(u"Comme $%s%s%s$ est un triangle isocèle en $%s$, je sais que les angles adjacents à la base sont de même mesure \
donc $\\widehat{%s%s%s}=\\widehat{%s%s%s}=%s\\degres$.\\par"%(A,B,C,C,A,B,C,B,A,C,angBAC))
##    cor.append(u"On peut alors calculer la mesure de $\\widehat{%s%s%s}$.\\\\"
##               %(A,C,B))
##    angACB=180-angBAC-angBAC
##    cor.append(u"car la somme des trois angles d'un triangle est égale à 180° donc $\\widehat{%s%s%s}=180-%s-%s=%s$.\\par"
##               %(A,C,B,angBAC,angBAC,angACB))
##    
    x_C=(c*tan(angABC))/(tan(angABC)+tan(angBAC))
    y_C=x_C*tan(angBAC)
    cor.append(u"\\begin{pspicture}(-1,-1)(%s,%s)"%(c+1,y_C+1))
    cor.append(u"\\psset{MarkAngleRadius=0.6}")
    cor.append(u"\\pstTriangle(0,0){%s}(%s,0){%s}(%s,%s){%s}"%(A,c,B,x_C,y_C,C))
    cor.append(u"\\pstSegmentMark[linecolor=enonce]{%s}{%s}"%(A,C))
    cor.append(u"\\pstSegmentMark[linecolor=enonce]{%s}{%s}"%(B,C))
    cor.append(u"\\pstLineAB[nodesepB=-1]{%s}{%s}\\pstLineAB[nodesepB=-1]{%s}{%s}"%(A,C,B,C))
    cor.append(u"\\pyrLongueur(0,0)(%s,0){\\color{enonce}\\unit[%s]{cm}}"%(c,decimaux(c)))
    cor.append(u"\\color{enonce}\\pstMarkAngle[linecolor=enonce]{%s}{%s}{%s}{%s\\degres}"%(B,A,C,angBAC))
    cor.append(u"\\color{calcul}\\pstMarkAngle[linecolor=calcul]{%s}{%s}{%s}{%s\\degres}"%(C,B,A,angABC))
    cor.append(u"\\end{pspicture}")
    return exo,cor

def quest_isocele_angprincipal(exo,cor):
    """on donne ABC isocele en C, AB=c et angACB"""
    A,B,C=geo.choix_points(3)
    c=0.2*random.randint(20,35)#longueur AB
    angACB=2*random.randint(20,60)#ACB est pair entre 40° et 120°
    angBAC=angABC=(180-angACB)/2
    exo.append(u"\\item Trace un triangle $%s%s%s$ isocèle en $%s$ tel que $%s%s=\\unit[%s]{cm}$,  $\\widehat{%s%s%s}=%s\\degres$."
               %(A,B,C,C,A,B,decimaux(c),A,C,B,angACB))
    cor.append(u"\\item Trace un triangle $%s%s%s$ isocèle en $%s$ tel que $%s%s=\\unit[%s]{cm}$,  $\\widehat{%s%s%s}=%s\\degres$.\\par"
               %(A,B,C,C,A,B,decimaux(c),A,C,B,angACB))
    cor.append(u"Comme $%s%s%s$ est un triangle isocèle en $%s$, je sais que les angles adjacents à la base sont de même mesure \
donc $\\widehat{%s%s%s}=$\\widehat{%s%s%s}$.\\par"%(A,B,C,C,A,B,C,B,A,C))
    cor.append(u"De plus, je sais que la somme des mesures des trois angles d'un triangle est égale à 180\\degres \\\\ \
donc $\\widehat{%s%s%s}=$\\widehat{%s%s%s}=(180\\degres-%s\\degres)\\div 2=%s\\degres$. \\par"
               %(B,A,C,A,B,C,angACB,angBAC))
    x_C=(c*tan(angABC))/(tan(angABC)+tan(angBAC))
    y_C=x_C*tan(angBAC)
    cor.append(u"\\begin{pspicture}(-1,-1)(%s,%s)"%(c+1,y_C+1))
    cor.append(u"\\psset{MarkAngleRadius=0.6}")
    cor.append(u"\\pstTriangle(0,0){%s}(%s,0){%s}(%s,%s){%s}"%(A,c,B,x_C,y_C,C))
    cor.append(u"\\pstSegmentMark[linecolor=enonce]{%s}{%s}"%(A,C))
    cor.append(u"\\pstSegmentMark[linecolor=enonce]{%s}{%s}"%(B,C))
    cor.append(u"\\pstLineAB[nodesepB=-1]{%s}{%s}\\pstLineAB[nodesepB=-1]{%s}{%s}"%(A,C,B,C))
    cor.append(u"\\pyrLongueur(0,0)(%s,0){\\color{enonce}\\unit[%s]{cm}}"%(c,decimaux(c)))
    cor.append(u"\\color{enonce}\\pstMarkAngle[linecolor=enonce]{%s}{%s}{%s}{%s\\degres}"%(A,C,B,angACB))
    cor.append(u"\\color{calcul}\\pstMarkAngle[linecolor=calcul]{%s}{%s}{%s}{%s\\degres}"%(B,A,C,angBAC))
    cor.append(u"\\pstMarkAngle[linecolor=calcul]{%s}{%s}{%s}{%s\\degres}"%(C,B,A,angABC))
    cor.append(u"\\end{pspicture}")
    return exo,cor
def quest_rectangle_hypo_angle(exo,cor):
    """on donne un triangle ABC rectangle en C et l'hypotenuse AB et l'angle BAC"""
    A,B,C=geo.choix_points(3)
    c=0.2*random.randint(20,35)#longueur AB
    angBAC=3*random.randint(7,23)#un angle mesurant entre 21° et 69°
    angABC=90-angBAC
    #angACB=90
    exo.append(u"\\item Trace un triangle $%s%s%s$ rectangle en $%s$ tel que $%s%s=\\unit[%s]{cm}$ et $\\widehat{%s%s%s}=%s\\degres$.\\par"
               %(A,B,C,C,A,B,decimaux(c),B,A,C,angBAC))
    cor.append(u"\\item Trace un triangle $%s%s%s$ rectangle en $%s$ tel que $%s%s=\\unit[%s]{cm}$ et $\\widehat{%s%s%s}=%s\\degres$.\\par"
               %(A,B,C,C,A,B,decimaux(c),B,A,C,angBAC))
    x_C=(c*tan(angABC))/(tan(angABC)+tan(angBAC))
    y_C=x_C*tan(angBAC)
    cor.append("\\begin{multicols}{2}")
    cor.append(u"Je sais que dans un triangle rectangle, les deux angles aigus sont complémentaires \\\\ \
donc $\widehat{%s%s%s}=90\\degres-%s\\degres=%s\\degres$."%(B,A,C,angBAC,angABC))
    cor.append("\\begin{enumerate}")
    cor.append(u"\\item Je trace le segment $[%s%s]$ mesurant $\\unit[%s]{cm}$ ;"%(A,B,c))
    cor.append(u"\\item puis la demi-droite $[%s%s)$ en traçant l'angle $\widehat{%s%s%s}$ ;"%(A,C,B,A,C))
    cor.append(u"\\item puis la demi-droite $[%s%s)$ en traçant l'angle $\widehat{%s%s%s}$ ;"%(B,C,A,B,C))
    cor.append(u"\\item enfin je vérifie les trois {\\color{enonce}conditions de l'énoncé}.")
    cor.append("\\end{enumerate}\n\columnbreak")
    cor.append(u"\\begin{pspicture}(-0.4,-1)(%s,%s)"%(c+0.4,y_C+1))
    cor.append(u"\\psset{MarkAngleRadius=0.6}")
    cor.append(u"\\pstTriangle(0,0){%s}(%s,0){%s}(%s,%s){%s}"%(A,c,B,x_C,y_C,C))
    cor.append(u"\\color{enonce}\\pstRightAngle[linecolor=enonce]{%s}{%s}{%s}"%(A,C,B))
    cor.append(u"\\pstLineAB[nodesepB=-1]{%s}{%s}\\pstLineAB[nodesepB=-1]{%s}{%s}"%(A,C,B,C))
    cor.append(u"\\pyrLongueur(0,0)(%s,0){\\color{enonce}\\unit[%s]{cm}}"%(c,decimaux(c)))
    cor.append(u"\\color{enonce}\\pstMarkAngle[linecolor=enonce]{%s}{%s}{%s}{%s\\degres}"%(B,A,C,angBAC))
    cor.append(u"\\color{calcul}\\pstMarkAngle[linecolor=calcul]{%s}{%s}{%s}{%s\\degres}"%(C,B,A,angABC))
    cor.append(u"\\end{pspicture}")
    cor.append("\\end{multicols}")
    return exo,cor
def quest_rectangle_hypo_cote(exo,cor):
    """on donne un triangle ABC rectangle en B et l'hypotenuse AC et le coté AB"""
    A,B,C=geo.choix_points(3)
    c=0.2*random.randint(20,35)#longueur AB
    b=0.1*random.randint(int(10*(c))+1,100)#longueur AC
    angABC=90
    #calcul pour tracer
    angBAC=math.degrees(math.acos(float(c)/float(b)))
    exo.append(u"\\item Trace un triangle $%s%s%s$ rectangle en $%s$ tel que $%s%s=\\unit[%s]{cm}$,  $%s%s=\\unit[%s]{cm}$.\\par"
               %(A,B,C,B,A,B,decimaux(c),A,C,decimaux(b)))
    cor.append(u"\\item Trace un triangle $%s%s%s$ rectangle en $%s$ tel que $%s%s=\\unit[%s]{cm}$, $%s%s=\\unit[%s]{cm}$.\\par"
               %(A,B,C,B,A,B,decimaux(c),A,C,decimaux(b)))
    cor.append("\\begin{multicols}{2}")
    cor.append(u"\\begin{enumerate}")
    cor.append(u"\\item Je trace le segment $[%s%s]$ mesurant $\\unit[%s]{cm}$ ;"%(A,B,decimaux(c)))
    cor.append(u"\\item puis je trace l'angle droit $\\widehat{%s%s%s}$ ;"%(A,B,C))
    cor.append(u"\\item enfin, je reporte au compas la longueur $%s%s=\\unit[%s]{cm}$ à partir de $%s$."%(A,C,decimaux(b),A))
    cor.append("\\end{enumerate}\n\columnbreak")
    x_C=(c*tan(angABC))/(tan(angABC)+tan(angBAC))
    y_C=x_C*tan(angBAC)
    cor.append(u"\\begin{pspicture}(-0.4,-1)(%s,%s)"%(c+0.4,y_C+1))
    cor.append(u"\\psset{MarkAngleRadius=0.6}")
    cor.append(u"\\pstTriangle(0,0){%s}(%s,0){%s}(%s,%s){%s}"%(A,c,B,x_C,y_C,C))
    cor.append(u"\\color{enonce}\\pstRightAngle[linecolor=enonce]{%s}{%s}{%s}"%(C,B,A))
    cor.append(u"\\pstRotation[RotAngle=7,PointSymbol=none,PointName=none]{%s}{%s}[C_1]"%(A,C))
    cor.append(u"\\pstRotation[RotAngle=-7,PointSymbol=none,PointName=none]{%s}{%s}[C_2]"%(A,C))
    cor.append(u"\\pstArcOAB[linecolor=calcul]{%s}{C_2}{C_1}"%(A))
    cor.append(u"\\pstLineAB{%s}{%s}\\pstLineAB[nodesepB=-1]{%s}{%s}"%(A,B,B,C))
    cor.append(u"\\pyrLongueur(0,0)(%s,0){\\color{enonce}\\unit[%s]{cm}}"%(c,decimaux(c)))
    cor.append(u"\\pyrLongueurh(0,0)(%s,%s){\\color{enonce}\\unit[%s]{cm}}"%(x_C,y_C,decimaux(b)))
    cor.append(u"\\end{pspicture}")
    cor.append("\\end{multicols}")
    return exo,cor
