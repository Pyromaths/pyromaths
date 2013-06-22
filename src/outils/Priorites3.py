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
#----------------------------------------------------------------------
# Pyromaths : GESTION DES PRIORITES
#----------------------------------------------------------------------
from ..classes.PolynomesCollege import Polynome
from ..outils.Affichage import decimaux


def cherche_polynome(calcul, index):
    """Recherche le premier polynôme dans la chaîne calcul à une position
    supérieure ou égale à index, sans expression régulière
    @calcul: str
    @index: int"""
    index = calcul.find("Polynome(", index)
    if index < 0: return None
    par, i = 1, index+9 # nombre de parenthèses ouvertes, début de recherche
    while par:
        if calcul.find("(", i)>0:
            i = min(calcul.find("(", i), calcul.find(")", i))
        else:
            i = calcul.find(")", i)
        if calcul[i] == ")": par += -1
        else: par += 1
    return calcul[index:i+1]

def cherche_decimal(calcul, index):
    """130 fois plus rapide qu'avec une expression régulière !
    Un nombre décimal peut être entouré de parenthèses s'il a un signe, ou avoir
    un signe s'il est en début de chaîne
    @calcul: str
    @index: int"""
    end = len(calcul)
    while index<=end:
        try:
            int(calcul[index])
        except:
            index+=1
        else:
            break
    if index>end: return None
    while end>index:
        try:
            float(calcul[index:end])
        except ValueError:
            end -= 1
        else:
            break
    if index>1 and (calcul[index-2:index] == "(+" or calcul[index-2:index] ==
            "(-") :
        if end < len(calcul) and calcul[end]==")":
            index -= 2
            end += 1
        else:
            index -= 1
    return calcul[index:end]

def split_calcul(calcul):
    """Partitionne la chaîne de caractères pour obtenir une liste d'opérateurs,
    de parenthèses, de polynômes et de nombres
    @calcul: str"""
    l = []
    findings = (cherche_polynome, cherche_decimal)
    for finding in findings:
        nb = finding(calcul, 0)
        while nb:
            l.extend(calcul.partition(nb))
            if l[-3] and l[-2]:
                l0 = split_calcul(l[-3])
                if l0:
                    l0.extend(l[-2:])
                    l = l[:-3]
                    l.extend(l0)
            elif not l[-3]:
                l.pop(-3)
            calcul = l[-1]
            nb = finding(calcul, 0)
            l = l[:-1]
    if calcul: l.append(calcul)
    while l and not l[0]:
        l.pop(0)
    return l

def EstNombre(value):
    """Test si Value est un nombre ou pas
    @value: str"""
    if value in "**/+-()":
        return False
    else:
        return isinstance(eval(value), (float, int, Polynome))

def splitting(calcul):
    """Partitionne la chaîne de caractères pour obtenir une liste d'opérateurs,
    de parenthèses, de polynômes et de nombres puis arrange la liste des
    opérandes et opérateurs
    @calcul: str"""
    if calcul == "": return []
    l = split_calcul(calcul)
    if l[0] == "+" and len(l) > 1: l[0] += l.pop(1)
    elif l[0] == "-" and len(l) > 1 and l[1][0] in "0123456789": l[0] += l.pop(1)
    j = 0
    while j < len(l):
        op, i, t = l[j], 0, []
        if op == "**": j+= 1
        else:
            while i < len(op) and op[i] in '+-*/()':
                t.append(op[i])
                i += 1
            if i == len(op):
                l[j:j+1] = t
                j += len(t)
            else: j += 1
    return l

def recherche_parentheses(calcul):
    """Recherche les parenthèses intérieures dans une liste
    @calcul: list"""
    if calcul.count("("):
        debut = calcul.index("(")
        if calcul[debut+1:].count(")"): fin = calcul[debut:].index(")") + debut
        else: return None
        for i in range(calcul[debut + 1:fin].count("(")):
            debut += calcul[debut+1:].index("(") + 1
        return (debut, fin+1)
    else:
        return None

def recherche_puissance(calcul):
    """Recherche la première occurrence d'une puissance dans une liste de
    calculs. Elle doit être entourée de deux nombres.
    @calcul: list"""
    if calcul.count("**"):
        i = calcul.index("**")
        return (i-1, i+2)
    else:
        return None

def recherche_operation(calcul, op, l_interdit, debut = 0):
    """Recherche la première occurrence de l'opération op dans la liste de
    calculs list. L'opérateur doit être entouré de deux nombres, le premier ne
    doit pas être précédé d'un opérateur inclus dans la liste l_interdit.
    L'opérateur à trouver doit être avant la position debut (si debut est non
    nul).
    @calcul: list
    @op: str
    @l_interdit: list
    @debut: int"""
    ind, fin = 0, len(calcul)
    for c in range(calcul.count(op)):
        ind = calcul.index(op, ind)
        if ind == 1 and ind < fin-1 and EstNombre(calcul[ind-1]) and\
            EstNombre(calcul[ind+1]):
                if debut: debut = min(debut, ind)
                else: debut = ind
                break
        elif ind > 1 and ind < fin -1 and EstNombre(calcul[ind-1]) and\
            EstNombre(calcul[ind+1]) and calcul[ind-2] not in l_interdit:
                if debut: debut = min(debut, ind)
                else: debut = ind
                break
        else:
            ind += 1
    if debut: return debut
    else: return None

def recherche_fin_operation(calcul, op, l_interdit, debut):
    """Recherche la fin de la suite d'opération @op situé à la position @debut
    de la liste de calculs @calcul, en vérifiant que cet enchaînement n'est pas
    suivi par un opérateur compris dans @l_interdit.
    @calcul: list
    @op: str
    @l_interdit: list
    @debut: int"""
    index, fin, unique = debut + 2, len(calcul), False
    while index < fin-1 and calcul[index] == op and EstNombre(calcul[index+1]):
        index +=2
    if index < fin and calcul[index] in l_interdit:
        index -=2
    if index == debut: return None
    return index

def recherche_produit(calcul):
    """Recherche la première occurrence d'une multiplication ou divisions dans
    une liste de calculs. Elle doit être précédée d'un nombre qui ne doit pas
    être précédé d'une puissance ou d'une division, NI SUIVIE D'UN EXPOSANT !
    @calcul: list"""
    debut = recherche_operation(calcul, "*", ("**", "/"))
    debut = recherche_operation(calcul, "/", ("**", "/"), debut)
    if debut is not None:
        fin = recherche_fin_operation(calcul, calcul[debut], ("**"), debut)
        if fin is not None: return (debut - 1, fin)
    return None

def recherche_somme(calcul):
    """Recherche la première occurrence d'une addition ou soustraction dans une
    liste de calculs. Elle doit être précédée d'un nombre qui ne doit pas être
    précédé d'une puissance, d'une multiplication, d'une division ou d'une
    soustraction, NI SUIVIE D'UN EXPOSANT, D'UNE MULTIPLICATION OU D'UNE
    DIVISION !
    @calcul: list"""
    debut = recherche_operation(calcul, "+", ("**", "*", "/", "-"))
    debut = recherche_operation(calcul, "-", ("**", "*", "/", "-"), debut)
    if debut is not None:
        fin = recherche_fin_operation(calcul, calcul[debut], ("**", "*", "/"),
                debut)
        if fin is not None: return (debut - 1, fin)
    return None

def recherche_neg(calcul):
    """Recherche la première occurence d'un opposé ## -(-5) ou -Polynome ## ou
    d'une écriture du style +(-5) dans une liste de calculs ET NE DOIT PAS ĘTRE
    SUIVI D'UN EXPOSANT !
    @calcul: list"""
    ind, debut, fin = 0, None, len(calcul)
    for c in range(calcul.count("-")):
        ind = calcul.index("-", ind)
        if ind < fin-1 and EstNombre(calcul[ind+1]):
            n = eval(calcul[ind+1])
            if calcul[ind+1][0] == "(" or isinstance(n, Polynome):
#                or (isinstance(n, Polynome) and (len(n)>1 or n.monomes[0][0]<0)):
                debut = ind
                break
        else:
            ind += 1
    for c in range(calcul[ind+1:].count("+")):
        ind = calcul.index("+", ind)
        if ind < fin-1 and EstNombre(calcul[ind+1]) and calcul[ind+1][0] == "(":
            if debut is not None: debut = min(debut, ind)
            else: debut = ind
            break
        else:
            ind += 1
    if debut is not None and (debut+2 == fin or (debut+2<fin and
        calcul[debut+2] != "**")):
        return (debut, debut+2)
    else: return None

def post_polynomes(l_calcul):
    """Réduit les polynômes de la liste de calculs"""
    for k in range(len(l_calcul)):
        if 'Polynome(' in l_calcul[k]:
            p = eval(l_calcul[k])
            if Polynome.reductible(p):
                p = Polynome.reduction_detaillee(p)
                if isinstance(p, Polynome): l_calcul[k] = repr(p)
                else:
                    if isinstance(p, basestring): p = splitting(p)
                    if (k and l_calcul[k-1] in "*-") or (k<len(l_calcul)-1 and l_calcul[k+1] in "**"):
                        p.insert(0, "(")
                        p.append(")")
                    l_calcul[k:k+1] = p
    return l_calcul

def effectue_calcul(calcul):
    """Effectue une étape du calcul en respectant les priorités
    @calcul: list"""
    serie = (recherche_parentheses, recherche_puissance, recherche_produit,
            recherche_neg, recherche_somme)
    result, post, break_somme = [], "", False
    for recherche in serie:
        if break_somme and recherche == recherche_somme: break
        if calcul: test = recherche(calcul)
        else: test = None
        while test:
            pre = calcul[:test[0]]
            calc = calcul[test[0]:test[1]]
            post = calcul[test[1]:]
            # On essaie d'utiliser les priorités sur la première partie du
            # calcul pour raccourcir la résolution de l'expression
            if test != recherche_neg and pre:
                # Si on simplifie les écritures, on n'essaie pas les sommes
                tmp = effectue_calcul(pre)
                if tmp and result and result[-1] not in "+-**/(" and tmp[0][0]\
                    not in "+-*/)":
                    # un signe + si l'expression en a besoin
                    result.append("+")
                # On ajoute le résultat ou l'expression
                if tmp: result.extend(tmp)
                else: result.extend(pre)
            else:
                result.extend(pre)
            if recherche == recherche_parentheses:
                # On supprime les parenthèses autour de l'expression
                calc = calc[1:-1]
                # On réduit directement les calculs numériques dans une
                # expression littérale
                sol = effectue_calcul(calc)
                if len(sol)>1:
                    sol.insert(0, "(")
                    sol.append(")")
                elif sol and isinstance(eval(sol[0]), (int, float)) and post and post[0] == "*" and \
                        'Polynome(' in post[1] and len(eval(post[1])) == 1 and \
                        eval(post[1])[0][0] == 1:
                            # Sans doute une factorisation de sommes de polynômes
                            sol = [repr(eval(sol[0])*eval(post [1]))]
                            post = post[2:]
                            #Suppression des parenthèses autour de ((9.0-80.0)*Polynome("x")) devenu (Polynome("-71.0x"))
                            if post and result and post[0] == ")" and result[-1] == "(" :
                                result,  post = result[:-1],  post[1:]
            else:
                # Transforme les réels en polynômes afin de permettre les opérations
                bpoly = False
                for k in range(len(calc)):
                    if not bpoly and calc[k][:9] == "Polynome(": bpoly = True
                    elif bpoly and calc[k] not in "**/-+()" and calc[k-1] != "**" and isinstance(eval(calc[k]), (float, int)):
                        calc[k] = "Polynome([[%s, 0]])" % eval(calc[k])
                sol = eval("".join(calc))
                if isinstance(sol, basestring): sol = splitting(sol)
                elif isinstance(sol, (int, float)): sol = [str(sol)]
                elif isinstance(sol, Polynome): sol = [repr(sol)]
                else : raise valueError(u"Le résultat a un format inattendu")
            if recherche == recherche_neg:
                # Ajoute le "+" ou sépare le "-":
                # "1-(-9)" => "1 + 9" et "1+(-9)" => "1 - 9"
                if sol[0][0] == "-": sol = ["-", sol[0][1:]]
                else: sol = ["+", sol[0]]
            if recherche == recherche_produit and len(sol) > 1:
                # Ajoute les parenthèses si produit précédé d'un "-" ou "*"
                # ou suivi d'un "*"
                if (result and result[-1] in "*-") or (post and post[0] == "*"):
                    sol.insert(0, "(")
                    sol.append(")")
            # Si @sol est négatif et @result se termine par un "+", on l'enlève
            if result and result[-1] == "+" and sol and sol[0][0] == "-":
                    result[-1] = "-"
                    sol[0] = sol[0].lstrip("-")
            result.extend(sol)
            calcul = post
            if calcul: test = recherche(calcul)
            else: test = None
            if post and recherche == recherche_neg: break_somme=True
    result.extend(post)
    if not result: result = calcul
    tmp = "".join(result)
#    if cherche_polynome(tmp, 0):
#        index = tmp.find("+-")
#        while index >=0 :
#            nb = cherche_decimal(tmp, index+2)
#            tmp = tmp[:index+1] + "(-" + nb + ")" + tmp[index+2+len(nb):]
#            index = tmp.find("+-")
#        result = splitting(tmp)
    return result

def priorites(calcul):
    """Effectue un enchaînement d'opérations contenues dans calcul en
    respectant les priorités et en détaillant les étapes.
    @calcul: str"""
#    if cherche_polynome(calcul, 0)>=0: litteral = True
#    else: litteral = False
    calcul = splitting(calcul)
    solution = []
    while len(calcul)>1:
        s= effectue_calcul(calcul)
        if s:
            s = post_polynomes(s)
            solution.append(s)
        calcul = [k for k in s] # dissocie calcul et s
        if len(calcul) == 1 and post_polynomes(calcul) != s:
            # Finit la réduction du polynôme résultat
            solution.append(calcul)
    return solution

def texify(liste_calculs):
    """Convertit une liste de chaînes de caractères 'liste_calculs' contenant
    des polynômes en liste de chaînes de caractères au format TeX"""
    ls = []
    for calcul in liste_calculs:
        if isinstance(calcul,  basestring): calcul = splitting(calcul)
        s = ""
        puiss = 0
        for i in range(len(calcul)):
            el = calcul[i]
            if el[:9] == "Polynome(":
                # Doit-on entourer ce polynôme de parenthèses ?
                p = eval(el)
                if i+1 < len(calcul): q = calcul[i+1]
                else: q= ""
                if (s and s[-1] in "*-" and (len(p)>1 or p.monomes[0][0]<0)) \
                    or (q and q == "*" and len(p)>1) \
                    or ((len(p)>1 or p.monomes[0][0]!=1) and q and q == "**"):
                    s += "(" + str(p) +")"
                elif s and s[-1] == "+" and p.monomes[0][0]<0:
                    s = s[:-1]
                    s += str(p)
                else:
                    s += str(p)
            elif EstNombre(el):
                if el[0]=="(": s += "(" + decimaux(el[1:-1]) + ")"
                else: s += decimaux(el)
            elif el == "**":
                s += "**{"
                puiss += 1
            elif el == "(":
                if puiss: puiss += 1
                s += "("
            elif el == ")":
                if puiss: puiss -= 1
                s += ")"
            else :
                # "+", "-", "*", "/"
                s += el
            if puiss == 1 and s[-1] != "{":
                puiss = 0
                s += "}"
        s = s.replace("**{", "^{")
        s = s.replace("(", "\\left( ")
        s = s.replace(")", "\\right) ")
        s = s.replace("*", _("\\times "))
        s = s.replace("/", _("\\div "))
        if not ls or s != ls[-1]:
            ls.append(s)
    return ls

#----------------------------------------------------------------------
# Pyromaths : FICHIERS DE TESTS
#----------------------------------------------------------------------
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
        long = random.randrange(3)
        degre=[0, 1, 2]
        p = [[deci(entier), degre.pop(random.randrange(len(degre)))] for i in range(long+1)]
        p = Polynome(p, "x")
        while p == Polynome([[0, 0]], "x"):
            degre=[0, 1, 2]
            p = [[deci(entier), degre.pop(random.randrange(len(degre)))] for i in range(long+1)]
            p = Polynome(p, "x")
        if len(p) == 1 and Polynome.degre(p) == 0:
            p = p[0][0]
            if p < 0: p = "(" + str(p) +")"
            else: p = str(p)
        else: p = repr(p)
        return p
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
            if s[-1] in '*-/' and i<=n-2 and not a:
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

def test_entiers(nbval, polynomes, entiers):
    for c in range(10000):
        a = valeurs(nbval, polynomes, entiers)
        try:
            r = priorites(a)
            texify(r)
        except:
            print(a)
            break
        else:
            if not polynomes:
                print _(u"%s ème calcul") % (c+1), a, " = ", eval(a), _(u" en %s étapes")%(len(r))
                if eval(a) != eval("".join(r[-1])):
                    print a, " = ", eval(a)
                    print r
                    break
            if polynomes:
                from sympy import Symbol, expand
                x = Symbol('x')
                print _(u" : %s ème calcul en %s étapes") % (c+1, len(r))
                if not len(r):
                    print a
                    break
                else:
                    t0=sympyfy([a])[0]
                    t1=sympyfy(r[-1])
                    if isinstance(eval(t1[0]), (int, float)) : t1[0] = "%s+x-x" % (t1[0])
                    if isinstance(eval(t0), (int, float)) : t0 = "%s+x-x" % (t0)

                    if eval(t0).expand()!=eval(t1[0]).expand():
                        print a, "=", t1
                        print "\n".join(sympyfy(r))

                        print _(u"Devrait être : "), eval(t0).expand()
                        break

def sympyfy(liste_calculs):
    """Convertit une liste de chaînes de caractères 'liste_calculs' contenant
    des polynômes en liste de chaînes de caractères au format Sympy"""
    ls = []
    for calcul in liste_calculs:
        if isinstance(calcul,  basestring): calcul = splitting(calcul)
        s = ""
        puiss = 0
        for i in range(len(calcul)):
            el = calcul[i]
            if el[:9] == "Polynome(":
                # Doit-on entourer ce polynôme de parenthèses ?
                p = eval(el)
                if i+1 < len(calcul): q = calcul[i+1]
                else: q= ""
                if (s and s[-1] in "*-" and (len(p)>1 or p.monomes[0][0]<0)) \
                    or (q and q == "*" and len(p)>1) \
                    or ((len(p)>1 or p.monomes[0][0]!=1) and q and q == "**"):
                    s += "(" + str(p) +")"
                elif s and s[-1] == "+" and p.monomes[0][0]<0:
                    s = s[:-1]
                    s += str(p)
                else:
                    s += str(p)
            elif EstNombre(el):
                if el[0]=="(": s += "(" + decimaux(el[1:-1]) + ")"
                else: s += decimaux(el)
            elif el == "**":
                s += "**{"
                puiss += 1
            elif el == "(":
                if puiss: puiss += 1
                s += "("
            elif el == ")":
                if puiss: puiss -= 1
                s += ")"
            else :
                # "+", "-", "*", "/"
                s += el
            if puiss == 1:
                puiss = 0
                s += "}"
        s = s.replace("\\,x", "*x")
        s = s.replace("\\,", "")
        s = s.replace("**{", "**")
        s = s.replace("^{", "**")
        s = s.replace("}", "")
#        s = s.replace("(", "\\left( ")
#        s = s.replace(")", "\\right) ")
#        s = s.replace("**{", "^{")
#        s = s.replace("*", _("\\times "))
#        s = s.replace("/", _("\\div "))
        if not ls or s != ls[-1]:
            ls.append(s)
    return ls

def main():
    from sympy import Symbol, expand
    x = Symbol('x')
    test_entiers(nbval=13, polynomes=1, entiers=1)
#    a = valeurs(2, 1, 1)
#    a = 'Polynome([[8, 2]], "x")*Polynome([[3, 1]], "x")-Polynome([[-3, 0], [4, 2], [10, 1]], "x")*Polynome([[-4, 2], [5, 0], [-11, 1]], "x")-Polynome([[3, 2], [-5, 1]], "x")-(Polynome([[3, 2], [-1, 0]], "x")*Polynome([[3, 2], [1, 0]], "x")*Polynome([[-6, 2], [10, 1], [2, 0]], "x"))*Polynome([[-9, 0], [-7, 2], [8, 1]], "x")-Polynome([[-8, 1]], "x")+Polynome([[-8, 2], [4, 0]], "x")+Polynome([[10, 1]], "x")+Polynome([[-9, 2], [6, 1], [7, 0]], "x")'
#    print(a)
##    s= sympyfy([a])
#    print sympyfy(priorites(a))
#    r = texify(priorites(a))
#    print "\\item $A=", texify([a])[0] , "$\\par"
#    for i in r:
#        print "$A=",
#        print "".join(i),
#        print "$\\par"
