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
import classes

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
    pattern = re.compile(r"^(-?\d{1,3}?)" + "(\d{3})" * \
                         ((len(entiere) - 1 - (entiere[0]=='-')) // 3) + "$")
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


def TeXz(nombre):
    '''n'affiche pas b si b=0'''
    if nombre==0:
        return ""
    else:
        return TeX(nombre)
def tTeX(nombre):
    '''raccourci pour TeX(nombre,terme=True)'''
    return TeX(nombre,terme=True)
def pTeX(nombre):
    '''raccourci pour TeX(nombre,parenthese=True)'''
    return TeX(nombre,parenthese=True)
def fTeX(nombre):
    '''raccourci pour TeX(nombre,fractex="\\frac")'''
    return TeX(nombre,fractex="\\frac")
    
def TeX(nombre,parenthese=False,terme=False,fractex="\\dfrac"):
    '''renvoie une chaine de caractere pour TeX'''
    strTeX=finTeX=""
    
    #Affichage simplifié des racines ou fractions
    if isinstance(nombre,classes.Racine.RacineDegre2) and nombre.radicande==0:
        #Affiche la RacineDegre2 comme une Fractions
        nombre=classes.Fractions.Fractions(nombre.numerateur,nombre.denominateur)
    if isinstance(nombre,classes.Fractions.Fractions) and nombre.denominateur==1:
        #Affiche la Fractions comme un entier
        nombre=nombre.numerateur
    #parentheses des fractions
    if parenthese and (
        isinstance(nombre,classes.Racine.RacineDegre2)
                       and nombre.denominateur==1 and (nombre.numerateur or nombre.coeff<0 )
        #RacineDegre2 avec radicande nécessairement grâce au tri
        or isinstance(nombre,classes.Fractions.Fractions) and nombre.numerateur<0
        or isinstance(nombre,int) and nombre<0
        or isinstance(nombre,float) and nombre<0):
        strTeX="\\left("
        finTeX="\\right)" 
    elif terme and (isinstance(nombre,classes.Racine.RacineDegre2) and
                        (nombre.denominateur!=1 or (nombre.numerateur >0 or nombre.numerateur==0 and nombre.coeff>=0))
                    or nombre>=0) :
        strTeX="+"
        finTeX=""

    ##Affichage
    if nombre==float("inf"):
        return "+\\infty "
    elif nombre==float("-inf"):
        return "-\\infty "
    elif isinstance(nombre,int) or isinstance(nombre,float):
        return strTeX+decimaux(nombre)+finTeX
    elif isinstance(nombre,classes.Fractions.Fractions):
        if nombre.numerateur < 0:
            strTeX += "-"+fractex+"{"+decimaux(-nombre.numerateur)+"}{"+decimaux(nombre.denominateur)+"} "
        else:
            strTeX += fractex+"{"+decimaux(nombre.numerateur)+"}{"+decimaux(nombre.denominateur)+"} "
        strTeX+=finTeX
        return strTeX
    elif isinstance(nombre,classes.Racine.RacineDegre2):
        return strTeX+str(nombre)+finTeX
    else:
        return strTeX+str(nombre)+finTeX
def radicalTeX(n):
    return "\\sqrt{%s}"%(TeX(n))
