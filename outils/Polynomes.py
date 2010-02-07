# -*- coding: utf-8 -*-

from outils.Arithmetique import carrerise
from outils.Affichage import suppr0list
from classes.SecondDegre import Poly2
import random
from math import *

def choix_coeffs(unitaire, nbrac, entiers):

    """Génère un polynôme du second degré, unitaire ou non, suivant le nombre de racines demandé, et avec des coeffs entiers ou non.
    Retourne un tuple contenant une liste [a, racines] et un objet polynôme."""
    sgn = [-1, 1]
    sgns = [random.randint(0,1), random.randint(0,1), random.randint(0,1)]

    if entiers:
        entier = 1.0
    else:
        entier = 10.0

    if unitaire:
        a = 1
        sgns[0] = 1
    else:
        a = random.randint(1, 30)

    if nbrac == 1:
        x = random.randint(1, 200) / entier
        coeffrac = [a*sgn[sgns[0]], x, x]
    elif nbrac == 0:
        coeffrac = []
    elif nbrac == 2:
        coeffrac = [a*sgn[sgns[0]], random.randint(0, 200)*sgn[sgns[1]] / entier, random.randint(0, 200)*sgn[sgns[2]]]


    if nbrac == 0:
        c = carrerise(a)*(random.randint(1, 10))**2
        b = 2*sqrt(a*c)
        coeffs = suppr0list([a*sgn[sgns[0]], b, (c+1)*sgn[sgns[0]]])
    else:

        coeffs = suppr0list([coeffrac[0], -coeffrac[0]*(coeffrac[1]+coeffrac[2]), coeffrac[0]*coeffrac[1]*coeffrac[2]])

    return (suppr0list(coeffrac), Poly2(coeffs[0], coeffs[1], coeffs[2]))

