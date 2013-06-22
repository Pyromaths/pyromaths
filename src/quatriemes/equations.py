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

from ..outils import Arithmetique
from ..troisiemes import fractions
from ..troisiemes import developpements

#
# ------------------- ÉQUATIONS -------------------


def valeurs(pyromax):  # crée les valeurs aléatoires pour l'équation
    sgn = Arithmetique.valeur_alea(-1, 1)
    while True:
        coefs = [Arithmetique.valeur_alea(-pyromax, pyromax) for i in range(6)]
        if ((coefs[0] + coefs[2] * sgn) - coefs[4]) != 0:
            break
    if sgn > 0:
        signe = "+"
    else:
        signe = "-"
    return (tuple(coefs), (signe, sgn))


def tex_equation0(valeurs):  # renvoie l'ecriture des quotients au meme denominateur
    texte = ''
    for i in range(3):
        texte = texte + developpements.tex_binome((valeurs[0][i * 2],
                valeurs[0][i * 2 + 1]), bplus=i == 1 and valeurs[1][1] >
                0, bpar=i == 1 and valeurs[1][1] < 0)
        if i == 0 and valeurs[1][1] < 0:
            texte = texte + valeurs[1][0]
        elif i == 1:
            texte = texte + '='
    return texte


def tex_equation0bis(valeurs):  # renvoie l'ecriture des quotients au meme denominateur sans les parentheses eventuelles
    texte = developpements.tex_binome((valeurs[0][0], valeurs[0][1]))
    texte = texte + developpements.tex_binome((valeurs[0][2] * valeurs[1][1],
            valeurs[0][3] * valeurs[1][1]), bplus=1)
    texte = texte + '=' + developpements.tex_binome((valeurs[0][4],
            valeurs[0][5]))
    return texte


def tex_equation1(valeurs):  # renvoie l'ecriture reduite de l'equation sans denominateur
    texte = developpements.tex_binome((valeurs[0][0] + valeurs[0][2] *
            valeurs[1][1], valeurs[0][1] + valeurs[0][3] * valeurs[1][1]))
    texte = texte + '=' + developpements.tex_binome((valeurs[0][4],
            valeurs[0][5]))
    return texte


def tex_equation2(valeurs):  # renvoie l'ecriture de l'equation avec l'inconnue d'un cote de l'egalite
    texte = developpements.tex_coef(valeurs[0][0] + valeurs[0][2] *
                                    valeurs[1][1], 'x') + developpements.tex_coef(-valeurs[0][4],
            'x', bplus=1)
    texte = texte + '=' + developpements.tex_coef(valeurs[0][5], '') + \
        developpements.tex_coef(-valeurs[0][1] - valeurs[0][3] * valeurs[1][1],
                                '', bplus=1)
    return texte


def tex_equation3(valeurs):  # renvoie l'ecriture reduite de l'equation avec l'inconnue d'un cote de l'egalite
    texte = developpements.tex_coef((valeurs[0][0] + valeurs[0][2] *
                                    valeurs[1][1]) - valeurs[0][4], 'x')
    texte = texte + '=' + developpements.tex_coef((valeurs[0][5] -
            valeurs[0][1]) - valeurs[0][3] * valeurs[1][1], '', ecu=1)
    return texte


def tex_equation4(valeurs):  # renvoie la solution de l'equation
    frac = ((valeurs[0][5] - valeurs[0][1]) - valeurs[0][3] * valeurs[1][1],
            (valeurs[0][0] + valeurs[0][2] * valeurs[1][1]) - valeurs[0][4])
    if (valeurs[0][0] + valeurs[0][2] * valeurs[1][1]) - valeurs[0][4] == \
        1:
        texte = ''
    else:
        #texte = 'x=' + fractions.tex_frac(frac)    # <-- MIO
        texte = 'x=\\cfrac{%s}{%s}' % frac
        simpl = fractions.simplifie(frac)
        if isinstance(simpl, tuple):
            texte = texte + '=' + fractions.tex_frac(simpl)
    return texte


def equations(exo, cor):  #resolution d'une equation
    exo.append(_(u"Résoudre les suivantes équations: "))
    exo.append('\\begin{multicols}{2}\\noindent')
    cor.append(_(u"Résoudre les suivantes équations: "))
    cor.append('\\begin{multicols}{2}\\noindent')
    for j in range(2):
        vals = valeurs(10)
        exo.append(u'$$ ' + tex_equation0(vals) + '$$ ')
        for i in range(5):
            exec('cor.append(u\'$$\' + tex_equation' + str(i) + '(vals) + \'$$ \')')
            if i == 0 and vals[1][1] < 0:
                cor.append(u'$$ ' + tex_equation0bis(vals) + '$$ ')
        frac = ((vals[0][5] - vals[0][1]) - vals[0][3] * vals[1][1],
                (vals[0][0] + vals[0][2] * vals[1][1]) - vals[0][4])
        simpl = fractions.simplifie(frac)
        if isinstance(simpl, tuple):
            sol = fractions.tex_frac(simpl)
        else:
            sol = fractions.tex_frac(frac)
        cor.append(u'\\begin{center}')
        cor.append(_(u'\\fbox{La solution de cette équation est $%s$\\,}') %
                 sol)
        cor.append(u'\\end{center}')
        if j % 2 == 0:
            exo.append('\\columnbreak\\stepcounter{nocalcul}%')
            cor.append('\\columnbreak\\stepcounter{nocalcul}%')
    exo.append('\\end{multicols}')
    cor.append('\\end{multicols}')
    

def tex_equations():
    exo = ['\\exercice']
    cor = ['\\exercice*']
    equations(exo, cor)
    return (exo, cor)
