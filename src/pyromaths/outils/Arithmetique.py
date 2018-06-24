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
import math, random

def pgcd(*n):
    """**pgcd**\ (*n*)

    Calcule le pgcd de plusieurs entiers entiers.

    Merci à http://python.jpvweb.com/mesrecettespython/doku.php?id=pgcd_ppcm

    :param n: Les entiers dont on veut le pgcd
    :type n: integer

    >>> from pyromaths.outils import Arithmetique
    >>> Arithmetique.pgcd(64,72,36)
    4

    :rtype: integer
    """
    from pyromaths.classes.SquareRoot import SquareRoot
    def _pgcd(a, b):
        #=======================================================================
        # print "pgcd dans arithmetique ", a, b, isinstance(a, int), isinstance(b, int)
        # print repr(a), repr(b)
        #=======================================================================
        if abs(a) == float('inf') or abs(b) == float('inf'): return 1
        while b: a, b = b, a % b
        return a
    # Pour pouvoir utiliser pgcd(a) où a=(2,4,6) :
    n = list(n)
    if isinstance(n[0], (list, tuple)): n = n[0]
    # Pour chercher à simplifier une fraction avec un objet SquareRoot
    if isinstance(n[0], SquareRoot):
        if len(n[0]) > 1:
            n[0] = pgcd(*[n[0][i][0] for i in range(len(n[0]))])
        else:
            n[0] = n[0][0][0]
    if isinstance(n[1], SquareRoot):
        if len(n[1]) > 1:
            n[1] = pgcd(*[n[1][i][0] for i in range(len(n[0]))])
        else: n[1] = n[1][0][0]
    p = _pgcd(n[0], n[1])
    for x in n[2:]:
        p = _pgcd(p, x)
    return p

def ppcm(*n):
    """**ppcm**\ (*n*)

    Calcule le ppcm de plusieurs entiers.

    Merci à http://python.jpvweb.com/mesrecettespython/doku.php?id=pgcd_ppcm

    :param n: Les entiers dont on veut le ppcm
    :type n: integer

    >>> from pyromaths.outils import Arithmetique
    >>> Arithmetique.ppcm(64, 72, 36)
    576

    :rtype: integer
    """
    def _pgcd(a, b):
        while b: a, b = b, a % b
        return a
    p = abs(n[0] * n[1]) // _pgcd(n[0], n[1])
    for x in n[2:]:
        p = abs(p * x) // _pgcd(p, x)
    return p

def premier(n):
    """**premier**\ (*n*)

    Teste si un nombre est premier.

    :param n: Nombre à tester
    :type n: integer

    >>> from pyromaths.outils import Arithmetique
    >>> Arithmetique.premier(2673)
    False

    :rtype: boolean
    """
    return not [x for x in range(2, int(math.sqrt(n)) + 1)
                if n % x == 0]

def eratosthene(n):
    """**eratosthene**\ (*n*)

    Établit la liste des nombres premiers inférieurs a n.

    :param n: borne supérieure
    :type n: integer

    >>> from pyromaths.outils import Arithmetique
    >>> Arithmetique.eratosthene(26)
    [2, 3, 5, 7, 11, 13, 17, 19, 23]

    :rtype: list
    """
    return [x for x in range(2, n) if premier(x)]


def factor(n):
    """**factor**\ (*n*)

    Retourne la liste des facteurs premiers du nombre n.

    :param n: Nombre à décomposer
    :type n: integer

    >>> from pyromaths.outils import Arithmetique
    >>> Arithmetique.factor(2673)
    [3, 3, 3, 3, 3, 11]
    >>> Arithmetique.factor(23)
    [23]

    :rtype: list
    """
    premiers = []
    candidats = list(range(2, n + 1))
    candidat = 2
    while not premiers and candidat in candidats:
        if n % candidat == 0 and premier(candidat):
            premiers.append(candidat)
            premiers = premiers + factor(old_div(n, candidat))
        candidat += 1
    return premiers


def factorise(n):
    """**factorise**\ (*n*)

    Retourne la liste des facteurs premiers du nombre n, ainsi que le détail de
    la factorisation.

    :param n: Nombre à décomposer
    :type n: integer

    >>> from pyromaths.outils import Arithmetique
    >>> Arithmetique.factorise(2673)
    ([3, 3, 3, 3, 3, 11], [['3', '891'], ['3', '3', '297'], ['3', '3', '3', '99'], ['3', '3', '3', '3', '33'], ['3', '3', '3', '3', '3', '11']])

    :rtype: tuple
    """
    primes = []
    etapes = []
    primes_etapes = []
    limite = int(math.sqrt(n)) + 1
    candidate = 2
    while (candidate < limite):
        if n % candidate == 0:
            primes.append(candidate)
            primes_etapes.append(str(candidate))
            n = old_div(n, candidate)
            if n == 1:
                break
            primes_etapes.append(str(n))
            etapes.append(primes_etapes)
            primes_etapes = primes_etapes[:-1]
        else:
            candidate += 1
    if (n != 1) or (primes == []):
        primes.append(n)
    return (primes, etapes)


def factoriseTex(n):
    r"""**factoriseTex**\ (*n*)

    Retourne la liste des facteurs premiers du nombre n, ainsi que le détail de
    la factorisation au format TeX.

    :param n: Nombre à décomposer
    :type n: integer

    >>> from pyromaths.outils import Arithmetique
    >>> Arithmetique.factoriseTex(2673)
    ([3, 3, 3, 3, 3, 11], ['\\begin{align*}', '2673', ' & = 3 \\times 891\\\\', ' & = 3 \\times 3 \\times 297\\\\', ' & = 3 \\times 3 \\times 3 \\times 99\\\\', ' & = 3 \\times 3 \\times 3 \\times 3 \\times 33\\\\', ' & = 3 \\times 3 \\times 3 \\times 3 \\times 3 \\times 11\\\\', '\\end{align*}'])

    :rtype: tuple
    """
    """Version LaTeX pour factorise."""

    corrige = ["\\begin{align*}", str(n)]
    etapes = factorise(n)[1]
    primes = factorise(n)[0]

    if len(primes) > 1:
        for i in range(len(etapes)):
            text = ' & = '
            for j in range(len(etapes[i])):
                if j != len(etapes[i]) - 1:
                    text += etapes[i][j] + ' \\times '
                else:
                    text += etapes[i][j]
            corrige.append(text + '\\\\')
        corrige.append("\\end{align*}")
    else:
        corrige = [str(n) + _(" est un nombre premier.\\par ")]

    return (primes, corrige)


def carrerise(n):
    """**carrerise**\ (*n*)

    Retourne le plus petit facteur par lequel multiplier pour obtenir un carré.

    :param n: Nombre à rendre carré
    :type n: integer

    >>> from pyromaths.outils import Arithmetique
    >>> Arithmetique.carrerise(75)
    3

    :rtype: integer
    """
    if round(math.sqrt(n), 0) == math.sqrt(n):
        return 1
    elif n <= 0:
        return n
    else:
        primes = factorise(n)[0]
        q = {}
        for element in primes:
            if (primes.count(element) % 2 == 1):
                q[element] = 1
        ncar = 1
        for element in list(q.keys()):
            ncar *= element
    return ncar

def combinaison(n, k):
    """**combinaison**\ (*n*\ , *k*)

    Retourne k parmi n

    :param n: Nombre d'éléments
    :type n: integer
    :param k: éléments pris k à k
    :type k: integer

    >>> from pyromaths.outils import Arithmetique
    >>> Arithmetique.combinaison(6,3)
    20

    :rtype: integer
    """
    if k > n // 2:
        k = n - k
    x = 1
    y = 1
    i = n - k + 1
    while i <= n:
        x = (x * i) // y
        y += 1
        i += 1
    return x

def signe(a):
    """**signe**\ (*a*)

    Retourne `1` si `a` est positif, `-1` sinon.

    :param a: Nombre à tester
    :type a: float

    >>> from pyromaths.outils import Arithmetique
    >>> Arithmetique.signe(234)
    1
    >>> Arithmetique.signe(-234)
    -1

    :rtype: integer
    """
    if a < 0:
        return -1
    else:
        return 1

def valeur_alea(a, b):
    """**valeur_alea**\ (*a*\ , *b*)

    Retourne une valeur comprise entre `a` et `b` non nulle.

    :param a,b: bornes de l'ensemble de définition
    :type a,b: integer

    >>> from pyromaths.outils import Arithmetique
    >>> Arithmetique.valeur_alea(-7,7)  # doctest: +SKIP
    2

    :rtype: integer
    """
    while True:
        alea = random.randrange(a, b + 1)
        if alea != 0:
            return alea

#---------------------------------------------------------------------
# A supprimer dès que quatriemes/developpements.py aura été corrigé
#---------------------------------------------------------------------

def ecrit_tex(fichier, formule, cadre=None, thenocalcul='\\thenocalcul = ',
              tabs=1):
    """**ecrit_tex**\ (*n*)

    **TODO :** À supprimer dès que quatriemes/developpements.py aura été corrigé

    Écrit `formule` dans `fichier`.

    :param fichier: Fichier dans lequel écrire
    :type fichier: I/O
    :param formule: formule à insérer
    :type formule: string
    :param cadre: faut-il entourer la formule ?
    :type cadre: boolean
    :param thenocalcul: Numérotation automatique par LaTeX de l'équation
    :type thenocalcul: string
    :param tabs: combien de tabulation insérer pour l'indentation du fichier ?
    :type tabs: integer

    :rtype: fichier
    """

    if formule != '':
        if cadre == None or not cadre:
            fichier.write((u'  \\[ %s%s \\] \n') % (thenocalcul, formule))
        else:
            fichier.write((u'  \\[ \\boxed{%s%s} \\] \n') % (thenocalcul, formule))
