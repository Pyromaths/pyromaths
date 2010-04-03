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

from random import randint
from outils.Affichage import decimaux

def ArrondirNombreDecimal():
    """Créée et corrige un exercice d'arrondis avec les encadrements."""
    hasard = [float(randint(10000,1000000)), float(randint(10000,1000000)),
            float(randint(10000,1000000)), float(randint(10000,1000000))]

    precision = [u'au millième', u'au centième', u'au dixième', u'à l\'unité',
            u'à la dizaine', u'à la centaine', 'au millier',
            u'à la dizaine de millier']

    choix_precision = [randint(0, 7), randint(0, 7), randint(0, 7),
            randint(0, 7)]

    supinf = ['', u'par défaut', u'par excès']

    choix_supinf = [randint(0, 2), randint(0, 2), randint(0, 2), randint(0, 2)]

    nombres = [(hasard[0])/(10**(-choix_precision[0]+4)),
            (hasard[1])/(10**(-choix_precision[1]+4)),
            (hasard[2])/(10**(-choix_precision[2]+4)),
            (hasard[3])/(10**(-choix_precision[3]+4))]
            
    exo = ["\\exercice", u'Arrondir les nombres suivants à la précision demandée :', '\\begin{enumerate}']
    cor = ["\\exercice*", u'Arrondir les nombres suivants à la précision demandée :', '\\begin{enumerate}']


    for k in range(4):
        
        exo.append( '\\item Nombre ' + str(k + 1) + ' : ' + decimaux(nombres[k]) + \
                ' ' + precision[choix_precision[k]] + ' ' + \
                supinf[choix_supinf[k]] + '.\n' )
   
        cor.append( '\\item Nombre ' + str(k + 1) + ' : ' + decimaux(nombres[k]) + \
                ' ' + precision[choix_precision[k]] + ' ' + \
                supinf[choix_supinf[k]] + '.\n' )
                
        arrondi = round(nombres[k], -choix_precision[k]+3)

        if (arrondi > nombres[k]):
            defaut = arrondi - 10**(choix_precision[k]-3)
            exc = arrondi

        if (arrondi <= nombres[k]):
            defaut = arrondi
            exc = arrondi + 10**(choix_precision[k]-3)

        if (choix_supinf[k] == 0):
            solution = arrondi
        elif (choix_supinf[k] == 1):
            solution = defaut
        elif (choix_supinf[k] == 2):
            solution = exc

        cor.append( 'L\'encadrement de ' + decimaux(nombres[k]) + ' ' + \
                precision[choix_precision[k]] + ' est : \n' )
        cor.append( decimaux(defaut) + ' < ' + decimaux(nombres[k]) + ' < ' + \
                decimaux(exc) + '\n' )
        cor.append( 'On en deduit que son arrondi ' + precision[choix_precision[k]] + \
                ' ' + supinf[choix_supinf[k]] + ' est : ' + decimaux(solution) + '.\n')

    exo.append("\\end{enumerate}")    
    cor.append("\\end{enumerate}") 
    
    return (exo, cor)