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
from __future__ import division
from __future__ import unicode_literals
from builtins import str
from builtins import range
from pyromaths import ex
from random import randrange, shuffle
#===============================================================================
# from pyromaths.outils import Priorites3
# from pyromaths.classes.Fractions import Fraction
# from pyromaths.classes.PolynomesCollege import Polynome, factoriser
# from pyromaths.classes.SquareRoot import SquareRoot
from pyromaths.outils.Arithmetique import valeur_alea
from pyromaths.outils.Affichage import decimaux
#===============================================================================

def PointsCourbes(sens_var=(-1, -1, 0, 1, 1), nb_var=(3, 5), absc=(-5, 5), ordo=(-4, 4), cstes=(0, 1)):
    """Définit les ordonnées entières dans [-5 ; 5] de points d'abscisses entières dans [-5 ; 5]
    de telle sorte que la fonction sur chaque intervalle comporte entre 3 et 5 variations différentes,
    une seule section pouvant être constante.
    La fonction doit avoir des images positives et négatives.
    variations= [[-1, -6, -2], [1, -2, 1], [-1, 1, 2], [0, 2, 4]]
    """
    while True:
        lY, sens, variations = [valeur_alea(ordo[0], ordo[1])], [], []
        nb_cste = 0
        for dummy in range(absc[1] - absc[0]):
            while True:
                lg = valeur_alea(1, 4)
                # pente maximale entre deux points consécutifs
                sens.append(sens_var[randrange(len(sens_var))])
                nY = lY[-1] + lg * sens[-1]
                if ordo[0] <= nY <= ordo[1]:
                    if nY * lY[-1] < 0: lY.append(0)
                    else: lY.append(nY)
                    if not variations or sens[-1] != variations[-1][0]:
                        variations.append([sens[-1], dummy + absc[0], dummy + absc[0] + 1])
                    else:
                        variations[-1][2] = dummy + absc[0] + 1
                    break
                else:
                    sens.pop(-1)
        if nb_var[0] <= len(variations) <= nb_var[1]:
            extremums = []
            gextr = [100, -100]  # extrema sur l'esnble de définition
            for i in range(len(variations)):
                if lY[variations[i][1] - absc[0]] > gextr[1]: gextr[1] = lY[variations[i][1] - absc[0]]
                elif lY[variations[i][1] - absc[0]] < gextr[0]: gextr[0] = lY[variations[i][1] - absc[0]]
                if extremums.count(lY[variations[i][1] - absc[0]]) > 0 and variations[i - 1][0] != 0:
                    nb_cste = cstes[1] + 1
                else:
                    extremums.append(lY[variations[i][1] - absc[0]])
                if variations[i][0] == 0:nb_cste += 1
            if extremums.count(lY[-1]): nb_cste = cstes[1] + 1
            if lY[-1] > gextr[1]: gextr[1] = lY[-1]
            elif lY[-1] < gextr[0]: gextr[0] = lY[-1]
            if gextr[0] * gextr[1] >= 0: nb_cste = cstes[1] + 1
            if cstes[0] <= nb_cste <= cstes[1]: break
    variations[-1][2] = absc[1]
    return lY, variations

def remplissage_tableau(lX, lY, variations):
    """Renvoie la liste des abscisses, des ordonnées et des zéros (position et abscisse)
    pour compléter un tableau de variations"""
    lAbsc = [str(v[1]) for v in variations] + [str(variations[-1][2])]
    lOrdo = []
    for index in range(len(variations)):
        lOrdo.append(lY[variations[index][1] - lX[0]])
    lOrdo.append(lY[-1])
    lZeros = []
    for absc in range(lX[0], lX[-1] + 1):
        if lY[absc - lX[0]] == 0:
            for index in range(len(variations)):
                if variations[index][1] < absc < variations[index][2]:
                    if variations[index][0] != 0:
                        lZeros.append([index + 1, index + 2, absc])
                    break
                if variations[index][1] == absc or variations[index][2] == absc:
                    break
    return lAbsc, lOrdo, lZeros

def integration_zeros(lX, lY, variations):
    """Renvoie la liste des abscisses et des ordonnées des extrema locaux et des zéros"""
    lAbs, lOrd, lZeros = remplissage_tableau(lX, lY, variations)
    lZeros.reverse()
    for z in lZeros:
        lAbs.insert(z[0], z[2])
        lOrd.insert(z[0], 0)
    return lAbs, lOrd


class Vf1SensEtTableau(ex.TexExercise):
    """Sens et Tableau de variations"""

    tags = ["Seconde"]

    def __init__(self):
        lX = [-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5]
        self.lX = lX
        self.lY1, self.variations1 = PointsCourbes(sens_var=(-1, 1))
        self.lY2, self.variations2 = PointsCourbes()



    def tex_statement(self):
        exo = [r'\exercice']
        exo.append(r'\begin{enumerate}')
        exo.append(_(u'\\item Quel est le sens de variation de la fonction $f$ ? Répondre par une phrase en précisant les intervalles.'))
        exo.append(_(r'\item Tracer les tableaux de variation des fonctions $f$ et $g$.'))
        exo.append(r'\end{enumerate}')
        exo.append(r'\begin{center}')
        exo.append('\\begin{asy}\n import graph;\n import interpolate;\n unitsize(5mm);')
        exo.append(r'defaultpen(fontsize(9pt));')
        exo.append(r'real[] xpt,ypt;')
        exo.append(r'real [] xpt={%s};' % (",".join([str(a).zfill(2) for a in self.lX])))
        exo.append(r'real [] ypt={%s};' % (",".join([str(a).zfill(2) for a in self.lY1])))
        exo.append(r'xlimits(-6.2, 6.2);')
        exo.append(r'ylimits(-5.2, 5.2);')
        exo.append(r'xaxis(axis=BottomTop, p=invisible,')
        exo.append(r'ticks=Ticks(format="%%", Step=1, extend=true,')
        exo.append(r'pTick=gray+.5, ptick=dotted)')
        exo.append(r');')
        exo.append(r'yaxis(axis=LeftRight, p=invisible,')
        exo.append(r'ticks=Ticks(format="%%", Step=1, extend=true,')
        exo.append(r'pTick=gray+.5, ptick=dotted)')
        exo.append(r');')
        exo.append(r'xequals(L="$y$", 0, extend=false, arrow=Arrow(HookHead, size=9pt), p=black+1,')
        exo.append(r'ticks=Ticks(scale(.7)*Label(filltype=Fill(white)), Step=1, Size=3pt,')
        exo.append(r'end=false, endlabel=false, beginlabel=false, NoZero));')
        exo.append(r'yequals(L="$x$", 0, extend=false, arrow=Arrow(HookHead, size=9pt), p=black+1,')
        exo.append(r'ticks=Ticks(scale(.7)*Label(filltype=Fill(white)), Step=1, Size=3pt,')
        exo.append(r'end=false, endlabel=false, beginlabel=false, NoZero));')
        exo.append(r'draw(graph(xpt,ypt,Hermite(monotonic)),brown+1.5);')
        exo.append(r'labelx(L=scale(.7)*"$0$", (0,0), align=SW);')
        exo.append(r'label(L="$\mathcal{C}_f$", (%s,%s), align=%s);' % (self.lX[0], self.lY1[0], ('SE', 'NW', 'SW')[self.variations1[0][0]]))
        exo.append(r'\end{asy}')
        exo.append(r'\kern1cm')
        exo.append('\\begin{asy}\n import graph;\n import interpolate;\n unitsize(5mm);')
        exo.append(r'defaultpen(fontsize(9pt));')
        exo.append(r'real[] xpt,ypt;')
        exo.append(r'real [] xpt={%s};' % (",".join([str(a).zfill(2) for a in self.lX])))
        exo.append(r'real [] ypt={%s};' % (",".join([str(a).zfill(2) for a in self.lY2])))
        exo.append(r'xlimits(-6.2, 6.2);')
        exo.append(r'ylimits(-5.2, 5.2);')
        exo.append(r'xaxis(axis=BottomTop, p=invisible,')
        exo.append(r'ticks=Ticks(format="%%", Step=1, extend=true,')
        exo.append(r'pTick=gray+.5, ptick=dotted)')
        exo.append(r');')
        exo.append(r'yaxis(axis=LeftRight, p=invisible,')
        exo.append(r'ticks=Ticks(format="%%", Step=1, extend=true,')
        exo.append(r'pTick=gray+.5, ptick=dotted)')
        exo.append(r');')
        exo.append(r'xequals(L="$y$", 0, extend=false, arrow=Arrow(HookHead, size=9pt), p=black+1,')
        exo.append(r'ticks=Ticks(scale(.7)*Label(filltype=Fill(white)), Step=1, Size=3pt,')
        exo.append(r'end=false, endlabel=false, beginlabel=false, NoZero));')
        exo.append(r'yequals(L="$x$", 0, extend=false, arrow=Arrow(HookHead, size=9pt), p=black+1,')
        exo.append(r'ticks=Ticks(scale(.7)*Label(filltype=Fill(white)), Step=1, Size=3pt,')
        exo.append(r'end=false, endlabel=false, beginlabel=false, NoZero));')
        exo.append(r'draw(graph(xpt,ypt,Hermite(monotonic)),brown+1.5);')
        exo.append(r'labelx(L=scale(.7)*"$0$", (0,0), align=SW);')
        exo.append(r'label(L="$\mathcal{C}_g$", (%s,%s), align=%s);' % (self.lX[0], self.lY2[0], ('SE', 'NW', 'SW')[self.variations2[0][0]]))
        exo.append(r'\end{asy}')
        exo.append(r'\end{center}')

        return "\n".join(exo)

    def tex_answer(self):
        exo = [r'\exercice*']
        exo.append(r'\begin{enumerate}')
        ans = _(u'\\item la fonction $f$ est')
        dvar = {_(u'décroissante'): [], _(u'croissante'): [], _(u'constante'):[]}
        for v in self.variations1:
            if v[0] == 1: dvar[_(u'croissante')].append('$\interval{%s}{%s}$' % (v[1], v[2]))
            elif v[0] == -1: dvar[_(u'décroissante')].append('$\interval{%s}{%s}$' % (v[1], v[2]))
            elif v[0] == 0: dvar[_(u'constante')].append('$\interval{%s}{%s}$' % (v[1], v[2]))
            else: raise ValueError(_('variation non attendue'))
        if dvar[_(u'décroissante')]: ans += u' décroissante sur %s,' % ' et '.join(dvar[_(u'décroissante')])
        if dvar[_(u'croissante')]: ans += u' croissante sur %s' % ' et '.join(dvar[_(u'croissante')])
        if dvar[_(u'constante')]: ans += u' constante sur %s' % ' et '.join(dvar[_(u'constante')])
        ans += '.'
        exo.append(ans)
        exo.append(r'\item')
        exo.append(r'\begin{tabular}[t]{ll}')
        for j in range(2):
            variations = [self.variations1, self.variations2][j]
            lY = [self.lY1, self.lY2][j]
            exo.append(r'\begin{tikzpicture}[scale=1]')
            exo.append(r'\tkzTabInit[lgt=1.2,espcl=1.2]{$x$/1,$%s\,(x)$/3}{$%s$}' % (['f', 'g'][j], '$,$'.join([str(v[1]) for v in variations] + [str(variations[-1][2])])))
            ans = r'\tkzTabVar{'  # %-/$-2$,+/$5$,-/$-3$,+/$-1$,-/$-4$}'
            trois_niv = False
            for index in range(len(variations)):
                yindex = variations[index][1] + 5
                if variations[index][0] == 1:
                    if trois_niv:
                        ans += r'+/ \raisebox{-2.7cm}{}\raisebox{-1.5cm}{$%s$},' % lY[yindex]
                        trois_niv = False
                    else: ans += r'-/$%s$,' % lY[yindex]
                if variations[index][0] == -1:
                    if trois_niv:
                        ans += r'+/ \raisebox{-2.7cm}{}\raisebox{-1.5cm}{$%s$},' % lY[yindex]
                        trois_niv = False
                    else: ans += r'+/$%s$,' % lY[yindex]
                if variations[index][0] == 0:
                    if index > 0 and index < len(variations) - 1 and variations[index - 1][0] * variations[index + 1][0] > 0:
                        trois_niv = True
                    if trois_niv: ans += r'+/ \raisebox{-2.7cm}{}\raisebox{-1.5cm}{$%s$},' % lY[yindex]
                    elif index > 0:
                        if variations[index - 1][0] == 1: ans += r'+/$%s$,' % lY[yindex]
                        else: ans += r'-/$%s$,' % lY[yindex]
                    elif index < len(variations) - 1:
                        if variations[index + 1][0] == 1: ans += r'-/$%s$,' % lY[yindex]
                        else: ans += r'+/$%s$,' % lY[yindex]
            if variations[-1][0] == 1:  ans += r'+/$%s$}' % lY[-1]
            elif variations[-1][0] == -1:  ans += r'-/$%s$}' % lY[-1]
            elif variations[-1][0] == 0:
                if variations[-2][0] == 1:  ans += r'+/$%s$}' % lY[-1]
                elif variations[-2][0] == -1:  ans += r'-/$%s$}' % lY[-1]
            exo.append(ans)
            # Place les zéros
            for absc in range(-5, 6):
                if lY[absc + 5] == 0:
                    for index in range(len(variations)):
                        if variations[index][1] < absc < variations[index][2]:
                            if variations[index][0] != 0:
                                exo.append(r'\tkzTabVal{%s}{%s}{0.5}{\scriptsize $%s$}{$0$}' % (index + 1, index + 2, absc))
                            break
                        if variations[index][1] == absc or variations[index][2] == absc:
                            break
            exo.append(r'\end{tikzpicture}')
            exo.append(r'&')
        exo.pop(-1)
        exo.append(r'\end{tabular}')
        exo.append(r'\end{enumerate}')

        return "\n".join(exo)

def extrema(lX, lY, intervalle):
    extremums = [[None, 1000], [None, -1000]]
    for i in range(intervalle[0] - lX[0], intervalle[1] + 1 - lX[0]):
        if lY[i] < extremums[0][1]:
            extremums[0][0] = lX[i]
            extremums[0][1] = lY[i]
        if lY[i] > extremums[1][1]:
            extremums[1][0] = lX[i]
            extremums[1][1] = lY[i]
    return extremums

class Vf2ExtremaGraphiques(ex.TexExercise):
    """Extrema et représentation graphique"""

    tags = ["Seconde"]

    def __init__(self):
        fin = False
        while not fin:  # Évite les boucles infinies
            lX = [-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5]
            self.lX = list(lX)
            self.lY1, self.variations1 = PointsCourbes(sens_var=(-1, 1))
            self.lY2, self.variations2 = PointsCourbes()
            self.extremum = (u'maximum', u'minimum')[randrange(2)]
            for dummy in range(20):
                lX = list(self.lX)
                intervalle1 = [lX.pop(randrange(len(lX)))]
                intervalle1.append(lX.pop(randrange(len(lX))))
                intervalle1 = sorted(intervalle1)
                [gmin, gmax] = extrema(self.lX, self.lY1, [-5, 5])
                [lmin, lmax] = extrema(self.lX, self.lY1, intervalle1)
                if abs(lmin[0] - lmax[0]) > 1 and lmin[1] != gmin[1] and lmax[1] != gmax[1]:
                    fin = True
                    break
            if fin:
                fin = False
                for dummy in range(20):
                    lX = list(self.lX)
                    lX.remove(intervalle1[0])
                    lX.remove(intervalle1[1])
                    intervalle2 = [lX.pop(randrange(len(lX)))]
                    intervalle2.append(lX.pop(randrange(len(lX))))
                    intervalle2 = sorted(intervalle2)
                    [gmin, gmax] = extrema(self.lX, self.lY1, [-5, 5])
                    [lmin, lmax] = extrema(self.lX, self.lY1, intervalle2)
                    if abs(lmin[0] - lmax[0]) > 1 and lmin[1] != gmin[1] and lmax[1] != gmax[1]:
                        fin = True
                        break
        self.intervalle1 = intervalle1
        self.intervalle2 = intervalle2

    def tex_statement(self):
        exo = [r'\exercice']
        exo.append(r'\begin{multicols}{2}')
        exo.append(r'\begin{enumerate}')
        exo.append(_(u'\\item Quels sont les extrema de la fonction $f$ ?'))
        exo.append(_(u'\\item Quel est le %s de $f$ sur l\'intervalle $\interval{%s}{%s}$ ?') % (self.extremum, self.intervalle1[0], self.intervalle1[1]))
        exo.append(_(u'\\item Quels sont les extrema de la fonction $g$ ?'))
        exo.append(_(u'\\item Quels sont les extrema de $g$ sur l\'intervalle $\interval{%s}{%s}$ ?') % (self.intervalle2[0], self.intervalle2[1]))
        exo.append(r'\end{enumerate}')
        exo.append(r'\end{multicols}')
        exo.append(r'\begin{center}')
        exo.append('\\begin{asy}\n import graph;\n import interpolate;\n unitsize(5mm);')
        exo.append(r'defaultpen(fontsize(9pt));')
        exo.append(r'real[] xpt,ypt;')
        exo.append(r'real [] xpt={%s};' % (",".join([str(a).zfill(2) for a in self.lX])))
        exo.append(r'real [] ypt={%s};' % (",".join([str(a).zfill(2) for a in self.lY1])))
        exo.append(r'xlimits(-6.2, 6.2);')
        exo.append(r'ylimits(-5.2, 5.2);')
        exo.append(r'xaxis(axis=BottomTop, p=invisible,')
        exo.append(r'ticks=Ticks(format="%%", Step=1, extend=true,')
        exo.append(r'pTick=gray+.5, ptick=dotted)')
        exo.append(r');')
        exo.append(r'yaxis(axis=LeftRight, p=invisible,')
        exo.append(r'ticks=Ticks(format="%%", Step=1, extend=true,')
        exo.append(r'pTick=gray+.5, ptick=dotted)')
        exo.append(r');')
        exo.append(r'xequals(L="$y$", 0, extend=false, arrow=Arrow(HookHead, size=9pt), p=black+1,')
        exo.append(r'ticks=Ticks(scale(.7)*Label(filltype=Fill(white)), Step=1, Size=3pt,')
        exo.append(r'end=false, endlabel=false, beginlabel=false, NoZero));')
        exo.append(r'yequals(L="$x$", 0, extend=false, arrow=Arrow(HookHead, size=9pt), p=black+1,')
        exo.append(r'ticks=Ticks(scale(.7)*Label(filltype=Fill(white)), Step=1, Size=3pt,')
        exo.append(r'end=false, endlabel=false, beginlabel=false, NoZero));')
        exo.append(r'draw(graph(xpt,ypt,Hermite(monotonic)),brown+1.5);')
        exo.append(r'labelx(L=scale(.7)*"$0$", (0,0), align=SW);')
        exo.append(r'label(L="$\mathcal{C}_f$", (%s,%s), align=%s);' % (self.lX[0], self.lY1[0], ('SE', 'NW', 'SW')[self.variations1[0][0]]))
        exo.append(r'\end{asy}')
        exo.append(r'\kern1cm')
        exo.append('\\begin{asy}\n import graph;\n import interpolate;\n unitsize(5mm);')
        exo.append(r'defaultpen(fontsize(9pt));')
        exo.append(r'real[] xpt,ypt;')
        exo.append(r'real [] xpt={%s};' % (",".join([str(a).zfill(2) for a in self.lX])))
        exo.append(r'real [] ypt={%s};' % (",".join([str(a).zfill(2) for a in self.lY2])))
        exo.append(r'xlimits(-6.2, 6.2);')
        exo.append(r'ylimits(-5.2, 5.2);')
        exo.append(r'xaxis(axis=BottomTop, p=invisible,')
        exo.append(r'ticks=Ticks(format="%%", Step=1, extend=true,')
        exo.append(r'pTick=gray+.5, ptick=dotted)')
        exo.append(r');')
        exo.append(r'yaxis(axis=LeftRight, p=invisible,')
        exo.append(r'ticks=Ticks(format="%%", Step=1, extend=true,')
        exo.append(r'pTick=gray+.5, ptick=dotted)')
        exo.append(r');')
        exo.append(r'xequals(L="$y$", 0, extend=false, arrow=Arrow(HookHead, size=9pt), p=black+1,')
        exo.append(r'ticks=Ticks(scale(.7)*Label(filltype=Fill(white)), Step=1, Size=3pt,')
        exo.append(r'end=false, endlabel=false, beginlabel=false, NoZero));')
        exo.append(r'yequals(L="$x$", 0, extend=false, arrow=Arrow(HookHead, size=9pt), p=black+1,')
        exo.append(r'ticks=Ticks(scale(.7)*Label(filltype=Fill(white)), Step=1, Size=3pt,')
        exo.append(r'end=false, endlabel=false, beginlabel=false, NoZero));')
        exo.append(r'draw(graph(xpt,ypt,Hermite(monotonic)),brown+1.5);')
        exo.append(r'labelx(L=scale(.7)*"$0$", (0,0), align=SW);')
        exo.append(r'label(L="$\mathcal{C}_g$", (%s,%s), align=%s);' % (self.lX[0], self.lY2[0], ('SE', 'NW', 'SW')[self.variations2[0][0]]))
        exo.append(r'\end{asy}')
        exo.append(r'\end{center}')
        return "\n".join(exo)

    def tex_answer(self):
        exo = [r'\exercice*']
        exo.append(r'\begin{enumerate}')
        extr = extrema(self.lX, self.lY1, [self.lX[0], self.lX[-1]])
        exo.append(u'\\item ')
        exo.append(r'\begin{itemize}[leftmargin=*]')
        exo.append(_(u'\\item Sur $\interval{%s}{%s}$ , le \\textbf{maximum} de $f$ est $y = %s$. Il est \\textbf{atteint en} $x = %s$.') % (self.lX[0], self.lX[-1], extr[1][1], extr[1][0]))
        exo.append(_(u'\\item Sur $\interval{%s}{%s}$ , le \\textbf{minimum} de $f$ est $y = %s$. Il est \\textbf{atteint en} $x = %s$.') % (self.lX[0], self.lX[-1], extr[0][1], extr[0][0]))
        exo.append(r'\end{itemize}')
        extr = extrema(self.lX, self.lY1, self.intervalle1)
        extr = extr[self.extremum == "maximum"]
        exo.append(_(u'\\item Sur $\interval{%s}{%s}$, le \\textbf{%s} de $f$ est $y = %s$. Il est \\textbf{atteint en} $x = %s$. ') % (self.intervalle1[0], self.intervalle1[1], self.extremum, extr[1], extr[0]))
        extr = extrema(self.lX, self.lY2, [self.lX[0], self.lX[-1]])
        exo.append(u'\\item ')
        exo.append(r'\begin{itemize}[leftmargin=*]')
        exo.append(_(u'\\item Sur $\interval{%s}{%s}$ , le \\textbf{maximum} de $g$ est $y = %s$. Il est \\textbf{atteint en} $x = %s$.') % (self.lX[0], self.lX[-1], extr[1][1], extr[1][0]))
        exo.append(_(u'\\item Sur $\interval{%s}{%s}$ , le \\textbf{minimum} de $g$ est $y = %s$. Il est \\textbf{atteint en} $x = %s$.') % (self.lX[0], self.lX[-1], extr[0][1], extr[0][0]))
        exo.append(r'\end{itemize}')
        extr = extrema(self.lX, self.lY2, self.intervalle2)
        exo.append(u'\\item ')
        exo.append(r'\begin{itemize}[leftmargin=*]')
        exo.append(_(u'\\item Sur $\interval{%s}{%s}$ , le \\textbf{maximum} de $g$ est $y = %s$. Il est \\textbf{atteint en} $x = %s$.') % (self.intervalle2[0], self.intervalle2[1], extr[1][1], extr[1][0]))
        exo.append(_(u'\\item Sur $\interval{%s}{%s}$ , le \\textbf{minimum} de $g$ est $y = %s$. Il est \\textbf{atteint en} $x = %s$.') % (self.intervalle2[0], self.intervalle2[1], extr[0][1], extr[0][0]))
        exo.append(r'\end{itemize}')
        exo.append(r'\end{enumerate}')
        return "\n".join(exo)

class Vf3VariationVersCourbe(ex.TexExercise):
    """Tableaux de variations et courbe"""

    tags = ["Seconde"]

    def __init__(self):
        lX = [-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5]
        self.lX = list(lX)
        self.lY1, self.variations1 = PointsCourbes(sens_var=(-1, 1))
        self.lY2, self.variations2 = PointsCourbes()

    def tex_statement(self):
        exo = [r'\exercice']
        exo.append(r'\begin{enumerate}')
        exo.append(_(u'\\item Pour chaque question, répondre avec une phrase en précisant les intervalles.\\vspace{-2ex}'))
        exo.append(r'\begin{multicols}{2}')
        exo.append(r'\begin{enumerate}')
        exo.append(_(u'\\item Quel est le signe de la fonction $f$ ?'))
        exo.append(_(u'\\item Quels sont les extrema de la fonction $g$ ?'))
        exo.append(r'\end{enumerate}')
        exo.append(r'\end{multicols}')
        exo.append(_(u'\\item Tracer une représentation graphique de $f$ et $g$ sur leurs ensembles de définition.'))
        exo.append(r'\end{enumerate}')
        exo.append(r'\begin{center}')
        exo.append(r'\begin{tabular}[t]{ll}')
        for j in range(2):
            variations = [self.variations1, self.variations2][j]
            lY = [self.lY1, self.lY2][j]
            exo.append(r'\begin{tikzpicture}[scale=1]')
            exo.append(r'\tkzTabInit[lgt=1.2,espcl=1.2]{$x$/1,$%s\,(x)$/3}{$%s$}' % (['f', 'g'][j], '$,$'.join([str(v[1]) for v in variations] + [str(variations[-1][2])])))
            ans = r'\tkzTabVar{'  # %-/$-2$,+/$5$,-/$-3$,+/$-1$,-/$-4$}'
            trois_niv = False
            for index in range(len(variations)):
                yindex = variations[index][1] + 5
                if variations[index][0] == 1:
                    if trois_niv:
                        ans += r'+/ \raisebox{-2.7cm}{}\raisebox{-1.5cm}{$%s$},' % lY[yindex]
                        trois_niv = False
                    else: ans += r'-/$%s$,' % lY[yindex]
                if variations[index][0] == -1:
                    if trois_niv:
                        ans += r'+/ \raisebox{-2.7cm}{}\raisebox{-1.5cm}{$%s$},' % lY[yindex]
                        trois_niv = False
                    else: ans += r'+/$%s$,' % lY[yindex]
                if variations[index][0] == 0:
                    if index > 0 and index < len(variations) - 1 and variations[index - 1][0] * variations[index + 1][0] > 0:
                        trois_niv = True
                    if trois_niv: ans += r'+/ \raisebox{-2.7cm}{}\raisebox{-1.5cm}{$%s$},' % lY[yindex]
                    elif index > 0:
                        if variations[index - 1][0] == 1: ans += r'+/$%s$,' % lY[yindex]
                        else: ans += r'-/$%s$,' % lY[yindex]
                    elif index < len(variations) - 1:
                        if variations[index + 1][0] == 1: ans += r'-/$%s$,' % lY[yindex]
                        else: ans += r'+/$%s$,' % lY[yindex]
            if variations[-1][0] == 1:  ans += r'+/$%s$}' % lY[-1]
            elif variations[-1][0] == -1:  ans += r'-/$%s$}' % lY[-1]
            elif variations[-1][0] == 0:
                if variations[-2][0] == 1:  ans += r'+/$%s$}' % lY[-1]
                elif variations[-2][0] == -1:  ans += r'-/$%s$}' % lY[-1]
            exo.append(ans)
            # Place les zéros
            for absc in range(-5, 6):
                if lY[absc + 5] == 0:
                    for index in range(len(variations)):
                        if variations[index][1] < absc < variations[index][2]:
                            if variations[index][0] != 0:
                                exo.append(r'\tkzTabVal{%s}{%s}{0.5}{\scriptsize $%s$}{$0$}' % (index + 1, index + 2, absc))
                            break
                        if variations[index][1] == absc or variations[index][2] == absc:
                            break
            exo.append(r'\end{tikzpicture}')
            exo.append(r'&')
        exo.pop(-1)
        exo.append(r'\end{tabular}')
        exo.append(r'\end{center}')

        return "\n".join(exo)

    def tex_answer(self):
        exo = [r'\exercice*']
        exo.append(r'\begin{enumerate}')
        exo.append(r'\item')
        exo.append(r'\begin{enumerate}')
        lneg, lpos = [], []
        for index in range(len(self.lX)):
            absc = self.lX[index]
            if self.lY1[index] < 0:
                if lneg and absc - lneg[-1][1] == 1:
                    lneg[-1][1] = absc
                else:
                    lneg.append([absc, absc])
            elif self.lY1[index] > 0:
                if lpos and absc - lpos[-1][1] == 1:
                    lpos[-1][1] = absc
                else:
                    lpos.append([absc, absc])
            else:  # nul
                if lneg and absc - lneg[-1][1] == 1:
                    lneg[-1][1] = absc
                    lpos.append([absc, absc])
                elif lpos and absc - lpos[-1][1] == 1:
                    lpos[-1][1] = absc
                    lneg.append([absc, absc])
                else:
                    lneg.append([absc, absc])
                    lpos.append([absc, absc])
        sneg, spos = '', ''
        for i in lneg:
            if i[1] == i[0]: lneg.remove(i)
            else: sneg += '$\interval{%s}{%s}$, ' % (i[0], i[1])
        sneg = sneg[:-2]
        for i in lpos:
            if i[1] == i[0]: lpos.remove(i)
            else: spos += '$\interval{%s}{%s}$, ' % (i[0], i[1])
        spos = spos[:-2]

        exo.append(_(u'\\item La fonction $f$ est \\textbf{négative} sur %s et \\textbf{positive} sur %s.') % (sneg, spos))
        extr = extrema(self.lX, self.lY2, [self.lX[0], self.lX[-1]])
        exo.append(r'\item')
        exo.append(r'\begin{itemize}[leftmargin=*]')
        exo.append(_(u'\\item Sur $\interval{%s}{%s}$ , le \\textbf{maximum} de $g$ est $y = %s$. Il est \\textbf{atteint en} $x = %s$.') % (self.lX[0], self.lX[-1], extr[1][1], extr[1][0]))
        exo.append(_(u'\\item Sur $\interval{%s}{%s}$ , le \\textbf{minimum} de $g$ est $y = %s$. Il est \\textbf{atteint en} $x = %s$.') % (self.lX[0], self.lX[-1], extr[0][1], extr[0][0]))
        exo.append(r'\end{itemize}')
        exo.append(r'\end{enumerate}')
        exo.append(r'\item\ ')
        exo.append(r'\begin{center}')
        exo.append(r'\begin{tabular}[t]{cc}')
        exo.append(r'\begin{adjustbox}{valign=t}')
        exo.append('\\begin{asy}\n import graph;\n import interpolate;\n unitsize(5mm);')
        exo.append(r'defaultpen(fontsize(9pt));')
        exo.append(r'real[] xpt,ypt;')
        lAbsc, lOrdo = integration_zeros(self.lX, self.lY1, self.variations1)
        exo.append(r'real [] xpt={%s};' % (",".join([str(a).zfill(2) for a in lAbsc])))
        exo.append(r'real [] ypt={%s};' % (",".join([str(a).zfill(2) for a in lOrdo])))
        exo.append(r'xlimits(-6.2, 6.2);')
        exo.append(r'ylimits(-5.2, 5.2);')
        exo.append(r'xaxis(axis=BottomTop, p=invisible,')
        exo.append(r'ticks=Ticks(format="%%", Step=1, extend=true,')
        exo.append(r'pTick=gray+.5, ptick=dotted)')
        exo.append(r');')
        exo.append(r'yaxis(axis=LeftRight, p=invisible,')
        exo.append(r'ticks=Ticks(format="%%", Step=1, extend=true,')
        exo.append(r'pTick=gray+.5, ptick=dotted)')
        exo.append(r');')
        exo.append(r'xequals(L="$y$", 0, extend=false, arrow=Arrow(HookHead, size=9pt), p=black+1,')
        exo.append(r'ticks=Ticks(scale(.7)*Label(filltype=Fill(white)), Step=1, Size=3pt,')
        exo.append(r'end=false, endlabel=false, beginlabel=false, NoZero));')
        exo.append(r'yequals(L="$x$", 0, extend=false, arrow=Arrow(HookHead, size=9pt), p=black+1,')
        exo.append(r'ticks=Ticks(scale(.7)*Label(filltype=Fill(white)), Step=1, Size=3pt,')
        exo.append(r'end=false, endlabel=false, beginlabel=false, NoZero));')
        exo.append(r'draw(graph(xpt,ypt,Hermite(monotonic)),brown+1.5);')
        exo.append(r'labelx(L=scale(.7)*"$0$", (0,0), align=SW);')
        exo.append(r'label(L="$\mathcal{C}_f$", (%s,%s), align=%s);' % (self.lX[0], self.lY1[0], ('SE', 'NW', 'SW')[self.variations1[0][0]]))
        exo.append(r'\end{asy}')
        exo.append(r'\end{adjustbox}')
        exo.append(r'&')
        exo.append(r'\begin{adjustbox}{valign=t}')
        exo.append('\\begin{asy}\n import graph;\n import interpolate;\n unitsize(5mm);')
        exo.append(r'defaultpen(fontsize(9pt));')
        exo.append(r'real[] xpt,ypt;')
        lAbsc, lOrdo = integration_zeros(self.lX, self.lY2, self.variations2)
        exo.append(r'real [] xpt={%s};' % (",".join([str(a).zfill(2) for a in lAbsc])))
        exo.append(r'real [] ypt={%s};' % (",".join([str(a).zfill(2) for a in lOrdo])))
        exo.append(r'xlimits(-6.2, 6.2);')
        exo.append(r'ylimits(-5.2, 5.2);')
        exo.append(r'xaxis(axis=BottomTop, p=invisible,')
        exo.append(r'ticks=Ticks(format="%%", Step=1, extend=true,')
        exo.append(r'pTick=gray+.5, ptick=dotted)')
        exo.append(r');')
        exo.append(r'yaxis(axis=LeftRight, p=invisible,')
        exo.append(r'ticks=Ticks(format="%%", Step=1, extend=true,')
        exo.append(r'pTick=gray+.5, ptick=dotted)')
        exo.append(r');')
        exo.append(r'xequals(L="$y$", 0, extend=false, arrow=Arrow(HookHead, size=9pt), p=black+1,')
        exo.append(r'ticks=Ticks(scale(.7)*Label(filltype=Fill(white)), Step=1, Size=3pt,')
        exo.append(r'end=false, endlabel=false, beginlabel=false, NoZero));')
        exo.append(r'yequals(L="$x$", 0, extend=false, arrow=Arrow(HookHead, size=9pt), p=black+1,')
        exo.append(r'ticks=Ticks(scale(.7)*Label(filltype=Fill(white)), Step=1, Size=3pt,')
        exo.append(r'end=false, endlabel=false, beginlabel=false, NoZero));')
        exo.append(r'draw(graph(xpt,ypt,Hermite(monotonic)),brown+1.5);')
        exo.append(r'labelx(L=scale(.7)*"$0$", (0,0), align=SW);')
        exo.append(r'label(L="$\mathcal{C}_g$", (%s,%s), align=%s);' % (self.lX[0], self.lY2[0], ('SE', 'NW', 'SW')[self.variations2[0][0]]))
        exo.append(r'\end{asy}')
        exo.append(r'\end{adjustbox}')
        exo.append(r'\end{tabular}')
        exo.append(r'\end{center}')
        exo.append(r'\end{enumerate}')
        return "\n".join(exo)

def elements_intervalle(variations, sens):
    """Renvoie deux nombres appartenant à un intervalle sur lequel la fonction est monotone, ainsi que l'intervalle monotone auquel ils appartiennent"""
    while True:
        index = randrange(len(variations))
        if variations[index][0] == sens:
            break
    x0 = decimaux(randrange(50 * variations[index][1] // 6 + 10 * variations[index][2] // 6, 20 * variations[index][1] // 3 + 10 * variations[index][2] // 3 + 1) / 10, True)
    x1 = decimaux(randrange(10 * variations[index][1] // 3 + 20 * variations[index][2] // 3, 10 * variations[index][1] // 6 + 50 * variations[index][2] // 6, +1) / 10, True)
    return [x0, x1, [variations[index][1], variations[index][2]]]

def non_monotone(variations, lX, lY, signe):
    """Donne un intervalle sur lequel la fonction n'est pas monotone. On peut malgré tout comparer
    les extrémités de cet intervalle par le signe de leurs images si signe=True"""
    for dummy in range(20):
        tirage = [a for a in range(len(variations))]
        try:
            i0 = tirage.pop(randrange(len(tirage)))
            while lY[i0] == lY[i0 + 1]:
                # intervalle constant
                i0 = tirage.pop(randrange(len(tirage)))
            i1 = tirage.pop(randrange(len(tirage)))
            while lY[i1] == lY[i1 + 1]:
                # intervalle constant
                i1 = tirage.pop(randrange(len(tirage)))
        except ValueError:
            return None
        x0 = randrange(10 * variations[i0][1] + 1, 10 * variations[i0][2]) / 10
        x1 = randrange(10 * variations[i1][1] + 1, 10 * variations[i1][2]) / 10
        for i in range(len(lX)):
            if x0 <= lX[i]:
                if x0 == lX[i]: y0 = lY[i]
                else: y0 = (lY[i - 1] + lY[i]) / 2
                break
        for i in range(len(lX)):
            if x1 <= lX[i]:
                if x1 == lX[i]: y1 = lY[i]
                else: y1 = (lY[i - 1] + lY[i]) / 2
                break
        if signe and y0 * y1 <= 0: return ([x0, y0], [x1, y1])
        if not signe and y0 * y1 > 0:
            I = intersection_intervalles(variations[i0][1:], variations[i1][1:])
            if I and I[0] != I[1]: return ([x0, y0], [x1, y1])
    return None

def intersection_intervalles(I0, I1):
    "renvoie l'intersection entre 2 intervalles, None si vide."
    x0, x1 = min(I0), max(I0)
    y0, y1 = min(I1), max(I1)
    x = max(x0, x1)
    y = min(y0, y1)
    if x <= y:return (x, y)
    else: return None

class Vf4ComparerImages(ex.TexExercise):
    """Comparer des images à partir du sens de variation"""

    tags = ["Seconde"]

    def __init__(self):
        fin = False
        while not fin:
            lX = [i for i in range(-10 + randrange(6), 10 - randrange(6))]
            self.lX = list(lX)
            lY, variations = PointsCourbes(nb_var=(4, 5), absc=(lX[0], lX[-1]), ordo=(lX[0], lX[-1]), cstes=(1, 1))
            self.lY = list(lY)
            self.variations = list(variations)
            lx = elements_intervalle(self.variations, -1)
            lx.append(-1)
            comparaison = [lx]
            lx = elements_intervalle(self.variations, 1)
            lx.append(1)
            comparaison.append(lx)
            lx = elements_intervalle(self.variations, 0)
            lx.append(0)
            comparaison.append(lx)
            shuffle(comparaison)
            self.comparaison = comparaison
            non_comparable = [non_monotone(self.variations, lX, self.lY, True)]
            non_comparable.append(non_monotone(self.variations, lX, self.lY, False))
            if non_comparable[0] != None and non_comparable[1] != None:
                fin = True
        shuffle(non_comparable)
        self.non_comparable = non_comparable

    def tex_statement(self):
        exo = [r'\exercice']
        exo.append(r'\begin{enumerate}')
        exo.append(_(u'\\item À partir du tableau de variation ci-dessous, recopier et compléter les égalités ou inégalités suivantes en justifiant :\\vspace{-2ex}'))
        exo.append(r'\begin{multicols}{3}')
        exo.append(r'\begin{enumerate}')
        exo.append(r'\item $f\,(%s) \ldots{} f\,(%s)$' % tuple(self.comparaison[0][:2]))
        exo.append(r'\item $f\,(%s) \ldots{} f\,(%s)$' % tuple(self.comparaison[1][:2]))
        exo.append(r'\item $f\,(%s) \ldots{} f\,(%s)$' % tuple(self.comparaison[2][:2]))
        exo.append(r'\end{enumerate}\vspace{-2ex}')
        exo.append(r'\end{multicols}')
        exo.append(_(u'\\item Peut-on comparer l’image des nombres $%s$ et $%s$ ? Justifier.') % (decimaux(self.non_comparable[0][0][0]), decimaux(self.non_comparable[0][1][0])))
        exo.append(_(u'\\item Peut-on comparer l’image des nombres $%s$ et $%s$ ? Justifier.') % (decimaux(self.non_comparable[1][0][0]), decimaux(self.non_comparable[1][1][0])))
        exo.append(r'\end{enumerate}')
        exo.append(r'\begin{center}')
        variations = list(self.variations)
        lY = list(self.lY)
        exo.append(r'\begin{tikzpicture}[scale=1]')
        exo.append(r'\tkzTabInit[lgt=1.2,espcl=2]{$x$/1,$f\,(x)$/3}{$%s$}' % ('$,$'.join([str(v[1]) for v in variations] + [str(variations[-1][2])])))
        ans = r'\tkzTabVar{'  # %-/$-2$,+/$5$,-/$-3$,+/$-1$,-/$-4$}'
        trois_niv = False
        for index in range(len(variations)):
            yindex = variations[index][1] - self.lX[0]
            if variations[index][0] == 1:
                if trois_niv:
                    ans += r'+/ \raisebox{-2.7cm}{}\raisebox{-1.5cm}{$%s$},' % lY[yindex]
                    trois_niv = False
                else: ans += r'-/$%s$,' % lY[yindex]
            if variations[index][0] == -1:
                if trois_niv:
                    ans += r'+/ \raisebox{-2.7cm}{}\raisebox{-1.5cm}{$%s$},' % lY[yindex]
                    trois_niv = False
                else: ans += r'+/$%s$,' % lY[yindex]
            if variations[index][0] == 0:
                if index > 0 and index < len(variations) - 1 and variations[index - 1][0] * variations[index + 1][0] > 0:
                    trois_niv = True
                if trois_niv: ans += r'+/ \raisebox{-2.7cm}{}\raisebox{-1.5cm}{$%s$},' % lY[yindex]
                elif index > 0:
                    if variations[index - 1][0] == 1: ans += r'+/$%s$,' % lY[yindex]
                    else: ans += r'-/$%s$,' % lY[yindex]
                elif index < len(variations) - 1:
                    if variations[index + 1][0] == 1: ans += r'-/$%s$,' % lY[yindex]
                    else: ans += r'+/$%s$,' % lY[yindex]
        if variations[-1][0] == 1:  ans += r'+/$%s$}' % lY[-1]
        elif variations[-1][0] == -1:  ans += r'-/$%s$}' % lY[-1]
        elif variations[-1][0] == 0:
            if variations[-2][0] == 1:  ans += r'+/$%s$}' % lY[-1]
            elif variations[-2][0] == -1:  ans += r'-/$%s$}' % lY[-1]
        exo.append(ans)
        # Place les zéros
        for absc in range(self.lX[0], self.lX[-1] + 1):
            if lY[absc - self.lX[0]] == 0:
                for index in range(len(variations)):
                    if variations[index][1] < absc < variations[index][2]:
                        if variations[index][0] != 0:
                            exo.append(r'\tkzTabVal{%s}{%s}{0.5}{\scriptsize $%s$}{$0$}' % (index + 1, index + 2, absc))
                        break
                    if variations[index][1] == absc or variations[index][2] == absc:
                        break
        exo.append(r'\end{tikzpicture}')
        exo.append(r'\end{center}')
        return "\n".join(exo)

    def tex_answer(self):
        exo = [r'\exercice*']
        exo.append(r'\begin{enumerate}')
        exo.append(r'\item')
        exo.append(r'\begin{enumerate}')
        for i in range(3):
            exo.append(_(u'\\item $f\\,(%s) %s f\\,(%s)$ car $%s < %s$ et $f$ est %s sur $\interval{%s}{%s}$.') % (self.comparaison[i][0], ['=', '<', '>'][self.comparaison[i][3]], self.comparaison[i][1], self.comparaison[i][0], self.comparaison[i][1], [_(u'constante'), _(u'croissante'), _(u'décroissante')][self.comparaison[i][3]], self.comparaison[i][2][0], self.comparaison[i][2][1]))
        exo.append(r'\end{enumerate}')
        for i in range(2):
            if self.non_comparable[i][0][1] * self.non_comparable[i][1][1] <= 0:
                exo.append(_(u'\\item $f\\,(%s) %s f\\,(%s)$ car d’après le signe de la fonction $f\\,(%s) %s 0$ et $f\\,(%s) %s 0$ (par contre, on ne peut pas utiliser le sens de variation qui change sur l’intervalle $\interval{%s}{%s}$).') % \
                           (decimaux(self.non_comparable[i][0][0], 1), ['<', '>'][self.non_comparable[i][0][1] > 0], decimaux(self.non_comparable[i][1][0], 1), \
                            decimaux(self.non_comparable[i][0][0], 1), ['<', '>'][self.non_comparable[i][0][1] > 0], decimaux(self.non_comparable[i][1][0], 1), \
                            ['<', '>'][self.non_comparable[i][1][1] > 0], decimaux(min(self.non_comparable[i][0][0], self.non_comparable[i][1][0]), 1), decimaux(max(self.non_comparable[i][0][0], self.non_comparable[i][1][0]), 1)))
            else:
                exo.append(_(u'\\item On ne peut pas comparer $f\\,(%s)$ et $f\\,(%s)$ car la fonction $f$ n\'est pas monotone (elle change de sens de variation) sur $\interval{%s}{%s}$.') % \
                           (decimaux(self.non_comparable[i][0][0], 1), decimaux(self.non_comparable[i][1][0], 1), decimaux(self.non_comparable[i][0][0], 1), decimaux(self.non_comparable[i][1][0], 1)))
        exo.append(r'\end{enumerate}')
        return "\n".join(exo)

def extrema_locaux(variations, lX, lY):
    """Donne un intervalle sur lequel la fonction n'est pas monotone et ou les extrema
    sont différents de ceux sur l'ensemble de définition."""
    [gmin, gmax] = extrema(lX, lY, [lX[0], lX[-1]])
    gmin = gmin[1]
    gmax = gmax[1]
    for i in range(20):
        tirage = [a for a in range(len(variations))]
        i0 = tirage.pop(randrange(len(tirage)))
        i1 = tirage.pop(randrange(len(tirage)))
        x0 = randrange(10 * variations[i0][1] + 1, 10 * variations[i0][2]) / 10
        x1 = randrange(10 * variations[i1][1] + 1, 10 * variations[i1][2]) / 10
        for i in range(len(lX)):
            if x0 <= lX[i]:
                if x0 == lX[i]: y0 = lY[i]
                else: y0 = (lY[i - 1] + lY[i]) / 2
                break
        for i in range(len(lX)):
            if x1 <= lX[i]:
                if x1 == lX[i]: y1 = lY[i]
                else: y1 = (lY[i - 1] + lY[i]) / 2
                break
        extremums = [100, -100]
        # extremums = [min(variations[i0][1], variations[i1][1]), max(variations[i0][2], variations[i1][2])]
        if i0 > i1: i0, x0, y0, i1, x1, y1 = i1, x1, y1, i0, x0, y0
        if y0 < 0 and variations[i0][0] == -1:
            extremums[1] = min(lY[variations[i0][1] - lX[0]], 0)
            extremums[0] = min(lY[variations[i0][1] - lX[0]], lY[variations[i0][2] - lX[0]])
        elif y0 > 0 and variations[i0][0] == 1:
            extremums[0] = max(lY[variations[i0][2] - lX[0]], 0)
            extremums[1] = max(lY[variations[i0][1] - lX[0]], lY[variations[i0][2] - lX[0]])
        else:
            extremums[1] = max(lY[variations[i0][1] - lX[0]], lY[variations[i0][2] - lX[0]])
            extremums[0] = min(lY[variations[i0][1] - lX[0]], lY[variations[i0][2] - lX[0]])
        if y1 < 0 and variations[i1][0] == 1: extremums[1] = max(min(0, lY[variations[i1][2] - lX[0]]), extremums[1])
        elif y1 > 0 and variations[i1][0] == -1: extremums[0] = min(max(0, lY[variations[i1][2] - lX[0]]), extremums[0])
        else:
            extremums[1] = max(lY[variations[i1][1] - lX[0]], lY[variations[i1][2] - lX[0]], extremums[1])
            extremums[0] = min(lY[variations[i1][1] - lX[0]], lY[variations[i1][2] - lX[0]], extremums[0])
        for index in range(i0 + 1, i1):
            extremums[0] = min(extremums[0], extrema(lX, lY, variations[index][1:])[0][1])
            extremums[1] = max(extremums[1], extrema(lX, lY, variations[index][1:])[1][1])
        if extremums[0] != gmin and extremums[1] != gmax:
            return [[x0, y0], [x1, y1], extremums]
    return None

class Vf5Extrema_Tableau(ex.TexExercise):
    """Extrema locaux à partir du tableau de variation"""

    tags = ["Seconde"]

    def __init__(self):
        fin = False
        while not fin:
            lX = [i for i in range(-10 + randrange(6), 10 - randrange(6))]
            self.lX = list(lX)
            lY, variations = PointsCourbes(nb_var=(4, 5), absc=(lX[0], lX[-1]), ordo=(lX[0], lX[-1]), cstes=(1, 1))
            self.lY = list(lY)
            self.variations = list(variations)
            comparaison = [extrema_locaux(variations, lX, lY)]
            comparaison.append(extrema_locaux(variations, lX, lY))
            if comparaison[0] != None and comparaison[1] != None:
                fin = True
        self.comparaison = comparaison
        inegalites = ['\\geqslant{}', '\\leqslant{}']
        shuffle(inegalites)
        inegalites.append(['\\leqslant{}', '\\geqslant{}'][randrange(2)])
        self.inegalites = inegalites

    def tex_statement(self):
        exo = [r'\exercice']
        exo.append(r'\begin{enumerate}')
        exo.append(_(u'\\item À partir du tableau de variation de la fonction $f$, compléter les égalités ou inégalités suivantes :\\vspace{-2ex}'))
        exo.append(r'\begin{multicols}{2}')
        exo.append(r'\begin{enumerate}')
        exo.append(r'\item Pour $x \in \interval{%s}{%s},\quad f\,(x) %s \ldots{}$' % (self.lX[0], self.lX[-1], self.inegalites[0]))
        exo.append(r'\item Pour $x \in \interval{%s}{%s},\quad f\,(x) %s \ldots{}$' % (self.lX[0], self.lX[-1], self.inegalites[1]))
        exo.append(r'\item Pour $x \in \interval{%s}{%s},\quad f\,(x) %s \ldots{}$' % (decimaux(self.comparaison[0][0][0], 1), decimaux(self.comparaison[0][1][0], 1), self.inegalites[2]))
        exo.append(r'\end{enumerate}')
        exo.append(r'\end{multicols}')
        exo.append(u'\\item')
        exo.append(r'\begin{enumerate}')
        exo.append(_(u'\\item Donner un encadrement de la fonction $f$ sur l’intervalle $\interval{%s}{%s}$.') % (self.lX[0], self.lX[-1]))
        exo.append(_(u'\\item Donner un encadrement de la fonction $f$ sur l’intervalle $\interval{%s}{%s}$.') % (decimaux(self.comparaison[1][0][0], 1), decimaux(self.comparaison[1][1][0], 1)))
        exo.append(r'\end{enumerate}')
        exo.append(r'\end{enumerate}')
        exo.append(r'\begin{center}')
        variations = list(self.variations)
        lY = list(self.lY)
        exo.append(r'\begin{tikzpicture}[scale=1]')
        exo.append(r'\tkzTabInit[lgt=1.2,espcl=2]{$x$/1,$f\,(x)$/3}{$%s$}' % ('$,$'.join([str(v[1]) for v in variations] + [str(variations[-1][2])])))
        ans = r'\tkzTabVar{'  # %-/$-2$,+/$5$,-/$-3$,+/$-1$,-/$-4$}'
        trois_niv = False
        for index in range(len(variations)):
            yindex = variations[index][1] - self.lX[0]
            if variations[index][0] == 1:
                if trois_niv:
                    ans += r'+/ \raisebox{-2.7cm}{}\raisebox{-1.5cm}{$%s$},' % lY[yindex]
                    trois_niv = False
                else: ans += r'-/$%s$,' % lY[yindex]
            if variations[index][0] == -1:
                if trois_niv:
                    ans += r'+/ \raisebox{-2.7cm}{}\raisebox{-1.5cm}{$%s$},' % lY[yindex]
                    trois_niv = False
                else: ans += r'+/$%s$,' % lY[yindex]
            if variations[index][0] == 0:
                if index > 0 and index < len(variations) - 1 and variations[index - 1][0] * variations[index + 1][0] > 0:
                    trois_niv = True
                if trois_niv: ans += r'+/ \raisebox{-2.7cm}{}\raisebox{-1.5cm}{$%s$},' % lY[yindex]
                elif index > 0:
                    if variations[index - 1][0] == 1: ans += r'+/$%s$,' % lY[yindex]
                    else: ans += r'-/$%s$,' % lY[yindex]
                elif index < len(variations) - 1:
                    if variations[index + 1][0] == 1: ans += r'-/$%s$,' % lY[yindex]
                    else: ans += r'+/$%s$,' % lY[yindex]
        if variations[-1][0] == 1:  ans += r'+/$%s$}' % lY[-1]
        elif variations[-1][0] == -1:  ans += r'-/$%s$}' % lY[-1]
        elif variations[-1][0] == 0:
            if variations[-2][0] == 1:  ans += r'+/$%s$}' % lY[-1]
            elif variations[-2][0] == -1:  ans += r'-/$%s$}' % lY[-1]
        exo.append(ans)
        # Place les zéros
        for absc in range(self.lX[0], self.lX[-1] + 1):
            if lY[absc - self.lX[0]] == 0:
                for index in range(len(variations)):
                    if variations[index][1] < absc < variations[index][2]:
                        if variations[index][0] != 0:
                            exo.append(r'\tkzTabVal{%s}{%s}{0.5}{\scriptsize $%s$}{$0$}' % (index + 1, index + 2, absc))
                        break
                    if variations[index][1] == absc or variations[index][2] == absc:
                        break
        exo.append(r'\end{tikzpicture}')
        exo.append(r'\end{center}')
        return "\n".join(exo)

    def tex_answer(self):
        exo = [r'\exercice*']
        exo.append(r'\begin{enumerate}')
        exo.append(r'\item')
        exo.append(r'\begin{multicols}{2}')
        exo.append(r'\begin{enumerate}')
        extr = extrema(self.lX, self.lY, [self.lX[0], self.lX[-1]])
        exo.append(_(r'\item Pour $x \in \interval{%s}{%s},\quad f\,(x) %s %s$') % (self.lX[0], self.lX[-1], self.inegalites[0], extr['\\leqslant{}' == self.inegalites[0]][1]))
        exo.append(_(r'\item Pour $x \in \interval{%s}{%s},\quad f\,(x) %s %s$') % (self.lX[0], self.lX[-1], self.inegalites[1], extr['\\leqslant{}' == self.inegalites[1]][1]))
        exo.append(_(r'\item Pour $x \in \interval{%s}{%s},\quad f\,(x) %s %s$') % (decimaux(self.comparaison[0][0][0], 1), decimaux(self.comparaison[0][1][0], 1), self.inegalites[2], self.comparaison[0][2]['\\leqslant{}' == self.inegalites[2]]))
        exo.append(r'\end{enumerate}')
        exo.append(r'\end{multicols}')
        exo.append(r'\item')
        exo.append(r'\begin{enumerate}')
        exo.append(_(u'\\item Sur $\interval{%s}{%s},\\quad %s \\leqslant{} f\\,(x) \\leqslant{} %s$.') % (self.lX[0], self.lX[-1], extr[0][1], extr[1][1]))
        exo.append(_(u'\\item Sur $\interval{%s}{%s},\\quad %s \\leqslant{} f\\,(x) \\leqslant{} %s$.') % (decimaux(self.comparaison[1][0][0], 1), decimaux(self.comparaison[1][1][0], 1), decimaux(self.comparaison[1][2][0], 1), decimaux(self.comparaison[1][2][1], 1)))
        exo.append(r'\end{enumerate}')
        exo.append(r'\end{enumerate}')

        return "\n".join(exo)
