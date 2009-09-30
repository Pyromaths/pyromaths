# -*- coding: utf-8 -*-

from outils/Arithmetique import factor

class Racine:
    """Classe pour les racines carrées."""
    def __init__(self, radicande, indice, coeff = 1):
        if (radicande < 0) or not (isinstance(indice, int)):
            print "Erreur de définition ! Le radicande doit être positif et l'indice un nombre entier !"
        self.radicande = radicande
        self.indice = indice # Nombre entier
        self.coeff = coeff # Coeff devant la racine
        self.simplifie()

    def __add__(self, other):
        if not (isinstance(other, Racine)):
            return str(self) + " + " + str(other)
        if (self.radicande == other.radicande) and (self.indice == other.indice):
            return Racine(self.radicande, self.indice, self.coeff + other.coeff)
        else:
            return str(self) + " + " + str(other)

    def __radd__(self, other):
        return self + other

    def __sub__(self, other):
        if not (isinstance(other, Racine)):
            return str(self) + " + " + str(other)
        if (self.radicande == other.radicande) and (self.indice == other.indice):
            return Racine(self.radicande, self.indice, self.coeff - other.coeff)
        else:
            return str(self) + " - " + str(other)

    def __rsub__(self, other):
        return -(self - other)

    def __mul__(self, other):
        if (isinstance(other, float)) or (isinstance(other, int)):
            return Racine(self.radicande, self.indice, self.coeff * other)
        elif self.indice == other.indice:
            return Racine(self.radicande * other.radicande, self.indice, self.coeff * other.coeff)
        else:
            return str(self) + ' x ' + str(other)

    def __rmul__(self, other):
        return self * other

    def __div__(self, other):
        if (isinstance(other, float)) or (isinstance(other, int)):
            return Racine(self.radicande, self.indice, self.coeff / other)
        elif self.indice == other.indice:
            return Racine(self.radicande / float(other.radicande), self.indice, self.coeff / float(other.coeff))
        else:
            return str(self) + ' / ' + str(other)

    def __rdiv__(self, other):
        if (isinstance(other, float)) or (isinstance(other, int)):
            return Racine(self.radicande, self.indice, other / float(self.coeff * self.radicande))
        elif self.indice == other.indice:
            return Racine(other.radicande / float(self.radicande), self.indice, other.coeff / float(self.coeff))
        else:
            return str(other) + ' / ' + str(self)
    

    def __str__(self):
        if self.coeff == 1:
            coeff = ''
        else:
            coeff = str(self.coeff) + ' '
        if self.radicande == 1:
            racine = ''
            radicande = ''
        elif self.radicande == 0:
            return str(0)
        else:
            racine = '(' + str(self.indice) + ')\/ '
            radicande = str(self.radicande)
        return coeff + racine + radicande

    def simplifie(self):
        facteurs = factor(self.radicande)
        for element in facteurs:
            if facteurs.count(element) % self.indice == 0:
                self.coeff *= element
                for n in range(self.indice):
                    facteurs.remove(element)
                self.radicande = self.radicande / (element**(self.indice))

        return False
                