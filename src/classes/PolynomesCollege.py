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
        [-+]?\d+(?:\.\d*)?[a-zA-Z]?(?:\^\d+)?   # au moins un nombre décimal
        |                                       # OU
        [-+]?\d*(?:\.\d*)?[a-zA-Z](?:\^\d+)?    # au moins une variable

    )
    \s*                                         # éventuellement des espaces pour finir
""", re.VERBOSE)

_MONOME_FORMAT = re.compile(r"""
    \s*                                         # éventuellement des espaces pour commencer
    (?P<sign>[-+]?)                             # un éventuel signe
    (?P<coef>\d*(?:\.\d*)?)                     # un éventuel coefficient
    (?:(?P<var>[a-zA-Z])(?:\^(?P<deg>\d+))?)?   # une éventuelle variable avec son éventuel degré
    \s*                                         # éventuellement des espaces pour finir
""", re.VERBOSE)

class Polynome():
    """Cette classe crée la notion de polynômes.
    Polynome([[2,2],[3,1],[4,0]], 'z') est équivalent à 2z^2+3z+4.

    Un polynôme peut aussi être produit à l'aide d'une chaîne de la forme
    Polynome("2y^2+3y+4")
    """

    def __init__(self, monomes, var=None):
        """Crée un polynôme.
        Accepte une chaîne de caractères comme '2x^2-4x+6' ou une liste de
        monômes [coefficient, degré] finit par une string contenant la variable.
        Par exemple, Polynome([[5,2], [-4,1], [6,0]], 't') équivaut à
        Polynome("+5t^2-4t+6")
        """
        self.var = var # variable du polynôme
        monomes = monomes or '0' # monômes du polynôme, par défaut un polynôme nul
        self.monomes = monomes
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
            var = var or 'x' # Variable par défaut
            if listmonomes: self.monomes = listmonomes
            else: self.monomes = [[0.0, 0]]
            self.var = var
        else:
            self.var = var or 'x' # Variable par défaut

    def __repr__(self):
        """repr(self)
        Renvoie une chaîne de caractère pouvant être utilisée pour créer un polynôme.
        S'appelle ainsi : repr(p) où p est un polynôme"""
        var = self.var
#        s = "Polynome(\""
        s = ""
        for m in self.monomes:
            if isinstance(m, list):
                if m[1] > 1:
                    # Monôme de degré au moins 2
                    if m[0] == 1:
                        s = s + "+" + var + "^" + str(m[1])
                    elif m[0] == -1:
                        s = s + "-" + var + "^" + str(m[1])
                    elif m[0] > 0:
                        s = s + "+" + str(m[0]) + var + "^" + str(m[1])
                    else:
                        s = s + str(m[0]) + var + "^" + str(m[1])
                elif m[1] == 1:
                    # Monôme de degré 1
                    if m[0] == 1:
                        s = s + "+" + var
                    elif m[0] == -1:
                        s = s + "-" + var
                    elif m[0] > 0:
                        s = s + "+" + str(m[0]) + var
                    else:
                        s = s + str(m[0]) + var
                else:
                    # Monôme de degré 0
                    if m[0] < 0:
                        s = s + str(m[0])
                    else:
                        s = s + "+" + str(m[0])
        s = s.lstrip("+") # supprime le + en début de séquence
        s = "Polynome(\"%s\")" % s
        return s

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
        if s and s[0]=='+': s=s[1:]
        elif not s: s="0"
        # supprime le + en début de séquence
        return s

    def reduit(self):
        m = [m for m in Polynome.ordonne(self).monomes]
        lm = [m[0]]
        for i in range(1, len(m)):
            if lm[-1][1] == m[i][1]:
                # les deux monômes ont le même degré
                lm[-1][0] += m[i][0]
            else:
                lm.append(m[i])
        i=len(lm)-1
        while i>=0:
            if len(lm)>1 and lm[i][0] == 0: lm.pop(i) # supprime un monôme nul
            i += -1
        return Polynome(lm, self.var)

    def reductible(self):
        """Renvoie 1 si le polynôme est réductible, 0 sinon."""
        if Polynome.ordonne(self) != Polynome.reduit(self):
            return 1
        else:
            return 0

    def ordonne(self):
        m = [m1 for m1 in self.monomes]
        m = sorted(m, key = lambda x: (-x[1]))
        return Polynome(m, self.var)

    def __ne__(self, other):
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
            raise ValueError(u'Pyromaths ne sait additionner que deux polynômes de même variable')
        else :
            m=[]
            m1.extend(m2)
            for monomes in m1:
                if monomes[0]: m.append(monomes)
            return Polynome(m, self.var)

    def somme_detail(self):
        reductible = False
        var = self.var
        m = [m for m in Polynome.ordonne(self).monomes]
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

    def __radd__(self, other):
        if isinstance(other, (float, int)):
            other = Polynome(repr(other), self.var)
        elif isinstance(other, str):
            return "%s+%r" % (other, self)
        return other + self

    def __sub__(self, other):
        if not isinstance(other, Polynome):
            other=Polynome(repr(other), self.var)
        return repr(self) + -other


    def __rsub__(self, other):
        if not isinstance(other, str):
            other=str(other)
        a= -self
        return other + -self

    def __neg__(self):
        m = [m1 for m1 in self.monomes]
        for i in range(len(m)):
            m[i][0] = -m[i][0]
        return "+" + repr(Polynome(m, self.var))

    def __pos__(self):
        """+a"""
        return self


    def __mul__(self,  other):
        if not isinstance(other, Polynome):
            other=Polynome(repr(other), self.var)
        m1, m2 = [m for m in self.monomes], [m for m in other.monomes]
        m = "("
        if Polynome.degre(self) == 0:
            self.var = other.var
        elif Polynome.degre(other)==0:
            other.var = self.var
        if self.var != other.var:
            raise ValueError(u'Pyromaths ne sait multiplier que deux polynômes de même variable')
        elif len(m1)>1 or len(m2)>1:
            for f1 in m1:
                for f2 in m2:
                    m+=repr(Polynome([f1], self.var)) + "*" + \
                       repr(Polynome([f2], self.var)) + "+"
            m = m[:-1] # suppression du dernier +
            m += ")"
            return m
        else:
            return Polynome([[m1[0][0]*m2[0][0], m1[0][1]+m2[0][1]]],self.var)

    def __rmul__(self,  other):
        if isinstance(other, (int, float)):
            other = Polynome(repr(other), self.var)
        elif isinstance(other, str):
            # vérifions s'il n'y a pas un enchaînement de produits de polynômes
            # de plus d'un monôme qu'il faudrait alors détailler
            r = recherche_polynome(other)
            while r:
                if r.group('post') and r.group('post')[0]=="+":
                    return "(%s)*%r" % (other, self)
                r = recherche_polynome(r.group('post'))
            other = eval(other)
        return other*self

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
            a=m.monomes
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
            result=self
            for i in range(other-1):
                result = result*self
            return result
        else:
            result=self
            for i in range(other-1):
                result = eval(result*self)
            return result

#---------------------------------------------------------------------
# EXPRESSIONS RÉGULIÈRES
#---------------------------------------------------------------------
# Expression régulière pour définir un nombre décimal
decimal = r"[-+]?\d+\.?\d*(?:e[-+]\d+)?"#(?=[^a-z])

# Expression régulière pour définir un nombre décimal avec ou sans parenthèses
# ex : -5 et (-5)
decimal_par = r"\(%s\)|%s" % (decimal, decimal)

# Expression régulière pour définir un polynôme
polynome = r"Polynome\([^\)]+\)"

# Expression régulière pour définir un polynôme avec ou sans parenthèses
polynome_par = r"\(%s\)|%s" % (polynome, polynome)

# Expression régulière pour définir un nombre dans une opération
# un  décimal est soit en début de chaîne, soit précédé d'un opérateur.
nb = """
    # Utilisé pour définir un nombre dans les expressions régulières
    (?:                 # doit être
        ^\s*            # en début de chaîne (aux espaces près)
    |                   # OU
        (?<=[-+*/(])    # précédé d'un opérateur ou d'une parenthèses ouvrante
    )
    (?:
        (?:%s)
        |               # un décimal ou un polynôme avec ou sans parenthèses
        (?:%s)
    )
    (?:                 # doit être
        (?=[-+*/)])     # suivi d'un opérateur ou d'une parenthèses fermante
    |                   # OU
        $               # en fin de chaîne
    )
    """ % (polynome_par, decimal_par)

# Recherche des parenthèses intérieures contenant un calcul
recherche_parentheses = re.compile(r"""
    ^(?P<pre>.*?)                   # un minimum de calculs
    (?P<calcul>                     # début d'une section parenthèses
        (?<!Polynome)               # ne doit pas concerner Polynome(
        \((?:[-+]?%s[-+*/]+)+%s\)   # une succession d'opérations
    )
    (?P<post>.*)$                   # groupe post (tout le reste)
    """ % (nb, nb), re.VERBOSE).search

# Recherche la première série de puissances dans la chaîne
recherche_pow = re.compile(r"""
    ^(?P<pre>               # groupe pre-calcul
        .*?[-+]?            # il y a des calculs avant l'opération cherchée et
    )
    (?P<calcul>
        (?:%s)(?:\*\*[-+]?\d+)+ # symbole exposant suivi d'un exposant entier
    )                       # relatif éventuellement plusieurs fois consécutives
    (?P<post>.*)$           # tout le reste
    """ % (nb), re.VERBOSE).search

# Recherche la première série de divisions ou de multiplications dans la chaîne
recherche_produit = re.compile(r"""
    ^(?P<pre>.*?(?<!\*\*))        # un minimum de calculs (mais pas de puissance)
    (?P<calcul>
        %s
        (?:(?:/%s)+ | (?:\*%s)+)  # plusieurs multiplications ou divisions
        (?!\*\*)
    )
    (?P<post>.*)$                 # tout le reste
    """ % (nb, nb,  nb), re.VERBOSE).search

# Recherche les opposés de nombres dans la chaîne
recherche_neg = re.compile(r"""
    ^(?P<pre>.*?)       # un minium de calculs
    (?P<calcul>         # un nombre entre parenthèses précédé d'un signe + ou -
        (?:[-+]\(%s\)(?!\*\*)) | (?:[-+]\(%s\)(?!\*\*)) | (?:\-%s)
    )
    (?P<post>.*)$       # groupe post (tout le reste)
    """ % (decimal, decimal, polynome), re.VERBOSE).search

# Recherche la première série d'additions ou de soustractions dans la chaîne
recherche_somme = re.compile(r"""
    ^(?P<pre>                      # une somme à calculer ne doit jamais être
        .*?                        # précédée d'un produit ou d'une différence
    )
    (?P<calcul>                    # groupe calcul
        (?<![-*/])%s
        (?:(?:\-%s)+ | (?:\+%s)+)  # série d'additions ou soustractions
        (?:$ | (?:(?=[^*/])))      # ne doit pas être suivi d'un produit
    )
    (?P<post>.*)$                  # groupe post (tout le reste)
    """ % (nb, nb, nb), re.VERBOSE).search

# Recherche un nombre décimal multiplié par un monôme de coefficient 1
recherche_simplification=re.compile(r"""
    (?P<pre>.*?)
    (?P<coef>%s)
    \*
    (?P<monome>Polynome\(\"[a-z](?:\^\d+)?\"\))
    (?P<post>.*?)$""" % decimal_par, re.VERBOSE).search

recherche_polynome = re.compile(r"""
    ^(?P<pre>.*?)
    (?P<calcul>(?:%s))
    (?P<post>.*)$
    """ % (polynome), re.VERBOSE).search

suppression_parentheses_polynomes = re.compile(r"""
    (?P<pre>.*?)
    (?P<par>\( %s \) )
    (?P<post>.*?)$""" % polynome, re.VERBOSE).search

recherche_somme_polynomes = re.compile(r"""
    ^(?P<pre>                      # une somme à calculer ne doit jamais être
        .*?                        # précédée d'un produit ou d'une différence
    )
    (?P<calcul>                    # groupe calcul
        (?<![-*/])%s
        (?:\+%s)+                  # série d'additions
        (?:$ | (?:(?=[^*/])))      # ne doit pas être suivi d'un produit
    )
    (?P<post>.*)$                  # groupe post (tout le reste)
    """ % (polynome, polynome), re.VERBOSE).search
def reduire(calcul,  detail=0):
    """réduit les polynômes compris dans une chaîne de caractères."""
    groups=recherche_polynome(calcul)
    reponse=""
    modifie = 0
    if groups:
        while groups:
            reponse+=groups.group('pre')
            if Polynome.reductible(eval(groups.group('calcul'))):
                modifie = 1
                s = Polynome.somme_detail(eval(groups.group('calcul')))
                if (reponse and reponse[-1] in '-*') or (groups.group('post') and groups.group('post')[0] == '*'):
                    reponse += "(" + s + ")"
                else:
                    reponse += s
            else:
                reponse+=groups.group('calcul')
            calcul = groups.group('post')
            groups=recherche_polynome(calcul)
        reponse += calcul
        if modifie:
            return reponse
        else:
            return None
    else:
        return None

def traitement_resultat(s, before, after):
    if isinstance(s,  (int,float)):
        if s>=0:
            if before and before[-1][-1] not in '+-*/(':
                s = "+%s" % (s)
            else: s = str(s)
        else:
            if (before and before[-1][-1] in '+-*/') or\
               (after and after[0:2]=="**"):
                s = "(%s)" % (s)
            else:
                s = str(s)
    elif isinstance(s, Polynome):
        r = reduire(repr(s))
        s = r or repr(s)
        if before and before[-1][-1] not in '+-*/(': s = "+" + s
    return s

def post_traitement(s):
    r = recherche_simplification(s)
    while r:
#        t = r.groups()
        if r.group('pre').rstrip("+") and r.group('pre').rstrip("+")[-1] in "(*-":
            s = r.group('pre').rstrip("+")
        else: s = r.group('pre').rstrip("+") + "+"
        s += repr(eval(r.group('coef'))*eval(r.group('monome'))) +\
             r.group('post')
        s = s.lstrip("+")
        r = recherche_simplification(s)
    r = recherche_somme_polynomes(s)
    while r:
#        t = r.groups()
        tmp = eval(r.group('calcul'))
        if isinstance(tmp, Polynome): tmp = repr(tmp)
        elif isinstance(tmp, (int, float)): tmp = str(tmp)
        s = r.group('pre') + tmp + r.group('post')
        r = recherche_somme_polynomes(s)
    r = suppression_parentheses_polynomes(s)
    while r:
#        t = r.groups()
        s = r.group('pre')+ r.group('par')[1:-1] + r.group('post')
        r = suppression_parentheses_polynomes(s)
    return s

def priorites_operations(calcul):
    """Recherche les opérations à effectuer dans un calcul.
    @calcul: string (ex:'Polynome("3z-4")*Polynome("4z-5")')
    @nepascherchersomme: Booléen ; permet d'éviter, dans l'exemple '(2+6)*4+5',
        de calculer 4+5 après avoir calculé (2+6)
    """
    serie=(recherche_parentheses, recherche_pow, recherche_produit,
           recherche_neg, recherche_somme)
    if calcul.find("Polynome(")<0: litteral = 0
    else: litteral = 1
    result=[]
    for recherche in serie:
        test = recherche(calcul)
        while test:
            while test:
#                t=test.groups()
                if test.group('pre'):
                    tmp = priorites_operations(test.group('pre'))
                    if result and result[-1][-1] not in '+-*/(' and \
                                  tmp[0] not in    '+-*/)':
                        tmp= "+" + tmp
                    result.append(tmp)
                if recherche == recherche_parentheses:
                    # on utilise les priorités sur le calcul entre parenthèses
                    if litteral and test.group('calcul').find('Polynome("')<0:
                        # on réduit directement les calculs numériques
                        s = str(eval(test.group('calcul')))
                    else:
                        spar=priorites(test.group('calcul')[1:-1], parentheses=1)
                        if len(spar)>1:
                            s = "(" + spar[0] +")"
                        else:
                            s = traitement_resultat(eval(spar[0]), result,
                                                    test.group('post'))
                else:
                # s est soit un résultat (par exemple un polynôme), soit une
                # chaîne de caractères contenant un nouveau calcul à effectuer
                # (par exemple pour le produit de deux polynômes).
                    s = eval(test.group('calcul'))
                    s = traitement_resultat(s, result, test.group('post'))
                result.append(s)
                calcul=test.group('post')
                if calcul:
                    test = recherche(calcul)
                else:
                    test=None
    if calcul: result.append(calcul)
    s = "".join(result)
    if s.find("Polynome(")>=0:
        s = post_traitement(s)
    return s

def priorites(calcul, parentheses=0):
    """Détaille un calcul sous forme de chaîne de caractères en respectant les
    priorités.
    @calcul: string contenant le calcul (ex: '3+6-(2+9)')
    @parentheses: booléen ; dans le cas où on extrait une opération entre
        parenthèses, on ne garde que les 2 premières étapes."""
    solution = []
    while not solution or (not parentheses and calcul != solution[-1]) or \
              (parentheses and len(solution)<2 and calcul != solution[-1]):
        if solution:
            calcul=solution[-1]
        else:
            #On réduit si possible le calcul initial
            s=reduire(calcul)
            if s:
                solution.append(s)
                calcul = s
        s = priorites_operations(calcul)
        solution.append(s)
        s=reduire(s)
        if s: solution.append(s)
    if calcul == solution[-1]: solution.pop(-1) # dernier calcul en double
    if parentheses and len(solution)>1:
        # si le calcul est un extrait d'un calcul entre parenthèses, on n'a pas
        # besoin du résultat complet
        return solution
    else:
        s = solution[-1]
        p = eval(s)
        if isinstance(p, Polynome) and Polynome.reductible(p):
            solution.append(repr(Polynome.reduit(p)))
#       print solution
        return solution

def texify(liste_calculs):
    """Convertit une liste de chaînes de caractères 'liste_calculs' contenant
    des polynômes en liste de chaînes de caractères au format TeX"""
    ls = []
    for calcul in liste_calculs:
        s, q = "", ""
        groups=recherche_polynome(calcul)
        if groups: calcul_litteral = 1
        else: calcul_litteral = 0
        while groups:
            deci = groups.group('pre')
            s += groups.group('pre')
            p = eval(groups.group('calcul'))
            q = groups.group('post')
            if (s and s[-1] in "*-" and (len(p)>1 or p.monomes[0][0]<0)) \
                or (q and q[0] == "*" and len(p)>1) \
                or ((len(p)>1 or p.monomes[0][0]!=1 and p.monomes[0][1]>0) and q[:2]=="**"):
                s += "("+ str(p) +")"
            elif s and s[-1] == "+" and p.monomes[0][0]<0:
                s = s[:-1]
                s += str(eval(groups.group('calcul')))
            else:
               s += str(eval(groups.group('calcul')))
            groups=recherche_polynome(groups.group('post'))
        s += q
        calcul, s, q = s, "", ""

        if calcul_litteral:
            recherche_suppression_multiplication = re.compile(r"""
                ^(?P<pre>.*?)
                (?P<calcul>
                    \*\(
                    |
                    \d\*[a-z]
                )
                (?P<post>.*)$""", re.VERBOSE).search
            groups = recherche_suppression_multiplication(calcul)
            while groups:
                s += groups.group('pre') + groups.group('calcul').replace("*", "\\,")
                q = groups.group('post')
                groups = recherche_suppression_multiplication(q)
            s += q
            if not s: s = calcul
        s = s.replace("**", "^")
        s = s.replace("*", " \\times ")
        s = s.replace("(", " \\left(")
        s = s.replace(")", "\\right) ")
        if not ls or s != ls[-1]:
            ls.append(s)
    return ls

def sympyfy(liste_calculs):
    """Convertit une liste de chaînes de caractères 'liste_calculs' contenant
    des polynômes en liste de chaînes de caractères au format TeX"""
    ls = []
    for calcul in liste_calculs:
        s, q = "", ""
        groups=recherche_polynome(calcul)
        if groups: calcul_litteral = 1
        else: calcul_litteral = 0
        while groups:
            deci = groups.group('pre')
            s += groups.group('pre')
            p = eval(groups.group('calcul'))
            q = groups.group('post')
            if (s and s[-1] in "*-" and (len(p)>1 or p.monomes[0][0]<0)) \
                or (q and q[0] == "*" and len(p)>1) \
                or ((len(p)>1 or p.monomes[0][0]!=1 and p.monomes[0][1]>0) and q[:2]=="**"):
                s += "("+ str(p) +")"
            elif s and s[-1] == "+" and p.monomes[0][0]<0:
                s = s[:-1]
                s += str(eval(groups.group('calcul')))
            else:
               s += str(eval(groups.group('calcul')))
            groups=recherche_polynome(groups.group('post'))
        s += q
        calcul, s, q = s, "", ""

        if calcul_litteral:
            recherche_suppression_multiplication = re.compile(r"""
                ^(?P<pre>.*?)
                (?P<calcul>
                    \*\(
                    |
                    \d\*[a-z]
                )
                (?P<post>.*)$""", re.VERBOSE).search
            groups = recherche_suppression_multiplication(calcul)
            while groups:
                s += groups.group('pre') + groups.group('calcul')
                q = groups.group('post')
                groups = recherche_suppression_multiplication(q)
            s += q
            if not s: s = calcul
        s = s.replace("\\,x", "*x")
        s = s.replace("\\,", "")
        s = s.replace("^{", "**")
        s = s.replace("}", "")
        if not ls or s != ls[-1]:
            ls.append(s)
    return ls

def valeurs(n, polynomes=0, entier=1):
    """Renvoie une chaîne de caractères contenant un calcul aléatoire de
    n nombres, qui sont soit des entiers, soit des décimaux, soit des polynômes."""
    import random
    def deci(entier):
        if entier:
            return random.randrange(-11, 11)
        else:
            return random.randrange(-110, 110)/10.
    def poly(entier):
        degre=random.randrange(2, 3)
        p = [[deci(entier), i] for i in range(degre)]
        return repr(eval('Polynome(%s, "x")'  %p))
    if polynomes: nb=poly
    else: nb=deci
    nbp = []
    lo = ['+','*','-']
    for i in range(n):
        if not i:
            s = "%s" % nb(entier)
        else:
            if nbp and nbp[-1] > 2 and not random.randrange(2):
                s += ')'
                nbp.pop(-1)
            s += lo[random.randrange(3)]
            if nbp:
                for cpt in range(len(nbp)):
                    nbp[cpt] += 1
            a = random.randrange(3)
            if s[-1] in '*-' and i<n-2 and not a:
                s += '('
                nbp.append(1)
            nombre = nb(entier)
            if nombre < 0: s += "(" + str(nombre) + ")"
            else: s += str(nombre)
            if not polynomes: #TODO: tester les puissances avec les polynômes
                a = random.randrange(10)
                if (not nbp or nbp[-1]>1) and not a:
                    s += "**2"
    while nbp:
        s += ')'
        nbp.pop(-1)
    return s

def remplace_decimaux(matchobj):
    nb = matchobj.group(0)
    if nb[0]=="+": return "+" + decimaux(nb[1:])
    else: return decimaux(nb)

def test_entiers(nbval, polynomes, entiers):
    for c in range(1000):
        a = valeurs(nbval, polynomes, entiers)
        r = priorites(a)
        if not polynomes:
            print u"%s ème calcul" % (c+1), a, " = ", eval(a), u" en %s étapes"%(len(r))
            if str(eval(a)) != r[-1]:
                print a, " = ", eval(a)
                print r
                break
        if polynomes:
            from sympy import Symbol, expand
            x = Symbol('x')
            print u"%s ème calcul en %s étapes : " % (c+1, len(r)),
            t0=sympyfy([a])[0]
            print a
            t1=sympyfy([r[-1]])[0]
            if eval(t0).expand()!=eval(t1):
                print a, "=", t1
                print r
                print eval(t0).expand()
                break

def main():
    test_entiers(nbval=3, polynomes=1, entiers=1)
    a='Polynome("-10+9x")-Polynome("2-11x")*Polynome("-4+5x")'
#    print sympyfy([a])
#    print recherche_somme(a).groups()
#    print "\n".join(priorites(a))
