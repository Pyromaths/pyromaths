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

import math
from random import randrange
from ..outils import Arithmetique
from ..outils import Geometrie


def eq_droites(A, B):
    (xA, yA) = A
    (xB, yB) = B
    a = ((yB - yA) * 1.0) / (xB - xA)
    b = ((xB * yA - xA * yB) * 1.0) / (xB - xA)
    return (a, b)


def inter_droites(A, B, C, D):
    """
    Calcule les coordonn\xc3\xa9es du point d'intersection des droites (AB) et (CD)
    """

    (a1, b1) = eq_droites(A, B)
    (a2, b2) = eq_droites(C, D)
    if a1 == a2:  #droites parallèles
        xI = A[0]
        yI = A[1]
    else:
        xI = ((b2 - b1) * 1.0) / (a1 - a2)
        yI = ((a1 * b2 - a2 * b1) * 1.0) / (a1 - a2)
    return (xI, yI)


def dist_pt_droite(A, B, C):
    """
    calcule la distance du point C \xc3\xa0 la droite (AB)
    """

    (a, b) = eq_droites(A, B)
    (xC, yC) = C
    d = (abs(a * xC - yC + b) * 1.0) / math.sqrt(a ** 2 + 1)
    return d


def dist_points(A, B):
    """ Calcul la distance entre deux points"""

    (xA, yA) = A
    (xB, yB) = B
    d = math.sqrt((xB - xA) ** 2 + (yB - yA) ** 2)
    return d


def coord_projete(A, B, C):
    """
    Calcule les coordonn\xc3\xa9es du projet\xc3\xa9 orthogonal de C sur la droite (AB)
    """

    (xA, yA) = A
    (xB, yB) = B
    (xC, yC) = C
    n = dist_points(A, B)
    p = (xB - xA) / n
    q = (yB - yA) / n
    s = p * (xC - xA) + q * (yC - yA)
    return (xA + s * p, yA + s * q)


def verifie_distance_mini(A, B, C, D):
    """
    V\xc3\xa9rifie que la distance minimale entre [AB] et [AC] est sup\xc3\xa9rieure \xc3\xa0 dmin
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
    (xI, yI) = inter_droites(A, B, C, D)
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
    V\xc3\xa9rifie que l'angle BAC ne coupe pas les autres angles d\xc3\xa9j\xc3\xa0 trac\xc3\xa9s
    """

    if len(lpoints) == 0:  #Premier angle créé
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
    cr\xc3\xa9e une s\xc3\xa9rie d\'angles "non s\xc3\xa9quents"
    '''

    (xmax, ymax) = (xmax - .5, ymax - .5)  #taille de l'image en cm
    lg_seg = 6  #longueur des côtés des angles
    lpoints = []
    cpt = 0  #evite une boucle infinie
    while len(lpoints) < nb_angles and cpt < 1000:
        (xA, yA) = (randrange(5, xmax * 10) / 10.0, randrange(5, ymax *
                    10) / 10.0)
        alpha = randrange(360)  #angle entre un côté et l'horizontal
        if len(lpoints) < nb_angles / 2:
            beta = randrange(90, 180)  #crée un angle droit ou obtus
        else:
            beta = randrange(0, 75) + 15  #crée un angle aigu (entre 15° et 89°)
        xB = xA + lg_seg * math.cos((alpha * math.pi) / 180)
        yB = yA + lg_seg * math.sin((alpha * math.pi) / 180)
        xC = xA + lg_seg * math.cos(((alpha + beta) * math.pi) / 180)
        yC = yA + lg_seg * math.sin(((alpha + beta) * math.pi) / 180)
        (A, B, C) = ((xA, yA), (xB, yB), (xC, yC))
        if xA != xB and xA != xC and .5 < xB < xmax and .5 < yB < ymax and \
            .5 < xC < xmax and .5 < yC < ymax and verifie_angle(lpoints,
                A, B, C):
            lpoints.append((A, B, C, alpha, beta))
        else:
            cpt = cpt + 1

    #print len(lpoints)

    return lpoints


def PosAngle(alpha, beta):
    """retourne les angles pour placer les points sur la figure"""

    A = (alpha + beta / 2.0 + 180) % 360
    B = (alpha - 90) % 360
    C = (alpha + beta + 90) % 360
    return (A, B, C)


def PointName(l3noms, indice):
    list = []
    for i in range(3):
        list.append(l3noms[i])
    return tuple(list)


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
        exo.append("\\pstMarkAngle{a%s%s}{a%s%s}{a%s%s}{}"%(1,i,0,i,2,i))
        cor.append("\\pstMarkAngle{a%s%s}{a%s%s}{a%s%s}{}"%(1,i,0,i,2,i))
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
            cor.append(_("angle aigu\\par"))
        elif lpoints[i][4] > 90:
            cor.append(_("angle obtus\\par"))
        else:
            cor.append(_("angle droit\\par"))
    cor.append("\\end{multicols}")
    exo.append("\\begin{tabularx}{\\textwidth}{|*{4}{X|}}")
    exo.append(_("\\hline angle 1 : & angle 2 : & angle 3 : & angle 4 : \\\\"))
    exo.append("\\hline &&& \\\\ &&& \\\\ &&& \\\\ \\hline")
    exo.append("\\end{tabularx}")


def MesureAngles():
    nb_angles = 4
    (xmax, ymax) = (18, 8)  #taille de l'image en cm
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
    exo = ["\\exercice", _("Nommer, mesurer et donner la nature de chacun des angles suivants :\\par ")]
    cor = ["\\exercice*", _("Nommer, mesurer et donner la nature de chacun des angles suivants :\\par ")]
    figure(exo, cor, lpoints, lnoms, xmax, ymax)
    reponses(exo, cor, lpoints, lnoms)
    return (exo, cor)
