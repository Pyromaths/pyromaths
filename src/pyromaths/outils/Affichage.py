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

# import re
from pyromaths.classes import Racine
from pyromaths.classes.Fractions import Fraction

from .decimaux import decimaux


def tex_coef(coef, var='', bplus=0, bpn=0, bpc=0):
    r"""**tex_coef**\ (*coef*\ [, *var*\ [, *bplus*\ [, *bpn*\ [, *bpc*\ ]]]])

    Gère l'affichage d'un monôme (par défaut de degré 0) au format TeX. Permet

    * d'écrire `3x` au format TeX
    * d'ajouter un `+` devant `3x` pour écrire la somme `2+3x` avec `bplus`
    * de mettre des parenthèses autour de `-3x` pour écrire le produit `(x+1)(-3x)` avec `bpn` alors qu'il n'en faut pas avec `(x+1)3x`
    * de mettre des parenthèses autour de 3x pour écrire la puissance `(3x)^2` avec `bpc` alors qu'il n'en faut pas pour `x^2`

    :param coef: est le coefficient à écrire devant la variable var
    :type coef: integer
    :param bplus: si vrai, il faut écrire le signe + devant le coefficient
    :type bplus: boolean
    :param bpn: si vrai, il faut mettre des parenthèses autour de l'écriture si *coef* est négatif.
    :type bpn: boolean
    :param bpc: si vrai, il faut mettre des parenthèses autour de l'écriture si `coef != 0 ou 1` et `var != ''`
    :type bpc: boolean

    >>> from pyromaths.outils import Affichage
    >>> Affichage.tex_coef(5,'x')
    5\,x
    >>> Affichage.tex_coef(5,'x',1)
    +5\,x
    >>> Affichage.tex_coef(-5,'x',0,1)
    \left( -5\,x\right)
    >>> Affichage.tex_coef(1,'x',0,1,1)
    x
    >>> Affichage.tex_coef(5,'x',0,1,1)
    \left( 5\,x\right)

    :rtype: string
    """
    if coef != 0 and abs(coef) != 1:
        if var == '':
                a = TeX(coef)
        else:
                a = '%s\\,%s' % (TeX(coef), var)
        if bplus and coef > 0:
            a = '+' + a
    elif coef == 1:
        if var == '':
            a = '1'
        else:
            a = '%s' % var
        if bplus:
            a = '+' + a
    elif coef == 0:
        a = ''
    elif coef == -1:
        if var == '':
            a = '-1'
        else:
            a = '-%s' % var
    if bpn and coef < 0 or bpc and coef != 0 and coef != 1 and var != '':
        a = '\\left( ' + a + '\\right)'
    return a

def TeXz(nombre):
    """n'affiche pas b si b=0

    Double emploi avec tex_coef(nombre)"""
    if nombre == 0:
        return ""
    else:
        return TeX(nombre)
def tTeX(nombre):
    '''raccourci pour TeX(nombre,terme=True)'''
    return TeX(nombre, terme=True)
def pTeX(nombre):
    '''raccourci pour TeX(nombre,parenthese=True)'''
    return TeX(nombre, parenthese=True)
def fTeX(nombre):
    '''raccourci pour TeX(nombre,fractex="\\frac")'''
    return TeX(nombre, fractex="\\frac")

def TeX(nombre, parenthese=False, terme=False, fractex="\\dfrac"):
    r"""**TeX**\ (*nombre*\ [, *parenthese*\ [, *terme*\ [, *fractex*\ ]]])

    Permet l'affichage de nombres au format TeX. Fait en partie double emploi avec tex_coef. Permet

    * d'écrire un nombre (décimal, rationnel ou radical) au format TeX
    * d'écrire l'infini au format TeX
    * d'ajouter un `+` devant `3` pour écrire `+3` avec `terme`
    * de mettre des parenthèses autour de `3` avec `parenthese`
    * de changer la commande d'écriture des fractions en TeX avec fractex

    :param nombre: est le nombre à écrire
    :type nombre: integer, Fractions, RacineDegre2
    :param parenthese: si vrai, il faut écrire des parenthèses autour de `nombre`
    :type parenthese: boolean
    :param terme: Ajoute un `+` devant nombre s'il est positif.
    :type terme: boolean
    :param fractex: commande à utiliser pour créer une fraction sous TeX
    :type fractex: string

    >>> from pyromaths.outils import Affichage
    >>> from pyromaths.classes.Fractions import Fraction
    >>> Affichage.TeX(Fraction(7,3)).strip()
    \dfrac{7}{3}
    >>> Affichage.TeX(Fraction(7,3),fractex='\\frac').strip()
    \frac{7}{3}

    :rtype: string
    """
    strTeX = finTeX = ""

    # Affichage simplifié des racines ou fractions
    if isinstance(nombre, Racine.RacineDegre2) and nombre.radicande == 0:
        # Affiche la RacineDegre2 comme une Fractions
        nombre = Fraction(nombre.numerateur, nombre.denominateur)
    if isinstance(nombre, Fraction) and nombre.d == 1:
        # Affiche la Fractions comme un entier
        nombre = nombre.n
    # parentheses des fractions
    if parenthese and (
        isinstance(nombre, Racine.RacineDegre2)
                       and nombre.denominateur == 1 and (nombre.numerateur or nombre.coeff < 0)
        # RacineDegre2 avec radicande nécessairement grâce au tri
        or isinstance(nombre, Fraction) and nombre.n < 0
        or isinstance(nombre, int) and nombre < 0
        or isinstance(nombre, float) and nombre < 0):
        strTeX = "\\left("
        finTeX = "\\right)"
    elif terme and (isinstance(nombre, Racine.RacineDegre2) and
                        (nombre.d != 1 or (nombre.n > 0 or nombre.n == 0 and nombre.coeff >= 0))
                    or nombre >= 0) :
        strTeX = "+"
        finTeX = ""

    # #Affichage
    if isinstance(nombre, (int, float)) and nombre == float("inf"):
        return "+\\infty "
    elif isinstance(nombre, (int, float)) and nombre == float("-inf"):
        return "-\\infty "
    elif isinstance(nombre, int) or isinstance(nombre, float):
        return strTeX + decimaux(nombre) + finTeX
    elif isinstance(nombre, Fraction):
        if nombre.n < 0:
            strTeX += "-" + fractex + "{" + decimaux(-nombre.n) + "}{" + decimaux(nombre.d) + "} "
        else:
            strTeX += fractex + "{" + decimaux(nombre.n) + "}{" + decimaux(nombre.d) + "} "
        strTeX += finTeX
        return strTeX
    elif isinstance(nombre, Racine.RacineDegre2):
        return strTeX + str(nombre) + finTeX
    else:
        return strTeX + str(nombre) + finTeX

def radicalTeX(n):
    return "\\sqrt{%s}" % (decimaux(n))
