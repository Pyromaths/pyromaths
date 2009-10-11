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
from math import atan, cos, pi, sin, floor, ceil

#===============================================================================
# Symétrique d'une figure par rapport à une droite avec quadrillage
#===============================================================================


def valeurs_quad2(nb_pts):
    vals = []
    for i in range(nb_pts):
        angle = random.randrange((i * 360) / nb_pts, ((i + 1) * 360) /
                                 nb_pts)
        vals.append(((random.randrange(1, 7) * .5) * cos((angle * pi) /
                    180), (random.randrange(1, 7) * .5) * sin((angle *
                    pi) / 180)))
    return vals


def valeurs_quad(nb_pts):
    vals = []
    for i in range(nb_pts):
        (alpha, beta) = ((i * 360) / nb_pts, ((i + 1) * 360) / nb_pts)
        (x, y) = (0, 0)
        while x == 0 or angle < alpha or angle > beta:
            (x, y) = (random.randrange(-6, 7) * .5, random.randrange(-6,
                      7) * .5)
            if x > 0:
                angle = int((atan((y * 1.0) / x) * 180) / pi + 360) % \
                    360
            if x < 0:
                angle = int((atan((y * 1.0) / x) * 180) / pi + 180)
        vals.append((x, y))
    return vals


def place_pts(vals, angle):
    txt = ["  \\pstGeonode[PointSymbol=x,PointName=none]"]
    for i in range(len(vals)):
        txt.append("(%s,%s)" % vals[i])
        txt.append("{%s}" % chr(i + 97))
    txt.append("\n\\pstGeonode[PointSymbol=x,PointName=none](-4.5;%s){A}(4.5;%s){B}" % (angle, angle))
    txt.append("\n\\psline[linewidth=1.5\\pslinewidth,nodesep=-4.5](A)(B)")
    txt.append("\n\\pspolygon")
    for i in range(len(vals)):
        txt.append("(%s)" % chr(i + 97))
    return ("").join(txt)


def SymetrieQuadrillage():
    exo = ["\\exercice", u"Construire la symétrique de chacune des figures par rapport à la droite en", "utilisant le quadrillage :\\par", "\\psset{unit=.9cm}"]
    cor = ["\\exercice*", u"Construire la symétrique de chacune des figures par rapport à la droite en", "utilisant le quadrillage :\\par", "\\psset{unit=.9cm}"]

    nbpts = 5
    langles = [0, 90, 45, 135]
    for j in range(3):
        angle = langles.pop(random.randrange(len(langles)))
        vals = valeurs_quad(nbpts)
        txt = place_pts(vals, angle)
        exo.append("\\begin{pspicture*}(-3,-3)(3,3)")
        exo.append("  \\psgrid[gridcolor=lightgray,subgridcolor=lightgray,subgriddiv=2,gridlabels=0pt]")
        exo.append(txt)
        cor.append("\\begin{pspicture*}(-3,-3)(3,3)")
        cor.append("  \\psgrid[gridcolor=lightgray,subgridcolor=lightgray,subgriddiv=2,gridlabels=0pt]")
        cor.append(txt)
        txt_cor = "\\pstOrtSym[PointSymbol=x,PointName=none]{A}{B}{"
        for i in range(len(vals)):
            if i > 0:
                txt_cor += ","
            txt_cor += "%s" % chr(i + 97)
        txt_cor += "}["
        for i in range(len(vals)):
            if i > 0:
                txt_cor += ","
            txt_cor += "%s1" % chr(i + 97)
        txt_cor += "]\n  \pspolygon[linecolor=gray,linestyle=dashed]"
        for i in range(len(vals)):
            txt_cor += "(%s1)" % chr(i + 97)
        cor.append(txt_cor)
        exo.append("\\end{pspicture*}")
        cor.append("\\end{pspicture*}")
        if j < 2:
            exo.append("\\hfill")
            cor.append("\\hfill")
    return (exo, cor)

