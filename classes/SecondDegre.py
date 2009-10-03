# -*- coding: utf-8 -*-

import random
from outils/Arithmetique import factorise, carrerise
from math import sqrt
from outils/Affichage import suppr0, suppr0list

class Poly2:
    """Classe pour les polynômes du second degré."""
    def __init__(self, a, b, c):
        if a == 0:
            print "Erreur de définition ! a doit être différent de 0."
        self.a = a
        self.b = b
        self.c = c
        self.delta = suppr0(b**2 - 4*a*c)
        if self.delta > 0:
            self.signedelta = "strictement positif"
            self.nbrac = 2
        elif self.delta < 0:
            self.signedelta = "strictement négatif"
            self.nbrac = 0
        else:
            self.signedelta = "nul"
            self.nbrac = 1

    def __add__(self, other):
        return poly2(self.a + other.a, self.b + other.b, self.c + other.c)

    def __radd__(self, other):
        return poly2(self.a + other.a, self.b + other.b, self.c + other.c)

    def __sub__(self, other):
        return poly2(self.a - other.a, self.b - other.b, self.c - other.c)

    def __rsub__(self, other):
        return poly2(self.a - other.a, self.b - other.b, self.c - other.c)

    def __str__(self):
        if self.b<=0:
            sep1 = ''
        else:
            sep1 = '+'
        if self.c<=0:
            sep2 = ''
        else:
            sep2 = '+'
        if self.a == 1:
            a1 = ''
        else:
            a1 = str(suppr0(self.a))
        if self.b == 1:
            b1 = ''
        else:
            b1 = str(suppr0(self.b))
        if self.b == 0:
            deg1 = ''
            b1 = ''
        else:
            deg1 = 'x'
        return a1 + 'x^2' + sep1 + b1 + deg1 + sep2 + str(suppr0(self.c))

    def print_signe(self, signe):
        return str(self) + " " + signe + " 0"

