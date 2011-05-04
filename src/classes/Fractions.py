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

import string
import math
import os
from ..outils import Arithmetique

class Fractions:

    """Classe permettant d'opérer sur les fractions.
    Une fraction est stockée ainsi : (numérateur, dénominateur)"""

    def __init__(self, n, d=1):
        self.numerateur = self.n = n
        self.denominateur = self.d = d


    def simplifie(self):

        # retourne la fraction rendue irréductible

        pgcd = Arithmetique.pgcd(self.n, self.d)
        return Fractions(self.n // pgcd, self.d // pgcd)

    def __str__(self):
        return self.TeX(signe=0,coef=None)
    def TeX(self, signe=0, coef=None):
        """Permet d'écrire une fraction au format TeX.

        @param signe: Si vrai, écrit la fraction avec un dénominateur positif
        @param coef: Multiplie le numérateur et le dénominateur par un même nombre
        """

        if signe:
            (self.n, self.d) = ((self.n * abs(self.d)) // self.d, abs(self.d))
        if self.n:
            if coef and coef != 1:
                text = "\\dfrac{%s_{\\times %s}}{%s_{\\times %s}}" % (self.n,
                        coef, self.d, coef)
            elif self.d != 1:
                text = "\\dfrac{%s}{%s}" % (self.n, self.d)
            else:
                text = "%s" % self.n
        else:
            text = "0"
        return text

    def TeXProduit(self, fraction):
        if self.d < 0:
            (self.n, self.d) = (-self.n, -self.d)
        if fraction.d < 0:
            (fraction.n, fraction.d) = (-fraction.n, -fraction.d)
        c1 = abs(Arithmetique.pgcd(self.n, fraction.d))
        c2 = abs(Arithmetique.pgcd(self.d, fraction.n))
        simplifiable = 0  # permet de savoir si on a simplifiée le produit
        if c1 > 1:
            n1 = "%s \\times \\cancel{%s}" % (self.n // c1, c1)
            d2 = "%s \\times \\cancel{%s}" % (fraction.d // c1, c1)
        else:
            n1 = self.n
            d2 = fraction.d
        if c2 > 1:
            d1 = "%s \\times \\bcancel{%s}" % (self.d // c2, c2)
            n2 = "%s \\times \\bcancel{%s}" % (fraction.n // c2, c2)
        else:
            d1 = self.d
            n2 = fraction.n
        return "%s \\times %s" % (Fractions.TeX(Fractions(n1, d1), signe=
                                  None), Fractions.TeX(Fractions(n2, d2),
                                  signe=None))

    def TeXSimplifie(self):
        frs = Fractions.simplifie(self)
        coef = abs(self.n // frs.n)
        if coef > 1:
            texte = \
                "\\dfrac{%s_{\\times \\cancel %s}}{%s_{\\times \\cancel %s}}" % \
                (self.n // coef, coef, self.d // coef, coef)
        else:
            texte = Fractions.TeX(self, signe=None)
        return texte

    def __add__(self, fraction):
        if (isinstance(fraction,int) or isinstance(fraction,float)):
            fraction=Fractions(fraction)
        if isinstance(fraction,Fractions):
            ppcm = Arithmetique.ppcm(self.d, fraction.d)
            return Fractions((self.n * ppcm) // self.d + (fraction.n * ppcm) //
                         fraction.d, ppcm)
        else:
            return fraction+self

    def __radd__(self,other):
        return self+other

    def __sub__(self, fraction):
        return self + (-fraction)
    def __rsub__(self,other):
        return (-self) + other

    def __mul__(self, fraction):
        if (isinstance(fraction,int) or isinstance(fraction,float)):
            fraction=Fractions(fraction)
        if isinstance(fraction,Fractions):
            return Fractions(self.n * fraction.n, self.d * fraction.d)
        else:
            return fraction*self

    def __rmul__(self,other):
        return self*other

    #def __truediv__(self, fraction): # pour Python 3
    def __div__(self, fraction):
            if (isinstance(fraction,int) or isinstance(fraction,float)):
                fraction=Fractions(fraction)
            if isinstance(fraction,Fractions):
                return Fractions(self.n * fraction.d, self.d * fraction.n)
            else:
                return self*~fraction
    def __rdiv__(self,other):
        return other*~self
    def __invert__(self):
        return Fractions(self.d,self.n)
    def __neg__(self):
        return Fractions(-self.n,self.d)

    def __pow__(self,n):
        result=1
        for i in range(n):
            result=result*self
        return result
    def __trunc__(self):
        return self.n//self.d

    def __lt__(self, other):
        if isinstance(other,int) or isinstance(other,float):
            other=Fractions(other)
        if other.d*self.d > 0:
            return self.n*other.d < self.d * other.n
        else :
            return not(self.n*other.d < self.d * other.n)

    def __le__(self, other):
        if isinstance(other,int) or isinstance(other,float):
            other=Fractions(other)
        if other.d*self.d > 0:
            return self.n*other.d <= self.d * other.n
        else :
            return not(self.n*other.d <= self.d * other.n)

    def __eq__(self, other):
        if isinstance(other,int) or isinstance(other,float):
            other=Fractions(other)
        if isinstance(other,Fractions):
            return self.n*other.d == self.d * other.n

    def __ne__(self, other):
        if isinstance(other,int) or isinstance(other,float):
            other=Fractions(other)
        return self.n*other.d != self.d * other.n

    def __gt__(self, other):
        if isinstance(other,int) or isinstance(other,float):
            other=Fractions(other)
        if other.d*self.d > 0:
            return self.n*other.d > self.d * other.n
        else :
            return not(self.n*other.d > self.d * other.n)

    def __ge__(self, other):
        if isinstance(other,int) or isinstance(other,float):
            other=Fractions(other)
        if other.d*self.d > 0:
            return self.n*other.d >= self.d * other.n
        else :
            return not(self.n*other.d >= self.d * other.n)

    def __float__(self):
        return 1.0*self.n/self.d

    def __int__(self):
        try:
          assert (self.n / self.d == int(self.n / self.d)), 'La fraction n\'est pas un nombre entier !'
          return int(self.n)
        except AssertionError, args:
          print '%s: %s' % (args.__class__.__name__, args)


