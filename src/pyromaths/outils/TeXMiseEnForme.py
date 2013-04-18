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

from . import Arithmetique
import string
import math
import os
from .Conversions import radians, degres
from ..classes.Fractions import Fractions


class TeXMiseEnForme:

    def __init__(self, text):
        self.text = text

    def monome(self, coef, var, bplus=0, bpn=0, bpc=0):

        # coef est le coefficient à écrire devant la variable var
        # bplus est un booleen : s'il est vrai, il faut ecrire le signe +
        # bpn est un booleen : s'il est vrai, il faut mettre des parentheses autour de l'ecriture si coef est negatif.
        # bpc est un booleen : s'il est vrai, il faut mettre des parentheses autour de l'ecriture si coef =! 0 ou 1 et var est non vide

        if coef != 0 and abs(coef) != 1:
            if var == "":
                if abs(coef) >= 1000:
                    a = '\\nombre{%s}' % coef
                else:
                    a = "%s" % coef
            else:
                if abs(coef) >= 1000:
                    a = '\\nombre{%s}\\,%s' % (coef, var)
                else:
                    a = '%s\\,%s' % (coef, var)
            if bplus and coef > 0:
                a = '+' + a
        elif coef == 1:
            if var == "":
                a = '1'
            else:
                a = "%s" % var
            if bplus:
                a = '+' + a
        elif coef == 0:
            a = ""
        elif coef == -1:
            if var == "":
                a = '-1'
            else:
                a = '-%s' % var
        if bpn and coef < 0 or bpc and coef != 0 and coef != 1 and var != \
            "":
            a = '\\left( ' + a + '\\right)'
        return a

    def sepmilliers(self, nb, mathenvironment=0):

        # Insère les espaces fines pour séparer les milliers et remplace le point
        # décimal par une virgule

        dec = [str(nb)[i] for i in range(len(str(nb)))]
        if dec.count('e'):  #nb ecrit en notation scientifique
            exposant = int(("").join(dec[dec.index('e') + 1:]))
            dec = dec[:dec.index('e')]
            lg = len(dec)
            if dec.count('.'):
                virg = dec.index('.')
                dec.remove('.')
            else:
                virg = len(dec)
            if virg + exposant < 0:  #L'ecriture decimale du nombre commence par 0,...
                dec2 = ["0", '.']
                for i in range(-virg - exposant):
                    dec2.append("0")
                dec2.extend(dec)
                dec = dec2
            elif virg + exposant > lg:

                #L'ecriture decimale du nombre finit par des 0

                for i in range(-((lg - virg) - 1) + exposant):
                    dec.append("0")
        dec2 = []
        if dec.count('.'):
            lavtvirg = dec.index('.')
            laprvirg = (len(dec) - dec.index('.')) - 1
        else:
            lavtvirg = len(dec)
            laprvirg = 0
        nbsep = lavtvirg // 3 + 1
        if lavtvirg > 3:
            cpt = lavtvirg % 3
            if cpt:
                dec2 = dec[0:cpt]
                dec2.append('\\,')
                nbsep = nbsep - 1
            for i in range(nbsep):
                dec2.extend(dec[cpt:cpt + 3])
                if nbsep - i > 1:
                    dec2.append('\\,')
                cpt = cpt + 3
        else:
            if dec.count('.'):
                dec2 = dec[0:dec.index('.')]
            else:
                dec2 = dec
        if dec.count('.'):
            cpt = dec.index('.')
        else:
            cpt = len(dec)
        if laprvirg <= 3:
            dec2.extend(dec[cpt:])
        else:
            nbsep = laprvirg // 3 - 1
            dec2.extend(dec[cpt:cpt + 4])
            dec2.append('\\,')
            cpt = cpt + 4
            for i in range(nbsep):
                dec2.extend(dec[cpt:cpt + 3])
                if cpt + 3 < len(dec):
                    dec2.append('\\,')
                cpt = cpt + 3
            dec2.extend(dec[cpt:])
        nb = ("").join(dec2)
        if nb.endswith('.0'):
            nb = string.rsplit(nb, '.0')[0]
        if mathenvironment:
            return string.join(string.rsplit(nb, sep='.'), '{,}')
        else:
            return string.join(string.rsplit(nb, sep='.'), ',')

sepmilliers=TeXMiseEnForme("").sepmilliers

def Affichage(l):
    """\xc3\x89crit une expressions contenant des d\xc3\xa9cimaux et des fractions au format TeX

    @param l: liste contenant l'expression [3, '+', 5, '*', 2]
    """

    expr = ""  # résultat
    for i in range(len(l)):  # on parcourt la liste
        if ["+", "-", "*", "/", '(', ')'].count(l[i]):  # Un opérateur
            if l[i] == "*":
                expr = expr + " \\times "
            elif l[i] == "/":
                expr = expr + " \\div "
            elif l[i] == ")" and type(l[i-1]) == type(Fractions(1, 1)):
                expr = expr + " \\big) "
            elif i<len(l)-2 and l[i] == "(":
                if type(l[i+1]) == type(Fractions(1, 1)):
                    expr = expr + " \\big( "
            else:
                expr = expr + " " + l[i] + " "
        elif type(l[i]) == type(Fractions(1, 1)):
            # C'est une fraction
            expr = expr + "%s" % Fractions.TeX(l[i], signe = 0)
        else:
            # C'est un nombre
            expr = expr + "%s" % Affichage.decimaux(l[i], 1)
    return expr
