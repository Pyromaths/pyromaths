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
from __future__ import division
from __future__ import unicode_literals
from builtins import range
from past.utils import old_div
from random import randint, randrange
from pyromaths.outils.decimaux import decimaux

def ncotation(A, B, longueur, couleur=""):
    """trace une flèche et inscrit horizontalement, dessous, la longueur entre A et B
    où A et B sont des \node"""
    linecouleur = ""
    if couleur != "":
        linecouleur = ",linecolor = %s" % couleur
        couleur = "\\color{%s}" % couleur
    return u"\\ncline[linestyle=dashed, offset = -1.5, linewidth = 0.4pt %s]{<->}{%s}{%s}  \\Bput{%s %s}" % (linecouleur, A, B, couleur, longueur)

def ncotation_h(A, B, longueur, couleur=""):
    """idem mais au dessus de la flèche"""
    linecouleur = ""
    if couleur != "":
        linecouleur = ",linecolor = %s" % couleur
        couleur = "\\color{%s}" % couleur
    return u"\\ncline[linestyle=dashed, offset = 1.5, linewidth = 0.4pt %s]{<->}{%s}{%s}  \\Aput{%s %s}" % (linecouleur, A, B, couleur, longueur)


def exo_echelles():
    """À partir d'un plan tracé, déterminer l'échelle et des longueurs déterminées."""

    # Échelle
    echelle = [ 100, 250, 400, 500, 750, 1000][randrange(6)]

    # figure : un plan d'appartement déssiner en psTricks
    a, d = randint(40, 60), randint(36, 45)
    b, c = randint(8, d - 27), randint(9, a - 25)
    xF = a - c
    xE = xF - 6
    yK = b + 9
    yF = b - 6
#     yH = b
    # Calculs des grandeurs réelles en mm !
    reels = [echelle * a, echelle * b, echelle * c, echelle * d]

    plan = [a, b, c, d]
    # choix permet de choisir si on donne a, b, c ou d en énoncé
    choix = randrange(4)
    reponses = ["a", "b", "c", "d"]
    enonce = reponses.pop(choix)

    # sur la deuxième ligne du tableau, on écrit en cm, en gras, les nombres calculés
    tab_reels = [ "\\bf"*(i != choix) + decimaux(old_div(reels[i], 10.0)) for i in range(4)]

    # Pour placer les quatre lettres sur le plan
    cotation_couleur = [["a", ""],
                        ["b", ""],
                        ["c", ""],
                        ["d", ""]]
        # la longueur donnée est tracée en bleu
    cotation_couleur[choix][1] = "enonce"

    # figure PSTricks en fonction des paramètres a, d, xE, XF, yF
    figure = ["\\psset{PointName = none,  PointSymbol = none, unit = 1mm, linewidth = .5pt}",
              "\\definecolor{enonce}{rgb}{0.11,0.56,0.98}",
              "\\begin{pspicture}(-10mm, -10mm)(50mm ,50mm)",
              # le rectangle ABCD
              "\\pstGeonode[CurveType = polygon, linewidth = 1pt](0, 0)A(%s,0)B (%s, %s)C (0, %s)D" % (a, a, d, d),
              # les points permettant de placer les cloisons
              "\\pstGeonode(%s, 0){E1}(%s, %s){E2}(%s, 0){F1}(%s, %s){F2}" % (xE, xE, yF, xF, xF, yF),
              "\\pstGeonode(%s, %s){G1}(%s, %s){G2}(%s, %s){G3}" % (a, b, xF, b, xF, 25),
              "\\pstGeonode(%s, %s){H1}(%s, %s){H2}(%s, %s){H3}(%s, %s){H4}" % (xE, b, xE, 25, xE, yK, 15, yK),
              "\\pstGeonode(0, %s){K2}(7, %s){K1}" % (yK, yK),
              "\\pstGeonode(%s, %s){J1}(%s, %s){J2}(%s, %s){J3}(%s, %s){J4}" % (xE, d - 7, xE, d, xF, d - 7, xF, d),
              # trace les cloisons, limitées par des tirets
              "\\ncline{-|}{E1}{E2}\\ncline{-|}{F1}{F2}",
              "\\ncline{|-}{J1}{J2}\\ncline{|-}{J3}{J4}",
              "\\ncline{|-}{K1}{K2}",
              "\\ncline{G1}{G2}\\ncline{|-|}{G3}{G2}",
              "\\ncline{|-|}{H1}{H2}\\ncline{-|}{H3}{H4}",
              # place les cotations sr la figure, l'énoncé en bleu
              ncotation_h("D", "C", cotation_couleur[0][0], cotation_couleur[0][1]),
              ncotation("B", "G1", cotation_couleur[1][0], cotation_couleur[1][1]),
              ncotation("F1", "B", cotation_couleur[2][0], cotation_couleur[2][1]),
              ncotation_h("A", "D", cotation_couleur[3][0], cotation_couleur[3][1]),
              "\\end{pspicture}"]


    exo = [_(u"\\exercice Sur ce plan, la longueur $%s$ mesure en réalité \\unit[%s]{m} :\n") % (enonce, decimaux(old_div(reels[choix], 1000.0)))] \
          + figure + \
           ["\\begin{enumerate}",
           _(u"\\item Déterminer l'échelle de ce plan."),
           _(u"\\item Déterminer les longueurs réelles $%s$, $%s$ et $%s$.") % (reponses[0], reponses[1], reponses[2]),
            "\\end{enumerate}"]
    cor = [_(u"\\exercice* Sur ce plan, la longueur $%s$ mesure en réalité \\unit[%s]{m} : \n") % (enonce, decimaux(old_div(reels[choix], 1000.0)))] \
           + figure + \
          ["\\begin{enumerate}",
           _(u"\\item Déterminer l'échelle de ce plan.\\par"),
           _(u"Sur le plan, je mesure que $%s=\\unit[%s]{cm}$.\\par") % (enonce, decimaux(old_div(plan[choix], 10.0))),
           _(u"Or on sait que en réalité $%s = \\unit[%s]{m} = \\unit[%s]{cm}$") % (enonce, decimaux(old_div(reels[choix], 1000.0)), decimaux(old_div(reels[choix], 10.0))),
           _(u" et  $%s \\div %s = %s$.\\par") % (decimaux(reels[choix]), decimaux(plan[choix]), decimaux(echelle)),
           _(u"L'échelle de ce plan est donc $1/%s^e$.") % echelle,
           _(u"\\item Déterminer les longueurs réelles $%s$, $%s$ et $%s$.\n") % (reponses[0], reponses[1], reponses[2]),
           _(u"Grâce à la question précédente, je peux compléter le tableau :\n"),
           "\\begin{tabular}{|l|c|c|c|c|c}",
           ("\\multicolumn{1}{c}{}" + "&\\multicolumn{1}{c}{$%s$}"*4 + "\\\\") % ("a", "b", "c", "d"),
           "\\cline{1-5}",
           _("Sur le plan (en cm)  & %s & %s & %s & %s &\\rnode{plan1}{}\\\\") % tuple([decimaux(old_div(n, 10.0)) for n in plan]),
           "\\cline{1-5}",
           _(u"En réalité (en cm)  & %s & %s & %s & %s &\\rnode{plan2}{}\\\\") % tuple(tab_reels),
           "\\cline{1-5}",
           "\\end{tabular}\n",
           "\\ncbar{->}{plan1}{plan2}\\Aput{$\\times %s$}" % echelle,
           _(u"Pour conclure, on convertit ses longueurs en m :\\par"),
           "$$a = \\unit[%s]{m} \\quad ; \\quad b = \\unit[%s]{m} \\quad ; \\quad c  = \\unit[%s]{m} \\quad ; \\quad d =\\unit[%s]{m}$$"\
                   % tuple([decimaux(old_div(n, 1000.0)) for n in reels]),
           "\\end{enumerate}"]

    return exo, cor

exo_echelles.description = _(u'Échelles')


def exo_fruits():
    fruit = [_("Cerises"), _("Tomates"), _("Pommes"), _("Poires"), _("Raisin"), _("Oranges")][randrange(6)]
    while 1:
        a, b, c = old_div(randint(10, 50), 10.0), old_div(randint(10, 50), 10.0), old_div(randint(10, 50), 10.0)
        if a != b and a != c and b != c:
            break
    tarif = old_div(randint(20, 50), 10.0)
    fruits_c = (fruit, a, b, c)
    fruits_e = (fruit, decimaux(a), decimaux(b), "")
    prix_c = (_("prix"), decimaux(fruits_c[1] * tarif), decimaux(fruits_c[2] * tarif), decimaux(fruits_c[3] * tarif))
    prix_e = (_("prix"), decimaux(fruits_c[1] * tarif), "", decimaux(fruits_c[3] * tarif))

    fruits_c = (fruit, decimaux(a), decimaux(b), decimaux(c))
    tableau_exo = ["\\begin{tabular}{|l|c|c|c|}",
               "\hline",
               _(u"%s (en kg) & %s & %s &  %s  \\\\") % fruits_e,
               "\hline",
               _(u"%s (en \\euro)  & %s &  %s  & %s \\\\") % prix_e,
               "\hline",
               "\\end{tabular}"]
    tableau_cor = ["\\begin{tabular}{|l|c|c|c|}",
               "\hline",
               _(u"%s (en kg) & %s & %s &  \\bf %s  \\\\") % fruits_c,
               "\hline",
               _(u"%s (en \\euro)  & %s &  \\bf %s  & %s \\\\") % prix_c,
               "\hline",
               "\\end{tabular}"]
    exo = [_(u"\\exercice Le prix à payer est proportionnel à la masse de fruits achetés.\\par"),
           _(u"Détermine la valeur des cases vides")]
    cor = [_(u"\\exercice Le prix à payer est proportionnel à la masse de fruits achetés.\\par"),
           _(u"Détermine la valeur des cases vides")]
    exo += ["\n"] + tableau_exo
    cor += ["\n"] + tableau_cor
    cor.append("$$\\frac{%s \\times %s}{%s} = %s \\quad;\\qquad" % (prix_e[1], fruits_e[2], fruits_e[1], prix_c[2]))
    cor.append("\\frac{%s \\times %s}{%s} = %s $$" % (fruits_c[1], prix_c[3], prix_e[1], fruits_c[3]))

    return (exo, cor)
