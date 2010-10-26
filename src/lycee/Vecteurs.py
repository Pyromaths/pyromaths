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


##- additions / soustractions de vecteurs ( difficulté : ne pas sortir du cadre )
##- multiplication d'un vecteur par un réel +  add + sous ( difficulté : ne pas sortir du cadre )
##- lire les coordonnées d'un vecteur
##- placer un point B connaissant A et les coordonnées de vec{AB} : avec coordonnées ou i et j ( difficulté : ne pas sortir du cadre )
##- calcul de norme
##- simplifier des sommes
##- problèmes de colinéarité

from classes.Vecteurs import *
import math

def dist_bords(a,b):
    '''Calcule les distances minimales d'un point de coordonnées (a,b) aux bords du cadre, selon l'axe x et y.'''
    x = min(a,18-a) # la largeur vaut 18
    y = min(b,10-b) # la hauteur vaut 10
    return (x,y)
    
def pair(n):
    '''Retourne le plus petit entier pair strictement plus grand que n'''
    if (n % 2 == 0):
      return n+2
    else:
      return n+1

def repr_somme(u,v,cor):
    '''Représente la somme des vecteurs u + v.'''

    a = u + v
                 
    if (u.x * a.x >= 0 ):
      largeur = max(math.fabs(u.x),math.fabs(a.x))
      if ( a.x > 0 ):
         departx = 0
      elif ( a.x == 0 ):
	 departx = -u.x/2+math.fabs(u.x)/2
      else:
         departx = max(math.fabs(u.x),math.fabs(a.x))
    else:
      largeur = math.fabs(u.x)+math.fabs(a.x)
      if ( u.x >= 0 ):
         departx = -a.x
      else:
         departx = -u.x 
    if (u.y * a.y >= 0 ):
      hauteur = max(math.fabs(u.y),math.fabs(a.y))
      if ( a.y > 0 ):
         departy = 0
      elif ( a.y == 0 ):
	 departy = -u.y/2+math.fabs(u.y)/2
      else:
         departy = max(math.fabs(u.y),math.fabs(a.y))
    else:
      hauteur = math.fabs(u.y)+math.fabs(a.y)
      if ( u.y >= 0 ):
         departy = -a.y
      else:
         departy = -u.y 
    
    depart = "(" + str(departx) + "," + str(departy) + ")"
    largeur = str(pair(int(largeur)/2))
    hauteur = str(pair(int(hauteur)/2))

    cor.append(u"\\begin{pspicture}(0,0)(" + largeur + "," + hauteur + ")")
    cor.append(u"\psgrid[gridcolor=lightgray, subgridcolor=lightgray, subgriddiv=2, gridlabels=0pt]")
    cor.append(u"\psset{unit=5mm}")
    
    ## NOMS des vecteurs ?
    
    cor.append(u"\\rput" + depart + "{")
    cor.append(u"\psline{->}(0, 0)(" + str(u.x) + ", " + str(u.y) + ")") ## Premier Vecteur
    cor.append(u"\\rput(" + str(u.x / 2 + 1) + "," + str(u.y / 2 ) + ") \
		  {\psframebox[linecolor=white, fillstyle=solid]{$\\vec{" + "u" + "}$}}")
    cor.append(u"\psline{->}(" + str(u.x) + ", " + str(u.y) + ")(" + str(a.x) + ", " + str(a.y) + ")") ## 2e Vecteur
    #cor.append(u"\\rput(" + str((vec[1].x + vec[2].x) / 2 + 1) + "," + str((vec[1].y + vec[2].y) / 2 + plus) + ") \
	#	  {\psframebox[linecolor=white, fillstyle=solid]{$\\vec{" + vec[4] + "}$}}")
    cor.append(u"\psline[linestyle=dashed]{->}(0, 0)(" + str(a.x) + ", " + str(a.y) + ")") ## Résultat de l'opération

    cor.append(u"}")
    cor.append(u"\\end{pspicture}")

def vecteurs_add():
    '''Exercice sur la définition des vecteurs et leurs sommes.'''
    (u, posux, posuy) = randvect(0, 10)
    (v, posvx, posvy) = randvect(math.fabs(u.x)+3, 10)
    (w, poswx, poswy) = randvect(math.fabs(v.x)+math.fabs(u.x)+6, 10)
    
    exo=["\\exercice"]
    cor=["\\exercice*"]
            
    exo.append(u"\\begin{pspicture*}(0,0)(18,10)")
    exo.append(u"\psgrid[gridcolor=lightgray, subgridcolor=lightgray, subgriddiv=2, gridlabels=0pt]")
    exo.append(u"\psset{unit=5mm}")
    for vec in [(u, posux, posuy, "u"), (v, posvx, posvy, "v"), (w, poswx, poswy, "w")]:
      if vec[0].y>0:
	plus = 1
      else:
	plus = 0
      exo.append(u"\\rput(" + str(vec[1]) + "," + str(vec[2]) + "){")
      exo.append(u"\psline{->}(0, 0)(" + str(vec[0].x) + ", " + str(vec[0].y) + ")")
      exo.append(u"\\rput(" + str(vec[0].x / 2 + 1) + "," + str(vec[0].y / 2 + plus) + ") \
                   {\psframebox[linecolor=white, fillstyle=solid]{$\\vec{" + vec[3] + "}$}}")
      exo.append(u"}")
    exo.append(u"\\end{pspicture}")
    
    cor.append(u"\\begin{pspicture}(0,0)(18,10)")
    cor.append(u"\psgrid[gridcolor=lightgray, subgridcolor=lightgray, subgriddiv=2, gridlabels=0pt]")
    cor.append(u"\psset{unit=5mm}")
    for vec in [(u, posux, posuy, "u"), (v, posvx, posvy, "v"), (w, poswx, poswy, "w")]:
      if vec[0].y>0:
	plus = 1
      else:
	plus = 0
      cor.append(u"\\rput(" + str(vec[1]) + "," + str(vec[2]) + "){")
      cor.append(u"\psline{->}(0, 0)(" + str(vec[0].x) + ", " + str(vec[0].y) + ")")
      cor.append(u"\psline[linestyle=dashed](0, 0)(" + str(vec[0].x) + ", 0)(" + str(vec[0].x) + "," + str(vec[0].y) + ")") # Ajouter coordonnées des vecteurs ?
      cor.append(u"\\rput(" + str(vec[0].x / 2 + 1) + "," + str(vec[0].y / 2 + plus) + "){\psframebox[linecolor=white, \
                   fillstyle=solid]{$\\vec{" + vec[3] + "}$}}")
      cor.append(u"}")
    cor.append(u"\\end{pspicture*}")
    
    exo.append("\\par")
    cor.append("\\par")
    exo.append(u"On considère les vecteurs $\\vec{u}$, $\\vec{v}$, et $\\vec{w}$ ci-dessous.")
    cor.append(u"On considère les vecteurs $\\vec{u}$, $\\vec{v}$, et $\\vec{w}$ ci-dessous.")
    
    exo.append("\\begin{enumerate}")
    cor.append("\\begin{enumerate}")
    
    exo.append(u"\\item Lire les coordonnées de chacun des vecteurs $\\vec{u}$, $\\vec{v}$, et $\\vec{w}$.")
    cor.append(u"\\item Lire les coordonnées de chacun des vecteurs $\\vec{u}$, $\\vec{v}$, et $\\vec{w}$.")    
    
    cor.append("\\par")
    cor.append(u"Un petit rappel : l'abscisse d'un vecteur est la différence d'abscisse entre le fin et le début du vecteur. \
                 Concernant le vecteur $\\vec{u}$, son abscisse est " + str(u.x) + u". \
                 On lit également son ordonnée : " + str(u.x) + u". \
                 Donc les coordonnées de $\\vec{u}$ sont (" + str(u.x) + ", " + str(u.y) + u" ). \
                 Des pointillés ont été ajoutés sur la figure pour faciliter la lecture des coordonnées.")
    cor.append(u"De même, les coordonnées de $\\vec{v}$ sont (" + str(v.x) + ", " + str(v.y) + u" ) \
                 et les coordonnées de $\\vec{w}$ sont (" + str(w.x) + ", " + str(w.y) + " ).")
    
    ## Vérifier les unités de lecture
    
    exo.append(u"\\item Placer un point B de sorte que le vecteur $\\vec{AB}$ soit égal à -2 * u et .....")
    cor.append(u"\\item Placer un point B de sorte que le vecteur $\\vec{AB}$ soit égal à -2 * u et .....")

    ## Reste à corriger, préciser l'énoncé et dessiner le point concerné

    exo.append(u"\\item Calculer les normes de chacun des vecteurs $\\vec{u}$, $\\vec{v}$, et $\\vec{w}$.")
    cor.append(u"\\item Calculer les normes de chacun des vecteurs $\\vec{u}$, $\\vec{v}$, et $\\vec{w}$.")

    cor.append("\\par")
    cor.append(u"$\|\\vec{u}\|=\\sqrt{(" + str(u.x) + ")^2+(" + str(u.y) + ")^2}=\\sqrt{" + str(u.x**2) + " + " + str(u.y**2) + "}= \
                 \\sqrt{" + str(u.x**2 + u.y**2) + "}=" + str(u.normeTex()) + "$.\\par")
    cor.append(u"De la même manière, on obtient : $\|\\vec{v}\| = " + str(v.normeTex()) + "$ \
                 et $\|\\vec{w}\| = " + str(w.normeTex()) + "$.")

    exo.append(u"\\item Dessiner des représentants des vecteurs $\\vec{u}+\\vec{v}$, $\\vec{u}-\\vec{v}$, $\\vec{u}-\\vec{w}$ \
                 et $\\vec{v}+\\vec{w}$.")
    cor.append(u"\\item Dessiner des représentants des vecteurs $\\vec{u}+\\vec{v}$, $\\vec{u}-\\vec{v}$, $\\vec{u}-\\vec{w}$ \
                 et $\\vec{v}+\\vec{w}$.\\par")
    cor.append(u"Pour dessiner les sommes ou différences de vecteurs, il faut les mettre \"bouts à bouts\", \
                 comme sur les figures qui suivent :\\par")
    
    repr_somme(u,v,cor)
    repr_somme(u,-v,cor)
    cor.append("\\par")
    repr_somme(u,-w,cor)
    repr_somme(v,w,cor)

    exo.append("\\end{enumerate}")
    cor.append("\\end{enumerate}")
    
    return exo,cor
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
