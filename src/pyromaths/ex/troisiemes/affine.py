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

# fonction affine 3e
# from math import *
from math import sqrt
from pyromaths.classes.Fractions import Fraction  # fractions pyromaths
from pyromaths.classes.PolynomesCollege import Polynome
from pyromaths.outils.Affichage import decimaux
import random
import pyromaths.outils.Priorites3
from pyromaths.outils import Priorites3


def extreme(a, b, xmin, xmax, ymin, ymax):
# donne les extremités de la droite passant par a et b (coordonnées)
    res = []
    x1 = float(a[0])
    x2 = float(b[0])
    y1 = float(a[1])
    y2 = float(b[1])
    coef = float((y1 - y2) / (x1 - x2))
    if coef != 0:
        xsort1 = float(x1 + (ymin - y1) / coef)  # abscisse du point d'ordonnée ymin
        if xsort1 >= xmin and xsort1 <= xmax and not(xsort1, ymin) in res:
            res.append((xsort1, ymin))
        xsort2 = float(x2 + (ymax - y2) / coef)  # abscisse du point d'ordonnée ymax
        if xsort2 >= xmin and xsort2 <= xmax and not(xsort2, ymax) in res:
            res.append((xsort2, ymax))
        ysort1 = float(y1 + coef * (xmin - x1))  # ordonnée du point d'abscisse xmin
        if ysort1 >= ymin and ysort1 <= ymax and not (xmin, ysort1)in res:
            res.append((xmin, ysort1))
        ysort2 = float(y2 + coef * (xmax - x2))  # ordonnée du point d'abscisse xmax
        if ysort2 >= ymin and ysort2 <= ymax and not(xmax, ysort2) in res:
            res.append((xmax, ysort2))
    else:
        res = [(xmin, y1), (xmax, y1)]
    return res

def vecdir(A, B):
    # retourne sous forme de liste le vecteur directeur normé de la droite (AB)
    norm = sqrt((B[0] - A[0]) ** 2 + (B[1] - A[1]) ** 2)
    u = [(B[0] - A[0]) / norm, (B[1] - A[1]) / norm]
    if u[0] < 0:
        u[0] = -u[0]
        u[1] = -u[1]
    return u

def validedroite(A, B):
    # valide le choix du couple A B pour qu'ils ne soient pas "collés",
    # la droite (AB) ne sera ni horizontale ni verticale

    rep = True
    if abs(A[0] - B[0]) <= 1 and abs(A[1] - B[1]) <= 1:
        rep = False
    if A[0] == B[0] or A[1] == B[1]:
        rep = False
    if abs(A[0] - B[0]) < 1 or abs(A[1] - B[1]) < 1:
        rep = False
    return rep


def validec(A, B):
    # valide le choix du couple A B pour qu'ils ne soient pas "collés"
    rep = True
    if abs(A[0] - B[0]) <= 1 and abs(A[1] - B[1]) <= 1:
        rep = False
    return rep

def doublefleche(A, B):
    # trace une flèche "double" de justification en pointillés
    mid = (float((A[0] + B[0])) / 2, float((A[1] + B[1])) / 2)
    res1 = "\\psline[linestyle=dashed,linewidth=1.1pt]{->}" + str(A) + str(mid) + '\n '
    res2 = "\\psline[linestyle=dashed,linewidth=1.1pt]{->}" + str(mid) + str(B)
    res = res1 + res2
    if A == B:
        res = ""

    return res

def couple () :
    A = (float(random.randrange(-8, 9)) / 2, float(random.randrange(-8, 9)) / 2)
    B = (float(random.randrange(-8, 9)) / 2, float(random.randrange(-8, 9)) / 2)
    while not validec(A, B):
        B = (float(random.randrange(-8, 9)) / 2, float(random.randrange(-8, 9)) / 2)
    return (A, B)

def coupletrace () :
    A = (0, float(random.randrange(-4, 5)))
    B = (float(random.randrange(-4, 5)), float(random.randrange(-4, 5)))
    while not validec(A, B):
        B = (float(random.randrange(-4, 5)), float(random.randrange(-4, 5)))
    return (A, B)

def couples ():
    # génère 6 points. Chaque couple correspondra a une droite ( (AB)(CD)(EF)).
    A = (float(random.randrange(-8, 9)) / 2, float(random.randrange(-8, 9)) / 2)
    B = (float(random.randrange(-8, 9)) / 2, float(random.randrange(-8, 9)) / 2)
    while not validedroite(A, B):
        B = (float(random.randrange(-8, 9)) / 2, float(random.randrange(-8, 9)) / 2)
    C = (0, float(random.randrange(-4, 5)))
    while not (validec(A, C) and validec(B, C)):
        C = (0, float(random.randrange(-4, 5)))
    D = (float(random.randrange(-4, 5)), float(random.randrange(-4, 5)))
    while not (validec(A, D) and validec(B, D) and validedroite(C, D)) :
        D = (float(random.randrange(-4, 5)), float(random.randrange(-4, 5)))
    E = (0, float(random.randrange(-8, 9)) / 2)
    while not (validec(A, E) and validec(B, E) and validec(C, E) and validec(D, E)):
        E = (0, float(random.randrange(-8, 9)) / 2)
    F = (float(random.randrange(-4, 5)), float(random.randrange(-4, 5)))
    while not (validec(A, F) and validec(B, F) and validec(C, F) and validec(D, F)and validedroite(E, F)):
        F = (float(random.randrange(-4, 5)), float(random.randrange(-4, 5)))
    return (A, B, C, D, E, F)

def tracedroite(A, B, xmin, xmax, ymin, ymax):
    # trace la droite (AB)
    l = extreme(A, B, xmin, xmax, ymin, ymax)
    return "\\psline " + str(l[0]) + str(l[1])

def dansrep(A, xmin, xmax, ymin, ymax):
# Si le points est dans le repère
    res = False
    if A[0] > xmin and A[0] < xmax and A[1] > ymin and A[1] < ymax:
        res = True
    return res

def nomdroite(i, coordo):
    # place le nom de la droite (d_i) sur le graphique aux coordonnées coordo
    x0 = coordo[0]
    y0 = coordo[1]
    if x0 != 0:
        x = x0 / abs(x0) * (abs(x0) + 0.5)
    else:
        x = 0
    if y0 != 0:
        y = y0 / abs(y0) * (abs(y0) + 0.5)
    else:
        y = 0
    return "\\rput" + str((x, y)) + "{($d_" + str(i) + "$)}"

def nom3droites(A, B, C, D, E, F, xmin, xmax, ymin, ymax):
    # place le nom des droites (AB), (CD), (EF) dans le graphique
    # les 3 instructions latex sont contenues dans une liste
    # évite la juxtaposition des écritures
    res = []
    l1 = extreme(A, B, xmin, xmax, ymin, ymax)
    res.append(nomdroite(1, l1[0]))
    l2 = extreme(C, D, xmin, xmax, ymin, ymax)
    if validec(l1[0], l2[0]):
        memo = l2[0]  # se rappeler qu'on a utilisé l2[0]
        res.append(nomdroite(2, l2[0]))
    else:
        memo = l2[1]
        res.append(nomdroite(2, l2[1]))
    l3 = extreme(E, F, xmin, xmax, ymin, ymax)
    if validec(l1[0], l3[0]) and validec(memo, l3[0]):
        res.append(nomdroite(3, l3[0]))
    else :
        res.append(nomdroite(3, l3[1]))
    return res

def isint(x):
    # est entier?
    res = False
    if int(x) == x:
        res = True
    return res

def isdemi(x):
    # est-ce une moitié d'entier
    res = False
    x = float(x) * 2
    if isint(x):
        res = True

    return res

def coefdir(A, B):
    # donne le coefficient directeur x/y sous forme de liste [x,y]
    # Si y=1 on ecrira x sinon on écrira la fraction x/y
    return Fraction.simplifie(Fraction(B[1] - A[1], B[0] - A[0]))

def anteimage(fonc, A, B):
    # Génère la 1ère question et sa réponse

    l = [' l\'image de ', ' un nombre qui a pour image ', u' un antécédent de ']
    lcor = [' est l\'image de ', ' a pour image ', u' est un antécédent de ']  # liste pour le corrigé
    i = random.randrange(0, 2)
    j = i
    if i == 1:
        j = i + random.randrange(0, 2)
    res = []
    res.append('Donner ' + l[j] + '$' + decimaux(str(A[i])) + '$' + ' par la fonction ' + '\\textit{' + fonc + '}.')
    res.append('$' + decimaux(str(A[abs(i - 1)])) + '$' + lcor[j] + '$' + decimaux(str(A[i])) + '$' + ' par la \\hbox{fonction ' + '\\textit{' + fonc + '}}.')
    if i == 0:
        res.append(doublefleche((A[0], 0), A))
        res.append(doublefleche(A, (0, A[1])))

    else:
        res.append(doublefleche((0, A[1]), A))
        res.append(doublefleche(A, (A[0], 0)))
    i = abs(i - 1)
    j = i
    if i == 1:
        j = i + random.randrange(0, 2)
    res.append('Donner ' + l[j] + '$' + decimaux(str(B[i])) + '$' + ' par la fonction ' + '\\textit{' + fonc + '}.')
    res.append('$' + decimaux(str(B[abs(i - 1)])) + '$' + lcor[j] + '$' + decimaux(str(B[i])) + '$' + ' par la \\hbox{fonction ' + '\\textit{' + fonc + '}}.')
    if i == 0:
        res.append(doublefleche((B[0], 0), B))
        res.append(doublefleche(B, (0, B[1])))
    else:
        res.append(doublefleche((0, B[1]), B))
        res.append(doublefleche(B, (B[0], 0)))
    return res

def tracefonc(f, i, A, B, xmin, xmax, ymin, ymax):
    """**tracefonc\ (*f*\ , *i*\ , *A*\ , *B*\ , *xmin*\ , *xmax*\ , *ymin*\ , *ymax*\ )

        *A* est sur l'axe des ordonnées, *f* est le nom de la fonction
        Génère la 2e queston et sa réponse

        >>> from pyromaths.classes.Fractions import Fraction
        >>> affine.tracefonc('f', 1, (0,-2),(3,2),-4,4,-4,-4)
        [u'Tracer la droite repr\xe9sentative ($d_1$) de la fonction $f:x\\longmapsto \\
            dfrac{4}{3}\\,x-2$.', 'On sait que $f(0)=-2$ et $f(-3)=\\dfrac{4}{3}\\times \\le
            ft( -3\\right) -2=\\dfrac{4\\times \\cancel{3}\\times -1}{\\cancel{3}\\times 1}-
            2=-4-2=-6', '\\psdot [dotsize=4.5pt,dotstyle=x](0, -2)', '\\psdot [dotsize=4.5pt
            ,dotstyle=x](-3, -6.0)']

        :rtype: list of string
        """
    u = coefdir(A, B)  
    if u.d == 1:
        x1 = decimaux(B[0])
    else:
        B = (u.d, u.n + float(A[1]))
        if not dansrep(B, xmin, xmax, ymin, ymax):
            B = (-u.d, -u.n + float(A[1]))
        x1 = decimaux(str(B[0]))
    l = Priorites3.texify([Polynome.evaluate(Polynome([[u, 1],[A[1], 0]], "x"), B[0])])
    l.extend(Priorites3.texify(Priorites3.priorites(Polynome.evaluate(Polynome([[u, 1],[A[1], 0]], "x"), B[0]))))
    l = [u'Tracer la droite représentative ($d_' + str(i) + '$) de la fonction $' + f + ':x\\longmapsto ' + str(Polynome([[u,1],[A[1], 0]], "x")) + '$.',
       'On sait que $' + f + '(0)=' + decimaux(str(A[1])) + '$ et $' + f + '(' + x1 + ')=' + "=".join(l),
       '\\psdot [dotsize=4.5pt,dotstyle=x]' + str(A),
       '\\psdot [dotsize=4.5pt,dotstyle=x]' + str(B),
       ]
    return l

def exprfonc(f, i, A, B):
# Génère la 3e question.
# A est sur l'axe des ordonnées, f est le nom de la fonction
    u = coefdir(A, B)
    Polynome.evaluate(Polynome([[u, 1],[A[1], 0]], "x"), B[0])
    #===========================================================================
    # if A[1] >= 0:
    #     b = '+' + decimaux(str(A[1]))
    # else:
    #     b = decimaux(str(A[1]))
    # if u.d == 1:
    #     coef = decimaux(str(u.n))
    #     if u.n == -1:
    #         coef = '-'  # utilisé dans l'expression de la fonction
    #     if u.n == 1:
    #         coef = ''
    #     coefres = decimaux(str(u.n))  # résultat utilisé pour a
    # else:
    #     if u.n > 0:
    #         coef = '\\dfrac{' + decimaux(str(u.n)) + '}{' + decimaux(str(u.d)) + '}'
    #     else:
    #         coef = '-\\dfrac{' + decimaux(str(abs(u.n))) + '}{' + decimaux(str(u.d)) + '}'
    #     coefres = coef
    #===========================================================================
 
    if A[1] - B[1] > 0:
        deltay = '+' + decimaux(str(A[1] - B[1]))
    else :
        deltay = decimaux(str(A[1] - B[1]))
    if A[0] - B[0] > 0:
        deltax = '+' + decimaux(str(A[0] - B[0]))
    else:
        deltax = decimaux(str(A[0] - B[0]))

    if float(B[0]) < 0 :
        mid11 = float(B[0]) - 0.75
        mid12 = float((B[1] + A[1])) / 2  # milieu de la flèche verticale
    else:
        mid11 = float(B[0]) + 0.75
        mid12 = float((B[1] + A[1])) / 2
    if float(B[0]) * float(u.d / u.n) > 0 :
        mid21 = float((A[0] + B[0])) / 2
        mid22 = A[1] - 0.6  # milieu de la flèche horizontale
    else :
        mid21 = float((A[0] + B[0])) / 2
        mid22 = A[1] + 0.5
    if mid12 < 0 and mid12 > -0.8:
        mid12 = -1
    if mid12 >= 0 and mid12 < 0.5:
        mid12 = 0.5
    if mid11 < 0 and mid11 > -0.8:
        mid11 = -1
    if mid11 >= 0 and mid11 < 0.5:
        mid11 = 0.5
    if mid21 < 0 and mid21 > -0.8:
        mid21 = -1
    if mid21 >= 0 and mid21 < 0.5:
        mid21 = 0.5
    if mid22 < 0 and mid22 > -0.8:
        mid22 = -1
    if mid22 >= 0 and mid22 < 0.5:
        mid22 = 0.5
    mid1 = (mid11, mid12)
    mid2 = (mid21, mid22)
    l = [u'Déterminer l\'expression de la fonction $' + f + u'$ représentée ci-contre par la droite ($d_' + str(i) + '$).',
       u'On lit l\'ordonnée à l\'origine et le coefficient de la fonction affine sur le graphique.\\\ ',
       '$' + f + '(x)=a\\,x+b$ ' + 'avec $b=' + decimaux(str(A[1])) + '$ et $a=' + '\\dfrac{' + deltay + '}{' + deltax + '}=' + str(u) + '$.\\\ ',
       'L\'expression de la fonction $' + f + '$ est $' + f + '(x)=' + str(Polynome([[u, 1],[A[1], 0]], "x")) + '$.',
       doublefleche(B, (B[0], A[1])),
       doublefleche((B[0], A[1]), A),
       '\\rput' + str(mid1) + '{(' + deltay + ')}',
       '\\rput' + str(mid2) + '{(' + deltax + ')}']

    return l


def affine():
    # Génère l'exercice
    xmin, xmax, ymin, ymax = -5, 5, -5, 5
    f = ['f', 'g', 'h', 'k', 'l', 'u']
    rgfonc1 = random.randrange(0, 6)
    fonc1 = f[rgfonc1]
    (A, B, C, D, E, F) = couples()
    l = anteimage(fonc1, A, B)  # lecture d'image d'antécédent
    fonc2 = f[(rgfonc1 + 1) % 6]
    l2 = tracefonc(fonc2, 2, C, D, xmin, xmax, ymin, ymax)  # représenter une fonction
    fonc3 = f[(rgfonc1 + 2) % 6]
    l3 = exprfonc(fonc3, 3, E, F)
    noms = nom3droites(A, B, C, D, E, F, xmin, xmax, ymin, ymax)
    exo = ["\\exercice", "\\parbox{0.5\\linewidth}{",
         u"($d_1$) est la droite représentative de la fonction $" + fonc1 + "$.",
         "\\begin{enumerate}",
         "\\item " + l[0],
         "\\item " + l[4],
         "\\item " + l2[0],
         "\\item " + l3[0],
         "\\end{enumerate}}\\hfill",
         "\\parbox{0.45\\linewidth}{",
         "\\psset{unit=0.8cm}",
         "\\begin{pspicture}" + str((xmin, ymin)) + str((xmax, ymax)),
         "\\psgrid[subgriddiv=2, gridlabels=8pt](0,0)" + str((xmin, ymin)) + str((xmax, ymax)),
         "\\psline[linewidth=1.2pt]{->}" + str((xmin, 0)) + str((xmax, 0)),
         "\\psline[linewidth=1.2pt]{->}" + str((0, ymin)) + str((0, ymax)),
         tracedroite(A, B, xmin, xmax, ymin, ymax),
         noms[0],
         tracedroite(E, F, xmin, xmax, ymin, ymax),
         noms[2],
         "\\end{pspicture}}"]

    cor = ["\\exercice*", "\\setlength{\\columnsep}{2mm}",
         "\\begin{multicols}{2}\\noindent \\small",
         u"($d_1$) est la droite représentative de la fonction $" + fonc1 + "$.",
         "\\begin{enumerate}",
         "\\item " + l[1],
         "\\item " + l[5],
         "\\item\n\\begin{flushleft}\n" + l2[1] + "\n\\end{flushleft}",
         "\\item\n\\begin{flushleft}\n" + l3[1],
         l3[2],
         l3[3] + "\n\\end{flushleft}",
         "\\end{enumerate}",
         "\\end{multicols}",
         "\\vspace{0.45cm}",
         "\\begin{minipage}{0.5\\linewidth}",
         "\\psset{unit=0.7cm}",
         "\\begin{center}",
         "\\begin{pspicture}" + str((xmin, ymin)) + str((xmax, ymax)),
         "\\psgrid[subgriddiv=2, gridlabels=8pt](0,0)" + str((xmin, ymin)) + str((xmax, ymax)),
         "\\psline[linewidth=1.2pt]{->}" + str((xmin, 0)) + str((xmax, 0)),
         "\\psline[linewidth=1.2pt]{->}" + str((0, ymin)) + str((0, ymax)),
         tracedroite(A, B, xmin, xmax, ymin, ymax),
         noms[0],
         tracedroite(C, D, xmin, xmax, ymin, ymax),
         noms[1],
         l[2],
         l[3],
         l[6],
         l[7],
         l2[2],
         l2[3],
         "\\end{pspicture}",
         "\\end{center}",
         "\\end{minipage}",
         "\\begin{minipage}{0.5\\linewidth}",
         "\\psset{unit=0.7cm}",
         "\\begin{center}",
         "\\begin{pspicture}" + str((xmin, ymin)) + str((xmax, ymax)),
         "\\psgrid[subgriddiv=2, gridlabels=8pt](0,0)" + str((xmin, ymin)) + str((xmax, ymax)),
         "\\psline[linewidth=1.2pt]{->}" + str((xmin, 0)) + str((xmax, 0)),
         "\\psline[linewidth=1.2pt]{->}" + str((0, ymin)) + str((0, ymax)),
         tracedroite(E, F, xmin, xmax, ymin, ymax),
         noms[2],
         l3[4],
         l3[5],
         l3[6],
         l3[7],
         "\\end{pspicture}",
         "\\end{center}",
         "\\end{minipage}",
         "\\vspace{0.45cm}"]
    return exo, cor

affine.description = u'Fonctions affines'
