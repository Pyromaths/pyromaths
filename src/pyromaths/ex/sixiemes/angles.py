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

from __future__ import division
from __future__ import unicode_literals
from builtins import chr
from builtins import range
from past.utils import old_div
import math
from random import randrange
from pyromaths.outils import Geometrie
from pyromaths import ex


def eq_droites(A, B):
    (xA, yA) = A
    (xB, yB) = B
    a = old_div(((yB - yA) * 1.0), (xB - xA))
    b = old_div(((xB * yA - xA * yB) * 1.0), (xB - xA))
    return (a, b)


def inter_droites(A, B, C, D):
    """
    Calcule les coordonnées du point d'intersection des droites (AB) et (CD)
    """

    (a1, b1) = eq_droites(A, B)
    (a2, b2) = eq_droites(C, D)
    if a1 == a2:  # droites parallèles
        xI = A[0]
        yI = A[1]
    else:
        xI = old_div(((b2 - b1) * 1.0), (a1 - a2))
        yI = old_div(((a1 * b2 - a2 * b1) * 1.0), (a1 - a2))
    return (xI, yI)


def dist_pt_droite(A, B, C):
    """
    calcule la distance du point C à la droite (AB)
    """

    (a, b) = eq_droites(A, B)
    (xC, yC) = C
    d = old_div((abs(a * xC - yC + b) * 1.0), math.sqrt(a ** 2 + 1))
    return d


def dist_points(A, B):
    """ Calcul la distance entre deux points"""

    (xA, yA) = A
    (xB, yB) = B
    d = math.sqrt((xB - xA) ** 2 + (yB - yA) ** 2)
    return d


def coord_projete(A, B, C):
    """
    Calcule les coordonnées du projeté orthogonal de C sur la droite (AB)
    """

    (xA, yA) = A
    (xB, yB) = B
    (xC, yC) = C
    n = dist_points(A, B)
    p = old_div((xB - xA), n)
    q = old_div((yB - yA), n)
    s = p * (xC - xA) + q * (yC - yA)
    return (xA + s * p, yA + s * q)


def verifie_distance_mini(A, B, C, D):
    """
    Vérifie que la distance minimale entre [AB] et [AC] est supérieure à dmin
    """

    dmin = 1.2
    (xA, yA) = A
    (xB, yB) = B
    if xA > xB:
        (xA, yA, xB, yB) = (xB, yB, xA, yA)
    (xC, yC) = C
    (xD, yD) = D
    if xC > xD:
        (xC, yC, xD, yD) = (xD, yD, xC, yC)
    (xI, dummy) = inter_droites(A, B, C, D)
    if xA <= xI <= xB and xC <= xI <= xD or xA <= coord_projete(A, B, C)[0] <= \
        xB and dist_pt_droite(A, B, C) < dmin or xA <= coord_projete(A,
            B, D)[0] <= xB and dist_pt_droite(A, B, D) < dmin or xC <= \
        coord_projete(C, D, A)[0] <= xD and dist_pt_droite(C, D, A) < \
        dmin or xC <= coord_projete(C, D, B)[0] <= xD and dist_pt_droite(C,
            D, B) < dmin or dist_points(A, C) < dmin or dist_points(A, D) < \
        dmin or dist_points(B, C) < dmin or dist_points(B, D) < dmin:
        isValid = False
    else:
        isValid = True
    return isValid


def verifie_angle(lpoints, A, B, C):
    """
    Vérifie que l'angle BAC ne coupe pas les autres angles déjà tracés
    """

    if len(lpoints) == 0:  # Premier angle créé
        isValid = True
    else:
        for i in range(len(lpoints)):
            (A1, B1, C1) = (lpoints[i])[:3]
            isValid = verifie_distance_mini(A, B, A1, B1) and \
                verifie_distance_mini(A, B, A1, C1) and \
                verifie_distance_mini(A, C, A1, B1) and \
                verifie_distance_mini(A, C, A1, C1)
            if not isValid:
                break
    return isValid


def cree_angles(nb_angles, xmax, ymax):
    '''
    crée une série d\'angles "non séquents"
    '''

    (xmax, ymax) = (xmax - .5, ymax - .5)  # taille de l'image en cm
    lg_seg = 6  # longueur des côtés des angles
    lpoints = []
    cpt = 0  # evite une boucle infinie
    while len(lpoints) < nb_angles and cpt < 1000:
        (xA, yA) = (old_div(randrange(5, xmax * 10), 10.0), old_div(randrange(5, ymax *
                    10), 10.0))
        alpha = randrange(360)  # angle entre un côté et l'horizontal
        if len(lpoints) < old_div(nb_angles, 2):
            beta = randrange(90, 180)  # crée un angle droit ou obtus
        else:
            beta = randrange(0, 75) + 15  # crée un angle aigu (entre 15° et 89°)
        xB = xA + lg_seg * math.cos(old_div((alpha * math.pi), 180))
        yB = yA + lg_seg * math.sin(old_div((alpha * math.pi), 180))
        xC = xA + lg_seg * math.cos(old_div(((alpha + beta) * math.pi), 180))
        yC = yA + lg_seg * math.sin(old_div(((alpha + beta) * math.pi), 180))
        (A, B, C) = ((xA, yA), (xB, yB), (xC, yC))
        if xA != xB and xA != xC and .5 < xB < xmax and .5 < yB < ymax and \
            .5 < xC < xmax and .5 < yC < ymax and verifie_angle(lpoints,
                A, B, C):
            lpoints.append((A, B, C, alpha, beta))
        else:
            cpt = cpt + 1

    # print len(lpoints)

    return lpoints


def PosAngle(alpha, beta):
    """retourne les angles pour placer les points sur la figure"""

    A = (alpha + old_div(beta, 2.0) + 180) % 360
    B = (alpha - 90) % 360
    C = (alpha + beta + 90) % 360
    return (A, B, C)


def PointName(l3noms, indice):
    liste = []
    for i in range(3):
        liste.append(l3noms[i])
    return tuple(liste)


def figure(exo, cor, lpoints, lnoms, xmax, ymax):
    exo.append("\\begin{pspicture}(%s,%s)" % (xmax, ymax))
    exo.append("\\psframe(0,0)(%s,%s)" % (xmax, ymax))
    exo.append("\\psset{PointSymbol=none,MarkAngleRadius=0.6}")
    cor.append("\\begin{pspicture}(%s,%s)" % (xmax, ymax))
    cor.append("\\psset{PointSymbol=none,MarkAngleRadius=0.6}")
    cor.append("\\psframe(0,0)(%s,%s)" % (xmax, ymax))
    for i in range(len(lnoms)):
        points_exo = ''
        points_cor = ''
        points_exo += "\\pstGeonode[PointName={%s,%s,%s}," % lnoms[i]
        points_cor += "\\pstGeonode[PointName={%s,%s,%s}," % lnoms[i]
        points_exo += "PosAngle={%s,%s,%s}]" % PosAngle(lpoints[i][3], lpoints[i][4])
        points_cor += "PosAngle={%s,%s,%s}]" % PosAngle(lpoints[i][3], lpoints[i][4])
        for j in range(3):
            points_exo += "(%.2f,%.2f)" % lpoints[i][j]
            points_exo += "{a%s%s}" % (j, i)
            points_cor += "(%.2f,%.2f)" % lpoints[i][j]
            points_cor += "{a%s%s}" % (j, i)
        exo.append(points_exo)
        cor.append(points_cor)
        exo.append("\\pstMarkAngle{a%s%s}{a%s%s}{a%s%s}{}" % (1, i, 0, i, 2, i))
        cor.append("\\pstMarkAngle{a%s%s}{a%s%s}{a%s%s}{}" % (1, i, 0, i, 2, i))
        exo.append("\\pstLineAB[nodesepB=-.5]{a0%s}{a1%s}\\pstLineAB[arrows=-|,linestyle=none]{a0%s}{a1%s}" % (i, i, i, i))
        cor.append("\\pstLineAB[nodesepB=-.5]{a0%s}{a1%s}\\pstLineAB[arrows=-|,linestyle=none]{a0%s}{a1%s}" % (i, i, i, i))
        exo.append("\\pstLineAB[nodesepB=-.5]{a0%s}{a2%s}\\pstLineAB[arrows=-|,linestyle=none]{a0%s}{a2%s}" % (i, i, i, i))
        cor.append("\\pstLineAB[nodesepB=-.5]{a0%s}{a2%s}\\pstLineAB[arrows=-|,linestyle=none]{a0%s}{a2%s}" % (i, i, i, i))
    exo.append("\\end{pspicture}\\par")
    cor.append("\\end{pspicture}\\par")
    return (exo, cor)


def reponses(exo, cor, lpoints, lnoms):
    cor.append("\\begin{multicols}{4}")
    for i in range(len(lnoms)):
        cor.append("$\\widehat{%s%s%s}=%s\degres$\\par" % (lnoms[i][1],
                 lnoms[i][0], lnoms[i][2], lpoints[i][4]))
        if lpoints[i][4] < 90:
            cor.append("angle aigu\\par")
        elif lpoints[i][4] > 90:
            cor.append("angle obtus\\par")
        else:
            cor.append("angle droit\\par")
    cor.append("\\end{multicols}")
    exo.append("\\begin{tabularx}{\\textwidth}{|*{4}{X|}}")
    exo.append("\\hline angle 1 : & angle 2 : & angle 3 : & angle 4 : \\\\")
    exo.append("\\hline &&& \\\\ &&& \\\\ &&& \\\\ \\hline")
    exo.append("\\end{tabularx}")


def MesureAngles():
    nb_angles = 4
    (xmax, ymax) = (18, 8)  # taille de l'image en cm
    lnoms = []
    lpoints = []
    cpt = 0
    while len(lpoints) < nb_angles:
        if cpt > 1000:
            lpoints = []
            cpt = 0
        lpoints = cree_angles(nb_angles, xmax, ymax)
        cpt = cpt + 1
    tmpl = Geometrie.choix_points(3 * nb_angles)
    for i in range(nb_angles):
        lnoms.append(tuple(tmpl[3 * i:3 * i + 3]))
    exo = ["\\exercice", "Nommer, mesurer et donner la nature de chacun des angles suivants :\\par "]
    cor = ["\\exercice*", "Nommer, mesurer et donner la nature de chacun des angles suivants :\\par "]
    figure(exo, cor, lpoints, lnoms, xmax, ymax)
    reponses(exo, cor, lpoints, lnoms)
    return (exo, cor)

MesureAngles.description = u'Mesurer des angles'

class ConstruireZigZag(ex.TexExercise):

    description = u'Construire des angles'

    def __init__(self):
        """ Crée une liste de nbp points situés à la distance lg les uns des
        autres"""
        from pyromaths.outils.Conversions import radians
        from math import sin, cos
        self.lg, nbp = 4, 6
        fini = False
        while not fini:
            ar = randrange(80, 91)
            angles_relatifs = [ar]
            angles_absolus = [ar]
            ar = radians(ar)
            points = [(.2, .2), (.2 + self.lg * cos(ar), .2 + self.lg * sin(ar))]
            for i in range(nbp - 1):
                point = (-1, -1)
                cpt = 0  # évite les boucles infinies
                while (not point[0] < 16.2 or not 0.2 < point[1] < self.lg + 1) and cpt < 100:
                    if i % 2:
                        aa = randrange(angles_absolus[-1], 80)
                    else:
                        aa = randrange(-80, angles_absolus[-1])
                    ar = 180 - abs(aa - angles_absolus[-1])
                    aar = radians(aa)
                    point = (points[-1][0] + self.lg * cos(aar), points[-1][1] + self.lg * sin(aar))
                    cpt += 1
                if cpt == 100:
                    break
                else:
                    points.append(point)
                    angles_absolus.append(aa)
                    angles_relatifs.append(ar)
            if cpt < 100: fini = True
        self.points, self.angles_relatifs, self.angles_absolus = points, angles_relatifs, angles_absolus

    def tex_place_les_points_zigzag(self, corrige=False):
        exo = "\\pstGeonode[PosAngle=%.2f, PointSymbol=x](%.2f, %.2f){%s} " % \
                (self.angles_absolus[0] - 180, self.points[0][0], self.points[0][1], chr(65))
        if not corrige:
            exo += "\\pstGeonode[PosAngle=%.2f, PointSymbol=x](%.2f, %.2f){B} " % \
                (self.angles_absolus[1] + old_div(self.angles_relatifs[1], 2.) - 180, self.points[1][0], self.points[1][1])
            exo += "\pstSegmentMark{A}{B}\n"
        x1, y1 = inter_droites(self.points[0], self.points[-1], self.points[1], self.points[-2])
        if 0 < x1 < 18 and 0 < y1 < self.lg + 2:
            cas = 0
        else:
            x1, y1 = inter_droites(self.points[0], self.points[-2], self.points[1], self.points[-1])
            cas = 1
        for i in range(1, 5):
            exo += "\pscircle[linecolor=Gray](%.2f, %.2f){%.1f}\n" % (x1, y1, old_div(i, 10.))
        if corrige:
            for i in range(1, len(self.angles_relatifs)):
                if self.angles_absolus[i - 1] > self.angles_absolus[i]:
                    exo += "\\pstGeonode[PosAngle=%.2f](%.2f, %.2f){%s} " % \
                            (self.angles_absolus[i] - old_div(self.angles_relatifs[i], 2.) - 180, self.points[i][0], self.points[i][1], chr(i + 65))
                else:
                    exo += "\\pstGeonode[PosAngle=%.2f](%.2f, %.2f){%s} " % \
                            (self.angles_absolus[i] + old_div(self.angles_relatifs[i], 2.) - 180, self.points[i][0], self.points[i][1], chr(i + 65))

                exo += "\pstSegmentMark{%s}{%s}\n" % (chr(i + 64), chr(i + 65))
            exo += "\\pstGeonode[PosAngle=%.2f, PointSymbol=x](%.2f, %.2f){%s} " % \
                    (self.angles_absolus[-1], self.points[-1][0], self.points[-1][1], chr(len(self.points) + 64))
            exo += "\pstSegmentMark{%s}{%s}\n" % (chr(len(self.points) + 63), chr(len(self.points) + 64))
            for i in range(len(self.angles_relatifs) - 1):
                if self.angles_absolus[i] > self.angles_absolus[i + 1]:
                    if self.angles_relatifs[i + 1] == 90:
                        exo += "\\pstRightAngle{%s}{%s}{%s}\n" % \
                                (chr(i + 65), chr(i + 66), chr(i + 67))
                    else:
                        exo += "\\pstMarkAngle{%s}{%s}{%s}{%s\\degres}\n" % \
                                (chr(i + 65), chr(i + 66), chr(i + 67), self.angles_relatifs[i + 1])
                else:
                    if self.angles_relatifs[i + 1] == 90:
                        exo += "\\pstRightAngle{%s}{%s}{%s}\n" % \
                                (chr(i + 67), chr(i + 66), chr(i + 65))
                    else:
                        exo += "\\pstMarkAngle{%s}{%s}{%s}{%s\\degres}\n" % \
                                (chr(i + 67), chr(i + 66), chr(i + 65), self.angles_relatifs[i + 1])
            if cas:
                exo += "\psline[linestyle=dotted](B)(G) "
                exo += "\psline[linestyle=dotted](A)(F)"
            else:
                exo += "\psline[linestyle=dotted](B)(F) "
                exo += "\psline[linestyle=dotted](A)(G)"
        return exo

    def tex_commun(self):
        exo = [u'Construire sur la figure ci-dessous les points $C$, $D$, $E$, $F$ et $G$ pour obtenir un zigzag tel que :\\par']
        exo_t = '$'
        for i in range(len(self.angles_relatifs) - 1):
            exo_t += r"\widehat{%s%s%s}=%s\degres \qquad " % (chr(i + 65), chr(i + 66), chr(i + 67), self.angles_relatifs[i + 1])
        exo_t += r'$\par'
        exo.append(exo_t)
        exo.append(u"Quand le travail est fait avec une bonne précision, les ")
        x1, y1 = inter_droites(self.points[0], self.points[-1], self.points[1], self.points[-2])
        if 0 < x1 < 18 and 0 < y1 < self.lg + 2:
            exo.append(u"droites $(AG)$ et $(BF)$ se coupent au c\\oe ur de la cible.\\par")
        else:
            exo.append(u"droites $(AF)$ et $(BG)$ se coupent au c\\oe ur de la cible.")
        exo.append(r'\begin{center}')
        exo.append("\\fbox{\n\\begin{pspicture}(-.4,-.4)(16.4, %s)\n" % (self.lg + 1.5))
        return exo


    def tex_statement(self):
        exo = [r'\exercice']
        exo.append(u'Voici deux exemples de zigzags :\par')
        exo.append(r'\psset{unit=3.5mm,PointSymbol=none}')
        exo.append(r'\begin{pspicture}(-.4,-1)(16.4, 7.5)')
        exo.append(r'%\psgrid')
        exo.append(r'\pstGeonode[PosAngle=-96.00,PointSymbol=x](0.20, 0.20){A}')
        exo.append(r'\pstGeonode[PosAngle=-265.00](0.83, 6.17){B} \pstSegmentMark{A}{B}')
        exo.append(r'\pstGeonode[PosAngle=-87.50](2.48, 0.40){C} \pstSegmentMark{B}{C}')
        exo.append(r'\pstGeonode[PosAngle=-241.00](3.63, 6.29){D} \pstSegmentMark{C}{D}')
        exo.append(r'\pstGeonode[PosAngle=-90.00](9.23, 4.14){E} \pstSegmentMark{D}{E}')
        exo.append(r'\pstGeonode[PosAngle=-299.50](14.83, 6.29){F} \pstSegmentMark{E}{F}')
        exo.append(r'\pstGeonode[PosAngle=-80.00,PointSymbol=x](15.87, 0.38){G}')
        exo.append(r'\pstSegmentMark{F}{G}')
        exo.append(r'\pstMarkAngle[MarkAngleRadius=1.5]{A}{B}{C}{}')
        exo.append(r'\pstMarkAngle[MarkAngleRadius=1.5]{D}{C}{B}{}')
        exo.append(r'\pstMarkAngle[MarkAngleRadius=1.5]{C}{D}{E}{}')
        exo.append(r'\pstMarkAngle[MarkAngleRadius=1.5]{F}{E}{D}{}')
        exo.append(r'\pstMarkAngle[MarkAngleRadius=1.5]{E}{F}{G}{}')
        exo.append(r'\end{pspicture}')
        exo.append(r'\hspace{2cm}')
        exo.append(r'\begin{pspicture}(-.4,-1)(16.4, 7.5)')
        exo.append(r'\pstGeonode[PosAngle=-91.00,PointSymbol=x](0.20, 0.20){A}')
        exo.append(r'\pstGeonode[PosAngle=-263.50](0.30, 6.20){B} \pstSegmentMark{A}{B}')
        exo.append(r'\pstGeonode[PosAngle=-101.00](1.76, 0.38){C} \pstSegmentMark{B}{C}')
        exo.append(r'\pstGeonode[PosAngle=-259.00](5.28, 5.23){D} \pstSegmentMark{C}{D}')
        exo.append(r'\pstGeonode[PosAngle=-82.50](10.37, 2.05){E} \pstSegmentMark{D}{E}')
        exo.append(r'\pstGeonode[PosAngle=-286.00](14.46, 6.44){F} \pstSegmentMark{E}{F}')
        exo.append(r'\pstGeonode[PosAngle=-79.00,PointSymbol=x](15.61, 0.55){G}')
        exo.append(r'\pstSegmentMark{F}{G}')
        exo.append(r'\pstMarkAngle[MarkAngleRadius=1.5]{A}{B}{C}{}')
        exo.append(r'\pstMarkAngle[MarkAngleRadius=1.5]{D}{C}{B}{}')
        exo.append(r'\pstMarkAngle[MarkAngleRadius=1.5]{C}{D}{E}{}')
        exo.append(r'\pstMarkAngle[MarkAngleRadius=1.5]{F}{E}{D}{}')
        exo.append(r'\pstMarkAngle[MarkAngleRadius=1.5]{E}{F}{G}{}')
        exo.append(r'\end{pspicture}\par')
        exo.append(r'\psset{unit=1cm}')
        exo.extend(self.tex_commun())
        exo.append(self.tex_place_les_points_zigzag(corrige=False))
        exo.append(r'\end{pspicture}')
        exo.append('}\n\\end{center}')
        return exo

    def tex_answer(self):
        exo = [r'\exercice*']
        exo.extend(self.tex_commun())
        exo.append(self.tex_place_les_points_zigzag(corrige=True))
        exo.append(r'\end{pspicture}')
        exo.append('}\n\\end{center}')
        return exo

