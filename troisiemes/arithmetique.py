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

from outils.Arithmetique import pgcd, ppcm, premier, factorise
from random import randint, shuffle

premiers = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 
131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 
277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 
443, 449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577, 587, 593, 599, 601, 607, 613, 
617, 619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691, 701, 709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 797, 
809, 811, 821, 823, 827, 829, 839, 853, 857, 859, 863, 877, 881, 883, 887, 907, 911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983, 
991, 997] ## Liste de longueur 168

def Arithmetique():
  """Exercice de décomposition de nombres en facteurs premiers, puis de recherche du PGCD et du PPCM, et d'applications aux fractions"""
  
  ### Question 1
  exo = ["\\exercice", '\\begin{enumerate}', 
        u"\\item Donner la décomposition en facteurs premiers des nombres suivants, et préciser si besoin est, quand il s\'agit d\'un nombre premier :\n"]
  cor = ["\\exercice*", '\\begin{enumerate}', 
        u"\\item Donner la décomposition en facteurs premiers des nombres suivants, et préciser si besoin est, quand il s\'agit d\'un nombre premier :\n"]
          
  prime = premiers[randint(10,167)]
  
  fauxpgcd = randint(1,101)
  fauxpgcdfactor = factorise(fauxpgcd)[0]

  complementaires = [randint(6,50), randint(6,50)]
  pgcdcompl = pgcd(complementaires[0], complementaires[1])
  pgcdcomplfact = factorise(pgcdcompl)[0]
  
  if pgcdcompl != 1:
    facteurs = pgcdcomplfact + fauxpgcdfactor
    facteurs.sort()
  else:
    facteurs = fauxpgcdfactor
  
  autresnombres = [randint(51,999), randint(51,999)]
  
  listenombres = [prime, complementaires[0] * fauxpgcd, complementaires[1] * fauxpgcd, ] + autresnombres
  melange = [prime, complementaires[0] * fauxpgcd, complementaires[1] * fauxpgcd, ] + autresnombres
  shuffle(melange)
  
  exo.append(str(melange[0]) + " ; " + str(melange[1]) + " ; " + str(melange[2]) + " ; " + str(melange[3]) + " ; " + str(melange[4]) + " ;\n")
  
  cor.append("\\begin{multicols}{2}")
  
  for i in range(5):
    cor += factorise(melange[i])[1]

  
  cor.append("\\end{multicols}") 
  
  ### Question 2
  exo.append(u'\\item En déduire le PGCD et le PPCM des nombres ' + str(listenombres[1]) + " et " + str(listenombres[2]) + ".\n")
  cor.append(u'\\item En déduire le PGCD et le PPCM des nombres ' + str(listenombres[1]) + " et " + str(listenombres[2]) + ".\n")
  
  cor.append(u"D'après la question 1), on sait que les nombres " + str(listenombres[1]) + " et " + str(listenombres[2]) + 
  " ont comme facteurs premiers communs : \n")
  
  for j in range(len(facteurs)):
    if j != len(facteurs)-1:
      cor.append(str(facteurs[j]) + " , ")
    else:
      cor.append(str(facteurs[j]) + ".\n")
  
  cor.append(u"On en déduit que le PGCD des nombres " + str(listenombres[1]) + " et " + str(listenombres[2]) + " est : ")

  for j in range(len(facteurs)):
    if j != len(facteurs)-1:
      cor.append(" " + str(facteurs[j]) + " \\times ")
    else:
      cor.append(str(facteurs[j]) + " = ")
      
  cor.append(str(fauxpgcd * pgcdcompl) + ".\n")
  
  vraippcm = (listenombres[1] * listenombres[2]) / (fauxpgcd * pgcdcompl)
  
  if (listenombres[1] % listenombres[2] == 0):
    cor.append(listenombres[1] + u" est un multiple de " + listenombres[2] + u", donc leur PPCM est directement " + listenombres[1] + ".\n")
  elif (listenombres[2] % listenombres[1] == 0):
    cor.append(listenombres[2] + u" est un multiple de " + listenombres[1] + u", donc leur PPCM est directement " + listenombres[2] + ".\n")
  else:
    cor.append(u"Il existe plusieurs méthodes pour calculer le PPCM de " + str(listenombres[1]) + " et de " + str(listenombres[2]) + ".\n" )
    cor.append(u"En voici deux :")
    cor.append("\\begin{enumerate}")
    
    cor.append(u"\\item On peut simplement utiliser la formule : a \\times b = PGCD(a;b) \\times PPCM(a;b)\n" +
              u"Donc : PPCM(" + str(listenombres[1]) + ";" + str(listenombres[2]) + ") = " +
              "\\dfrac{" + str(listenombres[1]) + "\\times" + str(listenombres[2]) + "}{" + str(fauxpgcd * pgcdcompl) +
              "} = " + str(vraippcm) + ".\n")
    
    cor.append(u"\\item On peut aussi multiplier un nombre par les \"facteurs complémentaires\" de l'autre.\n" +
              u"Ces \"facteurs complémentaires\" sont les facteurs qui complètent le PGCD pour former le nombre.\n" +
              u"Comme PGCD(" + str(listenombres[1]) + ";" + str(listenombres[2]) + ") = " + str(fauxpgcd * pgcdcompl) + 
              u", alors les \"facteurs complémentaires\" de " + str(listenombres[1]) + u" sont :")
    
    factcompl = factorise(listenombres[1] / (fauxpgcd * pgcdcompl))[0]
    
    for j in range(len(factcompl)):
      if j != len(factcompl)-1:
        cor.append(" " + str(factcompl[j]) + " , ")
      else:
        cor.append(str(factcompl[j]) + ".\n")
        
    cor.append(u"On en déduit que PPCM(" + str(listenombres[1]) + ";" + str(listenombres[2]) + ") = " + str(listenombres[2]) + " \\times ")
    
    for j in range(len(factcompl)):
      if j != len(factcompl)-1:
        cor.append(str(factcompl[j]) + " \\times ")
      else:
        cor.append(str(factcompl[j]) + " = ")
        
    cor.append(str(vraippcm) + ".\n")
    
    cor.append("\\end{enumerate}")
  
  ### Question 3
  exo.append(u"\\item Quel est le plus petit nombre par lequel il faut multiplier " + autresnombres[0] + u" pour que ce soit un carré parfait ?\n")
 
  ### Question 4
  exo.append(u"\\item Simplifier la fraction \\dfrac{" + str(listenombres[1]) + "}{" + str(listenombres[2]) + "} au maximum.\n")
  
  ### Question 5
  
  num = [randint(6,50), randint(6,50)]
  exo.append(u"\\item Calculer \\dfrac{" + str(num[0]) + "}{" + str(listenombres[1]) + "} + \\dfrac{" + str(num[1])
             + "}{" + str(listenombres[2]) + "}.\n")
  
  exo.append("\\end{enumerate}")
  cor.append("\\end{enumerate}")
  
  return (exo,cor)
  
  
    
    
  
  
    
  
  
  