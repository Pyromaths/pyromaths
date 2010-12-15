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


import math
import random
from ..classes.Racine import simplifie_racine

class Vecteur:
  
    def __init__(self, x=0, y=0):
      self.x=x
      self.y=y
    
    def __eq__(self, vec): 
      '''Teste l'égalité entre deux vecteurs'''
      return (self.x==vec.x) and (self.y==vec.y)
      
    def __add__(self, vec):  
      '''Addition'''
      return Vecteur(self.x+vec.x,self.y+vec.y)
      
    def __sub__(self, vec):
      '''Soustraction'''
      return Vecteur(self.x-vec.x,self.y-vec.y)
      
    def __mul__(self, c):
	'''Multiplication par un nombre''' ## Besoin du produit scalaire ou du produit vectoriel ?
        if isinstance(c, float) or isinstance(c, int):
	  return  Vecteur(c*self.x,c*self.y)
	  
    def __rmul__(self, c):
	'''Multiplication Reverse''' ## Besoin du produit scalaire ou du produit vectoriel ?
        if isinstance(c, float) or isinstance(c, int):
	  return  self * c
    def __neg__(self):
	'''Négatif d'un vecteur'''
	return -1 * self
	
    def __div__(self, c):
      if isinstance(c, float) or isinstance(c, int):
	  return Vecteur(self.x/float(c), self.y/float(c))
	  
    def __abs__(self):
      '''Retourne la norme du vecteur sous la forme coeff,radicande où sqrt(n)=coeff*sqrt(radicande)'''
      return simplifie_racine(self.x**2 + self.y**2)
      
    def __str__(self):
      '''Affichage sous forme de coordonnées'''
      return '(' + str(self.x) + ',' + str(self.y) + ')'
      
    def normeTex(self):
      '''Affichage TeX de la racine simplifiée de la racine, sans les dollars.'''
      norme = abs(self)
      if norme[0] == 1:
	return "\sqrt{" + str(norme[1]) + "}"
      elif norme[1] == 1:
	return str(norme[0])
      else:
	return str(norme[0]) + "\sqrt{" + str(norme[1]) + "}"
      
def randvect(a, b):
  '''Retourne un vecteur aléatoire et s'occupe de placer l'abscisse au-dessus de a et l'ordonnée dans [0,b]. Il faut que b>=10.'''
  x = random.randint(-5,5)
  y = random.randint(-5,5)
  posx = a + max(1-x, 1) ## 1 colonne minimum d'écart
  if y>=0:
    posy = random.randint(0, math.fabs(y - 2)) + 1 ## Ajouter 1 pour éviter de coller au bas de la grille
  else:
    posy = random.randint(math.fabs(y), b) ## Comme y < 0, cela ne colle pas au bas de la grille
  return [Vecteur(x,y), posx, posy]
