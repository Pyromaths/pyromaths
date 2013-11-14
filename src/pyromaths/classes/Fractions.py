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

from pyromaths.outils.Arithmetique import pgcd, ppcm

class Fraction():
    """Cette classe crée la notion de fractions.
    code permet de préciser si une décomposition a pour objectif une mise au
    même dénominateur 'r' ou une simplification 's'

        >>> from pyromaths.Fractions.Fractions import Fraction
        >>> Fraction(5,6)
        Fraction(5, 6)
        >>> Fraction('x',6)
        Fraction("x", 6)
        >>> Fraction(3.4)
        Fraction(34, 10)

    """
    def __init__(self, n, d = 1, code = ""):
        if isinstance(n, float):
            e = len(str(n).partition('.')[2])
            n = int(n * 10**e)
            d = d * 10**e
        self.n = n
        if n == 0 :
            self.d = 1
        else:
            self.d = d
        self.code = code


    def __str__(self):
        """**str**\ (*object*)

        Renvoie une version LaTeX de la :class:`Fraction`.
            >>> from pyromaths.classes.Fractions import Fraction
            >>> str(Fraction(5,6))
            '\\\\dfrac{5}{6}'
            >>> str(Fraction('-72*2', '11*2', 'r'))
            '\\\\dfrac{-72_{\\\\times 2}}{11_{\\\\times 2}}'
            >>> str(Fraction('-72*2', '11*2', 's'))
            '\\\\dfrac{-72\\\\times \\\\cancel{2}}{11\\\\times \\\\cancel{2}}'

        :rtype: string
        """
        if self.n:
            if self.d == 1:
                text = "%s" % self.n
            elif self.code == "r":
                text = "\\dfrac{%s_{\\times %s}}" % (tuple(self.n.split("*")))
                text += "{%s_{\\times %s}}" % (tuple(self.d.split('*')))
            elif self.code == "s":
                ln = self.n.split('*')
                ld = self.d.split('*')
                for i in range(len(ln)):
                    if ld.count(ln[i]):
                        ld[ld.index(ln[i])] = "\\cancel{%s}" % ln[i]
                        ln[i] = "\\cancel{%s}" % ln[i]
                text = "\\dfrac{%s}{%s}" % ("\\times ".join(ln), "\\times ".join(ld))
            else:
                text = "\\dfrac{%s}{%s}" % (self.n, self.d)
        else:
            text = "0"
        return text

    def __repr__(self):
        """**repr**\ (*object*)

        Renvoie une chaîne de caractère représentant une :mod:`Fraction`
        évaluable pour créer un :mod:`Fraction`.

            >>> from pyromaths.classes.Fractions import Fraction
            >>> repr(Fraction(5,6))
            'Fraction(5, 6)'
            >>> repr(Fraction('-72*2', '11*2', 'r'))
            'Fraction("-72*2", "11*2", "r")'
            >>> repr(Fraction('-72*2', '11*2', 's'))
            'Fraction("-72*2", "11*2", "s")'

        :rtype: string
        """
        if isinstance(self.n, str):
            num = "\"%s\"" % self.n
        else:
            num = "%s" % self.n
        if isinstance(self.d, str):
            den = "\"%s\"" % self.d
        else:
            den = "%s" % self.d
        if self.code:
            return "Fraction(%s, %s, \"%s\")" % (num, den, self.code)
        else:
            return "Fraction(%s, %s)" % (num, den)

    def __add__(self, other):
        """*object*\ .\ **__add__**\ (*other*)

        ``p.__add__(q)`` est équivalent à ``p + q``  calcule la somme de deux fractions.

        *other* peut être une chaîne représentant une fraction, un entier ou un réel.

        >>> from pyromaths.classes.Fractions import Fraction
        >>> Fraction(2,5) + Fraction(2,10)
        'Fraction("2*2", "5*2", "r")+Fraction(2, 10)'
        >>> Fraction(2,20) + Fraction(2,10)
        'Fraction(2, 20)+Fraction("2*2", "10*2", "r")'
        >>> Fraction(5,10) + Fraction(2,10)
        Fraction(7, 10)
        >>> Fraction(5,7) + Fraction(2,10)
        'Fraction("5*10", "7*10", "r")+Fraction("2*7", "10*7", "r")'

        :param: other
        :type: Fraction ou string
        :rtype: Fraction ou string

        **TODO :** Attention, 1+3/4 donne 1*4/1*4 + 3/4 à la place de 4/4+3/4. À corriger
        """
        if (isinstance(other,int) or isinstance(other,float)):
            other=Fraction(other)
        leppcm = ppcm(self.d, other.d)
        if other.d == self.d:
            return Fraction(self.n + other.n, leppcm)
        else:
            if leppcm != self.d and leppcm != other.d:
                return "Fraction(\"%s*%s\", \"%s*%s\", \"r\")+Fraction(\"%s*%s\", \"%s*%s\", \"r\")" % \
                    (self.n, leppcm/self.d, self.d, leppcm/self.d, other.n, leppcm/other.d, other.d, leppcm/other.d)
            elif leppcm != other.d:
                return "Fraction(%s, %s)+Fraction(\"%s*%s\", \"%s*%s\", \"r\")" % \
                    (self.n, self.d, other.n, leppcm/other.d, other.d, leppcm/other.d)
            else:
                return "Fraction(\"%s*%s\", \"%s*%s\", \"r\")+Fraction(%s, %s)" % \
                    (self.n, leppcm/self.d, self.d, leppcm/self.d, other.n, other.d)

    def __radd__(self,other):
        """*object*\ .\ **__radd__**\ (*other*)

        ``p.__radd__(q)`` est équivalent à ``p + q``  calcule la somme de l'objet p avec la fraction q

        *other* peut être une chaîne représentant un entier ou un réel.

        >>> from pyromaths.classes.Fractions import Fraction
        >>> 3 + Fraction(2,5)
        'Fraction("3*5", "1*5", "r")+Fraction(2, 5)'

        :param: other
        :type: real ou integer
        :rtype: string
        """
        return Fraction(other)+self

    def __sub__(self, other):
        """*object*\ .\ **__sub__**\ (*other*)

        ``p.__sub__(q)`` est équivalent à ``p - q``  calcule la différence de deux fractions.

        *other* peut être une chaîne représentant une fraction, un entier ou un réel.

        Pour plus de détails, voir :py:func:`__add__`"""
#         return self + (-fraction)
        if (isinstance(other,int) or isinstance(other,float)):
            other=Fraction(other)
        leppcm = ppcm(self.d, other.d)
        if other.d == self.d:
            return Fraction(self.n - other.n, leppcm)
        else:
            if leppcm != self.d and leppcm != other.d:
                return "Fraction(\"%s*%s\", \"%s*%s\", \"r\")-Fraction(\"%s*%s\", \"%s*%s\", \"r\")" % \
                    (self.n, leppcm/self.d, self.d, leppcm/self.d, other.n, leppcm/other.d, other.d, leppcm/other.d)
            elif leppcm != other.d:
                return "Fraction(%s, %s)-Fraction(\"%s*%s\", \"%s*%s\", \"r\")" % \
                    (self.n, self.d, other.n, leppcm/other.d, other.d, leppcm/other.d)
            else:
                return "Fraction(\"%s*%s\", \"%s*%s\", \"r\")-Fraction(%s, %s)" % \
                    (self.n, leppcm/self.d, self.d, leppcm/self.d, other.n, other.d)

    def __rsub__(self,other):
        """*object*\ .\ **__rsub__**\ (*other*)

        ``p.__rsub__(q)`` est équivalent à ``p - q``  calcule la différence de l'objet p par la fraction q.

        *other* peut être un entier ou un réel.

        Pour plus de détails, voir :py:func:`__radd__`"""
        return Fraction(other)-self

    def __mul__(self, other):
        """*object*\ .\ **__mul__**\ (*other*)

        ``p.__mul__(q)`` est équivalent à ``p * q``  calcule le produit deux fractions.

        *other* peut être une chaîne représentant une fraction, un entier ou un réel.

        >>> from pyromaths.classes.Fractions import Fraction
        >>> Fraction(2,5) * Fraction(2,10)
        'Fraction("2*2", "5*2*5", "s")'
        >>> Fraction(2,5) * 4
        Fraction(8, 5)
        >>> Fraction(63,20) * Fraction(8,27)
        'Fraction("9*7*4*2", "4*5*9*3", "s")'


        :param: other
        :type: Fraction ou string
        :rtype: Fraction ou string
        """
        if (isinstance(other,int) or isinstance(other,float)):
            other=Fraction(other)
        s = pgcd(self.n*other.n, self.d*other.d)
        if s - 1:
            n1, d1 = pgcd(self.n, s), pgcd(self.d, s)
            n2, d2 = s / n1, s / d1
            t = "Fraction("
            if n1 == 1 or n1 == self.n:
                t += str(self.n)
            else:
                t += "%s*%s" % (n1, self.n/n1)
            if n2 == 1 or n2 == other.n:
                t += "*%s, " % other.n
            else:
                t += "*%s*%s, " % (n2, other.n/n2)
            if d1 == 1 or d1 == self.d:
                t += str(self.d)
            else:
                t += "%s*%s" % (d1, self.d/d1)
            if d2 == 1 or d2 == other.d:
                t += "*%s, \"s\")" % other.d
            else:
                t += "*%s*%s, \"s\")" % (d2, other.d/d2)
            n1, n2 = t[9:-6].split(",")
            if "*" in n1: n1 = "\"%s\"" % n1.strip()
            if "*" in n2: n2 = "\"%s\"" % n2.strip()
            t = "Fraction(%s, %s, \"s\")" % (n1, n2)
            return t
        else:
            return Fraction(self.n * other.n, self.d * other.d)

    def __rmul__(self,other):
        """*object*\ .\ **__rmul__**\ (*other*)

        ``p.__rmul__(q)`` est équivalent à ``p * q``  calcule le produit de l'objet p par la fraction q.

        *other* peut être un entier ou un réel.

        Pour plus de détails, voir :py:func:`__radd__`"""
        return Fraction(other) * self

    #def __truediv__(self, fraction): # pour Python 3
    def __div__(self, other):
        """*object*\ .\ **__div__**\ (*other*)

        ``p.__div__(q)`` est équivalent à ``p / q``  calcule le quotient de deux fractions.

        *other* peut être une chaîne représentant une fraction, un entier ou un réel.

        >>> from pyromaths.classes.Fractions import Fraction
        >>> Fraction(2,5) / Fraction(10,2)
        'Fraction(2, 5)*Fraction(2, 10)'
        >>> Fraction(2,5) / 4
        'Fraction(2, 5)*Fraction(1, 4)'

        :param: other
        :type: Fraction ou string
        :rtype: Fraction ou string
        """
        if (isinstance(other,int) or isinstance(other,float)):
            other=Fraction(other)
        return "%r*%r" % (self, ~other)

    def __rdiv__(self,other):
        """*object*\ .\ **__rdiv__**\ (*other*)

        ``p.__rdiv__(q)`` est équivalent à ``p / q``  calcule le produit de l'objet p par la fraction q.

        *other* peut être un entier ou un réel.

        Pour plus de détails, voir :py:func:`__radd__`"""
        return "%r*%r" % (self, ~other)

    def __invert__(self):
        """**__invert__**\ (*self*)

        ``__invert__(p)`` est équivalent à ``~p`` calcule l'inverse de la fraction p.

        >>> from pyromaths.classes.Fractions import Fraction
        >>> ~Fraction(8,27)
        Fraction(27, 8, )
        """
        return Fraction(self.d,self.n)

    def __neg__(self):
        """**__neg__**\ (*self*)

        ``__neg__(p)`` est équivalent à ``-p`` calcule l'opposé de la fraction p.

        >>> from pyromaths.classes.Fractions import Fraction
        >>> -Fraction(8,27)
        Fraction(-8, 27)
        """
        return Fraction(-self.n,self.d)

    def __pow__(self,n):
        """**__pow__**\ (*self*, *n*)

        ``p__pow__(q)`` est équivalent à ``p**q`` calcule p à la puissance q.

        >>> from pyromaths.classes.Fractions import Fraction
        >>> Fraction(2,3)**4
        Fraction(16, 81)

        :param: n
        :type: Integer
        :rtype: Fraction
        """
        return Fraction(self.n**n, self.d**n)

    def __trunc__(self):
        return self.n//self.d

    def __lt__(self, other):
        if isinstance(other,int) or isinstance(other,float):
            other=Fraction(other)
        if other.d*self.d > 0:
            return self.n*other.d < self.d * other.n
        else :
            return not(self.n*other.d < self.d * other.n)

    def __le__(self, other):
        if isinstance(other,int) or isinstance(other,float):
            other=Fraction(other)
        if other.d*self.d > 0:
            return self.n*other.d <= self.d * other.n
        else :
            return not(self.n*other.d <= self.d * other.n)

    def __eq__(self, other):
        if isinstance(other,int) or isinstance(other,float):
            other=Fraction(other)
        if isinstance(other,Fraction):
            return self.n*other.d == self.d * other.n

    def __ne__(self, other):
        if isinstance(other,int) or isinstance(other,float):
            other=Fraction(other)
        return self.n*other.d != self.d * other.n

    def __gt__(self, other):
        if isinstance(other,int) or isinstance(other,float):
            other=Fraction(other)
        if other.d*self.d > 0:
            return self.n*other.d > self.d * other.n
        else :
            return not(self.n*other.d > self.d * other.n)

    def __ge__(self, other):
        if isinstance(other,int) or isinstance(other,float):
            other=Fraction(other)
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

    def reduit(self):
        """**reduit**\ (*object*)

        Retourne une version réduite de la fraction, ie calcule le numérateur et le dénominateur

            >>> from pyromaths.classes.Fractions import Fraction
            >>> Fraction.reduit(Fraction(2*4,5*4))
            Fraction(8, 20)
            >>> Fraction.reduit(Fraction('2*4', '5*4'))
            Fraction(8, 20)

        :param type: Fraction
        :rtype: Fraction
        """
        if isinstance(self.n, str): self.n = eval(self.n)
        if isinstance(self.d, str): self.d = eval(self.d)
        return Fraction(self.n, self.d)

    def simplifie(self):
        """**simplifie**\ (*object*)

        Retourne une version irréductible de la fraction

            >>> from pyromaths.classes.Fractions import Fraction
            >>> Fraction.simplifie(Fraction(2*4,5*4))
            Fraction(2, 5)
            >>> Fraction.simplifie(Fraction('2*4','5*4'))
            Fraction(2, 5)

        :param type: Fraction
        :rtype: Fraction
        """
        if isinstance(self.n, str): self.n = eval(self.n)
        if isinstance(self.d, str): self.d = eval(self.d)
        s = pgcd(self.n, self.d)
        return Fraction(self.n // s, self.d // s)

    def decompose(self):
        """**decompose**\ (*object*)

        Retourne une décomposition de la fraction afin de la simplifier

            >>> from pyromaths.classes.Fractions import Fraction
            >>> Fraction.decompose(Fraction(8,20))
            'Fraction("2*4","5*4", "s")'

        :param type: Fraction
        :rtype: Fraction ou None
        """
        if isinstance(self.n, str): self.n = eval(self.n)
        if isinstance(self.d, str): self.d = eval(self.d)
        if self.d == self.n:
            return "1"
        else:
            lepgcd = pgcd(self.n, self.d)
            if lepgcd == 1:
                return repr(self)
            else:
                return "Fraction(\"%s*%s\",\"%s*%s\", \"s\")" % (self.n // lepgcd, lepgcd, self.d // lepgcd, lepgcd)
