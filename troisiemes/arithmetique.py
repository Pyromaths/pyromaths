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

from outils.Arithmetique import pgcd, ppcm, premier, factorise, carrerise
from outils.Affichage import decimaux
from random import randint, shuffle

premiers = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61,
        67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139,
        149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223,
        227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293,
        307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383,
        389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463,
        467, 479, 487, 491, 499, 503, 509, 521, 523, 541, 547, 557, 563, 569,
        571, 577, 587, 593, 599, 601, 607, 613, 617, 619, 631, 641, 643, 647,
        653, 659, 661, 673, 677, 683, 691, 701, 709, 719, 727, 733, 739, 743,
        751, 757, 761, 769, 773, 787, 797, 809, 811, 821, 823, 827, 829, 839,
        853, 857, 859, 863, 877, 881, 883, 887, 907, 911, 919, 929, 937, 941,
        947, 953, 967, 971, 977, 983, 991, 997] ## Liste de longueur 168

def Arithmetique():
  """Exercice de décomposition de nombres en facteurs premiers, puis de
  recherche du PGCD et du PPCM, et d'applications aux fractions"""

  ### Question 1
  exo = ["\\exercice", '\\begin{enumerate}', u"\\item Donner la décomposition" +
          u" en facteurs premiers des nombres suivants, et préciser quand il" +
          u" s\'agit d\'un nombre premier :\\par"]
  cor = ["\\exercice*", '\\begin{enumerate}', u"\\item Donner la décomposition"
          + u" en facteurs premiers des nombres suivants, et préciser quand il"
          + u" s\'agit d\'un nombre premier :\\par"]

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

  listenombres = [prime, complementaires[0] * fauxpgcd, complementaires[1] *
          fauxpgcd, ] + autresnombres
  melange = [prime, complementaires[0] * fauxpgcd, complementaires[1] *
          fauxpgcd, ] + autresnombres
  shuffle(melange)

  exo.append(decimaux(melange[0]) + " ; " + decimaux(melange[1]) + " ; " +
          decimaux(melange[2]) + " ; " + decimaux(melange[3]) + " ; " +
          decimaux(melange[4]) + " ;")

  cor.append("\\begin{multicols}{2}")

  for i in range(5):
    cor += factorise(melange[i])[1]

  cor.append("\\end{multicols}")

  ### Question 2
  exo.append(u'\\item En déduire le PGCD et le PPCM des nombres ' +
          decimaux(listenombres[1]) + " et " + decimaux(listenombres[2]) +
          ".")
  cor.append(u'\\item En déduire le PGCD et le PPCM des nombres ' +
          decimaux(listenombres[1]) + " et " + decimaux(listenombres[2]) +
          ".\\par")

  cor.append(u"D'après la question 1), on sait que les nombres " +
          decimaux(listenombres[1]) + " et " + decimaux(listenombres[2]) +
          " ont comme facteurs premiers communs : $")

  for j in range(len(facteurs)):
    if j != len(facteurs)-1:
      cor.append(decimaux(facteurs[j]) + " , ")
    else:
      cor.append(decimaux(facteurs[j]) + ".$\\par")

  cor.append(u"On en déduit que le PGCD des nombres " +
          decimaux(listenombres[1]) + " et " + decimaux(listenombres[2]) +
          " est : $")

  for j in range(len(facteurs)):
    if j != len(facteurs)-1:
      cor.append(decimaux(facteurs[j]) + " \\times ")
    else:
      cor.append(decimaux(facteurs[j]) + " = ")

  cor.append(decimaux(fauxpgcd * pgcdcompl) + ".$\\par")

  vraippcm = (listenombres[1] * listenombres[2]) / (fauxpgcd * pgcdcompl)

  if (listenombres[1] % listenombres[2] == 0):
    cor.append(decimaux(listenombres[1]) + u" est un multiple de " +
            decimaux(listenombres[2]) + u", donc leur PPCM est directement "
               + decimaux(listenombres[1]) + ".")
  elif (listenombres[2] % listenombres[1] == 0):
    cor.append(decimaux(listenombres[2]) + u" est un multiple de " +
            decimaux(listenombres[1]) + u", donc leur PPCM est directement " +
            decimaux(listenombres[2]) + ".")
  else:
    cor.append(u"Il existe plusieurs méthodes pour calculer le PPCM de " +
            decimaux(listenombres[1]) + " et de " + decimaux(listenombres[2]) +
            ".\\par" )
    cor.append(u"En voici deux :")
    cor.append("\\begin{enumerate}")

    cor.append(u"\\item On peut simplement utiliser la formule :")
    cor.append(u"$a \\times b = PGCD(a;~b) \\times PPCM(a;~b)$.\\par")
    cor.append(u"Donc : $PPCM(" + decimaux(listenombres[1]) + ";~" +
        decimaux(listenombres[2]) + ") = " + "\\dfrac{" +
        decimaux(listenombres[1]) + "\\times" + decimaux(listenombres[2]) + "}{"
        + decimaux(fauxpgcd * pgcdcompl) + "} = " + decimaux(vraippcm) +
        ".$")

    cor.append(u"\\item On peut aussi multiplier un nombre par les \"facteurs "
        + u"complémentaires\" de l'autre.\n" + u"Ces \"facteurs " +
        u"complémentaires\" sont les facteurs qui complètent le PGCD pour " +
        u"former le nombre.\\par")
    cor.append(u"Comme $PGCD(" + decimaux(listenombres[1]) + ";~" +
        decimaux(listenombres[2]) + ") = " + decimaux(fauxpgcd * pgcdcompl))

    #TODO: la gestion du pluriel n'est psa bonne. Ce n'est pas parceque la
    #décomposition comporte plusieurs facteurs qu'il y a plusieurs facteurs
    #complémentaires
    if len(facteurs) > 1:
      cor.append(" = ")
      for j in range(len(facteurs)):
        if j != len(facteurs)-1:
          cor.append(decimaux(facteurs[j]) + " \\times ")
        else:
          cor.append(decimaux(facteurs[j]))
      textcompl = u"$, alors les \"facteurs complémentaires\" de $"
    else:
      textcompl = u"$, alors le \"facteur complémentaire\" de $"

    cor.append(textcompl + decimaux(listenombres[1]) + " = ")

    factornb1 = factorise(listenombres[1])[0]

    for j in range(len(factornb1)):
      if j != len(factornb1)-1:
        cor.append(decimaux(factornb1[j]) + " \\times ")
      else:
        cor.append(decimaux(factornb1[j]))

    factcompl = factorise(listenombres[1] / (fauxpgcd * pgcdcompl))[0]

    if len(factcompl) == 1:
      cor.append(u"$ est :")
    else:
      cor.append(u"$ sont :")

    for j in range(len(factcompl)):
      if j != len(factcompl)-1:
        cor.append(decimaux(factcompl[j]) + " , ")
      else:
        cor.append(decimaux(factcompl[j]) + ".\\par")

    cor.append(u"On en déduit que $PPCM(" + decimaux(listenombres[1]) + ";~" +
            decimaux(listenombres[2]) + ") = " + decimaux(listenombres[2]) +
            " \\times ")

    for j in range(len(factcompl)):
      if j != len(factcompl)-1:
        cor.append(decimaux(factcompl[j]) + " \\times ")
      else:
        cor.append(decimaux(factcompl[j]) + " = ")

    cor.append(decimaux(vraippcm) + ".$")

    cor.append("\\end{enumerate}")

  ### Question 3

  exo.append(u"\\item Quel est le plus petit nombre par lequel il faut " +
          u"multiplier " + decimaux(autresnombres[0]) +
          u" pour obtenir un carré parfait ?")

  cor.append(u" \\item Pour obtenir un carré parfait, il faut que sa " +
          u"décomposition en facteurs premiers ne contienne que des facteurs "
          + u"apparaissant un nombre pair de fois. D'après la question 1, " +
          u"la décomposition en facteurs premiers de "
          + decimaux(autresnombres[0]))

  decompautre = factorise(autresnombres[0])[1]

  if len(decompautre) == 1:
    cor.append(u" est lui-même, car c'est un nombre premier.")
  else:
    cor.append(" est : \\par\n$" + decimaux(autresnombres[0]) + " = " +
            decompautre[-2][5:-2] + ".$\\par")

  cor.append(u"Il faut donc encore multiplier ce nombre par ")

  carre = carrerise(autresnombres[0])
  factsup = factorise(carre)[0]

  if len(factsup)==1:
    cor.append(" le facteur ")
  else:
    cor.append(" les facteurs ")

  for j in range(len(factsup)):
    if (j != len(factsup)-1) and (j != len(factsup)-2):
      cor.append(decimaux(factsup[j]) + " , ")
    elif (j == len(factsup)-2):
      cor.append(decimaux(factsup[j]) + " et ")
    else:
      cor.append(decimaux(factsup[j]) + ".\\par")

  cor.append(u"Le nombre cherché est par conséquent " + decimaux(carre) +
          u" et le carré parfait obtenu est " + decimaux(carre *
              autresnombres[0]) + ".")

  ### Question 4
  exo.append(u"\\item Rendre la fraction $\\dfrac{" + decimaux(listenombres[1])
          + "}{" + decimaux(listenombres[2]) + u"}$ irréductible.")

  cor.append(u"\\item Le moyen le plus rapide de simplifier cette fraction est"
          + u"de diviser le numérateur et le dénominateur par leur PGCD." +
          u" D'après la question 2),  PGCD(" + decimaux(listenombres[1]) + ";~"
          + decimaux(listenombres[2]) + ") = "
          + decimaux(fauxpgcd * pgcdcompl) + ", donc on obtient :\\par")
  cor.append(u"$\dfrac{" + decimaux(listenombres[1]) + "{\\scriptstyle \\div " +
          decimaux(fauxpgcd * pgcdcompl) + "}}{" + decimaux(listenombres[2]) +
          "{\\scriptstyle \\div " + decimaux(fauxpgcd * pgcdcompl) +
          "}} = \dfrac{" + decimaux(listenombres[1] / (fauxpgcd * pgcdcompl)) +
          "}{" + decimaux(listenombres[2] / (fauxpgcd * pgcdcompl)) + "}.$")

  ### Question 5

  num = [randint(6,50), randint(6,50)]
  exo.append(u"\\item Calculer $\\dfrac{" + decimaux(num[0]) + "}{" +
          decimaux(listenombres[1]) + "} + \\dfrac{" + decimaux(num[1]) + "}{" +
          decimaux(listenombres[2]) + "}$.")

  mult1 = vraippcm / listenombres[1]
  mult2 = vraippcm / listenombres[2]

  num1 = mult1 * num[0]
  num2 = mult2 * num[1]

  simplfin = pgcd(num1+num2,vraippcm)

  if simplfin != 1:
    simpl = "{\\scriptstyle \\div " + decimaux(simplfin) + "}"
    result = " = \\dfrac{" + decimaux((num1+num2)/simplfin) + "}{" + \
            decimaux((vraippcm)/simplfin) + "}"
  else:
    simpl = ""
    result = ""

  cor.append(u"\\item Il faut mettre les fractions au même dénominateur. Grâce"
          + u"à la question 2), nous avons déjà un dénominateur commun : " +
          u"le PPCM des nombres " + decimaux(listenombres[1]) + " et " +
          decimaux(listenombres[2]) + u", qui est par définition le plus petit"
          + u"multiple commun de ces deux nombres.\\par")
  cor.append(u"$\\dfrac{" + decimaux(num[0]) + "{\\scriptstyle \\times " +
          decimaux(mult1) + "}}{" + decimaux(listenombres[1]) +
          "{\\scriptstyle \\times " + decimaux(mult1) + "}} + \\dfrac{" +
          decimaux(num[1]) + "{\\scriptstyle \\times " + decimaux(mult2) + "}}{"
          + decimaux(listenombres[2]) + "{\\scriptstyle \\times " +
          decimaux(mult2) + "}} = \\dfrac{" + decimaux(num1) + "}{" +
          decimaux(vraippcm) + "} + \\dfrac{" + decimaux(num2) + "}{" +
          decimaux(vraippcm) + "} = \\dfrac{" + decimaux(num1+num2) + simpl +
          "}{" + decimaux(vraippcm) + simpl + "}" + result + ".$")

  exo.append("\\end{enumerate}")
  cor.append("\\end{enumerate}")

  return (exo,cor)
