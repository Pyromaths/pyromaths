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

if __name__=="__main__":
    import sys
    sys.path.append('..')


from ..outils.Affichage import decimaux

_POLYNOME_FORMAT = re.compile(r"""
    \s*                                         # éventuellement des espaces pour commencer
    (                                           # chaque monôme
        [-+]?\d+\.?\d*(?:e[-+]\d+)?[a-df-hkmnp-zA-NP-Z]?(?:\^\d+)?   # au moins un nombre décimal
        |                                       # OU
        [-+]?\d*\.?\d*(?:e[-+]\d+)?[a-df-hkmnp-zA-NP-Z](?:\^\d+)?    # au moins une variable

    )
    \s*                                         # éventuellement des espaces pour finir
""", re.VERBOSE)

_MONOME_FORMAT = re.compile(r"""
    \s*                                         # éventuellement des espaces pour commencer
    (?P<sign>[-+]?)                             # un éventuel signe
    (?P<coef>\d*\.?\d*(?:e[-+]\d+)?)                     # un éventuel coefficient
    (?:(?P<var>[a-df-hkmnp-zA-NP-Z])(?:\^(?P<deg>\d+))?)?   # une éventuelle variable avec son éventuel degré
    \s*                                         # éventuellement des espaces pour finir
""", re.VERBOSE)

class Polynome():
    """Cette classe crée la notion de polynômes.
    Polynome([[2,2],[3,1],[4,0]], 'z') est équivalent à 2z^2+3z+4.

    Un polynôme peut aussi être produit à l'aide d'une chaîne de la forme
    Polynome("2y^2+3y+4")

    Les variables ne peuvent être : e, i, j, l, o, O.
    """

    def __init__(self, monomes, var=None):
        """Crée un polynôme.
        Accepte une chaîne de caractères comme '2x^2-4x+6' ou une liste de
        monômes [coefficient, degré] finit par une string contenant la variable.
        Par exemple, Polynome([[5,2], [-4,1], [6,0]], 't') équivaut à
        Polynome("+5t^2-4t+6")
        """
        monomes = monomes or '0' # monômes du polynôme, par défaut un polynôme nul
        if isinstance(monomes, basestring):
            # Gère la construction des polynôme à partir d'une chaîne de caractères
            listmonomes = []
            for monome in _POLYNOME_FORMAT.finditer(monomes):
                m = _MONOME_FORMAT.search(monome.group(0))
                if m is None:
                    raise ValueError(u'chaîne invalide pour un objet Polynôme : %s' % input)
                m_sign = m.group('sign') or '+'
                m_coef = float(m.group('coef') or 1)
                m_deg = int(m.group('deg') or (m.group('var') and '1') or '0')
                m_var = m.group('var') or var
                if m_var and not var: var = m_var # attribue une variable à var
                if m_var != var:
                    raise ValueError(u'Le nom de la variable (%s) est incorrect pour le Polynôme %s' % (var, monomes))
                if m_sign == '-': m_coef = -m_coef
                if m_coef:
                    # supprime les monômes de coefficient 0
                    listmonomes.append([m_coef, m_deg])
            if listmonomes: self.monomes = listmonomes
            else: self.monomes = [[0, 0]]
            self.var = var or 'x'
        else:
            #Supprime les monomes nuls :
            for k in range(len(monomes)-1, -1, -1):
                if not monomes[k][0]: monomes.pop(k)
            if not monomes: monomes=[[0, 0]]
            self.monomes = monomes
            self.var = var or 'x' # Variable par défaut

    def __repr__(self):
        """repr(self)
        Renvoie une chaîne de caractère pouvant être utilisée pour créer un polynôme.
        S'appelle ainsi : repr(p) où p est un polynôme"""
        return "Polynome(%s, \"%s\")" % (self.monomes, self.var)

    def __str__(self):
        """str(self)
        Renvoie une version LaTeX du polynôme"""
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
                    elif m[0] > 0:
                        s = s + "+" +decimaux(m[0], 1) + r"\," + var + "^{" + str(m[1]) + "}"
                    else:
                        s = s + decimaux(m[0], 1) + r"\," + var + "^{" + str(m[1]) + "}"
                elif m[1] == 1:
                    # Monôme de degré 1
                    if m[0] == 1:
                        s = s + "+" + var
                    elif m[0] == -1:
                        s = s + "-" + var
                    elif m[0] > 0:
                        s = s + "+" + decimaux(m[0], 1) + r"\," + var
                    else:
                        s = s + decimaux(m[0], 1) + r"\," + var
                else:
                    # Monôme de degré 0
                    if m[0] < 0:
                        s = s + decimaux(m[0], 1)
                    else:
                        s = s + "+" + decimaux(m[0], 1)
        # supprime le + en début de séquence
        s = s.lstrip("+")
        if not s: s="0"
        return s

    def __getitem__(self, i):
        """Renvoie le i ème monôme"""
        return self.monomes[i]

    def __iadd__(self, other):
        """Définit @self += @other"""
        if isinstance(other, (float, int)):
            other = Polynome([[other, 0]], self.var)
        m1, m2 = [m for m in self.monomes], [m for m in other.monomes]
        if Polynome.degre(self) <= 0:
            self.var = other.var
        elif Polynome.degre(other)<=0:
            other.var = self.var
        if self.var != other.var:
            raise ValueError(u'Pyromaths ne sait additionner que deux polynômes de même variable')
        else :
            m=[]
            m1.extend(m2)
            for monomes in m1:
                if monomes[0]: m.append(monomes)
            return Polynome(m, self.var)

    def __eq__(self, other):
        """Renvoie True si @self est égal à @other, False sinon. Ne tient pas
        compte de l'ordre des monômes"""
        if not isinstance(other, Polynome):
            other = Polynome(other, self.var)
        return not (self.var != other.var or \
                    sorted(self.monomes, key = lambda x: (-x[1], x[0])) != \
                    sorted(other.monomes, key = lambda x: (-x[1], x[0])))

    def __ne__(self, other):
        """ @self différent de @other ?"""
        return not (self==other)

    def __add__(self, other):
        """Calcule la somme des polynômes @self et @other"""
        if isinstance(other,  basestring):
            other = eval(other)
        self += other
        return self

    def __radd__(self, other):
        if isinstance(other,  basestring):
            other = eval(other)
        if isinstance(other, (float, int)):
            other = Polynome([[other, 0]], self.var)
        return other + self

    def __sub__(self, other):
        """Jamais utilisé !"""
        if not isinstance(other, Polynome):
            self.monomes.append([-other, 0])
            return self
        elif len(other) == 1 and other.monomes[0][0]>0:
            #Cas où on soustrait un polynôme de longueur 1 et de coef positif
            return self + (-other)
        return "%r+%r" %(self, -other)

    def __rsub__(self, other):
        """Jamais utilisé !"""
        if not isinstance(other, str):
            other=str(other)
        return other + -self

    def __neg__(self):
        """Renvoie l'opposé d'un polynôme"""
        m = [m1 for m1 in self.monomes]
        for i in range(len(m)):
            m[i][0] = -m[i][0]
        return Polynome(m, self.var)

    def __pos__(self):
        """+a"""
        return self

    def __mul__(self,  other):
        #TODO: Cas d'un produit par 0 ou 1
        if not isinstance(other, Polynome):
            other=Polynome(repr(other), self.var)
        m1, m2 = [m for m in self.monomes], [m for m in other.monomes]
        if Polynome.degre(self) == 0:
            self.var = other.var
        elif Polynome.degre(other)==0:
            other.var = self.var
        if self.var != other.var:
            raise ValueError(u'Pyromaths ne sait multiplier que deux polynômes de même variable')
        p0, p1 = Polynome.reduit(self), Polynome.reduit(other)
        if len(p0) == len(p1) == 2 and (p0[0]==p1[0] or p0[1] == p1[1]) and\
            ((p0[0][0] == -p1[0][0] and p0[0][1] == p1[0][1]) or \
            (p0[1][0] == -p1[1][0]  and p0[1][1] == p1[1][1])):
            # 3ème identité remarquable
            if p0[0]==p1[0]:
                return "%r**2-%r**2" % (Polynome([p0[0]], self.var), \
                                        Polynome([[abs(p0[1][0]), p0[1][1]]],\
                                                self.var))
            else:
                return "%r**2-%r**2" % (Polynome([p0[1]], self.var), \
                                        Polynome([[abs(p0[0][0]), p0[0][1]]], \
                                                self.var))
        elif len(m1)>1 or len(m2)>1:
            p0, p1 = Polynome.reduit(self), Polynome.reduit(other)
            if p0!=self or p1 != other:
                if isinstance(p0, Polynome): p0 = repr(p0)
                else: p0 = "(" + p0 + ")"
                if isinstance(p1, Polynome): p1 = repr(p1)
                else: p1 = "(" + p1 + ")"
                return p0 + "*" + p1
            m = ""
            for f1 in m1:
                for f2 in m2:
                    m += repr(Polynome([f1], self.var)) + "*"
                    m += repr(Polynome([f2], self.var)) + "+"
            m = m[:-1] # suppression du dernier +
            return m
        elif not m1[0][0] or not m1[0][0]: return 0
        else:
            if m2[0][0] == 1 or (m2[0][1] == 0 and m1[0][1] == 0):
                # 3*x ou 3*4 -> 3x ou 12
                return Polynome([[m1[0][0]*m2[0][0], m1[0][1]+m2[0][1]]],self.var)
            else:
                # 3x*4 ou x*3x ou 3x*4x => 3*4*x ou 3*x*x ou 3*4*x*x
                m = []
                if m1[0][0] != 1:
                    m.append(str(m1[0][0]))
                if m2[0][0]<0: m.append("(" + str(m2[0][0]) + ")")
                else: m.append(str(m2[0][0]))
                if m1[0][1]>0: m.append("Polynome(\"%s^%s\")" % (self.var, m1[0][1]))
                if m2[0][1]>0: m.append("Polynome(\"%s^%s\")" % (self.var, m2[0][1]))
                return "*".join(m)

    def __rmul__(self,  other):
        """Multiplication de @other (qui n'est pas un polynôme) par @self (qui
        en est un)
        - Si @other est une suite de produits de monômes, et @self un polynôme
          de rang 1, on effectue toutes les multiplications en une fois
        - Sinon, on calcule d'abord @other"""
        if isinstance(other, (int, float)):
            other = Polynome(repr(other), self.var)
            return other*self
        if isinstance(other, str):
            from PolynomesStr import splitting
            ls = splitting(other)
            if ls.count("+") or ls.count("-"):
                # Réduire @other avant de faire le produit et vérifier s'il faut
                # des parenthèses autour de l'expression @other
                par, besoin = 0, False
                for k in range(len(ls)):
                    if ls[k] == "(": par +=1
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
                        if len(eval(ls[i]))>1:
                            return other + "*" + repr(self)
                        elif Polynome.degre(eval(ls[i]))>0:
                            index = index or i
                index = index or len(ls)
                if self.monomes[0][0] != 1:
                    ls.insert(index, "*")
                    if self.monomes[0][0] < 0: ls.insert(index, "(" + str(self.monomes[0][0]) + ")")
                    else: ls.insert(index, str(self.monomes[0][0]))
                if self.monomes[0][1] > 0:
                    ls.append("*")
                    ls.append("Polynome([%s], \"%s\")" %([1, self.monomes[0][1]], self.var))
                return "".join(ls)
        else: raise ValueError(u"Type non prévu. Bogue en perspective !")

    def __len__(self):
        "retourne le nombre de monômes d'un polynôme"
        m = [m1 for m1 in self.monomes]
        m =Polynome.ordonne(Polynome(m, self.var))
        return len(self.monomes)

    def degre(self):
        "retourne le degré d'un polynôme, -1 pour le polynôme nul"
        if self == Polynome(""): return -1
        else:
            m = [m1 for m1 in self.monomes]
            m =Polynome.ordonne(Polynome(m, self.var))
            return m.monomes[0][1]

    def __pow__(self, other):
        if len(self) == 2 and other ==2:
            a0 = self.monomes[0][0]
            b0 = self.monomes[1][0]
            p = a0*b0
            a = Polynome([[abs(a0), self.monomes[0][1]]],  self.var)
            b = Polynome([[abs(b0), self.monomes[1][1]]],  self.var)
            if p < 0:
                return "%r**2-2*%r*%r+%r**2"%(a, a, b, b)
            else:
                return "%r**2+2*%r*%r+%r**2"%(a, a, b, b)
        elif len(self)==1:
            return Polynome([[self[0][0]**other, self[0][1]*other]], self.var)
        else:
            result=self
            for i in range(other-1):
                result = eval(result*self)
            return result

    def reduit(self):
        """Renvoie une version réduite du polynôme self"""
        polynome = []
        for monome in Polynome.ordonne(self).monomes:
            if  polynome and monome[1] == polynome[-1][1]:
                polynome[-1][0] += monome[0]
            else:
                polynome.append([monome[0], monome[1]])
                #ATTENTION : polynome.append(monome) modifie self !!!
        for k in range(len(polynome)-1, -1, -1):
            if polynome[k][0] == 0: polynome.pop(k)
        return Polynome(polynome, self.var)

    def reduction_detaillee(self):
        """Ordonne puis effectue les factorisations qui permettent de réduire un
        polynôme"""
        po = Polynome.ordonne(self)
        if not Polynome.reductible(self) or repr(po) != repr(self):
            return po
        else:
            reductible = False
            var = self.var
            m = [m for m in po.monomes]
            s, p = "", "Polynome(\""
            tmp = ""
            for i in range(len(m)):
                if tmp == "":
                    tmp = "(%s" % str(m[i][0])
                elif m[i][1] == m[i-1][1]:
                    if m[i][0]>0: tmp += "+"
                    tmp += str(m[i][0])
                    reductible = True
                else:
                    if reductible:
                        tmp += ")"
                        s += "+%s*%r" % (tmp, Polynome('1%s^%s' % (var, m[i-1][1])))
                    else:
                        s += "+Polynome(\"%s%s^%s\")" % (str(m[i-1][0]), var,  m[i-1][1])
                    tmp = "(%s" % str(m[i][0])
                    reductible = False
            if reductible:
                tmp += ")"
                if m[-1][1]==0:
                    tmp = eval(tmp)
                    s += "+Polynome(\"%s\")" % tmp
                else:
                    s += "+%s*%r" % (tmp, Polynome('1%s^%s' % (var,  m[-1][1])))
            else:
                s += "+Polynome(\"%s%s^%s\")" % (str(m[-1][0]), var,  m[-1][1])
            s = s.lstrip("+") # suppression du + initial
            return s

    def reductible(self):
        """Renvoie 1 si le polynôme est réductible, 0 sinon."""
        if self != Polynome.reduit(self):
            return 1
        else:
            return 0

    def ordonne(self):
        """Ordonne les monômes du polynôme @self en écrivant en premier ceux
        de degré supérieur"""
        m1 = self.monomes
        m1 = sorted(m1, key = lambda x: (-x[1]))
        return Polynome(m1, self.var)
