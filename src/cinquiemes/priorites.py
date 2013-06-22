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
#from ..outils import ecrit_tex, valeur_alea, signe, pgcd, ppcm

import random
import string

#
# -------------------  -------------------


def valeurs(nb, entier=1):  # renvoie les 2 listes contenant les opérateurs et les opérandes.
    listoperateurs = [
        '+',
        '*',
        '-',
        '/',
        '(',
        '(',
        '(',
        '(',
        ')',
        ')',
        ')',
        ')',
        ]
    loperateurs = []
    loperandes = []
    i = 0  #nombre d'opérateurs créés
    p = 0  #nombre de parenthèses ouvertes
    cpt = 0  #compteur pour éviter que le programme ne boucle.
    while i < nb - 1:
        cpt = cpt + 1
        if cpt > 10:  #On recommence
            (cpt, i, p, loperateurs) = (0, 0, 0, [])
        if p:
            if loperateurs[-1] == '(':  # On n'écrit pas 2 parenthèses à suivre
                operateur = listoperateurs[random.randrange(4)]
            else:
                operateur = listoperateurs[random.randrange(12)]
        elif loperateurs == []:

            # On ne commence pas par une parenthèse

            operateur = listoperateurs[random.randrange(4)]
        else:
            operateur = listoperateurs[random.randrange(8)]
        if nb > 3:
            test = ('-*/').find(operateur) >= 0 and \
                   loperateurs.count(operateur) < 1 or \
                   operateur == '+' and \
                   loperateurs.count(operateur) < 2
        else:
            test = ('-*/+').find(operateur) >= 0 and \
                   loperateurs.count(operateur) < 1
        if test:

            #On n'accepte pas plus de 1 produit, différence, quotient et de 2
            #sommes ou parenthèses par calcul.

            if i == 0 or loperateurs[-1] != '(' or ('*/').find(operateur) < \
                0:  #pas de * ou / dans une parenthèse.
                i = i + 1
                loperateurs.append(operateur)
        elif operateur == '(' and (')+').find(loperateurs[-1]) < 0:

            #Il ne peut y avoir de ( après une ) ou après un +

            p = p + 1
            loperateurs.append(operateur)
        elif operateur == ')':
            p = p - 1
            loperateurs.append(operateur)
    while p > 0:
        loperateurs.append(')')
        p = p - 1
    if entier:
        loperandes = [random.randrange(12) + 2 for i in range(nb)]
    else:
        loperandes = [((random.randrange(88) + 12) * 1.0) / 10 for i in
                      range(nb)]
    return (loperateurs, loperandes)


#######################


def affichage(loperateurs, loperandes):
    j = 0  #compteur des operateurs
    calcul = '%s' % nb_decimal((loperandes[0], ))
    for i in range(len(loperandes) - 1):
        if loperateurs[j] == ')':  #Il reste une opération mais je ferme d'abord une ou plusieurs parenthèses
            cpt = 1
            while loperateurs[j + cpt] == ')':
                cpt = cpt + 1  #j+cpt est la position de l'opération qui suit
        else:
            cpt = 0
        if j + cpt < len(loperateurs) - 1:  #Il reste au moins une opération, donc peut-etre une parenthèse ouvrante
            while loperateurs[j + cpt + 1] == '(':  #j+cpt est la position de la dernière parenthèse (
                cpt = cpt + 1
        for k in range(cpt + 1):
            calcul = calcul + '%s' % loperateurs[j + k]
        calcul = calcul + '%s' % nb_decimal((loperandes[i + 1], ))
        j = j + cpt + 1
    while j < len(loperateurs):
        calcul = calcul + '%s' % loperateurs[j]
        j = j + 1
    calcul = (_('\\times ')).join(calcul.split('*', 2))
    calcul = (_('\\div ')).join(calcul.split('/', 2))
    return calcul


def nb_decimal(a):  # verifie si des nombres décimaux dans le tuple a sont en fait des nombres entiers et change leur type
    list = []
    for i in range(len(a)):
        if str(a[i]).endswith('.0'):
            list.append(int(a[i] + .1))
        else:
            list.append(('{,}').join(str(a[i]).split('.', 2)))
    return tuple(list)


def verifie_calcul(listoperateurs, listoperandes, entier=1):

    #Vérifie que l'opération proposée est réalisable sans division
    # décimale ni nombre négatif

    p = 0
    loperateurs = listoperateurs[-1]
    loperandes = listoperandes[-1]
    if len(loperandes) == 1:
        return (listoperateurs, listoperandes)
    else:
        nbpar = loperateurs.count('(')
        nbmul = loperateurs.count('*')
        nbdiv = loperateurs.count('/')
        if nbpar:
            index = -1
            while p < nbpar:
                index = loperateurs[index + 1:].index('(') + index + 1
                p = p + 1
                if p < nbpar and loperateurs[index + 1:].index('(') > \
                    loperateurs[index + 1:].index(')'):
                    nbpar = p
            if loperateurs[index + 2] == ')':
                a = calcul(loperandes[(index + 1) - nbpar], loperateurs[index +
                           1], loperandes[(index + 2) - nbpar], entier)
                if a != 'hp':
                    al = loperateurs[:index]
                    al.extend(loperateurs[index + 3:])
                    loperateurs = al
                    al = loperandes[:(index + 1) - nbpar]
                    al.append(a)
                    al.extend(loperandes[index - nbpar + 3:])
                    loperandes = al
                    listoperateurs.append(loperateurs)
                    listoperandes.append(loperandes)
                    return verifie_calcul(listoperateurs, listoperandes)
        elif nbmul or nbdiv:
            (indexm, indexd) = (100, 100)
            if nbmul:
                indexm = loperateurs.index('*')
            if nbdiv:
                indexd = loperateurs.index('/')
            index = min(indexm, indexd)
            a = calcul(loperandes[index], loperateurs[index], loperandes[index +
                       1], entier)
            if a != 'hp':
                al = loperateurs[:index]
                al.extend(loperateurs[index + 1:])
                loperateurs = al
                al = loperandes[:index]
                al.append(a)
                al.extend(loperandes[index + 2:])
                loperandes = al
                listoperateurs.append(loperateurs)
                listoperandes.append(loperandes)
                return verifie_calcul(listoperateurs, listoperandes)
        else:
            a = calcul(loperandes[0], loperateurs[0], loperandes[1],
                       entier)
            if a != 'hp':
                loperateurs = loperateurs[1:]
                al = [a]
                al.extend(loperandes[2:])
                loperandes = al
                listoperateurs.append(loperateurs)
                listoperandes.append(loperandes)
                return verifie_calcul(listoperateurs, listoperandes)


def calcul(a, op, b, entier=1):  #retourne 'hp' (hors programme) ou le résultat de l'opération
    if op == '+':
        return a + b
    elif op == '*':
        return a * b
    elif op == '-':
        if a > b:
            return a - b
        else:
            return 'hp'
    else:
        if (a * 100) % (b * 100) and entier:
            return 'hp'
        elif not entier and (a * 1000) % (b * 100):
            return 'hp'
        else:
            return a / b


def main():
    nb = 9  # nombre de calculs
    exo = ["\\exercice",
           _(u"Calculer les expressions suivantes en détaillant les calculs.\n"),
           "\\begin{multicols}{3}", "\\noindent"]
    cor = ["\\exercice*",
           _(u"Calculer les expressions suivantes en détaillant les calculs."),
           "\\begin{multicols}{3}", "\\noindent"]
    i = 0
    while i < nb:
        if i < 3:  #Les 3 premiers calculs ne comportent que 3 nombres
            (loperateurs, loperandes) = valeurs(3)
        elif i > 6:
            (loperateurs, loperandes) = valeurs(5, 0)  #Les derniers calculs comportent des nombres décimaux
        else:
            (loperateurs, loperandes) = valeurs(6)

        if i > 6:
            list = verifie_calcul([loperateurs], [loperandes], entier=0)
        else:
            list = verifie_calcul([loperateurs], [loperandes], entier=1)
        if list != None:
            i = i + 1
            for j in range(len(list[0])):
                if j == 0:
                    exo.append("\\[ \\thenocalcul = %s \\]" %
                               affichage(list[0][j], list[1][j]))
                    exo.append('\\stepcounter{nocalcul}%')
                if j == len(list[0]) - 1:
                    cor.append("\\[ \\boxed{\\thenocalcul = %s} \\]" %
                               affichage(list[0][j], list[1][j]))
                    cor.append('\\stepcounter{nocalcul}%')
                else:
                    cor.append("\\[ \\thenocalcul = %s \\]" %
                               affichage(list[0][j], list[1][j]))
    exo.append("\\end{multicols}")
    cor.append("\\end{multicols}")
    return (exo, cor)
