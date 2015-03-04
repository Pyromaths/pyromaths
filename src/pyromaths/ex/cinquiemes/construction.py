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
from pyromaths.outils import Geometrie as geo
import random, math
from pyromaths.outils.Affichage import decimaux
from pyromaths.outils.Geometrie import cotation, cotation_h

# trigo en degré
tan = lambda z:math.tan(math.radians(z))
cos = lambda z:math.cos(math.radians(z))
sin = lambda z:math.sin(math.radians(z))
def shuffle_nom(polygone):
    """renvoie un nom aléatoire du polygone"""
    n = len(polygone)
    polygone = polygone + polygone + polygone
    debut = n + random.randrange(n)
    sens = [-1, 1][random.randrange(2)]
    nom = ""
    for i in range(debut, debut + n * sens, sens):
        nom += polygone[i]
    return nom

def exo_triangle(test=False):
    questions = [quest_equilateral,
           quest_LAL,
           quest_ALA,
           quest_AAL,
           quest_isocele_angbase,
           quest_isocele_angprincipal,
           quest_rectangle_hypo_cote,
           quest_rectangle_hypo_angle,
           ]
    exo = ["\\exercice",
         "\\begin{enumerate}"]
    cor = ["\\exercice*",
         "\\begin{enumerate}"]
    cor.append("\\definecolor{enonce}{rgb}{0.11,0.56,0.98}")
    cor.append("\\definecolor{calcul}{rgb}{0.13,0.54,0.13}")
    cor.append(u"\\psset{MarkAngleRadius=0.6,PointSymbol=none}")
    if test:  # toutes les constructions en test
        for quest in questions:
            quest(exo, cor)
    else:  # Construction choisies au hasard
        random.shuffle(questions)
        for i in range(4):
            questions[i](exo, cor)

    exo.append("\\end{enumerate}")
    cor.append("\\end{enumerate}")
    return exo, cor

exo_triangle.description = u'Construction de triangles'


def quest_equilateral(exo, cor):
    A, B, C = geo.choix_points(3)
    nom = shuffle_nom([A, B, C])
    c = 0.1 * random.randint(40, 70)  # longueur AB
    angBAC = angABC = 60
    exo.append(u"\\item Trace un triangle $%s$ équilatéral de côté $\\unit[%s]{cm}$.\\par" % (nom, decimaux(c)))
    cor.append(u"\\item Trace un triangle $%s$ équilatéral de côté $\\unit[%s]{cm}$.\\par" % (nom, decimaux(c)))
    x_C = (c * tan(angABC)) / (tan(angABC) + tan(angBAC))
    y_C = x_C * tan(angBAC)
    cor.append(u"\\begin{pspicture}(-1,-1)(%.3f,%.3f)" % (c + 1, y_C + 1))
    cor.append(u"\\pstTriangle(0,0){%s}(%.3f,0){%s}(%.3f,%.3f){%s}" % (A, c, B, x_C, y_C, C))
    cor.append(u"\\pstLineAB{%s}{%s}\\lput{:U}{\\psset{linecolor=enonce}\\MarkHashh}" % (C, A))
    cor.append(u"\\pstLineAB{%s}{%s}\\lput{:U}{\\psset{linecolor=enonce}\\MarkHashh}" % (B, C))
    cor.append(u"\\pstLineAB{%s}{%s}\\lput{:U}{\\psset{linecolor=enonce}\\MarkHashh}" % (A, B))
    cor.append(u"\\pstRotation[RotAngle=7,PointSymbol=none,PointName=none]{%s}{%s}[C_1]" % (A, C))
    cor.append(u"\\pstRotation[RotAngle=-7,PointSymbol=none,PointName=none]{%s}{%s}[C_2]" % (A, C))
    cor.append(u"\\pstArcOAB[linecolor=calcul]{%s}{C_2}{C_1}" % (A))
    cor.append(u"\\pstRotation[RotAngle=7,PointSymbol=none,PointName=none]{%s}{%s}[C_3]" % (B, C))
    cor.append(u"\\pstRotation[RotAngle=-7,PointSymbol=none,PointName=none]{%s}{%s}[C_4]" % (B, C))
    cor.append(u"\\pstArcOAB[linecolor=calcul]{%s}{C_4}{C_3}" % (B))
    cor.append(cotation((0, 0), (c, 0), decimaux(c), couleur="enonce"))
    cor.append(u"\\end{pspicture}")

def quest_LAL(exo, cor):
    """on donne un angle et les longueurs de ses deux côtés"""
    """            angBAC et      AB=c et AC=b"""
    A, B, C = geo.choix_points(3)
    nom = shuffle_nom([A, B, C])
    c = 0.1 * random.randint(40, 70)  # longueur AB
    b = 0.1 * random.randint(20, 100)  # longueur BC
    angBAC = 3 * random.randint(7, 50)  # BAC mesure entre 21° et 150°
    
    exo.append(u"\\item Trace un triangle $%s$ tel que $%s%s=\\unit[%s]{cm}$, $%s%s=\\unit[%s]{cm}$ et $\\widehat{%s%s%s}=%s\\degres$"
               % (nom, A, B, decimaux(c), A, C, decimaux(b), B, A, C, angBAC))
    cor.append(u"\\item Trace un triangle $%s$ tel que $%s%s=\\unit[%s]{cm}$, $%s%s=\\unit[%s]{cm}$ et $\\widehat{%s%s%s}=%s\\degres$.\\par"
               % (nom, A, B, decimaux(c), A, C, decimaux(b), B, A, C, angBAC))
    cor.append(u"\\begin{pspicture}(%.3f,%.3f)(%.3f,%.3f)" % (min(0, b * cos(angBAC)) - 0.4, -1, max(b, b * cos(angBAC)) + 0.4, b * sin(angBAC) + 1))
    cor.append(u"\\pstTriangle(0,0){%s}(%.3f;%.3f){%s}(%.3f,0){%s}" % (A, b, angBAC, C, c, B))
    cor.append(u"\\color{enonce}\\pstMarkAngle[linecolor=enonce]{%s}{%s}{%s}{%s\\degres}" % (B, A, C, angBAC))
    cor.append(u"\\pstLineAB[nodesepB=-1]{%s}{%s}" % (A, C))
    cor.append(u"\\pstRotation[RotAngle=7,PointSymbol=none,PointName=none]{%s}{%s}[C_1]" % (A, C))
    cor.append(u"\\pstRotation[RotAngle=-7,PointSymbol=none,PointName=none]{%s}{%s}[C_2]" % (A, C))
    cor.append(u"\\pstArcOAB[linecolor=calcul]{%s}{C_2}{C_1}" % (A))
    cor.append(cotation((0, 0), (c, 0), decimaux(c), couleur="enonce"))
    if angBAC < 111:
        x_C, y_C = b * cos(angBAC), b * sin(angBAC)
        cor.append(cotation_h((0, 0), (x_C, y_C), decimaux(b), couleur="enonce"))
    else:
        x_C, y_C = b * cos(angBAC), b * sin(angBAC)
        cor.append(cotation((x_C, y_C), (0, 0), decimaux(b), couleur="enonce"))
    cor.append(u"\\end{pspicture}")

def quest_ALA(exo, cor):
    """on donne deux angles et la longueur du côté commun"""
    """ angBAC et angABC et AB=c"""
    A, B, C = geo.choix_points(3)
    nom = shuffle_nom([A, B, C])
    c = 0.1 * random.randint(40, 70)  # longueur AB
    angBAC = 5 * random.randint(4, 12)
    angABC = 5 * random.randint(4, 12)
    exo.append(u"\\item Trace un triangle $%s$ tel que $%s%s=\\unit[%s]{cm}$,  $\\widehat{%s%s%s}=%s\\degres$ et $\\widehat{%s%s%s}=%s\\degres$"
               % (nom, A, B, decimaux(c), B, A, C, angBAC, A, B, C, angABC))
    cor.append(u"\\item Trace un triangle $%s$ tel que $%s%s=\\unit[%s]{cm}$,  $\\widehat{%s%s%s}=%s\\degres$ et $\\widehat{%s%s%s}=%s\\degres$\\par"
               % (nom, A, B, decimaux(c), B, A, C, angBAC, A, B, C, angABC))
    x_C = (c * tan(angABC)) / (tan(angABC) + tan(angBAC))
    y_C = x_C * tan(angBAC)
    cor.append(u"\\begin{pspicture}(-0.4,-1)(%.3f,%.3f)" % (c + 1, y_C + 1))
    cor.append(u"\\pstTriangle(0,0){%s}(%.3f,0){%s}(%.3f,%.3f){%s}" % (A, c, B, x_C, y_C, C))
    cor.append(u"\\pstLineAB[nodesepB=-1]{%s}{%s}\\pstLineAB[nodesepB=-1]{%s}{%s}" % (A, C, B, C))
    cor.append(cotation((0, 0), (c, 0), decimaux(c), couleur="enonce"))
    cor.append(u"\\color{enonce}\\pstMarkAngle[linecolor=enonce]{%s}{%s}{%s}{%s\\degres}" % (B, A, C, angBAC))
    cor.append(u"\\color{enonce}\\pstMarkAngle[linecolor=enonce]{%s}{%s}{%s}{%s\\degres}" % (C, B, A, angABC))
    cor.append(u"\\end{pspicture}")

def quest_AAL(exo, cor):
    """on donne deux angles et la longueur d'un côté non commun aux deux angles"""
    """ angBAC et angACB et AB=c"""
    A, B, C = geo.choix_points(3)
    nom = shuffle_nom([A, B, C])
    angBAC = 3 * random.randint(10, 24)  # entre 30° et 72°
    angACB = 3 * random.randint(10, 24)  # entre 30° et 72°
    angABC = 180 - angBAC - angACB
    ABmax = int(35 * (tan(angABC) + tan(angBAC)) / (tan(angBAC) * tan(angABC)))  # donne une hauteur inférieur à 35*0.2=7 cm
    c = 0.2 * random.randint(20, max(20, ABmax))  # longueur AB
    
    exo.append(u"\\item Trace un triangle $%s$ tel que $%s%s=\\unit[%s]{cm}$,  $\\widehat{%s%s%s}=%s\\degres$ et $\\widehat{%s%s%s}=%s\\degres$"
               % (nom, A, B, decimaux(c), B, A, C, angBAC, A, C, B, angACB))
    cor.append(u"\\item Trace un triangle $%s$ tel que $%s%s=\\unit[%s]{cm}$,  $\\widehat{%s%s%s}=%s\\degres$ et $\\widehat{%s%s%s}=%s\\degres$\\par"
               % (nom, A, B, decimaux(c), B, A, C, angBAC, A, C, B, angACB))
    cor.append(u"On doit d'abord calculer la mesure de $\\widehat{%s%s%s}$.\\\\"
               % (A, B, C))
    cor.append(u"Or la somme des trois angles d'un triangle est égale à 180\\degres donc $\\widehat{%s%s%s}=180\\degres-%s\\degres-%s\\degres=%s\\degres$.\\par"
               % (A, B, C, angBAC, angACB, angABC))
    x_C = (c * tan(angABC)) / (tan(angABC) + tan(angBAC))
    y_C = x_C * tan(angBAC)
    cor.append(u"\\begin{pspicture}(-1,-1)(%.3f,%.3f)" % (c + 1, y_C + 1))
    cor.append(u"\\pstTriangle(0,0){%s}(%.3f,0){%s}(%.3f,%.3f){%s}" % (A, c, B, x_C, y_C, C))
    cor.append(u"\\pstLineAB[nodesepB=-1]{%s}{%s}\\pstLineAB[nodesepB=-1]{%s}{%s}" % (A, C, B, C))
    cor.append(u"\\pstMarkAngle[linecolor=calcul]{%s}{%s}{%s}{\\color{calcul}%s\\degres}" % (C, B, A, angABC))
    cor.append(u"\\color{enonce}\\pstMarkAngle[linecolor=enonce]{%s}{%s}{%s}{%s\\degres}" % (A, C, B, angACB))
    cor.append(cotation((0, 0), (c, 0), decimaux(c), couleur="enonce"))
    cor.append(u"\\pstMarkAngle[linecolor=enonce]{%s}{%s}{%s}{%s\\degres}" % (B, A, C, angBAC))
    cor.append(u"\\end{pspicture}")

def quest_isocele_angbase(exo, cor):
    """on donne ABC isocele en C, AB=c et angBAC"""
    A, B, C = geo.choix_points(3)
    nom = shuffle_nom([A, B, C])
    angABC = angBAC = random.randint(20, 70)
    maxc = max(20, int(35 / tan(angBAC)))  # longueur c maximale pour que la hauteur soit 7 cm =0.2*35
    minc = min(20, int(35 / tan(angBAC)))
    c = 0.2 * random.randint(minc, min(maxc, 50))  # longueur AB
    # Calcul pour tracer
    x_C = c / 2
    y_C = x_C * tan(angBAC)

    exo.append(u"\\item Trace un triangle $%s$ isocèle en $%s$ tel que $%s%s=\\unit[%s]{cm}$,  $\\widehat{%s%s%s}=%s\\degres$."
               % (nom, C, A, B, decimaux(c), B, A, C, angBAC))
    cor.append(u"\\item Trace un triangle $%s$ isocèle en $%s$ tel que $%s%s=\\unit[%s]{cm}$,  $\\widehat{%s%s%s}=%s\\degres$. \\par"
               % (nom, C, A, B, decimaux(c), B, A, C, angBAC))
    cor.append(u"Comme $%s%s%s$ est un triangle isocèle en $%s$, je sais que les angles adjacents à la base sont de même mesure \
donc $\\widehat{%s%s%s}=\\widehat{%s%s%s}=%s\\degres$.\\par" % (A, B, C, C, A, B, C, B, A, C, angBAC))
    cor.append(u"\\begin{pspicture}(-1,-1)(%.3f,%.3f)" % (c + 1, y_C + 1))
    cor.append(u"\\pstTriangle(0,0){%s}(%.3f,0){%s}(%.3f,%.3f){%s}" % (A, c, B, x_C, y_C, C))
    cor.append(u"\\pstLineAB[nodesepB=-1]{%s}{%s}" % (A, C))
    cor.append("\\pstLineAB[linestyle=none]{%s}{%s} \\lput{:U}{\\psset{linecolor=enonce}\\MarkHashh}" % (A, C))
    cor.append(u"\\pstLineAB[nodesepB=-1]{%s}{%s}" % (B, C))
    cor.append(u"\\pstLineAB[linestyle=none]{%s}{%s}\\lput{:U}{\\psset{linecolor=enonce}\\MarkHashh}" % (B, C))
    cor.append(cotation((0, 0), (c, 0), decimaux(c), couleur="enonce"))
    cor.append(u"\\color{enonce}\\pstMarkAngle[linecolor=enonce]{%s}{%s}{%s}{%s\\degres}" % (B, A, C, angBAC))
    cor.append(u"\\color{calcul}\\pstMarkAngle[linecolor=calcul]{%s}{%s}{%s}{%s\\degres}" % (C, B, A, angABC))
    cor.append(u"\\end{pspicture}")

def quest_isocele_angprincipal(exo, cor):
    """on donne ABC isocele en C, AB=c et angACB"""
    A, B, C = geo.choix_points(3)
    nom = shuffle_nom([A, B, C])
    angACB = 2 * random.randint(20, 60)  # ACB est pair entre 40° et 120°
    angBAC = angABC = (180 - angACB) / 2
    maxc = max(20, int(35 / tan(angBAC)))  # longueur c maximale pour que la hauteur soit 7 cm =0.2*35
    c = 0.2 * random.randint(20, min(maxc, 35))  # longueur AB
    # Calcul pour tracer
    x_C = c / 2
    y_C = x_C * tan(angBAC)
    
    exo.append(u"\\item Trace un triangle $%s$ isocèle en $%s$ tel que $%s%s=\\unit[%s]{cm}$,  $\\widehat{%s%s%s}=%s\\degres$."
               % (nom, C, A, B, decimaux(c), A, C, B, angACB))
    cor.append(u"\\item Trace un triangle $%s$ isocèle en $%s$ tel que $%s%s=\\unit[%s]{cm}$,  $\\widehat{%s%s%s}=%s\\degres$.\\par"
               % (nom, C, A, B, decimaux(c), A, C, B, angACB))
    cor.append(u"Comme $%s%s%s$ est un triangle isocèle en $%s$, je sais que les angles adjacents à la base sont de même mesure \
donc $\\widehat{%s%s%s}=\\widehat{%s%s%s}$.\\par" % (A, B, C, C, A, B, C, B, A, C))
    cor.append(u"De plus, je sais que la somme des mesures des trois angles d'un triangle est égale à 180\\degres \\\\ \
donc $\\widehat{%s%s%s}=\\widehat{%s%s%s}=(180\\degres-%s\\degres)\\div 2=%s\\degres$. \\par"
               % (B, A, C, A, B, C, angACB, angBAC))
    cor.append(u"\\begin{pspicture}(-1,-1)(%.3f,%.3f)" % (c + 1, y_C + 1))
    cor.append(u"\\pstTriangle(0,0){%s}(%.3f,0){%s}(%.3f,%.3f){%s}" % (A, c, B, x_C, y_C, C))
    cor.append(u"\\pstLineAB[nodesepB=-1]{%s}{%s}" % (A, C))
    cor.append("\\pstLineAB[linestyle=none]{%s}{%s} \\lput{:U}{\\psset{linecolor=enonce}\\MarkHashh}" % (A, C))
    cor.append(u"\\pstLineAB[nodesepB=-1]{%s}{%s}" % (B, C))
    cor.append("\\pstLineAB[linestyle=none]{%s}{%s} \\lput{:U}{\\psset{linecolor=enonce}\\MarkHashh}" % (B, C))
    cor.append(cotation((0, 0), (c, 0), decimaux(c), couleur="enonce"))
    cor.append(u"\\color{enonce}\\pstMarkAngle[linecolor=enonce,Mark=MarkHash]{%s}{%s}{%s}{%s\\degres}" % (A, C, B, angACB))
    cor.append(u"\\color{calcul}\\pstMarkAngle[linecolor=calcul]{%s}{%s}{%s}{%s\\degres}" % (B, A, C, angBAC))
    cor.append(u"\\pstMarkAngle[linecolor=calcul]{%s}{%s}{%s}{%s\\degres}" % (C, B, A, angABC))
    cor.append(u"\\end{pspicture}")
    
def quest_rectangle_hypo_angle(exo, cor):
    """on donne un triangle ABC rectangle en C et l'hypotenuse AB et l'angle BAC"""
    A, B, C = geo.choix_points(3)
    nom = shuffle_nom([A, B, C])
    c = 0.2 * random.randint(20, 35)  # longueur AB
    angBAC = 3 * random.randint(7, 23)  # un angle mesurant entre 21° et 69°
    angABC = 90 - angBAC
    # angACB=90
    # Calcul pour tracer
    x_C = (c * tan(angABC)) / (tan(angABC) + tan(angBAC))
    y_C = x_C * tan(angBAC)
    
    exo.append(u"\\item Trace un triangle $%s$ rectangle en $%s$ tel que $%s%s=\\unit[%s]{cm}$ et $\\widehat{%s%s%s}=%s\\degres$.\\par"
               % (nom, C, A, B, decimaux(c), B, A, C, angBAC))
    cor.append(u"\\item Trace un triangle $%s$ rectangle en $%s$ tel que $%s%s=\\unit[%s]{cm}$ et $\\widehat{%s%s%s}=%s\\degres$.\\par"
               % (nom, C, A, B, decimaux(c), B, A, C, angBAC))
# #    cor.append("\\begin{multicols}{2}")
    cor.append(u"Je sais que dans un triangle rectangle, les deux angles aigus sont complémentaires \\\\ \
donc $\widehat{%s%s%s}=90\\degres-%s\\degres=%s\\degres$.\\par" % (B, A, C, angBAC, angABC))
    
    cor.append("\\figureadroite{")
    cor.append(u"\\begin{pspicture}(-0.4,-1)(%.3f,%.3f)" % (c + 0.4, y_C + 1))
    cor.append(u"\\pstTriangle(0,0){%s}(%.3f,0){%s}(%.3f,%.3f){%s}" % (A, c, B, x_C, y_C, C))
    cor.append(u"\\color{enonce}\\pstRightAngle[linecolor=enonce]{%s}{%s}{%s}" % (A, C, B))
    cor.append(u"\\pstLineAB[nodesepB=-1]{%s}{%s}\\pstLineAB[nodesepB=-1]{%s}{%s}" % (A, C, B, C))
    cor.append(cotation((0, 0), (c, 0), decimaux(c), couleur="enonce"))
    cor.append(u"\\color{enonce}\\pstMarkAngle[linecolor=enonce]{%s}{%s}{%s}{%s\\degres}" % (B, A, C, angBAC))
    cor.append(u"\\color{calcul}\\pstMarkAngle[linecolor=calcul]{%s}{%s}{%s}{%s\\degres}" % (C, B, A, angABC))
    cor.append(u"\\end{pspicture}}{")
    cor.append("\\begin{enumerate}")
    cor.append(u"\\item Je trace le segment $[%s%s]$ mesurant $\\unit[%s]{cm}$ ;" % (A, B, decimaux(c)))
    cor.append(u"\\item puis la demi-droite $[%s%s)$ en traçant l'angle~$\widehat{%s%s%s}$ ;" % (A, C, B, A, C))
    cor.append(u"\\item puis la demi-droite $[%s%s)$ en traçant l'angle~$\widehat{%s%s%s}$ ;" % (B, C, A, B, C))
# #    cor.append(u"\\item enfin je vérifie les trois {\\color{enonce}conditions de l'énoncé}.")
    cor.append("\\end{enumerate}\n")
# #    cor.append("\\end{multicols}")
    cor.append("}")
    
def quest_rectangle_hypo_cote(exo, cor):
    """on donne un triangle ABC rectangle en B et l'hypotenuse AC et le coté AB"""
    A, B, C = geo.choix_points(3)
    nom = shuffle_nom([A, B, C])
    c = 0.2 * random.randint(20, 35)  # longueur AB
    b = 0.1 * random.randint(int(10 * (c)) + 1, 100)  # longueur AC
    angABC = 90
    # calcul pour tracer
    angBAC = math.degrees(math.acos(float(c) / float(b)))
    x_C = (c * tan(angABC)) / (tan(angABC) + tan(angBAC))
    y_C = x_C * tan(angBAC)
    
    exo.append(u"\\item Trace un triangle $%s$ rectangle en $%s$ tel que $%s%s=\\unit[%s]{cm}$,  $%s%s=\\unit[%s]{cm}$.\\par"
               % (nom, B, A, B, decimaux(c), A, C, decimaux(b)))
    cor.append(u"\\item Trace un triangle $%s$ rectangle en $%s$ tel que $%s%s=\\unit[%s]{cm}$, $%s%s=\\unit[%s]{cm}$.\\par"
               % (nom, B, A, B, decimaux(c), A, C, decimaux(b)))
# #    cor.append("\\begin{multicols}{2}")
    cor.append("\\figureadroite{")
    cor.append(u"\\begin{pspicture}(-0.4,-1)(%.3f,%.3f)" % (c + 0.4, y_C + 1))
    cor.append(u"\\pstTriangle(0,0){%s}(%.3f,0){%s}(%.3f,%.3f){%s}" % (A, c, B, x_C, y_C, C))
    cor.append(u"\\color{enonce}\\pstRightAngle[linecolor=enonce]{%s}{%s}{%s}" % (C, B, A))
    cor.append(u"\\pstRotation[RotAngle=7,PointSymbol=none,PointName=none]{%s}{%s}[C_1]" % (A, C))
    cor.append(u"\\pstRotation[RotAngle=-7,PointSymbol=none,PointName=none]{%s}{%s}[C_2]" % (A, C))
    cor.append(u"\\pstArcOAB[linecolor=calcul]{%s}{C_2}{C_1}" % (A))
    cor.append(u"\\pstLineAB{%s}{%s}\\pstLineAB[nodesepB=-1]{%s}{%s}" % (A, B, B, C))
    cor.append(cotation((0, 0), (c, 0), decimaux(c), couleur="enonce"))
    cor.append(cotation_h((0, 0), (x_C, y_C), decimaux(b), couleur="enonce"))
    cor.append(u"\\end{pspicture}}{")
    cor.append(u"\\begin{enumerate}")
    cor.append(u"\\item Je trace le segment $[%s%s]$ mesurant $\\unit[%s]{cm}$ ;" % (A, B, decimaux(c)))
    cor.append(u"\\item puis je trace l'angle droit $\\widehat{%s%s%s}$ ;" % (A, B, C))
    cor.append(u"\\item enfin, je reporte au compas la longueur \\mbox{$%s%s=\\unit[%s]{cm}$} à partir de $%s$." % (A, C, decimaux(b), A))
    cor.append("\\end{enumerate}}")
# #    cor.append("\\end{multicols}")


#################################################################################################
#   Les construction sont faites avec [AB] horizontale (ou avec la diagonale [AC] horizontale)
#       D-------C
#      /       /
#     /       /
#    A-------B
#   A est toujours l'origine : A(0,0)
#
#   AB est la longueur AB : type(float) en cm
#   angBAC est la mesure de l'angle BAC : type(int) en degrés
#   x_C,y_C sont les coordonnées cartésiennes du point C
#  les coordonnées polaires sont notées (5 ; 60)
#
###################################################################################################

def exo_quadrilatere(test=False):
    
    exo = ["\\exercice",
         "\\begin{enumerate}"]
    cor = ["\\exercice*",
         "\\begin{enumerate}"]
    cor.append("\\definecolor{enonce}{rgb}{0.11,0.56,0.98}")
    # couleur pour reporter les informations de la consigne
    cor.append("\\definecolor{calcul}{rgb}{0.13,0.54,0.13}")
    # couleur pour reporter des informations déduites par raisonnement ou calcul
    cor.append(u"\\psset{MarkAngleRadius=0.7,PointSymbol=none,dotscale=2}")
    # MarkAngleRadius = rayon de l'arc marquant les angles
    # PointSymbol=none les points ne sont pas tracés
    # dotscale=2, grossit la  croix si PointSymbol=x

    # liste des questions possibles
    questions = [quest_rectangle_diag,
           quest_rectangle_angle,
           quest_rectangle_angle_diag,
           quest_rectangle_diag_angle,
           quest_parallelogramme_CCA,
           quest_parallelogramme_CDA,
           quest_parallelogramme_DDA,
           quest_losange_DD,
           quest_losange_CD,
           quest_losange_CDbis,
           quest_losange_CC,
           carre_diag]

    if test:  # toutes les constructions en test
        for quest in questions:
            quest(exo, cor)
    else:
        # on choisit un parallélogramme, un losange et un rectangle
        questions[random.randrange(4)](exo, cor)
        questions[random.randrange(4, 7)](exo, cor)
        questions[random.randrange(7, 11)](exo, cor)
        # questions[11], le carré n'est jamais proposé
    exo.append("\\end{enumerate}")
    cor.append("\\end{enumerate}")
    return exo, cor

exo_quadrilatere.description = u'Construction de parallélogrammes'

################################################################

####### RECTANGLES #############

def quest_rectangle_diag(exo, cor):
    """on donne un rectangle ABCD avec un côté AB et une diagonale AC"""
    A, B, C, D = geo.choix_points(4)
    nom = shuffle_nom([A, B, C, D])
    L = random.randint(40, 60)  # AB mesure entre 4cm et 7cm, tracé horizontalement
    Diag = 0.1 * random.randint(L + 10, 70)  # +1.1 pour éviter les problèmes d'arrondi
    L = 0.1 * L
    # Calcul pour tracer
    angBAC = math.degrees(math.acos(float(L) / float(Diag)))
    x_C = L
    y_C = x_C * tan(angBAC)
    
    exo.append(u"\\item Trace un rectangle $%s$ tel que $%s%s=\\unit[%s]{cm}$ et $%s%s=\\unit[%s]{cm}$.\\par"
               % (nom, A, B, decimaux(L), A, C, decimaux(Diag)))
    cor.append(u"\\item Trace un rectangle $%s$ tel que $%s%s=\\unit[%s]{cm}$ et $%s%s=\\unit[%s]{cm}$.\\par"
               % (nom, A, B, decimaux(L), A, C, decimaux(Diag)))
    # figure
    cor.append("\\figureadroite{")
    cor.append(u"\\begin{pspicture}(-0.4,-1)(%.3f,%.3f)" % (L + 0.4, y_C + 1))
    cor.append(u"\\pstTriangle(0,0){%s}(%.3f,0){%s}(%.3f,%.3f){%s}" % (A, L, B, x_C, y_C, C))
    cor.append(u"\\pstGeonode[PosAngle=135](0,%.3f){%s}" % (y_C, D))
    # codage
    cor.append(u"\\color{enonce}\\pstRightAngle[linecolor=enonce]{%s}{%s}{%s}" % (D, C, B))
    cor.append(u"\\color{enonce}\\pstRightAngle[linecolor=enonce]{%s}{%s}{%s}" % (B, A, D))
    cor.append(u"\\color{enonce}\\pstRightAngle[linecolor=enonce]{%s}{%s}{%s}" % (C, B, A))
    cor.append(u"\\pstRotation[RotAngle=7,PointSymbol=none,PointName=none]{%s}{%s}[C_1]" % (A, C))
    cor.append(u"\\pstRotation[RotAngle=-7,PointSymbol=none,PointName=none]{%s}{%s}[C_2]" % (A, C))
    cor.append(u"\\pstArcOAB[linecolor=calcul]{%s}{C_2}{C_1}" % (A))
    cor.append(u"\\pstLineAB[nodesepB=-1]{%s}{%s}\\pstLineAB[nodesepB=-1]{%s}{%s}\\pstLineAB{%s}{%s}\\pstLineAB[nodesepB=-1]{%s}{%s}" % (A, D, C, D, A, B, B, C))
    cor.append(cotation((0, 0), (L, 0), decimaux(L), couleur="enonce"))
    cor.append(cotation_h((0, 0), (x_C, y_C), decimaux(Diag), couleur="enonce"))
    cor.append(u"\\end{pspicture}}{")
    # Programme de construction
    cor.append(u"\\begin{enumerate}")
    cor.append(u"\\item Je trace le segment $[%s%s]$ mesurant $\\unit[%s]{cm}$ ;" % (A, B, decimaux(L)))
    cor.append(u"\\item puis je trace l'angle droit $\\widehat{%s%s%s}$ ;" % (A, B, C))
    cor.append(u"\\item je reporte au compas la longueur $%s%s=\\unit[%s]{cm}$ à partir de $%s$ ;" % (A, C, decimaux(Diag), A))
    cor.append(u"\\item je trace enfin les angles droits en $%s$ et en $%s$ pour placer le point $%s$." % (A, C, D))
    cor.append("\\end{enumerate}}")
    

def quest_rectangle_angle(exo, cor):
    """On donne un rectangle ABCD avec le côté AB et l'angle BAC"""
    A, B, C, D = geo.choix_points(4)
    nom = shuffle_nom([A, B, C, D])
    L = random.randint(40, 60)  # AB mesure entre 4cm et 7cm, tracé horizontalement
    angBAC = random.randint(25, 65)
    L = 0.1 * L
    # Calcul pour tracer
    x_C = L
    y_C = x_C * tan(angBAC)
    
    exo.append(u"\\item Trace un rectangle $%s$ tel que $%s%s=\\unit[%s]{cm}$ et $\\widehat{%s%s%s}=%s\\degres$.\\par"
               % (nom, A, B, decimaux(L), B, A, C, angBAC))
    cor.append(u"\\item Trace un rectangle $%s$ tel que $%s%s=\\unit[%s]{cm}$ et $\\widehat{%s%s%s}=%s\\degres$.\\par"
               % (nom, A, B, decimaux(L), B, A, C, angBAC))
    
    cor.append("\\figureadroite{")
    cor.append(u"\\begin{pspicture}(-0.4,-1)(%.3f,%.3f)" % (L + 0.4, y_C + 1))
    cor.append(u"\\pstTriangle(0,0){%s}(%.3f,0){%s}(%.3f,%.3f){%s}" % (A, L, B, x_C, y_C, C))
    cor.append(u"\\pstGeonode[PosAngle=135](0,%.3f){%s}" % (y_C, D))
    cor.append(u"\\color{enonce}\\pstRightAngle[linecolor=enonce]{%s}{%s}{%s}" % (D, C, B))
    cor.append(u"\\color{enonce}\\pstRightAngle[linecolor=enonce]{%s}{%s}{%s}" % (B, A, D))
    cor.append(u"\\color{enonce}\\pstRightAngle[linecolor=enonce]{%s}{%s}{%s}" % (C, B, A))
    cor.append(u"\\pstLineAB[nodesepB=-1]{%s}{%s}\\pstLineAB[nodesepB=-1]{%s}{%s}\\pstLineAB{%s}{%s}\\pstLineAB[nodesepB=-1]{%s}{%s}\\pstLineAB[nodesepB=-1]{%s}{%s}"
               % (A, D, C, D, A, B, B, C, A, C))
    cor.append(cotation((0, 0), (L, 0), decimaux(L), couleur="enonce"))
    cor.append(u"\\color{enonce}\\pstMarkAngle[linecolor=enonce]{%s}{%s}{%s}{%s\\degres}" % (B, A, C, angBAC))
    cor.append(u"\\end{pspicture}}{")
    # Programme de construction
    cor.append(u"\\begin{enumerate}")
    cor.append(u"\\item Je trace le segment $[%s%s]$ mesurant $\\unit[%s]{cm}$ ;" % (A, B, decimaux(L)))
    cor.append(u"\\item puis je trace l'angle droit $\\widehat{%s%s%s}$ ;" % (A, B, C))
    cor.append(u"\\item la demi-droite $[%s%s)$ en mesurant $\\widehat{%s%s%s}=%s\\degres$." % (A, C, B, A, C, angBAC))
    cor.append(u"\\item je trace enfin les angles droit en $%s$ et en $%s$ pour placer le point $%s$." % (A, C, D))
    cor.append("\\end{enumerate}}")

def quest_rectangle_angle_diag(exo, cor):
    """On donne un rectangle ABCD de centre E, la diagonale AC et l'angle AEB"""
    A, B, C, D, E = geo.choix_points(5)
    nom = shuffle_nom([A, B, C, D])
    angAEB = 2 * random.randint(20, 70)
    Diag = 0.2 * random.randint(25, 45)
    # calcul pour tracer
    angBAC = (180 - angAEB) / 2
    L = Diag * cos(angBAC)
    x_C = L
    y_C = x_C * tan(angBAC)
    
    exo.append(u"\\item Trace un rectangle $%s$ de centre $%s$ tel que $%s%s=\\unit[%s]{cm}$ et $\\widehat{%s%s%s}=%s\\degres$.\\par"
               % (nom, E, A, C, decimaux(Diag), A, E, B, angAEB))
    cor.append(u"\\item Trace un rectangle $%s$ de centre $%s$ tel que $%s%s=\\unit[%s]{cm}$ et $\\widehat{%s%s%s}=%s\\degres$.\\par"
               % (nom, E, A, C, decimaux(Diag), A, E, B, angAEB))
# #    cor.append("\\begin{multicols}{2}")
    # Programme de construction
    cor.append("\\figureadroite{")
# #    cor.append("\columnbreak")
    cor.append(u"\\begin{pspicture}(-0.4,-1)(%.3f,%.3f)" % (L + 0.4, y_C + 1))
    cor.append(u"\\pstTriangle(0,0){%s}(%.3f,0){%s}(%.3f,%.3f){%s}" % (A, L, B, x_C, y_C, C))
    cor.append(u"\\pstGeonode[PosAngle={135,0}](0,%.3f){%s}(%.3f,%.3f){%s}" % (y_C, D, x_C / 2.0, y_C / 2.0, E))
    cor.append(u"\\pstLineAB{%s}{%s}" % (C, D))
    cor.append(u"\\pstLineAB{%s}{%s}" % (A, D))
    cor.append(u"\\pstLineAB[nodesep=-1]{%s}{%s}" % (B, D))
    # codage
    cor.append(u"\\pstLineAB{%s}{%s}\\lput{:U}{\\psset{linecolor=calcul}\\MarkHashh}" % (E, A))
    cor.append(u"\\pstLineAB{%s}{%s}\\lput{:U}{\\psset{linecolor=calcul}\\MarkHashh}" % (E, B))
    cor.append(u"\\pstLineAB{%s}{%s}\\lput{:U}{\\psset{linecolor=calcul}\\MarkHashh}" % (E, C))
    cor.append(u"\\pstLineAB{%s}{%s}\\lput{:U}{\\psset{linecolor=calcul}\\MarkHashh}" % (E, D))
    cor.append(u"\\psarc[linecolor=calcul](%.3f,%.3f){%s}{%s}{%s} " % (x_C / 2.0, y_C / 2.0, Diag / 2, angBAC - 7, angBAC + 7))
    cor.append(u"\\psarc[linecolor=calcul](%.3f,%.3f){%s}{%s}{%s} " % (x_C / 2.0, y_C / 2.0, Diag / 2, 180 - angBAC - 7, 180 - angBAC + 7))
    cor.append(u"\\psarc[linecolor=calcul](%.3f,%.3f){%s}{%s}{%s} " % (x_C / 2.0, y_C / 2.0, Diag / 2, -angBAC - 7, -angBAC + 7))
    cor.append(u"\\psarc[linecolor=calcul](%.3f,%.3f){%s}{%s}{%s} " % (x_C / 2.0, y_C / 2.0, Diag / 2, 180 + angBAC - 7, 180 + angBAC + 7))
    cor.append("\\pcline[linestyle=none](0,0)(%.3f,%.3f)\\aput*{:U}{\\color{enonce}\\unit[%s]{cm}}" % (L, y_C, decimaux(Diag)))
    cor.append(u"\\color{enonce}\\pstMarkAngle[linecolor=enonce]{%s}{%s}{%s}{%s\\degres}" % (A, E, B, angAEB))
    cor.append(u"\\end{pspicture}}{")
    cor.append(u"\\begin{enumerate}")
    cor.append(u"\\item Je trace le segment $[%s%s]$ mesurant $\\unit[%s]{cm}$ ;" % (A, C, decimaux(Diag)))
    cor.append(u"\\item le centre du rectangle est le milieu des diagonales donc $%s$ est le milieu de $[%s%s]$ ;" % (E, A, C))
    cor.append(u"\\item je trace la diagonale $(%s%s)$ passant par $%s$ en mesurant \\mbox{$\\widehat{%s%s%s}=%s\\degres$} ;"
               % (B, D, E, A, E, B, angAEB))
    cor.append(u"\\item Comme les diagonales du rectangle sont de même longueur, je reporte les longueurs $%s%s=%s%s=\\unit[%s]{cm}$."
               % (E, D, E, B, decimaux(Diag / 2)))
# #    cor.append(u"\\item je trace enfin les angles droits en $%s$ et en $%s$ pour palcer le point $%s$."%(A,C,D))
    cor.append("\\end{enumerate}}")
# #    cor.append("\\end{multicols}")

def quest_rectangle_diag_angle(exo, cor):
    """On donne un rectangle ABCD la diagonale AC et l'angle BAC"""
    A, B, C, D = geo.choix_points(4)
    nom = shuffle_nom([A, B, C, D])
    angBAC = random.randint(25, 65)
    Diag = 0.1 * random.randint(50, 80)
    # Calcul
    L = Diag * cos(angBAC)
    x_C = L
    y_C = x_C * tan(angBAC)
    
    exo.append(u"\\item Trace un rectangle $%s$ tel que $%s%s=\\unit[%s]{cm}$ et $\\widehat{%s%s%s}=%s\\degres$.\\par"
               % (nom, A, C, decimaux(Diag), B, A, C, angBAC))
    cor.append(u"\\item Trace un rectangle $%s$ tel que $%s%s=\\unit[%s]{cm}$ et $\\widehat{%s%s%s}=%s\\degres$.\\par"
               % (nom, A, C, decimaux(Diag), B, A, C, angBAC))
    
# #    cor.append("\\begin{multicols}{2}")
    cor.append("\\figureadroite{")
# #    cor.append("\columnbreak")
    # figure
    cor.append(u"\\begin{pspicture}(-0.4,-1)(%.3f,%.3f)" % (L + 0.4, y_C + 1))
    cor.append(u"\\pstTriangle(0,0){%s}(%.3f,0){%s}(%.3f,%.3f){%s}" % (A, L, B, x_C, y_C, C))
    cor.append(u"\\pstGeonode[PosAngle=135](0,%.3f){%s}" % (y_C, D))
    # codage
    cor.append(u"\\color{enonce}\\pstRightAngle[linecolor=enonce]{%s}{%s}{%s}" % (D, C, B))
    cor.append(u"\\color{enonce}\\pstRightAngle[linecolor=enonce]{%s}{%s}{%s}" % (B, A, D))
    cor.append(u"\\color{enonce}\\pstRightAngle[linecolor=enonce]{%s}{%s}{%s}" % (C, B, A))
    cor.append(u"\\pstLineAB[nodesepB=-1]{%s}{%s}\\pstLineAB[nodesepB=-1]{%s}{%s}\\pstLineAB[nodesepB=-1]{%s}{%s}\\pstLineAB[nodesep=-1]{%s}{%s}"
               % (A, D, C, D, A, B, B, C))
    cor.append(cotation_h((0, 0), (L, y_C), decimaux(Diag), couleur="enonce"))
    cor.append(u"\\color{enonce}\\pstMarkAngle[linecolor=enonce]{%s}{%s}{%s}{%s\\degres}" % (B, A, C, angBAC))
    cor.append(u"\\end{pspicture}}{")
    # Programme de construction
    cor.append(u"\\begin{enumerate}")
    cor.append(u"\\item Je trace le segment $[%s%s]$ mesurant $\\unit[%s]{cm}$ ;" % (A, C, decimaux(Diag)))
    cor.append(u"\\item la demi-droite $[%s%s)$ en mesurant \\mbox{$\\widehat{%s%s%s}=%s\\degres$} ;" % (A, B, B, A, C, angBAC))
    cor.append(u"\\item puis la perpendiculaire à $[%s%s)$ passant par~$%s$ ;" % (A, B, C))
    cor.append(u"\\item je trace enfin les angles droits en $%s$ et en $%s$ pour placer le point~$%s$." % (A, C, D))
    cor.append("\\end{enumerate}}")
# #    cor.append("\\end{multicols}")

################## PARALLÉLOGRAMMES QUELCONQUES ###########################
    
def quest_parallelogramme_CCA(exo, cor):
    """On donne un parallélogramme avec la longueur de deux côtés et un angle."""
    # 3 choix d'angle : CC ou un autre angle CC ou un angle Côté Diagonale
    A, B, C, D = geo.choix_points(4)
    nom = shuffle_nom([A, B, C, D])
    AB = 0.1 * random.randint(40, 60)  # AB mesure entre 4cm et 7cm, tracé horizontalement
    AD = 0.1 * random.randint(40, 60)  # AD mesure entre 4cm et 7cm, tracé horizontalement
    angBAD = random.randint(25, 65)
    # Pour tracer
    x_C = AB + AD * cos(angBAD)
    y_C = AD * sin(angBAD)
    
    exo.append(u"\\item Trace un parallélogramme $%s$ tel que $%s%s=\\unit[%s]{cm}$, $%s%s=\\unit[%s]{cm}$ et $\\widehat{%s%s%s}=%s\\degres$.\\par"
               % (nom, A, B, decimaux(AB), D, A, decimaux(AD), B, A, D, angBAD))
    cor.append(u"\\item Trace un parallélogramme $%s$ tel que $%s%s=\\unit[%s]{cm}$, $%s%s=\\unit[%s]{cm}$ et $\\widehat{%s%s%s}=%s\\degres$.\\par"
               % (nom, A, B, decimaux(AB), D, A, decimaux(AD), B, A, D, angBAD))
    cor.append(u"\\begin{enumerate}")
    cor.append(u"\\item Je trace le segment $[%s%s]$ mesurant $\\unit[%s]{cm}$ ;" % (A, B, decimaux(AB)))
    cor.append(u"\\item je mesure l'angle  $\\widehat{%s%s%s}=%s\\degres$ puis je place le point~$%s$ ;" % (B, A, D, angBAD, D))
    cor.append(u"\\item enfin je reporte les longueurs $%s%s=%s%s$ et $%s%s=%s%s$ pour place le point~$%s$."
               % (D, C, A, B, B, C, A, D, C))
    cor.append("\\end{enumerate}\n")
    cor.append(u"\\begin{pspicture}(-0.4,-1)(%.3f,%.3f)" % (max(AB, x_C) + 0.4, y_C + 1))
    cor.append(u"\\pstGeonode[PosAngle={-135,-45,45,135}](0,0){%s}(%.3f,0){%s}(%.3f,%.3f){%s}(%.3f;%.3f){%s}" % (A, AB, B, x_C, y_C, C, AD, angBAD, D))
    cor.append(u"\\pstLineAB[nodesepB=-1]{%s}{%s}\\pstLineAB{%s}{%s}\\pstLineAB{%s}{%s}\\pstLineAB{%s}{%s}"
               % (A, D, C, D, A, B, B, C))
    cor.append(u"\\pstRotation[RotAngle=7,PointSymbol=none,PointName=none]{%s}{%s}[C_1]" % (D, C))
    cor.append(u"\\pstRotation[RotAngle=-7,PointSymbol=none,PointName=none]{%s}{%s}[C_2]" % (D, C))
    cor.append(u"\\pstArcOAB[linecolor=calcul]{%s}{C_2}{C_1}" % (D))
    cor.append(u"\\pstRotation[RotAngle=7,PointSymbol=none,PointName=none]{%s}{%s}[D_1]" % (A, D))
    cor.append(u"\\pstRotation[RotAngle=-7,PointSymbol=none,PointName=none]{%s}{%s}[D_2]" % (A, D))
    cor.append(u"\\pstArcOAB[linecolor=calcul]{%s}{D_2}{D_1}" % (A))
    cor.append(u"\\pstRotation[RotAngle=7,PointSymbol=none,PointName=none]{%s}{%s}[C_3]" % (B, C))
    cor.append(u"\\pstRotation[RotAngle=-7,PointSymbol=none,PointName=none]{%s}{%s}[C_4]" % (B, C))
    cor.append(u"\\pstArcOAB[linecolor=calcul]{%s}{C_4}{C_3}" % (B))
    cor.append(cotation_h((0, 0), (x_C - AB, y_C), decimaux(AD), couleur="enonce"))
    cor.append(cotation((0, 0), (AB, 0), decimaux(AB), couleur="enonce"))
    cor.append(u"\\color{enonce}\\pstMarkAngle[linecolor=enonce]{%s}{%s}{%s}{%s\\degres}" % (B, A, D, angBAD))
    cor.append(u"\\pstLineAB[linestyle=none]{%s}{%s}\\lput{:U}{\\psset{linecolor=calcul}\\MarkHashh}" % (A, D))
    cor.append(u"\\pstLineAB[linestyle=none]{%s}{%s}\\lput{:U}{\\psset{linecolor=calcul}\\MarkHashh}" % (B, C))
    cor.append(u"\\pstLineAB[linestyle=none]{%s}{%s}\\lput{:U}{\\psset{linecolor=calcul}\\MarkHash}" % (A, B))
    cor.append(u"\\pstLineAB[linestyle=none]{%s}{%s}\\lput{:U}{\\psset{linecolor=calcul}\\MarkHash}" % (D, C))
    cor.append(u"\\end{pspicture}")

def quest_parallelogramme_CDA(exo, cor):
    """On donne un parallélogramme avec la longueur d'un côté et une diagonale et l'angle entre ces deux segments"""
    
    A, B, C, D = geo.choix_points(4)
    nom = shuffle_nom([A, B, C, D])
    AB = 0.1 * random.randint(40, 60)  # AB mesure entre 4cm et 7cm, tracé horizontalement
    AC = 0.1 * random.randint(40, 70)  # AC mesure entre 4cm et 7cm, tracé horizontalement
    angBAC = random.randint(25, 65)
    # Calcul pour tracer
    x_C = round(AC * cos(angBAC), 4)  # round() évite une écriture scientifique si x_D=2.4e-15, non reconnue par PSTricks
    y_D = y_C = AC * sin(angBAC)
    x_D = round(x_C - AB, 4)
    
    exo.append(u"\\item Trace un parallélogramme $%s$ tel que $%s%s=\\unit[%s]{cm}$, $%s%s=\\unit[%s]{cm}$ et $\\widehat{%s%s%s}=%s\\degres$.\\par"
               % (nom, A, B, decimaux(AB), C, A, decimaux(AC), B, A, C, angBAC))
    cor.append(u"\\item Trace un parallélogramme $%s$ tel que $%s%s=\\unit[%s]{cm}$, $%s%s=\\unit[%s]{cm}$ et $\\widehat{%s%s%s}=%s\\degres$.\\par"
               % (nom, A, B, decimaux(AB), C, A, decimaux(AC), B, A, C, angBAC))
    # Programme de construction
    cor.append(u"\\begin{enumerate}")
    cor.append(u"\\item Je trace le segment $[%s%s]$ mesurant $\\unit[%s]{cm}$ ;" % (A, B, decimaux(AB)))
    cor.append(u"\\item je trace la demi-droite $[%s%s)$ en mesurant $\\widehat{%s%s%s}=%s\\degres$ ;" % (A, C, B, A, C, angBAC))
    cor.append(u"\\item je place le point $%s$ en mesurant $%s%s=\\unit[%s]{cm}$ ;" % (C, A, C, decimaux(AC)))
    cor.append(u"\\item je construis le point $%s$ en reportant au compas $%s%s=%s%s$ et $%s%s=%s%s$."
               % (D, C, D, B, A, A, D, B, C))
    cor.append("\\end{enumerate}\n")
    # Figure
    cor.append(u"\\begin{pspicture}(%.3f,-1)(%.3f,%.3f)" % (min(0, x_C - AB) - 0.4, max(AB, x_C) + 0.4, y_C + 1))
    cor.append(u"\\pstGeonode[PosAngle={-135,-45,45,135}](0,0){%s}(%.3f,0){%s}(%.3f,%.3f){%s}(%.3f,%.3f){%s}" % (A, AB, B, x_C, y_C, C, x_D, y_D, D))
    cor.append(u"\\pstLineAB{%s}{%s}\\pstLineAB{%s}{%s}\\pstLineAB{%s}{%s}\\pstLineAB{%s}{%s}\\pstLineAB[nodesepB=-1]{%s}{%s}"
               % (A, D, C, D, A, B, B, C, A, C))
    # Construction
    cor.append(u"\\pstRotation[RotAngle=7,PointSymbol=none,PointName=none]{%s}{%s}[C_1]" % (A, C))
    cor.append(u"\\pstRotation[RotAngle=-7,PointSymbol=none,PointName=none]{%s}{%s}[C_2]" % (A, C))
    cor.append(u"\\pstArcOAB[linecolor=calcul]{%s}{C_2}{C_1}" % (A))
    cor.append(u"\\pstRotation[RotAngle=7,PointSymbol=none,PointName=none]{%s}{%s}[D_1]" % (A, D))
    cor.append(u"\\pstRotation[RotAngle=-7,PointSymbol=none,PointName=none]{%s}{%s}[D_2]" % (A, D))
    cor.append(u"\\pstArcOAB[linecolor=calcul]{%s}{D_2}{D_1}" % (A))
    cor.append(u"\\pstRotation[RotAngle=7,PointSymbol=none,PointName=none]{%s}{%s}[D_3]" % (C, D))
    cor.append(u"\\pstRotation[RotAngle=-7,PointSymbol=none,PointName=none]{%s}{%s}[D_4]" % (C, D))
    cor.append(u"\\pstArcOAB[linecolor=calcul]{%s}{D_4}{D_3}" % (C))
    # Codage
    cor.append(cotation_h((0, 0), (x_C, y_C), decimaux(AC), couleur="enonce"))
    cor.append(cotation((0, 0), (AB, 0), decimaux(AB), couleur="enonce"))
    cor.append(u"\\color{enonce}\\pstMarkAngle[linecolor=enonce]{%s}{%s}{%s}{%s\\degres}" % (B, A, C, angBAC))
    cor.append(u"\\pstLineAB[linestyle=none]{%s}{%s}\\lput{:U}{\\psset{linecolor=calcul}\\MarkHashh}" % (A, D))
    cor.append(u"\\pstLineAB[linestyle=none]{%s}{%s}\\lput{:U}{\\psset{linecolor=calcul}\\MarkHashh}" % (B, C))
    cor.append(u"\\pstLineAB[linestyle=none]{%s}{%s}\\lput{:U}{\\psset{linecolor=calcul}\\MarkHash}" % (A, B))
    cor.append(u"\\pstLineAB[linestyle=none]{%s}{%s}\\lput{:U}{\\psset{linecolor=calcul}\\MarkHash}" % (D, C))
    cor.append(u"\\end{pspicture}")

def quest_parallelogramme_DDA(exo, cor):
    """On donne un parallélogramme avec la longueur des deux diagonales et l'angle entre les diagonales"""
    # choix d'angle : on pourrait donner l'angle BAC
    # diagonale ou demi-diagonale
    A, B, C, D, E = geo.choix_points(5)
    nom = shuffle_nom([A, B, C, D])
    BD = 0.2 * random.randint(20, 40)  # AB mesure entre 4cm et 8cm, tracé horizontalement
    AC = 0.2 * random.randint(20, 40)  # AC mesure entre 4cm et 8cm, tracé horizontalement
    angAEB = random.randint(35, 145)
    AE = AC / 2
    BE = BD / 2
    
    # calcul pour tracer
    AB = math.sqrt(AE ** 2 + BE ** 2 - 2 * AE * BE * cos(angAEB))
    angBAC = math.degrees(math.asin(BE * sin(angAEB) / AB))
    x_C = AC * cos(angBAC)
    y_D = y_C = round(AC * sin(angBAC), 4)
    x_D = round(x_C - AB, 4)
    
    exo.append(u"\\item Trace un parallélogramme $%s$ de centre $%s$ tel que $%s%s=\\unit[%s]{cm}$, $%s%s=\\unit[%s]{cm}$ et $\\widehat{%s%s%s}=%s\\degres$.\\par"
               % (nom, E, A, C, decimaux(AC), B, D, decimaux(BD), A, E, B, angAEB))
    cor.append(u"\\item Trace un parallélogramme $%s$ de centre $%s$ tel que $%s%s=\\unit[%s]{cm}$, $%s%s=\\unit[%s]{cm}$ et $\\widehat{%s%s%s}=%s\\degres$.\\par"
               % (nom, E, A, C, decimaux(AC), B, D, decimaux(BD), A, E, B, angAEB))
    cor.append(u"\\begin{enumerate}")
    cor.append(u"\\item Je trace le segment $[%s%s]$ mesurant $\\unit[%s]{cm}$ ;" % (A, C, decimaux(AC)))
    cor.append(u"\\item Dans un parallélogramme les diagonales se coupent en leur milieu donc $%s%s=%s%s=\\unit[%s]{cm}$ et $%s%s=%s%s=\\unit[%s]{cm}$ ;"
               % (A, E, C, E, decimaux(AC / 2), B, E, E, D, decimaux(BD / 2)))
    cor.append("\\end{enumerate}\n")
    cor.append(u"\\begin{pspicture}(%.3f,-1)(%.3f,%.3f)" % (min(0, x_D) - 0.4, max(AB, x_C) + 0.4, y_C + 1))
    cor.append(u"\\pstGeonode[PosAngle={-135,-45,45,135,%s}](0,0){%s}(%.3f,0){%s}(%.3f,%.3f){%s}(%.3f,%.3f){%s}(%.3f,%.3f){%s}"
               % ([round(angBAC - (180 - angAEB) / 2), round(angBAC + (angAEB) / 2)][angAEB > 90], A, AB, B, x_C, y_C, C, x_D, y_D, D, x_C / 2, y_C / 2, E))
    cor.append(u"\\pstLineAB{%s}{%s}\\lput{:U}{\\psset{linecolor=calcul}\\MarkHashh}" % (A, E))
    cor.append(u"\\pstLineAB{%s}{%s}\\lput{:U}{\\psset{linecolor=calcul}\\MarkHashh}" % (C, E))
    cor.append(u"\\pstLineAB{%s}{%s}\\lput{:U}{\\psset{linecolor=calcul}\\MarkCros}" % (B, E))
    cor.append(u"\\pstLineAB{%s}{%s}\\lput{:U}{\\psset{linecolor=calcul}\\MarkCros}" % (D, E))
    cor.append(u"\\pstLineAB{%s}{%s}\\pstLineAB{%s}{%s}\\pstLineAB{%s}{%s}\\pstLineAB{%s}{%s}"
               % (A, D, C, D, A, B, B, C))
    cor.append(cotation_h((0, 0), (x_C / 2, y_C / 2), decimaux(AC / 2), couleur="enonce"))
    cor.append(cotation_h((x_C / 2, y_C / 2), (AB, 0), decimaux(BD / 2), couleur="enonce"))
    cor.append(u"\\color{enonce}\\pstMarkAngle[linecolor=enonce]{%s}{%s}{%s}{%s\\degres}" % (A, E, B, angAEB))
    cor.append(u"\\end{pspicture}")

###################### LOSANGES ########################
    
def quest_losange_DD(exo, cor):
    """On donne un losange avec la longueur des deux diagonales"""
    # diagonale ou demi-diagonale
    A, B, C, D, E = geo.choix_points(5)
    nom = shuffle_nom([A, B, C, D])
    BD = 0.2 * random.randint(15, 25)  # AB mesure entre 4cm et 8cm, tracé horizontalement
    AC = 0.2 * random.randint(20, 40)  # AC mesure entre 4cm et 8cm, tracé horizontalement
    
    exo.append(u"\\item Trace un losange $%s$  tel que $%s%s=\\unit[%s]{cm}$ et $%s%s=\\unit[%s]{cm}$.\\par"
               % (nom, A, C, decimaux(AC), B, D, decimaux(BD)))
    cor.append(u"\\item Trace un losange $%s$  tel que $%s%s=\\unit[%s]{cm}$ et $%s%s=\\unit[%s]{cm}$.\\par"
               % (nom, A, C, decimaux(AC), B, D, decimaux(BD)))
    
    cor.append(u"Je note $%s$ le centre du losange.\\par" % E)
    
    cor.append("\\figureadroite{")
    cor.append(u"\\begin{pspicture}(%.3f,%.3f)(%.3f,%.3f)" % (-BD / 2 - 0.7, -AC / 2 - 0.4, BD / 2 + 0.4, AC / 2 + 0.4))
    cor.append(u"\\pstGeonode[PosAngle={-90,0,90,180}](0,%.3f){%s}(%.3f,0){%s}(0,%.3f){%s}(%.3f,0){%s}"
               % (-AC / 2, A, BD / 2, B, AC / 2, C, -BD / 2, D))
    cor.append("\\pstGeonode[PosAngle=-45](0,0){%s}" % E)
    
    cor.append(u"\\pstLineAB{%s}{%s}\\lput{:U}{\\psset{linecolor=calcul}\\MarkCross}" % (A, E))
    cor.append(u"\\pstLineAB{%s}{%s}\\lput{:U}{\\psset{linecolor=calcul}\\MarkCross}" % (C, E))
    cor.append(u"\\pstLineAB{%s}{%s}\\lput{:U}{\\psset{linecolor=calcul}\\MarkCros}" % (B, E))
    cor.append(u"\\pstLineAB{%s}{%s}\\lput{:U}{\\psset{linecolor=calcul}\\MarkCros}" % (D, E))
    cor.append(u"\\pstLineAB{%s}{%s}\\lput{:U}{\\psset{linecolor=enonce}\\MarkHashh}" % (A, B))
    cor.append(u"\\pstLineAB{%s}{%s}\\lput{:U}{\\psset{linecolor=enonce}\\MarkHashh}" % (C, D))
    cor.append(u"\\pstLineAB{%s}{%s}\\lput{:U}{\\psset{linecolor=enonce}\\MarkHashh}" % (B, C))
    cor.append(u"\\pstLineAB{%s}{%s}\\lput{:U}{\\psset{linecolor=enonce}\\MarkHashh}" % (D, A))
    cor.append("\\pstRightAngle[linecolor=calcul]{%s}{%s}{%s}" % (B, E, C))
    cor.append(cotation_h((-BD / 2, 0), (0, 0), decimaux(BD / 2), couleur="enonce"))
    cor.append(cotation_h((0, -AC / 2), (0, 0), decimaux(AC / 2), couleur="enonce"))
    cor.append(u"\\end{pspicture}}{")
    cor.append(u"Les diagonales du losange se coupent perpendiculairement en leur milieu~$%s$ ;  on a donc :" % E)
    cor.append(u"\\begin{enumerate}")
    cor.append(u"\\item $%s%s=%s%s=\\unit[%s]{cm}$ \\item $%s%s=%s%s=\\unit[%s]{cm}$ ;"
               % (A, E, C, E, decimaux(AC / 2), B, E, E, D, decimaux(BD / 2)))
    cor.append(u"\\item $(%s%s)\\perp(%s%s)$." % (A, C, B, D))
    cor.append("\\end{enumerate}}\n")

def quest_losange_CC(exo, cor):
    """On donne un losange avec la longueur d'un côté et un angle entre côtés"""
    # diagonale ou demi-diagonale
    A, B, C, D = geo.choix_points(4)
    nom = shuffle_nom([A, B, C, D])
    AB = 0.2 * random.randint(15, 25)  # AB mesure entre 4cm et 8cm, tracé horizontalement
    angBAD = random.randint(30, 150)
    # Calcul pour tracer
    x_D = AB * cos(angBAD)
    y_D = y_C = AB * sin(angBAD)
    x_C = x_D + AB
    
    exo.append(u"\\item Trace un losange $%s$  tel que $%s%s=\\unit[%s]{cm}$ et $\\widehat{%s%s%s}=%s\\degres$.\\par"
               % (nom, A, B, decimaux(AB), B, A, D, angBAD))
    cor.append(u"\\item Trace un losange $%s$  tel que $%s%s=\\unit[%s]{cm}$ et $\\widehat{%s%s%s}=%s\\degres$.\\par"
               % (nom, A, B, decimaux(AB), B, A, D, angBAD))
    
    cor.append(u"Les quatre côtés du losange sont de même longueur donc $%s%s=%s%s=%s%s=%s%s=\\unit[%s]{cm}$ ;" % (A, B, B, C, C, D, D, A, decimaux(AB)))
    cor.append(u"\\begin{enumerate}")
    cor.append(u"\\item On trace le côté $[%s%s]$ puis on mesure l'angle $\\widehat{%s%s%s}=%s\\degres$ ;" % (A, B, B, A, D, angBAD))
    cor.append(u"\\item ensuite on reporte au compas les longueurs $%s%s$ et $%s%s$ pour construire le point $%s$." % (C, D, B, C, C))
    cor.append("\\end{enumerate}\n")
    cor.append(u"\\begin{pspicture}(%.3f,%.3f)(%.3f,%.3f)" % (min(0, x_D) - 0.4, 0 - 0.4, max(AB, x_C), y_D + 0.4))
    cor.append(u"\\pstGeonode[PosAngle={%s,%s,%s,%s}](0,0){%s}(%.3f,0){%s}(%.3f,%.3f){%s}(%.3f,%.3f){%s}"
               % (angBAD / 2 - 180, angBAD / 2 - 90, angBAD / 2, angBAD / 2 + 90, A, AB, B, x_C, y_C, C, x_D, y_D, D))
    
    cor.append(u"\\pstLineAB{%s}{%s}\\lput{:U}{\\psset{linecolor=enonce}\\MarkHashh}" % (A, B))
    cor.append(u"\\pstLineAB{%s}{%s}\\lput{:U}{\\psset{linecolor=enonce}\\MarkHashh}" % (C, D))
    cor.append(u"\\pstLineAB{%s}{%s}\\lput{:U}{\\psset{linecolor=enonce}\\MarkHashh}" % (B, C))
    cor.append(u"\\pstLineAB{%s}{%s}\\lput{:U}{\\psset{linecolor=enonce}\\MarkHashh}" % (D, A))
    
    cor.append(u"\\pstRotation[RotAngle=7,PointSymbol=none,PointName=none]{%s}{%s}[C_1]" % (D, C))
    cor.append(u"\\pstRotation[RotAngle=-7,PointSymbol=none,PointName=none]{%s}{%s}[C_2]" % (D, C))
    cor.append(u"\\pstArcOAB[linecolor=calcul]{%s}{C_2}{C_1}" % (D))
    cor.append(u"\\pstRotation[RotAngle=7,PointSymbol=none,PointName=none]{%s}{%s}[C_3]" % (B, C))
    cor.append(u"\\pstRotation[RotAngle=-7,PointSymbol=none,PointName=none]{%s}{%s}[C_4]" % (B, C))
    cor.append(u"\\pstArcOAB[linecolor=calcul]{%s}{C_4}{C_3}" % (B))
    cor.append(cotation((0, 0), (AB, 0), decimaux(AB), couleur="enonce"))
    cor.append(u"\\color{enonce}\\pstMarkAngle[linecolor=enonce]{%s}{%s}{%s}{%s\\degres}" % (B, A, D, angBAD))
    cor.append(u"\\end{pspicture}")
    
def quest_losange_CD(exo, cor):
    """On donne un losange avec la longueur d'un côté et la mesure d'un angle entre un côté et une diagonale"""
    
    A, B, C, D = geo.choix_points(4)
    nom = shuffle_nom([A, B, C, D])
    AC = 0.1 * random.randint(40, 60)  # AB mesure entre 4cm et 7cm, tracé horizontalement
    angBAC = random.randint(25, 75)
    # Calcul pour tracer
    x_D = AC / 2
    y_D = AC / 2 * tan(angBAC)
    
    exo.append(u"\\item Trace un losange $%s$ tel que $%s%s=\\unit[%s]{cm}$ et $\\widehat{%s%s%s}=%s\\degres$.\\par"
               % (nom, A, C, decimaux(AC), B, A, C, angBAC))
    cor.append(u"\\item Trace un losange $%s$ tel que $%s%s=\\unit[%s]{cm}$ et $\\widehat{%s%s%s}=%s\\degres$.\\par"
               % (nom, A, C, decimaux(AC), B, A, C, angBAC))
    # Rédaction
    cor.append(u" Comme $%s$ est un losange, je sais que $\\widehat{%s%s%s}=\\widehat{%s%s%s}=\\widehat{%s%s%s}=\\widehat{%s%s%s}=%s\\degres$."
               % (nom, B, A, C, A, C, B, A, C, D, C, A, D, angBAC))
    # Programme de construction
    cor.append(u"\\begin{enumerate}")
    cor.append(u"\\item Je trace le segment $[%s%s]$ mesurant $\\unit[%s]{cm}$ ;" % (A, C, decimaux(AC)))
    cor.append(u"\\item je trace $\\widehat{%s%s%s}$ et $\\widehat{%s%s%s}$ pour construire le point $%s$ ;" % (B, A, C, A, C, B, B))
    cor.append(u"\\item je trace $\\widehat{%s%s%s}$ et $\\widehat{%s%s%s}$ pour construire le point $%s$ ;" % (A, C, D, C, A, D, D))
    cor.append("\\end{enumerate}\n")
    cor.append(u"\\begin{pspicture}(-0.4,%.3f)(%.3f,%.3f)" % (-y_D - 1, AC + 0.4, y_D + 1))
    # figure
    cor.append(u"\\pstGeonode[PosAngle={-180,0,90,-90}](0,0){%s}(%.3f,0){%s}(%.3f,%.3f){%s}(%.3f,%.3f){%s}" % (A, AC, C, x_D, y_D, D, x_D, -y_D, B))
    cor.append(u"\\pstLineAB[nodesepB=-1]{%s}{%s}\\lput{:U}{\\psset{linecolor=enonce}\\MarkHashh}" % (A, B))
    cor.append(u"\\pstLineAB[nodesepB=-1]{%s}{%s}\\lput{:U}{\\psset{linecolor=enonce}\\MarkHashh}" % (C, D))
    cor.append(u"\\pstLineAB[nodesepA=-1]{%s}{%s}\\lput{:U}{\\psset{linecolor=enonce}\\MarkHashh}" % (B, C))
    cor.append(u"\\pstLineAB[nodesepA=-1]{%s}{%s}\\lput{:U}{\\psset{linecolor=enonce}\\MarkHashh}" % (D, A))
    cor.append(u"\\pstLineAB{%s}{%s}" % (A, C))
    cor.append(cotation_h((0, 0), (AC, 0), decimaux(AC), couleur="enonce"))
    cor.append(u"\\color{enonce}\\pstMarkAngle[linecolor=enonce,Mark=MarkHash]{%s}{%s}{%s}{%s\\degres}" % (B, A, C, angBAC))
    cor.append(u"\\color{enonce}\\pstMarkAngle[linecolor=calcul,Mark=MarkHash]{%s}{%s}{%s}{}" % (C, A, D))
    cor.append(u"\\color{enonce}\\pstMarkAngle[linecolor=calcul,Mark=MarkHash]{%s}{%s}{%s}{}" % (D, C, A))
    cor.append(u"\\color{enonce}\\pstMarkAngle[linecolor=calcul,Mark=MarkHash]{%s}{%s}{%s}{}" % (A, C, B))
    cor.append(u"\\end{pspicture}")

def quest_losange_CDbis(exo, cor):
    """On donne un losange avec la longueur d'un côté et la mesure d'un angle entre un côté et une diagonale"""
    
    A, B, C, D = geo.choix_points(4)
    nom = shuffle_nom([A, B, C, D])
    AC = 0.1 * random.randint(40, 60)  # AB mesure entre 4cm et 7cm, tracé horizontalement
    angCDA = 2 * random.randint(15, 70)
    # Calcul pour tracer
    angCAD = (180 - angCDA) / 2
    x_D = AC / 2
    y_D = AC / 2 * tan(angCAD)
    
    exo.append(u"\\item Trace un losange $%s$ tel que $%s%s=\\unit[%s]{cm}$ et $\\widehat{%s%s%s}=%s\\degres$.\\par"
               % (nom, A, C, decimaux(AC), C, D, A, angCDA))
    cor.append(u"\\item Trace un losange $%s$ tel que $%s%s=\\unit[%s]{cm}$ et $\\widehat{%s%s%s}=%s\\degres$.\\par"
               % (nom, A, C, decimaux(AC), C, D, A, angCDA))

    # Rédaction des calculs
    cor.append(u"Les quatre côtés du losange sont de même longueur donc $%s%s=%s%s=%s%s=%s%s$.\\par" % (A, B, B, C, C, D, D, A))
    cor.append(u"Ainsi, le triangle $%s%s%s$ est isocèle en $%s$ et je peux calculer la mesure des angles $\\widehat{%s%s%s}=\\widehat{%s%s%s}$.\\par"
               % (A, C, D, A, A, C, D, C, A, D))
    cor.append(u"Dans un triangle, la somme des angles du triangle est égale à 180\\degres\\\\")
    cor.append(u"donc $\\widehat{%s%s%s}=\\widehat{%s%s%s}=(180\\degres-%s)\\div2=%s\\degres$" % (A, C, D, C, A, D, angCDA, angCAD))
    # Programme de construction
    cor.append(u"\\begin{enumerate}")
    cor.append(u"\\item Je trace le segment $[%s%s]$ mesurant $\\unit[%s]{cm}$ ;" % (A, C, decimaux(AC)))
    cor.append(u"\\item je trace $\\widehat{%s%s%s}$ et $\\widehat{%s%s%s}$ pour construire le point $%s$ ;" % (B, A, C, A, C, B, B))
    cor.append(u"\\item je trace $\\widehat{%s%s%s}$ et $\\widehat{%s%s%s}$ pour construire le point $%s$ ;" % (A, C, D, C, A, D, D))
    cor.append("\\end{enumerate}\n")
    
    cor.append(u"\\begin{pspicture}(-0.4,%.3f)(%.3f,%.3f)" % (-y_D - 1, AC + 0.4, y_D + 1))
    # Figure
    cor.append(u"\\pstGeonode[PosAngle={-180,0,90,-90}](0,0){%s}(%.3f,0){%s}(%.3f,%.3f){%s}(%.3f,%.3f){%s}" % (A, AC, C, x_D, y_D, D, x_D, -y_D, B))
    cor.append(u"\\pstLineAB{%s}{%s}" % (A, C))
    cor.append(u"\\pstLineAB[nodesepB=-1]{%s}{%s}" % (A, B))
    cor.append(u"\\pstLineAB[nodesepB=-1]{%s}{%s}" % (C, B))
    cor.append(u"\\pstLineAB[nodesepB=-1]{%s}{%s}" % (C, D))
    cor.append(u"\\pstLineAB[nodesepB=-1]{%s}{%s}" % (A, D))
    # codage
    cor.append(u"\\color{calcul}\\pstMarkAngle[linecolor=calcul,Mark=MarkHash]{%s}{%s}{%s}{}" % (B, A, C))
    cor.append(u"\\color{calcul}\\pstMarkAngle[linecolor=calcul,Mark=MarkHash]{%s}{%s}{%s}{%s\\degres}" % (C, A, D, angCAD))
    cor.append(u"\\color{calcul}\\pstMarkAngle[linecolor=calcul,Mark=MarkHash]{%s}{%s}{%s}{%s\\degres}" % (D, C, A, angCAD))
    cor.append(u"\\color{calcul}\\pstMarkAngle[linecolor=calcul,Mark=MarkHash]{%s}{%s}{%s}{}" % (A, C, B))
    cor.append(u"\\pstLineAB{%s}{%s}\\lput{:U}{\\psset{linecolor=enonce}\\MarkHashh}" % (A, B))
    cor.append(u"\\pstLineAB{%s}{%s}\\lput{:U}{\\psset{linecolor=enonce}\\MarkHashh}" % (C, B))
    cor.append(u"\\pstLineAB{%s}{%s}\\lput{:U}{\\psset{linecolor=enonce}\\MarkHashh}" % (C, D))
    cor.append(u"\\pstLineAB{%s}{%s}\\lput{:U}{\\psset{linecolor=enonce}\\MarkHashh}" % (A, D))
    cor.append(cotation((0, 0), (AC, 0), decimaux(AC), couleur="enonce"))
    cor.append(u"\\color{enonce}\\pstMarkAngle[linecolor=enonce]{%s}{%s}{%s}{%s\\degres}" % (A, D, C, angCDA))
    cor.append(u"\\end{pspicture}")

################### CARRÉ #######################

def carre_diag(exo, cor):
    """trace un carré dont on donne la longueur de la diagonale"""

    A, B, C, D, E = geo.choix_points(5)
    nom = shuffle_nom([A, B, C, D])
    BD = AC = 0.2 * random.randint(20, 40)  # AC mesure entre 4cm et 8cm, tracé horizontalement
    
    exo.append(u"\\item Trace un carré $%s$  tel que $%s%s=\\unit[%s]{cm}$.\\par"
               % (nom, A, C, decimaux(AC)))
    cor.append(u"\\item Trace un carré $%s$  tel que $%s%s=\\unit[%s]{cm}$.\\par"
               % (nom, A, C, decimaux(AC)))

    cor.append(u"Je note $%s$ le centre du carré.\\par" % (E))
    cor.append(u" Les diagonales du carré se coupent perpendiculairement en leur milieu $%s$ donc on a :" % E)
    cor.append("\\begin{enumerate}")
    cor.append(u"\\item $(%s%s)\\perp(%s%s)$." % (A, C, B, D))
    cor.append(u"\\item  $%s%s=%s%s=%s%s=%s%s=\\unit[%s]{cm}$ ;"
               % (A, E, C, E, B, E, D, E, decimaux(BD / 2)))
    cor.append("\\end{enumerate}\n")
    
    cor.append("\\begin{pspicture}(%.3f,%.3f)(%.3f,%.3f)" % (-BD / 2 - 0.4, -AC / 2 - 0.4, BD / 2 + 0.4, AC / 2 + 0.4))
    cor.append("\\pstGeonode[PosAngle={-90,0,90,180}](0,%.3f){%s}(%.3f,0){%s}(0,%.3f){%s}(%.3f,0){%s}"
               % (-AC / 2, A, BD / 2, B, AC / 2, C, -BD / 2, D))
    cor.append("\\pstGeonode[PosAngle=-45](0,0){%s}" % E)
    
    cor.append("\\pstLineAB{%s}{%s}\\lput{:U}{\\psset{linecolor=calcul}\\MarkCros}" % (A, E))
    cor.append("\\pstLineAB{%s}{%s}\\lput{:U}{\\psset{linecolor=calcul}\\MarkCros}" % (C, E))
    cor.append("\\pstLineAB{%s}{%s}\\lput{:U}{\\psset{linecolor=calcul}\\MarkCros}" % (B, E))
    cor.append("\\pstLineAB{%s}{%s}\\lput{:U}{\\psset{linecolor=calcul}\\MarkCros}" % (D, E))
    cor.append("\\pstLineAB{%s}{%s}\\lput{:U}{\\psset{linecolor=enonce}\\MarkHashh}" % (A, B))
    cor.append("\\pstLineAB{%s}{%s}\\lput{:U}{\\psset{linecolor=enonce}\\MarkHashh}" % (C, D))
    cor.append("\\pstLineAB{%s}{%s}\\lput{:U}{\\psset{linecolor=enonce}\\MarkHashh}" % (B, C))
    cor.append("\\pstLineAB{%s}{%s}\\lput{:U}{\\psset{linecolor=enonce}\\MarkHashh}" % (D, A))
    cor.append("\\pstRightAngle[linecolor=calcul]{%s}{%s}{%s}" % (B, E, C))
    cor.append(cotation_h((-BD / 2, 0), (0, 0), decimaux(BD / 2), couleur="enonce"))
    cor.append(u"\\end{pspicture}")
