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
from pyromaths.outils.decimaux import decimaux
from pyromaths.outils import Priorites3
from pyromaths.classes.Fractions import Fraction

class Polynome():
    """Cette classe crée la notion de polynômes.
    
        >>> from pyromaths.classes.PolynomesCollege import Polynome
        >>> Polynome([[2,2],[3,1],[4,0]], 'z')
        Polynome([[2, 2], [3, 1], [4, 0]], "z", False, True)
        >>> Polynome("2y^2+3y+4")
        Polynome([[2, 2], [3, 1], [4, 0]], "y", False, True)

    Les variables e, i, j, l, o, O sont interdites pour des raisons de
    lisibilité (l, o, O) ou parce qu'elles sont utilisées comme constantes (e,
    i, j).
    """

    def __init__(self, monomes, var=None, reduire=False, detailler=True):
        """Crée un polynôme. Si ``var == None`` alors la variable est ``x``.
        
            >>> from pyromaths.classes.PolynomesCollege import Polynome
            >>> Polynome([[2,2],[3,1],[4,0]], 'z')
            Polynome([[2, 2], [3, 1], [4, 0]], "z", False, True)
            >>> Polynome("2y^2+3y+4")
            Polynome([[2, 2], [3, 1], [4, 0]], "y", False, True)
            >>> Polynome([[1, 1], [2, 2]])
            Polynome([[1, 1], [2, 2]], "x", False, True)
            >>> Polynome("Fraction(1,7)x^2-Fraction(3,8)x-1")
            Polynome([[Fraction(1, 7), 2], [Fraction(-3, 8), 1], [-1, 0]], "x", False, True)

        """
        monomes = monomes or '0'  # monômes du polynôme, par défaut un polynôme nul
        if isinstance(monomes, Polynome):
            self.monomes = monomes.monomes
            self.var = monomes.var
            self.detailler = monomes.detailler
            self.reduire = monomes.reduire
        elif isinstance(monomes, basestring):
            # Gère la construction des polynôme à partir d'une chaîne de caractères
            self.reduire = reduire
            self.detailler = detailler
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
                if not monomes[k][0]: monomes.pop(k)
                elif isinstance(monomes[k][0], str): reduire = True
            if not monomes: monomes = [[0, 0]]
            self.monomes = monomes
            self.var = var or 'x'  # Variable par défaut
            self.reduire = reduire
            self.detailler = detailler

    def __repr__(self):
        """**repr**\ (*object*)

        Renvoie une chaîne de caractère représentant un :mod:`Polynome`
        évaluable pour créer un :mod:`Polynome`.

            >>> from pyromaths.classes.PolynomesCollege import Polynome
            >>> repr(Polynome([[2,2],[3,1],[4,0]], 'z'))
            'Polynome([[2, 2], [3, 1], [4, 0]], "z", False, True)'

        :rtype: string
        """
        return "Polynome(%s, \"%s\", %s, %s)" % (self.monomes, self.var, self.reduire, self.detailler)

    def __str__(self):
        r"""**str**\ (*object*)

        Renvoie une version LaTeX du polynôme.
            >>> from pyromaths.classes.PolynomesCollege import Polynome
            >>> str(Polynome([[2,2],[3,1],[4,0]], 'z'))
            '2\\,z^{2}+3\\,z+4'
            >>> str(Polynome("y^2-Fraction(3,2)y-1"))
            'y^{2}+\\dfrac{-3}{2}\\,y-1'

        :rtype: string
        """
        def print_coef(coef):
            """Gère le format du coef
            """
            if isinstance(coef, (float, int)):
                if coef > 0: return "+" + decimaux(coef)
                else: return decimaux(coef)
            if isinstance(coef, Fraction): return "+" + str(coef)
            if isinstance(coef, str):
                texte = "(" + Priorites3.texify([Priorites3.splitting(coef)])[0] + ")"
                if texte[0] != "-": return "+" + texte
                else: return texte

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
            '4-5-(-5)**2+(-5)**3-2*(-5)**5'

        :param: valeur
        :type: integer, float or Fraction
        :rtype: string
        """
        if Polynome.degre(self) == 0:
            return self.monomes[0][0]
        if valeur == 0:
            retour = ''
            for m in self.monomes:
                if m[1] == 0: retour += '+%r' % m[0]
            return retour.lstrip('+').replace('+-', '-')
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
            >>> p
            Polynome([[2, 1], [4, 0]], "y", False, True)

        :rtype: Polynome
        """
        m = self.monomes
        del m[i]
        return Polynome(m, self.var, self.reduire, self.detailler)

    def __iadd__(self, other):
        """*object*\ .\ **__iadd__**\ (*other*)

        ``p.__iadd__(q)`` est équivalent à ``p += q``

            >>> from pyromaths.classes.PolynomesCollege import Polynome
            >>> p=Polynome("2y+3y^2+4")
            >>> p += Polynome('-y+6')
            >>> p
            Polynome([[2, 1], [3, 2], [4, 0], [-1, 1], [6, 0]], "y", False, True)

        :rtype: Polynome
        """
        if isinstance(other, (float, int, Fraction)):
            other = Polynome([[other, 0]], self.var)
#         elif isinstance(self, (float, int, Fraction)):
#             self = Polynome([[self, 0]], other.var)
        m1, m2 = [m for m in self.monomes], [m for m in other.monomes]
        if self.var != other.var and self.degre() <= 0:
            self.var = other.var
        elif self.var != other.var and other.degre() <= 0:
            other.var = self.var
        if self.var != other.var:
            raise ValueError(u'Pyromaths ne sait additionner que deux polynômes de même variable')
        else :
            m = []
            m1.extend(m2)
            for monomes in m1:
                if monomes[0]: m.append(monomes)
            return Polynome(m, self.var, detailler=self.detailler)

    def __eq__(self, other):
        """*object*\ .\ **__eq__**\ (*other*)

        ``p.__eq__(q)`` est équivalent à ``p == q``
        Renvoie True si deux polynômes sont égaux. Ne tient pas compte de
        l'ordre des monômes.

            >>> from pyromaths.classes.PolynomesCollege import Polynome
            >>> p = Polynome("2y+3y^2+4")
            >>> q = Polynome('-y+6')
            >>> p == q
            False

        :rtype: boolean
        """
        if not isinstance(other, Polynome):
            other = Polynome([[other, 0]], self.var)
        return not (self.var != other.var or \
                    sorted(self.monomes, key=lambda x: (-x[1], x[0])) != \
                    sorted(other.monomes, key=lambda x: (-x[1], x[0])))

    def __ne__(self, other):
        """*object*\ .\ **__ne__**\ (*other*)

        ``p.__ne__(q)`` est équivalent à ``p != q``
        Renvoie True si deux polynômes sont différents. Ne tient pas compte de
        l'ordre des monômes.

            >>> from pyromaths.classes.PolynomesCollege import Polynome
            >>> p = Polynome("2y+3y^2+4")
            >>> q = Polynome('-y+6')
            >>> p.__ne__(q)
            True
            >>> p != q
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
            >>> Polynome("2y+3y^2+4")+Polynome('-y+6')
            Polynome([[3, 2], [2, 1], [-1, 1], [4, 0], [6, 0]], "y", False, True)

        :param: other
        :type: Polynome ou string *évaluable comme Polynome*
        :rtype: Polynome
        """
#         if isinstance(other, basestring):
#             other = eval(other)
        for other in others:
            if isinstance(other, (float, int, Fraction)): other = Polynome([[other, 0]], self.var)
            self +=other
        return self.reduction()

    def __radd__(self, other):
        """*object*\ .\ **__radd__**\ (*other*)

        ``p.__radd__(q)`` est équivalent à ``q + p``

        >>> from pyromaths.classes.PolynomesCollege import Polynome
        >>> from pyromaths.classes.Fractions import Fraction
        >>> Fraction(5,4)+Polynome("3x")
        Polynome([[3, 1], [Fraction(5, 4), 0]], "x", False, True)

        :param: other
        :type: Polynome ou string *évaluable comme Polynome*
        :rtype: Polynome
        """
        if isinstance(other, basestring):
            other = eval(other)
        if isinstance(other, (float, int)):
            other = Polynome([[other, 0]], self.var)
        return other + self

    def __sub__(self, *others):
        """*object*\ .\ **__sub__**\ (*other*)

        ``p.__sub__(q)`` est équivalent à ``p + q``  calcule la somme de
        polynômes.

        *other* peut être une chaîne représentant un polynôme.

            >>> from pyromaths.classes.PolynomesCollege import Polynome
            >>> Polynome("2y+3y^2+4")-Polynome('-y+6')
            'Polynome([[2, 1], [3, 2], [4, 0]], "y", False, True)+Polynome([[1, 1], [-6, 0]], "y", False, True)'
            >>> Polynome("x+6")-Polynome("3x")
            Polynome([[1, 1], [-3, 1], [6, 0]], "x", False, True)

        :param: other
        :type: Polynome ou string *évaluable comme Polynome*
        :rtype: Polynome or string
        """
        sub = [self]
        for other in others:
            if not isinstance(other, Polynome):
                if isinstance(sub[-1], Polynome): sub[-1] += Polynome([[-other, 0]], self.var, False, self.detailler)
                else: sub.append(Polynome([[-other, 0]], self.var, False, self.detailler))
            elif len(other) == 1:
            # Cas où on soustrait un polynôme de longueur 1
                if isinstance(sub[-1], Polynome):
                    sub[-1] += -other
                    if other[0][0] <= 0: sub[-1] = sub[-1].ordonne()
                    # On ordonne directement 3-4x en -4x+3. Attention, -other a changé other
                else: sub.append(-other)
            else:
                sub.append(-other)
        if len(sub) == 1: return sub[0]
        for i in range(len(sub)):
            if isinstance(sub[i], Polynome): sub[i] = repr(sub[i])
        return '+'.join(sub)

    def __rsub__(self, other):
        """*object*\ .\ **__rsub__**\ (*other*)

        ``p.__rsub__(q)`` est équivalent à ``q - p``

        >>> from pyromaths.classes.PolynomesCollege import Polynome
        >>> 1-Polynome([[-4, 1], [-9, 2], [-5, 0]], "x")
        'Polynome([[1, 0]], "x", False, True)+Polynome([[4, 1], [9, 2], [5, 0]], "x", False, True)'
        >>> from pyromaths.classes.Fractions import Fraction
        >>> Fraction(5,4)-Polynome("3x")
        Polynome([[-3, 1], [Fraction(5, 4), 0]], "x", False, True)
        >>> Fraction(5,4)-Polynome("-3x")
        Polynome([[Fraction(5, 4), 0], [3, 1]], "x", False, True)

        :param: other
        :type: Polynome ou string *évaluable comme Polynome*
        :rtype: Polynome
        """
        other = Polynome([[other, 0]], self.var)
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
            >>> -Polynome("2y+3y^2+4")
            Polynome([[-2, 1], [-3, 2], [-4, 0]], "y", False, True)

        :rtype: Polynome
        """
        m = [m1 for m1 in self.monomes]
        for i in range(len(m)):
            if isinstance(m[i][0], str): return '-%r' % self.reduction()
            elif isinstance(m[i][0], Fraction) and m[i][0].code: m[i][0] = -m[i][0].traitement()
            else: m[i][0] = -m[i][0]
        return Polynome(m, self.var, self.reduire, self.detailler)

    def __pos__(self):
        """*object*\ .\ **__pos__**\ ()

        ``p.__pos__()`` est équivalent à ``+p``

        Renvoie le polynôme.

            >>> from pyromaths.classes.PolynomesCollege import Polynome
            >>> +Polynome("2y+3y^2+4")
            Polynome([[2, 1], [3, 2], [4, 0]], "y", False, True)

        :rtype: Polynome
        """
        return self


    def __mul__(self, *others):
        """*object*\ .\ **__mul__**\ (*other*)

        ``p.__mul__(q)`` est équivalent à ``p * q``

        **TODO :** Cas d'un produit par 0 ou 1

        Renvoie une chaîne de caractère ou un objet Polynôme dont les éléments
        sont :

        * le produit de ``p`` et ``q`` si ce sont deux monômes dont un au moins
          a pour coefficient 1.
        * le produit détaillé de ``p`` et ``q`` si ce sont deux monômes ne
          dépendant pas du cas précédent.
        * le développement par distributivité dans les autres cas
        * **TODO :** le développement par une identité remarquable si ``p ==
          q`` ou si ``p`` et ``q`` sont respectivement de la forme ``a.x + b``
          et ``a.x - b``

            >>> from pyromaths.classes.PolynomesCollege import Polynome
            >>> Polynome('3x+4')*Polynome('2x+5')
            'Polynome([[3, 1]], "x", False, True)*Polynome([[2, 1]], "x", False, True)+Polynome([[3, 1]], "x", False, True)*Polynome([[5, 0]], "x", False, True)+Polynome([[4, 0]], "x", False, True)*Polynome([[2, 1]], "x", False, True)+Polynome([[4, 0]], "x", False, True)*Polynome([[5, 0]], "x", False, True)'
            >>> Polynome('3x')*Polynome('2x')
            "3*2*Polynome([[1, 1]], 'x', False, True)*Polynome([[1, 1]], 'x', False, True)"
            >>> Polynome('3x')*Polynome('x')
            Polynome([[3, 2]], "x", False, True)

        :param: other
        :type: Polynome ou string *évaluable comme Polynome*
        :rtype: string ou Polynome
        """
        def id_rem(p1, p2):
            '''Renvoie 1, 2 ou 3 selon l'identité remarquable trouvée, None sinon'''
            if len(p1) != 2 or len(p2) != 2: return None
            p1, p2 = p1.ordonne(), p2.ordonne()
            if p1 == p2:
                if p1[0][0] * p1[1][0] > 0:  return 1
                else: return 2
            if (p1[0][1] == p2[0][1] and p1[1][1] == p2[1][1]) and (p1[0][0] == p2[0][0] and\
                p1[1][0] == -p2[1][0]) or (p1[0][0] == -p2[0][0] and p1[1][0] == p2[1][0]): return 3
            return None

        if not isinstance(others[0], Polynome):
            others[0] = Polynome(repr(others[0]), self.var)
        if self == 0: return 0
        lother, detailler, var, reduire = [self], self.detailler, self.var, False
        if self == 1: lother = []
        for other in others:
            if other == 0:
                return 0
            elif other == 1:
                pass
            elif isinstance(other, Polynome):
                if var != other.var: raise ValueError(u'Pyromaths ne sait multiplier que deux polynômes de même variable : %r et %r' % (self, other))
                detailler = detailler and other.detailler
                reduire = reduire or other.reduire
                lother.append(other)
            elif isinstance(other, (int, float, Fraction)):
                lother.append(Polynome([[other, 0]], var))
            else:
                raise ValueError(u'Format not implemented : %s' % (other))
        if reduire:
            lother = [other.reduction() for other in lother]
            return "*".join([repr(other) for other in lother])

        if len(lother) == 0: return 1  # Produit de polynômes égaux à 1
        elif len(lother) == 1: return lother[0]  # Produit d'un polynôme par 1
        if len(lother[0]) == len(lother[1]) == 1:
            coef, exp, finaliser = [], [], True
            if lother[0][0][0] != 1:coef.append(repr(lother[0][0][0]))
            if lother[0][0][1] != 0:exp.append(lother[0][0][1])
            if coef and exp: finaliser = False
            i = 1
            while i < len(lother) and len(lother[i]) == 1:
                if lother[i][0][0] != 1:
                    coef.append(repr(lother[i][0][0]))
                    if coef[-1][0] == '-':coef[-1] = '(' + coef[-1] + ')'
                if lother[i][0][1] != 0:exp.append(lother[i][0][1])
                finaliser = finaliser and (lother[i][0][0] != 1 and not exp) or (lother[i][0][0] == 1 and lother[i][0][1])
                i += 1
            if finaliser or not detailler:
                if len(coef) > 1: coef = Priorites3.priorites('*'.join(coef))[0]
                else:
                    if isinstance(eval(coef[0]), (float, int)): coef[0]
                    elif isinstance(eval(coef[0]), Fraction) and eval(coef[0]).code:
                        coef = Priorites3.priorites(coef[0])[0]
                    else: coef[0]
                if len(coef) > 1: coef = ''.join(coef)
                else: coef = eval(coef[0])
                if exp: exp = reduce(lambda x, y: x + y, exp)
                else: exp = 0
                m = Polynome([[coef, exp]], var, isinstance(coef, str), True)
                if len(lother) > i: return repr(m) + "*" + "*".join([repr(other) for other in lother[i:]])
                else: return m
            else:
                exp = ["Polynome([[1, %s]], '%s', False, True)" % (puiss, var) for puiss in exp]
                m = "*".join(coef) + "*" + "*".join(exp)
                if len(lother) > i: return m + "*" + "*".join([repr(other) for other in lother[i:]])
                else: return m
        elif id_rem(lother[0], lother[1]):
            i = 2
            ident = id_rem(lother[0], lother[1])
            if ident < 3: m = lother[0] ** 2
            else:
                # 3e identité remarquable
                if lother[0][0] == lother[1][0]:
                    m = "%r**2-%r**2" % (Polynome([lother[0][0]], var, reduire, detailler), \
                                            Polynome([[abs(lother[0][1][0]), lother[0][1][1]]], var, reduire, detailler))
                else:
                    m = "%r**2-%r**2" % (Polynome([lother[0][1]], var, reduire, detailler), \
                                            Polynome([[abs(lother[0][0][0]), lother[0][0][1]]], var, reduire, detailler))
            if len(lother) > i: return "(" + m + ")*" + "*".join([repr(other) for other in lother[i:]])
            else: return m
        else:
            i = 2
            m = []
            for f1 in lother[0].monomes:
                # Distributivité
                for f2 in lother[1].monomes:
                    if detailler:
                        m.append(repr(Polynome([f1], var, False, True)) + "*" + repr(Polynome([f2], var, False, True)))
                    else:
                        if f2[0] < 0:coef = Priorites3.priorites('%r*(%r)' % (f1[0], f2[0]))[0]
                        else: coef = Priorites3.priorites('%r*%r' % (f1[0], f2[0]))[0]
                        exp = f1[1] + f2[1]
                        if len(coef) > 1: coef = ''.join(coef)
                        else: coef = eval(coef[0])
                        m.append(repr(Polynome([[coef, exp]], var, isinstance(coef, str), False)))
            m = "+".join(m)
            if len(lother) > i: return "(" + m + ")*" + "*".join([repr(other) for other in lother[i:]])
            else: return m


    def __rmul__(self, other):
        """Multiplication de *other* (qui n'est pas un polynôme) par *object*
        (qui en est un)

        * Si *other* est une suite de produits de monômes, et *self* un polynôme
          de rang 1, on effectue toutes les multiplications en une fois
        * Sinon, on calcule d'abord @other

        :param: other
        :type: Polynome ou string *évaluable comme Polynome*
        :rtype: string ou Polynome"""
        if isinstance(other, (int, float, Fraction)):
            other = Polynome([[other, 0]], self.var)
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
                    if self.monomes[0][0] < 0: ls.insert(index, "(" + repr(self.monomes[0][0]) + ", %s, %s)" % (self.reduire, self.detailler))
                    else: ls.insert(index, repr(self.monomes[0][0]))
                if self.monomes[0][1] > 0:
                    ls.append("*")
                    ls.append("Polynome([%s], \"%s\", %s, %s)" % ([1, self.monomes[0][1]], self.var, self.reduire, self.detailler))
                return "".join(ls)
        else: raise ValueError(u"Type non prévu. Bogue en perspective !")

    def __div__(self, other):
        """*object*\ .\ **div**\ (*other*)

        ``p.__div__(q)`` est équivalent à ``p / q``

        Renvoie deux polynomes où le premier élément est le quotient et le second
        le reste de la division euclidienne de self par other.

            >>> from pyromaths.classes.PolynomesCollege import Polynome
            >>> Polynome('3x+4', detailler = False)/Polynome('2x+5', detailler = False)
            (Polynome([[Fraction(3, 2), 0]], "x", False, True), Polynome([[Fraction(-7, 2), 0]], "x", False, False))
            >>> Polynome("x^4+2x^3+3x^2+5x+6") / Polynome("7x+8")
            (Polynome([[Fraction(1, 7), 3], [Fraction(6, 49), 2], [Fraction(99, 343), 1], [Fraction(923, 2401), 0]], "x", False, True), Polynome([[Fraction(7022, 2401), 0]], "x", False, True))

        :param: other
        :type: Polynome ou string *évaluable comme Polynome*
        :rtype: Deux Polynome
        """
        if isinstance(other, (float, int)):
            return Fraction(1, other) * self
        elif isinstance(other, Fraction):
            return (1 / other) * self
        else:
            quotient = Polynome([], self.var, self.detailler)
            reste = Polynome.ordonne(self)
            diviseur = other.ordonne()
            degre_diviseur = diviseur.degre()
            while reste.degre() >= degre_diviseur:
                degre = reste.degre() - degre_diviseur
                if isinstance(reste[0][0], Fraction) or isinstance(diviseur[0][0], Fraction):
                    coef = eval(Priorites3.priorites('%r/%r' % (reste[0][0], diviseur[0][0]))[-1][0])
                else:
                    coef = Fraction(reste[0][0], diviseur[0][0])
                quotient.monomes.append([coef, degre])
#                 print '%r-Polynome([[%r, %s]], "%s", %s, %s)*%r' % (reste, coef, degre, self.var, self.reduire, self.detailler, diviseur)
                reste = eval(Priorites3.priorites('%r-Polynome([[%r, %s]], "%s", %s, %s)*%r' % (reste, coef, degre, self.var, self.reduire, self.detailler, diviseur))[-1][0])
            return quotient.reduit(), reste

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
        if self == Polynome(""): return -1
        else: return self.reduit()[0][1]

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
            >>> Polynome("2y+4")**2
            'Polynome([[2, 1]], "y", False, True)**2+2*Polynome([[2, 1]], "y", False, True)*Polynome([[4, 0]], "y", False, True)+Polynome([[4, 0]], "y", False, True)**2'
            >>> Polynome("2y")**3
            Polynome([[8, 3]], "y", False, True)

        :rtype: string ou Polynome
        """
        if len(self) == 2 and other == 2:
            a0 = self.monomes[0][0]
            b0 = self.monomes[1][0]
            p = a0 * b0
            a = Polynome([[abs(a0), self.monomes[0][1]]], self.var, self.reduire, self.detailler)
            b = Polynome([[abs(b0), self.monomes[1][1]]], self.var, self.reduire, self.detailler)
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

    def reduit(self):
        """**reduit**\ (*object*)

        Retourne une version réduite et ordonnée du polynôme

            >>> from pyromaths.classes.PolynomesCollege import Polynome
            >>> Polynome.reduit(Polynome([[2, 1], [3, 2], [4, 0], [-1, 1], [6, 0]], "y"))
            Polynome([[3, 2], [1, 1], [10, 0]], "y", False, True)

        :param type: Polynome
        :rtype: Polynome
        """
#         from pyromaths.classes.Fractions import Fraction
        polynome, reduire = [], False
        for monome in self.ordonne().monomes:
            if polynome and monome[1] == polynome[-1][1]:
#                 if isinstance(monome[0],(float,int)): decimaux = decimaux and True
#                 else: decimaux=False
                if isinstance(polynome[-1][0], list):
                    polynome[-1][0].append(repr(monome[0]))
                else:
                    polynome[-1][0] = [polynome[-1][0]]
                    polynome[-1][0].append(repr(monome[0]))
            else:
#                 if isinstance(monome[0],(float,int)): decimaux = True
#                 else: decimaux=False
                polynome.append([repr(monome[0]), monome[1]])
        for k in range(len(polynome) - 1, -1, -1):
            if isinstance(polynome[k][0], list):
                decimaux = True
                for nb in polynome[k][0]:
                    if isinstance(eval(nb), (float, int)): decimaux = decimaux and True
                    else: decimaux = False
                if decimaux:
                    # On effectue directement la somme de nombres entiers et/ou décimaux
                    polynome[k][0] = eval('+'.join(polynome[k][0]))
                else:
                    res = Priorites3.priorites('+'.join(polynome[k][0]))
                    if res:
                        if len(res[0]) > 1:
                            polynome[k][0] = ''.join(res[0])
                            reduire = True
                        else: polynome[k][0] = eval(res[0][0])
                    else:polynome[k][0] = eval('+'.join(polynome[k][0]))
                    if polynome[k][0] == 0: polynome.pop(k)
            else: polynome[k][0] = eval(polynome[k][0])
        return Polynome(polynome, self.var, reduire, self.detailler)

    def reduction(self, final=False):
        """**reduction**\ (*object*)
        
        Évalue chaque coefficient d'un polynôme et le réduit si nécessaire
        Si *final* est vrai, alors simplifie les fractions dans le polynôme.
        
            >>> Polynome([[2, 1], [3, 2], [4, 0], [-1, 1], [6, 0]], "y").reduction()
            Polynome([[3, 2], [2, 1], [-1, 1], [4, 0], [6, 0]], "y", False, True)
            >>> Polynome([[3, 2], [2, 1], [-1, 1], [4, 0], [6, 0]], "y").reduction()
            Polynome([[3, 2], ['2-1', 1], [10, 0]], "y", True, True)
            >>> Polynome([[3, 2], ['2-1', 1], [10, 0]], "y", True).reduction()
            Polynome([[3, 2], [1, 1], [10, 0]], "y", False, True)
            >>> Polynome([[3, 2], [2, 1], [-1, 1], [4, 0], [6, 0]], "y", detailler=False).reduction()
            Polynome([[3, 2], [1, 1], [10, 0]], "y", False, False)

        """
        delai = False
        for i in xrange(len(self) - 1, -1, -1):
            # Vérifie si des coefficients sont à calculer
            m = self[i]
            self.reduire = False
            if isinstance(m[0], str):
                res = Priorites3.priorites(m[0])
                if res and len(res[0]) == 1:
                    delai = True
                    self[i][0] = eval(res[0][0])
                    if self[i][0] == 0: del self[i]
                elif res:
                    delai = True
                    self.reduire = True
                    self[i][0] = ''.join(res[0])
                else:
                    self[i][0] = eval(self[i][0])
                    if self[i][0] == 0: del self[i]
            elif isinstance(m[0], Fraction) and m[0].code:
                delai = True
                self[i][0] = m[0].traitement()
        if delai: return self
        if self.detailler:
            if self.monomes != self.ordonne().monomes:
                "Ordonne un polynôme"
                return self.ordonne()
            deg, factoriser = -1, False
            for m in self.monomes:
                if m[0] and deg == m[1]:
                    factoriser = True
                    break
                elif isinstance(m[0], Fraction):
                    if isinstance(m[0].traitement(True), str): self.reduire = True
                elif isinstance(m[0], str): self.reduire = True
                else:
                    deg = m[1]
            if factoriser:
                "Écrit les factorisation qui permettent de réduire le polynôme"
                return self.reduction_detaillee()
        else:
            p = self.reduit()
            if repr(p) != repr(self): return p
        if self.reduire:
            "Calcule chaque factorisation"
            reduire = False
            for i in xrange(len(self) - 1, -1, -1):
                if isinstance(self[i][0], str):
                    if len(Priorites3.splitting(self[i][0])) > 1:
                        coeff = Priorites3.priorites(self[i][0])[0]
                        self[i][0] = "".join(coeff)
                        if len(coeff) > 1:
                            reduire = True
                        else:
                            self[i][0] = eval(self[i][0])
#                             if isinstance(self[i][0], (float, int)): reduire = False
                            if isinstance(self[i][0], Fraction):
                                if self[i][0].code: reduire = True
                                elif repr(self[i][0].traitement(True)) != repr(self[i][0]): reduire = True
#                                 else: reduire = False
                    else:
                        self[i][0] = eval(self[i][0])
                        if isinstance(self[i][0], Fraction):
                            f = self[i][0].traitement(True)
                            if isinstance(f, str) or repr(f) != repr(self[i][0]):
                                self[i][0] = f
                                if isinstance(f, str) or repr(f.traitement(True)) != repr(f): reduire = True
                    if self[i][0] == 0:
                        del self[i]
                elif isinstance(self[i][0], Fraction):
                    f = self[i][0].traitement(True)
                    if isinstance(f, str) or repr(f) != repr(self[i][0]):
                        self[i][0] = f
                        if isinstance(f, str) or repr(f.traitement(True)) != repr(f): reduire = True
            self.reduire = reduire
            return self
        elif final:
            for i in range(len(self)):
                if isinstance(self[i][0], Fraction):
                    f = self[i][0].traitement(True)
                    if repr(f) != repr(self[i][0]):
                        self[i][0] = f
            return self
        else: return self

    def reduction_detaillee(self):
        """**reduction_detaillee**\ (*object*)

        Cette fonction écrit les factorisation qui permettent de réduire un polynôme

        >>> from pyromaths.classes.PolynomesCollege import Polynome
        >>> Polynome([[2, 1], [3, 2], [4, 0], [-1, 1], [6, 0]], "y").reduction_detaillee()
        Polynome([[2, 1], [3, 2], [4, 0], [-1, 1], [6, 0]], "y", False, True)
        >>> Polynome([[3, 2], [2, 1], [-1, 1], [4, 0], [6, 0]], "y").reduction_detaillee()
        Polynome([[3, 2], ['2-1', 1], [10, 0]], "y", True, True)
        >>> from pyromaths.classes.Fractions import Fraction
        >>> Polynome([[5, 1], [Fraction(1, 3), 1], [3, 0], [4, 0], [7, 0]], "x", False, True).reduction_detaillee()
        Polynome([['5+Fraction(1, 3)', 1], [14, 0]], "x", True, True)
        >>> Polynome([[5, 1], [1, 0], [Fraction(1, 3), 0], [3, 0]], "x", False, True).reduction_detaillee()
        Polynome([[5, 1], ['Fraction("1*3", "1*3", "r")+Fraction(1, 3)+Fraction("3*3", "1*3", "r")', 0]], "x", True, True)

        :param type: Polynome
        :rtype: Polynome
        """
        reduction = []
        for m in self.monomes:
            if reduction and m[1] == reduction[-1][1]:
                if m[0]:
                    if isinstance(reduction[-1][0], str):
                        if not isinstance(m[0], str): m[0] = repr(m[0])
                        if repr(m[0])[0] in '+-': reduction[-1][0] += m[0]
                        else: reduction[-1][0] += "+" + m[0]
                    else:
                        if not isinstance(m[0], str): m[0] = repr(m[0])
                        if m[0][0] in '+-': reduction[-1][0] = "%r%s" % (reduction[-1][0], m[0])
                        else: reduction[-1][0] = "%r+%s" % (reduction[-1][0], m[0])
            else:
                reduction.append(m)
        if reduction[-1][1] == 0 and isinstance(reduction[-1][0], str):
            detail = Priorites3.priorites(reduction[-1][0])
            if len(detail) == 1:
                reduction[-1][0] = eval(detail[0][0])
            else:
                reduction[-1][0] = "".join(detail[0])
        return Polynome(reduction, self.var)

    def reductible(self):
        """**reductible**\ (*object*)

        Retourne True si le polynôme est réductible, False sinon.

            >>> from pyromaths.classes.PolynomesCollege import Polynome
            >>> Polynome([[2, 1], [3, 2], [4, 0], [-1, 1], [6, 0]], "y").reductible()
            True

        :param type: Polynome
        :rtype: boolean
        """
        if self != self.reduit():
            return True
        else:
            return False

    def ordonne(self):
        """**ordonne**\ (*object*)

        Retourne une version ordonnée d'un polynôme en écrivant en premier les
        monômes de degré supérieur.

            >>> from pyromaths.classes.PolynomesCollege import Polynome
            >>> Polynome([[2, 1], [3, 2], [4, 0], [-1, 1], [6, 0]], "y").ordonne()
            Polynome([[3, 2], [2, 1], [-1, 1], [4, 0], [6, 0]], "y", False, True)

        :param type: Polynome
        :rtype: Polynome
        """
#         if len(self) == 1: return self
        m1 = self.monomes
        m1 = sorted(m1, key=lambda x: (-x[1]))
        return Polynome(m1, self.var, self.reduire, self.detailler)
