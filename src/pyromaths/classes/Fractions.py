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
from collections import Counter
from pyromaths.classes.SquareRoot import SquareRoot
from pyromaths.outils.Priorites3 import EstNombre, texify
from __builtin__ import str
from functools import reduce

class Fraction():
    """Cette classe crée la notion de fractions.
    code permet de préciser si une décomposition a pour objectif une mise au
    même dénominateur 'r' ou une simplification 's'

    >>> from pyromaths.classes.Fractions import Fraction
    >>> repr(Fraction(5,6))
    Fraction(5, 6)
    >>> repr(Fraction('x',6))
    Fraction("x", 6)
    >>> repr(Fraction(3.4))
    Fraction(34, 10)
    >>> repr(Fraction(3.0, 4.0))
    Fraction(3, 4)
    >>> repr(Fraction(Fraction(1,3)))
    Fraction(1, 3)

    """
    def __init__(self, n, d=1, code=""):
        from pyromaths.classes.PolynomesCollege import Polynome
        if isinstance(n, float) and abs(n) != float("inf"):
            e = len(str(n).partition('.')[2].rstrip('0'))
            n = int(n * 10 ** e)
            d = d * 10 ** e
        if isinstance(d, float):
            e = len(str(d).partition('.')[2].rstrip('0'))
            d = int(d * 10 ** e)
            n = n * 10 ** e
        self.n = n
        if n == 0 :
            self.d = 1
        else:
            self.d = d
        self.code = code
        if isinstance(n, Fraction) and d == 1 and code == "":
            # Fraction(Fraction(1, 3)) renvoie Fraction(1, 3)
            self.n = n.n
            self.d = n.d
            self.code = n.code


    def __str__(self):
        r"""**str**\ (*object*)

        Renvoie une version LaTeX de la :class:`Fraction`.
            >>> from pyromaths.classes.Fractions import Fraction
            >>> str(Fraction(8,1))
            8
            >>> str(Fraction(5,6))
            \dfrac{5}{6}
            >>> str(Fraction('-5*2', '3*2', 'r'))
            \dfrac{-5_{\times 2}}{3_{\times 2}}
            >>> str(Fraction('5*-7*2', '11*2*5', 's'))
            \dfrac{\cancel{5}\times \left( -7\right) \times \cancel{2}}{11\times \cancel{2}\times \cancel{5}}
            >>> str(Fraction('-144', '22', 's'))
            \dfrac{-72\times \cancel{2}}{11\times \cancel{2}}
            >>> from pyromaths.classes.SquareRoot import SquareRoot
            >>> str(Fraction(SquareRoot([[-10, None], [-1, 80]]), -2))
            \dfrac{-10-\sqrt{80}}{-2}
            >>> str(Fraction(SquareRoot([[-10, None], [-4, 5]]), -2, 's'))
            \dfrac{\left( 5+2\,\sqrt{5}\right) \times \cancel{-2}}{1\times \cancel{-2}}

        :rtype: string
        """
        from pyromaths.outils.Priorites3 import splitting
        #=======================================================================
        # print (repr(self))
        #=======================================================================
        if self.n == 0 or self.n == '0':
            return '0'
        lnum, lden = [], []
        if isinstance(self.n, str): lnum = splitting(self.n)
        if isinstance(self.d, str): lden = splitting(self.d)
        if len(lnum) == 1: self.n, lnum = eval(self.n), []
        if len(lden) == 1: self.d, lden = eval(self.d), []
        if self.d == 1:
            return (str(self.n), texify([lnum])[0])[lnum != []]
        if self.code == "r":
            # lnum et lden doivent être définis et se terminer par [..., '*', valeur]
            if not lnum or not lden or lnum[-2:] != lden[-2:]:
                raise ValueError(u'Mauvais usage de l\'étiquettes "r" dans %r' % self)
            lden[-2], lden[-1], lnum[-2], lnum[-1] = [lden[-2], 'indice'], [lden[-1], 'indice'], [lnum[-2], 'indice'], [lnum[-1], 'indice']
            return '\\dfrac{%s}{%s}' % (texify([lnum])[0], texify([lden])[0])
        if self.code == "s":
            if isinstance(self.n, (int, float, SquareRoot)) and isinstance(self.d, (int, float, SquareRoot)):
                lepgcd = pgcd(self.n, self.d)
                lnum, lden = [repr(self.n // lepgcd), '*', [str(lepgcd), 'cancel']], [repr(self.d // lepgcd), '*', [str(lepgcd), 'cancel']]
            else:
                for i in range(len(lnum)):
                    if lnum[i] != '*' and lden.count(lnum[i]):
                        # On doit simplifier la fraction par ce nombre
                        j = lden.index(lnum[i])
                        lden[j] = [lden[j], 'cancel']
                        lnum[i] = [lnum[i], 'cancel']
            return '\\dfrac{%s}{%s}' % (texify([lnum])[0], texify([lden])[0])
        s = r'\dfrac'
        s += '{%s}' % (self.n, texify([lnum])[0])[lnum != []]
        s += '{%s}' % (self.d, texify([lden])[0])[lden != []]
        return s


    def __repr__(self):
        """**repr**\ (*object*)

        Renvoie une chaîne de caractère représentant une :mod:`Fraction`
        évaluable pour créer un :mod:`Fraction`.

            >>> from pyromaths.classes.Fractions import Fraction
            >>> repr(Fraction(5,6))
            Fraction(5, 6)
            >>> repr(Fraction('-72*2', '11*2', 'r'))
            Fraction("-72*2", "11*2", "r")
            >>> repr(Fraction('-72*2', '11*2', 's'))
            Fraction("-72*2", "11*2", "s")

        :rtype: string
        """
        if isinstance(self.n, str):
            num = "\"%s\"" % self.n
        else:
            num = "%r" % self.n
        if isinstance(self.d, str):
            den = "\"%s\"" % self.d
        else:
            den = "%r" % self.d
        if self.code:
            return "Fraction(%s, %s, \"%s\")" % (num, den, self.code)
        else:
            return "Fraction(%s, %s)" % (num, den)

    def __abs__(self):
        """Renvoie la valeur absolue d'une fraction
        """
        self = Fraction(self.n, self.d)
        if self.n * self.d > 0:
            return self
        else:
            return -self

    def __add__(self, *others):
        """*object*\ .\ **__add__**\ (*other*)

        ``p.__add__(q)`` est équivalent à ``p + q``  calcule la somme de deux fractions.

        *other* peut être une chaîne représentant une fraction, un entier ou un réel.

        >>> from pyromaths.classes.Fractions import Fraction
        >>> Fraction(2,5) + Fraction(2,10)
        Fraction("2*2", "5*2", "r")+Fraction(2, 10)
        >>> Fraction(2,20) + Fraction(2,10)
        Fraction(2, 20)+Fraction("2*2", "10*2", "r")
        >>> repr(Fraction(5,10) + Fraction(2,10))
        Fraction(7, 10)
        >>> Fraction(5,7) + Fraction(2,10)
        Fraction("5*10", "7*10", "r")+Fraction("2*7", "10*7", "r")

        :param: other
        :type: Fraction ou string
        :rtype: Fraction ou string

        **TODO :** Attention, 1+3/4 donne 1*4/1*4 + 3/4 à la place de 4/4+3/4. À corriger
        """
        from pyromaths.classes.PolynomesCollege import Polynome
        lother, lden, traiter = [], [], False
        if self.code: traiter = True
        details, var = '', ''
        for other in others:
            if other == 0:
                pass
            elif isinstance(other, Polynome):
                var = other.var
                if details != 0  : details = min(details, other.details)
                else: details = other.details
                lother.append(other)
            elif isinstance(other, (int, float)):
                    lother.append(Fraction(other))
                    lden.append(1)
            elif isinstance(other, Fraction):
                lother.append(other)
                if other.code: traiter = True
                try: lden.append(eval(other.d))
                except TypeError: lden.append(other.d)
            else:
                raise ValueError(u'Format incorrect : %s' % (other))
        if var:
            self = Polynome([[self, 0]], var, details)
            for i in range(len(lother)):
                if not isinstance(lother[i], Polynome): lother[i] = Polynome([[lother[i], 0]], var, details)
            return Polynome.__add__(self, *lother)

        if traiter:
            lfrac = [repr(self.traitement())]
            for other in lother:
                lfrac.append(repr(other.traitement()))
            return "+".join(lfrac)
        try: self.d = eval(self.d)
        except TypeError: pass
        if not lother: return self  # On a ajouté 0
        leppcm = ppcm(self.d, *lden)
        if self.d == leppcm:
            # Vérifions si toutes les fractions ont le même dénominateur
            d = Counter(lden)
            if d[leppcm] == len(lden):
                try: num = eval(self.n)
                except TypeError: num = self.n
                for other in lother:
                    try: num += eval(other.n)
                    except TypeError: num += other.n
                return Fraction(num, leppcm)
        if self.n: lfrac = [repr(self.choix_denominateur(leppcm))]
        else: lfrac = []
        for other in lother: lfrac.append(repr(other.choix_denominateur(leppcm)))
        if lfrac: return "+".join(lfrac)
        else: return "0"

    def choix_denominateur(self, denominateur):
        """
        Écrit la fraction self avec le dénominateur denominateur
        """
        if denominateur != self.d:
            return Fraction("%s*%s" % (self.n, denominateur / self.d), "%s*%s" % (self.d, denominateur / self.d), "r")
        else:
            return self

    def __radd__(self, other):
        """*object*\ .\ **__radd__**\ (*other*)

        ``p.__radd__(q)`` est équivalent à ``p + q``  calcule la somme de l'objet p avec la fraction q

        *other* peut être une chaîne représentant un entier ou un réel.

        >>> from pyromaths.classes.Fractions import Fraction
        >>> 3 + Fraction(2,5)
        Fraction("3*5", "1*5", "r")+Fraction(2, 5)

        :param: other
        :type: real ou integer
        :rtype: string
        """
        if other == 0 : return self
        if self == 0 : return other
        if isinstance(other, str):
            other = eval(other)
            if isinstance(other, str): return '%s+%r' % (other, self)
            else: return '%r+%r' % (other, self)
        return Fraction(other) + self

    def __sub__(self, *others):
        """*object*\ .\ **__sub__**\ (*other*)

        ``p.__sub__(q)`` est équivalent à ``p - q``  calcule la différence de deux fractions.

        *other* peut être une chaîne représentant une fraction, un entier ou un réel.

        Pour plus de détails, voir :py:func:`__add__`"""
        from pyromaths.classes.PolynomesCollege import Polynome
        lother, lden, traiter = [], [], False
        if self.code: traiter = True
        details, var = True, ''
        for other in others:
            if other == 0:
                pass
            elif isinstance(other, Polynome):
                var = other.var
                if details != 0 : details = min(details, other.details)
                else: details = other.details
                lother.append(other)
            elif isinstance(other, (int, float)):
                    lother.append(Fraction(other))
                    lden.append(1)
            elif isinstance(other, Fraction):
                lother.append(other)
                if other.code: traiter = True
                try: lden.append(eval(other.d))
                except TypeError: lden.append(other.d)
            else:
                raise ValueError(u'Format incorrect : %s' % (other))
        if var:
            self = Polynome([[self, 0]], var, details)
            for i in range(len(lother)):
                if not isinstance(lother[i], Polynome): lother[i] = Polynome([[lother[i], 0]], var, details)
            return Polynome.__sub__(self, *lother)

        if traiter:
            lfrac = [repr(self.traitement())]
            for other in lother:
                lfrac.append(repr(other.traitement()))
            return "-".join(lfrac)
        try: self.d = eval(self.d)
        except TypeError: pass
        if not lother: return self  # On a ajouté 0
        leppcm = ppcm(self.d, *lden)
        if self.d == leppcm:
            # Vérifions si toutes les fractions ont le même dénominateur
            d = Counter(lden)
            if d[leppcm] == len(lden):
                try: num = eval(self.n)
                except TypeError: num = self.n
                for other in lother:
                    try: num += -eval(other.n)
                    except TypeError: num += -other.n
                return Fraction(num, leppcm)
        if self.n: lfrac = [repr(self.choix_denominateur(leppcm))]
        else: lfrac = []
        for other in lother:
            if lfrac: lfrac.append(repr(other.choix_denominateur(leppcm)))
            else: lfrac.append(repr(-other.choix_denominateur(leppcm)))
            # On effectue Fraction(0,3)-Fraction(2,3), il faut donc prendre l'opposé de Fraction(2,3), puisque Fraction(0,3) a été supprimée
        if lfrac: return "-".join(lfrac)
        else: return "0"

    def __rsub__(self, other):
        """*object*\ .\ **__rsub__**\ (*other*)

        ``p.__rsub__(q)`` est équivalent à ``p - q``  calcule la différence de l'objet p par la fraction q.

        *other* peut être un entier ou un réel.

        Pour plus de détails, voir :py:func:`__radd__`"""
        return Fraction(other) - self

    def __mul__(self, *others):
        """*object*\ .\ **__mul__**\ (*other*)

        ``p.__mul__(q)`` est équivalent à ``p * q``  calcule le produit deux fractions.

        *other* peut être une chaîne représentant une fraction, un entier ou un réel.

        >>> from pyromaths.classes.Fractions import Fraction
        >>> repr(Fraction(2,5) * Fraction(2,10))
        Fraction("2*2", "5*2*5", "s")
        >>> repr(Fraction(2,5) * 4)
        Fraction(8, 5)
        >>> repr(Fraction(63,20) * Fraction(8,27))
        Fraction("9*7*4*2", "4*5*9*3", "s")
        >>> repr(Fraction(24,12) * 12)
        Fraction("24*12", "12*1", "s")
        >>> repr(12*Fraction(24,12))
        Fraction("12*24", "1*12", "s")

        :param: other
        :type: Fraction ou string
        :rtype: Fraction ou string
        """
        from pyromaths.classes.PolynomesCollege import Polynome
        from pyromaths.classes.Polynome import Polynome as PolynomeLycee
        from .Racine import RacineDegre2

        if self == 0: return 0
        self = Fraction(self.n, self.d)  # Pour contourner le cas où self = Fraction(Fraction(1, 1), 1)
        lother, lnum, lden, details, var, traiter, lycee = [self], [self.n], [self.d], 0, '', False, False
        for other in others:
            if other == 0:
                return 0
            elif isinstance(other, Polynome):
                var = other.var
                details = min(details, other.details)
                lother.append(other)
            elif isinstance(other, PolynomeLycee):
                var = other.var
                lycee = True
                lother.append(other)
            elif isinstance(other, (int, float)):
                lden.append(1)
                lnum.append(other)
                lother.append(Fraction(other))
            elif isinstance(other, Fraction):
                lother.append(other)
                if other.code: traiter = True
                try: lden.append(eval(other.d))
                except TypeError: lden.append(other.d)
                try: lnum.append(eval(other.n))
                except TypeError: lnum.append(other.n)
            elif isinstance(other, RacineDegre2):
                lother.append(other)
                lden.append(other.denominateur)
                lnum.append(other.numerateur)
            else:
                raise ValueError(u'Format incorrect : %s' % (other))
        if var:
            if lycee:
                self = PolynomeLycee({0:self}, var)
                return PolynomeLycee.__mul__(self, other)
            else:
                self = Polynome([[self, 0]], var, details)
                return Polynome.__mul__(self, *lother[1:])

        if traiter:
            lfrac = [repr(self.traitement())]
            for other in lother:
                lfrac.append(repr(other.traitement()))
            return "*".join(lfrac)
        try: self.d = eval(self.d)
        except TypeError: pass
        s = abs(pgcd(reduce(lambda x, y: x * y, lnum), reduce(lambda x, y: x * y, lden)))
        if s == 1: return Fraction(reduce(lambda x, y: x * y, lnum), reduce(lambda x, y: x * y, lden))
        lepgcd, num, den = s, [], []
        i = 0
        while i < len(lnum):
            if lepgcd == 1 or lepgcd in lnum:
                num.append("*".join([repr(lnum[k]) for k in range(i, len(lnum))]))
                break
            else:
                lepgcdtmp = pgcd(lnum[i], lepgcd)
                if lepgcdtmp != 1: num.append("%r*%r" % (lepgcdtmp, lnum[i] // lepgcdtmp))
                else: num.append("%r" % lnum[i])
                lepgcd = lepgcd / lepgcdtmp
                i += 1
        i, lepgcd = 0, s
        while i < len(lden):
            if lepgcd == 1 or lepgcd in lden:
                den.append("*".join([repr(lden[k]) for k in range(i, len(lden))]))
                break
            else:
                lepgcdtmp = pgcd(lden[i], lepgcd)
                if lepgcdtmp != 1: den.append("%r*%r" % (lepgcdtmp, lden[i] // lepgcdtmp))
                else: den.append("%r" % lden[i])
                lepgcd = lepgcd / lepgcdtmp
                i += 1
        num, den = "*".join(num), "*".join(den)
        while num[:2] == "1*": num = num[2:]
        while "*1*" in num: num = num.replace("*1*", "*", 1)
        if num[-2:] == "*1": num = num[:-2]
        if s == reduce(lambda x, y: x * y, lnum):
            # laisser un *1 ou 1* selon
            if self.n == 1: num = "1*" + num
            else: num += "*1"
        while den[:2] == "1*": den = den[2:]
        while "*1*" in den: den = den.replace("*1*", "*" , 1)
        if den[-2:] == "*1": den = den[:-2]
        if s == reduce(lambda x, y: x * y, lden):
            # laisser un *1
            if self.d == 1: den = "1*" + den
            else: den += "*1"

        if "*" in num: num = num.strip()
        if "*" in den: den = den.strip()
        return Fraction(num, den, "s")


    def __rmul__(self, other):
        """*object*\ .\ **__rmul__**\ (*other*)

        ``p.__rmul__(q)`` est équivalent à ``p * q``  calcule le produit de l'objet p par la fraction q.

        *other* peut être un entier ou un réel.

        Pour plus de détails, voir :py:func:`__radd__`"""
        return Fraction(other) * self

    # def __truediv__(self, fraction): # pour Python 3
    def __div__(self, other):
        """*object*\ .\ **__div__**\ (*other*)

        ``p.__div__(q)`` est équivalent à ``p / q``  calcule le quotient de deux fractions.

        *other* peut être une chaîne représentant une fraction, un entier ou un réel.

        >>> from pyromaths.classes.Fractions import Fraction
        >>> repr(Fraction(2,5) / Fraction(10,2))
        'Fraction(2, 5)*Fraction(2, 10)'
        >>> repr(Fraction(2,5) / 4)
        'Fraction(2, 5)*Fraction(1, 4)'

        :param: other
        :type: Fraction ou string
        :rtype: Fraction ou string
        """
        if (isinstance(other, int) or isinstance(other, float)):
            other = Fraction(other)
        return "%r*%r" % (self, ~other)

    def __rdiv__(self, other):
        """*object*\ .\ **__rdiv__**\ (*other*)

        ``p.__rdiv__(q)`` est équivalent à ``p / q``  calcule le produit de l'objet p par la fraction q.

        *other* peut être un entier ou un réel.

        >>> from pyromaths.classes.Fractions import Fraction
        >>> repr(1/Fraction(1,3))
        '1*Fraction(3, 1)'

        Pour plus de détails, voir :py:func:`__radd__`"""
        return "%r*%r" % (other, ~self)

    def __invert__(self):
        """**__invert__**\ (*self*)

        ``__invert__(p)`` est équivalent à ``~p`` calcule l'inverse de la fraction p.

        >>> from pyromaths.classes.Fractions import Fraction
        >>> repr(~Fraction(8,27))
        Fraction(27, 8)
        """
        return Fraction(self.d, self.n)

    def __neg__(self):
        """**__neg__**\ (*self*)

        ``__neg__(p)`` est équivalent à ``-p`` calcule l'opposé de la fraction p.

        >>> from pyromaths.classes.Fractions import Fraction
        >>> repr(-Fraction(8,27))
        Fraction(-8, 27)
        """
        if self.code: self = self.traitement()
        return Fraction(-self.n, self.d)

    def __pos__(self):
        """**__pos__**\ (*self*)

        ``__pos__(p)`` est équivalent à ``+p`` Renvoie la fraction p.

        >>> from pyromaths.classes.Fractions import Fraction
        >>> repr(+Fraction(8,27))
        Fraction(8, 27)
        """
        return Fraction(self.n, self.d)

    def __pow__(self, n):
        """**__pow__**\ (*self*, *n*)

        ``p__pow__(q)`` est équivalent à ``p**q`` calcule p à la puissance q.

        >>> from pyromaths.classes.Fractions import Fraction
        >>> repr(Fraction(2,3)**4)
        Fraction(16, 81)

        :param: n
        :type: Integer
        :rtype: Fraction
        """
        return Fraction(self.n ** n, self.d ** n)

    def __trunc__(self):
        return self.n // self.d

    def __lt__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            other = Fraction(other)
        if other.d * self.d > 0:
            return self.n * other.d < self.d * other.n
        else :
            return not(self.n * other.d < self.d * other.n)

    def __le__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            other = Fraction(other)
        if other.d * self.d > 0:
            return self.n * other.d <= self.d * other.n
        else :
            return not(self.n * other.d <= self.d * other.n)

    def __eq__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            other = Fraction(other)
        if isinstance(other, Fraction):
            return self.reduit().n * other.reduit().d == self.reduit().d * other.reduit().n

    def __ne__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            other = Fraction(other)
        return self.n * other.d != self.d * other.n

    def __gt__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            other = Fraction(other)
        if other.d * self.d > 0:
            return self.n * other.d > self.d * other.n
        else :
            return not(self.n * other.d > self.d * other.n)

    def __ge__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            other = Fraction(other)
        if other.d * self.d > 0:
            return self.n * other.d >= self.d * other.n
        else :
            return not(self.n * other.d >= self.d * other.n)

    def __float__(self):
        return 1.0 * self.n / self.d

    def __int__(self):
        assert self.n % self.d == 0, "La fraction n'est pas un nombre entier !"
        return int(self.n / self.d)

    def reduit(self):
        """**reduit**\ (*object*)

        Retourne une version réduite de la fraction, ie calcule le numérateur et le dénominateur

            >>> from pyromaths.classes.Fractions import Fraction
            >>> repr(Fraction.reduit(Fraction(2*4,5*4)))
            Fraction(8, 20)
            >>> repr(Fraction.reduit(Fraction('2*4', '5*4')))
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
            >>> repr(Fraction.simplifie(Fraction(2*4,5*4)))
            Fraction(2, 5)
            >>> repr(Fraction.simplifie(Fraction('2*4','5*4')))
            Fraction(2, 5)

        :param type: Fraction
        :rtype: Fraction
        """
        conv = False
        if isinstance(self.n, str):
            self.n = eval(self.n)
            conv = True
        if isinstance(self.d, str):
            self.d = eval(self.d)
            conv = True
        if conv : self = Fraction(self.n, self.d)
        conv = False
        if isinstance(self.n, SquareRoot):
            s = self.n.simplifie()
            if s != self.n:
                self.n = s
                conv = True
        if isinstance(self.d, SquareRoot):
            s = self.d.simplifie()
            if s != self.d:
                self.d = s
                conv = True
        if conv: return self
        s = pgcd(self.n, self.d)
        if self.d != s:
            return Fraction(self.n // s, self.d // s)
        else:
            return self.n // s

    def decompose(self):
        """**decompose**\ (*object*)

        Retourne une décomposition de la fraction afin de la simplifier

            >>> from pyromaths.classes.Fractions import Fraction
            >>> repr(Fraction.decompose(Fraction(8,20)))
            Fraction("2*4", "5*4", "s")

        :param type: Fraction
        :rtype: Fraction
        """
        if isinstance(self.n, str): self.n = eval(self.n)
        if isinstance(self.d, str): self.d = eval(self.d)
        conv = False
        if isinstance(self.n, SquareRoot):
            s = self.n.simplifie()
            if s != self.n:
                self.n = s
                conv = True
        if isinstance(self.d, SquareRoot):
            s = self.d.simplifie()
            if s != self.d:
                self.d = s
                conv = True
        if conv:
            return self
        if self.d == self.n:
            return 1
        else:
            lepgcd = pgcd(self.n, self.d)
            if lepgcd == 1:
                return self
            else:
                return Fraction("%r*%s" % (self.n // lepgcd, lepgcd), "%r*%s" % (self.d // lepgcd, lepgcd), "s")

    def traitement(self, final=False):
        """**traitement**\ (*object*,\ *self*)

        Finit la mise au même dénominateur ou la simplification de la fraction.
        Si *final* est vrai, alors essaie de simplifier la fraction.

            >>> from pyromaths.classes.Fractions import Fraction
            >>> repr(Fraction("3*4", "3*7", "r").traitement())
            Fraction(12, 21)
            >>> repr(Fraction("3*4", "3*7", "s").traitement())
            Fraction(4, 7)
            >>> repr(Fraction(12, 21).traitement())
            Fraction(12, 21)
            >>> repr(Fraction(12, 21).traitement(True))
            Fraction("4*3", "7*3", "s")

        :param: final
        :type: boolean
        :rtype: Fraction
        """
        if self.code == "r":
            if isinstance(self.n, str): n = eval(self.n)
            else: n = self.n
            if isinstance(self.d, str): d = eval(self.d)
            else: d = self.d
            return Fraction(n, d)
        if self.code == "s":
            if isinstance(self.n, str): n = eval(self.n)
            else: n = self.n
            if isinstance(self.d, str): d = eval(self.d)
            else: d = self.d
            s = pgcd(n, d)
            return Fraction(n // s, d // s)
        if final:
            return self.decompose()
        # Pas de traitement spécifique nécessaire
        return self
