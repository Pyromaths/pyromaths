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

#
# ------------------- Diagrammes -------------------
#


def exo_diagrammes():
    exo = ["\\exercice"]
    cor = ["\\exercice*"]
    h1 = random.randrange(2) + 5
    h2 = 8
    h3 = random.randrange(2) + 7
    h5 = random.randrange(4)+1
    h6 = random.randrange(3)
    h7 = random.randrange(2)+1
    h4 = 30 - h1 - h2 - h3 - h5 - h6 - h7
    basket = random.randrange(7) + 3
    tennis = random.randrange(7) + 3
    judo = random.randrange(7) + 3
    football = 30 - tennis - basket - judo
    question1 = \
        u"""\\renewcommand{\\arraystretch}{1.8}
        \\item On a demandé aux élèves d'une classe de cinquième combien de temps par semaine était consacré à leur sport favori.\\par
    \\begin{tabular}{|c|c|c|c|c|c|c|c|}\\hline Durée t (en h)&  $0 \\le t < 1$ & $1 \\le t  < 2$ & $2 \\le t  < 3$ & $3 \\le t  < 4$ &  $4 \\le t  < 5$ & $5 \\le t  < 6$ & $6 \\le t  < 7$ \\\\\\hline Effectif & %s & %s & %s & %s & %s & %s & %s \\\\\\hline \\end{tabular}\\par
    À partir de ce tableau, construire un  histogramme pour représenter ces données.\\par""" % (h1, h2, h3, h4, h5, h6, h7)
    question2 = \
        u"""\\item On a demandé aux élèves quel était leur sport préféré. %s élèves préfèrent le basket-ball, %s le tennis, %s le football et %s le judo. Construire un diagramme circulaire représentant cette répartion.\\par""" % (basket, tennis, football, judo)
    exo.append("\\begin{enumerate}")
    exo.append(question1)
    exo.append(question2)
    exo.append("\\end{enumerate}")
    cor.append("\\begin{enumerate}")
    cor.append(question1)
    cor.append(u"""\\begin{minipage}{10cm}
    \\begin{pspicture}(0,-1)(8.5,9.5)
    \\psaxes[showorigin=false]{->}(7.5,8.5)
    \\psset{fillstyle=solid,fillcolor=gray,linewidth=0.5pt}
    \\psframe(0,0)(1,%s)
    \\psframe(1,0)(2,%s)
    \\psframe(2,0)(3,%s)
    \\psframe(3,0)(4,%s)
    \\psframe(4,0)(5,%s)
    \\psframe(5,0)(6,%s)
    \\psframe(6,0)(7,%s)
    \\rput(-0.2,-0.425){$0$}
    \\rput(8.3,0){Durée}
    \\rput(0,8.8){Effectif}
    \\end{pspicture}
    \\end{minipage}
    \\begin{minipage}{6cm}
    Sur l'axe horizontal, on représente les durées en heures et, sur l'axe vertical, on représente les effectifs.
    \\end{minipage}""" % (h1, h2, h3, h4, h5, h6, h7))
    cor.append(question2)
    cor.append(u"L'effectif total est égal à $ %s + %s + %s + %s = 30$. La mesure d'angle d'un secteur circulaire est proportionnelle à l'effectif du sport qu'il représente. Le coefficient de proportionnalité est égal au quotient de l'effectif total par 360\\degre c'est à dire $360 \\div 30=12$.\\par" % (basket, tennis, football, judo))
    cor.append(u"""\\renewcommand\\tabcolsep{10pt}
    \\begin{tabular}{|l|c|c|c|c|c|c}
    \\cline{1-6}
    Sport favori  & Basket-ball & Tennis & Football & Judo & Total &\\rnode{plan1}{}\\\\
    \\cline{1-6}
    Effectif & %s & %s & %s & %s & 30 &\\rnode{plan1}{}\\\\
    \\cline{1-6}
    Mesure (en degré)  & \\bf%s & \\bf%s & \\bf%s & \\bf%s & 360 &\\rnode{plan2}{}\\\\
    \\cline{1-6}
    \\end{tabular}
    \\ncbar{->}{plan1}{plan2}\\Aput{$\\times 12$}\\par
    \\begin{minipage}{6cm}
    En utilisant les mesures d'angles obtenues dans le tableau de proportionnalité, on trace le diagramme circulaire.
    \\end{minipage}""" % (basket, tennis, football, judo, basket*12, tennis*12, football*12, judo*12))
    cor.append(u"""\\begin{minipage}{13cm}
    \\psset{unit=3cm,fillstyle=solid}
    \\pspicture(-1.5,-1)(1,1.5)
    \\pswedge[fillcolor=lightgray]{1}{0}{%s}
    \\pswedge[fillcolor=gray]{1}{%s}{%s}
    \\pswedge[fillcolor=darkgray]{1}{%s}{%s}
    \\pswedge{1}{%s}{360}
    \\rput(.6;%s){Basket}
    \\rput(.6;%s){Tennis}
    \\rput(.6;%s){\\white Football}
    \\rput(.6;%s){Judo}
    \\endpspicture
    \\end{minipage}""" %(basket*12, basket*12, basket*12+tennis*12, basket*12+tennis*12, basket*12+tennis*12+football*12, basket*12+tennis*12+football*12, basket*6, basket*12+tennis*6, basket*12+tennis*12+football*6, basket*6+tennis*6+football*6+180 ))
    cor.append(u"\\end{enumerate}")
    return (exo, cor)