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
import string
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


def centre_sym(vals):
    fin = 0
    while not fin:
        (fin, cpt) = (1, 0)
        (o1, o2) = (random.randrange(-6, 7) * .5, random.randrange(-6, 7) *
                    .5)
        while fin and cpt < len(vals):
            fin = fin and -3 <= 2 * o1 - vals[cpt][0] <= 3 and -3 <= 2 * \
                o2 - vals[cpt][1] <= 3
            cpt = cpt + 1
    return (o1, o2)


def place_pts(vals, O):
    txt = ["  \\pstGeonode[PointSymbol=none,PointName=none]"]
    for i in range(len(vals)):
        txt.append("(%s,%s)" % vals[i])
        txt.append("{%s}" % chr(i + 97))
    txt.append("\n  \\pstGeonode[PointSymbol=x, linecolor=Black, dotsize=6pt](%s,%s){O}" % O)
    txt.append("\n  \\pspolygon[linewidth=1pt]")
    for i in range(len(vals)):
        txt.append("(%s)" % chr(i + 97))
    return ("").join(txt)


def place_pts_sym(vals):
    txt = ["  \\pstSymO[PointSymbol=x,PointName=none]{O}{"]
    for i in range(len(vals)):
        if i > 0:
            txt.append(",")
        txt.append("%s" % chr(i + 97))
    txt.append("}[")
    for i in range(len(vals)):
        if i > 0:
            txt.append(",")
        txt.append("%s1" % chr(i + 97))
    txt.append("]\n\pspolygon[linecolor=Black,linestyle=dashed, linewidth=1pt]")
    for i in range(len(vals)):
        txt.append("(%s1)" % chr(i + 97))
    return ("").join(txt)


def exo_quadrillage(f0, f1):
    pass


def main():
    exo = ["\\exercice",
           _(u"Construire la symétrique de chacune des figures par rapport au point O en"),
           _("utilisant le quadrillage :\\par"), "\\psset{unit=.9cm}"]
    cor = ["\\exercice*",
           _(u"Construire la symétrique de chacune des figures par rapport au point O en"),
           _("utilisant le quadrillage :\\par"), "\\psset{unit=.9cm}"]
    nbpts = 5
    for i in range(3):
        vals = valeurs_quad(nbpts)
        O = centre_sym(vals)
        txt = place_pts(vals, O)
        exo.append("\\begin{pspicture*}(-3,-3)(3,3)")
        exo.append("\\psgrid[subgriddiv=2,gridlabels=0pt]")
        exo.append(txt)
        cor.append("\\begin{pspicture*}(-3,-3)(3,3)")
        cor.append("\\psgrid[subgriddiv=2,gridlabels=0pt]")
        cor.append(txt)
        cor.append(place_pts_sym(vals))
        exo.append("\end{pspicture*}")
        cor.append("\end{pspicture*}")
        if i < 2:
            exo.append("\\hfill")
            cor.append("\\hfill")
    return (exo, cor)
