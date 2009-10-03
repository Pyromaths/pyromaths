# -*- coding: utf-8 -*-

import sys
sys.path[:0] = ['../outils']
from Arithmetique import *
from Affichage import decimaux

def produitfacteurs(facteurs):
    """Affiche sous forme de produit les éléments d'une liste."""
    prodfacteurs = ''
    for element in facteurs:
        prodfacteurs += str(element) + ' \\times '
    return prodfacteurs[:-7]


class Racine:
    def __init__(self, radicande, coeff = 1, indice = 2):
        if (radicande < 0) or not (isinstance(indice, int)):
            print "Erreur de définition ! Le radicande doit être positif et l'indice un nombre entier !"
        self.radicande = radicande
        self.indice = indice # Nombre entier
        self.coeff = coeff # Coeff devant la racine

    def __add__(self, other):
        if not (isinstance(other, Racine)):
            return str(self) + " + " + str(other)
        if (self.radicande == other.radicande) and (self.indice == other.indice):
            return Racine(self.radicande, self.coeff + other.coeff, self.indice)
        else:
            return str(self) + " + " + str(other)

    def __radd__(self, other):
        return self + other

    def __sub__(self, other):
        if not (isinstance(other, Racine)):
            return str(self) + " + " + str(other)
        if (self.radicande == other.radicande) and (self.indice == other.indice):
            return Racine(self.radicande, self.coeff - other.coeff, self.indice)
        else:
            return str(self) + " - " + str(other)

    def __rsub__(self, other):
        return -(self - other)

    def __mul__(self, other):
        if (isinstance(other, float)) or (isinstance(other, int)):
            return Racine(self.radicande, self.coeff * other, self.indice)
        elif self.indice == other.indice:
            return Racine(self.radicande * other.radicande, self.coeff * other.coeff, self.indice)
        else:
            return str(self) + ' x ' + str(other)

    def __rmul__(self, other):
        return self * other

    def __div__(self, other):
        if (isinstance(other, float)) or (isinstance(other, int)):
            return Racine(self.radicande, self.coeff / other, self.indice)
        elif self.indice == other.indice:
            return Racine(self.radicande / float(other.radicande), self.coeff / float(other.coeff), self.indice)
        else:
            return str(self) + ' / ' + str(other)

    def __rdiv__(self, other):
        if (isinstance(other, float)) or (isinstance(other, int)):
            return Racine(self.radicande, other / float(self.coeff * self.radicande), self.indice)
        elif self.indice == other.indice:
            return Racine(other.radicande / float(self.radicande), other.coeff / float(self.coeff), self.indice)
        else:
            return str(other) + ' / ' + str(self)

    def __str__(self):
        if self.coeff == 0:
            return "0"
        else:
            if self.coeff == 1:
                coeff = ""
            else:
                coeff = decimaux(self.coeff, 1) + " \\, "
            if self.radicande == 0:
                coeff = ""
                racine = ""
                radicande = "0"
            elif self.indice == 2:
                racine = "\\sqrt{"
                radicande = decimaux(self.radicande, 1) + "}"
            else:
                racine = "\\sqrt[{0}]{{".format(self.indice)
                radicande = decimaux(self.radicande, 1) + "}"
            return coeff + racine + radicande

    def simplifie(self):
        facteurs = factor(self.radicande)
        prodfacteurs = produitfacteurs(facteurs)
        if self.indice == 2:
            racine = "\\sqrt{"
        else:
            racine = "\\sqrt[{0}]{{".format(self.indice)
        coeff = self.coeff
        radicande = self.radicande
        detail = [str(self), ' = ', str(coeff) + racine + prodfacteurs + '}']
        for element in facteurs:
            if facteurs.count(element) % self.indice == 0:
                coeff *= element
                for n in range(self.indice):
                    facteurs.remove(element)
                radicande = radicande // (element**(self.indice))
                prodfacteurs = produitfacteurs(facteurs)
                detail.append(' = ')
                detail.append(str(coeff) + ' \\times ' + racine + prodfacteurs + '}')
        if radicande == 1:
            return (coeff, detail)
        else:
            return (Racine(radicande, coeff, self.indice), detail)
                