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

import outils
from . import fractions
from . import developpements

#
# ------------------- ÉQUATIONS -------------------


def valeurs(pyromax):  # crée les valeurs aléatoires pour l'équation
    while True:
        coefs = [outils.valeur_alea(-pyromax, pyromax) for i in range(6)]
        sgn = outils.valeur_alea(-1, 1)
        if sgn > 0:
            signe = "+"
        else:
            signe = "-"
        while True:
            while True:
                dens = [outils.valeur_alea(2, 9) for i in range(3)]
                if dens[0] != dens[1] and dens[0] != dens[2] and dens[1] != \
                    dens[2]:
                    break
            ppcm = outils.ppcm(dens[0], outils.ppcm(dens[1], dens[2]))
            densprim = [ppcm // dens[i] for i in range(3)]
            if densprim[0] < 10 and densprim[1] < 10 and densprim[2] < \
                10:
                break

        nvxcoefs = [coefs[i] * densprim[i // 2] for i in range(6)]
        if (nvxcoefs[0] + nvxcoefs[2] * sgn) - nvxcoefs[4] != 0:
            break
    return (tuple(coefs), tuple(dens), tuple(densprim), (signe, sgn),
            tuple(nvxcoefs))


def tex_quotient0(a, b, c):  # renvoie l'ecriture d'un quotient de l'enonce
    return '\\cfrac{%s}{%s}' % (developpements.tex_binome((a, b)), c)


def tex_quotient1(a, b, c, d):  # renvoie l'ecriture de la mise au meme denominateur d'un quotient
    if d == 1:
        return tex_quotient0(a, b, c)
    else:
        return '\\cfrac{%s_{\\times%s}}{%s_{\\times%s}}' % (developpements.tex_binome((a,
                b), bpar=1), d, c, d)


def tex_equation0(valeurs):  # renvoie l'ecriture des quotients de l'enonce
    texte = ''
    for i in range(3):
        texte = texte + tex_quotient0(valeurs[0][i * 2], valeurs[0][i *
                2 + 1], valeurs[1][i])
        if i == 0:
            texte = texte + valeurs[3][0]
        elif i == 1:
            texte = texte + '='
    return texte


def tex_equation1(valeurs):  # renvoie l'ecriture de la mise au meme denominateur des quotients
    texte = ''
    for i in range(3):
        texte = texte + tex_quotient1(valeurs[0][i * 2], valeurs[0][i *
                2 + 1], valeurs[1][i], valeurs[2][i])
        if i == 0:
            texte = texte + valeurs[3][0]
        elif i == 1:
            texte = texte + '='
    return texte


def tex_equation2(valeurs):  # renvoie l'ecriture des quotients au meme denominateur
    texte = '\\cfrac{'
    for i in range(3):
        texte = texte + developpements.tex_binome((valeurs[4][i * 2],
                valeurs[4][i * 2 + 1]), bplus=i == 1 and valeurs[3][1] >
                0, bpar=i == 1 and valeurs[3][1] < 0)
        if i == 0 and valeurs[3][1] < 0:
            texte = texte + valeurs[3][0]
        elif i == 1:
            texte = texte + '}{\\cancel{%s}}=\cfrac{' % (valeurs[1][0] *
                    valeurs[2][0])
    texte = texte + '}{\\cancel{%s}}' % (valeurs[1][0] * valeurs[2][0])
    return texte


def tex_equation2bis(valeurs):  # renvoie l'ecriture des quotients au meme denominateur sans les parentheses eventuelles
    texte = developpements.tex_binome((valeurs[4][0], valeurs[4][1]))
    texte = texte + developpements.tex_binome((valeurs[4][2] * valeurs[3][1],
            valeurs[4][3] * valeurs[3][1]), bplus=1)
    texte = texte + '=' + developpements.tex_binome((valeurs[4][4],
            valeurs[4][5]))
    return texte


def tex_equation3(valeurs):  # renvoie l'ecriture reduite de l'equation sans denominateur
    texte = developpements.tex_binome((valeurs[4][0] + valeurs[4][2] *
            valeurs[3][1], valeurs[4][1] + valeurs[4][3] * valeurs[3][1]))
    texte = texte + '=' + developpements.tex_binome((valeurs[4][4],
            valeurs[4][5]))
    return texte


def tex_equation4(valeurs):  # renvoie l'ecriture de l'equation avec l'inconnue d'un cote de l'egalite
    texte = developpements.tex_coef(valeurs[4][0] + valeurs[4][2] *
                                    valeurs[3][1], 'x') + developpements.tex_coef(-valeurs[4][4],
            'x', bplus=1)
    texte = texte + '=' + developpements.tex_coef(valeurs[4][5], '') + \
        developpements.tex_coef(-valeurs[4][1] - valeurs[4][3] * valeurs[3][1],
                                '', bplus=1)
    return texte


def tex_equation5(valeurs):  # renvoie l'ecriture reduite de l'equation avec l'inconnue d'un cote de l'egalite
    texte = developpements.tex_coef((valeurs[4][0] + valeurs[4][2] *
                                    valeurs[3][1]) - valeurs[4][4], 'x')
    texte = texte + '=' + developpements.tex_coef((valeurs[4][5] -
            valeurs[4][1]) - valeurs[4][3] * valeurs[3][1], '')
    return texte


def tex_equation6(valeurs):  # renvoie la solution de l'equation
    frac = ((valeurs[4][5] - valeurs[4][1]) - valeurs[4][3] * valeurs[3][1],
            (valeurs[4][0] + valeurs[4][2] * valeurs[3][1]) - valeurs[4][4])
    if (valeurs[4][0] + valeurs[4][2] * valeurs[3][1]) - valeurs[4][4] == \
        1:
        texte = ''
    else:
        texte = 'x=' + fractions.tex_frac(frac)
        simpl = fractions.simplifie(frac)
        if isinstance(simpl, tuple):
            texte = texte + '=' + fractions.tex_frac(simpl)
    return texte


def equations(f0, f1, valeurs):  #resolution d'une equation
    f0.write(u"  Résoudre l'équation : \n")
    outils.ecrit_tex(f0, tex_equation0(valeurs), thenocalcul='')
    f1.write(u"  Résoudre l'équation : \n")
    for i in range(7):
        exec('outils.ecrit_tex(f1,tex_equation' + str(i) + \
            '(valeurs),thenocalcul=\'\')')
        if i == 2 and valeurs[3][1] < 0:
            outils.ecrit_tex(f1, tex_equation2bis(valeurs), thenocalcul=
                             '')
    frac = ((valeurs[4][5] - valeurs[4][1]) - valeurs[4][3] * valeurs[3][1],
            (valeurs[4][0] + valeurs[4][2] * valeurs[3][1]) - valeurs[4][4])
    simpl = fractions.simplifie(frac)
    if isinstance(simpl, tuple):
        sol = fractions.tex_frac(simpl)
    else:
        sol = fractions.tex_frac(frac)
    f1.write(u'  \\fbox{La solution de cette équation est $%s$\\,.}\n' %
             sol)


