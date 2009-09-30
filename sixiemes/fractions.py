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

import random
import math

#===============================================================================
# Fractions partage
#===============================================================================


def dimensions_rectangle():
    taille_max = 8
    while True:
        (l, h) = (random.randrange(4, taille_max), random.randrange(4,
                  taille_max))
        div_t = diviseurs(l * h)
        if len(div_t) > 3:
            break
    if l < h:
        (l, h) = (h, l)
    return (l, h)


def numerateur_denominateur(l, h, cas):
    """

    @param l: largeur
    @param h: longueur
    @param cas:
        - nid: numerateur < denominateur
        - un: numerateur = denominateur
        - nsd: numerateur > denominateur
    @type cas: string
    """

    ldiv = diviseurs(l * h)
    if cas == "un":
        d = random.randrange(3, l * h)
    else:
        while True:
            d = ldiv[random.randrange(len(ldiv) - 1)]
            if d > 2:
                break
    if cas == "un":
        n = d
    elif cas == "nid":
        n = random.randrange(1, d)
    else:
        n = random.randrange(d + 1, d * 2)
    return (n, d)


def trace_rectangle(f0, f1, l, h, cas):
    f0.write("        \\multips(0,0)(1,0){17}{\\psline[linecolor=lightgray](0,0)(0,%s)}\n" %
             h)
    f1.write("        \\multips(0,0)(1,0){17}{\\psline[linecolor=lightgray](0,0)(0,%s)}\n" %
             h)
    f0.write("        \\multips(0,0)(0,1){%s}{\\psline[linecolor=lightgray](0,0)(16,0)}\n" %
             (h + 1))
    f1.write("        \\multips(0,0)(0,1){%s}{\\psline[linecolor=lightgray](0,0)(16,0)}\n" %
             (h + 1))
    f0.write("        \\psframe[linewidth=1.5\\pslinewidth](0,0)(%s,%s)\n" %
             (l, h))
    f1.write("        \\psframe[linewidth=1.5\\pslinewidth](0,0)(%s,%s)\n" %
             (l, h))
    if cas == "nsd":
        f1.write("        \\psframe[linewidth=1.5\\pslinewidth](%s,0)(%s,%s)\n" %
                 (l + 1, 2 * l + 1, h))


def fractions_partage_corrige(l, h, n, d):
    div_l = diviseurs(l)
    div_h = diviseurs(h)
    div_d = diviseurs(d)
    (lc, hc) = (l, h)
    if n == d:
        (lc, hc) = (l, h)
    elif div_l.count(d):
        lc = l / d
    elif div_h.count(d):
        hc = h / d
    else:
        for i in range(len(div_d) - 1):
            if div_l.count(div_d[i + 1]) and div_h.count(d / div_d[i + 1]):
                (lc, hc) = (l / div_d[i + 1], (h * div_d[i + 1]) / d)
                break
    return (lc, hc)


def trace_partage(f1, l, h, lc, hc, cas):
    if lc < l:
        f1.write("        \\multips(%s,0)(%s,0){%s}{\\psline(0,0)(0,%s)}\n" %
                 (lc, lc, l / lc - 1, h))
        if cas == "nsd":
            f1.write("        \\rput(%s,0){\\multips(%s,0)(%s,0){%s}{\\psline(0,0)(0,%s)}}\n" %
                     (l + 1, lc, lc, l / lc - 1, h))
    if hc < h:
        f1.write("        \\multips(0,%s)(0,%s){%s}{\\psline(0,0)(%s,0)}\n" %
                 (hc, hc, h / hc - 1, l))
        if cas == "nsd":
            f1.write("        \\rput(%s,0){\\multips(0,%s)(0,%s){%s}{\\psline(0,0)(%s,0)}}\n" %
                     (l + 1, hc, hc, h / hc - 1, l))


def coloriage(f1, n, d, l, h, lc, hc):
    if n == d:
        f1.write("        \\psframe[fillstyle=solid,fillcolor=gray](0,0)(%s,%s)\n" %
                 (l, h))
    else:
        (x, y, nfig) = (0, 0, 0)
        for i in range(n):
            if nfig:
                f1.write("        \\rput(%s,0){\\psframe[fillstyle=solid,fillcolor=gray](%s,%s)(%s,%s)}\n" %
                         (nfig, x, y, x + lc, y + hc))
            else:
                f1.write("        \\psframe[fillstyle=solid,fillcolor=gray](%s,%s)(%s,%s)\n" %
                         (x, y, x + lc, y + hc))
            if x + lc < l:
                x = x + lc
            elif y + hc < h:
                (x, y) = (0, y + hc)
            else:
                (x, y, nfig) = (0, 0, l + 1)


def diviseurs(n):
    l = []
    for i in range(1, int(math.sqrt(n)) + 1):
        if not n % i:
            l.append(i)
            if i != n // i:
                l.append(n // i)
    l.sort()
    return l


def exo_fraction_partage(f0, f1):
    lcas = ["nid", "un", "nsd", "nid", "nsd"]
    for i in range(4):
        cas = lcas.pop(random.randrange(len(lcas)))
        if cas == "nsd":
            while True:
                (l, h) = dimensions_rectangle()
                if l < 8:
                    break
        else:
            (l, h) = dimensions_rectangle()
        (n, d) = numerateur_denominateur(l, h, cas)
        (lc, hc) = fractions_partage_corrige(l, h, n, d)

        f0.write("    \\item Colorer $\\frac{%s}{%s}$ de ce rectangle.\\par\n" %
                 (n, d))
        f1.write("    \\item Colorer $\\frac{%s}{%s}$ de ce rectangle.\\par\n" %
                 (n, d))
        f0.write("      \\psset{unit=4mm}\n")
        f1.write("      \\psset{unit=4mm}\n")
        f0.write("      \\begin{pspicture}(16,%s)\n" % h)
        f1.write("      \\begin{pspicture}(16,%s)\n" % h)
        (lc, hc) = fractions_partage_corrige(l, h, n, d)
        coloriage(f1, n, d, l, h, lc, hc)
        trace_rectangle(f0, f1, l, h, cas)
        trace_partage(f1, l, h, lc, hc, cas)
        f0.write("      \\end{pspicture}\n")
        f1.write("      \\end{pspicture}\n")
        if i == 1:
            f0.write("      \\columnbreak\n")
            f1.write("      \\columnbreak\n")


#===============================================================================
# Fractions et abscisses
#===============================================================================


def valeurs_abscisses():
    origine = random.randrange(3, 11)
    nb_divisions = (
        6,
        8,
        9,
        10,
        12,
        14,
        15,
        16,
        18,
        20,
        )
    div = nb_divisions[random.randrange(len(nb_divisions))]
    nb_subd = diviseurs(div)
    subd = nb_subd[random.randrange(len(nb_subd) - 2) + 1]
    while subd < 3:
        subd = nb_subd[random.randrange(len(nb_subd) - 2) + 1]
    nb_grad = 58  #nb de graduations sur la demi-droite graduée
    lpts = [0 for i in range(7)]  #liste des places des points à trouver/placer sur la 1/2 droite graduée
    lpts[4] = random.randrange(1, nb_grad // div + 1) * div
    for i in range(2):
        a = random.randrange(1, nb_grad)
        while lpts.count(a):
            a = random.randrange(1, nb_grad)
        lpts[i] = a
    for i in range(2):
        a = random.randrange(1, (nb_grad * subd) // div)
        while lpts.count((a * div) // subd):
            a = random.randrange(1, (nb_grad * subd) // div)
        lpts[i + 2] = (a * div) // subd
    for i in range(2):
        a = random.randrange(1, (nb_grad * subd) // div)
        while lpts.count((a * div) // subd):
            a = random.randrange(1, (nb_grad * subd) // div)
        lpts[i + 5] = (a * div) // subd

    #npts=noms_pts(7)

    npts = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
    lnum = list(range(7))  #liste des numérateurs
    lnum[0] = origine * div + lpts[0]
    lnum[1] = origine * div + lpts[1]
    lnum[2] = origine * subd + (lpts[2] * subd) // div
    lnum[3] = origine * subd + (lpts[3] * subd) // div
    lnum[4] = random.randrange(3, div)
    while diviseurs(div).count(lnum[4]):
        lnum[4] = random.randrange(3, div)
    lnum[5] = origine * div + lpts[5]
    lnum[6] = origine * div + lpts[6]
    return (origine, div, subd, lpts, npts, lnum)


def noms_pts(nb):  # renvoie nb noms de points
    (listenb, listepts) = ([], [])
    for i in range(26):
        listenb.append(i + 65)
    for i in range(nb):
        listepts.append(chr(listenb.pop(random.randrange(26 - i))))
    listepts.sort()
    return listepts


def unites_fractions(f0, f1, origine, div, subd):
    postf = 'ièmes'
    lch = [
        'cinqu',
        'six',
        'sept',
        'huit',
        'neuv',
        'dix',
        'onz',
        'douz',
        'treiz',
        'quatorz',
        'quinz',
        'seiz',
        'dix-sept',
        'dix-huit',
        'dix-neuv',
        'vingt',
        ]
    lfr = dict([(i + 5, lch[i] + postf) for i in range(len(lch))])
    lfr[2] = 'demis'
    lfr[3] = 'tiers'
    lfr[4] = 'quarts'
    f0.write('        \\item 1 unité = \\ldots~%s\n' % lfr[div])
    f0.write('        \\item 1 unité = \\ldots~%s\n' % lfr[subd])
    f0.write('        \\item %s unités = \\ldots~%s\n' % (origine,
             lfr[div]))
    f0.write('        \\item %s unités = \\ldots~%s\n' % (origine,
             lfr[subd]))
    f1.write('        \\item 1 unité = %s %s\n' % (div, lfr[div]))
    f1.write('        \\item 1 unité = %s %s\n' % (subd, lfr[subd]))
    f1.write('        \\item %s unités = %s %s\n' % (origine,
             origine * div, lfr[div]))
    f1.write('        \\item %s unités = %s %s\n' % (origine,
             origine * subd, lfr[subd]))


def trace_demi_droite(f0, f1, origine, div, subd, lpts, npts, lnum):
    f0.write("  \\psline[arrowscale=2]{->}(0,0)(18,0)\n")
    f0.write("  \\rput(2mm,0){%\n")
    f0.write("  \\multips(0,0)(3 mm,0){58}{\\psline(0,-.1)(0,.1)}\n")
    f0.write("  \\multips(0,0)(%s mm,0){%s}{\\psline(0,-.2)(0,.2)}\n" %
             (div * 3, 58 // div + 1))
    f1.write("  \\psline[arrowscale=2]{->}(0,0)(18,0)\n")
    f1.write("  \\rput(2mm,0){%\n")
    f1.write("  \\multips(0,0)(3 mm,0){58}{\\psline(0,-.1)(0,.1)}\n")
    f1.write("  \\multips(0,0)(%s mm,0){%s}{\\psline(0,-.2)(0,.2)}\n" %
             (div * 3, 58 // div + 1))
    for i in range(58 // div + 1):
        f0.write("  \\rput[t](%s mm,-3mm){\\centering %s}\n" % ((i * div) *
                 3, origine + i))
        f1.write("  \\rput[t](%s mm,-3mm){\\centering %s}\n" % ((i * div) *
                 3, origine + i))
    for i in range(2):
        f0.write("  \\rput[t](%s mm,4mm){\\centering $%s$}\n" % (lpts[i +
                 5] * 3 + .1, npts[i + 5]))
    for i in range(7):
        f1.write("  \\rput[t](%s mm,4mm){\\centering $%s$}\n" % (lpts[i] *
                 3 + .1, npts[i]))
    f0.write("  }\n")
    f1.write("  }\n")


def ecrit_abscisses(f0, f1, origine, div, subd, lpts, lnum):
    f0.write("        \\item $\\left(\\cfrac{%s}{%s}\\right)$\n" % (lnum[0],
             div))
    f0.write("        \\item $\\left(\\cfrac{%s}{%s}\\right)$\n" % (lnum[1],
             div))
    f0.write("        \\item $\\left(\\cfrac{%s}{%s}\\right)$\n" % (lnum[2],
             subd))
    f0.write("        \\item $\\left(\\cfrac{%s}{%s}\\right)$\n" % (lnum[3],
             subd))
    f0.write("        \\item $\\left(\\cfrac{%s}{%s}\\right)$\n" % (origine *
             lnum[4] + (lpts[4] / div) * lnum[4], lnum[4]))
    f1.write("        \\item $\\left(\\cfrac{%s}{%s}\\right)$\n" % (lnum[0],
             div))
    f1.write("        \\item $\\left(\\cfrac{%s}{%s}\\right)$\n" % (lnum[1],
             div))
    f1.write("        \\item $\\left(\\cfrac{%s}{%s}\\right)$\n" % (lnum[2],
             subd))
    f1.write("        \\item $\\left(\\cfrac{%s}{%s}\\right)$\n" % (lnum[3],
             subd))
    f1.write("        \\item $\\left(\\cfrac{%s}{%s}\\right)$\n" % (origine *
             lnum[4] + (lpts[4] / div) * lnum[4], lnum[4]))


def trouve_abscisses(f0, f1, div, subd, lnum):
    f0.write("        \\item $F~\\left(\\cfrac{\\ldots}{%s}\\right)$\n" %
             div)
    f0.write("        \\item $F~\\left(\\cfrac{\\ldots}{%s}\\right)$\n" %
             subd)
    f0.write("        \\item $G~\\left(\\cfrac{\\ldots}{%s}\\right)$\n" %
             div)
    f0.write("        \\item $G~\\left(\\cfrac{\\ldots}{%s}\\right)$\n" %
             subd)
    f1.write("        \\item $F~\\left(\\cfrac{%s}{%s}\\right)$\n" % (lnum[5],
             div))
    f1.write("        \\item $F~\\left(\\cfrac{%s}{%s}\\right)$\n" % ((lnum[5] *
             subd) / div, subd))
    f1.write("        \\item $G~\\left(\\cfrac{%s}{%s}\\right)$\n" % (lnum[6],
             div))
    f1.write("        \\item $G~\\left(\\cfrac{%s}{%s}\\right)$\n" % ((lnum[6] *
             subd) / div, subd))


def questions_fractions_abscisses(f0, f1):
    (origine, div, subd, lpts, npts, lnum) = valeurs_abscisses()
    f0.write("\\begin{enumerate}\n")
    f0.write("  \\item Compléter :\n")
    f0.write("    \\begin{multicols}{2}\n")
    f0.write("      \\begin{enumerate}\n")
    f1.write("\\begin{enumerate}\n")
    f1.write("  \\item Compléter :\n")
    f1.write("    \\begin{multicols}{2}\n")
    f1.write("      \\begin{enumerate}\n")
    unites_fractions(f0, f1, origine, div, subd)
    f0.write("      \\end{enumerate}\n")
    f0.write("    \\end{multicols}\n")
    f0.write("  \\item Sur la demi-droite ci-dessous, placer les points d'abscisse donnée :\n")
    f0.write("    \\begin{multicols}{5}\n")
    f0.write("      \\begin{enumerate}\n")
    f0.write("        \\renewcommand{\\theenumii}{\\Alph{enumii}}\n")
    f0.write("        \\renewcommand{\\labelenumii}{$\\theenumii$}\n")
    f1.write("      \\end{enumerate}\n")
    f1.write("    \\end{multicols}\n")
    f1.write("  \\item Sur la demi-droite ci-dessous, placer les points d'abscisse donnée :\n")
    f1.write("    \\begin{multicols}{5}\n")
    f1.write("      \\begin{enumerate}\n")
    f1.write("        \\renewcommand{\\theenumii}{\\Alph{enumii}}\n")
    f1.write("        \\renewcommand{\\labelenumii}{$\\theenumii$}\n")
    ecrit_abscisses(f0, f1, origine, div, subd, lpts, lnum)
    f0.write("      \\end{enumerate}\n")
    f0.write("    \\end{multicols}\n")
    f0.write("  \\item Compléter les abscisses des points suivants :\n")
    f0.write("    \\begin{multicols}{4}\n")
    f0.write("      \\begin{enumerate}")
    f1.write("      \\end{enumerate}\n")
    f1.write("    \\end{multicols}\n")
    f1.write("  \\item Compléter les abscisses des points suivants :\n")
    f1.write("    \\begin{multicols}{4}\n")
    f1.write("      \\begin{enumerate}")
    trouve_abscisses(f0, f1, div, subd, lnum)
    f0.write("      \\end{enumerate}\n")
    f0.write("    \\end{multicols}\n")
    f0.write("\\end{enumerate}\n")
    f0.write("\\begin{pspicture}(0,-.5)(18,.5)\n")
    f1.write("      \\end{enumerate}\n")
    f1.write("    \\end{multicols}\n")
    f1.write("\\end{enumerate}\n")
    f1.write("\\begin{pspicture}(0,-.5)(18,.5)\n")
    trace_demi_droite(f0, f1, origine, div, subd, lpts, npts, lnum)
    f0.write("\\end{pspicture}\n")
    f1.write("\\end{pspicture}\n")


