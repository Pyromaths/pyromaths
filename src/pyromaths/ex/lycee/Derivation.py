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
from itertools import count
'''
Created on 24 janv. 2015

@author: jerome
'''
from pyromaths import ex
from pyromaths.outils.Arithmetique import pgcd
from pyromaths.classes.Fractions import Fraction
from random import randrange, shuffle
from string import zfill

def InitPoints(minimum=-6.1, maximum=6.1, nbval=3):
    dY = []
    directions = [(-1) ** i for i in range(nbval - 1)]
    directions.append(0)
    shuffle(directions)
    for i in range((nbval - 1) // 2):
        while True:
            a, b = randrange(1, 5), randrange(1, 5)
            if pgcd(a, b) == 1 and a % b != 0:
                dY.append(Fraction(a, b))
                break
    for i in range(nbval - 1 - len(dY)):
        dY.append(randrange(1, 5))
    shuffle(dY)
    for i in range(nbval):
        if directions[i] == 0:
            dY.insert(i, 0)
        else:
            dY[i] = dY[i] * directions[i]
    dY.insert(0, 0)
    dY.append(0)
    redo = True
    while redo:
        lX = [int(minimum) + 1 + int(1.*i * (maximum - minimum - 2) / nbval) + randrange(4) for i in range(nbval)]
        for i in range(len(lX) - 1):
            if lX[i + 1:].count(lX[i]):
                redo = True
                break
            else:
                redo = False
    lX.insert(0, minimum)
    lX.append(maximum)
    lX.sort()
    lY = [randrange(-4, 5)]
    for i in range(1, len(lX)):
        inf = lY[-1] - 4 * int(lX[i] - lX[i - 1])
        sup = lY[-1] + 4 * int(lX[i] - lX[i - 1])
        nY = randrange(int(max(-4, inf)), int(min(5, sup)))
        lY.append(nY)
        #=======================================================================
        # while True:
        #     lg = randrange(1, 4) * (-1) ** randrange(2) * int(lX[i] - lX[i - 1])
        #     nY = lY[-1] + lg
        #     if -4 <= nY <= 4 :
        #         lY.append(nY)
        #         break
        #=======================================================================
    return lX, lY, dY


class Fd1Tangentes(ex.TexExercise):
    '''
    classdocs
    '''
    description = _(u'Nombre dérivé graphiquement')
    level = _(u"1.1èreS")


    def __init__(self):
        '''
        Constructor
        '''

        self.lX1, self.lY1, self.dY1 = InitPoints(minimum=-6.1, maximum=6.1, nbval=3)
        self.lX2, self.lY2, self.dY2 = InitPoints(minimum=-6.1, maximum=6.1, nbval=4)


    def tex_statement(self):
        dY1 = list(self.dY1)
        for i in range(len(dY1)):
            if isinstance(dY1[i], Fraction): dY1[i] = 1. * dY1[i].n / dY1[i].d
        exo = [r'\exercice']
        exo.append(r'\begin{minipage}[]{\linewidth-8cm}')
        exo.append(r'\begin{enumerate}')
        exo.append(_(u'\\item Déterminer graphiquement les nombres dérivés de la fonction $f$ en $\qquad x=%s \qquad x=%s \qquad x=%s$.') % (self.lX1[1], self.lX1[2], self.lX1[3]))
        exo.append(_(u'\\item On considère le tableau de valeurs suivant :\\par'))
        exo.append(r'\renewcommand{\arraystretch}{2}')
        exo.append(r'\begin{tabularx}{\linewidth}[t]{|*5{>{\centering\arraybackslash}X|}}')
        exo.append(r'\hline')
        exo.append(r'$x$ & $%s$ \\ \hline' % ("$ & $".join([str(a) for a in self.lX2[1:-1]])))
        exo.append(r'$g\,(x)$ & $%s$ \\ \hline' % ("$ & $".join([str(a) for a in self.lY2[1:-1]])))
        exo.append('$g\'\\,(x)$ & $%s$ \\\\ \\hline' % ("$ & $".join([str(a) for a in self.dY2[1:-1]])))
        exo.append(r'\end{tabularx}')
        exo.append(r'\begin{enumerate}')
        exo.append(_(u'\\item Dans un nouveau repère, placer les points de la courbe $\\mathcal{C}_g$ ainsi connus.'))
        exo.append(_(u'\\item Tracer les tangentes à $\\mathcal{C}_g$ en ces points.'))
        exo.append(_(u'\\item Donner une allure possible de la courbe $\\mathcal{C}_g$.'))
        exo.append(r'\end{enumerate}')
        exo.append(r'\end{enumerate}')
        exo.append(r'\end{minipage}')
        exo.append(r'\hfill')
        exo.append(r'\begin{minipage}[]{7.5cm}')
        exo.append(r'\begin{asy}[width=\linewidth]')
        exo.append(r'import graph;')
        exo.append(r'import interpolate;')
        exo.append(r'import geometry;')
        exo.append(r'defaultpen(fontsize(9pt));')
        exo.append(r'real[] xpt={%s};' % (",".join([zfill(str(a), 2) for a in self.lX1])))
        exo.append(r'real[] ypt={%s};' % (",".join([zfill(str(a), 2) for a in self.lY1])))
        exo.append(r'real[] dy= {%s};' % (",".join([zfill(str(a), 2) for a in dY1])))
        exo.append(r'real f(real t){return pwhermite(xpt,ypt,dy)(t);}')
        exo.append(r'path Cf=graph(f,-6.1,6.1);')
        exo.append(r'void tangente(int k,real lg=sqrt(1+dy[k]^2),real ld=lg, pen p=black+1, arrowbar arr=Arrows(SimpleHead,size=9pt)) {')
        exo.append(r'draw(((xpt[k],ypt[k])-lg*unit((1,dy[k])))--((xpt[k],ypt[k])+ld*unit((1,dy[k]))),p,arr);')
        exo.append(r'dot((xpt[k],ypt[k]));')
        exo.append(r'}')
        exo.append(r'xlimits(-6.1, 6.1);')
        exo.append(r'ylimits(-5.5, 5.5, Crop);')
        exo.append(r'xaxis(axis=BottomTop, p=invisible,')
        exo.append(r'ticks=Ticks(format="%", Step=1, extend=true,')
        exo.append(r'pTick=gray+.5pt, ptick=dotted)')
        exo.append(r');')
        exo.append(r'yaxis(axis=LeftRight, p=invisible,')
        exo.append(r'ticks=Ticks(format="%", Step=1, extend=true,')
        exo.append(r'pTick=gray+.5pt, ptick=dotted)')
        exo.append(r');')
        exo.append(r'xequals(L="$y$", 0, extend=false, arrow=Arrow(HookHead, size=9pt), p=black+1,')
        exo.append(r'ticks=Ticks(scale(.7)*Label(filltype=Fill(white)), Step=1, Size=3pt,')
        exo.append(r'end=false, endlabel=false, beginlabel=false, NoZero));')
        exo.append(r'yequals(L="$x$", 0, extend=false, arrow=Arrow(HookHead, size=9pt), p=black+1,')
        exo.append(r'ticks=Ticks(scale(.7)*Label(filltype=Fill(white)), Step=1, Size=3pt,')
        exo.append(r'end=false, endlabel=false, beginlabel=false, NoZero));')
        exo.append(r'labelx(L=scale(.7)*"$0$", (0,0), align=SW);')
        exo.append(r'label("$\mathcal C_f$", (-6, f(-6)), 1.5%sE, brown);' % ('NS'[self.lY1[1] > self.lY1[0]]))
        exo.append(r'draw(Cf, brown+1.5);')
        exo.append(r'tangente(1,lg=sqrt(%s));' % (Fraction(self.dY1[1]).n ** 2 + Fraction(self.dY1[1]).d ** 2))
        exo.append(r'tangente(2,lg=sqrt(%s));' % (Fraction(self.dY1[2]).n ** 2 + Fraction(self.dY1[2]).d ** 2))
        exo.append(r'tangente(3,lg=sqrt(%s));' % (Fraction(self.dY1[3]).n ** 2 + Fraction(self.dY1[3]).d ** 2))
        exo.append(r'xlimits(-6.1, 6.1, Crop);')
        exo.append(r'ylimits(-5.5, 5.5, Crop);')
        exo.append(r'\end{asy}')
        exo.append(r'\end{minipage}')
        return exo

    def tex_answer(self):
        dY2 = list(self.dY2)
        for i in range(len(dY2)):
            if isinstance(dY2[i], Fraction): dY2[i] = 1. * dY2[i].n / dY2[i].d
        exo = [r'\exercice*']
        exo.append(r'\begin{enumerate}')
        exo.append(_(u'\\item  On lit graphiquement le coefficient directeur de chacune des tangentes en ces points.\par'))
        exo.append(u'$f\'\\,(%s)=%s \\qquad f\'\\,(%s)=%s \\qquad f\'\\,(%s)=%s$.' % (self.lX1[1], self.dY1[1], self.lX1[2], self.dY1[2], self.lX1[3], self.dY1[3]))
        exo.append(u'\\item')
        exo.append(r'\begin{asy}[height=6.5cm]')
        exo.append(r'import graph;')
        exo.append(r'import interpolate;')
        exo.append(r'import geometry;')
        exo.append(r'defaultpen(fontsize(9pt));')
        exo.append(r'real[] xpt={%s};' % (",".join([zfill(str(a), 2) for a in self.lX2])))
        exo.append(r'real[] ypt={%s};' % (",".join([zfill(str(a), 2) for a in self.lY2])))
        exo.append(r'real[] dy= {%s};' % (",".join([zfill(str(a), 2) for a in dY2])))
        exo.append(r'real f(real t){return pwhermite(xpt,ypt,dy)(t);}')
        exo.append(r'path Cf=graph(f,-6.1,6.1);')
        exo.append(r'void tangente(int k,real lg=sqrt(1+dy[k]^2),real ld=lg, pen p=black+1, arrowbar arr=Arrows(SimpleHead,size=9pt)) {')
        exo.append(r'draw(((xpt[k],ypt[k])-lg*unit((1,dy[k])))--((xpt[k],ypt[k])+ld*unit((1,dy[k]))),p,arr);')
        exo.append(r'dot((xpt[k],ypt[k]));')
        exo.append(r'}')
        exo.append(r'xlimits(%s, %s);' % (self.lX2[1] - 1.1, self.lX2[-2] + 1.1))
        exo.append(r'ylimits(-5.5, 5.5, Crop);')
        exo.append(r'xaxis(axis=BottomTop, p=invisible,')
        exo.append(r'ticks=Ticks(format="%", Step=1, extend=true,')
        exo.append(r'pTick=gray+.5pt, ptick=dotted)')
        exo.append(r');')
        exo.append(r'yaxis(axis=LeftRight, p=invisible,')
        exo.append(r'ticks=Ticks(format="%", Step=1, extend=true,')
        exo.append(r'pTick=gray+.5pt, ptick=dotted)')
        exo.append(r');')
        exo.append(r'xequals(L="$y$", 0, extend=false, arrow=Arrow(HookHead, size=9pt), p=black+1,')
        exo.append(r'ticks=Ticks(scale(.7)*Label(filltype=Fill(white)), Step=1, Size=3pt,')
        exo.append(r'end=false, endlabel=false, beginlabel=false, NoZero));')
        exo.append(r'yequals(L="$x$", 0, extend=false, arrow=Arrow(HookHead, size=9pt), p=black+1,')
        exo.append(r'ticks=Ticks(scale(.7)*Label(filltype=Fill(white)), Step=1, Size=3pt,')
        exo.append(r'end=false, endlabel=false, beginlabel=false, NoZero));')
        exo.append(r'labelx(L=scale(.7)*"$0$", (0,0), align=SW);')
        exo.append(r'label("$\mathcal C_f$", (-6, f(-6)), 1.5%sE, brown);' % ('NS'[self.lY2[1] > self.lY2[0]]))
        exo.append(r'draw(Cf, brown+1);')
        exo.append(r'tangente(1,lg=sqrt(%s));' % (Fraction(self.dY2[1]).n ** 2 + Fraction(self.dY2[1]).d ** 2))
        exo.append(r'tangente(2,lg=sqrt(%s));' % (Fraction(self.dY2[2]).n ** 2 + Fraction(self.dY2[2]).d ** 2))
        exo.append(r'tangente(3,lg=sqrt(%s));' % (Fraction(self.dY2[3]).n ** 2 + Fraction(self.dY2[3]).d ** 2))
        exo.append(r'tangente(4,lg=sqrt(%s));' % (Fraction(self.dY2[4]).n ** 2 + Fraction(self.dY2[4]).d ** 2))
        exo.append(r'xlimits(%s, %s, Crop);' % (self.lX2[1] - 1.1, self.lX2[-2] + 1.1))
        exo.append(r'ylimits(-5.5, 5.5, Crop);')
        exo.append(r'\end{asy}')
        exo.append(r'\end{enumerate}')
        return exo
