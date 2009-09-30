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

import math
import random
import string
import outils

#===============================================================================
# Poser des opérations
#===============================================================================


def valeurs():
    nba = outils.valeur_alea(111, 99999)
    while 1:
        nbb = outils.valeur_alea(111, 99999)
        if nbb - (nbb // 10) * 10:
            break
    puisb = outils.valeur_alea(-2, 0)
    nbb = nbb * 10 ** puisb
    deca = [str(nba)[i] for i in range(len(str(nba)))]
    decb = [str(nbb)[i] for i in range(len(str(nbb)))]
    if random.randrange(2):
        (nba, deca, nbb, decb) = (nbb, decb, nba, deca)
    if deca.count('.'):
        posa = deca.index('.')
    else:
        posa = len(deca)
    if decb.count('.'):
        posb = decb.index('.')
    else:
        posb = len(decb)

    lavtvirg = max(posa, posb)
    laprvirg = max(len(deca) - posa, len(decb) - posb)
    return (nba, nbb, deca, decb, lavtvirg, laprvirg)


def valeurs_prod():
    while 1:
        nba = outils.valeur_alea(101, 9999)
        if nba - (nba // 10) * 10:
            break
    puisa = outils.valeur_alea(-3, -1)
    while 1:
        nbb = outils.valeur_alea(101, 999)
        if nbb - (nbb // 10) * 10:
            break
    puisb = outils.valeur_alea(-3, -1)
    return (nba, nbb, puisa, puisb)


def lignes(ligne, deca, lavtvirg, laprvirg):
    if deca.count('.'):
        posa = deca.index('.')
    else:
        posa = len(deca)
    if posa < lavtvirg:
        for i in range(lavtvirg - posa):
            ligne.append('')
    for i in range(len(deca)):
        if deca[i] == '.':
            ligne.append(',')
        else:
            ligne.append(str(deca[i]))
    for i in range(laprvirg - (len(deca) - posa)):
        if ligne.count(','):
            ligne.append('0')
        else:
            ligne.append(',')
    return ligne


def mon_int(t):  # retourne un entier texte sous la forme d'un nombre, zéro sinon
    if t == '':
        t = 0
    elif ('1234567890').count(t):
        t = int(t)
    else:
        t = 0
    return t


def retenues_somme(ligne1, ligne2):
    lg = len(ligne1)
    ligne0 = ['' for i in range(lg)]
    for i in range(lg - 1):

        #on déplace la retenue pour qu'elle ne soit pas au-dessus de la virgule

        if ligne1[(lg - i) - 1] == ',' and ligne0[(lg - i) - 1] == '1':
            ligne0[(lg - i) - 2] = '1'
        elif mon_int(ligne1[(lg - i) - 1]) + mon_int(ligne2[(lg - i) - 1]) + \
            mon_int(ligne0[(lg - i) - 1]) > 9:
            ligne0[(lg - i) - 2] = '1'
    return ligne0


def retenues_diff(ligne1, ligne2):
    lg = len(ligne1)
    ret = 0
    for i in range(lg - 1):
        if not (ligne1[(lg - i) - 1] == ',' and ret):
            if mon_int(ligne1[(lg - i) - 1]) < mon_int(ligne2[(lg - i) -
                    1]) + ret:
                ligne1[(lg - i) - 1] = '$_1$%s' % ligne1[(lg - i) - 1]
                tmpret = 1
            else:
                tmpret = 0
            if ret:
                ligne2[(lg - i) - 1] = '%s$_1$' % ligne2[(lg - i) - 1]
            ret = tmpret
    return (ligne1, ligne2)


def tex_somme(f0, f1):
    (ligne1, ligne2) = ([''], ['+'])
    (nba, nbb, deca, decb, lavtvirg, laprvirg) = valeurs()
    total = nba + nbb
    dectotal = [str(total)[i] for i in range(len(str(total)))]
    if dectotal.index('.') <= lavtvirg:
        ligne3 = ['']
    else:
        ligne3 = []
    ligne1 = lignes(ligne1, deca, lavtvirg, laprvirg)
    ligne2 = lignes(ligne2, decb, lavtvirg, laprvirg)
    ligne3 = lignes(ligne3, dectotal, lavtvirg, laprvirg)
    ligne0 = retenues_somme(ligne1, ligne2)
    if ligne0[0] == '1':
        ligne0[0] = '\\tiny 1'
    f0.write('      \\item La somme des termes %s et %s.\\par\n' % (outils.sepmilliers(nba),
             outils.sepmilliers(nbb)))
    f1.write('      \\item La somme des termes %s et %s.\\par\n' % (outils.sepmilliers(nba),
             outils.sepmilliers(nbb)))
    f1.write('        \\begin{tabular}[t]{*{%s}{c}}\n' % (lavtvirg +
             laprvirg + 1))
    f1.write('          %s \\\\\n' % ' & \\tiny '.join(ligne0))
    f1.write('          %s \\\\\n' % ' & '.join(ligne1))
    f1.write('          %s \\\\\n          \\hline\n' % ' & '.join(ligne2))
    f1.write('          %s \\\\\n' % ' & '.join(ligne3))
    f1.write('        \\end{tabular}\\par\n')
    outils.ecrit_tex(f1, '%s+%s = %s' % (outils.sepmilliers(nba, 1),
                     outils.sepmilliers(nbb, 1), outils.sepmilliers(nba +
                     nbb, 1)), cadre=1, thenocalcul='', tabs=3)


def tex_difference(f0, f1):
    (ligne1, ligne2) = ([''], ['-'])
    (nba, nbb, deca, decb, lavtvirg, laprvirg) = valeurs()
    if nba < nbb:
        (nba, nbb, deca, decb) = (nbb, nba, decb, deca)
    total = nba - nbb
    dectotal = [str(total)[i] for i in range(len(str(total)))]
    if dectotal.index('.') <= lavtvirg:
        ligne3 = ['']
    else:
        ligne3 = []
    ligne1 = lignes(ligne1, deca, lavtvirg, laprvirg)
    ligne2 = lignes(ligne2, decb, lavtvirg, laprvirg)
    ligne3 = lignes(ligne3, dectotal, lavtvirg, laprvirg)
    (ligne1, ligne2) = retenues_diff(ligne1, ligne2)
    f0.write("      \\item La différence des termes %s et %s.\\par\n" %
             (outils.sepmilliers(nba), outils.sepmilliers(nbb)))
    f1.write("      \\item La différence des termes %s et %s.\\par\n" %
             (outils.sepmilliers(nba), outils.sepmilliers(nbb)))
    f1.write('        \\begin{tabular}[t]{*{%s}{c}}\n' % (lavtvirg +
             laprvirg + 1))
    f1.write('          %s \\\\\n' % ' & '.join(ligne1))
    f1.write('          %s \\\\\n          \\hline\n' % ' & '.join(ligne2))
    f1.write('          %s \\\\\n' % ' & '.join(ligne3))
    f1.write('        \\end{tabular}\\par\n')
    outils.ecrit_tex(f1, '%s-%s = %s' % (outils.sepmilliers(nba, 1),
                     outils.sepmilliers(nbb, 1), outils.sepmilliers(nba -
                     nbb, 1)), cadre=1, thenocalcul='', tabs=3)


def pose_mult(nba, nbb):
    (ligne, total) = ([], 0)
    for i in range(int(math.log10(nbb)) + 1):
        sstotal = ((nbb - (nbb // 10) * 10) * nba) * 10 ** i
        total = total + sstotal
        ligne.append(sstotal)
        nbb = nbb // 10
    return (ligne, total)


def ligneprod(ligne, dec, lg):
    ligne.extend(['' for i in range((lg - len(dec)) - len(ligne))])
    ligne.extend(dec)
    return ligne


def tex_produit(f0, f1):
    (nba, nbb, puisa, puisb) = valeurs_prod()
    deca = [','.join(str(nba * 10 ** puisa).rsplit('.'))[i] \
                    for i in range(len(str(nba * 10 ** puisa)))]
    decb = [','.join(str(nbb * 10 ** puisb).rsplit('.'))[i] \
                    for i in range(len(str(nbb * 10 ** puisb)))]

    (dec3, total) = pose_mult(nba, nbb)
    (dec3bis, total) = pose_mult(nbb, nba)
    total = ((nba * 10 ** puisa) * nbb) * 10 ** puisb
    dec4 = [str(total)[i] for i in range(len(str(total)))]
    if dec4.count('.'):
        i = dec4.index('.')
        if (len(dec4) - i) - 1 < -(puisa + puisb):
            for j in range(-(puisa + puisb) - len(dec4) + i + 1):
                dec4.append('0')  #ajoute les 0 inutiles au produit
        dec4.pop(i)  # supprime le point décimal
        dec4[i - 1] = '%s\\Huge ,' % dec4[i - 1]  # et ajoute une Huge virgule au chiffre des unités
    lg = max(len(dec4), max(len(deca), len(decb)))  # nombre de colonnes dans le tableau
    f0.write('      \\item Le produit des facteurs %s et %s.\\par\n' % (outils.sepmilliers(nba *
             10 ** puisa), outils.sepmilliers(nbb * 10 ** puisb)))
    f1.write('      \\item Le produit des facteurs %s et %s.\\par\n' % (outils.sepmilliers(nba *
             10 ** puisa), outils.sepmilliers(nbb * 10 ** puisb)))
    f1.write('        \\begin{enumerate}\n')
    f1.write('          \\item Première méthode :\\par\n')
    f1.write('          \\begin{tabular}[t]{*{%s}{c}}\n' % lg)
    f1.write('            %s \\\\\n' % ' & '.join(ligneprod([], deca,lg)))
    f1.write('            %s \\\\\n          \\hline\n' % \
                            ' & '.join(ligneprod(['$\\times$'], decb, lg)))
    for i in range(len(dec3)):
        dec = [str(dec3[i])[j] for j in range(len(str(dec3[i])))]
        f1.write('            %s \\\\\n' % ' & '.join(ligneprod([], dec, lg)))
    f1.write('            \\hline \\\\\n')
    f1.write('            %s \\\\\n' % ' & '.join(ligneprod([], dec4, lg)))
    f1.write('          \\end{tabular}\n')
    f1.write('          \\item Seconde méthode :\\par\n')
    f1.write('          \\begin{tabular}[t]{*{%s}{c}}\n' % len(dec4))
    f1.write('            %s \\\\\n' % ' & '.join(ligneprod([], decb, lg)))
    f1.write('            %s \\\\\n          \\hline\n' % \
                            ' & '.join(ligneprod(['$\\times$'], deca, lg)))
    for i in range(len(dec3bis)):
        dec = [str(dec3bis[i])[j] for j in range(len(str(dec3bis[i])))]
        f1.write('            %s \\\\\n' % ' & '.join(ligneprod([], dec, lg)))
    f1.write('            \\hline \\\\\n')
    f1.write('            %s \\\\\n' % ' & '.join(ligneprod([], dec4, lg)))
    f1.write('          \\end{tabular}\n')
    f1.write('          \\end{enumerate}\n')
    outils.ecrit_tex(f1, '%s\\times%s = %s' % (outils.sepmilliers(nba *
                     10 ** puisa, 1), outils.sepmilliers(nbb * 10 **
                     puisb, 1), outils.sepmilliers((nba * nbb) * 10 ** (puisa +
                     puisb), 1)), cadre=1, thenocalcul='', tabs=3)


#===============================================================================
# Calcul mental
#===============================================================================


def tex_calcul_mental(f0, f1):
    modules = (plus, moins, plus, div)
    calculs = [i for i in range(20)]
    for i in range(20):
        j = random.randrange(0, len(calculs))
        (a, b) = modules[calculs[j] // 5](10)
        if calculs[j] // 5 == 0:
            choix_trou(a, b, a + b, '+', f0, f1)
        if calculs[j] // 5 == 1:
            choix_trou(a, b, a - b, '-', f0, f1)
        if calculs[j] // 5 == 2:
            choix_trou(a, b, a * b, '\\times', f0, f1)
        if calculs[j] // 5 == 3:
            choix_trou(a, b, a // b, '\\div', f0, f1)
        calculs.pop(j)


def choix_trou(nb1, nb2, tot, operateur, f0, f1):
    nbaleatoire = outils.randrange(4)
    if nbaleatoire > 1:
        f0.write('    \\item $%s %s %s = \\ldots\\ldots$\n' % (nb1,
                 operateur, nb2))
        f1.write('    \\item $%s %s %s = \\mathbf{%s}$\n' % (nb1,
                 operateur, nb2, tot))
    elif nbaleatoire > 0:
        f0.write('    \\item $%s %s \\ldots\\ldots = %s$\n' % (nb1,
                 operateur, tot))
        f1.write('    \\item $%s %s \\mathbf{%s} = %s$\n' % (nb1,
                 operateur, nb2, tot))
    else:
        f0.write('    \\item $\\ldots\\ldots %s %s = %s$\n' % (operateur,
                 nb2, tot))
        f1.write('    \\item $\\mathbf{%s} %s %s = %s$\n' % (nb1,
                 operateur, nb2, tot))


def plus(valeurmax):
    (a, b) = (outils.valeur_alea(1, valeurmax), outils.valeur_alea(1,
              valeurmax))
    return (a, b)


def moins(valeurmax):
    (a, b) = (outils.valeur_alea(1, valeurmax), outils.valeur_alea(1,
              valeurmax))
    return (a + b, a)


def div(valeurmax):
    (a, b) = (outils.valeur_alea(1, valeurmax), outils.valeur_alea(1,
              valeurmax))
    return (a * b, a)


#===============================================================================
# PRODUITS ET QUOTIENTS PAR 10, 100, 1000
#===============================================================================


def tex_dix(f0, f1):
    nb = 4  # nb de calculs de chaque type
    l = valeurs10(nb)
    for i in range(len(l)):
        j = random.randrange(0, len(l))
        tex_formule_dix(l.pop(j), f0, f1)


def tex_formule_dix(l, f0, f1):
    if l[2] == '*':
        alea = random.randrange(0, 5)
        if alea > 1:
            f0.write('        \\item $%s \\quad\\times\\quad %s \\quad = \\quad \\dotfill$\n' %
                     (outils.sepmilliers(l[0], 1), outils.sepmilliers(l[1],
                     1)))
            f1.write('        \\item $%s \\times %s = \\mathbf{%s}$\n' %
                     (outils.sepmilliers(l[0], 1), outils.sepmilliers(l[1],
                     1), outils.sepmilliers(l[0] * l[1], 1)))
        elif alea > 0:
            f0.write('        \\item $%s \\quad\\times\\quad \\dotfill \\quad = \\quad %s$\n' %
                     (outils.sepmilliers(l[0], 1), outils.sepmilliers(l[0] *
                     l[1], 1)))
            f1.write('        \\item $%s \\times \\mathbf{%s} = %s$\n' %
                     (outils.sepmilliers(l[0], 1), outils.sepmilliers(l[1],
                     1), outils.sepmilliers(l[0] * l[1], 1)))
        else:
            f0.write('        \\item $\\dotfill \\quad\\times\\quad %s \\quad = \\quad %s$\n' %
                     (outils.sepmilliers(l[1], 1), outils.sepmilliers(l[0] *
                     l[1], 1)))
            f1.write('        \\item $\\mathbf{%s} \\times %s = %s$\n' %
                     (outils.sepmilliers(l[0], 1), outils.sepmilliers(l[1],
                     1), outils.sepmilliers(l[0] * l[1], 1)))
    else:
        alea = random.randrange(0, 5)
        if alea > 1:
            f0.write('        \\item $%s \\quad\\div\\quad %s \\quad = \\quad \\dotfill$\n' %
                     (outils.sepmilliers(l[0], 1), outils.sepmilliers(l[1],
                     1)))
            f1.write('        \\item $%s \\div %s = \\mathbf{%s}$\n' % (outils.sepmilliers(l[0],
                     1), outils.sepmilliers(l[1], 1), outils.sepmilliers(l[0] /
                     l[1], 1)))
        elif alea > 0:
            f0.write('        \\item $%s \\quad\\div\\quad \\dotfill \\quad = \\quad %s$\n' %
                     (outils.sepmilliers(l[0], 1), outils.sepmilliers(l[0] /
                     l[1], 1)))
            f1.write('        \\item $%s \\div \\mathbf{%s} = %s$\n' % (outils.sepmilliers(l[0],
                     1), outils.sepmilliers(l[1], 1), outils.sepmilliers(l[0] /
                     l[1], 1)))
        else:
            f0.write('        \\item $\\dotfill \\quad\\div\\quad %s \\quad = \\quad %s$\n' %
                     (outils.sepmilliers(l[1], 1), outils.sepmilliers(l[0] /
                     l[1], 1)))
            f1.write('        \\item $\\mathbf{%s} \\div %s = %s$\n' % (outils.sepmilliers(l[0],
                     1), outils.sepmilliers(l[1], 1), outils.sepmilliers(l[0] /
                     l[1], 1)))


def valeurs10(nb):  # renvoie nb valeur de chaque type : *10, /10, *0.1
    l = []
    for i in range(nb):
        if random.randrange(0, 1):
            l.append((outils.valeur_alea(111, 999) * 10 ** random.randrange(-3,
                     0), 10 ** (i + 1), '*'))
        else:
            l.append((10 ** (i + 1), outils.valeur_alea(111, 999) * 10 **
                     random.randrange(-3, 0), '*'))
    for i in range(nb):
        l.append((outils.valeur_alea(111, 999) * 10 ** random.randrange(-3,
                 0), 10 ** (i + 1), '/'))
    for i in range(nb):
        if random.randrange(0, 1):
            l.append((outils.valeur_alea(111, 999) * 10 ** random.randrange(-3,
                     0), 10 ** (-i - 1), '*'))
        else:
            l.append((10 ** (-i - 1), outils.valeur_alea(111, 999) * 10 **
                     random.randrange(-3, 0), '*'))
    return l


