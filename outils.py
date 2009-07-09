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
# ------------------- OUTILS -------------------

from random import randrange
import string
import os
import math


def ecrit_tex(file, formule, cadre=None, thenocalcul='\\thenocalcul = ',
              tabs=1):

                        # ecrit la ligne dans le fichier

    if formule != '':
        if cadre == None or not cadre:
            file.write(('  \\[ %s%s \\] \n').expandtabs(2 * tabs) % (thenocalcul,
                       formule))
        else:
            file.write(('  \\[ \\boxed{%s%s} \\] \n').expandtabs(2 *
                       tabs) % (thenocalcul, formule))


def pgcd(a, b):  # calcule le pgcd positif des nombres entiers a et b
    (a, b) = (abs(a), abs(b))
    if a < b:
        (a, b) = (b, a)
    while b > 0:
        (a, b) = (b, a % b)
    return abs(a)


def ppcm(a, b):  # calcule le ppcm positif des nombres entiers a et b
    return abs((a * b) / pgcd(a, b))


def signe(a):  # renvoie 1 si a est>0, -1 si a<0
    if a < 0:
        return -1
    else:
        return 1


def valeur_alea(a, b):  # choisit une valeur comprise entre a et b non nulle
    while True:
        alea = randrange(a, b + 1)
        if alea != 0:
            return alea
            break


def tex_entete(fichier):  #ecrit l'entete du document tex
    fichier.write('\\documentclass[a4paper,11pt]{article}\n')
    fichier.write('\\usepackage[latin1]{inputenc}\n')
    fichier.write('\\usepackage[frenchb]{babel}\n')
    fichier.write('\\usepackage[fleqn]{amsmath}\n')
    fichier.write('\\usepackage{amssymb,multicol,calc,vmargin,cancel,fancyhdr,units,pst-eucl,wrapfig,lastpage,wasysym,pst-plot,tabularx}\n')
    fichier.write('\\setmarginsrb{1.5cm}{1.5cm}{1.5cm}{1.5cm}{.5cm}{.5cm}{.5cm}{1.cm}\n')
    fichier.write('\\newcounter{exo}\n')
    fichier.write('\\setlength{\\headheight}{18pt}\n')
    fichier.write('\\setlength{\\fboxsep}{1em}\n')
    fichier.write('\\setlength\\parindent{0em}\n')
    fichier.write('\\setlength\\mathindent{0em}\n')
    fichier.write('\\setlength{\\columnsep}{30pt}\n')
    fichier.write('\\usepackage[ps2pdf,pagebackref=true,colorlinks=true,linkcolor=blue,plainpages=true]{hyperref}\n')
    fichier.write('\\hypersetup{pdfauthor={J\xe9r\xf4me Ortais},pdfsubject={Exercices de math\xe9matiques},')
    fichier.write('pdftitle={Exercices cr\xe9\xe9s par Pyromaths, un programme en Python de J\xe9r\\^ome Ortais}}\n')
    fichier.write('\\makeatletter\n')
    fichier.write('\\newcommand\\styleexo[1][]{\n')
    fichier.write('  \\renewcommand{\\theenumi}{\\arabic{enumi}}\n')
    fichier.write('  \\renewcommand{\\labelenumi}{$\\blacktriangleright$\\textbf{\\theenumi.}}\n')
    fichier.write('  \\renewcommand{\\theenumii}{\\alph{enumii}}\n')
    fichier.write('  \\renewcommand{\\labelenumii}{\\textbf{\\theenumii)}}\n')
    fichier.write('  {\\fontfamily{pag}\\fontseries{b}\\selectfont \\underline{#1 \\theexo}}\n')
    fichier.write('  \\par\\@afterheading\\vspace{0.5\\baselineskip minus 0.2\\baselineskip}}\n')

    fichier.write('\\newcommand*\\exercice{%\n')
    fichier.write('  \\psset{unit=1cm}\n')
    fichier.write('  \\ifthenelse{\\equal{\\theexo}{0}}{}{\\filbreak}\n')
    fichier.write('  \\refstepcounter{exo}%\n')
    fichier.write('  \\par\\addvspace{1.5\\baselineskip minus 1\\baselineskip}%\n')
    fichier.write('  \\@ifstar%\n')
    fichier.write('  {\\penalty-130\\styleexo[Corrig\xe9 de l\'exercice]}%\n')
    fichier.write('  {\\filbreak\\styleexo[Exercice]}%\n')
    fichier.write('  }\n')

    fichier.write('\\makeatother\n')
    fichier.write('\\count1=\\year \\count2=\\year \\ifnum\\month<8\\advance\\count1by-1\\else\\advance\\count2by1\\fi\n')
    fichier.write('\\pagestyle{fancy}\n')
    fichier.write('\\cfoot{\\textsl{\\footnotesize{Ann\xe9e \\number\\count1/\\number\\count2}}}\n')
    fichier.write('\\rfoot{\\textsl{\\tiny{http://www.pyromaths.org}}}\n')
    fichier.write('\\lhead{\\textsl{\\footnotesize{Page \\thepage/ \\pageref{LastPage}}}}\n')
    fichier.write('\\begin{document}\n')
    fichier.write('\\newcounter{nocalcul}[exo]\n')
    fichier.write('''\\renewcommand{\\thenocalcul}{\\Alph{nocalcul}}
\\raggedcolumns
''')


#def pyromin(a, b):
#    if a < b:
#        return a
#    else:
#        return b
#
#
#def pyromax(a, b):
#    if a > b:
#        return a
#    else:
#        return b


def sepmilliers(nb, mathenvironment=0):

    # Insère les espaces fines pour séparer les milliers et remplace le point
    # décimal par une virgule

    dec = [str(nb)[i] for i in xrange(len(str(nb)))]
    if dec.count('e'):  #nb ecrit en notation scientifique
        exposant = int(('').join(dec[dec.index('e') + 1:]))
        dec = dec[:dec.index('e')]
        lg = len(dec)
        if dec.count('.'):
            virg = dec.index('.')
            dec.remove('.')
        else:
            virg = len(dec)
        if virg + exposant < 0:  #L'ecriture decimale du nombre commence par 0,...
            dec2 = ['0', '.']
            for i in xrange(-virg - exposant):
                dec2.append('0')
            dec2.extend(dec)
            dec = dec2
        elif virg + exposant > lg:

            #L'ecriture decimale du nombre finit par des 0

            for i in xrange(-((lg - virg) - 1) + exposant):
                dec.append('0')
    dec2 = []
    if dec.count('.'):
        lavtvirg = dec.index('.')
        laprvirg = (len(dec) - dec.index('.')) - 1
    else:
        lavtvirg = len(dec)
        laprvirg = 0
    nbsep = lavtvirg // 3 + 1
    if lavtvirg > 3:
        cpt = lavtvirg % 3
        if cpt:
            dec2 = dec[0:cpt]
            dec2.append('\\,')
            nbsep = nbsep - 1
        for i in xrange(nbsep):
            dec2.extend(dec[cpt:cpt + 3])
            if nbsep - i > 1:
                dec2.append('\\,')
            cpt = cpt + 3
    else:
        if dec.count('.'):
            dec2 = dec[0:dec.index('.')]
        else:
            dec2 = dec
    if dec.count('.'):
        cpt = dec.index('.')
    else:
        cpt = len(dec)
    if laprvirg <= 3:
        dec2.extend(dec[cpt:])
    else:
        nbsep = laprvirg // 3 - 1
        dec2.extend(dec[cpt:cpt + 4])
        dec2.append('\\,')
        cpt = cpt + 4
        for i in xrange(nbsep):
            dec2.extend(dec[cpt:cpt + 3])
            if cpt + 3 < len(dec):
                dec2.append('\\,')
            cpt = cpt + 3
        dec2.extend(dec[cpt:])
    nb = ('').join(dec2)
    if nb.endswith('.0'):
        nb = string.rsplit(nb, '.0')[0]
    if mathenvironment:
        return string.join(string.rsplit(nb, sep='.'), ',')
    else:
        return string.join(string.rsplit(nb, sep='.'), '{,}')


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


def choix_points(n):
    """
    choisit n points parmi A, B, C, ..., Z
    @param n: nombre de points \xc3\xa0 choisir
    @type n: integer
    """

    points = [unichr(i + 65) for i in xrange(26)]
    liste = []
    for i in xrange(n):
        liste.append(points.pop(randrange(len(points))))
    return liste


def melange_liste(list):
    """M\xc3\xa9lange de fa\xc3\xa7on al\xc3\xa9atoire les \xc3\xa9l\xc3\xa8ment de la liste list
    @param list: liste
    """

    tmp = []
    lg = len(list)
    for i in xrange(lg):
        tmp.append(list.pop(randrange(len(list))))
    return tmp


def fusion(liste1, liste2):
    (i1, i2) = (0, 0)
    liste = []
    while i1 < len(liste1) and i2 < len(liste2):
        if liste1[i1] < liste2[i2]:
            liste.append(liste1[i1])
            i1 = i1 + 1
        else:
            liste.append(liste2[i2])
            i2 = i2 + 1
    if i1 == len(liste1):
        liste.extend(liste2[i2:])
    else:
        liste.extend(liste1[i1:])
    return liste


def trie_liste_croissant(liste):
    if len(liste) == 1:
        return liste
    else:
        milieu = len(liste) / 2
        liste_a_trier = fusion(trie_liste_croissant(liste[:milieu]),
                               trie_liste_croissant(liste[milieu:]))
        return liste_a_trier


def detecter_modules(repertoire):
    modules = [nom[:-3] for nom in os.listdir(repertoire) if nom.enswith(".py")]
    liste = []
    for module in modules:
        m = __import__(module)
        if hasattr(m, "main"):
            liste.append(m.main)
    return liste


def radians(alpha):
    # convertit un angle en degré en radians
    return alpha*math.pi/180

def degres(alpha):
    return alpha*180/math.pi
