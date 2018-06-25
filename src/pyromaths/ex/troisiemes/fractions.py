#!/usr/bin/env python3

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

from __future__ import unicode_literals
from builtins import range
from pyromaths.outils.Arithmetique import ppcm, pgcd, signe, valeur_alea
from random import randrange

#
# ------------------- FRACTIONS -------------------


def den_com0(a, b):  # renvoie un tuple contenant les 2 nombres par lesquels multiplier les deux denominateurs pour obtenir leur ppcm
    c = ppcm(a[1], b[1])
    return (abs(c // a[1]), abs(c // b[1]))


def den_com1(a, b):  # renvoie un tuple contenant les fractions a et b avec le meme denominateur
    c = den_com0(a, b)
    sgn1 = signe(a[1])
    sgn2 = signe(b[1])
    return (((a[0] * c[0]) * sgn1, (a[1] * c[0]) * sgn1), ((b[0] * c[1]) * 
            sgn2, (b[1] * c[1]) * sgn2))


def somme(a, b, sgn):  # renvoie un tuple contenant la somme des fractions a et b ayant pour denominateur le ppcm de leurs denominateurs
    c = den_com1(a, b)
    if sgn == '+':
        return (c[0][0] + c[1][0], c[0][1])
    else:
        return (c[0][0] - c[1][0], c[0][1])


def simplifie(a):  # renvoie la fraction a simplifiee
    b = pgcd(a[0], a[1])
    if b != 1:
        return (a[0] // b, a[1] // b)
    else:
        return ''


def decomp_prod(a, b):  # renvoie un tuple contenant les deux fractions apres simplification et un tuple contenant les nb par lesquels on

    # simplifie le produit de fractions

    c = pgcd(a[0], b[1])
    d = pgcd(a[1], b[0])
    sgn1 = signe(a[1])
    sgn2 = signe(b[1])
    if c == d == 1:
        return (((sgn1 * a[0]) // c, (sgn1 * a[1]) // d), ((sgn2 * b[0]) // 
                d, (sgn2 * b[1]) // c), '')
    else:
        return (((sgn1 * a[0]) // c, (sgn1 * a[1]) // d), ((sgn2 * b[0]) // 
                d, (sgn2 * b[1]) // c), (c, d))


def produit(a, b):  # renvoie un tuple contenant le produit des fractions a et b
    sgn1 = signe(a[1] * b[1])
    return ((sgn1 * a[0]) * b[0], (sgn1 * a[1]) * b[1])


def inverse(a):  # renvoie l'inverse de la fraction a
    sgn1 = signe(a[0])
    return (sgn1 * a[1], sgn1 * a[0])


def tex_frac(a):  # renvoie l'ecriture au format tex de la fraction a
    if not isinstance(a, tuple):
        return ''
    else:
        a = ((a[0] * a[1]) // abs(a[1]), abs(a[1]))
        if a[1] == 1:
            if abs(a[1]) >= 1000:
                return '\nombre{%i}' % a[0]
            else:
                return '%i' % a[0]
        else:
            if abs(a[0]) >= 1000:
                if abs(a[1]) >= 1000:
                    return '\cfrac{\\nombre{%s}}{\\nombre{%s}}' % a
                else:
                    return '\cfrac{\\nombre{%s}}{%s}' % a
            elif abs(a[1]) >= 1000:
                return '\cfrac{%s}{\\nombre{%s}}' % a
            else:
                return '\cfrac{%s}{%s}' % a


def OOo_frac(a):  # renvoie l'ecriture au format OOo de la fraction a
    if not isinstance(a, tuple):
        return ''
    else:
        if a[1] == 1:
            return a[0]
        else:
            return '{{%s} over {%s}}' % a


def tex_decomp_prod(a):  # renvoie l'ecriture au format tex de la decomposition d'un produit
    if not isinstance(a[2], tuple):  # pas de decomposition possible
        return ''
    elif a[2][0] == 1:

        # decomposition que du denominateur

        b = (a[0][0], a[0][1], a[2][1], a[1][0], a[2][1], a[1][1])
        return '\cfrac{%s}{%s\\times\\bcancel{%s}}\\times\\cfrac{%s\\times\\bcancel{%s}}{%s}' % \
            b
    elif a[2][1] == 1:
        b = (a[0][0], a[2][0], a[0][1], a[1][0], a[1][1], a[2][0])  # decomposition que du numerateur
        return '\cfrac{%s\\times\\cancel{%s}}{%s}\\times\\cfrac{%s}{%s\\times\\cancel{%s}}' % \
            b
    else:

        # decomposition du numerateur et du denominateur

        b = (a[0][0], a[2][0], a[0][1], a[2][1], a[1][0], a[2][1], a[1][1],
             a[2][0])
        return '\\cfrac{%s\\times\\cancel{%s}}{%s\\times\\bcancel{%s}}\\times\\cfrac{%s\\times\\bcancel{%s}}{%s\\times\\cancel{%s}}' % \
            b


def OOo_decomp_prod(a):  # renvoie l'ecriture au format OOo de la decomposition du produit
    if a[2][0] == 1:
        if a[2][1] == 1:  # pas de decomposition
            b = (a[0][0], a[2][1], a[1][0], a[1][1])
            return '{{%s}over{%s}}times{{%s}over{%s}}' % b
        else:

            # decomposition que du denominateur

            b = (a[0][0], a[0][1], a[2][1], a[1][0], a[2][1], a[1][1])
            return '{{%s}over{{%s}times overstrike{%s}}}times{{{%s}times overstrike{%s}}over{%s}}' % \
                b
    elif a[2][1] == 1:
        b = (a[0][0], a[2][0], a[0][1], a[1][0], a[1][1], a[2][0])  # decomposition que du numerateur
        return '{{{%s}times overstrike{%s}}over{%s}}times{{%s}over{{%s}times overstrike{%s}}}' % \
            b
    else:

        # decomposition du numerateur et du denominateur

        b = (a[0][0], a[2][0], a[0][1], a[2][1], a[1][0], a[2][1], a[1][1],
             a[2][0])
        return '{{{%s}times overstrike{%s}}over{{%s}times overstrike{%s}}}times{{{%s}times overstrike{%s}}over{{%s}times overstrike{%s}}}' % \
            b


def tex_den_com0(a, b, c, sgn):  # renvoie l'ecriture au format tex de la mise au meme denominateur des fraction a et b
    if not isinstance(c, tuple):  # les deux fractions ont deja le meme denominateur
        return ''
    else:
        (sgn1, sgn2) = (signe(a[1]), signe(b[1]))
        if c[0] == 1:
            if c[1] == 1:
                d = (a[0] * sgn1, a[1] * sgn1, b[0] * sgn2, b[1] * sgn2)
                return ''
            else:
                d = (a[0] * sgn1, a[1] * sgn1, sgn, b[0] * sgn2, c[1], b[1] * 
                     sgn2, c[1])
                return '\dfrac{%s}{%s}%s\\dfrac{%s_{\\times %s}}{%s_{\\times %s}}' % \
                    d
        elif c[1] == 1:
            d = (a[0] * sgn1, c[0], a[1] * sgn1, c[0], sgn, b[0] * sgn2,
                 b[1] * sgn2)
            return '\dfrac{%s_{\\times %s}}{%s_{\\times %s}}%s\\dfrac{%s}{%s}' % \
                d
        else:
            d = (
                a[0] * sgn1,
                c[0],
                a[1] * sgn1,
                c[0],
                sgn,
                b[0] * sgn2,
                c[1],
                b[1] * sgn2,
                c[1],
                )
            return '\dfrac{%s_{\\times %s}}{%s_{\\times %s}}%s\\dfrac{%s_{\\times %s}}{%s_{\\times %s}}' % \
                d


def tex_den_com1(a, sgn):  # renvoie l'ecriture au format tex de la somme des fractions au meme denominateur
    if not isinstance(a, tuple):  # les deux fractions ont deja le meme denominateur
        return ''
    else:
        (sgn1, sgn2) = (signe(a[0][1]), signe(a[1][1]))
        b = (a[0][0] * sgn1, a[0][1] * sgn1, sgn, a[1][0] * sgn2, a[1][1] * 
             sgn2)
        return '\dfrac{%s}{%s}%s\\dfrac{%s}{%s}' % b


def tex_somme_prod(valeurs, exo, cor):  # calcul du type a+b*c, d contenant (+,*)
    (a, b, c, d) = (valeurs[0], valeurs[1], valeurs[2], valeurs[3])
    if d[1] == '*':
        exo.append(u'\\[ \\thenocalcul = ' + tex_frac(a) + d[0] + tex_frac(b) + '\\times' + 
                  tex_frac(c) + '\\] ')
        cor.append(u'\\[ \\thenocalcul = ' + tex_frac(a) + d[0] + tex_frac(b) + '\\times' + 
                  tex_frac(c) + '\\] ')
        e = decomp_prod(b, c)
        if e[2] != '':
            cor.append(u'\\[ \\thenocalcul = ' + tex_frac(a) + d[0] + tex_decomp_prod(decomp_prod(b,
                      c)) + '\\] ')
    else:
        exo.append(u'\\[ \\thenocalcul = ' + tex_frac(a) + d[0] + tex_frac(b) + '\\div' + 
                  tex_frac(c) + '\\] ')
        cor.append(u'\\[ \\thenocalcul = ' + tex_frac(a) + d[0] + tex_frac(b) + '\\div' + 
                  tex_frac(c) + '\\] ')
        cor.append(u'\\[ \\thenocalcul = ' + tex_frac(a) + d[0] + tex_frac(b) + '\\times' + 
                  tex_frac(inverse(c)) + '\\] ')
        e = decomp_prod(b, inverse(c))
        if e[2] != '':
            cor.append(u'\\[ \\thenocalcul = ' + tex_frac(a) + d[0] + tex_decomp_prod(decomp_prod(b,
                      inverse(c))) + '\\] ')
    f = produit(e[0], e[1])
    cor.append(u'\\[ \\thenocalcul = ' + tex_frac(a) + d[0] + tex_frac(f) + '\\] ')
    cor.append(u'\\[ \\thenocalcul = ' + tex_den_com0(a, f, den_com0(a, f), d[0]) + '\\] ')
    cor.append(u'\\[ \\thenocalcul = ' + tex_den_com1(den_com1(a, f), d[0]) + '\\] ')
    g = somme(a, f, d[0])
    if isinstance(simplifie(g), tuple):
        cor.append(u'\\[ \\thenocalcul = ' + tex_frac(g) + '\\] ')
        cor.append(u'\\[ \\boxed{\\thenocalcul = ' + tex_frac(simplifie(g)) + '} \\] ')
    else:
        cor.append(u'\\[ \\boxed{\\thenocalcul = ' + tex_frac(g) + '} \\] ')


def tex_prod_parenth(valeurs, exo, cor):  # calcul du type a*(b+c), d contenant (*,+)
    (a, b, c, d) = (valeurs[0], valeurs[1], valeurs[2], valeurs[3])
    if d[0] == '*':
        exo.append(u'\\[ \\thenocalcul = ' + tex_frac(a) + '\\times\\left(' + tex_frac(b) + d[1] + 
                  tex_frac(c) + '\\right) \\] ')
        cor.append(u'\\[ \\thenocalcul = ' + tex_frac(a) + '\\times\\left(' + tex_frac(b) + d[1] + 
                  tex_frac(c) + '\\right) \\] ')
        if isinstance(den_com0(b, c), tuple):
            cor.append(u'\\[ \\thenocalcul = ' + tex_frac(a) + '\\times\\left(' + tex_den_com0(b,
                      c, den_com0(b, c), d[1]) + '\\right) \\] ')
            cor.append(u'\\[ \\thenocalcul = ' + tex_frac(a) + '\\times\\left(' + tex_den_com1(den_com1(b,
                      c), d[1]) + '\\right) \\] ')
        cor.append(u'\\[ \\thenocalcul = ' + tex_frac(a) + '\\times' + tex_frac(somme(b, c, d[1])) + '\\] ')
        if isinstance(simplifie(somme(b, c, d[1])), tuple):
            e = simplifie(somme(b, c, d[1]))
            cor.append(u'\\[ \\thenocalcul = ' + tex_frac(a) + '\\times' + tex_frac(e) + '\\] ')
        else:
            e = somme(b, c, d[1])
    else:
        exo.append(u'\\[ \\thenocalcul = ' + tex_frac(a) + '\\div\\left(' + tex_frac(b) + d[1] + 
                  tex_frac(c) + '\\right) \\] ')
        cor.append(u'\\[ \\thenocalcul = ' + tex_frac(a) + '\\div\\left(' + tex_frac(b) + d[1] + 
                  tex_frac(c) + '\\right) \\] ')
        if isinstance(den_com0(b, c), tuple):
            cor.append(u'\\[ \\thenocalcul = ' + tex_frac(a) + '\\div\\left(' + tex_den_com0(b,
                      c, den_com0(b, c), d[1]) + '\\right) \\] ')
            cor.append(u'\\[ \\thenocalcul = ' + tex_frac(a) + '\\div\\left(' + tex_den_com1(den_com1(b,
                      c), d[1]) + '\\right) \\] ')
        cor.append(u'\\[ \\thenocalcul = ' + tex_frac(a) + '\\div' + tex_frac(somme(b, c, d[1])) + '\\] ')
        if isinstance(simplifie(somme(b, c, d[1])), tuple):
            e = simplifie(inverse(somme(b, c, d[1])))
            cor.append(u'\\[ \\thenocalcul = ' + tex_frac(a) + '\\div' + tex_frac(inverse(e)) + '\\] ')
        else:
            e = inverse(somme(b, c, d[1]))
        cor.append(u'\\[ \\thenocalcul = ' + tex_frac(a) + '\\times' + tex_frac(e) + '\\] ')
    f = decomp_prod(a, e)
    cor.append(u'\\[ \\thenocalcul = ' + tex_decomp_prod(f) + '\\] ')
    if isinstance(simplifie(produit(f[0], f[1])), tuple):
        cor.append(u'\\[ \\thenocalcul = ' + tex_frac(produit(f[0], f[1])) + '\\] ')
        cor.append(u'\\[ \\boxed{\\thenocalcul = ' + tex_frac(simplifie(produit(f[0], f[1]))) + '} \\] ')
    else:
        cor.append(u'\\[ \\boxed{\\thenocalcul = ' + tex_frac(produit(f[0], f[1])) + '} \\] ')


def tex_quotient_frac(valeurs, exo, cor):  # effectue le quotient {a+b}/{c+d}, e contenant (+,+)
    (a, b, c, d, e) = (valeurs[0], valeurs[1], valeurs[2], valeurs[3],
                       valeurs[4])
    exo.append(u'\\[ \\thenocalcul = \cfrac{' + tex_frac(a) + e[0] + tex_frac(b) + '}{' + 
              tex_frac(c) + e[1] + tex_frac(d) + '} \\] ')
    cor.append(u'\\[ \\thenocalcul =  \cfrac{' + tex_frac(a) + e[0] + tex_frac(b) + '}{' + 
              tex_frac(c) + e[1] + tex_frac(d) + '} \\] ')
    cor.append(u'\\[ \\thenocalcul = \cfrac{' + tex_den_com0(a, b, den_com0(a, b), e[0]) + 
              '}{' + tex_den_com0(c, d, den_com0(c, d), e[1]) + '} \\] ')
    cor.append(u'\\[ \\thenocalcul = \cfrac{' + tex_den_com1(den_com1(a, b), e[0]) + '}{' + 
              tex_den_com1(den_com1(c, d), e[1]) + '} \\] ')

    # ecrit_tex(f1,'\\cfrac{'+tex_frac(somme(a,b,e[0]))+'}{'+tex_frac(somme(c,d,e[1]))+'}')

    cor.append(u'\\[ \\thenocalcul = ' + tex_frac(somme(a, b, e[0])) + '\\div' + tex_frac(somme(c,
              d, e[1])) + ' \\] ')
    cor.append(u'\\[ \\thenocalcul = ' + tex_frac(somme(a, b, e[0])) + '\\times' + tex_frac(inverse(somme(c,
              d, e[1]))) + ' \\] ')
    f = decomp_prod(somme(a, b, e[0]), inverse(somme(c, d, e[1])))
    cor.append(u'\\[ \\thenocalcul = ' + tex_decomp_prod(f) + ' \\] ')
    if isinstance(simplifie(produit(f[0], f[1])), tuple):
        cor.append(u'\\[ \\thenocalcul = ' + tex_frac(produit(f[0], f[1])) + ' \\] ')
        cor.append(u'\\[ \\boxed{\\thenocalcul = ' + tex_frac(simplifie(produit(f[0], f[1]))) + '} \\] ')
    else:
        cor.append(u'\\[ \\boxed{\\thenocalcul = ' + tex_frac(produit(f[0], f[1])) + '} \\] ')


def valeurs_somme_prod():  # cree 3 fractions et un tuple de signes (+,*)
    while True:
        (base1, base2) = (valeur_alea(-13, 13), valeur_alea(-13, 13))
        lepgcd = pgcd(base1, base2)
        (base1, base2) = (base1 // lepgcd, base2 // lepgcd)
        if base1 != 1 and base2 != 1:
            break
    (n2, d2) = (base1 * valeur_alea(-10, 10), abs(base2 * valeur_alea(2,
                10)))
    lepgcd = pgcd(n2, d2)
    (n2, d2) = (n2 // lepgcd, d2 // lepgcd)
    (n3, d3) = (base2 * valeur_alea(-10, 10), abs(base1 * valeur_alea(2,
                10)))
    lepgcd = pgcd(n3, d3)
    (n3, d3) = (n3 // lepgcd, d3 // lepgcd)
    (n1, d1) = (base1 * valeur_alea(-10, 10), abs(pgcd(d2, base2 * 
                valeur_alea(2, 10))))
    lepgcd = pgcd(n1, d1)
    (n1, d1) = (n1 // lepgcd, d1 // lepgcd)
    if randrange(2) == 0:
        s1 = '+'
    else:
        s1 = '-'
    if randrange(2) == 0:
        s2 = '*'
    else:
        s2 = ':'
    if s2 == '*':
        return ((n1, d1), (n2, d2), (n3, d3), (s1, s2))
    else:
        return ((n1, d1), (n2, d2), (d3, n3), (s1, s2))


def valeurs_prod_parenth():  # cree 3 fractions et un tuple de signes (*,+)
    while True:
        (base1, base2) = (valeur_alea(2, 13), valeur_alea(2, 13))
        lepgcd = pgcd(base1, base2)
        (base1, base2) = (base1 // lepgcd, base2 // lepgcd)
        if base1 != 1 and base2 != 1:
            break
    while True:
        n2 = valeur_alea(-13, 13)
        lepgcd = pgcd(n2, base1)
        if lepgcd == 1:
            break
    while True:
        n3 = valeur_alea(-13, 13)
        lepgcd = pgcd(n3, base2)
        if lepgcd == 1:
            break
    while True:
        (n1, d1) = (valeur_alea(-10, 10), valeur_alea(2, 10))
        lepgcd = pgcd(n1, d1)
        if lepgcd != n1 and lepgcd != d1:
            break
    (n1, d1) = (n1 // lepgcd, d1 // lepgcd)
    if randrange(2) == 0:
        s1 = '*'
    else:
        s1 = ':'
    if randrange(2) == 0:
        s2 = '+'
    else:
        s2 = '-'
    return ((n1, d1), (n2, base1), (n3, base2), (s1, s2))


def valeurs_quotient_frac():  # cree 4 fractions et un tuple de signes (+,+)
    while True:
        (n1, d1) = (valeur_alea(-10, 10), valeur_alea(2, 10))
        lepgcd = pgcd(n1, d1)
        if lepgcd != n1 and lepgcd != d1:
            break
    (n1, d1) = (n1 // lepgcd, d1 // lepgcd)
    while True:
        (n3, d3) = (valeur_alea(-10, 10), valeur_alea(2, 10))
        lepgcd = pgcd(n3, d3)
        if lepgcd != n3 and lepgcd != d3:
            break
    (n3, d3) = (n3 // lepgcd, d3 // lepgcd)
    (n2, n4) = (valeur_alea(1, 10), valeur_alea(1, 10))
    if randrange(2) == 0:
        s1 = '+'
    else:
        s1 = '-'
    if randrange(2) == 0:
        s2 = '+'
    else:
        s2 = '-'
    return ((n1, d1), (n2, 1), (n3, d3), (n4, 1), (s1, s2))


def tex_fractions():
    nb_exos = 3
    tex_exos = (tex_somme_prod,
                tex_prod_parenth,
                tex_quotient_frac)
    valeurs_exos = (valeurs_somme_prod,
                    valeurs_prod_parenth,
                    valeurs_quotient_frac)
    ordre_exos = [i for i in range(nb_exos)]
    exo = ['''\n\\exercice''', u"Calculer les expressions suivantes et donner le résultat sous la forme d'une fraction irréductible."]
    exo.append('\\begin{multicols}{3}\\noindent')
    cor = ['''\\exercice*''', u"Calculer les expressions suivantes et donner le résultat sous la forme d'une fraction irréductible."]
    cor.append('\\begin{multicols}{3}\\noindent')
    for i in range(nb_exos):
        a = randrange(nb_exos - i)
        tex_exos[ordre_exos[a]](valeurs_exos[ordre_exos.pop(a)](), exo, cor)
        if i < nb_exos - 1:
            exo.append('\\columnbreak\\stepcounter{nocalcul}')
            cor.append('\\columnbreak\\stepcounter{nocalcul}')
        else:
            exo.append('\\end{multicols}')
            cor.append('\\end{multicols}')
    return (exo, cor)

tex_fractions.description = u'Fractions'
