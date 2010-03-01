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

from outils.Affichage import decimaux


_POLYNOME_FORMAT = re.compile(r"""
    \s*                                         # éventuellement des espaces pour commencer
    (                                           # chaque monome
        [-+]?\d+(?:\.\d*)?[a-zA-Z]?(?:\^\d+)?   # au moins un nombre décimal
        |                                       # OU
        [-+]?\d*(?:\.\d*)?[a-zA-Z](?:\^\d+)?    # au moins une variable

    )
    \s*                                         # éventuellement des espaces pour finir
""", re.VERBOSE)

_MONOME_FORMAT = re.compile(r"""
    \s*                                         # éventuellement des espaces pour commencer
    (?P<sign>[-+]?)                             # un éventuel signe
    (?P<coef>\d*(?:\.\d*)?)                     # un éventuel coefficent
    (?:(?P<var>[a-zA-Z])(?:\^(?P<deg>\d+))?)?   # une éventuelle variable avec son éventuel degré
    \s*                                         # éventuellement des espaces pour finir
""", re.VERBOSE)

class Polynome():
    """Cette classe crée la notion de polynomes.
    Polynome([[2,2],[3,1],[4,0]], 'z') est équivalent à 2z^2+3z+4.

    Un polynome peut aussi être produit à l'aide d'une chaine de la forme
    Polynome("2y^2+3y+4")
    """

    def __init__(self, monomes, var=None):
        """Crée un polynome.
        Accepte une chaine de caractères comme '2x^2-4x+6' ou une liste de
        monomes [coefficient, degré] finit par une string contenant la variable.
        Par exemple, Polynome([[5,2], [-4,1], [6,0]], 't') équivaut à
        Polynome("+5t^2-4t+6")
        """
        self.var = var # variable du polynome
        monomes = monomes or '0' # monomes du polynome, par défaut un polynome nul
        self.monomes = monomes
        if isinstance(monomes, basestring):
            # Gère la construction des polynome à partir d'une chaine de caractères
            listmonomes = []
            for monome in _POLYNOME_FORMAT.finditer(monomes):
                m = _MONOME_FORMAT.search(monome.group(0))
                if m is None:
                    raise ValueError('Chaine invalide pour un objet Polynome : %s' % input)
                m_sign = m.group('sign') or '+'
                m_coef = float(m.group('coef') or 1)
                m_deg = int(m.group('deg') or (m.group('var') and '1') or '0')
                m_var = m.group('var') or var
                if m_var and not var: var = m_var # attribue une variable à var
                if m_var != var:
                    raise ValueError('Le nom de la variable (%s) est incorrect pour le Polynome %s' % (var, monomes))
                if m_sign == '-': m_coef = -m_coef
                if m_coef or m_deg==0:
                    # supprime les monomes de coefficient 0, sauf celui de degré 0
                    listmonomes.append([m_coef, m_deg])
            var = var or 'x' # Variable par défaut
            self.monomes = listmonomes
            self.var = var
        else:
            self.var = var or 'x' # Variable par défaut

    def __repr__(self):
        """repr(self)
        Renvoie une chaine de caractère pouvant être utilisée pour créer un polynome.
        S'appelle ainsi : repr(p) où p est un polynome"""
        var = self.var
        s = "Polynome(\""
        for m in self.monomes:
            if isinstance(m, list):
                if m[1] > 1:
                    # Monome de degré au moins 2
                    if m[0] == 1:
                        s = s + "+" + var + "^" + str(m[1])
                    elif m[0] == -1:
                        s = s + "-" + var + "^" + str(m[1])
                    elif m[0] > 0:
                        s = s + "+" + str(m[0]) + var + "^" + str(m[1])
                    else:
                        s = s + str(m[0]) + var + "^" + str(m[1])
                elif m[1] == 1:
                    # Monome de degré 1
                    if m[0] == 1:
                        s = s + "+" + var
                    elif m[0] == -1:
                        s = s + "-" + var
                    elif m[0] > 0:
                        s = s + "+" + str(m[0]) + var
                    else:
                        s = s + str(m[0]) + var
                else:
                    # Monome de degré 0
                    if m[0] < 0:
                        s = s + str(m[0])
                    else:
                        s = s + "+" + str(m[0])
        if s[0]=='+': s=s[1:]
        # supprime le + en début de séquence
        s += "\")"
        return s

    def __str__(self):
        """str(self)
        Renvoie une version LaTeX du polynome"""
        var = self.var
        s = ""
        for m in self.monomes:
            if isinstance(m, list):
                if m[1] > 1:
                    # Monome de degré au moins 2
                    if m[0] == 1:
                        s = s + "+" + var + "^{" + str(m[1]) + "}"
                    elif m[0] == -1:
                        s = s + "-" + var + "^{" + str(m[1]) + "}"
                    elif m[0] > 0:
                        s = s + "+" +decimaux(m[0], 1) + r"\," + var + "^{" + str(m[1]) + "}"
                    else:
                        s = s + decimaux(m[0], 1) + r"\," + var + "^{" + str(m[1]) + "}"
                elif m[1] == 1:
                    # Monome de degré 1
                    if m[0] == 1:
                        s = s + "+" + var
                    elif m[0] == -1:
                        s = s + "-" + var
                    elif m[0] > 0:
                        s = s + "+" + decimaux(m[0], 1) + r"\," + var
                    else:
                        s = s + decimaux(m[0], 1) + r"\," + var
                else:
                    # Monome de degré 0
                    if m[0] < 0:
                        s = s + decimaux(m[0], 1)
                    else:
                        s = s + "+" + decimaux(m[0], 1)
        if s[0]=='+': s=s[1:]
        # supprime le + en début de séquence
        return s

    def reduit(self):
        m = [m for m in Polynome.ordonne(self).monomes]
        lm = [m[0]]
        for i in range(1, len(m)):
            if lm[-1][1] == m[i][1]:
                # les deux monomes ont le même degré
                lm[-1][0] += m[i][0]
                if lm[-1][0] == 0: lm.pop(-1)
                # supprime un monome nul
            else:
                lm.append(m[i])
        return Polynome(lm, self.var)

    def reductible(self):
        """Renvoie 1 si le polynome est reductible, 0 sinon."""
        if self != Polynome.reduit(self):
            return 1
        else:
            return 0

    def ordonne(self):
        m = [m1 for m1 in self.monomes]
        if len(m)>1:
            m = sorted(m, key = lambda x: (-x[1]))
        return Polynome(m, self.var)

    def __ne__(self,  other):
        return 1-(self==other)

    def __eq__(self, other):
        if isinstance(other, Polynome):
            m1, m2 = [m for m in self.monomes], [m for m in other.monomes]
            if len(m1) != len(m2) or self.var != other.var:
                equal = 0
            else:
                equal = 1
                for i in range(len(m1)):
                    if m1[i] != m2[i]:
                        equal = 0
                        break
            return equal
        else:
            other = Polynome(other, self.var)
            return self==other

    def __add__(self, other):
        if not isinstance(other, Polynome):
            other=Polynome(repr(other), self.var)
        m1, m2 = [m for m in self.monomes], [m for m in other.monomes]
        if Polynome.degre(self) == 0:
            self.var = other.var
        elif Polynome.degre(other)==0:
            other.var = self.var
        if self.var != other.var:
            raise ValueError('Pyromaths ne sait additionner que deux polynomes de meme variable')
        else :
            m1.extend(m2)
            if Polynome.ordonne(Polynome(m1, self.var)) == Polynome(m1, self.var):
                return Polynome.reduit(Polynome(m1, self.var))
            else:
                return Polynome.ordonne(Polynome(m1, self.var))

    def __radd__(self, other):
        if not isinstance(other, Polynome):
            other=Polynome(repr(other), self.var)
        return other + self

    def __sub__(self, other):
        if len(other) == 1:
            return self+-other
        else:
            return [self, "+", -other]

    def __rsub__(self, other):
        if not isinstance(other, Polynome):
            other=Polynome(repr(other), self.var)
        return other - self

    def __neg__(self):
        m = [m1 for m1 in self.monomes]
        for i in range(len(m)):
            m[i][0] = -m[i][0]
        return Polynome(m, self.var)

    def __mul__(self,  other):
        if not isinstance(other, Polynome):
            other=Polynome(repr(other), self.var)
        m1, m2 = [m for m in self.monomes], [m for m in other.monomes]
        m = []
        if Polynome.degre(self) == 0:
            self.var = other.var
        elif Polynome.degre(other)==0:
            other.var = self.var
        if self.var != other.var:
            raise ValueError('Pyromaths ne sait multiplier que deux polynomes de meme variable')
        elif len(m1)>1 or len(m2)>1:
            for f1 in m1:
                for f2 in m2:
                    m.extend([repr(Polynome([f1], self.var)),
                              "*", repr(Polynome([f2], self.var)), "+"])
            m.pop(-1) # suppression du dernier +
            return m
        else:
            return Polynome([[m1[0][0]*m2[0][0], m1[0][1]+m2[0][1]]],self.var)

    def __rmul__(self,  other):
        if not isinstance(other, Polynome):
            other=Polynome(repr(other), self.var)
        return other*self

    def __len__(self):
        "retourne le nombre de monomes d'un polynome"
        m = [m1 for m1 in self.monomes]
        m =Polynome.ordonne(Polynome(m, self.var))
        return len(self.monomes)

    def degre(self):
        "retourne le degré d'un polynome"
        m = [m1 for m1 in self.monomes]
        m =Polynome.ordonne(Polynome(m, self.var))
        return m.monomes[-1][1]

    def __pow__(self, other):
        if len(self) == 1:
            return self*self
        elif len(self) == 2 and other ==2:
            a = Polynome([self.monomes[0]],  self.var)
            b = Polynome([self.monomes[1]],  self.var)
            return ["%r**2+2*%r*%r+%r**2"%(a, a, b, b)]

#---------------------------------------------------------------------
# version des priorités pour les polynomes (extensible aux décimaux ?)
#---------------------------------------------------------------------
nb = r"""
    # Utilisé pour définir un nombre dans les expressions régulières
    (?:
        [-+]?\((?:[-+]?\d+\.?\d*(?:e[-+]\d+)?|Polynome\([^)]*\))\)
        # un nombre relatif ou un polynome avec parenthèses (par exemple -(-3))
    |                           # OU
        [-+]?(?:[-+]?\d+\.?\d*(?:e[-+]\d+)?|Polynome\([^)]*\))
        # un nombre relatif ou un polynome sans parenthèses
    )"""
recherche_parentheses = re.compile(r"""
    ^(?P<pre>.*?)                   # un minium de calculs

    (?P<calcul>                     # début d'une section parenthèses
        (?<!Polynome)\((?:%s[-+*/]+)+%s\)
    )

    (?P<post>.*)$                   # groupe post (tout le reste)
    """ % (nb, nb), re.VERBOSE).search

recherche_pow = re.compile(r"""
    # Recherche la première série de puissances dans la chaine
    ^(?P<pre>                       # groupe pre-calcul
        (?:[-+*/e\d.]|(?:\<polynome\>[^(?:</polynome>)]*</polynome>))*?[-+]?
        # il y a des calculs avant l'opération cherchée avec des décimaux
        # et/ou un polynome. Le [-+] de la fin est pour le cas '3+-8**2'
    |
        \(*                         # l'opération est au début (aux parenthèses près)
    )

    (?P<calcul>                     # groupe calcul
        %s
        # remplacé par l'expression régulière représentant les nombres
        (?:\*\*[-+]?\d+)+
        # symbole exposant suivi d'un exposant entier relatif
        # éventuellement plusieurs fois consécutives
    )

    (?P<post>.*)$                  # groupe post (tout le reste)
    """ % nb, re.VERBOSE).search

recherche_produit = re.compile(r"""
    # Recherche la première série de divisions ou de multiplications dans la chaine
    ^(?P<pre>                       # groupe pre-calcul
        \(*                         # l'opération est au début (aux parenthèses près)
        |
        (?:[-+*/\d.e]|(?:\<polynome\>[^(?:</polynome>)]*</polynome>))*?(?<=\d)[-+]
        # il y a des calculs avant l'opération cherchée avec des décimaux et/ou
        # un polynome. Le [-+] de la fin est pour conserver l'opérateur avant le
        # calcul qui va être effectué
    )

    (?P<calcul>                     # groupe calcul
        %s
        # remplacé par l'expression régulière représentant les nombres
        (?:
            (?:/%s)+
        |
            (?:\*%s)+
        )
        # nb puis symbole division (ou multiplication) suivi d'un nombre
        # éventuellement plusieurs fois consécutives
    )

    (?P<post>.*)$                  # groupe post (tout le reste)
    """ % (nb, nb, nb), re.VERBOSE).search

recherche_somme = re.compile(r"""
    # Recherche la première série d'additions ou de soustractions dans la chaine
    ^(?P<pre>                       # groupe pre-calcul
        \(*                         # l'opération est au début (aux parenthèses près)
        |
        (?:[-+\d.e]|(?:\<polynome\>[^(?:</polynome>)]*</polynome>))*?(?<=\d)[-+]
        # il y a des calculs avant l'opération cherchée avec des décimaux et/ou
        # un polynome. Le [-+] de la fin est pour conserver l'opérateur avant le
        # calcul qui va être effectué
    )

    (?P<calcul>                     # groupe calcul
        %s
        # remplacé par l'expression régulière représentant les nombres
        (?:
            (?:-%s)+
        |
            (?:\+%s)+
        )
        # nb puis symbole addition ( ou soustraction) suivi d'un nombre
        # éventuellement plusieurs fois consécutives
    )

    (?P<post>.*)$                  # groupe post (tout le reste)
    """ % (nb, nb, nb), re.VERBOSE).search

recherche_polynome = re.compile(r"""
    $(?P<pre>.*?)
    (?P<calcul>Polynome\([^)]*\))
    (?P<post>.*)$""", re.VERBOSE).search

def priorites_operations(calcul):
    serie=(recherche_polynome, recherche_parentheses, recherche_pow, recherche_produit, recherche_somme)#, recherche_sub, recherche_add)
    result=[]
    for recherche in serie:
        test = recherche(calcul)
        while test:
            while test:
                t=test.groups()
                if test.group('pre'):
                    result.extend(priorites_operations(test.group('pre')))
                if recherche == recherche_polynome:
                    if Polynome.reductible(eval(test.group('calcul'))):
                        result.append(Polynome.reduit(eval(test.group('calcul'))))
                else:
                    s = eval(test.group('calcul'))
                    if not isinstance(s, str) and not isinstance(s, list):
                        s = repr(s)
                    if isinstance(s, str) and eval(s)<0 and test.group('post') and \
                       test.group('post')[0:2]=="**":
                        result.append("("+s+")")
                    elif isinstance(s, list):
                        for e in s:
                            if isinstance(e, str):
                                result.append(e)
                            else:
                                result.append(repr(e))
                    else:
                        result.append(s)
                calcul=test.group('post')
                if calcul and (calcul[0]!="-" or recherche!=recherche_somme):
                    result.append(calcul[0])
                    calcul = calcul[1:]
                    test=recherche(calcul)
                else:
                    test=None
    if calcul: result.append(calcul)
    return result

def priorites(calcul):
    solution = []
    while not solution or len(solution[-1])>1:
        if solution:
            calcul="".join(solution[-1])
        s = priorites_operations(calcul)
        if solution:
            solution.append(s)
        else:
            solution=[s]
    if isinstance(eval(s[0]), Polynome) and Polynome.reductible(eval(s[0])):
        solution.append([repr(Polynome.reduit(eval(s[0])))])
    return solution

def main():
    p=Polynome('+5z-4')
    m=Polynome('3z-9')
    n=Polynome('8z')
    q=Polynome('15.0z^2')
#    print q
#    print priorites("%r-%r" % (p, m))
    print priorites('Polynome("2z+4")**2')
#    print priorites("%r*(%r-%r)" %(n, p, m))
#    print p**2
#    calcul = '6*2/3**5+8*6**2'
#    calcul="(2.4-5.1)**2+(5.5-2.4)**3"
#    calcul='-16/-8*4+8*4'
#    calcul="((-(-1)+-2)++3)"
#    calcul="(-2**4)**4"
#    calcul="3+(-8)**2"
    calcul="2+6-4+8-9-1+7-6"
#    print(calcul)
    print(priorites(calcul))
