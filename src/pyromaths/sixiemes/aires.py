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
#import sys, os
#sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import random
from pyromaths.outils import Affichage
def boxes():
    """Crée les boites pour insérer les figures dans un environnement 36x16"""
    b0x, b0y = random.randrange(5, 2*36/3-1), random.randrange(5, 2*16/3+1)
    b1x, b1y = random.randrange(5,  2*(36-b0x)/3-1), random.randrange(5,
            2*16/3+1)
    b2x, b2y = 36-b0x-b1x-2, random.randrange(5, 2*16/3+1)
    b3x, b3y = b0x, 16-b0y-1
    b4x, b4y = b1x, 16-b1y-1
    b5x, b5y = b2x, 16-b2y-1
    return (b0x, b0y), (b1x, b1y), (b2x, b2y), (b3x, b3y), (b4x, b4y), (b5x,
            b5y)

def carre(dim, n_fig):
    """Dessine en psTricks un carre de dimensions inf(dim) et numérote la figure
    avec n_fig"""
    if dim[0]<dim[1]: dim = (dim[0], dim[0])
    else: dim = (dim[1], dim[1])
    f = "\\psframe[fillstyle=hlines](0, 0)(%s, %s)\n" % dim
    f += "\\rput(%.2f,%.2f)" % isobarycentre((0, 0), dim)
    f += "{\\psframebox[linecolor=white, fillcolor=white, fillstyle=solid]{figure %s}} " %  n_fig
    s = u"Aire de la figure %s : $%s = %s$~unités d'aire" %(n_fig,
            aire_rectangle(dim)[0], aire_rectangle(dim)[1])
    return (f, f, s)

def rectangle(dim, n_fig):
    """Dessine en psTricks un rectangle de dimensions dim et numérote la figure
    avec n_fig"""
    f = "\\psframe[fillstyle=hlines](0, 0)(%s, %s)\n" % dim
    f += "\\rput(%.2f,%.2f)" % isobarycentre((0, 0), dim)
    f += "{\\psframebox[linecolor=white, fillcolor=white, fillstyle=solid]{figure %s}}" %  n_fig
    s = u"Aire de la figure %s : $%s = %s$~unités d'aire" %(n_fig,
            aire_rectangle(dim)[0], aire_rectangle(dim)[1])
    return (f, f, s)

def parallelogramme(dim, n_fig):
    """Dessine en psTricks un parallelogramme inclus dans un rectangle de
    dimensions dim et numérote la figure avec n_fig"""
    base_h = random.randrange(2)
    if base_h:
        tab = random.randrange(1, min(dim[0]/2, dim[0]-3))*(-1)**random.randrange(2)
        if tab>0:
            s0, s1, s2, s3 = (tab, 0), (dim[0], 0), (dim[0]-tab, dim[1]), (0,
                    dim[1])
            frame0, frame1 = s0, dim
        else:
            s0, s1, s2, s3 = (0, 0), (dim[0]+tab, 0), (dim[0], dim[1]), (-tab,
                    dim[1])
            frame0, frame1 = s0, (dim[0]+tab, dim[1])
    else:
        tab = random.randrange(1, min(dim[1]/2, dim[1]-3))*(-1)**random.randrange(2)
        if tab>0:
            s0, s1, s2, s3 = (0, tab), (dim[0], 0), (dim[0], dim[1]-tab), (0,
                    dim[1])
            frame0, frame1 = s0, dim
        else:
            s0, s1, s2, s3 = (0, 0), (dim[0], -tab), (dim[0], dim[1]), (0,
                    dim[1]+tab)
            frame0, frame1 = s0, (dim[0], dim[1]+tab)
    f = "\\pspolygon[fillstyle=hlines]%s%s%s%s\n" % (s0,
            s1, s2, s3)
    f += "\\rput(%.2f,%.2f)" % isobarycentre((0, 0), dim)
    f += "{\\psframebox[linecolor=white, fillcolor=white, fillstyle=solid]{figure %s}} " %  n_fig
    fc = "\\pspolygon%s%s%s%s\n" % (s0, s1, s2, s3)
    fc += "\\psframe[linestyle=dashed, fillstyle=hlines]%s%s\n" % (frame0, frame1)
    fc += "\\rput(%.2f,%.2f)" % isobarycentre((0, 0), dim)
    fc += "{\\psframebox[linecolor=white, fillcolor=white, fillstyle=solid]{figure %s}} " %  n_fig
    s = "Aire de la figure %s : " % n_fig
    s += u"c'est l'aire du rectangle en pointillés.\\par\n"
    s += u"$%s = %s$~unités d'aire" %(aire_rectangle(frame0, frame1)[0],
            aire_rectangle(frame0, frame1)[1])
    return (f, fc, s)

def triangle_rectangle(dim, n_fig):
    """Dessine en psTricks un triangle rectangle dans une boite de dimensions
    dim et numérote la figure avec n_fig"""
    sommets = [(0, 0), (dim[0], 0), dim, (0, dim[1])]
    s0 = random.randrange(4)
    s1, s2 = (s0+1)%4, (s0+2)%4
    s0, s1, s2 = sommets[s0], sommets[s1], sommets[s2]
    f = "\\pspolygon[fillstyle=hlines]%s%s%s\n" % (s0, s1,
            s2)
    f += "\\rput(%.2f,%.2f)" % isobarycentre(s0, s1, s2)
    f += "{\\psframebox[linecolor=white, fillcolor=white, fillstyle=solid]{figure %s}} " %  n_fig
    fc = "\\psframe[linestyle=dashed]%s%s\n" % (s0, s2)
    fc += f
    s = "Aire de la figure %s : " % n_fig
    s += u"c'est la moitié de l'aire du rectangle en pointillés.\\par\n"
    s += u"$(%s) \\div 2= %s$~unités d'aire" %(aire_rectangle(dim)[0],
            Affichage.decimaux(aire_rectangle(dim)[1]/2., 1))
    return f, fc, s

def triangle_base(dim, n_fig):
    """Dessine en psTricks un triangle avec une base horizontale ou verticale
    dans une boite de dimensions dim et numérote la figure avec n_fig"""
    sommets = [(0, 0), (dim[0], 0), dim, (0, dim[1])]
    s0 = random.randrange(4)
    s1 = (s0+1)%4
    x0, x1 = sommets[(s0+2)%4][0], sommets[(s0+3)%4][0]
    y0, y1 = sommets[(s0+2)%4][1], sommets[(s0+3)%4][1]
    if x0>x1: x0, x1 = x1, x0
    if y0>y1: y0, y1 = y1, y0
    if x0 != x1: x0 = random.randrange(x0+1, x1)
    if y0 != y1: y0 = random.randrange(y0+1, y1)
    s2 = (x0, y0)
    s0, s1 = sommets[s0], sommets[s1]
    f = "\\pspolygon[fillstyle=hlines]%s%s%s\n" % (s0, s1,
            s2)
    f += "\\rput(%.2f,%.2f)" % isobarycentre(s0, s1, s2)
    f += "{\\psframebox[linecolor=white, fillcolor=white, fillstyle=solid]{figure %s}} " %  n_fig
    fc = "\\psframe[linestyle=dashed]%s%s\n" % (s0, s2)
    fc += "\\psframe[linestyle=dashed]%s%s\n" % (s2, s1)
    fc += f
    s = "Aire de la figure %s : " % n_fig
    s += u"c'est la moitié de l'aire du rectangle en pointillés.\\par\n"
    s += u"$(%s) \\div 2= %s$~unités d'aire" %(aire_rectangle(dim)[0],
            Affichage.decimaux(aire_rectangle(dim)[1]/2., 1))
    return f, fc, s

def triangle_qcq(dim, n_fig):
    """Dessine en psTricks un triangle quelconque dans une boite de dimensions
    dim et numérote la figure avec n_fig"""
    sommets = [(0, 0), (dim[0], 0), dim, (0, dim[1])]
    s0 = random.randrange(4)
    angle0, angle1, angle2 = sommets[(s0+1)%4], sommets[(s0+2)%4], sommets[(s0+3)%4]
    x0, x1 = sommets[(s0+1)%4][0], sommets[(s0+2)%4][0]
    y0, y1 = sommets[(s0+1)%4][1], sommets[(s0+2)%4][1]
    if x0>x1: x0, x1 = x1, x0
    if y0>y1: y0, y1 = y1, y0
    if x0 != x1: x0 = random.randrange(x0+1, x1)
    if y0 != y1: y0 = random.randrange(y0+1, y1)
    s1 = (x0, y0)
    x0, x1 = sommets[(s0+2)%4][0], sommets[(s0+3)%4][0]
    y0, y1 = sommets[(s0+2)%4][1], sommets[(s0+3)%4][1]
    if x0>x1: x0, x1 = x1, x0
    if y0>y1: y0, y1 = y1, y0
    if x0 != x1: x0 = random.randrange(x0+1, x1)
    if y0 != y1: y0 = random.randrange(y0+1, y1)
    s2 = (x0, y0)
    s0 = sommets[s0]
    f = "\\pspolygon[fillstyle=hlines]%s%s%s\n" % (s0, s1,
            s2)
    f += "\\rput(%.2f,%.2f)" % isobarycentre(s0, s1, s2)
    f += "{\\psframebox[linecolor=white, fillcolor=white, fillstyle=solid]{figure %s}}" %  n_fig
    fc = "\\psframe[linestyle=dashed](0,0)(%s,%s) " % dim
    fc += "\\rput(%.2f,%.2f){\\pscirclebox{1}} " % isobarycentre(s0, s1, angle0)
    fc += "\\rput(%.2f,%.2f){\\pscirclebox{2}} " % isobarycentre(s1, s2, angle1)
    fc += "\\rput(%.2f,%.2f){\\pscirclebox{3}}\n" % isobarycentre(s2, s0, angle2)
    fc += f
    s = "Aire de la figure %s : " % n_fig
    s += u"on calcule l'aire du rectangle en pointillés et on soustrait "
    s += "les aires des triangles rectangles \\pscirclebox{1}, "
    s += "\\pscirclebox{2} et \\pscirclebox{3}.\\par\n"
    s += "$(%s) - (%s) \\div 2 - (%s) \\div 2 - (%s) \\div 2 " %\
            (aire_rectangle(dim)[0], aire_rectangle(s0, s1)[0],
                    aire_rectangle(s1, s2)[0], aire_rectangle(s2, s0)[0])
    s += u"= %s$~unités d'aire" % Affichage.decimaux(aire_rectangle(dim)[1] -
            aire_rectangle(s0, s1)[1]/2. - aire_rectangle(s0, s2)[1]/2. -
            aire_rectangle(s1, s2)[1]/2., 1)
    return f, fc, s

def aire_rectangle(pos1, pos2=(0, 0)):
    """Affiche le calcul et le résultat de l'aire d'un rectangle, les
    coordonnées de deux sommets opposés étant pos1 et pos2"""
    dx = abs(pos1[0] - pos2[0])
    dy = abs(pos1[1] - pos2[1])
    return ("%s \\times %s" % (dx, dy), dx*dy)

def isobarycentre(*args):
    nbarg = len(args)*1.
    isobar = [0, 0]
    for i in args:
        isobar = [isobar[0]+i[0]/nbarg, isobar[1]+i[1]/nbarg]
    return tuple(isobar)

def figure():
    """Dessine en psTricks la figure de l'exercice sur les aires (quadrillage et
    figures géométriques)"""
    exo, cor, sol = [], [], ["\\begin{enumerate}"]
    t = "\\begin{pspicture}(0,0)(18,9)\n"
    t += "\\psgrid[subgriddiv=2, gridlabels=0pt]\n"
    t += "\\psframe[fillstyle=vlines, hatchsep=1pt](0,0)(.5,.5)\n"
    t += u"\\rput[l](0.6,0.25){\\psframebox[linecolor=white, fillcolor=white, fillstyle=solid]{unité d'aire}}\n"
    t += "\\psset{unit=5mm}\n"
    exo.append(t)
    cor.append(t)
    dim0, dim1, dim2, dim3, dim4, dim5 = boxes()
    xtab0 = 0
    ytab3 = ytab4 = ytab5 = 2
    xtab1 = dim0[0] + 1
    xtab2 = dim0[0] + dim1[0] + 2
    ytab0 = dim3[1]+3
    ytab1 = dim4[1]+3
    ytab2 = dim5[1]+3
    fig = [carre, rectangle, triangle_rectangle, triangle_base, triangle_qcq, parallelogramme]
    for i in range(len(fig)):
        r = fig.pop(random.randrange(len(fig)))(eval('dim'+str(i)), i+1)
        exo.append("\\rput(%s,%s){\n" % (eval('xtab' + str(i%3)),
                eval('ytab' + str(i)))+ r[0] + '\n}')
        cor.append("\\rput(%s,%s){\n" % (eval('xtab' + str(i%3)),
                eval('ytab' + str(i)))+ r[1] + '\n}')
        sol.append("\\item %s" % r[2])
    exo.append("\\end{pspicture}")
    cor.append("\\end{pspicture}")
    cor.extend(sol)
    cor.append("\\end{enumerate}")
    return("\n".join(exo), "\n".join(cor))

def main():
    exo, cor, sol = [], [], []
    exo = ["\\exercice", u"Calculer l'aire de chacune des figures suivantes dans l'unité d'aire donnée :\\par"]
    cor = ["\\exercice*", u"Calculer l'aire de chacune des figures suivantes dans l'unité d'aire donnée :\\par"]
    exercice = figure()
    exo.append(exercice[0])
    cor.append(exercice[1])
    return(exo, cor)
