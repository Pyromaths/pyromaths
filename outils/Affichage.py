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

import re

def printlist(liste):
    """Affiche chaque élément d'une liste, ligne par ligne."""
    for element in liste:
        print(element)
    return False

def suppr0(nombre):
    """Supprime le zéro inutile après la virgule d'un float, si c'est possible."""
    if round(nombre, 0) == nombre:
        return int(nombre)
    else:
        return nombre

def suppr0list(liste):
    """Supprime le zéro inutile après la virgule des éléments d'une liste de floats, si c'est possible."""
    for element in liste:
        element = suppr0(element)
    return liste

def decomp3(nombre):
    """Affiche un nombre entier avec les chiffres par 3."""
    i = 0 ## 1
    result = ''
    nombrestr = repr(nombre)
    longueur = len(nombrestr)
    reste = longueur % 3

    while (i < longueur):
        if i == reste:
            caract = ' '
            reste += 3
        else:
            caract = nombrestr[i]
            i += 1
        result += caract

    return result

def ecrire_par3(nombre):
    """Affiche un nombre quelconque avec les chiffres par 3."""
    intvir = re.findall( '(\d+)\.*(\d*)', repr(nombre))

    if (re.findall('\.', repr(nombre)) and ((intvir[0][1]) != '0')):
      secondterm = decomp3(intvir[0][1])
      separateur = ', '
    else:
      secondterm = ''
      separateur = ' '

    return decomp3(intvir[0][0]) + separateur + secondterm

#---------------------------------------------------------------------
# Affichages des nombres décimaux
#---------------------------------------------------------------------
def decimaux(nb, mathenv = 0):
    pattern = re.compile(r"^(-?\d+)\.*(\d*)e?([\+\-]?\d*)$")
    entiere,  decimale,  exposant = pattern.search(str(nb)).groups()
    if exposant:
        if int(exposant) > 0:
            if int(exposant) < len(decimale):
                entiere = entiere + decimale[:int(exposant)]
                decimale = decimale[int(exposant):]
            else:
                entiere = entiere + decimale + "0"*(int(exposant)-len(decimale))
                decimale = ''
        else:
            if -int(exposant) < len(entiere):
                decimale = entiere[len(entiere)+int(exposant):] + decimale
                entiere = entiere[:len(entiere)+int(exposant)]
            else:
                decimale = "0"*(-int(exposant)-len(entiere)) + entiere + decimale
                entiere = "0"
    pattern = re.compile(r"^(-?\d{1,3}?)" + "(\d{3})" * ((len(entiere) - 1) // 3) \
                         + "$")
    partie_entiere = pattern.search(entiere).groups()
    if decimale and int(decimale):
        """Vérifie si la partie décimale existe et si elle est différente de
        zéro"""
        pattern = re.compile(r"^" + "(\d{3})" * ((len(decimale) - 1)  // 3) + \
                             "(\d{1,3})?$")
        partie_decimale = pattern.search(decimale).groups()
        if mathenv:
            return "{,}".join(("\,".join(partie_entiere),
                               "\,".join(partie_decimale)))
        else:
            return ",".join(("\,".join(partie_entiere),
                             "\,".join(partie_decimale)))
    else:
        return "\,".join(partie_entiere)
def tex_coef(coef, var, bplus=0, bpn=0, bpc=0):
    """
    coef est le coefficient à écrire devant la variable var
    bplus est un booleen : s'il est vrai, il faut ecrire le signe +
    bpn est un booleen : s'il est vrai, il faut mettre des parentheses autour de
        l'écriture si coef est negatif.
    bpc est un booleen : s'il est vrai, il faut mettre des parentheses autour de
        l'écriture si coef =! 0 ou 1 et var est non vide
    """
    if coef != 0 and abs(coef) != 1:
        if var == '':
            if abs(coef) >= 1000:
                a = '\\nombre{%s}' % coef
            else:
                a = '%s' % coef
        else:
            if abs(coef) >= 1000:
                a = '\\nombre{%s}\\,%s' % (coef, var)
            else:
                a = '%s\\,%s' % (coef, var)
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
