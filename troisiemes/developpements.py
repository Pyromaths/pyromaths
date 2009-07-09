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

from fractions import tex_frac, simplifie, tex_decomp_prod, decomp_prod, \
    produit, den_com0
from outils import ecrit_tex, valeur_alea, signe, pgcd
import random

#
# ------------------- DEVELOPPEMENTS -------------------


def coef_opposes(a):  # renvoie un tuple dont les valeurs sont les opposees de celles de a
    l = []
    for i in xrange(len(a)):
        l.append(-a[i])
    return tuple(l)


def dev(a):  # renvoi un tuple avec les 3 coefficients du developpement
    return (a[0][0] * a[1][0], a[0][0] * a[1][1] + a[0][1] * a[1][0], a[0][1] *
            a[1][1])


def somme_polynomes(a, b):  # renvoie un tuple dont les valeurs sont les sommes des valeurs correspondantes dans a et b
    l = []
    if len(a) > len(b):
        long = len(a)
    else:
        long = len(b)
    for i in xrange(long):
        if (len(a) - i) - 1 < 0:
            l.append(b[(len(b) - 1) - i])
        elif (len(b) - i) - 1 < 0:
            l.append(a[(len(a) - 1) - i])
        else:
            l.append(a[(len(a) - 1) - i] + b[(len(b) - 1) - i])
    l.reverse()
    return tuple(l)


def tex_coef(coef, var, bplus=0, bpn=0, bpc=0):

    # coef est le coefficient à écrire devant la variable var
    # bplus est un booleen : s'il est vrai, il faut ecrire le signe +
    # bpn est un booleen : s'il est vrai, il faut mettre des parentheses autour de l'ecriture si coef est negatif.
    # bpc est un booleen : s'il est vrai, il faut mettre des parentheses autour de l'ecriture si coef =! 0 ou 1 et var est non vide

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


def tex_dev0(a, bplus=0):  # renvoi (a+b)², (a-b)² ou (a+b)(c+d) ou a(c+d) ou (a+b)*c

    # a est de la forme ((3, 2), (3, 2)) pour (3x+2)(3x+2)

    (ca, cb, cc, cd) = (a[0][0], a[0][1], a[1][0], a[1][1])  # coefficients a, b, c et d
    if ca == 0 and cb == 0 or cc == 0 and cd == 0:
        return '0'
    elif a[0] == a[1]:

                        # (a+b)² ou (a-b)²

        if ca == 0:
            return '%s^2' % tex_coef(cb, '', bpn=1)
        elif cb == 0:
            return '%s^2' % tex_coef(ca, 'x', bpc=1)
        else:
            return '(%s%s)^2' % (tex_coef(ca, 'x'), tex_coef(cb, '',
                                 bplus=1))
    else:

        # (a+b)(c+d)

        if ca == 0 or cb == 0:
            if cc == 0 or cd == 0:
                return '%s%s\\times %s%s' % (tex_coef(ca, 'x'), tex_coef(cb,
                        '', bplus=ca != 0), tex_coef(cc, 'x', bpn=1),
                        tex_coef(cd, '', bplus=cc != 0, bpn=1))
            else:
                return '%s%s\\,(%s%s)' % (tex_coef(ca, 'x'), tex_coef(cb,
                        '', bplus=ca != 0), tex_coef(cc, 'x'), tex_coef(cd,
                        '', bplus=cc != 0))
        elif cc == 0 or cd == 0:
            if cc == 0 and cd == 1:
                return '%s%s' % (tex_coef(ca, 'x', bplus=bplus),
                                 tex_coef(cb, '', bplus=ca != 0))
            else:
                return '(%s%s)\\times %s%s' % (tex_coef(ca, 'x'),
                        tex_coef(cb, '', bplus=ca != 0), tex_coef(cc,
                        'x', bpn=1), tex_coef(cd, '', bplus=cc != 0, bpn=
                        1))
        else:
            return '(%s%s)\\,(%s%s)' % (tex_coef(ca, 'x'), tex_coef(cb,
                    '', bplus=1), tex_coef(cc, 'x'), tex_coef(cd, '',
                    bplus=1))


def tex_dev1(a, bplus=0, bpar=0, bpn=0):  # renvoi le developpement (a)²+2*a*b+(b)², (a)²-2*a*b+(b)², (a)²-(b)² ou a*c+a*d+b*c+b*d

    # a est de la forme ((3, 2)(3, 2)) pour (3x+2)(3x+2)

    (ca, cb, cc, cd) = (a[0][0], a[0][1], a[1][0], a[1][1])  # coefficients a, b, c et d
    if a[0] == a[1]:  # (a+b)² ou (a-b)²
        if signe(ca) == signe(cb):  # (a+b)²
            (ca, cb) = (abs(ca), abs(cb))
            texte = '%s^2+2\\times %s\\times %s+%s^2' % (tex_coef(ca,
                    'x', bpc=1), tex_coef(ca, 'x', bpn=1), tex_coef(cb,
                    '', bpn=1), tex_coef(cb, '', bpn=1, bpc=1))
            if bpar:
                return '(' + texte + ')'
            else:
                return texte
        else:

            # (a-b)²

            (ca, cb) = (abs(ca), abs(cb))
            texte = '%s^2-2\\times %s\\times %s+%s^2' % (tex_coef(ca,
                    'x', bpc=1), tex_coef(ca, 'x', bpn=1), tex_coef(cb,
                    '', bpn=1), tex_coef(cb, '', bpn=1, bpc=1))
            if bpar:
                return '(' + texte + ')'
            else:
                return texte
    if abs(ca) == abs(cc) and abs(cb) == abs(cd):  # (a+b)(a-b) ou (a+b)(-a+b)
        if ca == cc:  # (a+b)(a-b)
            texte = '%s^2-%s^2' % (tex_coef(ca, 'x', bpc=1), tex_coef(abs(cb),
                                   ''))
            if bpar:
                return '(' + texte + ')'
            else:
                return texte
        else:

            # (a+b)(-a+b)

            texte = '%s^2-%s^2' % (tex_coef(cb, '', bpn=1), tex_coef(abs(ca),
                                   'x', bpc=1))
            if bpar:
                return '(' + texte + ')'
            else:
                return texte
    else:

        # (a+b)(c+d)

        if cc == 0 and cd == 1:
            texte = '%s%s' % (tex_coef(ca, 'x', bplus=bplus), tex_coef(cb,
                              '', bplus=ca != 0))
            if bpar:
                return '(' + texte + ')'
            else:
                return texte
        else:
            texte = '%s+%s+%s+%s' % (tex_coef(ca * cc, 'x^2', bpn=bpn),
                    tex_coef(ca * cd, 'x', bpn=1), tex_coef(cb * cc, 'x',
                    bpn=1), tex_coef(cb * cd, '', bpn=1))
            if bpar:
                return '(' + texte + ')'
            else:
                return texte


def tex_developpe1(a, f0, f1):  # developpe l'expression a
    ecrit_tex(f0, tex_dev0(a), tabs=2)
    ecrit_tex(f1, tex_dev0(a), tabs=2)
    ecrit_tex(f1, tex_dev1(a), tabs=2)
    ecrit_tex(f1, tex_trinome(dev(a)), cadre=True, tabs=2)


def tex_developpe2(a, nega, b, negb, f1, f0=None, tabs=1):  # developpe l'expression a plus l'expression b.
    if nega:
        if negb:
            if b[1][0] == 0 and b[1][1] == 1:
                if f0:
                    ecrit_tex(f0, '-' + tex_dev0(a) + '-(' + tex_dev0(b) +
                              ')', tabs=2)
                ecrit_tex(f1, '-' + tex_dev0(a) + '-(' + tex_dev0(b) +
                          ')', tabs=tabs)
            elif a[1][0] == 0 and a[1][1] == 1:
                if f0:
                    ecrit_tex(f0, '-(' + tex_dev0(a) + ')-' + tex_dev0(b),
                              tabs=2)
                ecrit_tex(f1, '-(' + tex_dev0(a) + ')-' + tex_dev0(b),
                          tabs=tabs)
            else:
                if f0:
                    ecrit_tex(f0, '-' + tex_dev0(a) + '-' + tex_dev0(b),
                              tabs=2)
                ecrit_tex(f1, '-' + tex_dev0(a) + '-' + tex_dev0(b),
                          tabs=tabs)
            ecrit_tex(f1, '-(' + tex_dev1(a) + ')-(' + tex_dev1(b) + ')',
                      tabs=tabs)
            ecrit_tex(f1, '-(' + tex_trinome(dev(a)) + ')-(' +
                      tex_trinome(dev(b)) + ')', tabs=tabs)
            ecrit_tex(f1, tex_trinome(coef_opposes(dev(a))) +
                      tex_trinome(coef_opposes(dev(b)), bplus=1), tabs=
                      tabs)
            ecrit_tex(f1, tex_trinome(somme_polynomes(coef_opposes(dev(a)),
                      coef_opposes(dev(b)))), cadre=True, tabs=tabs)
        else:
            if a[1][0] == 0 and a[1][1] == 1:
                if f0:
                    ecrit_tex(f0, '-(' + tex_dev0(a) + ')+' + tex_dev0(b),
                              tabs=2)
                ecrit_tex(f1, '-(' + tex_dev0(a) + ')+' + tex_dev0(b),
                          tabs=tabs)
                ecrit_tex(f1, '-(' + tex_dev1(a) + ')+' + tex_dev1(b,
                          bpn=1), tabs=tabs)
                ecrit_tex(f1, '-(' + tex_trinome(dev(a)) + ')+' +
                          tex_trinome(dev(b)), tabs=tabs)
            elif b[1][0] == 0 and b[1][1] == 1:
                if f0:
                    ecrit_tex(f0, '-' + tex_dev0(a) + tex_dev0(b, bplus=
                              1), tabs=2)
                ecrit_tex(f1, '-' + tex_dev0(a) + tex_dev0(b, bplus=1),
                          tabs=tabs)
                ecrit_tex(f1, '-(' + tex_dev1(a) + ')' + tex_dev1(b,
                          bplus=1), tabs=tabs)
                ecrit_tex(f1, '-(' + tex_trinome(dev(a)) + ')' +
                          tex_trinome(dev(b), bplus=1), tabs=tabs)
            else:
                if f0:
                    ecrit_tex(f0, '-' + tex_dev0(a) + '+' + tex_dev0(b),
                              tabs=2)
                ecrit_tex(f1, '-' + tex_dev0(a) + '+' + tex_dev0(b),
                          tabs=tabs)
                ecrit_tex(f1, '-(' + tex_dev1(a) + ')+' + tex_dev1(b,
                          bpn=1), tabs=tabs)
                ecrit_tex(f1, '-(' + tex_trinome(dev(a)) + ')' +
                          tex_trinome(dev(b), bplus=1), tabs=tabs)
            ecrit_tex(f1, tex_trinome(coef_opposes(dev(a))) +
                      tex_trinome(dev(b), bplus=1), tabs=tabs)
            ecrit_tex(f1, tex_trinome(somme_polynomes(coef_opposes(dev(a)),
                      dev(b))), cadre=True, tabs=tabs)
    elif negb:
        if b[1][0] == 0 and b[1][1] == 1:
            if f0:
                ecrit_tex(f0, tex_dev0(a) + '-(' + tex_dev0(b) + ')',
                          tabs=2)
            ecrit_tex(f1, tex_dev0(a) + '-(' + tex_dev0(b) + ')', tabs=
                      tabs)
        else:
            if f0:
                ecrit_tex(f0, tex_dev0(a) + '-' + tex_dev0(b), tabs=2)
            ecrit_tex(f1, tex_dev0(a) + '-' + tex_dev0(b), tabs=tabs)
        ecrit_tex(f1, tex_dev1(a) + '-(' + tex_dev1(b) + ')', tabs=tabs)
        ecrit_tex(f1, tex_trinome(dev(a)) + '-(' + tex_trinome(dev(b)) +
                  ')', tabs=tabs)
        ecrit_tex(f1, tex_trinome(dev(a)) + tex_trinome(coef_opposes(dev(b)),
                  bplus=1), tabs=tabs)
        ecrit_tex(f1, tex_trinome(somme_polynomes(dev(a), coef_opposes(dev(b)))),
                  cadre=True, tabs=tabs)
    else:
        if b[1][0] == 0 and b[1][1] == 1:
            if f0:
                ecrit_tex(f0, tex_dev0(a) + tex_dev0(b, bplus=1), tabs=2)
            ecrit_tex(f1, tex_dev0(a) + tex_dev0(b, bplus=1), tabs=tabs)
            ecrit_tex(f1, tex_dev1(a) + tex_dev1(b, bplus=1), tabs=tabs)
        else:
            if f0:
                ecrit_tex(f0, tex_dev0(a) + '+' + tex_dev0(b), tabs=2)
            ecrit_tex(f1, tex_dev0(a) + '+' + tex_dev0(b), tabs=tabs)
            ecrit_tex(f1, tex_dev1(a) + '+' + tex_dev1(b), tabs=tabs)
        ecrit_tex(f1, tex_trinome(dev(a)) + tex_trinome(dev(b), bplus=1),
                  tabs=tabs)
        ecrit_tex(f1, tex_trinome(somme_polynomes(dev(a), dev(b))),
                  cadre=True, tabs=tabs)


def tex_trinome(a, bplus=0, bpar=0):  # renvoi le trinome ax²+bx+c

    # bplus est un booleen : s'il est vrai, le premier terme est precede d'un signe + si son coefficient est positif.
    # bpar est un booleen : s'il est vrai, ecrit des parentheses autour du trinome si deux valeurs au moins ne sont pas nulles ou si la valeur est -

    texte = '%s%s%s' % (tex_coef(a[0], 'x^2', bplus=bplus), tex_coef(a[1],
                        'x', bplus=bplus or a[0] != 0), tex_coef(a[2],
                        '', bplus=bplus or a[0] != 0 or a[1] != 0))
    if bpar:
        v0 = 0
        for i in xrange(3):  # compte le nombre de valeurs nulles
            if a[i] == 0:
                v0 = v0 + 1
        if v0 == 2:  # une seule valeur non nulle (on suppose que les trois coef ne sont pas nuls)
            if a[0] < 0 or a[1] < 0 or a[2] < 0:  # le coefficient non nul est negatif, il faut donc des parentheses
                return '(' + texte + ')'
            else:
                return texte
        else:
            return '(' + texte + ')'
    else:
        return texte


def valeurs_apb2(pyromax):  # renvoie un tuple contenant ((3,5),(3,5))
    a = valeur_alea(1, pyromax)
    b = valeur_alea(1, pyromax)
    return ((a, b), (a, b))


def valeurs_amb2(pyromax):  # renvoie un tuple contenant ((3,-5),(3,-5))
    a = valeur_alea(1, pyromax)
    b = valeur_alea(-pyromax, -1)
    return ((a, b), (a, b))


def valeurs_apbamb(pyromax):  # renvoie un tuple contenant ((3,-5),(3,+5))
    a = valeur_alea(1, pyromax)
    b = valeur_alea(1, pyromax)
    if random.randrange(2):
        return ((a, -b), (a, b))
    else:
        return ((a, b), (a, -b))


def valeurs_distr(pyromax):

    # renvoie in tuple contenant ((a,b),(c,d)) avec a != c ou b != d (en valeur
    # absolue)

    a = valeur_alea(-pyromax, pyromax)
    b = valeur_alea(-pyromax, pyromax)
    c = valeur_alea(-pyromax, pyromax)
    d = valeur_alea(-pyromax, pyromax)
    while abs(a) == abs(c) and abs(b) == abs(d):
        c = valeur_alea(-pyromax, pyromax)
        d = valeur_alea(-pyromax, pyromax)
    return ((a, b), (c, d))


#
# ------------------- FACTORISATIONS -------------------


def facteur_commun(a, b):  #renvoie le facteur commun et les les deux autres binomes
    if a[0] == b[0]:  # recherche le facteur commun et le nomme f0, f1 et f2 etant les deux autres facteurs
        (f0, f1, f2) = (a[0], a[1], b[1])
    elif a[0] == b[1]:
        (f0, f1, f2) = (a[0], a[1], b[0])
    elif a[1] == b[0]:
        (f0, f1, f2) = (a[1], a[0], b[1])
    elif a[1] == b[1]:
        (f0, f1, f2) = (a[1], a[0], b[0])
    return (f0, f1, f2)


def facteur_commun2(f, nega, negb):  # renvoie (2x+3)(4x+5+6x+7) sous la forme ((2,3),(4,5),(6,7))
    if nega:
        if negb:
            return (f[0], coef_opposes(f[1]), coef_opposes(f[2]))
        else:
            return (f[0], coef_opposes(f[1]), f[2])
    elif negb:
        return (f[0], f[1], coef_opposes(f[2]))
    else:
        return (f[0], f[1], f[2])


def facteur_commun3(f, nega, negb):  # renvoie un tuple contenant les deux binomes finaux de la mise en facteur
    if nega and negb:
        return (f[0], somme_polynomes(coef_opposes(f[1]), coef_opposes(f[2])))
    elif nega:
        return (f[0], somme_polynomes(coef_opposes(f[1]), f[2]))
    elif negb:
        return (f[0], somme_polynomes(f[1], coef_opposes(f[2])))
    else:
        return (f[0], somme_polynomes(f[1], f[2]))


def tex_binome(a, bplus=0, bpar=0):  # renvoi le binome ax+b

    # bplus est un booleen : s'il est vrai, le premier terme est precede d'un signe + si son coefficient est positif.
    # bpar est un booleen : s'il est vrai, ecrit des parentheses autour du binome si les deux coef ne sont pas nuls ou si le seul coef est -

    texte = '%s%s' % (tex_coef(a[0], 'x', bplus=bplus), tex_coef(a[1],
                      '', bplus=bplus or a[0] != 0))
    if bpar:
        if (a[0] != 0 or a[1] < 0) and (a[1] != 0 or a[0] < 0):
            texte = '(' + texte + ')'
    return texte


def tex_trinome_alea(a, bplus=0):  # renvoi le trinome ax²+bx+c dans le desordre
    valeurs = [tex_coef(a[0], 'x^2', bplus=1), tex_coef(a[1], 'x', bplus=
               1), tex_coef(a[2], '', bplus=1)]
    ordre1 = []
    while ordre1 == [] or ordre1 == [0, 1, 2]:
        ordre0 = [i for i in xrange(3)]
        ordre1 = [ordre0.pop(random.randrange(3 - i)) for i in xrange(3)]
    liste = [valeurs[ordre1[i]] for i in xrange(3)]
    if not bplus and liste[0].startswith('+'):
        liste[0] = liste[0].replace('+', '', 1)
    return '%s%s%s' % tuple(liste)


def tex_facteur_commun0(a):  #renvoie -(2x+3)(x+5)+(2x+3)(3x+6)
    if a[2]:
        if a[3]:
            return '-' + tex_dev0(a[0]) + '-' + tex_dev0(a[1])
        else:
            return '-' + tex_dev0(a[0]) + '+' + tex_dev0(a[1])
    elif a[3]:
        return tex_dev0(a[0]) + '-' + tex_dev0(a[1])
    else:
        return tex_dev0(a[0]) + '+' + tex_dev0(a[1])


def tex_facteur_commun1(f, nega, negb):  # renvoie (2x+3)(-(x+5)+3x+6)
    texte = tex_binome(f[0], bpar=1)
    if nega or negb:
        texte = texte + '\\,\\big( '
    else:
        texte = texte + '\\,('
    if nega:
        texte = texte + '-' + tex_binome(f[1], bpar=1)
    else:
        texte = texte + tex_binome(f[1], bpar=0)
    if negb:
        texte = texte + '-' + tex_binome(f[2], bpar=1)
    else:
        texte = texte + tex_binome(f[2], bplus=1)
    if nega or negb:
        texte = texte + '\\big)'
    else:
        texte = texte + ')'
    return texte


def tex_facteur_commun2(a):  # renvoie renvoie (2x+3)(-x-5+3x+6)
    return tex_binome(a[0], bpar=1) + '\\,(' + tex_binome(a[1]) + \
        tex_binome(a[2], bplus=1) + ')'


def tex_a2moinsb2_0(a):  # renvoie 16-(2x+3)²
    if a[0][0] == 0:
        return '%s-%s^2' % (a[0][1] ** 2, tex_binome(a[1], bpar=1))
    else:
        return '%s^2-%s' % (tex_binome(a[0], bpar=1), a[1][1] ** 2)


def tex_a2moinsb2_2(a):  # renvoie (4+2x+3)(4-(2x+3))
    if a[0][0] == 0:
        return '(%s%s)\\,\\big( %s-%s\\big)' % (tex_binome(a[0]),
                tex_binome(a[1], bplus=1), tex_binome(a[0]), tex_binome(a[1],
                bpar=1))
    else:
        return '(%s%s)\\,(%s-%s)' % (tex_binome(a[0]), tex_binome(a[1],
                bplus=1), tex_binome(a[0]), tex_binome(a[1], bpar=1))


def tex_a2moinsb2_3(a):  # renvoie (4+2x+3)(4-2x-3)
    if a[0][0] == 0:
        return '(%s%s)\\,(%s%s)' % (tex_binome(a[0]), tex_binome(a[1],
                                    bplus=1), tex_binome(a[0]),
                                    tex_binome(coef_opposes(a[1]), bplus=
                                    1))
    else:
        return ''


def tex_facteur_commun(valeurs, f1, f0=None):  # ecrit toutes les etapes de la factorisation
    (a, b, nega, negb) = valeurs
    f = facteur_commun(a, b)
    if f0:
        ecrit_tex(f0, tex_facteur_commun0(valeurs), tabs=2)
    ecrit_tex(f1, tex_facteur_commun0(valeurs), tabs=2)
    ecrit_tex(f1, tex_facteur_commun1(f, nega, negb), tabs=2)
    f2 = facteur_commun2(f, nega, negb)
    if nega and f2[1][0] != 0 and f2[1][1] != 0 or negb and f2[2][0] != \
        0 and f2[2][0] != 0:
        ecrit_tex(f1, tex_facteur_commun2(f2), tabs=2)
    ecrit_tex(f1, tex_dev0((f2[0], somme_polynomes(f2[1], f2[2]))),
              cadre=True, tabs=2)


def tex_a2moinsb2(valeurs, f1, f0):  # ecrit toutes les etapes de la factorisation
    if f0:
        ecrit_tex(f0, tex_a2moinsb2_0(valeurs), tabs=2)
    ecrit_tex(f1, tex_a2moinsb2_0(valeurs), tabs=2)
    ecrit_tex(f1, '%s^2-%s^2' % (tex_binome(valeurs[0], bpar=1),
              tex_binome(valeurs[1], bpar=1)), tabs=2)
    ecrit_tex(f1, tex_a2moinsb2_2(valeurs), tabs=2)
    ecrit_tex(f1, tex_a2moinsb2_3(valeurs), tabs=2)
    ecrit_tex(f1, tex_dev0((somme_polynomes(valeurs[0], valeurs[1]),
              somme_polynomes(valeurs[0], coef_opposes(valeurs[1])))),
              cadre=True, tabs=2)


def valeurs_facteur_commun(pyromax):  # renvoie les valeurs pour obtenir un facteur commun.
    a = ((valeur_alea(-pyromax, pyromax), valeur_alea(-pyromax, pyromax)),
         (valeur_alea(-pyromax, pyromax), valeur_alea(-pyromax, pyromax)))
    while a[0] == a[1]:  # on refuse un carre
        a = ((valeur_alea(-pyromax, pyromax), valeur_alea(-pyromax,
             pyromax)), (valeur_alea(-pyromax, pyromax), valeur_alea(-pyromax,
             pyromax)))
    if random.randrange(2) == 0:
        while True:
            b = (a[random.randrange(2)], (valeur_alea(-pyromax, pyromax),
                 valeur_alea(-pyromax, pyromax)))
            if b[0] != b[1]:
                break
    else:
        while True:
            b = ((valeur_alea(-pyromax, pyromax), valeur_alea(-pyromax,
                 pyromax)), a[random.randrange(2)])
            if b[0] != b[1]:
                break
    (nega, negb) = (random.randrange(2), random.randrange(2))
    return (a, b, nega, negb)


def valeurs_facteur1(pyromax):  # renvoie les valeurs pour obtenir un facteur commun facteur de 1
    a = ((valeur_alea(-pyromax, pyromax), valeur_alea(-pyromax, pyromax)),
         (valeur_alea(-pyromax, pyromax), valeur_alea(-pyromax, pyromax)))
    while a[0] == a[1]:  # on refuse un carre
        a = ((valeur_alea(-pyromax, pyromax), valeur_alea(-pyromax,
             pyromax)), (valeur_alea(-pyromax, pyromax), valeur_alea(-pyromax,
             pyromax)))
    b = (a[random.randrange(2)], (0, 1))
    if random.randrange(2) == 1:  # le 1 est dans le deuxieme terme
        return (a, b, random.randrange(2), random.randrange(2))
    else:
        return (b, a, random.randrange(2), random.randrange(2))


def valeurs_facteurcarre(pyromax):  # renvoie les valeurs pour obtenir un facteur commun au carre
    a = ((valeur_alea(-pyromax, pyromax), valeur_alea(-pyromax, pyromax)),
         (valeur_alea(-pyromax, pyromax), valeur_alea(-pyromax, pyromax)))
    while a[0] == a[1]:  # on refuse un carre
        a = ((valeur_alea(-pyromax, pyromax), valeur_alea(-pyromax,
             pyromax)), (valeur_alea(-pyromax, pyromax), valeur_alea(-pyromax,
             pyromax)))
    if random.randrange(2) == 0:
        b = (a[0], a[0])
    else:
        b = (a[1], a[1])
    if random.randrange(2) == 0:  # le carre est en premier
        return (b, a, 0, random.randrange(2))
    else:
        return (a, b, random.randrange(2), 0)


def valeurs_facteura2mb2(pyromax):  # renvoie (((a,b),(a,-b)),((a,b),(c,d));nega,negb)
    a = ((valeur_alea(-pyromax, pyromax), valeur_alea(-pyromax, pyromax)),
         (valeur_alea(-pyromax, pyromax), valeur_alea(-pyromax, pyromax)))
    while a[0] == a[1]:  # on refuse un carre
        a = ((valeur_alea(-pyromax, pyromax), valeur_alea(-pyromax,
             pyromax)), (valeur_alea(-pyromax, pyromax), valeur_alea(-pyromax,
             pyromax)))
    if random.randrange(2) == 0:
        a = ((abs(a[0][0]), a[0][1]), a[1])
        b = (a[0], (a[0][0], -a[0][1]))
    else:
        a = (a[0], (abs(a[1][0]), a[1][1]))
        b = (a[1], (a[1][0], -a[1][1]))
    if random.randrange(2) == 0:  # le a²-b² est en premier
        return (b, a, 0, random.randrange(2))
    else:
        return (a, b, random.randrange(2), 0)


def valeurs_a2moinsb2(pyromax):  # renvoie les valeurs pour obtenir a²-(bx+c)²
    a = (0, valeur_alea(1, pyromax))
    b = (valeur_alea(-pyromax, pyromax), valeur_alea(-pyromax, pyromax))
    if random.randrange(2) == 0:  #  le nombre est en premier
        return (a, b)
    else:
        return (b, a)


def factorisation0(f1, f0=None, valeurs=None):  # factorise (ax+b)(cx+d)+(ax+b)(ex+f)
    if not valeurs:
        valeurs = valeurs_facteur_commun(10)
    tex_facteur_commun(valeurs, f1, f0)


def tex_factorisation1(valeurs):  # renvoie la premiere etape de la factorisation 1
    if valeurs[2] == 0:
        siga = ''
    else:
        siga = '-'
    if valeurs[3] == 0:
        sigb = '+'
    else:
        sigb = '-'
    if valeurs[0][1][0] == 0 and valeurs[0][1][1] == 1:  # le 1 est dans la premiere partie
        return '%s%s%s%s' % (siga, tex_trinome(dev(valeurs[0]), bpar=1),
                             sigb, tex_dev0(valeurs[1]))
    else:
        return '%s%s%s%s' % (siga, tex_dev0(valeurs[0]), sigb,
                             tex_trinome(dev(valeurs[1]), bpar=1))


def factorisation1(f1, f0=None, valeurs=None):  # factorise (ax+b)(cx+d)+(ax+b)
    if not valeurs:
        valeurs = valeurs_facteur1(10)
    if valeurs[2] == 0:
        siga = ''
    else:
        siga = '-'
    if valeurs[3] == 0:
        sigb = '+'
    else:
        sigb = '-'
    if valeurs[0][1][0] == 0 and valeurs[0][1][1] == 1:  # le 1 est dans la premiere partie
        texte = '%s%s%s%s' % (siga, tex_trinome(dev(valeurs[0]), bpar=1),
                              sigb, tex_dev0(valeurs[1]))
        ecrit_tex(f1, texte, tabs=2)
        if f0:
            ecrit_tex(f0, texte, tabs=2)
        texte = '%s%s\\times1%s%s' % (siga, tex_trinome(dev(valeurs[0]),
                bpar=1), sigb, tex_dev0(valeurs[1]))
        ecrit_tex(f1, texte, tabs=2)
    else:
        texte = '%s%s%s%s' % (siga, tex_dev0(valeurs[0]), sigb,
                              tex_trinome(dev(valeurs[1]), bpar=1))
        ecrit_tex(f1, texte, tabs=2)
        if f0:
            ecrit_tex(f0, texte, tabs=2)
        texte = '%s%s%s%s\\times1' % (siga, tex_dev0(valeurs[0]), sigb,
                tex_trinome(dev(valeurs[1]), bpar=1))
        ecrit_tex(f1, texte, tabs=2)
    f = facteur_commun(valeurs[0], valeurs[1])
    ecrit_tex(f1, tex_facteur_commun1(f, valeurs[2], valeurs[3]), tabs=2)
    f2 = facteur_commun2(f, valeurs[2], valeurs[3])
    if valeurs[2] and f2[1][0] != 0 and f2[1][1] != 0 or valeurs[3] and \
        f2[2][0] != 0 and f2[2][0] != 0:
        ecrit_tex(f1, tex_facteur_commun2(f2), tabs=2)
    ecrit_tex(f1, tex_dev0((f2[0], somme_polynomes(f2[1], f2[2]))),
              cadre=True, tabs=2)


def factorisation2(f1, f0=None, valeurs=None):  # factorise (ax+b)(cx+d)+(ax+b)²
    if not valeurs:
        valeurs = valeurs_facteurcarre(10)
    tex_facteur_commun(valeurs, f1, f0)


def tex_factorisation3(valeurs):  # renvoie les deux premieres etapes de la factorisation 3
    if valeurs[2] == 0:
        nega = ''
    else:
        nega = '-'
    if valeurs[3] == 0:
        negb = '+'
    else:
        negb = '-'
    if valeurs[0][0][0] == valeurs[0][1][0] and valeurs[0][0][1] == -valeurs[0][1][1]:
        return ('%s%s%s%s' % (nega, tex_trinome(dev(valeurs[0])), negb,
                tex_dev0(valeurs[1])), '%s%s%s%s' % (nega, tex_dev1(valeurs[0]),
                negb, tex_dev0(valeurs[1])))
    else:
        return ('%s%s%s%s' % (nega, tex_dev0(valeurs[0]), negb,
                tex_trinome(dev(valeurs[1]))), '%s%s%s%s' % (nega,
                tex_dev0(valeurs[0]), negb, tex_dev1(valeurs[1])))


def factorisation3(f1, f0=None, valeurs=None):  # factorise (ax+b)(cx+d)+(ax)²-b²
    if not valeurs:
        valeurs = valeurs_facteura2mb2(10)
    textes = tex_factorisation3(valeurs)
    if f0:
        ecrit_tex(f0, textes[0], tabs=2)
    ecrit_tex(f1, textes[0], tabs=2)
    ecrit_tex(f1, textes[1], tabs=2)
    tex_facteur_commun(valeurs, f1)


def factorisation4(f1, f0=None, valeurs=None):  #factorise 64-(x-5)²
    if not valeurs:
        valeurs = valeurs_a2moinsb2(10)
    tex_a2moinsb2(valeurs, f1, f0)


def factorisation5(f1, f0=None, valeurs=None):  # factorise a²-b²
    if not valeurs:
        valeurs = valeurs_apbamb(10)
    if valeurs[0][0] == -valeurs[1][0]:
        valeurs = ((valeurs[0][0], abs(valeurs[0][1])), (valeurs[1][0],
                   abs(valeurs[1][1])))
    else:
        valeurs = ((abs(valeurs[0][0]), valeurs[0][1]), (abs(valeurs[1][0]),
                   valeurs[1][1]))
    if f0:
        ecrit_tex(f0, tex_trinome(dev(valeurs)), tabs=2)
    ecrit_tex(f1, tex_trinome(dev(valeurs)), tabs=2)
    ecrit_tex(f1, tex_dev1(valeurs), tabs=2)
    ecrit_tex(f1, tex_dev0(valeurs), cadre=True, tabs=2)


def tex_factorisation6(valeurs):  # renvoie les deux premieres etapes de la factorisation 6
    if valeurs[0][0] == valeurs[0][1]:  # le carre est en premier
        if valeurs[3] == 0:  # on insere un signe +
            return (tex_trinome_alea(dev(valeurs[0])) + '+' + tex_dev0(valeurs[1]),
                    tex_trinome(dev(valeurs[0])) + '+' + tex_dev0(valeurs[1]))
        else:
            return (tex_trinome_alea(dev(valeurs[0])) + '-' + tex_dev0(valeurs[1]),
                    tex_trinome(dev(valeurs[0])) + '-' + tex_dev0(valeurs[1]))
    else:
        if valeurs[2] == 0:  # on insere un signe +
            return (tex_dev0(valeurs[0]) + tex_trinome_alea(dev(valeurs[1]),
                    bplus=1), tex_dev0(valeurs[0]) + tex_trinome(dev(valeurs[1]),
                    bplus=1))
        else:
            return ('-' + tex_dev0(valeurs[0]) + tex_trinome_alea(dev(valeurs[1]),
                    bplus=1), '-' + tex_dev0(valeurs[0]) + tex_trinome(dev(valeurs[1]),
                    bplus=1))


def factorisation6(f1, f0=None, valeurs=None):  # factorise (ax+b)(cx+d)+2abx+a²x²+b²
    if not valeurs:
        valeurs = valeurs_facteurcarre(10)
    textes = tex_factorisation6(valeurs)
    if f0:
        ecrit_tex(f0, textes[0], tabs=2)
    ecrit_tex(f1, textes[0], tabs=2)
    ecrit_tex(f1, textes[1], tabs=2)
    tex_facteur_commun((valeurs[0], valeurs[1], valeurs[2], valeurs[3]),
                       f1)


#
# ------------------- DEV-FACT-EQUAT -------------------


def choix_exo(a):  # renvoie un tuple contenant les valeurs
    if a == 0:
        return valeurs_facteur_commun(10)
    elif a == 1:
        return valeurs_facteur1(10)
    elif a == 2:
        return valeurs_facteurcarre(10)
    elif a == 3:
        return valeurs_facteura2mb2(10)
    else:
        return valeurs_facteurcarre(10)


def valeur_quotient():  # renvoie un tuple contenant la valeur du quotient à calculer
    (a, b) = (random.randrange(-10, 1), random.randrange(1, 11))
    return (a / pgcd(a, b), b / pgcd(a, b))


def tex_initial(exo, a):  # renvoie l'écriture de l'expression A
    if exo == 0 or exo == 2:
        return tex_facteur_commun0(a)
    elif exo == 1:
        return tex_factorisation1(a)
    elif exo == 3:
        return tex_factorisation3(a)[0]
    else:
        return tex_factorisation6(a)[0]


def fin_fact(a):  # renvoie un tuple contenant la version factorisee de a
    return facteur_commun3(facteur_commun(a[0], a[1]), a[2], a[3])


def tex_equations(fact, f1):  # renvoie un tuple contenant les deux binomes egaux a 0
    f1.write('    Nous savons que $A=%s$. Nous devons donc r\xe9soudre $%s=0$.\\par\n' %
             (tex_dev0(fact), tex_dev0(fact)))
    f1.write('    Un produit de facteurs est nul signifie qu\'un des facteurs est nul. Donc :\n')
    f1.write('    \\[%s=0 \\qquad\\text{ou}\\qquad %s=0\\]\n' % (tex_binome(fact[0]),
             tex_binome(fact[1])))
    eq = equations1(fact)
    if not isinstance(eq, tuple):
        f1.write("  \t\\fbox{Cette \xe9quation n'admet aucune solution.}\n")
    elif not isinstance(eq[0], tuple):
        f1.write('    \\[ %s=%s \\]\n' % (tex_coef(eq[1][0], 'x'), eq[1][1]))
        if eq[1][0] != 1:
            f1.write('\\[ x=%s \\]\n' % tex_frac(equations2(eq)[1]))
        f1.write('    \\fbox{La solution de cette \xe9quation est \\,$%s$\\,.}\n' %
                 tex_frac(equations3(eq)[1]))
    elif not isinstance(eq[1], tuple):
        f1.write('    \\[ %s=%s \\]\n' % (tex_coef(eq[0][0], 'x'), eq[0][1]))
        if eq[0][0] != 1:
            f1.write('    \\[ x=%s \\]\n' % tex_frac(equations2(eq)[0]))
        f1.write('    \\fbox{La solution de cette \xe9quation est \\,$%s$\\,.}\n' %
                 tex_frac(equations3(eq)[0]))
    else:
        f1.write('    \\[%s=%s \\qquad\\text{ou}\\qquad %s=%s\\]\n' % (tex_coef(eq[0][0],
                 'x'), eq[0][1], tex_coef(eq[1][0], 'x'), eq[1][1]))
        if eq[0][0] != 1 or eq[1][0] != 1:
            f1.write('    \\[x=%s \\qquad\\text{ou}\\qquad x=%s\\]\n' %
                     (tex_frac(equations2(eq)[0]), tex_frac(equations2(eq)[1])))
        f1.write('    \\fbox{Les solutions de cette \xe9quation sont \\,$%s\\,\\text{ et }\\,%s$\\,.}\n' %
                 (tex_frac(equations3(eq)[0]), tex_frac(equations3(eq)[1])))


def equations1(a):  #renvoie ((9,5),(3,-7)) pour pouvoir ecrire 9x=5 ou 3x=-7
    if a[0][0] == 0:
        if a[1][0] == 0:
            return ''
        else:
            return ('', (a[1][0], -a[1][1]))
    elif a[1][0] == 0:
        return ((a[0][0], -a[0][1]), '')
    else:
        return ((a[0][0], -a[0][1]), (a[1][0], -a[1][1]))


def equations2(a):  # renvoie ((5,9),(-7,3)) pour pouvoir ecrire x=5/9 ou x=-7/3
    if not isinstance(a, tuple):
        return ''
    elif not isinstance(a[0], tuple):
        return ('', (a[1][1], a[1][0]))
    elif not isinstance(a[1], tuple):
        return ((a[0][1], a[0][0]), '')
    else:
        return ((a[0][1], a[0][0]), (a[1][1], a[1][0]))


def equations3(a):  # renvoie les solutions éventuellement simplifiée
    a = equations2(a)
    if not isinstance(a, tuple):
        return ''
    elif not isinstance(a[0], tuple):
        if simplifie(a[1]):
            return ('', simplifie(a[1]))
        else:
            return a
    elif not isinstance(a[1], tuple):
        if simplifie(a[0]):
            return (simplifie(a[0]), '')
        else:
            return a
    else:
        if simplifie(a[0]):
            if simplifie(a[1]):
                return (simplifie(a[0]), simplifie(a[1]))
            else:
                return (simplifie(a[0]), a[1])
        elif simplifie(a[1]):
            return (a[0], simplifie(a[1]))
        else:
            return a


def developpements(expr, exo, f1):  # effectue les developpements
    if exo != 3 and exo != 6:
        tex_developpe2(expr[0], expr[2], expr[1], expr[3], f1, tabs=2)
    elif exo == 6 and expr[0][0] == expr[0][1] or exo == 3 and expr[0][0][0] == \
        expr[0][1][0] and expr[0][0][1] == -expr[0][1][1]:
        ecrit_tex(f1, tex_initial(exo, expr), tabs=2)
        if expr[2]:
            siga = '-'
        else:
            siga = ''
        if expr[3]:
            sigb = '-'
        else:
            sigb = ''
        ecrit_tex(f1, '%s%s%s%s' % (siga, tex_trinome(dev(expr[0])),
                  sigb, tex_dev1(expr[1], bpar=expr[3], bplus=expr[3] -
                  1)), tabs=2)
        if expr[2]:
            a = coef_opposes(dev(expr[0]))
        else:
            a = dev(expr[0])
        if expr[3]:
            b = coef_opposes(dev(expr[1]))
        else:
            b = dev(expr[1])
        ecrit_tex(f1, tex_trinome(a) + tex_trinome(b, bplus=1), tabs=2)
        ecrit_tex(f1, tex_trinome(somme_polynomes(a, b)), cadre=True,
                  tabs=2)
    else:
        ecrit_tex(f1, tex_initial(exo, expr), tabs=2)
        if expr[2]:
            siga = '-'
        else:
            siga = ''
        if expr[3]:
            sigb = '-'
        else:
            sigb = ''
        ecrit_tex(f1, '%s%s%s%s' % (siga, tex_dev1(expr[0], bpar=expr[2],
                  bplus=expr[2] - 1), sigb, tex_trinome(dev(expr[1]),
                  bpar=expr[3], bplus=expr[3] - 1)), tabs=2)
        if expr[2]:
            a = coef_opposes(dev(expr[0]))
        else:
            a = dev(expr[0])
        if expr[3]:
            b = coef_opposes(dev(expr[1]))
        else:
            b = dev(expr[1])
        ecrit_tex(f1, tex_trinome(a) + tex_trinome(b, bplus=1), tabs=2)
        ecrit_tex(f1, tex_trinome(somme_polynomes(a, b)), cadre=True,
                  tabs=2)


def version_developpee(expr):  # renvoie la version developpe de A
    if expr[2]:
        a = coef_opposes(dev(expr[0]))
    else:
        a = dev(expr[0])
    if expr[3]:
        b = coef_opposes(dev(expr[1]))
    else:
        b = dev(expr[1])
    return somme_polynomes(a, b)


def tex_fractions(expr, nb, f1):  # repond a la question sur la valeur de x
    a = version_developpee(expr)
    f1.write('    Nous savons que $A=%s$\\,. Donc pour $x=%s$\\, : \n' %
             (tex_trinome(a), tex_frac(nb)))
    ecrit_tex(f1, tex_valeurx0(a, nb), tabs=2)
    ecrit_tex(f1, tex_valeurx1(a, nb), cadre=nb == (0, 1), tabs=2)
    b = decomp_prod((a[0], 1), (nb[0] ** 2, nb[1] ** 2))[0:2]
    c = decomp_prod((a[1], 1), (nb[0], nb[1]))[0:2]
    a = (produit(b[0], b[1]), produit(c[0], c[1]), (a[2], 1))
    ecrit_tex(f1, tex_valeurx2(a, nb), cadre=a[0][1] == a[1][1] == 1,
              tabs=2)
    ecrit_tex(f1, tex_valeurx3(a, nb), 1, tabs=2)


def tex_valeurx0(a, nb):
    if nb == (0, 1):
        return '%s%s%s' % (tex_coef(a[0], '\\times %s^2' % tex_frac(nb)),
                           tex_coef(a[1], '\\times %s' % tex_frac(nb),
                           bplus=a[0]), tex_coef(a[2], '', bplus=a[0] or
                           a[1]))
    else:
        return '%s%s%s' % (tex_coef(a[0], '\\times\\left(%s\\right)^2' %
                           tex_frac(nb)), tex_coef(a[1],
                           '\\times\\left(%s\\right)' % tex_frac(nb),
                           bplus=a[0]), tex_coef(a[2], '', bplus=a[0] or
                           a[1]))


def tex_valeurx1(a, nb):
    if nb == (0, 1):
        return tex_coef(a[2], '')
    elif nb[1] == 1:
        return tex_coef(a[0] * nb[0] ** 2, '') + tex_coef(a[1] * nb[0],
                '', bplus=a[0]) + tex_coef(a[2], '', bplus=a[0] or a[1])
    else:
        texte = ''
        if a[0] != 0:
            a0 = ((a[0], 1), (nb[0] ** 2, nb[1] ** 2))
            if isinstance(decomp_prod(a0[0], a0[1])[2], tuple):
                texte = tex_coef(1, tex_decomp_prod(decomp_prod(a0[0],
                                 a0[1])))
            else:
                texte = tex_coef(1, tex_frac(produit(a0[0], a0[1])))
        if a[1] != 0:
            a1 = ((a[1], 1), (nb[0], nb[1]))
            if isinstance(decomp_prod(a1[0], a1[1])[2], tuple):
                texte = texte + tex_coef(1, tex_decomp_prod(decomp_prod(a1[0],
                        a1[1])), bplus=a[0])
            else:
                texte = texte + tex_coef(1, tex_frac(produit(a1[0], a1[1])),
                        bplus=a[0])
        texte = texte + tex_coef(a[2], '', bplus=1)
        return texte


def tex_valeurx2(a, nb):
    if nb == (0, 1):
        return ''
    else:
        if a[0][1] == a[1][1] == 1:
            return tex_coef(a[0][0] + a[1][0] + a[2][0], '')
        else:
            c = den_com0(a[0], a[1])
            texte = ''
            if a[0][0] != 0:
                texte = tex_coef(1, tex_frac((a[0][0] * c[0], a[0][1] *
                                 c[0])))
            if a[1][0] != 0:
                texte = texte + tex_coef(1, tex_frac((a[1][0] * c[1], a[1][1] *
                        c[1])), bplus=texte)
            if a[2][0] != 0:
                texte = texte + tex_coef(1, tex_frac(((a[2][0] * a[0][1]) *
                        c[0], a[0][1] * c[0])), bplus=texte)
            return texte


def tex_valeurx3(a, nb):
    if nb == (0, 1) or a[0][1] == a[1][1] == 1:
        return ''
    else:
        c = den_com0(a[0], a[1])
        b = (a[0][0] * c[0] + a[1][0] * c[1] + (a[2][0] * a[0][1]) * c[0],
             a[0][1] * c[0])
        if simplifie(b):
            return tex_frac(b) + '=' + tex_frac(simplifie(b))
        else:
            return tex_frac(b)


