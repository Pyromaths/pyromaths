# -*- coding: utf-8 -*-

from random import randint
import re
from outils/Affichage import ecrire_par3

def arrondi():
    """Créée et corrige un exercice d'arrondis avec les encadrements. PAS FINI."""
    hasard = [float(randint(10000,1000000)), float(randint(10000,1000000)), float(randint(10000,1000000)), float(randint(10000,1000000))]

    precision = ['au millième', 'au centième', 'au dixième', 'à l\'unité', 'à la dizaine', 'à la centaine', 'au millier', 'à la dizaine de millier']

    choix_precision = [randint(0, 7), randint(0, 7), randint(0, 7), randint(0, 7)]

    supinf = ['', 'par défaut', 'par excès']

    choix_supinf = [randint(0, 2), randint(0, 2), randint(0, 2), randint(0, 2)]

    nombres = [(hasard[0])/(10**(-choix_precision[0]+4)), (hasard[1])/(10**(-choix_precision[1]+4)), (hasard[2])/(10**(-choix_precision[2]+4)), (hasard[3])/(10**(-choix_precision[3]+4))]

    print 'Arrondir les nombres suivants à la précision demandée :'

    for j in range(4):
        print 'Nombre ' + str(j + 1) + ' : ' + ecrire_par3(nombres[j]) + ' ' + precision[choix_precision[j]] + ' ' + supinf[choix_supinf[j]] + '.\n'


    for k in range(4):

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

    print 'L\'encadrement de ' + ecrire_par3(nombres[k]) + ' ' + precision[choix_precision[k]] + ' est : \n'
    print ecrire_par3(defaut) + ' < ' + ecrire_par3(nombres[k]) + ' < ' + ecrire_par3(exc) + '\n'
    print 'On en déduit que son arrondi ' + precision[choix_precision[k]] + ' ' + supinf[choix_supinf[k]] + ' est : ' + ecrire_par3(solution)

    if k != 3:
        print '################################\n'