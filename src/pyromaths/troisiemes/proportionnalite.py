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
from random import randint, shuffle, randrange
from pyromaths.outils.decimaux import decimaux
import math
from pyromaths.outils.Geometrie import cotation, cotation_h

def choix_valeurs(min_prct, max_prct, min_nbre, max_nbre):

    while 1:
        decomp100 = [2,2,5,5,1,1]
        shuffle(decomp100)
        prct = decomp100[0] * decomp100[1] * decomp100[2]  # qui donne 2, 4, 5, 10, 20, 25 ou 50
        tot = decomp100[3] * decomp100[4] * decomp100[5]
        if (max_prct / prct != 0) and (max_nbre / tot != 0):
            break
    prct = randint(max(min_prct / prct, 1 ), (max_prct / prct )) * prct
    tot = tot * randint( max(min_nbre / tot,1) , (max_nbre / tot ))
    return prct, tot
    
def proportionnalite_3eme():
    #choix exercice
    i = randrange(2)
    #choix valeurs
    [min_prct, max_prct, min_nbre, max_nbre] = [[40, 80, 40, 65],
                                                [40, 80, 65, 90]][i]
    #choisit les valeurs du groupe A
    #prctA : pourcentage d'individu dans le groupe A entre 40% et 80%
    #totA : nombre total du groupe A entre 40 et 70
    prctA, totA = choix_valeurs(min_prct = 40, max_prct = 80, min_nbre = 40, max_nbre = 65)

    #On choisit B avec des valeurs différentes
    while 1:
        prctB, totB = choix_valeurs(min_prct = 40, max_prct = 80, min_nbre = 40, max_nbre = 65)
        if prctA != prctB and totB != totA:
            break
        
    Total = totA + totB

    #calcul
    nbA = (prctA * totA / 100)
    nbB = (prctB * totB / 100)
    nbTotal = ((nbA + nbB))
    prct_final = (100.0*nbTotal/Total)
    prct_final_arrondi = round(100.0*nbTotal/Total, 1)
    if prct_final == prct_final_arrondi:
        approx = "="
    else:
        approx = "\\approx"
    
    #La situation
    texte = [u"Lors d'un voyage scolaire, les élèves sont répartis dans deux bus :",
             u"Au collège Dubois, il y a $%s$ élèves en quatrièmes et $%s$ élèves en troisièmes."%(totA,totB)][i]

    #Les deux groupes
    ligne1 = [u"\\item Bus A : %s élèves dont %s %s de garçons."%(totA, prctA,"\\%"),
              u"\\item $%s$ %s des élèves de quatrièmes possèdent un ordinateur ;"%(prctA,"\\%")][i]
    ligne2 = [u"\\item Bus A : %s élèves dont %s %s de garçons."%(totB, prctB,"\\%"),
              u"\\item $%s$ %s des élèves de troisièmes possèdent un ordinateur ;"%(prctB,"\\%")][i]

    #La question
    question = [u"Quel est, sur l'ensemble des deux bus, le pourcentage de garçons ?\\par",
                u"Quel est le pourcentage des élèves qui possèdent un ordinateur ?\\par"][i]

    #La correction
    correction =[#Dans le bus
        [u"Dans le bus A, il y a $\\cfrac{%s \\times %s}{100} = %s$ garçons.\\par"%(prctA, totA, decimaux(nbA)),
           u"Dans le bus B, il y a $\\cfrac{%s \\times %s}{100} = %s$ garçons.\\par"%(prctB, totB, decimaux(nbB)),
           u"On en déduit qu'il y a $%s + %s = %s$ garçons sur un total de $%s + %s = %s $ élèves.\\par"
                   %(decimaux(nbA), decimaux(nbB), nbTotal, totA, totB, Total),
            u" Le pourcentage de garçons sur l'ensemble des deux bus est donc de $\\cfrac{%s}{%s}\\times 100 %s %s%s$"
                  %(nbTotal, Total, approx, decimaux(prct_final_arrondi), "\,\\%")],
        #À l'ordinateurs
                 [u"En quatrièmes, $\\cfrac{%s \\times %s}{100} = %s$ élèves possèdent un ordinateur.\\par"%(prctA, totA, decimaux(nbA)),
                  u"En troisièmes, $\\cfrac{%s \\times %s}{100} = %s$ élèves possèdent un ordinateur.\\par"%(prctB, totB, decimaux(nbB)),
                  u"On en déduit qu'il y a $%s + %s = %s$ élèves qui possèdent un ordinateur sur un total de $%s + %s = %s $ élèves.\\par"
                   %(decimaux(nbA), decimaux(nbB), nbTotal, totA, totB, Total),
                   u" Le pourcentage d'élèves possédant un ordinateur est donc de $\\cfrac{%s}{%s}\\times 100 %s %s%s$"
                  %(nbTotal, Total, approx, decimaux(prct_final_arrondi), "\,\\%")],
                   ][i]
    exo = ["\\exercice",
           texte,
           "\\begin{itemize}",
           ligne1,
           ligne2,
           "\\end{itemize}",
           question,
           ]
        
    cor = ["\\exercice*",
           texte,
           "\\begin{itemize}",
           ligne1,
           ligne2,
           "\\end{itemize}",
           question,
           "\\dotfill\\par"
           ] + correction
    
    
    return (exo,cor)
