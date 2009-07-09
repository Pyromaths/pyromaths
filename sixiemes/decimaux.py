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

import operations
import outils
import random

#===============================================================================
# Écrire un nombre en lettres ou en chiffres
#===============================================================================


def NombreEnLettres(n, France=True):
    unite = {
        1: "un",
        2: 'deux',
        3: 'trois',
        4: 'quatre',
        5: 'cinq',
        6: 'six',
        7: 'sept',
        8: 'huit',
        9: 'neuf',
        10: 'dix',
        11: 'onze',
        12: 'douze',
        13: 'treize',
        14: 'quatorze',
        15: 'quinze',
        16: 'seize',
        17: 'dix-sept',
        18: 'dix-huit',
        19: 'dix-neuf',
        }
    dizaineF = {2: 'vingt', 3: 'trente', 4: 'quarante', 5: 'cinquante',
                6: 'soixante', 7: "", 8: 'quatre-vingt', 9: ""}
    dizaineB = {2: 'vingt', 3: 'trente', 4: 'quarante', 5: 'cinquante',
                6: 'soixante', 7: 'septante', 8: 'octante', 9: 'nonante'}
    coefs = {0: 'cent', 1: 'mille', 2: 'million', 3: 'milliard'}
    result = ""

  # Cas particulier de zéro

    if n == 0:
        result = 'z\xe9ro'
    else:
        coef = 0

        while n > 0:

        # Récupération de l'unité du bloc de trois chiffres en cours

            u = n % 10
            n = n / 10

        # Récupération de la dizaine du bloc de trois chiffres en cours

            d = n % 10
            n = n / 10

        # Traitement des dizaines

            temp = ""

        # Passage sur la dizaine inférieure pour 10 à 19
        # et pour 70-79 90-99 dans le cas de la France

            if d == 1 or (d == 7 or d == 9) and France:
                d = d - 1
                u = u + 10
            if d > 1:
                if France:
                    if n:
                        temp = '-' + dizaineF[d]
                        None
                    else:
                        temp = dizaineF[d]
                        None

            # Ajout du cas particulier de 'et' entre la dizaine et 1

                    if d < 8 and (u == 1 or u == 11):
                        temp = temp + '-et'
                        None
                else:
                    if n:
                        temp = '-' + dizaineB[d]
                    else:
                        temp = dizaineB[d]

              # Ajout du cas particulier de 'et' entre la dizaine et 1

                    if u == 1:
                        temp = temp + '-et'

        # ajout du texte de l'unité

            if u > 0 and (d or n):
                temp = temp + '-' + unite[u]
            elif u > 0:
                temp = unite[u]

        # ajout du 's' à Quatre-vingt si rien ne suit
        #if (result == '') and (d == 8) and (u == 0) and France : result = 's'

            if d == 8 and u == 0 and France:
                temp = temp + 's'
            result = temp + result

        # Récupération de la centaine du bloc de trois chiffres en cours

            c = n % 10
            n = n / 10
            if c > 0:
                temp = ""
                None
                if c > 1 and n:
                    temp = '-' + unite[c]
                elif c > 1:
                    temp = unite[c]
                if c == 1 and not n:
                    temp = coefs[0]
                else:
                    temp = temp + '-' + coefs[0]

          # Traitement du cas particulier du 's' à cent si rien ne suit

                if result == "" and c > 1:
                    result = 's'
                result = temp + result

        # Traitement du prochain groupe de 3 chiffres

            if n > 0:
                coef = coef + 1
                i = n % 1000
                if i > 1 and coef > 1:
                    result = 's' + result

          # Traitement du cas particulier 'mille' ( non pas 'un mille' )

                if i == 1 and coef == 1:
                    n = n - 1
                    result = coefs[coef] + result
                elif i > 0:

                    result = '-' + coefs[coef] + result

    return result


def nombreATrouver():

    # a contient la liste des nombres à créer où il peut ne pas y avoir de centaines,
    # de centaines de milliers, d'unités ou de milliers

    a = [random.randrange(100) + random.randrange(1000) * 10 ** 3,
         random.randrange(1000) + random.randrange(100) * 10 ** 3,
         random.randrange(1000) * 10 ** 3, random.randrange(1000)]
    (lnb, list) = ([], [])
    for i in xrange(4):
        lnb.append(random.randrange(1, 1000) * 10 ** 6 + a[i])
    for i in xrange(4):
        n = a[i]
        if n % 1000:  # il y a des unités dans le nombre
            lnb.append(n * 10 ** (-random.randrange(1, 4)))
        else:
            lnb.append(n * 10 ** (-random.randrange(4, 7)))
    for i in xrange(8):
        list.append(lnb.pop(random.randrange(len(lnb))))
    return list


def EcritNombreDecimal(n):
    txt = ""
    if n != int(n):

        #n n'est pas un nombre entier

        (e, d) = str(n).split('.')
        (e, d) = (int(e), int(d))
    else:
        (e, d) = (int(n), 0)
    if not d:
        txt = NombreEnLettres(e)
    elif e:
        txt = NombreEnLettres(e)
    if d:
        partieDec = [" dixi\xe8me", " centi\xe8me", " milli\xe8me"]
        if txt.rfind("un") == len(txt) - 2:

        # le texte se finit par un. On l'accorde en genre avec unité

            txt = txt + "e"
        if e == 1:
            txt = txt + ' unit\xe9 et '
        if e > 1:
            txt = txt + ' unit\xe9s et '
        txt = txt + NombreEnLettres(d) + partieDec[len(str(d)) - 1]
        if d > 1:
            txt = txt + 's'
    return txt


def EcritEnChiffre(f0, f1):
    lnb = nombreATrouver()
    for i in xrange(8):
        f0.write("      \\item " + EcritNombreDecimal(lnb[i]) +
                 " : \\dotfill\n")
        f1.write("      \\item " + EcritNombreDecimal(lnb[i]) + " : ")
        f1.write(outils.sepmilliers(lnb[i], 0) + '\n')


def EcritEnLettre(f0, f1):
    lnb = nombreATrouver()
    for i in xrange(8):
        f0.write("      \\item " + outils.sepmilliers(lnb[i], 0) +
                 " : \\dotfill\n")
        f1.write("      \\item " + outils.sepmilliers(lnb[i], 0) + " : ")
        f1.write(EcritNombreDecimal(lnb[i]) + '\n')


#===============================================================================
# Conversions
#===============================================================================

units = ["L", "m", "g"]
division = ["k", "h", "da", "", "d", "c", "m"]


def valeurs_units():
    """
    renvoie les valeurs pour les conversions d'unit\xc3\xa9s
    """

    a = outils.valeur_alea(101, 999)
    p = random.randrange(-2, 0)
    unit = random.randrange(3)
    if unit:  #mètres ou grammes, on peut utiliser les k
        imax = 7
    else:

          #Litres, donc pas de kL

        imax = 6
    div0 = random.randrange(imax)
    if not unit:
        div0 = div0 + 1
    while 1:
        div1 = random.randrange(imax)
        if not unit:
            div1 = div1 + 1
        if div0 != div1:
            break
    return (a, p, unit, div0, div1)


def tex_units(f0, f1):
    """
    \xc3\x89crit l'exercice sur les conversions d'unit\xc3\xa9s et le corrig\xc3\xa9 au format
    LaTeX
    @param f0: fichier exercices
    @param f1: fichier corrige
    """

    for i in xrange(6):
        (a, p, unit, div0, div1) = valeurs_units()
        if unit:
            u = tuple([units[unit] for i in xrange(7)])
        else:
            u = tuple([units[unit] for i in xrange(6)])
        nb0 = operations.outils.sepmilliers(a * 10 ** p, 0)
        nb1 = operations.outils.sepmilliers(a * 10 ** ((p + div1) - div0),
                0)
        f0.write("    \\item %s~%s%s=\dotfill~%s%s\n" % (nb0, division[div0],
                 units[unit], division[div1], units[unit]))
        f1.write("    \\item %s~%s%s=%s~%s%s\\par\n" % (nb0, division[div0],
                 units[unit], nb1, division[div1], units[unit]))
        nblist = [nb0[i] for i in xrange(len(nb0))]
        if nblist.count(','):
            chf_unite = nblist.index(',') - 1
            nblist.pop(chf_unite + 1)
        else:
            chf_unite = len(nblist) - 1
        if unit:
            tex_tableau_autres(f1, div0, u, nblist, chf_unite)
        else:
            tex_tableau_litres(f1, div0, u, nblist, chf_unite)
        f1.write("      \\end{tabular}\n")


def tex_tableau_autres(f1, div0, u, nblist, chf_unite):
    f1.write("      \\begin{tabular}{c|c|c|c|c|c|c}\n")
    f1.write("        k%s & h%s & da%s & %s & d%s & c%s & m%s \\\\ \\hline\n" %
             u)
    for i in xrange(-div0 + chf_unite):
        tmp = nblist.pop(0)
        nblist[0] = tmp + nblist[0]

    for i in xrange(div0 - chf_unite):
        nblist.insert(0, '0')

    for i in xrange(-7 + len(nblist)):
        tmp = nblist.pop(7)
        nblist[6] = nblist[6] + tmp

    for i in xrange(7 - len(nblist)):
        nblist.append('0')

    f1.write("        %s & %s & %s & %s & %s & %s & %s\n" % tuple(nblist))


def tex_tableau_litres(f1, div0, u, nblist, chf_unite):
    f1.write("      \\begin{tabular}{c|c|c|c|c|c}\n")
    f1.write("        h%s & da%s & %s & d%s & c%s & m%s \\\\ \\hline\n" %
             u)
    for i in xrange(-div0 + 1 + chf_unite):
        tmp = nblist.pop(0)
        nblist[0] = tmp + nblist[0]

    for i in xrange((div0 - 1) - chf_unite):
        nblist.insert(0, '0')

    for i in xrange(-6 + len(nblist)):
        tmp = nblist.pop(6)
        nblist[5] = nblist[5] + tmp

    for i in xrange(6 - len(nblist)):
        nblist.append('0')

    f1.write("        %s & %s & %s & %s & %s & %s\n" % tuple(nblist))


#===============================================================================
# Placer une virgule
#===============================================================================

valeurs = ["milliers", "centaines", "dizaines", "unit\xe9s",
           "dixi\xe8mes", "centi\xe8mes", "milli\xe8mes"]


def valeurs_decimaux():
    """
    Choisit les valeurs
    """

    nb = 0
    chiffres = [
        1,
        2,
        3,
        4,
        5,
        6,
        7,
        8,
        9,
        ]
    for i in xrange(6):
        nb = nb + chiffres.pop(random.randrange(len(chiffres))) * 10 ** \
            i
    return nb


def tex_place_virgule(f0, f1):
    """
    \xc3\x89crit un exercices demandant de placer une virgule dans un nombre.
    @param f0: fichier exerices
    @param f1:fichier corrig\xc3\xa9
    """

    valeurs_index = [0, 1, 2, 3, 4, 5, 6]
    nb = valeurs_decimaux()
    f0.write("""Placer une virgule (en ajoutant \xe9ventuellement des z\xe9ros) dans le nombre
%s de telle sorte que :
""" %
             nb)
    f0.write('\\begin{enumerate}\n')
    f1.write("""Placer une virgule (en ajoutant \xe9ventuellement des z\xe9ros) dans le nombre
%s de telle sorte que :
""" %
             nb)
    f1.write('\\begin{enumerate}\n')
    for i in xrange(6):
        dec = [str(nb)[i] for i in xrange(len(str(nb)))]
        index_dec = random.randrange(6)
        index_valeurs = valeurs_index.pop(random.randrange(len(valeurs_index)))
        f0.write("  \\item le chiffre %s soit le chiffre des %s : " % (dec[index_dec],
                 valeurs[index_valeurs]))
        f1.write("  \\item le chiffre %s soit le chiffre des %s : " % (dec[index_dec],
                 valeurs[index_valeurs]))
        resultat = ecrit_nombre_decimal(dec, (index_dec + 4) -
                index_valeurs)
        f0.write('\\dotfill\n')
        f1.write(operations.outils.sepmilliers(resultat, 0) + '\n')
    f0.write('\\end{enumerate}\n')
    f1.write('\\end{enumerate}\n')


def ecrit_nombre_decimal(dec, index):
    """
    Renvoie une chaine de caract\xc3\xa8re repr\xc3\xa9sentant le nombre dec avec la virgule \xc3\xa0 la place index.
    Ajoute les z\xc3\xa9ros n\xc3\xa9cessaires.
    @param dec: d\xc3\xa9composition d'un nombre entier
    @param index: place de la virgule dans la liste dec
    """

    if index < 1:
        dec.insert(0, '0')
        dec.insert(1, '.')
        for i in xrange(-index):
            dec.insert(2, '0')
    elif index < len(dec):
        dec.insert(index, '.')
    else:
        for i in xrange(index - len(dec)):
            dec.append('0')
    strnb = ""
    for i in xrange(len(dec)):
        strnb = strnb + dec[i]
    return strnb


#===============================================================================
#    Écriture fractionnaire
#===============================================================================


def valeurs_frac():
    n1 = random.randrange(11, 10000)
    p1 = random.randrange(1, 4)
    return (n1, p1)


def choix_trou_frac(f0, f1, n1, p1):
    i = random.randrange(3)
    p2 = random.randrange(2)  #sert à compliquer un peu l'exercice
    if i > 1:
        f0.write('\\cfrac{%s}{%s}=\\ldots$\n' % (operations.outils.sepmilliers(n1 *
                 10 ** p2), operations.outils.sepmilliers(10 ** (p1 + p2))))
    elif i > 0:
        f0.write('\\cfrac{%s}{\ldots}=%s$\n' % (operations.outils.sepmilliers(n1 *
                 10 ** p2), operations.outils.sepmilliers(n1 * 10 ** (-p1),
                 1)))
    else:
        f0.write('\\cfrac{\ldots}{%s}=%s$\n' % (operations.outils.sepmilliers(10 **
                 (p1 + p2)), operations.outils.sepmilliers(n1 * 10 ** (-p1),
                 1)))
    f1.write('\\cfrac{%s}{%s}=%s$\n' % (operations.outils.sepmilliers(n1 *
             10 ** p2), operations.outils.sepmilliers(10 ** (p1 + p2)),
             operations.outils.sepmilliers(n1 * 10 ** (-p1), 1)))


def tex_frac(f0, f1):
    for i in xrange(6):
        f0.write('    \\item $')
        f1.write('    \\item $')
        (nombre, puissance) = valeurs_frac()
        choix_trou_frac(f0, f1, nombre, puissance)


#===============================================================================
#    Décomposition des nombres décimaux
#===============================================================================


def valeurs_dec():
    lpuissances = [3, 2, 1, 0, -1, -2, -3]
    p = []
    v = []
    for i in xrange(3):
        p.append(lpuissances.pop(random.randrange(len(lpuissances))))
        v.append(random.randrange(1, 10))
    return (v, p)


def tex_decomposition(f0, f1, v, p):
    for i in xrange(3):
        if p[i] < 0:
            f0.write('%s\\times \\cfrac{1}{%s}' % (v[i], operations.outils.sepmilliers(10 **
                     (-p[i]), 1)))
            f1.write('%s\\times \\cfrac{1}{%s}' % (v[i], operations.outils.sepmilliers(10 **
                     (-p[i]), 1)))
        else:
            f0.write('%s\\times %s' % (v[i], operations.outils.sepmilliers(10 **
                     p[i], 1)))
            f1.write('%s\\times %s' % (v[i], operations.outils.sepmilliers(10 **
                     p[i], 1)))
        if i < 2:
            f0.write('+')
            f1.write('+')
        else:
            f0.write('=')
            f1.write('=')
    f0.write('\\dotfill$\n')
    f1.write('%s$\n' % operations.outils.sepmilliers(v[0] * 10 ** p[0] +
             v[1] * 10 ** p[1] + v[2] * 10 ** p[2], 1))


def tex_dec(f0, f1):
    for i in xrange(6):
        f0.write('    \\item $')
        f1.write('    \\item $')
        (chiffres, puissances) = valeurs_dec()
        tex_decomposition(f0, f1, chiffres, puissances)


#===============================================================================
# Classer des nombres dans l'ordre
#===============================================================================


def choix_nombres():
    nb = []
    unite = random.randrange(10)
    for i in xrange(3):
        n = unite
        for j in xrange(i + 1):
            n = n + random.randrange(1, 10) * 10 ** (-(j + 1))
        nb.append(n)
    n = random.randrange(10) + random.randrange(10) / 10.0
    while n == nb[0]:
        n = random.randrange(10) + random.randrange(10) / 10.0
    nb.append(n)
    return nb


def classer(f0, f1):
    lnb = choix_nombres()
    lnb = outils.melange_liste(lnb)
    if random.randrange(2):
        ordre = "croissant"
    else:
        ordre = "d\xe9croissant"
    f0.write("Classer les nombres suivants dans l'odre %s.\\par\n    " %
             ordre)
    f1.write("Classer les nombres suivants dans l'odre %s.\\par\n    " %
             ordre)
    for i in xrange(len(lnb)):
        if i:
            f0.write(" \\kern1cm ; \\kern1cm ")
            f1.write(" \\kern1cm ; \\kern1cm ")
        f0.write(outils.sepmilliers(lnb[i], 0))
        f1.write(outils.sepmilliers(lnb[i], 0))
    lnb.sort()
    if ordre == "croissant":
        ordre = "\\textless"
    else:
        ordre = "\\textgreater"
        lnb.reverse()
    f1.write("\\par\n    ")
    for i in xrange(len(lnb)):
        if i:
            f1.write(" \\kern1cm %s \\kern1cm " % ordre)
        f1.write(outils.sepmilliers(lnb[i], 0))


