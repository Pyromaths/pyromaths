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
# along with this program; if notPopen, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301 USA

from __future__ import unicode_literals
from builtins import str
from builtins import chr
from builtins import range
import random
# from pyromaths.outils.Affichage import decimaux
from pyromaths.ex import LegacyExercise

def noms_sommets(nb):
    """Renvoie nb noms de sommets"""

    (listenb, listepts) = ([], [])
    for i in range(26):
        listenb.append(i + 65)
    for i in range(nb):
        listepts.append(str(chr(listenb.pop(random.randrange(26 - i)))))
    listepts.sort()
    return listepts

def connect(pt, F1, F2):
    """renvoie les sommets connectes à pt"""
    if pt in F1:
        result = [F1[F1.index(pt) - 1], F1[(F1.index(pt) + 1) % len(F1)], F2[F1.index(pt)]]
    else:
        result = [F2[F2.index(pt) - 1], F2[(F2.index(pt) + 1) % len(F2)], F1[F2.index(pt)]]
    return result


def reponse1(pt, F1, F2):
    """renvoie la réponse à la première question"""
    conn = connect(pt, F1, F2)
    ptc1 = conn[random.randrange(0, len(conn))]
    conn.remove(ptc1)
    ptc2 = conn[random.randrange(0, len(conn))]
    conn.remove(ptc2)
    ptc3 = conn[0]
    F3 = [F2[0], F1[0], F1[3], F2[3]]
    F4 = [F2[0], F2[1], F1[1], F1[0]]
    F5 = [F1[1], F2[1], F2[2], F1[2]]
    F6 = [F1[2], F2[2], F2[3], F1[3]]
    F2b = F2[:]
    F2b.reverse()
    if (pt in F1) and (ptc1 in F1) and (ptc2 in F1):
        i = F1.index(pt)
        j = F2.index(ptc3)
        res = [pt, F1[(i + 1) % 4], F1[(i + 2) % 4], F1[(i + 3) % 4], ptc3, F2[(j + 1) % 4], F2[(j + 2) % 4], F2[(j + 3) % 4]]
    elif (pt in F2) and (ptc1 in F2) and (ptc2 in F2):
        i = F2b.index(pt)
        j = F1.index(ptc3)
        res = [pt, F2b[(i + 1) % 4], F2b[(i + 2) % 4], F2b[(i + 3) % 4], ptc3, F1[(j - 1) % 4], F1[(j - 2) % 4], F1[(j - 3) % 4]]
    elif (pt in F3) and (ptc1 in F3) and (ptc2 in F3):
        i = F3.index(pt)
        j = F5.index(ptc3)
        res = [pt, F3[(i + 1) % 4], F3[(i + 2) % 4], F3[(i + 3) % 4], ptc3, F5[(j - 1) % 4], F5[(j - 2) % 4], F5[(j - 3) % 4]]
    elif (pt in F4) and (ptc1 in F4) and (ptc2 in F4):
        i = F4.index(pt)
        j = F6.index(ptc3)
        res = [pt, F4[(i + 1) % 4], F4[(i + 2) % 4], F4[(i + 3) % 4], ptc3, F6[(j - 1) % 4], F6[(j - 2) % 4], F6[(j - 3) % 4]]
    elif (pt in F5) and (ptc1 in F5) and (ptc2 in F5):
        i = F5.index(pt)
        j = F3.index(ptc3)
        res = [pt, F5[(i + 1) % 4], F5[(i + 2) % 4], F5[(i + 3) % 4], ptc3, F3[(j - 1) % 4], F3[(j - 2) % 4], F3[(j - 3) % 4]]
    elif (pt in F6) and (ptc1 in F6) and (ptc2 in F6):
        i = F6.index(pt)
        j = F4.index(ptc3)
        res = [pt, F6[(i + 1) % 4], F6[(i + 2) % 4], F6[(i + 3) % 4], ptc3, F5[(j - 1) % 4], F5[(j - 2) % 4], F5[(j - 3) % 4]]
    return res




def reponse2(pt1, ptc1, F1, F2):
    """renvoie la réponse à la deuxième question et le segment[p1ptc1]"""
    rep = []
    connects = connect(pt1, F1, F2)
    for pt in connects:
        if pt != ptc1:
            rep.append('[' + pt1 + pt + ']')
    connects2 = connect(ptc1, F1, F2)
    for pt in connects2:
        if pt != pt1:
            rep.append('[' + ptc1 + pt + ']')
    rep.append('[' + pt1 + ptc1 + ']')
    return tuple(rep)
def reponse3(pt2, ptc2, F1, F2):
    """renvoie la réponse à la troisièmequestion et le segment[pt2ptc2]"""
    if (pt2 in F1) and (ptc2 in F1):
        copy = F1[:]
        i = F1.index(pt2)
        j = F1.index(ptc2)
        copy.remove(pt2)
        copy.remove(ptc2)
        k = F1.index(copy[0])
        l = F1.index(copy[1])
        rep = ('[' + F2[i] + F2[j] + ']', '[' + F1[k] + F1[l] + ']', '[' + F2[k] + F2[l] + ']', '[' + pt2 + ptc2 + ']')
    elif (pt2 in F2) and (ptc2 in F2):
        copy = F2[:]
        i = F2.index(pt2)
        j = F2.index(ptc2)
        copy.remove(pt2)
        copy.remove(ptc2)
        k = F2.index(copy[0])
        l = F2.index(copy[1])
        rep = ('[' + F1[i] + F1[j] + ']', '[' + F1[k] + F1[l] + ']', '[' + F2[k] + F2[l] + ']', '[' + pt2 + ptc2 + ']')
    else:
        if pt2 in F1:
            i = F1.index(pt2)
        else:
            i = F2.index(pt2)
        rep = ('[' + F1[(i + 1) % len(F1)] + F2[(i + 1) % len(F1)] + ']', '[' + F1[(i + 2) % len(F1)] + F2[(i + 2) % len(F1)] + ']', '[' + F1[(i + 3) % len(F1)] + F2[(i + 3) % len(F1)] + ']', '[' + pt2 + ptc2 + ']')

    return tuple(rep)

def _espace():
    """Face 1, Face 2"""
    noms_pts = (noms_sommets(8))
    F1 = noms_pts[0:4]
    F2 = noms_pts[4:8]
    pt = noms_pts[random.randrange(0, len(noms_pts))]
    rp1 = reponse1(pt, F1, F2)
    pt1 = noms_pts[random.randrange(0, len(noms_pts))]
    conn1 = connect(pt1, F1, F2)
    pt2 = noms_pts[random.randrange(0, len(noms_pts))]
    conn2 = connect(pt2, F1, F2)
    ptc1 = conn1[random.randrange(0, len(conn1))]
    ptc2 = conn2[random.randrange(0, len(conn2))]
    rp2 = u"%s, %s, %s et %s sont les arêtes perpendiculaires à %s." % reponse2(pt1, ptc1, F1, F2)
    rp3 = u"%s, %s et %s sont les arêtes parallèles à %s." % reponse3(pt2, ptc2, F1, F2)
    exo = ["\\exercice",
         u"Les figures 1 et 2 représentent le même cube %s%s%s%s%s%s%s%s.\\\ " % tuple(noms_pts),
         "\\psset{xunit=1.0cm,yunit=1.0cm,dotstyle=*,dotsize=3pt 0,linewidth=0.8pt,arrowsize=3pt 2,arrowinset=0.25}",
         "\\begin{pspicture*}(-2,-0.38)(15,4.5)",
         "\\psframe[fillstyle=solid,fillcolor=darkgray,framearc=0.2](-1,3.5)(-0.5,4)",
         "\\rput[bl](-0.85,3.65){\\white{\\textbf{$1$}}}",
         "\\psline[linestyle=dashed,linecolor=Maroon,dash=4pt 4pt](3.5,1)(1.5,1)",
         "\\psline[linestyle=dashed,linecolor=Maroon,dash=4pt 4pt](1.5,1)(1.5,3)",
         "\\psline[linestyle=dashed,linecolor=Maroon,dash=4pt 4pt](1.5,1)(0.5,0)",
         "\\psframe[linecolor=Maroon](0.5,0)(2.5,2)",
         "\\psline[linecolor=Maroon](1.5,3)(3.5,3)",
         "\\psline[linecolor=Maroon](3.5,3)(3.5,1)",
         "\\psline[linecolor=Maroon](0.5,2)(1.5,3)",
         "\\psline[linecolor=Maroon](2.5,2)(3.5,3)",
         "\\psline[linecolor=Maroon](2.5,0)(3.5,1)",
         "\\rput[bl](0.22,2.08){%s}" % F1[0],
         "\\rput[bl](2.28,2.16){%s}" % F1[1],
         "\\rput[bl](2.6,-0.22){%s}" % F1[2],
         "\\rput[bl](0.15,-0.22){%s}" % F1[3],
         "\\rput[bl](1.4,3.08){%s}" % F2[0],
         "\\rput[bl](3.58,3.04){%s}" % F2[1],
         "\\rput[bl](3.58,1.04){%s}" % F2[2],
         "\\rput[bl](1.58,1.04){%s}" % F2[3],
         "\\psline[linecolor=Maroon](5.2,-04)(5.2,4)",
         "\\psframe[fillstyle=solid,fillcolor=darkgray,framearc=0.2](5.7,3.5)(6.2,4)",
         "\\rput[bl](5.85,3.65){\\white{\\textbf{$2$}}}",
         "\\psline[linecolor=Maroon](8.48,2.71)(7.18,2.42)",
         "\\psline[linecolor=Maroon](7.18,2.42)(7.18,0.46)",
         "\\psline[linestyle=dashed, linecolor=Maroon, dash=4pt 4pt](7.18,0.46)(8.48,0.75)",
         "\\psline[linestyle=dashed, linecolor=Maroon, dash=4pt 4pt](8.48,0.75)(8.48,2.71)",
         "\psline[linecolor=Maroon](10,2.46)(8.7,2.17)",
         "\\psline[linecolor=Maroon](8.7,2.17)(8.7,0.21)",
         "\\psline[linecolor=Maroon](8.7,0.21)(10,0.5)",
         "\\psline[linecolor=Maroon](10,0.5)(10,2.46)",
         "\\psline[linecolor=Maroon](10,2.46)(8.48,2.71)",
         "\\psline[linecolor=Maroon](7.18,2.42)(8.7,2.17)",
         "\\psline[linecolor=Maroon](8.7,0.21)(7.18,0.46)",
         "\\psline[linestyle=dashed,dash=4pt 4pt, linecolor=Maroon](10,0.5)(8.48,0.75)",
         "\\rput[bl](8.68,2.27){%s}" % rp1[0],
         "\\rput[bl](10.06,2.5){%s}" % rp1[1],
         "\\rput[bl](8.71,-0.1){%s}" % rp1[3],
         "\\end{pspicture*}",
         "\\begin{enumerate}",
         u"\\item Compléter les sommets manquants de la figure 2.",
         u"\\item Donner toutes les arêtes perpendiculaires à [%s%s]." % (pt1, ptc1),
         u"\\item Donner toutes les arêtes parallèles à [%s%s]." % (pt2, ptc2),
         "\\end{enumerate}"]
    cor = ["\\exercice*",
         u"Les figures 1 et 2 représentent le même cube %s%s%s%s%s%s%s%s.\\\ " % tuple(noms_pts),
         "\\psset{xunit=1.0cm,yunit=1.0cm,dotstyle=*,dotsize=3pt 0,linewidth=0.8pt,arrowsize=3pt 2,arrowinset=0.25}",
         "\\begin{pspicture*}(-2,-0.38)(15,4.5)",
         "\\psframe[fillstyle=solid,fillcolor=darkgray,framearc=0.2](-1,3.5)(-0.5,4)",
         "\\rput[bl](-0.85,3.65){\\white{\\textbf{$1$}}}",
         "\\psline[linestyle=dashed,linecolor=Maroon,dash=4pt 4pt](3.5,1)(1.5,1)",
         "\\psline[linestyle=dashed,linecolor=Maroon,dash=4pt 4pt](1.5,1)(1.5,3)",
         "\\psline[linestyle=dashed,linecolor=Maroon,dash=4pt 4pt](1.5,1)(0.5,0)",
         "\\psframe[linecolor=Maroon](0.5,0)(2.5,2)",
         "\\psline[linecolor=Maroon](1.5,3)(3.5,3)",
         "\\psline[linecolor=Maroon](3.5,3)(3.5,1)",
         "\\psline[linecolor=Maroon](0.5,2)(1.5,3)",
         "\\psline[linecolor=Maroon](2.5,2)(3.5,3)",
         "\\psline[linecolor=Maroon](2.5,0)(3.5,1)",
         "\\rput[bl](0.22,2.08){%s}" % F1[0],
         "\\rput[bl](2.28,2.16){%s}" % F1[1],
         "\\rput[bl](2.6,-0.22){%s}" % F1[2],
         "\\rput[bl](0.15,-0.22){%s}" % F1[3],
         "\\rput[bl](1.4,3.08){%s}" % F2[0],
         "\\rput[bl](3.58,3.04){%s}" % F2[1],
         "\\rput[bl](3.58,1.04){%s}" % F2[2],
         "\\rput[bl](1.58,1.04){%s}" % F2[3],
         "\\psline[linecolor=Maroon](5.2,-04)(5.2,4)",
         "\\psframe[fillstyle=solid,fillcolor=darkgray,framearc=0.2](5.7,3.5)(6.2,4)",
         "\\rput[bl](5.85,3.65){\\white{\\textbf{$2$}}}",
         "\\psline[linecolor=Maroon](8.48,2.71)(7.18,2.42)",
         "\\psline[linecolor=Maroon](7.18,2.42)(7.18,0.46)",
         "\\psline[linestyle=dashed,dash=4pt 4pt, linecolor=Maroon](7.18,0.46)(8.48,0.75)",
         "\\psline[linestyle=dashed,dash=4pt 4pt, linecolor=Maroon](8.48,0.75)(8.48,2.71)",
         "\psline[linecolor=Maroon](10,2.46)(8.7,2.17)",
         "\\psline[linecolor=Maroon](8.7,2.17)(8.7,0.21)",
         "\\psline[linecolor=Maroon](8.7,0.21)(10,0.5)",
         "\\psline[linecolor=Maroon](10,0.5)(10,2.46)",
         "\\psline[linecolor=Maroon](10,2.46)(8.48,2.71)",
         "\\psline[linecolor=Maroon](7.18,2.42)(8.7,2.17)",
         "\\psline[linecolor=Maroon](8.7,0.21)(7.18,0.46)",
         "\\psline[linestyle=dashed,dash=4pt 4pt, linecolor=Maroon](10,0.5)(8.48,0.75)",
         "\\rput[bl](10.05,0.2){%s}" % rp1[2],
         "\\rput[bl](8.71,-0.1){%s}" % rp1[3],
         "\\rput[bl](8.1,0.79){%s}" % rp1[6],
         "\\rput[bl](6.8,0.2){%s}" % rp1[7],
         "\\rput[bl](10.06,2.5){%s}" % rp1[1],
         "\\rput[bl](8.68,2.27){%s}" % rp1[0],
         "\\rput[bl](7.08,2.54){%s}" % rp1[4],
         "\\rput[bl](8.5,2.83){%s}" % rp1[5],
         "\\end{pspicture*}",
         "\\begin{enumerate}",
         u"\\item Compléter les sommets manquants de la figure 2.",
         u"\\item Donner toutes les arêtes perpendiculaires à [%s%s].\\par " % (pt1, ptc1),
         rp2,
         u"\\item Donner toutes les arêtes parallèles à [%s%s]. \\par " % (pt2, ptc2),
         rp3,
         "\\end{enumerate}"]
    return (exo, cor)

class espace(LegacyExercise):
    """Représentation dans l\'espace"""

    tags = ["Sixième"]
    function = _espace
