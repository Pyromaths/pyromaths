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
from __future__ import unicode_literals
from builtins import str
import random
from pyromaths.outils.decimaux import decimaux

#
# ------------------- Aire de disques -------------------
#


def arrondir(nombre):
    [partie_entiere, partie_decimale] = nombre.split(".")
    return int(partie_entiere) + (int(partie_decimale[0]) >= 5)


def exo_aire_diques():
    exo = ["\\exercice"]
    cor = ["\\exercice*"]
    rayon1 = 2 * (random.randrange(33) + 1)
    rayon2 = int(1.5 * rayon1)
    i = random.randrange(2)
    if i == 0:
        donnees = (_('rayons'), rayon1, rayon2)
    else:
        donnees = (_(u'diamètres'), 2 * rayon1, 2 * rayon2)
    difference_des_carres = rayon2 ** 2 - rayon1 ** 2
    aire_arrondie = arrondir(str(3.14 * difference_des_carres))
    enonce = \
        _(u"""\\begin{minipage}{4cm}
\\begin{pspicture}(-2,-2)(2,2)
\\pscircle[fillstyle=solid](0,0){1.5}
\\pscircle[fillstyle=solid, fillcolor=white](0,0){1}
\\psdots[dotstyle=x](0,0)
\\rput(0.3;60){$O$}
\\end{pspicture}
\\end{minipage}\\hfill
\\begin{minipage}{13cm}
On considère deux cercles de centre $O$ et de %s respectifs $\\unit[%s]{cm}$ et $\\unit[%s]{cm}$.\\par
Calculer l'aire de la couronne circulaire (partie colorée) comprise entre les deux cercles en arrondissant le résultat au $\\unit{cm^2}$ le plus proche.""") % donnees
    exo.append(enonce)
    cor.append(enonce)
    cor.append(_("\\par\\dotfill{}\\\\\n"))
    if i == 0:
        cor.append(_(u"On calcule l'aire du disque de rayon $\\unit[%s]{cm}$:") % rayon2)
        cor.append(_(u"\\[\\pi \\times %s^2 = \\pi \\times %s \\times %s = \\unit[%s \\pi]{cm^2}\\]") % (rayon2, rayon2, rayon2, decimaux(rayon2 ** 2)))
        cor.append(_(u"On calcule l'aire du disque de rayon $\\unit[%s]{cm}$:") % rayon1)
        cor.append(_(u"\\[ \\pi \\times %s^2 = \\pi \\times %s \\times %s = \\unit[%s \\pi]{cm^2}\]") % (rayon1, rayon1, rayon1, decimaux(rayon1 ** 2)))
    else:
        cor.append(_(u"Un disque de diamètre $\\unit[%s]{cm}$ a pour rayon $%s \div 2 = \\unit[%s]{cm}$. Calculons son aire:") % (2 * rayon2, 2 * rayon2, rayon2))
        cor.append(_(u"\\[\\pi \\times %s^2 = \\pi \\times %s \\times %s = \\unit[%s \\pi]{cm^2}\\]") % (rayon2, rayon2, rayon2, decimaux(rayon2 ** 2)))
        cor.append(_(u"Un disque de diamètre $\\unit[%s]{cm}$ a pour rayon $%s \div 2 = \\unit[%s]{cm}$. Calculons son aire:") % (2 * rayon1, 2 * rayon1, rayon1))
        cor.append(_(u"\\[\\pi \\times %s^2 = \\pi \\times %s \\times %s = \\unit[%s \\pi]{cm^2}\\]") % (rayon1, rayon1, rayon1, decimaux(rayon1 ** 2)))
    cor.append(_(u"L'aire $\\mathcal{A}$ de la couronne est obtenue en retranchant l'aire du disque de rayon  $\\unit[%s]{cm}$  à l'aire du disque de rayon  $\\unit[%s]{cm}$:") % (rayon1, rayon2))
    cor.append(u"\\[\\mathcal{A} = %s \\pi  - %s \\pi= (%s - %s)\\pi =\\unit[%s \\pi]{cm^2}\\]" % (decimaux(rayon2 ** 2), decimaux(rayon1 ** 2), decimaux(rayon2 ** 2), decimaux(rayon1 ** 2), decimaux(difference_des_carres)))
    cor.append(_(u"L'aire exacte de la couronne est $\\unit[%s \\pi]{cm^2}$.") % (decimaux(difference_des_carres)))
    cor.append(_(u"En prenant 3,14 comme valeur approchée du nombre $\\pi$, on obtient :"))
    cor.append(u"\\[\\mathcal{A}  \\approx %s \\times 3,14\\]" % decimaux(difference_des_carres))
    cor.append(u"\\[\\boxed{\\mathcal{A} \\approx  \\unit[%s]{cm^2}}\\]" % decimaux(aire_arrondie))
    exo.append("\\end{minipage}\n")
    cor.append("\\end{minipage}\n")
    return (exo, cor)

exo_aire_diques.description = _(u'Aire de disques')
