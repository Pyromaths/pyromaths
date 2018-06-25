#!/usr/bin/env python3
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
'''
Created on 21 janv. 2015

@author: jerome
'''
from __future__ import unicode_literals
from builtins import str
from builtins import range
from pyromaths import ex
from random import randrange
def listeToclasses(liste):
    result = [r'$[%s' % (liste[0])]
    for l in liste[1:]:
        result.append(r'$[%s' % (l + eval(result[-1][2:])))
        result[-2] = result[-2] + r' ~;~ %s[$' % (l + eval(result[-2][2:]))
    result.pop(-1)
    return result

class _Histogramme(ex.TexExercise):
    """Construire un histogramme"""

    tags = ["Seconde"]

    def __init__(self):
        '''
        Constructor
        '''
        echelle1 = 5 * 2 ** randrange(1, 6)
        debut = randrange(0, 4) * 10 ** randrange(0, 4)
        classes = [debut]
        classes.extend([echelle1 * randrange(1, 5) for dummy in range(randrange(4, 6))])
        echelle2 = 5 * 2 ** randrange(1, 6)
        effectifs = [echelle2 * randrange(1, 5) for dummy in range(len(classes) - 1)]
        self.classes = classes
        self.effectifs = effectifs
        self.echelle1 = echelle1
        self.echelle2 = echelle2

    def tex_statement(self):
        exo = [r'\exercice']
        exo.append(_(u'Tracer l\'histogramme de la série ci-dessous :\\par'))
        exo.append(r'\begin{tabularx}{.8\linewidth}[t]{|l|*{%s}{>{\centering\arraybackslash}X|}}' % len(self.classes))
        exo.append(_(r'\hline Classe & %s \\' % " & ").join(listeToclasses(self.classes)))
        exo.append(_(r'\hline Effectif & %s \\ \hline') % " & ".join([str(i) for i in self.effectifs]))
        exo.append(r'\end{tabularx}')
        return "\n".join(exo)

    def tex_answer(self):
        exo = [r'\exercice*']
        exo.append(r'\begin{center}')
        exo.append(r'\begin{asy}')
        exo.append(r'import stats;')
        exo.append(r'import graph;')
        exo.append(r'size(15cm,7cm,false);')
        # exo.append(r'unitsize(1cm);')
        exo.append(r'real[] tabxi={%s};' % ",".join([str(sum(self.classes[:i + 1])) for i in range(len(self.classes))]))
        exo.append(r'real[] tabni={%s};' % ",".join([str(i) for i in self.effectifs]))
        exo.append(r'real uniteaire=%s;' % self.echelle2)
        exo.append(r'string libelleunite="Effectif de %s.";' % (self.echelle2))
        exo.append(r'pen p1=lightred,p2=1bp+black;')
        exo.append(u'string libellecaractere="Valeurs du caractère";')
        exo.append(r'real minaxe=%s;' % self.classes[0])
        exo.append(r'real maxaxe=%s;' % sum(self.classes))
        exo.append(r'real uniteaxe=%s;' % self.echelle1)
        exo.append(r'real largeurunite=abs(tabxi[1]-tabxi[0]);')
        exo.append(r'int iclasse=0;')
        exo.append(r'real[] tabhi;')
        exo.append(r'for(int i=0; i < tabni.length; ++i){')
        exo.append(r'tabhi[i]=tabni[i]/(tabxi[i+1]-tabxi[i]);')
        exo.append(r'if (largeurunite>abs(tabxi[i+1]-tabxi[i])) {')
        exo.append(r'largeurunite=abs(tabxi[i+1]-tabxi[i]);')
        exo.append(r'iclasse=i;')
        exo.append(r'}')
        exo.append(r'}')
        exo.append(r'real hauteurmaxi=max(tabhi);')
        exo.append(r'real hauteurunite=(uniteaire/tabni[iclasse])*tabhi[iclasse];')
        exo.append(r'histogram(tabxi,tabhi,low=0,bars=true,p1,p2);')
        exo.append(r'filldraw(box((%s,hauteurmaxi+.5hauteurunite),(%s+largeurunite,hauteurmaxi+1.5hauteurunite)),p1,p2);' % (self.classes[0], self.classes[0]))
        exo.append(r'xaxis(libellecaractere, Bottom, minaxe,maxaxe,')
        exo.append(r'RightTicks(Label(currentpen+fontsize(6)), new real[]{%s}),above=false);' % (",".join([str(self.classes[0] + k * self.echelle1) for k in range(sum(self.classes) // self.echelle1 + 1)])))
        exo.append(r'for(int k=0; k<(2*hauteurmaxi/hauteurunite+4); ++k){')
        exo.append(r'draw((minaxe,.5k*hauteurunite)--(maxaxe,.5k*hauteurunite),.5bp+gray);')
        exo.append(r'}')
        exo.append(r'for(int k=0; k<=((maxaxe-minaxe)/uniteaxe); ++k){')
        exo.append(r'draw((minaxe+k*uniteaxe,0)--(minaxe+k*uniteaxe,hauteurmaxi+1.5hauteurunite),.5bp+gray);')
        exo.append(r'}')
        exo.append(r'label(libelleunite,(%s+largeurunite,hauteurmaxi+hauteurunite),align=E,Fill(white));' % (self.classes[0]))
        exo.append(r'histogram(tabxi,tabhi,low=0,bars=true,p1+opacity(0),p2);')
        exo.append(r'\end{asy}')
        exo.append(r'\end{center}')
        return "\n".join(exo)
