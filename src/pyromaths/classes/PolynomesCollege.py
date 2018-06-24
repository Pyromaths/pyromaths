#!/usr/bin/env python3
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
from __future__ import division
from __future__ import unicode_literals
from builtins import str
from builtins import range
from past.utils import old_div
from builtins import object
from pyromaths.outils.decimaux import decimaux
from pyromaths.outils import Priorites3
from pyromaths.classes.SquareRoot import SquareRoot
from pyromaths.classes.Fractions import Fraction

from random import *
from functools import reduce

class Polynome(object):
    """ Cette classe crée la notion de polynômes.
    
        Si ``var == None`` alors la variable est ``x``.
        
        *details* donne le niveau de détails attendus dans les développements et réductions :

        - 0 : pas de détails : 3x+4x => 7x
        - 1 : ordonne avant de réduire
        - 2 : ordonne puis factorise les réductions : 3x+4x=(3+4)x
        - 3 : comme 2 et détaille les produits : 2x*3x=2*3*x*x

        >>> from pyromaths.classes.PolynomesCollege import Polynome
        >>> repr(Polynome([[2,2],[3,1],[4,0]], 'z'))
        Polynome([[2, 2], [3, 1], [4, 0]], "z", 0)
        >>> repr(Polynome("2y^2+3y+4"))
        Polynome([[2, 2], [3, 1], [4, 0]], "y", 0)
        >>> repr(Polynome([[1, 1], [2, 2]]))
        Polynome([[1, 1], [2, 2]], "x", 0)
        >>> repr(Polynome("Fraction(1,7)x^2-Fraction(3,8)x-1"))
        Polynome([[Fraction(1, 7), 2], [Fraction(-3, 8), 1], [-1, 0]], "x", 0)
    """

    def __init__(self, monomes, var=None, details=0):
        """Crée un polynôme."""
        monomes = monomes or '0'  # monômes du polynôme, par défaut un polynôme nul
        if isinstance(monomes, Polynome):
            self.monomes = monomes.monomes
            self.var = monomes.var
            self.details = monomes.details
        elif isinstance(monomes, str):
            # Gère la construction des polynôme à partir d'une chaîne de caractères
            self.details = details
            listmonomes = []
            splitted = Priorites3.splitting(monomes)
            m_coef, var, coef = None, None, ''
            while splitted:
                extract = splitted.pop(0)
                if extract in '+-':
                    if m_coef:
                        listmonomes.append([m_coef, 0])
                        m_coef = None
                    coef = extract
                elif Priorites3.EstNombre(extract):
                    m_coef = eval(coef + extract)
                else:
                    if var and extract != var:
                        raise ValueError(u'Le nom de la variable (%s) est incorrect pour le Polynôme %s' % (var, monomes))
                    if var is None: var = extract
                    if splitted and splitted[0] == '^':
                        splitted.remove('^')
                        m_deg = eval(splitted.pop(0))
                    else:
                        m_deg = 1
                    if m_coef is None:
                        if coef == '-':
                            m_coef = -1
                        else:
                            m_coef = 1
                    listmonomes.append([m_coef, m_deg])
                    m_coef = None
            if m_coef: listmonomes.append([m_coef, 0])
            if listmonomes: self.monomes = listmonomes
            else: self.monomes = [[0, 0]]
            self.var = var or 'x'
        else:
            # Supprime les monomes nuls :
            for k in range(len(monomes) - 1, -1, -1):
                if monomes[k][0] == 0: monomes.pop(k)
            if not monomes: monomes = [[0, 0]]
            self.monomes = monomes
            self.var = var or 'x'  # Variable par défaut
            self.details = details


    def __repr__(self):
        """**repr**\ (*object*)

        Renvoie une chaîne de caractère représentant un :mod:`Polynome`
        évaluable pour créer un :mod:`Polynome`.

            >>> from pyromaths.classes.PolynomesCollege import Polynome
            >>> repr(Polynome([[2,2],[3,1],[4,0]], 'z'))
            Polynome([[2, 2], [3, 1], [4, 0]], "z", 0)

        :rtype: string
        """
        return "Polynome(%s, \"%s\", %s)" % (self.monomes, self.var, self.details)

    def __str__(self):
        r"""**str**\ (*object*)

        Renvoie une version LaTeX du polynôme.
            >>> from pyromaths.classes.PolynomesCollege import Polynome
            >>> str(Polynome([[2,2],[3,1],[4,0]], 'z'))
            2\,z^{2}+3\,z+4
            >>> str(Polynome("y^2-Fraction(3,2)y-1"))
            y^{2}-\dfrac{3}{2}\,y-1
            >>> from pyromaths.classes.Fractions import Fraction
            >>> print(Polynome([[1, 1], [Fraction(-5, 1), 0]]))
            x-5

        :rtype: string
        """
        def print_coef(coef):
            """Gère le format du coef
            """
            if isinstance(coef, (float, int)):
                if coef > 0: return "+" + decimaux(coef)
                else: return decimaux(coef)
            if isinstance(coef, Fraction):
                if isinstance(coef.n, int) and isinstance(coef.d, int) and coef.n < 0 and coef.d > 0:
                    return "-" + str(Fraction(-coef.n, coef.d, coef.code))
                return "+" + str(coef)
            if isinstance(coef, SquareRoot):
                if len(coef) > 1: coef = str(coef)
                else:
                    if coef[0][0] > 0:
                        return '+' + str(coef)
                    else:
                        return str(coef)
            if isinstance(coef, str):
                texte = "(" + "".join(Priorites3.texify([Priorites3.splitting(coef)])) + ")"
                if texte[0] != "-": return "+" + texte
                else: return texte
            raise ValueError(u'Not Implemented : Coefficient %s' % coef)

        var = self.var
        s = ""
        for m in self.monomes:
            if isinstance(m, list):
                if m[1] > 1:
                    # Monôme de degré au moins 2
                    if m[0] == 1:
                        s = s + "+" + var + "^{" + str(m[1]) + "}"
                    elif m[0] == -1:
                        s = s + "-" + var + "^{" + str(m[1]) + "}"
                    else:
                        s = s + print_coef(m[0]) + r"\," + var + "^{" + str(m[1]) + "}"
                elif m[1] == 1:
                    # Monôme de degré 1
                    if m[0] == 1:
                        s = s + "+" + var
                    elif m[0] == -1:
                        s = s + "-" + var
                    else:
                        s = s + print_coef(m[0]) + r"\," + var
                else:
                    # Monôme de degré 0
                    s = s + print_coef(m[0])
        # supprime le + en début de séquence
        s = s.lstrip("+")
        if not s: s = "0"
        return s

    def __call__(self, valeur):
        """**__call__**\ (*object*\ ,*valeur*)

        ``p.__call__(valeur)`` est équivalent à ``p(valeur)``
        Retourne l'expression numérique du polynôme pour sa variable égale à
        valeur.

            >>> from pyromaths.classes.PolynomesCollege import Polynome
            >>> Polynome("4+x-x^2+x^3-2x^5")(-5)
            4-5-(-5)**2+(-5)**3-2*(-5)**5

        :param: valeur
        :type: integer, float or Fraction
        :rtype: string
        """
        if Polynome.degre(self) == 0:
            return self.monomes[0][0] or '0'
        if valeur == 0:
            retour = ''
            for m in self.monomes:
                if m[1] == 0: retour += '+%r' % m[0]
            return retour.lstrip('+').replace('+-', '-') or '0'
        if valeur < 0 and isinstance(valeur, (float, int)): nb = "(%s)" % valeur
        else: nb = repr(valeur)
        retour = ''
        for m in self.monomes:
            if m[1] == 0: retour += '+%r' % m[0]
            elif m[1] == 1:
                if m[0] == 1:
                    retour += '+%r' % valeur
                elif m[0] == -1:
                    retour += '-' + nb
                else:
                    retour += '+%r*' % m[0] + nb
            else:
                if m[0] == 1:
                    retour += '+' + nb + '**%s' % m[1]
                elif m[0] == -1:
                    retour += '-' + nb + '**%s' % m[1]
                else:
                    retour += '+%r*' % m[0] + nb + '**%s' % m[1]
        return retour.lstrip('+').replace('+-', '-')

    def derive(self):
        if self.degre < 1:
            return Polynome([0, 0], self.var, self.details)
        else:
            p = []
            for m in self:
                if m[1] > 0:
                    p.append([m[0] * m[1], m[1] - 1])
            return Polynome(p, self.var, self.details)


    def __getitem__(self, i):
        """*object*\ .\ **__getitem__**\ (*integer*)

        Renvoie le i ème monome du polynôme.

            >>> from pyromaths.classes.PolynomesCollege import Polynome
            >>> Polynome("2y+3y^2+4")[1]
            [3, 2]

        :rtype: list
        """
        return self.monomes[i]

    def __delitem__(self, i):
        """*object*\ .\ **__delitem__**\ (*integer*)

        Renvoie le polynôme privé du i ème monome.

            >>> from pyromaths.classes.PolynomesCollege import Polynome
            >>> p = Polynome("2y+3y^2+4")
            >>> del p[1]
            >>> repr(p)
            Polynome([[2, 1], [4, 0]], "y", 0)

        :rtype: Polynome
        """
        m = self.monomes
        del m[i]
        return Polynome(m, self.var, self.details)

    def __iadd__(self, other):
        """*object*\ .\ **__iadd__**\ (*other*)

        ``p.__iadd__(q)`` est équivalent à ``p += q``

            >>> from pyromaths.classes.PolynomesCollege import Polynome
            >>> p=Polynome("2y+3y^2+4")
            >>> p += Polynome('-y+6')
            >>> repr(p)
            Polynome([[2, 1], [3, 2], [4, 0], [-1, 1], [6, 0]], "y", 0)

        :rtype: Polynome
        """
        other = self._convert_other(other)
        m1, m2 = [m for m in self.monomes], [m for m in other.monomes]
        m = []
        m1.extend(m2)
        for monomes in m1:
            if monomes[0]: m.append(monomes)
        return Polynome(m, self.var, self.details)

    def __eq__(self, other):
        """*object*\ .\ **__eq__**\ (*other*)

        ``p.__eq__(q)`` est équivalent à ``p == q``
        Renvoie True si deux polynômes sont égaux. Ne tient pas compte de
        l'ordre des monômes.

            >>> from pyromaths.classes.PolynomesCollege import Polynome
            >>> Polynome("2y+3y^2+4") == Polynome('-y+6')
            False
            >>> Polynome('3x+5x+4')== Polynome('8x+4')
            False

        :rtype: boolean
        """
        other = self._convert_other(other)
        return sorted(self.monomes, key=lambda x: (-x[1], x[0])) == \
               sorted(other.monomes, key=lambda x: (-x[1], x[0]))

    def __ne__(self, other):
        """*object*\ .\ **__ne__**\ (*other*)

        ``p.__ne__(q)`` est équivalent à ``p != q``
        Renvoie True si deux polynômes sont différents. Ne tient pas compte de
        l'ordre des monômes.

            >>> from pyromaths.classes.PolynomesCollege import Polynome
            >>> Polynome("2y+3y^2+4") != Polynome('-y+6')
            True

        :rtype: boolean
        """
        return not (self == other)

    def __add__(self, *others):
        """*object*\ .\ **__add__**\ (*\ \*others*)

        ``p.__add__(q)`` est équivalent à ``p + q``  calcule la somme de
        polynômes.

        *other* peut être une chaîne représentant un polynôme.

            >>> from pyromaths.classes.PolynomesCollege import Polynome
            >>> repr(Polynome("2y+3y^2+4", details=2)+Polynome('-y+6', details=2))
            Polynome([[3, 2], [2, 1], [-1, 1], [4, 0], [6, 0]], "y", 2)

        :param: other
        :type: Polynome ou string *évaluable comme Polynome*
        :rtype: Polynome
        """
#         if isinstance(other, str):
#             other = eval(other)
        for other in others:
            other = self._convert_other(other)
            self +=other
        return self.nreduction()

    def __radd__(self, other):
        """*object*\ .\ **__radd__**\ (*other*)

        ``p.__radd__(q)`` est équivalent à ``q + p``

        >>> from pyromaths.classes.PolynomesCollege import Polynome
        >>> from pyromaths.classes.Fractions import Fraction
        >>> repr(Fraction(5,4)+Polynome("3x"))
        Polynome([[3, 1], [Fraction(5, 4), 0]], "x", 0)

        :param: other
        :type: Polynome ou string *évaluable comme Polynome*
        :rtype: Polynome
        """
        if isinstance(other, str):
            other = eval(other)
        other = self._convert_other(other)
        return other + self

    def __sub__(self, *others):
        """*object*\ .\ **__sub__**\ (*other*)

        ``p.__sub__(q)`` est équivalent à ``p + q``  calcule la somme de
        polynômes.

        *other* peut être une chaîne représentant un polynôme.

            >>> from pyromaths.classes.PolynomesCollege import Polynome
            >>> repr(Polynome("2y+3y^2+4")-Polynome('-y+6'))
            'Polynome([[2, 1], [3, 2], [4, 0]], "y", 0)+Polynome([[1, 1], [-6, 0]], "y", 0)'
            >>> repr(Polynome("3y^2+2y+4")-Polynome('-y+6'))
            'Polynome([[3, 2], [2, 1], [4, 0]], "y", 0)+Polynome([[1, 1], [-6, 0]], "y", 0)'
            >>> repr(Polynome("x+6")-Polynome("3x"))
            Polynome([[-2, 1], [6, 0]], "x", 0)
            >>> repr(Polynome("x+6",details=2)-Polynome("3x",details=2))
            Polynome([[1, 1], [-3, 1], [6, 0]], "x", 2)

        :param: other
        :type: Polynome ou string *évaluable comme Polynome*
        :rtype: Polynome or string
        """
        areduire = False
        if self.ordonne().reductible(): areduire = True
        lother = []
        details, etapes = self.details, False
        for other in others:
            other = self._convert_other(other)
            if other == 0:
                pass
            else:
                if other.ordonne().reductible(): areduire = True
                details = min(details, other.details)
                if len(other) > 1: etapes = True
                lother.append(other)
        if areduire:
            lother = [other.nreduction() for other in lother]
            lother.insert(0, self.nreduction())
            return "-".join([repr(other) for other in lother])
        else:
            calcul = "%r+" % self +"+".join([repr(-other) for other in lother])
            if etapes: return calcul
            else: return eval(calcul)


    def __rsub__(self, other):
        """*object*\ .\ **__rsub__**\ (*other*)

        ``p.__rsub__(q)`` est équivalent à ``q - p``

        >>> from pyromaths.classes.PolynomesCollege import Polynome
        >>> repr(1-Polynome([[-4, 1], [-9, 2], [-5, 0]], "x"))
        'Polynome([[1, 0]], "x", 0)+Polynome([[4, 1], [9, 2], [5, 0]], "x", 0)'
        >>> from pyromaths.classes.Fractions import Fraction
        >>> repr(Fraction(5,4)-Polynome("3x"))
        Polynome([[-3, 1], [Fraction(5, 4), 0]], "x", 0)
        >>> repr(Fraction(5,4)-Polynome("-3x"))
        Polynome([[3, 1], [Fraction(5, 4), 0]], "x", 0)

        :param: other
        :type: Polynome ou string *évaluable comme Polynome*
        :rtype: Polynome
        """
        other = self._convert_other(other)
        if len(self) == 1:
            # Cas où on soustrait un polynôme de longueur 1
            other += -self
            return other.ordonne()
        return "%r+%r" % (other, -self)

    def __neg__(self):
        """*object*\ .\ **__neg__**\ ()

        ``p.__neg__()`` est équivalent à ``-p`` est équivalent à ``p = -p``

        **TODO :** Corriger ce dernier point ; p ne devrait pas être modifié

        Renvoie l'opposé d'un polynôme.

            >>> from pyromaths.classes.PolynomesCollege import Polynome
            >>> repr(-Polynome("2y+3y^2+4"))
            Polynome([[-2, 1], [-3, 2], [-4, 0]], "y", 0)

        :rtype: Polynome
        """
        if self.ordonne().reductible(): return '-%r' % self.nreduction()
        m = [m1 for m1 in self.monomes]
        for i in range(len(m)):
            m[i][0] = -m[i][0]
        return Polynome(m, self.var, self.details)

    def __pos__(self):
        """*object*\ .\ **__pos__**\ ()

        ``p.__pos__()`` est équivalent à ``+p``

        Renvoie le polynôme.

            >>> from pyromaths.classes.PolynomesCollege import Polynome
            >>> repr(+Polynome("2y+3y^2+4"))
            Polynome([[2, 1], [3, 2], [4, 0]], "y", 0)

        :rtype: Polynome
        """
        return self


    def __mul__(self, *others):
        """*object*\ .\ **__mul__**\ (*other*)

        ``p.__mul__(q)`` est équivalent à ``p * q``

        Renvoie une chaîne de caractère ou un objet Polynôme dont les éléments
        sont :

        * le produit de ``p`` et ``q`` si ce sont deux monômes dont un au moins
          a pour coefficient 1.
        * le produit détaillé de ``p`` et ``q`` si ce sont deux monômes ne
          dépendant pas du cas précédent.
        * le développement par distributivité dans les autres cas

        si details est égal à 0, les produits dans les distributivités sont calculés immédiatement,
        sinon les produits sont explicités.

            >>> from pyromaths.classes.PolynomesCollege import Polynome
            >>> repr(Polynome('3x+4', details=0)*Polynome('2x+5', details=0))
            'Polynome([[6, 2]], "x", 0)+Polynome([[15, 1]], "x", 0)+Polynome([[8, 1]], "x", 0)+Polynome([[20, 0]], "x", 0)'
            >>> repr(Polynome('3x', details=1)*Polynome('2x+5', details=1))
            'Polynome([[3, 1]], "x", 1)*Polynome([[2, 1]], "x", 1)+Polynome([[3, 1]], "x", 1)*Polynome([[5, 0]], "x", 1)'
            >>> repr(Polynome('3x', details=3) * Polynome('2x', details=3))
            "Polynome([[3, 0]], var = 'x', details=3)*Polynome([[1, 1]], var = 'x', details=3)*Polynome([[2, 0]], var = 'x', details=3)*Polynome([[1, 1]], var = 'x', details=3)"
            >>> repr(Polynome('3', details=3)*Polynome('x', details=3))
            Polynome([[3, 1]], "x", 3)

        :param: other
        :type: Polynome ou string *évaluable comme Polynome*
        :rtype: string ou Polynome
        """
        def id_rem(p1, p2):
            '''Renvoie 1, 2 ou 3 selon l'identité remarquable trouvée, None sinon'''
            if len(p1) != 2 or len(p2) != 2: return None
            p1, p2 = p1.ordonne(), p2.ordonne()
            m0 = [abs(p1[0][0]), p1[0][1]]
            m1 = [abs(p1[1][0]), p1[1][1]]
            if p1 == p2:
                # 1ère ou 2ème identité remarquable
                return p1 ** 2
            if (p1[0][1] == p2[0][1] and p1[1][1] == p2[1][1]) and (p1[0][0] == p2[0][0] and\
                p1[1][0] == -p2[1][0]) or (p1[0][0] == -p2[0][0] and p1[1][0] == p2[1][0]):
                # 3ème identité remarquable
                if p1[0][0] == p2[0][0]:
                    poly = "%r**2-%r**2" % (Polynome([p1[0]], self.var, self.details), \
                                            Polynome([m1], self.var, self.details))
                else:
                    poly = "%r**2-%r**2" % (Polynome([p1[1]], self.var, self.details), \
                                            Polynome([m0], self.var, self.details))
                return poly
            return None

        if self == 0: return 0
        lother = [self] + list(others)
        for el in lother:
            if el.ordonne().reductible():
                # On commence par réduire la chaîne
                return "*".join([repr(other.nreduction()) for other in lother])

        lcoeff, lexp, reduire, ordonne = [], [], True, True
        for i in range(len(lother)):
            lother[i] = self._convert_other(lother[i])
            if len(lother[i]) == 1:
                # c'est un monôme, il est donc probablement réduit
                coeff, exp = lother[i][0][0], lother[i][0][1]
                if coeff != 1: lcoeff.append(coeff)
                if exp != 0: lexp.append(exp)
                if coeff != 1 and exp != 0: reduire = False
                if lexp and exp < lexp[-1]: ordonne = False
                if lother[i] == 0: return 0
            if len(lother[i]) > 1 or i + 1 == len(lother):
                # Ce n'est pas un monôme, il va donc falloir utiliser la distributivité
                # ou alors la chaine est fini et on calcule
                if i > 1 or len(lother[i]) == 1 or len(lcoeff) > 1 or len(lexp) > 1:
                    # on a multiplié au moins 2 monômes auparavant
                    if lother[i].details == 3 and not reduire:
                        # TODO: cas où un coeff est une str
                        #=======================================================
                        # return "*".join([repr(coeff) for coeff in lcoeff]) + "*" + \
                        #     "*".join(["Polynome([[1, %s]], '%s', %s)" % (exp, self.var, self.details) for exp in lexp]) + \
                        #     "*".join([repr(other.nreduction()) for other in lother[i + 1:]])
                        #=======================================================
                        produit = []
                        for j in lother:
                            if j[0][0] != 1 and j[0][1] > 0:
                                produit.append("*".join(['Polynome([[%s, 0]], var = \'%s\', details=%s)' % (j[0][0], j.var, j.details), \
                                                'Polynome([[1, %s]], var = \'%s\', details=%s)' % (j[0][1], j.var, j.details)]))
                            else:
                                produit.append(repr(j))
                        return "*".join(produit)
                    if lother[i].details == 3 and not ordonne:
                        coeff = "*".join([repr(coeff) for coeff in lcoeff])
                        if coeff: sol = [coeff]
                        else: sol = []
                        exp = "*".join(["Polynome([[1, %s]], '%s', %s)" % (exp, self.var, self.details) for exp in lexp])
                        if exp: sol.append(exp)
                        if lother[i + 1:]: sol.append("*".join([repr(other.nreduction()) for other in lother[i + 1:]]))
                        return "*".join(sol)
                    else:
                        lcoeff.append(1)
                        lexp.append(0)
                        poly = Polynome([[reduce(lambda x, y: x * y, lcoeff), \
                                          reduce(lambda x, y: x + y, lexp)]], self.var, self.details)
                        if i + 1 == len(lother): return poly
                        else: return \
                            "*".join([repr(poly)] + [repr(other.nreduction()) for other in lother[i:]])
                else:
                    # On distribue :
                    if i:
                        # on va utiliser la distributivité simple
                        poly = Polynome([[coeff, exp]], self.var, self.details)
                        if self.details > 0:
                            produit = "+".join([repr(poly) + "*" + repr(Polynome([other], self.var, self.details)) for other in lother[i]])
                            if i + 1 < len(lother): produit = "(" + produit + ")"
                            return "*".join([produit] + [repr(other.nreduction()) for other in lother[i + 1:]])
                        else:
                            produit = "+".join([repr(Polynome([[poly[0][0] * other[0], poly[0][1] + other[1]]], self.var, self.details)) for other in lother[i]])
                            if i + 1 < len(lother): produit = "(" + produit + ")"
                            return "*".join([produit] + [repr(other.nreduction()) for other in lother[i + 1:]])
                    else:
                        # le premier polynome est de longueur au moins 2
                        produit = id_rem(lother[0], lother[1])
                        if produit == None:
                            # Distributivité
                            # TODO: Convertir (a-b) en (a+(-b)) pour details=3
                            #===================================================
                            # if self.details == 3:
                            #     difference, produit = False, []
                            #     for poly in lother:
                            #         if len(poly) > 1:
                            #             for j in range(1, len(poly)):
                            #                 if poly[j][0] < 0:
                            #                     difference = True
                            #                     produit.append("(" + "+".join(['Polynome(%s, var = \'%s\', details=%s)' % (poly[i], poly.var, poly.details) for i in range(len(poly))]) + ")")
                            #                     break
                            #         if not difference: produit.append(repr(poly))
                            #     if difference:
                            #         return "*".join(produit)
                            #===================================================

                            if self.details > 0:
                                produit = "+".join(["+".join([repr(Polynome([premier], self.var, self.details)) + \
                                                              "*" + repr(Polynome([second], self.var, self.details)) \
                                                              for second in lother[1]]) for premier in lother[0]])
                                if i + 2 < len(lother): produit = "(" + produit + ")"
                                return "*".join([produit] + [repr(other.nreduction()) for other in lother[i + 2:]])
                            else:
                                produit = "+".join(["+".join([repr(Polynome([[premier[0] * second[0], premier[1] + second[1]]], self.var, self.details)) \
                                                              for second in lother[1]]) for premier in lother[0]])
                                if i + 2 < len(lother): produit = "(" + produit + ")"
                                return "*".join([produit] + [repr(other.nreduction()) for other in lother[i + 2:]])
                        else:
                            # identité remarquable
                            if i + 2 < len(lother): produit = "(" + produit + ")"
                            return "*".join([produit] + [repr(other.nreduction()) for other in lother[i + 2:]])

    def __rmul__(self, other):
        """Multiplication de *other* (qui n'est pas un polynôme) par *self*
        (qui en est un)

        * Si *other* est une suite de produits de monômes, et *self* un polynôme
          de rang 1, on effectue toutes les multiplications en une fois
        * Sinon, on calcule d'abord @other

        :param: other
        :type: Polynome ou string *évaluable comme Polynome*
        :rtype: string ou Polynome"""
        if isinstance(other, (int, float, Fraction)):
            other = self._convert_other(other)
            return other * self
        if isinstance(other, str):
            from pyromaths.outils.Priorites3 import splitting
            ls = splitting(other)
            if ls.count("+") or ls.count("-"):
                # Réduire @other avant de faire le produit et vérifier s'il faut
                # des parenthèses autour de l'expression @other
                par, besoin = 0, False
                for k in range(len(ls)):
                    if ls[k] == "(": par += 1
                    elif ls[k] == ")": par -= 1
                    elif not par and ls[k] in "+-":
                        besoin = True
                        break
                if besoin: return "(" + other + ")*" + repr(self)
                else: return other + "*" + repr(self)
            elif len(self) > 1:
                return other + "*" + repr(self)
            else:
                index = 0
                for i in range(len(ls)):
                    if "Polynome(" in ls[i]:
                        if len(eval(ls[i])) > 1:
                            return other + "*" + repr(self)
                        elif Polynome.degre(eval(ls[i])) > 0:
                            index = index or i
                index = index or len(ls)
                if self.monomes[0][0] != 1:
                    ls.insert(index, "*")
                    if self.monomes[0][0] < 0: ls.insert(index, "(" + repr(self.monomes[0][0]) + ", %s)" % self.details)
                    else: ls.insert(index, repr(self.monomes[0][0]))
                if self.monomes[0][1] > 0:
                    ls.append("*")
                    ls.append("Polynome([%s], \"%s\", %s)" % ([1, self.monomes[0][1]], self.var, self.details))
                return "".join(ls)
        else: raise ValueError(u"Type non prévu. Bogue en perspective !")

    def _divide(self, other):
        """*object*\ .\ **div**\ (*other*)

        ``p.__truediv__(q)`` est équivalent à ``p / q``

        Renvoie (self // other, self % other) deux polynomes où le premier élément est le quotient et le second
        le reste de la division euclidienne de self par other.

            >>> from pyromaths.classes.PolynomesCollege import Polynome
            >>> Polynome('3x+4', 0)._divide(Polynome('2x+5', 0))
            (Polynome([[Fraction(3, 2), 0]], "x", 0), Polynome([[Fraction(-7, 2), 0]], "x", 0))
            >>> Polynome("x^4+2x^3+3x^2+5x+6")._divide(Polynome("7x+8"))
            (Polynome([[Fraction(1, 7), 3], [Fraction(6, 49), 2], [Fraction(99, 343), 1], [Fraction(923, 2401), 0]], "x", 0), Polynome([[Fraction(7022, 2401), 0]], "x", 0))

        :param: other
        :type: Polynome ou string *évaluable comme Polynome*
        :rtype: Deux Polynome
        """
        other = self._convert_other(other)
        quotient = Polynome([], self.var, self.details)
        reste = Polynome.ordonne(self)
        diviseur = other.ordonne()
        degre_diviseur = diviseur.degre()
        while reste.degre() >= degre_diviseur:
            degre = reste.degre() - degre_diviseur
            if isinstance(reste[0][0], Fraction) or isinstance(diviseur[0][0], Fraction):
                coef = eval(Priorites3.priorites('%r/%r' % (reste[0][0], diviseur[0][0]))[-1][0])
            else:
                if reste[0][0] % diviseur[0][0]:
                    coef = Fraction(reste[0][0], diviseur[0][0])
                else:
                    coef = reste[0][0] // diviseur[0][0]
            quotient.monomes.append([coef, degre])
            reste = eval(Priorites3.priorites('%r-Polynome([[%r, %s]], "%s", %s)*%r' % (reste, coef, degre, self.var, self.details, diviseur))[-1][0])
        return quotient.nreduction(True), reste

    def __mod__(self, other):
        """
        self % other
        """
        other = self._convert_other(other)
        if other is NotImplemented:
            return other
        if not other:
            if self:
                raise ValueError(u'Opération non valide : x % 0')
            else:
                raise ValueError(u'Division non définie : 0 % 0')
        return self._divide(other)[1]

    def __floordiv__(self, other):
        """
        self // other
        """
        other = self._convert_other(other)
        if other is NotImplemented:
            return other
        if not other:
            if self:
                raise ValueError(u'Opération non valide : x // 0')
            else:
                raise ValueError(u'Division non définie : 0 // 0')
        return self._divide(other)[0]

    def __len__(self):
        """*object*\ .\ **__len__**\ ()

        ``p.__len__()`` équivaut à ``len(p)`` et renvoie le nombre de monômes d'un polynôme.

            >>> from pyromaths.classes.PolynomesCollege import Polynome
            >>> len(Polynome("2y+3y^2+4"))
            3

        :rtype: integer
        """
        m = [m1 for m1 in self.monomes]
        m = Polynome.ordonne(Polynome(m, self.var))
        return len(self.monomes)

    def degre(self):
        """**degre**\ (*object*)

        Retourne le degré d'un polynôme, -1 pour le polynôme nul

            >>> from pyromaths.classes.PolynomesCollege import Polynome
            >>> Polynome("2y+3y^2+4").degre()
            2
            >>> Polynome('').degre()
            -1

        :rtype: integer
        """
        if self == 0: return -1
        else: return self.nreduction(True)[0][1]

    def __pow__(self, other):
        """*object*\ .\ **pow**\ (*integer*)

        ``p.__pow__(n)`` équivaut à ``p**n`` et renvoie le développement du
        polynôme p à la puissance n.

        * Si ``n == 1``, alors renvoie l'objet Polynome ;
        * si ``n == 2``, alors renvoie une chaîne avec le développement en
          utilisant une identité remarquable ;
        * si ``n > 1``, renvoie le développement en utilisant la formule du
          binôme de Newton.

        **TODO :** si ``n == 2`` et ``len(p) > 2``, bug

            >>> from pyromaths.classes.PolynomesCollege import Polynome
            >>> repr(Polynome("2y+4")**2)
            'Polynome([[2, 1]], "y", 0)**2+2*Polynome([[2, 1]], "y", 0)*Polynome([[4, 0]], "y", 0)+Polynome([[4, 0]], "y", 0)**2'
            >>> repr(Polynome("2y")**3)
            Polynome([[8, 3]], "y", 0)

        :rtype: string ou Polynome
        """
        if len(self) == 2 and other == 2:
            a0 = self.monomes[0][0]
            b0 = self.monomes[1][0]
            p = a0 * b0
            a = Polynome([[abs(a0), self.monomes[0][1]]], self.var, self.details)
            b = Polynome([[abs(b0), self.monomes[1][1]]], self.var, self.details)
            if p < 0:
                return "%r**2-2*%r*%r+%r**2" % (a, a, b, b)
            else:
                return "%r**2+2*%r*%r+%r**2" % (a, a, b, b)
        elif len(self) == 1:
            return Polynome([[self[0][0] ** other, self[0][1] * other]], self.var)
        else:
            result = self
            for dummy in range(other - 1):
                result = eval(result * self)
            return result

    def reductible(self):
        """**reductible**\ (*object*)

        Retourne True si le polynôme est réductible ou ordonnable, False sinon.

            >>> from pyromaths.classes.PolynomesCollege import Polynome
            >>> Polynome([[2, 1], [3, 2], [4, 0], [-1, 1], [6, 0]], "y").reductible()
            True

        :param type: Polynome
        :rtype: boolean
        """
        #=======================================================================
        # if self != self.reduit():
        #     return True
        # else:
        #     return False
        #=======================================================================
        ldegres = []
        for m in self:
            if m[1] in ldegres: return True
            # Il existe déjà un monome de même degré, le polynome est donc réductible.
            elif ldegres and m[1] > ldegres[-1]: return True
            # Polynome non ordonné
            else: ldegres.append(m[1])
            if isinstance(m[0], str) and Priorites3.effectue_calcul(Priorites3.splitting(m[0])) != [m[0]]: return True
            if isinstance(m[0], Fraction) and repr(m[0].traitement(True)) != repr(m[0]): return True
            if isinstance(m[0], SquareRoot) and repr(m[0].simplifie()) != repr(m[0]): return True
            # une simplification de fraction ou un calcul est à faire
        return False

    def ordonnable(self):
        """**ordonnable**\ (*object*)

        Retourne True si le polynome n'est pas ordonnée, False sinon.

        :param type: Polynome
        :rtype: boolean
        """
        lastdegre = None
        for m in self:
            if lastdegre is not None and m[1] > lastdegre: return True
            else: lastdegre = m[1]
        return False

    def ordonne(self):
        """**ordonne**\ (*object*)

        Retourne une version ordonnée d'un polynome en écrivant en premier les
        monômes de degré supérieur.

            >>> from pyromaths.classes.PolynomesCollege import Polynome
            >>> repr(Polynome([[2, 1], [3, 2], [4, 0], [-1, 1], [6, 0]], "y").ordonne())
            Polynome([[3, 2], [2, 1], [-1, 1], [4, 0], [6, 0]], "y", 0)

        :param type: Polynome
        :rtype: Polynome
        """
#         if len(self) == 1: return self
        m1 = self.monomes
        m1 = sorted(m1, key=lambda x: (-x[1]))
        return Polynome(m1, self.var, self.details)

    def nreduction(self, bdirecte=False):
        """**nreduction**\ (*object*)

        Retourne une étape de la réduction d'un polynome selon la valeur de *detail*
        Si bdirecte est True, alors donne la version réduite sans aucun détail de calcul

        :param type: Polynome
        :param bdirecte: faut-il donner directement le résultat de la réduction, sans étape de calcul ?
        :param type: boolean
        :rtype: Polynome
        """
        def _reduit_monome(monome, bdirecte):
            if isinstance(monome[0], (str, Fraction, SquareRoot)):
            # une réduction peut-être à faire ici
                if isinstance(monome[0], Fraction):
                    monome[0] = repr(monome[0].traitement(True))
                    res = []
                elif isinstance(monome[0], SquareRoot):
                    monome[0] = repr(monome[0].simplifie())
                    res = []
                else:
                    splitted = Priorites3.splitting(monome[0])
                    if len(splitted) > 1:
                        res = Priorites3.effectue_calcul(splitted)
                        if len(res) == 1:  # Le calcul s'effectue en une seule étape
                            monome[0] = res[0]
                if len(res) > 1:
                # Il y a un calcul à effectuer en plusieurs étapes
                    if bdirecte:  # on ne détaille pas
                        monome[0] = eval(Priorites3.priorites(monome[0])[-1][0])
                    else:
                        bdec = True
                        # *bdec* est un booléen qui est True si le calcul ne contient que des décimaux
                        for nb in res:
                            if nb[0] not in "+-*/0123456789(":
                                bdec = False
                                break

                        if bdec:  # on calcule en une étape 3+4-5
                            monome[0] = eval(Priorites3.priorites(monome[0])[-1][0])
                        else:
                            monome[0] = ''.join(res)  # on calcule étape par étape
                else:
                    monome[0] = eval(monome[0])  # le texte n'était pas nécessaire, c'est un nombre ou la fraction était irréductible
            return monome


        if not self.reductible(): return self
        else:
            if self.ordonnable() and self.details > 0 and not bdirecte:
                return self.ordonne()
            if not self.ordonne().reductible():
                # le polynome est seulement ordonnable
                return self.ordonne()
            # le polynome est donc réductible :
            factorisation, bfact = [], False
            # *factorisation* est une liste de monomes, qui va contenir les monomes du polynome en cours
            # de réduction, en stockant au format texte la somme des coefficients des monomes de même degré
            # *bfact* est un booléen qui est vrai si on doit effectuer une factorisation pour réduire le
            # polynome
            for m in self.ordonne().monomes:
                if factorisation and  m[1] == factorisation[-1][1]:
                    # deux monomes de même degré
                    bfact = True
                    if not isinstance(factorisation[-1][0], str): factorisation[-1][0] = repr(factorisation[-1][0])
                    if isinstance(m[0], str):
                        # On écrit la somme des deux coefficients au format str
                        factorisation[-1][0] += '+' + m[0]
                    elif m[0] > 0:
                        factorisation[-1][0] += '+%r' % m[0]
                        # On écrit la somme des deux coefficients au format str
                    elif m[0] < 0:
                        if isinstance(m[0], Fraction) and isinstance(m[0].d, str):
                            # On écrit la somme des deux coefficients au format str
                            factorisation[-1][0] += '+%r' % m[0]
                        else:
                            # On écrit la différence des deux coefficients au format str, '2-4'
                            # plutôt que '2+(-4)'
                            factorisation[-1][0] += '-%r' % -m[0]
                else:
                    # on ajoute un nouveau monome de degré inférieur au précédent
                    factorisation.append([m[0], m[1]])
            if bfact and self.details > 1 and not bdirecte:
                    # On retorune le polynome avec les factorisations mises en évidence
                    # Cas du monome de degré 0
                    if factorisation[-1][1] == 0 and isinstance(factorisation[-1][0], str):
                        factorisation[-1] = _reduit_monome(factorisation[-1], bdirecte)
                    return Polynome(factorisation, self.var, details=self.details)
            # on réduit le polynome
            for i in range(len(factorisation)):
                factorisation[i] = _reduit_monome(factorisation[i], bdirecte)
            return Polynome(factorisation, self.var, details=self.details)
            # Les monomes nuls sont retirés par la classe Polynome

    def _convert_other(self, other):
        """Convertit other en Polynome

        Utilisée dans les fonctions d'opérations entre Polynomes :add, sub, mul, ...
        """
        if isinstance(other, Polynome):
            if self.var == other.var:
                return other
            else:
                raise ValueError(u'Pyromaths ne sait manipuler que deux polynômes de même variable : %s et %s' % (self.var, other.var))
        if isinstance(other, (float, int, Fraction)):
            return Polynome([[other, 0]], self.var, self.details)
        return NotImplemented

def factoriser(calcul):
    """Factorise la somme calcul. Cette procédure n'est ni exaustive, ni
    robuste. Elle permet actuellement de résoudre les exercices proposés en 3e.

    :param calcul: Expression à factoriser
    :type calcul: str

    >>> from pyromaths.classes.PolynomesCollege import factoriser
    >>> factoriser("Polynome('4x^2+12x+9')")
    'Polynome([[2.0, 1]], "x", 0)**2+2*Polynome([[2.0, 1]], "x", 0)*Polynome([[3.0, 0]], "x", 0)+Polynome([[3.0, 0]], "x", 0)**2'
    >>> factoriser("Polynome('-4x^2+12x-9')")
    '-(Polynome([[2.0, 1]], "x", 0)**2-2*Polynome([[2.0, 1]], "x", 0)*Polynome([[3.0, 0]], "x", 0)+Polynome([[3.0, 0]], "x", 0)**2)'
    >>> factoriser("Polynome('4x^2-9')")
    'Polynome([[SquareRoot([[1, 4]]), 1]], "x", 0)**2-Polynome([[SquareRoot([[1, 9]]), 0]], "x", 0)**2'
    >>> factoriser("Polynome('3x^2-5')")
    'Polynome([[SquareRoot([[1, 3]]), 1]], "x", 0)**2-Polynome([[SquareRoot([[1, 5]]), 0]], "x", 0)**2'
    >>> factoriser("Polynome('4x^2')")
    'Polynome([[2.0, 1]], "x", 0)**2'
    >>> factoriser("Polynome('4x')")
    >>> factoriser("Polynome('x+1')*Polynome('x+2')+Polynome('x+1')*Polynome('x+3')")
    'Polynome([[1, 1], [1, 0]], "x", 0)*(Polynome([[1, 1], [2, 0]], "x", 0)+Polynome([[1, 1], [3, 0]], "x", 0))'
    >>> factoriser("Polynome('x+1')*Polynome('x+2')+Polynome('x+1')")
    'Polynome([[1, 1], [1, 0]], "x", 0)*Polynome([[1, 1], [2, 0]], "x", 0)+Polynome([[1, 1], [1, 0]], "x", 0)*1'
    >>> factoriser("Polynome('x+1')*Polynome('x+2')+Polynome('x+1')**2")
    'Polynome([[1, 1], [1, 0]], "x", 0)*Polynome([[1, 1], [2, 0]], "x", 0)+Polynome([[1, 1], [1, 0]], "x", 0)*Polynome([[1, 1], [1, 0]], "x", 0)'
    >>> factoriser("Polynome('x+1')**2-Polynome([[81, 0]], 'x', 3)")
    'Polynome([[1, 1], [1, 0]], "x", 0)**2-Polynome([[9.0, 0]], "x", 3)**2'

    :rtype: str
    """
    def id_rem(poly):
        """Vérifie si poly correspond au développement d'une identité
        remarquable ou est un carré.

        :param poly: polynome à évaluer
        :type poly: Polynome

        >>> from pyromaths.classes.PolynomesCollege import Polynome
        >>> from pyromaths.classes.PolynomesCollege.factoriser import id_rem
        >>> id_rem(Polynome('4x^2+12x+9'))
        "Polynome('2x')+2*Polynome('2x')*Polynome('3')+Polynome('3')**2"
        >>> id_rem(Polynome('-4x^2+12x-9'))
        "-(Polynome('2x')-2*Polynome('2x')*Polynome('3')+Polynome('3')**2)"
        >>> id_rem(Polynome('4x^2-9'))
        "(Polynome('2x')+Polynome('3'))*(Polynome('2x')-Polynome('3'))"
        >>> id_rem(Polynome('4x^2'))
        "Polynome('2x')**2"
        >>> id_rem(Polynome('4x'))
        None

        :rtype: str ou None
        """
        from math import sqrt
        from pyromaths.classes.SquareRoot import SquareRoot
        poly = poly.ordonne()
        if len(poly) == 1:
            if poly[0][1] % 2 == 0 and isinstance(poly[0][0], int) and \
              Arithmetique.carrerise(poly[0][0]) == 1:
                return "%r**2" % (Polynome([[sqrt(abs(poly[0][0])), poly[0][1] // 2]], poly.var, poly.details))
        elif len(poly) == 2:
            # if isinstance(SquareRoot([1, abs(poly[0][0])]).simplifie(),str):

            a = repr(Polynome([[SquareRoot([1, abs(poly[0][0])]), poly[0][1] // 2]], poly.var, poly.details))
            b = repr(Polynome([[SquareRoot([1, abs(poly[1][0])]), poly[1][1] // 2]], poly.var, poly.details))
            if not poly[0][1] % 2 and not poly[1][1] % 2:
                # Les deux exposants sont des carrés
                if poly[0][0] * poly[1][0] < 0:
                    # 3ème identité remarquable
                    if poly[0][0] < 0: return '%s**2-%s**2' % (b, a)
                    else: return '%s**2-%s**2' % (a, b)
        elif len(poly) == 3:
            a = repr(Polynome([[sqrt(abs(poly[0][0])), poly[0][1] // 2]], poly.var, poly.details))
            b = repr(Polynome([[sqrt(abs(poly[2][0])), poly[2][1] // 2]], poly.var, poly.details))
            if not poly[0][1] % 2 and not poly[2][1] % 2 and (old_div(poly[0][1], 2) + old_div(poly[2][1], 2) == poly[1][1]):
                # Ça ressemble à l'une des deux premières indentités remarquables
                if poly[0][0] * poly[2][0] > 0 and poly[0][0] * poly[1][0] > 0 and \
                      4 * poly[0][0] * poly[2][0] == poly[1][0] ** 2:
                    # 1ère identité remarquable, au signe près
                    if poly[0][0] > 0:
                        return a + '**2+2*' + a + '*' + b + '+' + b + '**2'
                    else:
                        return '-(' + a + '**2+2*' + a + '*' + b + '+' + b + '**2)'
                if poly[0][0] * poly[2][0] > 0 and poly[0][0] * poly[1][0] < 0 and \
                      4 * poly[0][0] * poly[2][0] == poly[1][0] ** 2:
                    if poly[0][0] > 0:
                        return a + '**2-2*' + a + '*' + b + '+' + b + '**2'
                    else:
                        return '-(' + a + '**2-2*' + a + '*' + b + '+' + b + '**2)'
        return None

    def EstFactorise(lcalcul):
        """indique si une liste de calculs est factorisée

        :param lcalcul: liste de calculs
        :type lcalcul: list

        >>> from pyromaths.classes.PolynomesCollege.factoriser import EstFactorise
        >>> EstFactorise(["Polynome('3x+4')", "*", "5"])
        True
        >>> EstFactorise(["Polynome('3x+4')", "*", "5", "+", "Polynome('2x+7')"])
        False

        :rtype: boolean
        """
        # Si le premier symbole est '+' ou '-', alors cela n'influe pas sur somme / produit
        dummy = [lcalcul[i] for i in range(len(lcalcul))]
        if dummy[0] == '+' or dummy[0] == '-': dummy = dummy[1:]
        par = Priorites3.recherche_parentheses(dummy)
        if par:
            if par[0] == 0 and par[1] == len(dummy):
                return EstFactorise(dummy[1:-1])
            while par:
                del dummy[par[0]:par[1]]
                par = Priorites3.recherche_parentheses(dummy)

            if '+' in dummy[1:] or '-' in dummy[1:]:
                return False
        else:
            if '+' in dummy or '-' in dummy:
                return False
        return True

    from pyromaths.outils import Arithmetique

    lcalcul = Priorites3.splitting(calcul)
    if len(lcalcul) == 1:
        # On tente une identité remarquable, un facteur commun ou une méthode Lycée (à faire plus tard)
        if 'Polynome(' == lcalcul[0][:9]:
            poly = eval(lcalcul[0])
            id_rem = id_rem(poly)
            if id_rem is None and len(poly) > 1:
                # Cherchons un facteur commun
                facteur = Arithmetique.pgcd([m[0] for m in poly])
                exp = min([m[1] for m in poly])
                if abs(facteur) != 1 or exp != 0:
                    k = Polynome([[facteur, exp]], poly.var, poly.details)
                    a = poly // k
                    return "*".join([repr(k), repr(a)])
                return None
            else:
                return id_rem
        else:
            raise ValueError(u'%s n\'est pas un Polynome et ne peut être factorisé')
    else:
        # C'est soit une somme de polynomes qu'il faut factoriser, soit déjà un produit
        if EstFactorise(lcalcul):
            # Il faut réduire les sommes
            poly = Priorites3.effectue_calcul(lcalcul)
            if EstFactorise(poly): return "".join(poly)
            else: return None
        else:
            # On cherche un facteur commun ou une identité remarquable
            nbpar = 0
            ltermes = [[]]
            if lcalcul[0] in '+-':
                lsgn = [lcalcul[0]]
            else:
                lsgn = ['']
                if lcalcul[0][:9] == 'Polynome(': ltermes = [[repr(eval(lcalcul[0]))]]
                else: ltermes = [[lcalcul[0]]]
            for el in lcalcul[1:]:
                if el in '+-' and nbpar == 0:
                    lsgn.append(el)
                    ltermes.append([])
                else:
                    if el == '(': nbpar += 1
                    elif el == ')': nbpar += -1
                    if el[:9] == 'Polynome(': ltermes[-1].append(repr(eval(el)))
                    else: ltermes[-1].append(el)

            if len(ltermes) >= 3 and lcalcul.count('**') > 1 and lcalcul.count('*') > 1 and lcalcul.count('2') > 2:
                # On peut être en présence de l'une des 2 premières identités remarquables
                exp1 = lcalcul.index('**')
                a = lcalcul[exp1 - 1]
                indexa = ltermes.index([a, '**', '2'])
                sgna = lsgn[indexa] or '+'
                exp2 = lcalcul[exp1 + 1:].index('**') + exp1 + 1
                b = lcalcul[exp2 - 1]
                indexb = ltermes.index([b, '**', '2'])
                sgnb = lsgn[indexb] or '+'

                for i in range(len(ltermes)):
                    if len(ltermes[i]) == 5 and ltermes[i].count('2') > 0 and \
                      ltermes[i].count('*') == 2 and ltermes[i].count(a) and \
                      ltermes[i].count(b):
                        indexp = i
                        sgnp = lsgn[i] or '+'

                if sgna == sgnb and sgna != sgnp:
                    poly = '(%s-%s)**2' % (a, b)
                elif sgna == sgnb and sgna == sgnp:
                    poly = '(%s+%s)**2' % (a, b)
                else:
                    # Pas d'identité remarquable
                    poly = None
                if poly:
                    if sgna == '-': poly = '-%s' % poly
                    lindex = [indexa, indexb, indexp]
                    lindex.sort()
                    lindex.reverse()
                    for i in lindex:
                        lsgn.pop(i)
                        ltermes.pop(i)

                    ltermes.insert(min(len(ltermes), indexa, indexb, indexp), Priorites3.splitting(poly))
                    res = []
                    for i in range(len(ltermes)):
                        # TODO: IndexError: list index out of range

                        if lsgn and lsgn[i]: res.append(lsgn[i])
                        res.extend(ltermes[i])
                    return "".join(res)

            if (('+' in lsgn or '' in lsgn) and '-' in lsgn) and calcul.count("**") == lcalcul.count("2") == 2 and len(ltermes) == 2:
                # 3ème identité remarquable
                # print ltermes[0][0], ltermes[1][0]
                a, b = eval(ltermes[0][0]), eval(ltermes[1][0])
                if lsgn[0] == '-': return '(%r+%r)*(%r-%r)' % (b, a, b, a)
                else: return '(%r+%r)*(%r-%r)' % (a, b, a, b)

            for k in ltermes[0]:
                commun = False
                if k[:9] == 'Polynome(':
                    commun = False
                    bdetail = False
                    pos = ltermes[0].index(k)
                    if len(ltermes[0]) == 1: bdetail = True
                    elif pos < len(ltermes[0]) - 1 and ltermes[0][pos + 1] == "**": bdetail = True
                    for i in range(len(ltermes) - 1):
                        if ltermes[i + 1].count(k):
                            commun = True
                            pos = ltermes[i + 1].index(k)
                            if len(ltermes[i + 1]) == 1: bdetail = True
                            elif pos < len(ltermes[i + 1]) - 1 and ltermes[i + 1][pos + 1] == "**": bdetail = True
                        else:
                            commun = False
                            break
                if commun: break
            if commun:
                for i in range(len(ltermes)):
                    pos = ltermes[i].index(k)
                    if len(ltermes[i]) == 1:
                        ltermes[i].extend(["*", "1"])
                    elif pos < len(ltermes[i]) - 1 and ltermes[i][pos + 1] == "**" and ltermes[i][pos + 2] == "2":
                        ltermes[i][pos + 1:pos + 3] = ["*", ltermes[i][pos]]
                    elif pos < len(ltermes[i]) - 1 and ltermes[i][pos + 1] == "**":
                        ltermes[i][pos + 2] == str(eval(ltermes[i][pos + 2]) - 1)
                    elif not bdetail:
                        del ltermes[i][pos]
                        if pos: del ltermes[i][pos - 1]
                        # supprime le symbole *
                        else: del ltermes[i][pos]
                a = []
                for i in range(len(ltermes)):
                    if lsgn[i]:a.append(lsgn[i])
                    a.extend(ltermes[i])
                if bdetail:
                    # On affiche le facteur commun de façon claire
                    return "".join(a)
                else:
                    # On effectuer la factorisation par le facteur commun
                    return "%s*(%s)" % (k, "".join(a))
            else:
                bfact = False
                for i in range(len(lcalcul)):
                    if 'Polynome(' == lcalcul[i][:9]:
                        poly = id_rem(eval(lcalcul[i]))
                        if poly:
                            bfact = True
                            lcalcul[i:i + 1] = Priorites3.splitting(poly)
                        else:
                            lcalcul[i] = repr(eval(lcalcul[i]))
                if bfact:
                    return "".join(lcalcul)
                else:
                    return None

def choix_points(min=-4, max=4, nb=5):
    """**choix_points**\ ()

    Renvoie un tuple contenant nb coordonnées sous forme de tuple telles que
    les abscisses et ordonnées sont distinctes, comprises entre min et max,
    une abscisse n'est jamais égale à une ordonnée et la coordonnée (b, a) n'est
    pas listée si la coordonnée (a, b) existe.

    >>> from pyromaths.ex.troisiemes import notion_de_fonction
    >>> notion_de_fonction.choix_points()  # doctest: +SKIP
    ((-4, -2), (-2, 0), (0, 4), (2, -4), (4, 2))

    :rtype: tuple

    """
    if nb > max - min + 1:
        raise ValueError('On demande trop de points vu le min et le max')
    abscisse = [i for i in range(min, max + 1)]
    for dummy in range(max - min - nb):
        del abscisse[randrange(len(abscisse))]
    refaire = True
    while refaire:
        ordonnee = [abscisse[i] for i in range(nb)]
        shuffle(ordonnee)
        refaire = False
        for i in range(nb):
            if abscisse[i] == ordonnee[i] or abscisse.index(ordonnee[i]) == ordonnee.index(abscisse[i]):
                refaire = True
                break
    return tuple([(abscisse[i], ordonnee[i]) for i in range(nb)])

def Lagrange(points):
    """**Lagrange**\ (*points*)
    Renvoie le polynôme d'interpolation de Lagrange pour les points de coordonnées *points*

    Est prévue pour être utilisé avec :py:func:`choix_points`

    Associé à  :py:func:`pyromaths.outils.Priorites3.priorites`, permet d'obtenir sa version réduite.

    Associé à  :py:func:`pyromaths.outils.Priorites3.plotify`, permet d'obtenir sa version utilisable avec psplot.

    >>> from pyromaths.ex.troisiemes import notion_de_fonction
    >>> p = notion_de_fonction.Lagrange(((-4, -2), (-2, 0), (0,4), (2,-4), (4,2)))

    >>> from pyromaths.outils import Priorites3
    >>> Priorites3.priorites(p)[-1]
    ['Polynome([[Fraction(5, 48), 4], [Fraction(1, 8), 3], [Fraction(-23, 12), 2], [Fraction(-3, 2), 1], [Fraction(4, 1), 0]], "x", 0)']
    >>> Priorites3.plotify(Priorites3.priorites(p)[-1])
    5/48*x^4+1/8*x^3-23/12*x^2-3/2*x^1+4/1
    """
    PIL = []
    for i in range(len(points)):
        if points[i][1]:
            PIL.append('Fraction(%s, ' % points[i][1])
            produit = []
            for j in  range(len(points)):
                if j != i: produit.append(repr(points[i][0] - points[j][0]))
            produit = repr(eval("*".join(produit)))
            PIL[i] += produit + ")*"
            produit = []
            for j in  range(len(points)):
                if j != i and points[j][0] > 0: produit.append("Polynome(\"x-%s\", details = 0)" % points[j][0])
                elif j != i and points[j][0] < 0: produit.append("Polynome(\"x+%s\", details = 0)" % -points[j][0])
                elif j != i and points[j][0] == 0: produit.append("Polynome(\"x\", details = 0)")
            produit = "*".join(produit)
            PIL[i] += produit
        else:
            PIL.append('0')
    return "+".join(PIL)

