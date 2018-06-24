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
from builtins import object
from past.utils import old_div
if __name__ == "__main__":
    import sys, os
    sys.path.append(os.path.join('..'))

# from .Racine import simplifie_racine, RacineDegre2, sqrt
from .Racine import RacineDegre2
from .Fractions import Fraction
from pyromaths.outils import Priorites3
import re
# from pyromaths.outils.Affichage import pTeX, TeX, radicalTeX, fTeX, Fractions, tTeX
from pyromaths.outils.Affichage import TeX, tTeX

class Polynome(object):
    '''Classe de polynôme pour le lycee'''
    def __init__(self, liste_coeff, var="x"):
        self.var = var  # Lettre pour la var
        liste_reduite = {}
        if isinstance(liste_coeff, str):
            liste_coeff = _str_Polynome(liste_coeff, var)
        elif isinstance(liste_coeff, list):
            liste_coeff = dict((i, liste_coeff[i])for i in range(len(liste_coeff)))
        elif isinstance(liste_coeff, int) or isinstance(liste_coeff, Fraction) or isinstance(liste_coeff, float):
            liste_coeff = {0:liste_coeff}
        for i in list(liste_coeff.keys()):
            if liste_coeff[i] != 0:
                if isinstance(liste_coeff[i], (RacineDegre2, Fraction)):
                    #===========================================================
                    # print liste_coeff[i]
                    #===========================================================
                    liste_reduite[i] = liste_coeff[i].simplifie()
                else:
                    liste_reduite[i] = Fraction(liste_coeff[i], 1)
        if liste_reduite == {} or liste_coeff == []:
            liste_reduite = {0:0}
        self.dictio = liste_reduite
        self.puiss = list(liste_reduite.keys())
        self.puiss.sort(reverse=True)
        self.deg = self.degre()
        self.degre_max = max(0, self.deg)

    def __len__(self):
        return max(0, self.deg) + 1

    def degre(self):
        degre = float("-inf")
        for i in list(self.dictio.keys()):
            if i > degre and self.dictio[i] != 0:
                degre = i
        return degre

    def __getitem__(self, i):
        '''P[i] renvoie le coefficient de rang i'''
        return self.dictio.get(i, 0)

    def __str__(self):
        '''renvoie une str pour un affichage python'''
        return self.TeX(var=self.var)

    def __repr__(self):
        return '{classe}({coef}, var="{var}")'.format(
                classe=self.__class__.__name__,
                coef=repr(self.dictio),
                var=self.var,
                )

    def TeX(self, var='', display=True, parenthese=False):
        '''renvoie une chaine de caractere imprimant les fractions dans TeX'''
        if var == '':
            var = self.var
        exposants = [] + self.puiss
        premier = 1
        string = ''
        #=======================================================================
        # if display:
        #     fractex="\\dfrac"
        # else:
        #     fractex="\\frac"
        #=======================================================================
        for exposant in exposants :
            if premier:
                if self[exposant] == 1 and exposant != 0:
                    string = ''
                elif self[exposant] == -1 and exposant != 0:
                    string = '-'
                else:
                    string = TeX(self[exposant])
                premier = 0
            elif self[exposant] != 1:
                if self.dictio[exposant] == -1:
                    string += '-'
                else:
                    string += tTeX(self[exposant])
            else:
                string += "+"
            if exposant == 1:
                terme = var
            elif (exposant == 0) and ((self[exposant] == 1) or (self[exposant] == -1)):
                terme = '1'
            elif exposant == 0:
                terme = ''
            else:
                terme = var + u'^' + str(exposant)
            string += terme
        if parenthese and (len(self.puiss) > 1 or self[self.degre_max] < 0):
            return "\\left(" + string + "\\right)"
        else:
            return string

    def __add__(self, other):
        if isinstance(other, int) or isinstance(other, float) or  isinstance(other, Fraction) or isinstance(other, RacineDegre2):
            return self +Polynome({0:other}, var=self.var)
        result = {0:0}
        liste1 = self.puiss
        liste2 = other.puiss
        for i in liste1 :
            s = self.dictio.get(i) + other.dictio.get(i, 0)
            if s != 0:
                result[i] = s
        for i in liste2:
            if i not in liste1:
                result[i] = other.dictio[i]
        return Polynome(result, var=self.var)

    def __mul__(self, other):
        if isinstance(other, Polynome):
            result = Polynome({0:0}, var=self.var)
            for i in list(self.dictio.keys()):
                for j in list(other.dictio.keys()):
                    exposant = i + j
                    coefficient = self.dictio[i] * other.dictio[j]
                    result = result + Polynome({exposant:coefficient}, var=self.var)
            return result
        else:
            return self * Polynome(other)
    def __ne__(self, other):
        return not(self == other)
    def __eq__(self, other):
        if (isinstance(other, int) or isinstance(other, Fraction) or isinstance(other, float)):
            if self.degre_max == 0 and self[0] == other:
                return True
            else:
                return False
        elif self.var == other.var and self.dictio == other.dictio:
            return True
        else:
            return False

    def __pow__(self, other):
        if isinstance(other, int) and other >= 0:
            result = Polynome({0:1}, self.var)
            for dummy in range(other):
                result *= self
            return result

    def __radd__(self, other):
        if isinstance(other, int) or isinstance(other, float) or isinstance(other, Fraction):
            return self +Polynome({0:other}, var=self.var)
        return self +other

    def __sub__(self, other):
        return self +(-other)

    def __rsub__(self, other):
        return -(self -other)

    def __neg__(self):
        return self * Polynome({0:-1}, var=self.var)

    def __rmul__(self, nombre):
        return self * Polynome({0:nombre})

    def __truediv__(self, other):
        if isinstance(other, int):
            return Fraction(1, other) * self
        elif isinstance(other, Fraction) or isinstance(other, float)or isinstance(other, RacineDegre2):
            return (old_div(1, other)) * self
        else:
            quotient = Polynome({}, var=self.var)
            reste = self
            diviseur_degre = other.deg
            while diviseur_degre <= reste.deg:
                ajout_quotient_deg = reste.deg - diviseur_degre
                facteur = old_div(reste.dictio[reste.deg], other.dictio[other.deg])
                ajout_quotient = Polynome({ajout_quotient_deg:facteur}, var=self.var)
                quotient = quotient + ajout_quotient
                soustrait_reste = ajout_quotient * other
                reste = reste - soustrait_reste
            return quotient, reste
    def simplifie(self):
        result = {}
        for i in self.puiss:
            if isinstance(self[i], (Fraction, RacineDegre2)):
                result[i] = self[i].simplifie()
            else:
                result[i] = self[i]
        return Polynome(result)

    def __call__(self, x,):
        '''renvoie la Fraction ou l'int P(x)'''
        if x == float("inf") or x == float("-inf"):
            if self.degre_max == 0:
                return self[0]
            elif self.deg % 2 == 0:
                return self[self.deg] * float("inf")
            else:
                return self[self.deg] * x
        elif isinstance(x, str):
            return self.TeX(var=x)
        else:
            result = 0
            for i in list(self.dictio.keys()):
                result = result + self[i] * x ** i
            if isinstance(result, str):
                result = eval(Priorites3.priorites(result)[-1][0])
            if isinstance(result, (int, float)):
                return result
            elif isinstance(result, Fraction):
                result = result.simplifie()
                if isinstance(result, int):
                    return result
                if result.d == 1:
                    return result.n
                else:
                    return result
            elif result.denominateur == 1:
                return result.numerateur
            else:
                return result

    def racine_evidente(self, liste=[-2, -1, 0, 1, 2]):
        listerac = []
        for i in liste:
            if self(i) == 0:
                listerac = listerac + [i]
        return listerac

    def factorise(self, TeX=False, racines=[0, -1, 1, 2, -2]):
        facteurs = [Polynome({0:self.dictio[self.deg]}, var=self.var)]
        developpe, reste = old_div(self, facteurs[0])
        for r in racines:
            while developpe(r) == 0:
                rac = -r
                developpe, reste = old_div(developpe, Polynome({1:1, 0:rac}, var=self.var))
                facteurs = facteurs + [Polynome({1:1, 0:rac})]
        if TeX:
            stringTeX = ""
            if not(facteurs[0] == Polynome({0:1}, var=self.var)):
                stringTeX += facteurs[0].TeX()
            for i in facteurs[1:]:
                if i[0] != 0:
                    stringTeX += "\\left(" + i.TeX() + "\\right) \\times "
                else:
                    stringTeX += i.TeX() + " \\times "
            if developpe == Polynome({0:1}, var=self.var):
                return stringTeX[:-7]
            else:
                return stringTeX + "\\left(" + developpe.TeX() + "\\right)"
        else:
            return facteurs + [developpe]

    def derive(self):
        result = {}
        for i in list(self.dictio.keys()):
            if i == 0:
                result[0] = 0
            else:
                result[i - 1] = int(i) * self[i]
        return Polynome(result, self.var)
    def primitive(self):
        result = {}
        for i in list(self.dictio.keys()):
            result[i + 1] = Fraction(1, int(i + 1)) * self.dictio[i]
        return Polynome(result, self.var)

def _str_Polynome(string, var='x'):
    '''str -> dict'''
    # TODO reconnaitre les coefficients fractionnaires
    resultat = []
    termes = {}
    separeplus = (string).split("+")
    for element in separeplus:
        temp = []
        temp = element.split("-")
        for bis in temp:
            resultat.append(bis)
            if temp.index(bis) != len(temp) - 1:
                resultat.append(-1)
        if separeplus.index(element) != len(separeplus) - 1:
            resultat.append(1)
    if '' in resultat:
        resultat.remove('')
    for element in resultat:
        index = resultat.index(element)
        if index > 0:
            coeff = resultat[index - 1]
        else:
            coeff = 1
        if (element not in [-1, 1]):
            if element == var:
                termes[1] = (coeff)
            else:
                a = re.findall('\d+(?:\.\d*)?', element)
                if (len(a) == 1) and (not re.findall('\^', element)) and (re.findall(var, element)):
                    termes[1] = coeff * Fraction(eval(a[0]))
                elif (len(a) == 1) and (re.findall(var, element)):
                    termes[int(a[0])] = coeff * 1
                elif (len(a) == 1):
                    termes[0] = coeff * Fraction(eval(a[0]))
                else:
                    termes[int(a[1])] = coeff * Fraction(eval(a[0]))
    return termes

if __name__ == "__main__":
    from TEST.imprimetest import *
    X = Polynome("x")
    P = Polynome({2:4, 1:8, 0:1, 3:0})
# #    Q=Polynome({2:-4,0:-1,1:8})
# #    R=Polynome({3:1,2:1,1:-2})
# #    D=Polynome({1:1,0:2})
# #    F=Polynome("x-4")
# #    FF=Polynome("x^2-3")
# #    Divi=FF*F+7
# #    FR=Polynome({3:Fraction(2,3),2:Fraction(2,3),1:Fraction(-4,3)})
# #    print "P=", P
# #    print "Q=", Q
# #    print "R=", R
# #    print "FR=",FR
# #    R_facteur=R.factorise()
# #    print "R=",R.factorise(TeX=True)
# #    #TeX_division(R,D)
# #    print Divi*Polynome("x^3")-28*X
# #    #imprime_TeX(TeX_division(Divi*Polynome("x^3")-28*X,F*X))
