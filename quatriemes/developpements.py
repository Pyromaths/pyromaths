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

from outils import ecrit_tex, valeur_alea, signe
from random import randrange

#
# ------------------- DEVELOPPEMENTS -------------------


def exo_distributivite():
    exo = ["\\exercice",
           "Développer et réduire les expressions suivantes :",
           "\\begin{multicols}{2}", "  \\noindent%"]
    cor = ["\\exercice*",
           "Développer et réduire les expressions suivantes :",
           "\\begin{multicols}{2}", "  \\noindent%"]
    for i in range(8):
        (l1, l2) = tex_developpe1(valeurs_distr(10))
        exo.extend(l1)
        cor.extend(l2)
        exo.append("  \\stepcounter{nocalcul}%")
        cor.append("  \\stepcounter{nocalcul}%")
    exo.append("\\end{multicols}\n")
    cor.append("\\end{multicols}\n")
    return (exo, cor)


def exo_double_distributivite():
    exo = ["\\exercice",
           "Développer et réduire les expressions suivantes :",
           "\\begin{multicols}{2}", "  \\noindent%"]
    cor = ["\\exercice*",
           "Développer et réduire les expressions suivantes :",
           "\\begin{multicols}{2}", "  \\noindent%"]
    for i in range(6):
        (l1, l2) = tex_developpe1(valeurs_dbldistr(10))
        exo.extend(l1)
        cor.extend(l2)
        exo.append("  \\stepcounter{nocalcul}%")
        cor.append("  \\stepcounter{nocalcul}%")
    exo.append("\\end{multicols}\n")
    cor.append("\\end{multicols}\n")
    return (exo, cor)


def coef_opposes(a):  # renvoie un tuple dont les valeurs sont les opposees de celles de a
    l = []
    for i in range(len(a)):
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
    for i in range(int):
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
        elif ca == 0 or cb == 0 or cc == 0 or cd == 0:
            if ca == 0:
                texte = '%s\\times %s+%s\\times %s' % (tex_coef(cb, '',
                        bpn=bpn), tex_coef(cc, 'x', bpn=1), tex_coef(cb,
                        '', bpn=1), tex_coef(cd, '', bpn=1))
            elif cb == 0:
                texte = '%s\\times %s+%s\\times %s' % (tex_coef(ca, 'x',
                        bpn=bpn), tex_coef(cc, 'x', bpn=1), tex_coef(ca,
                        'x', bpn=1), tex_coef(cd, '', bpn=1))
            elif cc == 0:
                texte = '%s\\times %s+%s\\times %s' % (tex_coef(cd, '',
                        bpn=bpn), tex_coef(ca, 'x', bpn=1), tex_coef(cd,
                        '', bpn=1), tex_coef(cb, '', bpn=1))
            else:
                texte = '%s\\times %s+%s\\times %s' % (tex_coef(cc, 'x',
                        bpn=bpn), tex_coef(ca, 'x', bpn=1), tex_coef(cc,
                        'x', bpn=1), tex_coef(cb, '', bpn=1))
            return texte
        else:
            texte = '%s+%s+%s+%s' % (tex_coef(ca * cc, 'x^2', bpn=bpn),
                    tex_coef(ca * cd, 'x', bpn=1), tex_coef(cb * cc, 'x',
                    bpn=1), tex_coef(cb * cd, '', bpn=1))
            if bpar:
                return '(' + texte + ')'
            else:
                return texte


def tex_developpe1(a):  # developpe l'expression a
    (exo, cor) = ([], [])
    exo.append("  \\[ \\thenocalcul = %s \\]" % tex_dev0(a))
    cor.append("  \\[ \\thenocalcul = %s \\]" % tex_dev0(a))
    cor.append("  \\[ \\thenocalcul = %s \\]" % tex_dev1(a))
    cor.append("  \\[ \\boxed{\\thenocalcul = %s} \\]" % tex_trinome(dev(a)))
    return (exo, cor)


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
        for i in range(3):  # compte le nombre de valeurs nulles
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


def valeurs_amb2(pyromax):  # renvoie un tuple contenant ((3,-5),(3-5))
    a = valeur_alea(1, pyromax)
    b = valeur_alea(-pyromax, -1)
    return ((a, b), (a, b))


def valeurs_apbamb(pyromax):  # renvoie un tuple contenant ((3,-5),(3,+5))
    a = valeur_alea(-pyromax, pyromax)
    b = valeur_alea(-pyromax, pyromax)
    if randrange(2) == 0:
        return ((a, b), (-a, b))
    else:
        return ((a, b), (a, -b))


def valeurs_distr(pyromax):  # renvoie in tuple contenant ((a,b),(c,d)) avec a != c ou b != d (en valeur absolue) et a, b, c ou d nul.
    while True:
        a = valeur_alea(-pyromax, pyromax)
        b = valeur_alea(-pyromax, pyromax)
        c = valeur_alea(-pyromax, pyromax)
        l = [a, b, c]
        l.insert(randrange(4), 0)
        if abs(l[1]) != 1 and abs(l[3]) != 1:
            break  #Pour qu'il y ait quelque chose à développer.
    return ((l[0], l[1]), (l[2], l[3]))


def valeurs_dbldistr(pyromax):  # renvoie in tuple contenant ((a,b),(c,d)) avec a != c ou b != d (en valeur absolue)
    a = valeur_alea(-pyromax, pyromax)
    b = valeur_alea(-pyromax, pyromax)
    c = valeur_alea(-pyromax, pyromax)
    d = valeur_alea(-pyromax, pyromax)
    while abs(a) == abs(c) and abs(b) == abs(d):
        c = valeur_alea(-pyromax, pyromax)
        d = valeur_alea(-pyromax, pyromax)
    return ((a, b), (c, d))


#===============================================================================
# Développements
#===============================================================================


def def_vals():
    lexp = [0, 1, 2, 0, 1, 2]
    expr = []
    for i in range(6):
        a = valeur_alea(-10, 10)
        e = lexp.pop(randrange(len(lexp)))
        expr.append([a, 'x', e])
    return expr


def def_vals2():
    expr = []
    loper = ['+', '-', '\\times', '+', '-', '\\times', '+', '-']
    for i in range(8):
        a = valeur_alea(-10, 10)
        e = randrange(3)
        o = loper.pop(randrange(len(loper)))
        expr.append([a, 'x', e, o])
    return expr


def def_vals3():
    expr = []
    lsgn = ['+', '-', '+', '-']
    for i in range(9):
        if i % 3 == 0:
            sgn = lsgn.pop(randrange(len(lsgn)))
            if i > 0 or sgn == '-':
                expr.append(sgn)
            expr.append(" (")
        elif i % 3 == 1:
            a = valeur_alea(-10, 10)
            e = randrange(3)
            expr.append([a, 'x', e])
        else:
            a = valeur_alea(-10, 10)
            e = randrange(3)
            while e == expr[-1][2]:
                e = randrange(3)
            expr.append([a, 'x', e])
            expr.append(') ')
    return expr


def def_vals4():
    expr = []
    for i in range(9):
        a = valeur_alea(-10, 10)
        e = randrange(3)
        if i % 3 == 0:
            expr.append([a, 'x', e])
            expr.append(' \,(')
        elif i % 3 == 1:
            expr.append([a, 'x', e])
        else:
            while e == expr[-1][2]:
                e = randrange(3)
            expr.append([a, 'x', e])
            expr.append(') ')
    return expr


def def_vals5():
    expr = []
    for i in range(8):
        a = valeur_alea(-10, 10)
        e = randrange(3)
        if i % 2 == 0:
            if i % 4 == 0:
                expr.append(" (")
            else:
                expr.append(' \,(')
            expr.append([a, 'x', e])
        else:
            while e == expr[-1][2]:
                e = randrange(3)
            expr.append([a, 'x', e])
            expr.append(') ')
            if i == 3:
                expr.append(['+', '+', '-'].pop(randrange(3)))
    return expr


def monome(coef, var, exposant, bplus=0, bpn=0, bpc=0):

    # coef est le coefficient à écrire devant la variable var
    # bplus est un booleen : s'il est vrai, il faut ecrire le signe +
    # bpn est un booleen : s'il est vrai, il faut mettre des parentheses autour de l'ecriture si coef est negatif.
    # bpc est un booleen : s'il est vrai, il faut mettre des parentheses autour de l'ecriture si coef =! 0 ou 1 et var est non vide

    if exposant == 0:
        var = ''
    elif exposant > 1:
        var = '%s^{%s}' % (var, exposant)
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


def print_expr(expr):
    text = '$'
    for i in range(len(expr)):
        coef = expr[i][0]
        var = expr[i][1]
        exposant = expr[i][2]
        if i > 0:
            text = '%s%s' % (text, monome(coef, var, exposant, bplus=1))
        else:
            text = '%s%s' % (text, monome(coef, var, exposant))
    return '%s$' % text


def print_expr2(expr):
    text = '$'
    for i in range(len(expr)):
        coef = expr[i][0]
        var = expr[i][1]
        exposant = expr[i][2]
        if i > 0:
            text = '%s %s %s' % (text, expr[i - 1][3], monome(coef, var,
                                 exposant, bpn=1))
        else:
            text = '%s%s' % (text, monome(coef, var, exposant))
    return '%s$' % text


def print_expr3(expr):
    text = '$'
    for i in range(len(expr)):
        if isinstance(expr[i], list):
            coef = expr[i][0]
            var = expr[i][1]
            exposant = expr[i][2]
            if expr[i - 1] == " (":
                text = '%s %s' % (text, monome(coef, var, exposant))
            else:
                text = '%s %s' % (text, monome(coef, var, exposant,
                                  bplus=1))
        else:
            text = '%s%s' % (text, expr[i])
    return '%s$' % text


def print_expr4(expr):
    text = '$'
    for i in range(len(expr)):
        if isinstance(expr[i], list):
            coef = expr[i][0]
            var = expr[i][1]
            exposant = expr[i][2]
            if i == 0 or expr[i - 1] == " (":
                text = '%s %s' % (text, monome(coef, var, exposant))
            else:
                text = '%s %s' % (text, monome(coef, var, exposant,
                                  bplus=1))
        else:
            text = '%s%s' % (text, expr[i])
    return '%s$' % text


#for i in xrange(2):
    #print '  \item %s' % print_expr4(def_vals5())

# ------------ ÉQUATIONS ------------
#for i in xrange(20):
 #print '\\item $x %s = %s$' % (monome(valeur_alea(-10,10),'',0,bplus=1), randrange(-10,10))
 #print '\\item $%s = %s$' % (monome(valeur_alea(-10,10),'x',1), randrange(-10,10))
 #print '\\item $%s %s = %s$' % (monome(valeur_alea(-10,10),'x',1), monome(valeur_alea(-10,10),'',0,bplus=1), randrange(-10,10))
 #print '\\item $%s %s = %s %s$' % (monome(valeur_alea(-10,10),'x',1), monome(valeur_alea(-10,10),'',0,bplus=1),monome(valeur_alea(-10,10),'x',1), monome(randrange(-10,10),'',0,bplus=1))
