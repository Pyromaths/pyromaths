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

'''
Created on 19 déc. 2014

@author: jerome
'''
from pyromaths.outils.Arithmetique import carrerise
from pyromaths.outils.decimaux import decimaux
from pyromaths.outils import Priorites3
from pyromaths import classes

from math import sqrt
class SquareRoot():
    '''
    Définit la classe SquareRoot permettant de manipuler des racines carrées.
    
    SquareRoot([a,b], [c, d], e) ou SquareRoot([a,b], [c, d], [e, None]) permet de définir a*sqrt(b)+c*sqrt(d)+e
    
    Cette définition permet d'utiliser pyromaths.outils.Priorites3
    
    >>> from pyromaths.classes.SquareRoot import SquareRoot
    >>> repr(SquareRoot(-4,[-2,1],[3,45],[-1,7],8))
    SquareRoot([[-4, None], [-2, 1], [3, 45], [-1, 7], [8, None]])
    '''


    def __init__(self, *radicandes):
        '''
        Constructor
        '''
        #  print radicandes, len(radicandes), radicandes[0], len(radicandes[0])
        if len(radicandes) == 1 and len(radicandes[0]) == 2 and not isinstance(radicandes[0][0], list) and not isinstance(radicandes[0][1], list):
            # SquareRoot([3, 4]),
            self.racines = [radicandes[0]]
        else:
            if len(radicandes) == 1 and (len(radicandes[0]) != 2 or isinstance(radicandes[0][0], list) or isinstance(radicandes[0][1], list)):
                # SquareRoot([1, [3, 4]])
                radicandes = radicandes[0]
            self.racines = []
            for arg in radicandes:
                if isinstance(arg, list) and len(arg) == 2:
                    # On gère a*sqrt(b)
                    if isinstance(arg[1], (float, int))and arg[1] < 0:
                        raise ValueError(u'Le radicande doit être un nombre positif.')
                    else:
                        self.racines.append(arg)
                elif isinstance(arg, (float, int)):
                    self.racines.append([arg, None])
                else:
                    raise ValueError(u'Not Implemented : SquareRoot(%s)' % arg)

    def __str__(self):
        r"""Renvoie une version LaTeX d'un objet SquareRoot.

        >>> from pyromaths.classes.SquareRoot import SquareRoot
        >>> str(SquareRoot([[-4, None], [-2, 1], [3, 45], [-1, 7], [8, None]]))
        -4-2\,\sqrt{1}+3\,\sqrt{45}-\sqrt{7}+8

        :rtype: String
        """
        def print_coef(coef):
            """Gère le format du coef
            """
            if isinstance(coef, (float, int)):
                if coef > 0: return "+" + decimaux(coef)
                else: return decimaux(coef)
            if isinstance(coef, classes.Fractions.Fraction):
                if isinstance(coef.n, int) and isinstance(coef.d, int) and coef.n < 0 and coef.d > 0:
                    return "-" + str(Fraction(-coef.n, coef.d, coef.code))
                return "+" + str(coef)
            if isinstance(coef, str):
                texte = "(" + "".join(Priorites3.texify([Priorites3.splitting(coef)])) + ")"
                if texte[0] != "-": return "+" + texte
                else: return texte
        s = ""
        for m in self.racines:
            if m[1] == None:
                # pas de racine ici
                s = s + print_coef(m[0])
            else:
                # Racine carrée
                if m[0] == 1:
                    s += r'+\sqrt{%s}' % m[1]
                elif m[0] == -1:
                    s += r'-\sqrt{%s}' % m[1]
                else:
                    s += print_coef(m[0]) + r'\,\sqrt{%s}' % m[1]
        # supprime le + en début de séquence
        s = s.lstrip("+")
        if not s: s = "0"
        return s

    def __repr__(self):
        """Renvoie une chaîne de caractère représentant un :mod:`SquareRoot`
        évaluable pour créer un :mod:`SquareRoot`.

        >>> from pyromaths.classes.SquareRoot import SquareRoot
        >>> repr(SquareRoot(-4, [-2, 1], [3, 45], [-1, 7], 8))
        SquareRoot([[-4, None], [-2, 1], [3, 45], [-1, 7], [8, None]])

        :rtype: String
        """
        return "SquareRoot(%s)" % self.racines

    def __len__(self):
        """*object*\ .\ **__len__**\ ()

        Renvoie le nombre d'éléments de l'objet SquareRoot.

        >>> from pyromaths.classes.SquareRoot import SquareRoot
        >>> len(SquareRoot(3, [2, 2], [4, 5]))
        3

        :rtype: integer
        """
        return len(self.racines)

    def __getitem__(self, i):
        """*object*\ .\ **__getitem__**\ (*integer*)

        Renvoie le i ème élément de l'objet SquareRoot.

        >>> from pyromaths.classes.SquareRoot import SquareRoot
        >>> SquareRoot(3, [2, 2], [4, 5])[2]
        [4, 5]

        :rtype: list
        """
        return self.racines[i]


    def __add__(self, other):
        """Renvoie la somme d'un objet SquareRoot et d'un nombre.
        
        >>> from pyromaths.classes.SquareRoot import SquareRoot
        >>> repr(SquareRoot([3,45],3)+SquareRoot([2,45]))
        SquareRoot([[3, None], [5, 45]])
        
        :rtype: SquareRoot
        """

        if not isinstance(other, SquareRoot):
            other = SquareRoot([other, None])
        self.racines.extend(other.racines)
        return SquareRoot(self.racines).simplifie()

    def __radd__(self, other):
        """
        >>> from pyromaths.classes.SquareRoot import SquareRoot
        >>> repr(2+SquareRoot([3,45],3))
        SquareRoot([[5, None], [3, 45]])

        :rtype: SquareRoot
        """
        other = SquareRoot([other, None])
        other.racines.extend(self.racines)
        return SquareRoot(other.racines).simplifie()

    def __neg__(self):
        """*object*\ .\ **__neg__**\ ()

        ``p.__neg__()`` est équivalent à ``-p`` est équivalent à ``p = -p``

        Renvoie l'opposé d'un objet SquareRoot.

        :rtype: SquareRoot
        """
        if self.EstDecomposable() or self.EstReductible(): return '-%r' % self.simplifie()
        r = list(self.racines)
        for i in range(len(r)):
            r[i][0] = -r[i][0]
        return SquareRoot(r)

    def __abs__(self):
        """ Renvoie la valeur absolue d'un objet SquareRoot
        
        >>> from pyromaths.classes.SquareRoot import SquareRoot
        >>> repr(abs(SquareRoot([5, 5], [-2, 7])))
        SquareRoot([[5, 5], [-2, 7]])
        >>> repr(abs(SquareRoot([-5, 5], [2, 7])))
        SquareRoot([[5, 5], [-2, 7]])
       
        :rtype: SquareRoot
        """
        t = 0
        for e in self.racines:
            if e[1] == None: t += e[0]
            else: t += e[0] * sqrt(e[1])
        if t > 0: return self
        else: return -self


    def __mul__(self, other):
        """Multiplie un objet SquareRoot par un nombre.
        
        >>> from pyromaths.classes.SquareRoot import SquareRoot
        >>> repr(SquareRoot([3,45],3)*SquareRoot([2,45],-1))
        SquareRoot([['6*45', None], [-3, 45], [6, 45], [-3, None]])
        """
        if not isinstance(other, SquareRoot):
            other = SquareRoot([other, None])
        reduction = False
        if self.EstReductible():
            self = self.simplifie()
            reduction = True
        if other.EstReductible():
            other = other.simplifie()
            reduction = True
        if reduction: return '%r*%r' % (self, other)
        lprod = []
        for e in self.racines:
            for f in other.racines:
                if e[1] == None or f[1] == None:
                    lprod.append([e[0] * f[0], max(e[1], f[1])])
                elif e[1] == f[1]:
                    lprod.append(['%r*%r' % (e[0] * f[0], e[1]), None])
                elif carrerise(e[1]) == 1 or carrerise(f[1]) == 1:
                    if carrerise(e[1]) == 1: e[0], e[1] = e[0] * int(sqrt(e[1])), 1
                    if carrerise(f[1]) == 1: f[0], f[1] = f[0] * int(sqrt(f[1])), 1
                    lprod.append([e[0] * f[0], e[1] * f[1]])
                else:
                    lprod.append([e[0] * f[0], e[1] * f[1]])
        return SquareRoot(lprod)

    def __rmul__(self, other):
        """
        >>> from pyromaths.classes.SquareRoot import SquareRoot
        >>> repr(5*SquareRoot([3,45],3))
        SquareRoot([[15, 45], [15, None]])

        :rtype: SquareRoot
        """
        return SquareRoot([other, None]) * self

    def  __floordiv__(self, other):
        """
        Division entière par un entier
        
        >>> from pyromaths.classes.SquareRoot import SquareRoot
        >>> repr(SquareRoot([10, 8], [15, 5])//5)
        SquareRoot([[2, 8], [3, 5]])

        :rtype: SquareRoot
        """
        if isinstance(other, int):
            r = list(self.racines)
            for i in range(len(r)):
                r[i][0] = r[i][0] // other
            return SquareRoot(r)
        else:
            raise NotImplemented
    def EstDecomposable(self):
        """
        Renvoie True si une des racines est de la forme sqrt{a**2*b} avec a != 1
        
        >>> from pyromaths.classes.SquareRoot import SquareRoot
        >>> SquareRoot([5, 8], [1, 7]).EstDecomposable()
        True
        >>> SquareRoot([5, 7], [1, 7]).EstDecomposable()
        False
     
        :rtype: Boolean
        """
        for e in self.racines:
            if e[1] != None and (carrerise(e[1]) != e[1] or e[1] == 1):
                return True
        return False

    def EstReductible(self):
        """
        Renvoie True si la somme de racines est réductible

        >>> from pyromaths.classes.SquareRoot import SquareRoot
        >>> SquareRoot([5, 8], [1, 45]).EstReductible()
        False
        >>> SquareRoot([5, 8], [1, 8]).EstReductible()
        True

        :rtype: Boolean
        """
        lradicandes = []
        rationnel = False
        for e in self.racines:
            if e[1] != None:
                if e[1] in lradicandes:
                    return True
                else:
                    lradicandes.append(e[1])
            elif e[1] == None:
                if rationnel: return True
                else: rationnel = True
        return False

    def Decompose(self):
        """
        Décompose une unique racine carrée de la forme a*sqrt(b^2*c) en a*sqrt(b^2)*sqrt(c)
        
        >>> from pyromaths.classes.SquareRoot import SquareRoot
        >>> SquareRoot([5, 8]).Decompose()
        SquareRoot([[5, 4]])*SquareRoot([[1, 2]])

        :rtype: string
        """
        racine = self.racines[0]
        if racine[1] == None: return repr(racine[0])
        if isinstance(racine[1], int):
            complement = carrerise(racine[1])
            if complement == 1:
                if racine[0] == 1:
                    return int(sqrt(racine[1]))
                if racine[0] == -1:
                    return -int(sqrt(racine[1]))
                if racine[1] == 1:
                    return str(racine[0])
                return '%r*%r' % (racine[0], int(sqrt(racine[1])))
            if complement == racine[1]:
                return repr(self)
            return '%r*%r' % (SquareRoot([racine[0], racine[1] / complement]), SquareRoot([1, complement]))
        raise ValueError(u'Not Implemented : SquareRoot(%s)' % racine)

    def simplifie(self):
        """
        Additionne les nombres rationnels et décompose les racines carrées.
         
        >>> from pyromaths.classes.SquareRoot import SquareRoot
        >>> repr(SquareRoot([[3, 9]]).simplifie())
        '3*3'
        >>> repr(SquareRoot(-2, [-2, 1], [3, 1], [-1, 7], 8).simplifie())
        SquareRoot([[6, None], [1, 1], [-1, 7]])
        >>> repr(SquareRoot(-2, [-2, 1], [3, 45], [-1, 7], 8).simplifie())
        SquareRoot([[6, None], [-2, 1], [3, 45], [-1, 7]])
        >>> repr(SquareRoot([-2,1],[3,45]).simplifie())
        '-2+SquareRoot([[3, 9]])*SquareRoot([[1, 5]])'
        
        :rtype: SquareRoot ou String
        """
        decomposable = self.EstDecomposable()
        reductible = self.EstReductible()
        if not decomposable and not reductible:
            return self
        if reductible:
            racines = []
            # racines = [[sum([x[0] for i, x in enumerate(self.racines) if x[1] == None]), None]]
            # TODO: cas de fractions
            lsomme = [x[0] for i, x in enumerate(self.racines) if x[1] == None]
            s = ''
            for ls in lsomme:
                if isinstance(ls, str): s += '+%s' % ls
                else: s += '+%r' % ls
            s.lstrip('+')
            racines.append([eval(s), None])
            for pos in reversed([i for i, x in enumerate(self.racines) if x[1] == None]):
                    self.racines.__delitem__(pos)
            if racines[0][0] == 0: racines = []
            while len(self.racines) > 0:
                # racines.append([sum([x[0] for i, x in enumerate(self.racines) if x[1] == self.racines[0][1]]), self.racines[0][1]])
                # TODO: cas de fractions
                lsomme = [x[0] for i, x in enumerate(self.racines) if x[1] == self.racines[0][1]]
                s = ''
                for ls in lsomme:
                    if isinstance(ls, str): s += '+%s' % ls
                    else: s += '+%r' % ls
                s.lstrip('+')
                racines.append([eval(s), self.racines[0][1]])
                if racines[-1][0] == 0: racines.pop(-1)
                for pos in reversed([i for i, x in enumerate(self.racines) if x[1] == self.racines[0][1]]):
                    self.racines.__delitem__(pos)
            if racines:
                if len(racines) == 1 and racines[0][1] == None:
                    return racines[0][0]
                else:
                    return SquareRoot(racines)
            else: return 0
        # Décomposable
        s = ''
        if len(self.racines) == 1 and isinstance(SquareRoot(self.racines).Decompose(), int):
            return SquareRoot(self.racines).Decompose()
        for e in self.racines:
            decomposee = SquareRoot(e).Decompose()
            if isinstance(decomposee, int): decomposee = str(decomposee)
            if decomposee[0]in'+-':
                s += decomposee
            else:
                s += '+' + decomposee
        s = s.lstrip('+')
        return s
