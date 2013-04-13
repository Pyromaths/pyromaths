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

import math, random

def pgcd(a, b):
    """Calcule le pgcd entre a et b."""
    while b:
        a, b = b, a%b
    return a

def ppcm(a, b):
    """Calcule le ppcm entre a et b."""
    return a*b/pgcd(a, b)

def premier(n):
    """Teste si un nombre est premier."""
    return not [x for x in xrange(2,int(math.sqrt(n)) + 1)
                if n%x == 0]

def eratosthene(n):
    """Etablit la liste des nombres premiers inferieurs a n."""
    return [x for x in xrange(2, n) if premier(x)]


def factor(n):
    """Retourne la liste des facteurs premiers du nombre n."""
    premiers = []
    candidats = xrange(2,n+1)
    candidat = 2
    while not premiers and candidat in candidats:
        if n%candidat == 0 and premier(candidat):
            premiers.append(candidat)
            premiers = premiers + factor(n/candidat)
        candidat += 1
    return premiers


def factorise(n):
    """Retourne la liste des facteurs premiers du nombre n, ainsi que le détail
    de la factorisation."""

    primes = []
    temp = n
    etapes = []
    primes_etapes = []
    limite=int(math.sqrt(n))+1
    candidate = 2
    while (candidate < limite):
        if n % candidate == 0:
            primes.append(candidate)
            primes_etapes.append(str(candidate))
            n = n / candidate
            if n  == 1:
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
      corrige = [str(n) + " est un nombre premier.\\par "]

    return (primes, corrige)


def carrerise(n):
    """Trouve le plus petit facteur par lequel multiplier pour obtenir un carré."""
    if round(math.sqrt(n), 0)==math.sqrt(n):
        return 1
    elif n<=0:
        return n
    else:
        primes = factorise(n)[0]
        q = {}
        for element in primes:
            if (primes.count(element) % 2 == 1):
                q[element]=1
        ncar=1
        for element in q.iterkeys():
            ncar *= element
    return ncar

def combinaison(n, k):
    """renvoie le nombre de combinaisons de n objets pris k à k"""
    if k > n//2:
        k = n-k
    x = 1
    y = 1
    i = n-k+1
    while i <= n:
        x = (x*i)//y
        y += 1
        i += 1
    return x

def signe(a):
    """renvoie 1 si a est>0, -1 si a<0"""
    if a < 0:
        return -1
    else:
        return 1
    
def valeur_alea(a, b):
    """choisit une valeur comprise entre a et b non nulle"""
    while True:
        alea = random.randrange(a, b + 1)
        if alea != 0:
            return alea

#---------------------------------------------------------------------
# A supprimer dès que quatriemes/developpements.py aura été corrigé
#---------------------------------------------------------------------

def ecrit_tex(file, formule, cadre=None, thenocalcul='\\thenocalcul = ',
              tabs=1):
    """Écrit la ligne dans le fichier"""
    if formule != '':
        if cadre == None or not cadre:
            file.write((u'  \\[ %s%s \\] \n') % (thenocalcul, formule))
        else:
            file.write((u'  \\[ \\boxed{%s%s} \\] \n') % (thenocalcul, formule))
