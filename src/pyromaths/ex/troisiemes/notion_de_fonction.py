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
'''
Créé le 9 déc. 2013

.. sectionauthor:: Jérôme Ortais <jerome.ortais@pyromaths.org>
'''
from random import shuffle, randrange
if __name__ == '__main__':
    pass

def choix_points(min=-4, max=4, nb=5):
    """**choix_points**\ ()

    Renvoie un tuple contenant nb coordonnées sous forme de tuple telles que
    les abscisses et ordonnées sont distinctes, comprises entre min et max,
    une abscisse n'est jamais égale à une ordonnée et la coordonnée (b, a) n'est
    pas listée si la coordonnée (a, b) existe.

    >>> from pyromaths.ex.troisiemes import notion_de_fonction
    >>> notion_de_fonction.choix_points()  # doctest: +SKIP
    ((-4, -2), (-2, 0), (0, 4), (2, -4), (4, 2))

    :rtype: tuple

    """
    if nb > max - min + 1:
        raise ValueError('On demande trop de points vu le min et le max')
    abscisse = [i for i in range(min, max + 1)]
    for dummy in range(max - min - nb):
        del abscisse[randrange(len(abscisse))]
    refaire = True
    while refaire:
        ordonnee = [abscisse[i] for i in range(nb)]
        shuffle(ordonnee)
        refaire = False
        for i in range(nb):
            if abscisse[i] == ordonnee[i] or abscisse.index(ordonnee[i]) == ordonnee.index(abscisse[i]):
                refaire = True
                break
    return tuple([(abscisse[i], ordonnee[i]) for i in range(nb)])

def Lagrange(points):
    """**Lagrange**\ (*points*)
    Renvoie le polynôme d'interpolation de Lagrange pour les points de coordonnées *points*

    Est prévue pour être utilisé avec :py:func:`choix_points`

    Associé à  :py:func:`pyromaths.outils.Priorites3.priorites`, permet d'obtenir sa version réduite.

    Associé à  :py:func:`pyromaths.outils.Priorites3.plotify`, permet d'obtenir sa version utilisable avec psplot.

    >>> from pyromaths.ex.troisiemes import notion_de_fonction
    >>> p = notion_de_fonction.Lagrange(((-4, -2), (-2, 0), (0,4), (2,-4), (4,2)))

    >>> from pyromaths.outils import Priorites3
    >>> Priorites3.priorites(p)[-1]
    ['Polynome([[Fraction(5, 48), 4], [Fraction(1, 8), 3], [Fraction(-23, 12), 2], [Fraction(-3, 2), 1], [Fraction(4, 1), 0]], "x", 0)']
    >>> Priorites3.plotify(Priorites3.priorites(p)[-1])
    '5/48*x^4+1/8*x^3-23/12*x^2-3/2*x^1+4/1'
    """
    PIL = []
    for i in range(len(points)):
        if points[i][1]:
            PIL.append('Fraction(%s, ' % points[i][1])
            produit = []
            for j in  range(len(points)):
                if j != i: produit.append(repr(points[i][0] - points[j][0]))
            produit = repr(eval("*".join(produit)))
            PIL[i] += produit + ")*"
            produit = []
            for j in  range(len(points)):
                if j != i and points[j][0] > 0: produit.append("Polynome(\"x-%s\", details = 0)" % points[j][0])
                elif j != i and points[j][0] < 0: produit.append("Polynome(\"x+%s\", details = 0)" % -points[j][0])
                elif j != i and points[j][0] == 0: produit.append("Polynome(\"x\", details = 0)")
            produit = "*".join(produit)
            PIL[i] += produit
        else:
            PIL.append('0')
    return "+".join(PIL)

def creer_fonction(degre):
    """Crée une fonction polynôme de degré donné

    >>> notion_de_fonction.creer_fonction(2) # doctest: +SKIP
    'Polynome([[7, 2], [-1, 1], [-3, 0]], "x", details=0)'
    """
    p = []
    for exp in range(degre + 1):
        p.insert(0, [randrange(1, 10) * (-1) ** (randrange(3)), exp])
    return 'Polynome(%s, "x", details=0)' % p


def corrige(nom, fct, ant):
    from pyromaths.outils import Priorites3
    sol = []
    calc = fct(ant)
    res = Priorites3.priorites(calc)
    res = Priorites3.texify(res)
    sol.append(r"\par $%s\,(%s)=%s$\par" % (nom, ant, Priorites3.texify([Priorites3.splitting(calc)])[0]))
    sol.append('\\par\n'.join(['$%s\\,(%s)=%s$' % (nom, ant, res[j]) for j in range(len(res) - 1)]))
    sol.append(r'\par')
    sol.append('\\fbox{$%s\\,(%s)=%s$}\\\\\n' % (nom, ant, res[-1]))
    return sol

def notion_fonction():
    """Créé un exercice bilan sur la notion de fonction"""
    from pyromaths.classes.PolynomesCollege import Polynome
    from pyromaths.outils import Priorites3
    fct = [eval(creer_fonction(1)), eval(creer_fonction(2))]
    ant = [randrange(1, 6) * (-1) ** fct[0].degre(), randrange(1, 6) * (-1) ** fct[1].degre(), randrange(1, 6) * (-1) ** fct[1].degre(), randrange(1, 6) * (-1) ** fct[0].degre()]
    shuffle(fct)
    val_exo2 = choix_points(nb=7)
    exo = [r"\exercice", r"\begin{multicols}{2}", r"\begin{enumerate}", u"\\item On donne"]
    exo.append(r"$\begin{array}[t]{l}")
    exo.append(u"f:~x \\longmapsto %s \\\\ g:~x \\longmapsto %s" % (fct[0], fct[1]))
    exo.extend([r"\end{array}$", r"\begin{enumerate}", ])
    exo.append(u"\\item Quelle est l'image de $%s$ par la fonction $f$ ?" % ant[0])
    cor = [r"\exercice", r"\begin{multicols}{2}", r"\begin{enumerate}", u"\\item On donne"]
    cor.append(r"$\begin{array}[t]{l}")
    cor.append(u"f:~x \\longmapsto %s \\\\ g:~x \\longmapsto %s" % (fct[0], fct[1]))
    cor.extend([r"\end{array}$", r"\begin{enumerate}", ])
    cor.append(u"\\item Quelle est l'image de $%s$ par la fonction $f$ ?" % ant[0])
    cor.extend(corrige('f', fct[0], ant[0]))
    exo.append(u"\\item Quelle est l'image de $%s$ par la fonction $g$ ?" % ant[1])
    cor.append(u"\\item Quelle est l'image de $%s$ par la fonction $g$ ?" % ant[1])
    cor.extend(corrige('g', fct[1], ant[1]))
    exo.append(u"\\item Calculer $f\\,(%s)$." % ant[2])
    cor.append(u"\\item Calculer $f\\,(%s)$." % ant[2])
    cor.extend(corrige('f', fct[0], ant[2]))
    exo.append(u"\\item Calculer $g\\,(%s)$." % ant[3])
    cor.append(u"\\item Calculer $g\\,(%s)$." % ant[3])
    cor.extend(corrige('g', fct[1], ant[3]))
    exo.append(r"\end{enumerate}")
    cor.append(r"\end{enumerate}")
    exo.append(u"\\item Voici un tableau de valeurs correspondant à une fonction $h$.\\par")
    exo.append(r"\renewcommand{\arraystretch}{1.5}")
    exo.append(r"\begin{tabularx}{\linewidth}[t]{|c|*7{>{\centering}X|}}")
    exo.append(r"\hline")
    exo.append(r"$x$ & %s \tabularnewline \hline" % " & ".join(["$%s$" % c[0] for c in val_exo2]))
    exo.append(r"$h\,(x)$ & %s \tabularnewline \hline" % " & ".join(["$%s$" % c[1] for c in val_exo2]))
    exo.append(r"\end{tabularx} \medskip")
    exo.append(r"\begin{enumerate}")
    cor.append(u"\\item Voici un tableau de valeurs correspondant à une fonction $h$.\\par")
    cor.append(r"\renewcommand{\arraystretch}{1.5}")
    cor.append(r"\begin{tabularx}{\linewidth}[t]{|c|*7{>{\centering}X|}}")
    cor.append(r"\hline")
    cor.append(r"$x$ & %s \tabularnewline \hline" % " & ".join(["$%s$" % c[0] for c in val_exo2]))
    cor.append(r"$h\,(x)$ & %s \tabularnewline \hline" % " & ".join(["$%s$" % c[1] for c in val_exo2]))
    cor.append(r"\end{tabularx} \medskip")
    cor.append(r"\begin{enumerate}")
    lpos21 = [i for i in range(7)]
    for dummy in range(3):
        del lpos21[randrange(len(lpos21))]
    shuffle(lpos21)
    lquest = [u"Quelle est l'image de $%s$ par la fonction $h$ ?" % val_exo2[lpos21[0]][0],
              u"Quel est l'antécédent de $%s$ par la fonction $h$ ?" % val_exo2[lpos21[1]][1],
              u"Compléter : $h\\,(%s)=\\ldots\\ldots$" % val_exo2[lpos21[2]][0],
              u"Compléter : $h\\,(\\ldots\\ldots)=%s$" % val_exo2[lpos21[3]][1]]
    lpos22 = [0, 1, 2, 3]
    shuffle(lpos22)
    for i in range(4):
        exo.append(u"\\item %s" % lquest[lpos22[i]])
        if lpos22[i] == 0:
            cor.append(u"\\item L'image de $%s$ par la fonction $h$ est $\\mathbf{%s}$." % (val_exo2[lpos21[0]][0], val_exo2[lpos21[0]][1]))
        elif lpos22[i] == 1:
            cor.append(u"\\item Un antécédent de $%s$ par la fonction $h$ est $\\mathbf{%s}$." % (val_exo2[lpos21[1]][1], val_exo2[lpos21[1]][0]))
        if lpos22[i] == 2:
            cor.append(u"\\item $h\\,(%s)=\\mathbf{%s}$." % (val_exo2[lpos21[2]][0], val_exo2[lpos21[2]][1]))
        elif lpos22[i] == 1:
            cor.append(u"\\item $h\\,(\\mathbf{%s})=%s$." % (val_exo2[lpos21[3]][0], val_exo2[lpos21[3]][1]))

    exo.extend([r"\end{enumerate}", r"\columnbreak"])
    cor.append(r"\end{enumerate}")
    val_exo3 = choix_points()
    p = Priorites3.plotify(Priorites3.priorites(Lagrange(val_exo3))[-1])
    exo.extend([u"\\item Le graphique ci-dessous représente une fonction $k$ : \\par", r"\begin{center}",
                r"\psset{unit=8mm, algebraic, dotsize=4pt 4}", r"\begin{pspicture*}(-4.2,-4.2)(4.2,4.2)"])
    exo.append(r"\psgrid[subgriddiv=2, gridwidth=.6pt,subgridcolor=lightgray, gridlabels=0pt]")
    exo.append(r"\psaxes[linewidth=1.2pt,]{->}(0,0)(-4.2,-4.2)(4.2,4.2)")
    exo.append(r"\psplot[plotpoints=200, linewidth=1.5pt, linecolor=DarkRed]{-4.2}{4.2}{%s}" % p)
    exo.append(r"\psdots %s" % " ".join([str(val) for val in val_exo3]))
    exo.extend([r"\end{pspicture*}", r"\end{center}", r"\begin{enumerate}"])
    cor.extend([u"\\item Le graphique ci-après représente une fonction $k$ : \\par", r"\begin{center}",
                r"\psset{unit=8mm, algebraic, dotsize=4pt 4}", r"\begin{pspicture*}(-4.2,-4.2)(4.2,4.2)"])
    cor.append(r"\psgrid[subgriddiv=2, gridwidth=.6pt,subgridcolor=lightgray, gridlabels=0pt]")
    cor.append(r"\psaxes[linewidth=1.2pt,]{->}(0,0)(-4.2,-4.2)(4.2,4.2)")
    cor.append(r"\psplot[plotpoints=200, linewidth=1.5pt, linecolor=DarkRed]{-4.2}{4.2}{%s}" % p)
    cor.append(r"\psdots %s" % " ".join([str(val) for val in val_exo3]))
    lpos31 = [i for i in range(5)]
    for dummy in range(1):
        del lpos31[randrange(len(lpos31))]
    for i in range(4):
        cor.append(r"\psline[linestyle=dashed, linecolor=DarkRed](0, %s)(%s, %s)(%s, 0)" % (val_exo3[lpos31[i]][1], val_exo3[lpos31[i]][0], val_exo3[lpos31[i]][1], val_exo3[lpos31[i]][0]))
    cor.extend([r"\end{pspicture*}", r"\end{center}", r"\begin{enumerate}"])
    shuffle(lpos31)
    lquest = [u"Quelle est l'image de $%s$ par la fonction $k$ ?" % val_exo3[lpos31[0]][0],
              u"Donner un antécédent de %s par la fonction $k$." % val_exo3[lpos31[1]][1],
              u"Compléter : $k\\,(%s)=\\ldots\\ldots$" % val_exo3[lpos31[2]][0],
              u"Compléter : $k\\,(\\ldots\\ldots)=%s$" % val_exo3[lpos31[3]][1]]
    lpos32 = [0, 1, 2, 3]
    shuffle(lpos32)
    for i in range(4):
        exo.append(u"\\item %s" % lquest[lpos32[i]])
        if lpos32[i] == 0:
            cor.append(u"\\item L'image de $%s$ par la fonction $k$ est $\\mathbf{%s}$." % (val_exo3[lpos31[0]][0], val_exo3[lpos31[0]][1]))
        elif lpos32[i] == 1:
            cor.append(u"\\item Un antécédent de $%s$ par la fonction $k$ est $\\mathbf{%s}$." % (val_exo3[lpos31[1]][1], val_exo3[lpos31[1]][0]))
        if lpos32[i] == 2:
            cor.append(u"\\item $h\\,(%s)=\\mathbf{%s}$." % (val_exo3[lpos31[2]][0], val_exo3[lpos31[2]][1]))
        elif lpos32[i] == 1:
            cor.append(u"\\item $h\\,(\\mathbf{%s})=%s$." % (val_exo3[lpos31[3]][0], val_exo3[lpos31[3]][1]))
    exo.append(r"\end{enumerate}")
    cor.append(r"\end{enumerate}")



    exo.append(r"\end{enumerate}")
    exo.append(r"\end{multicols}")
    cor.append(r"\end{enumerate}")
    cor.append(r"\end{multicols}")

    return exo, cor
notion_fonction.description = u'Bilan sur la notion de fonction'

