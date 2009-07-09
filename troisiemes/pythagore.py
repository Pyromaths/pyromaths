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
import fractions
from math import acos, asin, atan, pi, sin, cos, tan
from outils import valeur_alea, pgcd, ecrit_tex

#
# ------------------- THEOREME DE PYTHAGORE -------------------

couples_pythagore = (
    (12, 16, 20),
    (15, 20, 25),
    (10, 24, 26),
    (20, 21, 29),
    (18, 24, 30),
    (16, 30, 34),
    (21, 28, 35),
    (12, 35, 37),
    (15, 36, 39),
    (24, 32, 40),
    (27, 36, 45),
    (14, 48, 50),
    (30, 40, 50),
    (24, 45, 51),
    (20, 48, 52),
    (28, 45, 53),
    (33, 44, 55),
    (40, 42, 58),
    (36, 48, 60),
    (11, 60, 61),
    (16, 63, 65),
    (25, 60, 65),
    (33, 56, 65),
    (39, 52, 65),
    (32, 60, 68),
    (42, 56, 70),
    (48, 55, 73),
    (24, 70, 74),
    (21, 72, 75),
    (45, 60, 75),
    (30, 72, 78),
    (48, 64, 80),
    (18, 80, 82),
    (13, 84, 85),
    (36, 77, 85),
    (40, 75, 85),
    (51, 68, 85),
    (60, 63, 87),
    (39, 80, 89),
    (54, 72, 90),
    (35, 84, 91),
    (57, 76, 95),
    (65, 72, 97),
    (28, 96, 100),
    (60, 80, 100),
    (20, 99, 101),
    (48, 90, 102),
    (40, 96, 104),
    (63, 84, 105),
    (56, 90, 106),
    (60, 91, 109),
    (66, 88, 110),
    (36, 105, 111),
    (15, 112, 113),
    (69, 92, 115),
    (80, 84, 116),
    (45, 108, 117),
    (56, 105, 119),
    (72, 96, 120),
    (22, 120, 122),
    (27, 120, 123),
    (35, 120, 125),
    (44, 117, 125),
    (75, 100, 125),
    (32, 126, 130),
    (50, 120, 130),
    (66, 112, 130),
    (78, 104, 130),
    (81, 108, 135),
    (64, 120, 136),
    (88, 105, 137),
    (84, 112, 140),
    (55, 132, 143),
    (17, 144, 145),
    (24, 143, 145),
    (87, 116, 145),
    (100, 105, 145),
    (96, 110, 146),
    (48, 140, 148),
    (51, 140, 149),
    (42, 144, 150),
    (90, 120, 150),
    (72, 135, 153),
    (93, 124, 155),
    (60, 144, 156),
    (85, 132, 157),
    (84, 135, 159),
    (96, 128, 160),
    (36, 160, 164),
    (99, 132, 165),
    (65, 156, 169),
    (119, 120, 169),
    (26, 168, 170),
    (72, 154, 170),
    (80, 150, 170),
    (102, 136, 170),
    (52, 165, 173),
    (120, 126, 174),
    (49, 168, 175),
    (105, 140, 175),
    (78, 160, 178),
    (108, 144, 180),
    (19, 180, 181),
    (70, 168, 182),
    (33, 180, 183),
    (57, 176, 185),
    (60, 175, 185),
    (104, 153, 185),
    (111, 148, 185),
    (88, 165, 187),
    (114, 152, 190),
    (95, 168, 193),
    (130, 144, 194),
    (48, 189, 195),
    (75, 180, 195),
    (99, 168, 195),
    (117, 156, 195),
    (28, 195, 197),
    (56, 192, 200),
    (120, 160, 200),
    )


def trouve_couples_pythagore(valeurmax):
    (liste, listecouples) = ([], [])
    for a in xrange(valeurmax):
        liste.append(a ** 2)
    for c in xrange(valeurmax):
        for b in xrange(int((c + 1) / 2 ** .5)):
            if liste.count((c + 1) ** 2 - (b + 1) ** 2):
                a = liste.index((c + 1) ** 2 - (b + 1) ** 2)
                listeinter = [c + 1, b + 1, a]
                listeinter.sort()
                if listeinter[0] > 9:
                    listecouples.append(tuple(listeinter))

#                if listecouples==[] :
#                   listecouples.append(tuple(listeinter))
#                else :
#                    ajout=1
#                    for i in xrange(len(listecouples)) :
#                        if not(listeinter[2]%listecouples[i][2]) and not(listeinter[1]%listecouples[i][1]) and not(listeinter[0]%listecouples[i][0]) :
#                            if listeinter[2]//listecouples[i][2]==listeinter[1]//listecouples[i][1]==listeinter[0]//listecouples[i][0] : ajout=0
#                    if ajout :
#                        listeinter=[c+1,b+1,a]
#                        listeinter.sort()
#                        listecouples.append(tuple(listeinter))

    return tuple(listecouples)


def noms_sommets(nb):  # renvoie nb noms de sommets
    (listenb, listepts) = ([], [])
    for i in xrange(26):
        listenb.append(i + 65)
    for i in xrange(nb):
        listepts.append(unichr(listenb.pop(random.randrange(26 - i))))
    listepts.sort()
    return tuple(listepts)


def fig_tr_rect(lg):  # renvoie les angles au centre des trois sommets du triangle ABC rectange en C
    a = random.randrange(360)
    if a < 180:
        b = a + 180
    else:
        b = a - 180
    c = (int((180 - ((2 * acos((lg[1] * 1.0) / lg[2])) * 180) / pi) *
         100) * 1.0) / 100 + a
    if c < 0:
        c = c + 360
    return (str(a), str(b), str(c))


def enonce_pythagore(noms, angles, longueurs, cotes, nom_tr, long0,
                     long1, diam=0):
    if diam:
        return (
            noms[0],
            angles[0],
            angles[0],
            noms[1],
            angles[1],
            angles[1],
            noms[2],
            angles[2],
            angles[2],
            int(float(angles[0]) - 90),
            cotes[2],
            noms[2],
            cotes[long0],
            nombre(longueurs[long0]),
            cotes[long1],
            nombre(longueurs[long1]),
            cotes[(3 - long0) - long1],
            )
    else:
        return (
            noms[0],
            angles[0],
            angles[0],
            noms[1],
            angles[1],
            angles[1],
            noms[2],
            angles[2],
            angles[2],
            nom_tr,
            noms[2],
            cotes[long0],
            nombre(longueurs[long0]),
            cotes[long1],
            nombre(longueurs[long1]),
            cotes[(3 - long0) - long1],
            )


def tex_pythagore(f0, f1, noms, angles, longueurs):
    nom_tr = nom_triangle(noms)
    long0 = random.randrange(3)
    long1 = (random.randrange(2) + 1 + long0) % 3
    cotes = cotes_sommets(noms)
    enonce = \
        '''  \\begin{minipage}{4cm}
    \\begin{pspicture}(-2,-2)(2,2)
      \\SpecialCoor\\psset{PointSymbol=x}
      \\pstGeonode[PointName=%s,PosAngle=%s](1.5;%s){a}\\pstGeonode[PointName=%s,PosAngle=%s](1.5;%s){b}\\pstGeonode[PointName=%s,PosAngle=%s](1.5;%s){c}
      \\pspolygon(a)(b)(c)
      \\pstRightAngle{b}{c}{a}
    \\end{pspicture}
  \\end{minipage}\\hfill
  \\begin{minipage}{13cm}
    Soit $%s$ un triangle rectangle en $%s$ tel que $%s=\\unit[%s]{cm}\\text{ et }%s=\\unit[%s]{cm}$.\\par
    Calculer la longueur $%s$.
''' % \
        enonce_pythagore(noms, angles, longueurs, cotes, nom_tr, long0,
                         long1)
    f0.write(enonce)
    f1.write(enonce)
    f1.write("    \\par\\dotfill{}\\\\\n\n")
    f1.write("    Le triangle %s est rectangle en %s donc, d'apr\\`es le \\textbf{th\\'eor\\`eme de Pythagore} :\n" %
             (nom_tr, noms[2]))
    f1.write("    \\[%s^2=%s^2+%s^2\\kern1cm\\text{(car }[%s]\\text{ est \\emph{l'hypot\\'enuse})}\\]\n" %
             (cotes[2], cotes[0], cotes[1], cotes[2]))
    if long0 == 2 or long1 == 2:
        f1.write("    \\[%s^2=%s^2-%s^2\\kern1cm\\text{(On cherche }%s)\\]\n" %
                 (cotes[(3 - long0) - long1], cotes[2], cotes[((4 -
                 long0) - long1) % 2], cotes[(3 - long0) - long1]))
    if long0 == 2 or long1 == 2:
        f1.write("    \\[%s^2=%s^2-%s^2\\]\n" % (cotes[(3 - long0) -
                 long1], nombre(longueurs[2]), nombre(longueurs[((4 -
                 long0) - long1) % 2])))
    else:
        f1.write("    \\[%s^2=%s^2+%s^2\\]\n" % (cotes[2], nombre(longueurs[0]),
                 nombre(longueurs[1])))
    if long0 == 2 or long1 == 2:
        f1.write("    \\[%s^2=%s-%s\\]\n" % (cotes[(3 - long0) - long1],
                 nombre(longueurs[2] ** 2), nombre(longueurs[((4 - long0) -
                 long1) % 2] ** 2)))
    else:
        f1.write("    \\[%s^2=%s+%s\\]\n" % (cotes[2], nombre(longueurs[0] **
                 2), nombre(longueurs[1] ** 2)))
    if long0 == 2 or long1 == 2:
        f1.write("    \\[%s^2=%s\\]\n" % (cotes[(3 - long0) - long1],
                 nombre(longueurs[2] ** 2 - longueurs[((4 - long0) -
                 long1) % 2] ** 2)))
    else:
        f1.write("    \\[%s^2=%s\\]\n" % (cotes[2], nombre(longueurs[0] **
                 2 + longueurs[1] ** 2)))
    if long0 == 2 or long1 == 2:
        f1.write("    \\[\\boxed{\\text{Donc }%s=\\sqrt{%s}=\\unit[%s]{cm}}\\]\n" %
                 (cotes[(3 - long0) - long1], nombre(longueurs[2] ** 2 -
                 longueurs[((4 - long0) - long1) % 2] ** 2), nombre(longueurs[(3 -
                 long0) - long1])))
    else:
        f1.write("    \\[\\boxed{\\text{Donc }%s=\\sqrt{%s}=\\unit[%s]{cm}}\\]\n" %
                 (cotes[2], nombre(longueurs[0] ** 2 + longueurs[1] ** 2),
                 nombre(longueurs[2])))
    f0.write('  \\end{minipage}\n')
    f1.write('  \\end{minipage}\n')


def nom_triangle(noms):  # renvoie le nom du triangle dans un ordre aleatoire
    a = random.randrange(3)
    b = (random.randrange(2) + 1 + a) % 3
    c = (3 - a) - b
    return '%s%s%s' % (noms[a], noms[b], noms[c])


def cotes_sommets(noms):  # renvoie les noms des 3 cotes du triangle en finissant par l'hypotenuse
    return (noms[1] + noms[2], noms[0] + noms[2], noms[0] + noms[1])


#
# ------------------- CERCLE ET THEOREME DE PYTHAGORE -------------------
#


def tex_triangle_cercle(f0, f1, noms, angles, longueurs):
    nom_tr = nom_triangle(noms)
    long0 = random.randrange(3)
    long1 = (random.randrange(2) + 1 + long0) % 3
    cotes = cotes_sommets(noms)
    enonce = \
        '''  \\begin{minipage}{4cm}
    \\begin{pspicture}(-2,-2)(2,2)
      \\SpecialCoor\\psset{PointSymbol=x}
      \\pstGeonode[PointName=%s,PosAngle=%s](1.5;%s){a}\\pstGeonode[PointName=%s,PosAngle=%s](1.5;%s){b}\\pstGeonode[PointName=%s,PosAngle=%s](1.5;%s){c}
      \\pspolygon(a)(b)(c)\\pscircle(0,0){1.5}\\rput(1.8;%s){$\\big(\\mathcal{C}\\big)$}
    \\end{pspicture}
  \\end{minipage}\\hfill
  \\begin{minipage}{13cm}
    $\\big(\\mathcal{C}\\big)$ est un cercle de diam\\`etre $[%s]$ et $%s$ est un 
    point de $\\big(\\mathcal{C}\\big)$.\\par
    On donne $%s=\\unit[%s]{cm}\\text{ et }%s=\\unit[%s]{cm}$.\\par
    Calculer la longueur $%s$.
''' % \
        enonce_pythagore(noms, angles, longueurs, cotes, nom_tr, long0,
                         long1, diam=1)
    f0.write(enonce)
    f1.write(enonce)
    f1.write("    \\par\\dotfill{}\\\\\n\n")
    f1.write("    $[%s]$ est le diam\`etre du cercle circonscrit au triangle $%s$.\\par\n" %
             (cotes[2], nom_tr))
    f1.write("    \\fbox{Donc le triangle %s est rectangle en %s.}\\\\\n\n" %
             (nom_tr, noms[2]))
    f1.write("    D'apr\\`es le \\textbf{th\\'eor\\`eme de Pythagore} :\n")
    f1.write("    \\[%s^2=%s^2+%s^2\\kern1cm\\text{(car }[%s]\\text{ est \\emph{l'hypot\\'enuse})}\\]\n" %
             (cotes[2], cotes[0], cotes[1], cotes[2]))
    if long0 == 2 or long1 == 2:
        f1.write("    \\[%s^2=%s^2-%s^2\\kern1cm\\text{(On cherche }%s)\\]\n" %
                 (cotes[(3 - long0) - long1], cotes[2], cotes[((4 -
                 long0) - long1) % 2], cotes[(3 - long0) - long1]))
    if long0 == 2 or long1 == 2:
        f1.write("    \\[%s^2=%s^2-%s^2\\]\n" % (cotes[(3 - long0) -
                 long1], nombre(longueurs[2]), nombre(longueurs[((4 -
                 long0) - long1) % 2])))
    else:
        f1.write("    \\[%s^2=%s^2+%s^2\\]\n" % (cotes[2], nombre(longueurs[0]),
                 nombre(longueurs[1])))
    if long0 == 2 or long1 == 2:
        f1.write("    \\[%s^2=%s-%s\\]\n" % (cotes[(3 - long0) - long1],
                 nombre(longueurs[2] ** 2), nombre(longueurs[((4 - long0) -
                 long1) % 2] ** 2)))
    else:
        f1.write("    \\[%s^2=%s+%s\\]\n" % (cotes[2], nombre(longueurs[0] **
                 2), nombre(longueurs[1] ** 2)))
    if long0 == 2 or long1 == 2:
        f1.write("    \\[%s^2=%s\\]\n" % (cotes[(3 - long0) - long1],
                 nombre(longueurs[2] ** 2 - longueurs[((4 - long0) -
                 long1) % 2] ** 2)))
    else:
        f1.write("    \\[%s^2=%s\\]\n" % (cotes[2], nombre(longueurs[0] **
                 2 + longueurs[1] ** 2)))
    if long0 == 2 or long1 == 2:
        f1.write("    \\[\\boxed{\\text{Donc }%s=\\sqrt{%s}=\\unit[%s]{cm}}\\]\n" %
                 (cotes[(3 - long0) - long1], nombre(longueurs[2] ** 2 -
                 longueurs[((4 - long0) - long1) % 2] ** 2), nombre(longueurs[(3 -
                 long0) - long1])))
    else:
        f1.write("    \\[\\boxed{\\text{Donc }%s=\\sqrt{%s}=\\unit[%s]{cm}}\\]\n" %
                 (cotes[2], nombre(longueurs[0] ** 2 + longueurs[1] ** 2),
                 nombre(longueurs[2])))
    f0.write('  \\end{minipage}\n')
    f1.write('  \\end{minipage}\n')


#
# ------------------- RECIPROQUE DU THEOREME DE PYTHAGORE -------------------
#


def tex_reciproque_pythagore(f0, f1, noms, longueurs):
    nom_tr = nom_triangle(noms)
    l = [i for i in xrange(3)]
    n = [l.pop(random.randrange(3 - i)) for i in xrange(3)]
    del l
    c = cotes_sommets(noms)
    recip = (nom_tr, c[n[0]], nombre(longueurs[n[0]]), c[n[1]], nombre(longueurs[n[1]]),
             c[n[2]], nombre(longueurs[n[2]]), nom_tr)
    enonce = \
        '''  Soit $%s$ un triangle tel que : $\\quad %s=\\unit[%s]{cm}\\quad$, $\\quad %s=\\unit[%s]{cm}\\quad$ et $\\quad %s=\\unit[%s]{cm}$.\\par
  Quelle est la nature du triangle $%s$?
''' % \
        recip
    f0.write(enonce)
    f1.write(enonce)
    f1.write("  \\par\\dotfill{}\\\\\n\n")
    f1.write("  Le triangle %s n'est ni isoc\\`ele, ni \\'equilat\\'eral.\\par\n" %
             nom_tr)
    f1.write('''  $\\left.
  \\renewcommand{\\arraystretch}{2}
  \\begin{array}{l}
''')
    f1.write("    \\bullet %s^2=%s^2=%s\\qquad\\text{(}[%s]\\text{ est le plus grand c\\^ot\\'e.)}\\\\\n" %
             (c[2], nombre(longueurs[2]), nombre(longueurs[2] ** 2), c[2]))
    f1.write("    \\bullet  %s^2+%s^2=%s^2+%s^2=%s \n" % (c[0], c[1],
             nombre(longueurs[0]), nombre(longueurs[1]), nombre(longueurs[0] **
             2 + longueurs[1] ** 2)))
    f1.write('  \\end{array}  \\right\\rbrace$\n')
    f1.write("""  Donc $%s^2=%s^2+%s^2$.\\par
  D'apr\\`es la \\textbf{r\\'eciproque du th\\'eor\\`eme de Pythagore}, \\fbox{le triangle $%s$ est rectangle en $%s$.}
""" %
             (c[2], c[0], c[1], nom_tr, noms[2]))


#
# ------------------- THEOREME DE THALES -------------------
#


def valeurs_thales(valeurmax):
    liste = [0, 0, 0, 0, 0, 0, 0, 0]
    while liste == [0, 0, 0, 0, 0, 0, 0, 0]:
        for i in xrange(3):
            liste[i] = random.randrange(2)
    a = random.randrange(liste.count(1))
    for i in xrange(3):
        if liste[i]:
            if not a:
                liste[i + 3] = 1
            a = a - 1
        else:
            liste[i + 3] = 1  # on doit connaitre le numeratuer ou le denominateur
    for i in xrange(2):  # AB et AE  ou  AB et BE  ou  AE et EB
        if liste[i] and liste[i + 3]:  # i est le rapport complet. On choisit une des 3 formes ci-dessus
            a = random.randrange(2)
            liste[i + 6] = 1
            liste[i + 3 * a] = 0
            rapport = [i + 3 * ((a + 1) % 3), i + 3 * ((a + 2) % 3)]
            rapport.sort()
    if liste[2] and liste[5]:
        rapport = [2, 5]
    valeurs = [0, 0, 0, 0, 0, 0, 0, 0]
    for i in xrange(3):
        if liste[i]:
            valeurs[i] = random.randrange(15, valeurmax) / 10.0
        if liste[i + 3] and liste[i]:
            valeurs[i + 3] = random.randrange(5, valeurs[i] * 10 - 9) / \
                10.0
        elif liste[i + 3]:
            valeurs[i + 3] = random.randrange(5, valeurmax) / 10.0
    if liste[6]:
        valeurs[6] = random.randrange(5, valeurmax) / 10.0
    if liste[7]:
        valeurs[7] = random.randrange(5, valeurmax) / 10.0

    #------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    type_thales = valeur_alea(-1, 1)  # -1 si papillon, 1 si triangle

    #type_thales=-1

    valeurs.append((rapport, type_thales))
    if test_valeurs_thales(valeurs, rapport, type_thales):
        return valeurs
    else:
        return 0


def test_valeurs_thales(valeurs, rapport, type_thales):
    v = [valeurs[i] for i in xrange(8)]
    if rapport[0] // 3 == 0 and rapport[1] // 3 == 2:  # On donne AB et EB
        v[rapport[0] + 3] = (v[rapport[0]] - v[rapport[1]]) * \
            type_thales
    elif rapport[0] // 3 == 1 and rapport[1] // 3 == 2:

                                                # On donne AE et EB

        v[rapport[0] - 3] = v[rapport[0]] * type_thales + v[rapport[1]]
    if v[rapport[0] % 3]:  # rapport est AE/AB
        rapp = (v[rapport[0] % 3 + 3] * 1.0) / v[rapport[0] % 3]
    else:
        rapp = 0
    for i in xrange(3):
        if not v[i] and rapp:
            v[i] = v[i + 3] / rapp
        elif not v[i + 3]:
            v[i + 3] = v[i] * rapp
    if inegalite_triangulaire(v[0:3]) and inegalite_triangulaire(v[3:6]) and \
        .3 < rapp < .7:
        return v
    else:
        return 0


def inegalite_triangulaire(a):  # renvoie 1 si c'est un triangle, 0 sinon
    vrai = 0
    coef = 1.2  # evite les triangles trop ecrases
    if a[0] > a[1] and a[0] > a[2]:
        if a[1] + a[2] > coef * a[0]:
            vrai = 1
    elif a[1] > a[0] and a[1] > a[2]:
        if a[0] + a[2] > coef * a[1]:
            vrai = 1
    elif a[2] > a[0] and a[2] > a[1]:
        if a[0] + a[1] > coef * a[2]:
            vrai = 1
    return vrai


def thales(f0, f1):
    noms = noms_sommets(5)  # les noms des sommets
    while True:
        valeurs = valeurs_thales(70)  # les longueurs en mm
        if valeurs:
            break
    f0.write(tex_fig_thales(noms, valeurs))
    f0.write(tex_enonce_thales(noms, valeurs) + '  \\vspace{2cm}\n')
    f1.write(tex_fig_thales(noms, valeurs))
    f1.write(tex_enonce_thales(noms, valeurs) +
             "  \\par\\dotfill{}\\\\\n\n")
    f1.write(tex_resolution_thales0(noms))
    f1.write(tex_resolution_thales1(noms, valeurs))
    f1.write(tex_resolution_thales2(noms, valeurs))
    f1.write(tex_resolution_thales3(noms, valeurs))


def long_val(noms, valeurs):  # renvoie un tuple contenant les noms des segments et leur longueur puis les noms des longueurs a calculer
    liste = []
    for i in xrange(8):
        if valeurs[i]:
            liste.append(creer_noms(noms, i))
            liste.append(nombre(valeurs[i]))
    for i in xrange(6):
        if not valeurs[i] and valeurs[8][0][0] % 3 != i % 3:
            liste.append(creer_noms(noms, i))
    return liste


def lAB(a):  # renvoie AB
    return str(a[0]) + str(a[1])


def nombre(a):
    texte = str(a).replace('.', ',')
    if a >= 1000 or a <= 0.0001:
        return '\\nombre{%s}' % texte
    else:
        if texte.count(',') and len(texte) - texte.find(',0') == 2:
            return texte.replace(',', '{,}').replace('{,}0', '')
        elif texte.count(','):
            return texte.replace(',', '{,}')
        else:
            return texte


def creer_noms(noms, i):
    if i == 0:
        return str(noms[0]) + str(noms[1])
    elif i == 1:
        return str(noms[0]) + str(noms[2])
    elif i == 2:
        return str(noms[1]) + str(noms[2])
    elif i == 3:
        return str(noms[0]) + str(noms[3])
    elif i == 4:
        return str(noms[0]) + str(noms[4])
    elif i == 5:
        return str(noms[3]) + str(noms[4])
    elif i == 6:
        return str(noms[3]) + str(noms[1])
    elif i == 7:
        return str(noms[4]) + str(noms[2])


def tex_enonce_thales(noms, valeurs):
    texte = \
        '  Sur la figure ci-contre, les droites $(%s)\\text{ et }(%s)$ sont parall\xe8les.\\par\n' % \
        (lAB(noms[1:3]), lAB(noms[3:5]))
    liste = long_val(noms, valeurs)
    texte = texte + \
        '  On donne $%s=\\unit[%s]{cm},\\quad %s=\\unit[%s]{cm}, \\quad %s=\\unit[%s]{cm}\\quad\\text{et}\\quad %s~=~\\unit[%s]{cm}$.\\par\n' % \
        tuple(liste[0:8])
    texte = texte + '  Calculer $%s\\text{ et }%s$.\n' % tuple(liste[8:10])
    return texte


def tex_resolution_thales0(n):
    return """  Les points $%s$,~ $%s$,~ $%s$ et $%s$, $%s$, $%s$ sont align\\'es et les droites $(%s)$ et $(%s)$ sont parall\\`eles.\\par
  D'apr\\`es le \\textbf{th\\'eor\\`eme de Thal\\`es} :
  $\\qquad\\mathbf{\\cfrac{%s}{%s}=\\cfrac{%s}{%s}=\\cfrac{%s}{%s}}$
""" % \
        (
        n[0],
        n[3],
        n[1],
        n[0],
        n[4],
        n[2],
        n[1] + n[2],
        n[3] + n[4],
        creer_noms(n, 0),
        creer_noms(n, 3),
        creer_noms(n, 1),
        creer_noms(n, 4),
        creer_noms(n, 2),
        creer_noms(n, 5),
        )


def tex_resolution_thales1(n, v):
    r = v[8][0][0] % 3  # grand rapport
    if v[8][1] == 1:
        sgn = '+'
    else:
        sgn = '-'
    if v[r] and v[r + 3]:  # on connait les deux rapports
        donnees = 0
    elif v[r + 3]:

        # on connait  le petit rapport, mais pas le grand

        v[r] = v[r + 6] + v[r + 3] * v[8][1]
        donnees = (creer_noms(n, r), creer_noms(n, r + 6), sgn,
                   creer_noms(n, r + 3), nombre(v[r]))
    else:
        v[r + 3] = (v[r] - v[r + 6]) * v[8][1]
        if sgn == '+':
            donnees = (creer_noms(n, r + 3), creer_noms(n, r), '-',
                       creer_noms(n, r + 6), nombre(v[r + 3]))
        else:
            donnees = (creer_noms(n, r + 3), creer_noms(n, r + 6), '-',
                       creer_noms(n, r), nombre(v[r + 3]))
    if donnees:
        return '  \\vspace{1ex}\\par De plus $%s=%s%s%s=\\unit[%s]{cm}$\n' % \
            donnees
    else:
        return ''


def tex_resolution_thales2(n, v):
    donnees = []
    for i in xrange(3):
        if v[i]:
            donnees.append(nombre(v[i]))
        else:
            donnees.append(creer_noms(n, i))
        if v[i + 3]:
            donnees.append(nombre(v[i + 3]))
        else:
            donnees.append(creer_noms(n, i + 3))
    return '  \\[\\frac{%s}{%s}=\\frac{%s}{%s}=\\frac{%s}{%s}\\]\n' % \
        tuple(donnees)


def nom_ou_valeur(n, v, i):
    if v[i]:
        return nombre(v[i])
    else:
        return creer_noms(n, i)


def valeur_exacte(a, approx=3, unit=1):
    nb = nombre(a)
    if unit:
        if nb.count(',') and (len(nb) - nb.find(',')) - 1 > approx:
            return '\\simeq\\unit[' + nombre(int(1000.0 * a) / 1000.0) + \
                ']{cm}'
        else:
            return '=\\unit[' + nombre(a) + ']{cm}'
    else:
        if nb.count(',') and (len(nb) - nb.find(',')) - 1 > approx:
            return '\\simeq' + nombre(int(1000.0 * a) / 1000.0)
        else:
            return '=' + nombre(a)


def tex_resolution_thales3(n, v):
    r = v[8][0][0] % 3  # grand rapport
    donnees = []
    for i in xrange(3):
        if i != r:
            donnees.extend([nom_ou_valeur(n, v, r), nom_ou_valeur(n, v,
                           r + 3), nom_ou_valeur(n, v, i), nom_ou_valeur(n,
                           v, i + 3)])
            if v[i]:  # on cherche i+3
                donnees.extend([creer_noms(n, i + 3), nombre(v[i]),
                               nombre(v[r + 3]), nombre(v[r]),
                               valeur_exacte(((v[i] * 1.0) * v[r + 3]) /
                               v[r])])
            else:
                donnees.extend([creer_noms(n, i), nombre(v[i + 3]),
                               nombre(v[r]), nombre(v[r + 3]),
                               valeur_exacte(((v[r] * 1.0) * v[i + 3]) /
                               v[r + 3])])
    texte = \
        '  $\\cfrac{%s}{%s}=\\cfrac{%s}{%s}\\quad$ donc $\\quad\\boxed{%s=\\cfrac{%s\\times %s}{%s}%s}$\\par\n' % \
        tuple(donnees[0:9])
    texte = texte + \
        '  $\\cfrac{%s}{%s}=\\cfrac{%s}{%s}\\quad$ donc $\\quad\\boxed{%s=\\cfrac{%s\\times %s}{%s}%s}$\\par\n' % \
        tuple(donnees[9:18])
    return texte


#def pyromax(a):
#    maxi = a[0]
#    for i in xrange(len(a)):
#        if a[i] > maxi:
#            maxi = a[i]
#    return maxi
#
#
#def pyromin(a):
#    mini = a[0]
#    for i in xrange(len(a)):
#        if a[i] < mini:
#            mini = a[i]
#    return mini


def fig_thales(noms, valeurs):
    v = test_valeurs_thales(valeurs[0:8], valeurs[8][0], valeurs[8][1])
    type_thales = valeurs[8][1]
    angle = int(((100.0 * acos(((v[0] ** 2 + v[1] ** 2) - v[2] ** 2) / ((2 *
                v[0]) * v[1]))) * 180) / pi) / 100.0
    v = [int(v[i] * 100) / 100.0 for i in xrange(8)]
    mini_x = int(100.0 * min(0, v[1] * cos((angle * pi) / 180), v[3] *
                 type_thales, (v[4] * cos((angle * pi) / 180)) *
                 type_thales)) / 100.0 - 1.5
    mini_y = int(100.0 * min(0, (v[4] * sin((angle * pi) / 180)) *
                 type_thales)) / 100.0 - 1.5
    maxi_x = int(100.0 * max(v[0], v[1] * cos((angle * pi) / 180))) / \
        100.0 + 1.5
    maxi_y = int((100.0 * v[1]) * sin((angle * pi) / 180)) / 100.0 + .5
    echelle = int(400 / max(abs(mini_x) + maxi_x, abs(mini_y) + maxi_y)) / \
        100.0
    if type_thales == 1:
        return (
            echelle,
            mini_x,
            mini_y,
            maxi_x,
            maxi_y,
            225,
            angle + 45,
            noms[0],
            noms[1],
            noms[2],
            v[0],
            v[1],
            angle,
            -45,
            angle + 90,
            noms[3],
            noms[4],
            v[3],
            v[4],
            angle,
            )
    else:
        return (
            echelle,
            mini_x,
            mini_y,
            maxi_x,
            maxi_y,
            135,
            angle + 45,
            noms[0],
            noms[1],
            noms[2],
            v[0],
            v[1],
            angle,
            135,
            angle + 180,
            noms[3],
            noms[4],
            -v[3],
            -v[4],
            angle,
            )


def tex_fig_thales(noms, valeurs):
    donnees = fig_thales(noms, valeurs)
    enonce = \
        '''  \\begin{wrapfigure}{r}{4cm}
    \\psset{PointSymbol=x,unit=%s}
    \\begin{pspicture}(%s,%s)(%s,%s)
        \\SpecialCoor
        \\pstTriangle[PosAngleA=%s,PosAngleB=-45,PosAngleC=%s,PointNameA=%s,PointNameB=%s,PointNameC=%s](0,0){a}(%s,0){b}(%s;%s){c}
        \\pstTriangle[PosAngleB=%s,PosAngleC=%s,PointSymbolA=none,PointNameA=none,PointNameB=%s,PointNameC=%s](0,0){a}(%s,0){b}(%s;%s){c}
    \\end{pspicture}
  \\end{wrapfigure}\\par
''' % \
        donnees
    return enonce


#
# ------------------- RECIPROQUE DU THEOREME DE THALES -------------------
#


def valeurs_reciproque_thales():
    while True:
        (a, b, c, d) = (random.randrange(2, 50), random.randrange(2, 50),
                        random.randrange(2, 20), random.randrange(2, 20))
        p1 = pgcd(a, b)
        (a, b) = (a / p1, b / p1)
        if c < d:
            (c, d) = (d, c)
        if a != b and int(c / d) != (c * 1.0) / d and 10 < a * c < 200 and \
            10 < a * d < 200 and 10 < b * c < 200 and 10 < b * d < 200 and \
            .3 < (d * 1.0) / c < .7:
            break
    t = valeur_alea(-1, 1)  # -1 si papillon, 1 si triangle
    r = random.randrange(5)
    while r == 2:
        r = random.randrange(5)
    angle = random.randrange(15, 105)
    valeurs = (
        (a * c) / 10.0,
        (b * c) / 10.0,
        0,
        (a * d) / 10.0,
        (b * d) / 10.0,
        0,
        (a * c - (t * a) * d) / 10.0,
        (b * c - (t * b) * d) / 10.0,
        angle,
        t,
        r,
        )
    return valeurs


def fig_rec_thales(noms, v):
    type_thales = v[9]
    angle = v[8]
    mini_x = int(100.0 * min(0, v[1] * cos((angle * pi) / 180), v[3] *
                 type_thales, (v[4] * cos((angle * pi) / 180)) *
                 type_thales)) / 100.0 - 1.5
    mini_y = int(100.0 * min(0, (v[4] * sin((angle * pi) / 180)) *
                 type_thales)) / 100.0 - 1.5
    maxi_x = int(100.0 * max(v[0], v[1] * cos((angle * pi) / 180))) / \
        100.0 + 1.5
    maxi_y = int((100.0 * v[1]) * sin((angle * pi) / 180)) / 100.0 + .5
    echelle = int(400 / max(abs(mini_x) + maxi_x, abs(mini_y) + maxi_y)) / \
        100.0
    if type_thales == 1:
        return (
            echelle,
            mini_x,
            mini_y,
            maxi_x,
            maxi_y,
            225,
            angle + 45,
            noms[0],
            noms[1],
            noms[2],
            v[0],
            v[1],
            angle,
            -45,
            angle + 90,
            noms[3],
            noms[4],
            v[3],
            v[4],
            angle,
            )
    else:
        return (
            echelle,
            mini_x,
            mini_y,
            maxi_x,
            maxi_y,
            135,
            angle + 45,
            noms[0],
            noms[1],
            noms[2],
            v[0],
            v[1],
            angle,
            135,
            angle + 180,
            noms[3],
            noms[4],
            -v[3],
            -v[4],
            angle,
            )


def tex_fig_rec_thales(noms, valeurs):
    donnees = fig_rec_thales(noms, valeurs)
    enonce = \
        '''  \\begin{wrapfigure}{r}{4cm}
    \\psset{PointSymbol=x,unit=%s}
    \\begin{pspicture}(%s,%s)(%s,%s)
      \\SpecialCoor
      \\pstTriangle[PosAngleA=%s,PosAngleB=-45,PosAngleC=%s,PointNameA=%s,PointNameB=%s,PointNameC=%s](0,0){a}(%s,0){b}(%s;%s){c}
      \\pstTriangle[PosAngleB=%s,PosAngleC=%s,PointSymbolA=none,PointNameA=none,PointNameB=%s,PointNameC=%s](0,0){a}(%s,0){b}(%s;%s){c}
    \\end{pspicture}
  \\end{wrapfigure}\\par
''' % \
        donnees
    return enonce


def rec_thales(f0, f1):
    noms = noms_sommets(5)  # les noms des sommets
    valeurs = valeurs_reciproque_thales()
    f0.write(tex_fig_rec_thales(noms, valeurs))
    f0.write(tex_enonce_rec_thales(noms, valeurs) + '  \\vspace{2cm}\n')
    f1.write(tex_fig_rec_thales(noms, valeurs))
    f1.write(tex_enonce_rec_thales(noms, valeurs) +
             "  \\par\\dotfill{}\\\\\n\n")
    f1.write(tex_resolution_rec_thales0(noms, valeurs))
    f1.write(tex_resolution_rec_thales1(noms, valeurs))


    #  f1.write(tex_resolution_rec_thales2(noms, valeurs))
    # f1.write(tex_resolution_rec_thales3(noms, valeurs))


def enonce_rec_thales(n, v):
    (r, l) = (v[10], [])
    for i in xrange(5):
        if i != 2:
            if i == r:
                l.extend([creer_noms(n, 6 + i % 3), nombre(v[6 + i % 3])])
            else:
                l.extend([creer_noms(n, i), nombre(v[i])])
    l1 = [i for i in xrange(4)]
    l2 = []
    for i in xrange(4):
        a = l1.pop(random.randrange(4 - i))
        l2.extend([l[2 * a], l[2 * a + 1]])
    l2.extend([creer_noms(n, 2), creer_noms(n, 5)])
    return tuple(l2)


def tex_enonce_rec_thales(n, v):
    d = enonce_rec_thales(n, v)
    texte = \
        '''  Sur la figure ci-contre, on donne $%s=\\unit[%s]{cm}$, $%s=\\unit[%s]{cm}$, $%s=\\unit[%s]{cm}$ et $%s=\\unit[%s]{cm}$.\\par
  D\xe9montrer que les droites $(%s)$ et $(%s)$ sont parall\xe8les.
''' % \
        d
    return texte


def resolution_rec_thales0(n, v):
    t = v[9]
    r = v[10]
    if t > 0:
        d = [n[0], n[3], n[1], n[0], n[4], n[2], creer_noms(n, r)]
    else:
        d = [n[3], n[0], n[1], n[4], n[0], n[2], creer_noms(n, r)]
    if r < 2:
        if t > 0:
            d.extend([creer_noms(n, r + 6), '+', creer_noms(n, r + 3),
                     nombre(v[r])])
        else:
            d.extend([creer_noms(n, r + 6), '-', creer_noms(n, r + 3),
                     nombre(v[r])])
    else:
        if t > 0:
            d.extend([creer_noms(n, r - 3), '-', creer_noms(n, r + 3),
                     nombre(v[r])])
        else:
            d.extend([creer_noms(n, r + 3), '-', creer_noms(n, r - 3),
                     nombre(v[r])])
    return tuple(d)


def tex_resolution_rec_thales0(n, v):
    return """  Les points $%s$, $%s$, $%s$~ et $%s$, $%s$, $%s$ sont align\\'es dans le m\\^eme ordre.\\par
  De plus $%s=%s%s%s=\\unit[%s]{cm}$.\\par
""" % \
        resolution_rec_thales0(n, v)


def resolution_rec_thales1(n, v):
    (d, t) = ([], '')
    for i in xrange(2):
        d.extend([creer_noms(n, i), creer_noms(n, i + 3), nombre(v[i]),
                 nombre(v[i + 3])])
        if valeur_exacte(v[i] / v[i + 3], approx=5).count('='):
            d.append(valeur_exacte(v[i] / v[i + 3], approx=5, unit=0))
        else:
            if v[i] != int(v[i]) or v[i + 3] != int(v[i + 3]):
                p = pgcd(int(v[i] * 10), int(v[i + 3] * 10))
                if p == 1:
                    t = '=\\cfrac{%s}{%s}' % (nombre(v[i] * 10), nombre(v[i +
                            3] * 10))
                else:
                    t = '=\\cfrac{%s_{\\div%s}}{%s_{\\div%s}}' % (nombre(v[i] *
                            10), p, nombre(v[i + 3] * 10), p)
            if fractions.simplifie((int(v[i] * 10), int(v[i + 3] * 10))):
                d.append(t + '=' + fractions.tex_frac(fractions.simplifie((int(v[i] *
                         10), int(v[i + 3] * 10)))))
            else:
                d.append(t + '=' + fractions.tex_frac((int(v[i] * 10),
                         int(v[i + 3] * 10))))
    d.extend([creer_noms(n, 0), creer_noms(n, 3), creer_noms(n, 1),
             creer_noms(n, 4), creer_noms(n, 2), creer_noms(n, 5)])
    return tuple(d)


def tex_resolution_rec_thales1(n, v):
    d = resolution_rec_thales1(n, v)
    return """  $\\left.
  \\renewcommand{\\arraystretch}{2}
  \\begin{array}{l}
    \\bullet\\cfrac{%s}{%s}=\\cfrac{%s}{%s}%s\\\\\n    \\bullet\\cfrac{%s}{%s}=\\cfrac{%s}{%s}%s
  \\end{array}
  \\right\\rbrace$
  Donc $\\cfrac{%s}{%s}=\\cfrac{%s}{%s}$\\,.\\par
  D'apr\xe8s la \\textbf{r\xe9ciproque du th\xe9or\xe8me de Thal\xe8s}, \\fbox{les droites $(%s)$ et $(%s)$ sont parall\xe8les.}
""" % \
        d


#
# ------------------- TRIGONOMETRIE -------------------
#


def trigo_init(f0, f1):
    s = noms_sommets(6)
    n1 = cotes_sommets(s[0:3])
    n2 = cotes_sommets(s[3:6])
    v = valeurs_trigo()
    enonce_trigo(f0, f1, ((s[0:3], n1, v[0]), (s[3:6], n2, v[1])))


def enonce_trigo(f0, f1, v):
    (l, lt) = ([], [])
    for j in xrange(2):
        f = (('\\sin', 1, 0), ('\\cos', 2, 0), ('\\tan', 1, 2))[v[j][2][0]]
        for i in xrange(2):
            l.append(v[j][1][f[i + 1]])
            l.append(v[j][2][i + 1])
        l.append(tex_angle(v[j][0], 1))
        l.append(v[j][2][3])
    for j in xrange(2):
        tmp = []
        for i in xrange(3):
            if len(l[2 * i + 6 * j]) < 3:
                if l[2 * i + 6 * j + 1]:
                    lt.append('$%s=\\unit[%s]{cm}$' % (l[2 * i + 6 * j],
                              nombre(l[2 * i + 6 * j + 1])))
                else:
                    tmp = 'la longueur $%s$' % l[2 * i + 6 * j]
            elif l[2 * i + 6 * j + 1]:
                lt.append('$%s=%s\\degres$' % (l[2 * i + 6 * j], l[2 * i +
                          6 * j + 1]))
            else:
                lt.append('la mesure de l\'angle $%s$' % l[2 * i + 6 * j])
        if tmp:
            lt.append(tmp)
    f0.write('  \\begin{multicols}{2}\n')
    f0.write('    \\begin{enumerate}\n')
    f1.write('  \\begin{multicols}{2}\n')
    f1.write('    \\begin{enumerate}\n')
    tr = nom_triangle(v[0][0])
    f0.write('    \\item $%s$ est un triangle rectangle en $%s$ tel que :\\par \n' %
             (tr, v[0][0][0]))
    f0.write('''      %s et %s.\\par
      Calculer %s.\\par
''' % tuple(lt[0:3]))
    f1.write('    \\item $%s$ est un triangle rectangle en $%s$ tel que :\\par \n' %
             (tr, v[0][0][0]))
    f1.write('''      %s et %s.\\par
      Calculer %s.\\par
''' % tuple(lt[0:3]))
    f1.write("      \\dotfill{}\\par\\vspace{2ex}\n")
    f1.write('      Dans le triangle $%s$ rectangle en $%s$,\n' % (tr, v[0][0][0]))  # résolution
    v2 = (v[0][1], v[0][2])
    l2 = l[0:6]
    resolution_trigo(f1, v2, l2)
    tr = nom_triangle(v[1][0])
    f0.write('      \\columnbreak\n')
    f1.write('      \\columnbreak\n')
    f0.write('    \\item $%s$ est un triangle rectangle en $%s$ tel que :\\par\n' %
             (tr, v[1][0][0]))
    f0.write('''      %s et %s.\\par
      Calculer %s.\\par
''' % tuple(lt[3:6]))
    f1.write('    \\item $%s$ est un triangle rectangle en $%s$ tel que :\\par\n' %
             (tr, v[1][0][0]))
    f1.write('''      %s et %s.\\par
      Calculer %s.\\par
''' % tuple(lt[3:6]))
    f1.write("      \\dotfill{}\\par\\vspace{2ex}\n")
    f1.write('      Dans le triangle $%s$ rectangle en $%s$,\n' % (tr, v[1][0][0]))  # résolution
    v2 = (v[1][1], v[1][2])
    l2 = l[6:12]
    resolution_trigo(f1, v2, l2)
    f0.write('    \\end{enumerate}\n')
    f0.write('  \\end{multicols}\n')
    f1.write('    \\end{enumerate}\n')
    f1.write('  \\end{multicols}\n')


def resolution_trigo(f1, v2, l2):
    f = (('\\sin', 1, 0), ('\\cos', 2, 0), ('\\tan', 1, 2))[v2[1][0]]
    ecrit_tex(f1, '%s%s=\\cfrac{%s}{%s}' % (f[0], l2[4], v2[0][f[1]], v2[0][f[2]]),
              tabs=3, thenocalcul='')
    if not v2[1][3]:
        ecrit_tex(f1, '%s%s=\\cfrac{%s}{%s}' % (f[0], l2[4], nombre(v2[1][1]),
                  nombre(v2[1][2])), tabs=3, thenocalcul='')
        if f[0] == '\\sin':
            r = (asin(v2[1][1] / v2[1][2]) * 180) / pi
        elif f[0] == '\\cos':
            r = (acos(v2[1][1] / v2[1][2]) * 180) / pi
        else:
            r = (atan(v2[1][1] / v2[1][2]) * 180) / pi
        ecrit_tex(f1,
                  '%s=%s^{-1}\\left(\\cfrac{%s}{%s}\\right)\\simeq%s\\degres' %
                  (l2[4], f[0], nombre(v2[1][1]), nombre(v2[1][2]),
                  nombre(int(r * 10) / 10.0)), tabs=3, cadre=1,
                  thenocalcul='')
    elif not v2[1][1]:
        ecrit_tex(f1, '%s%s=\\cfrac{%s}{%s}' % (f[0], v2[1][3], v2[0][f[1]],
                  nombre(v2[1][2])), tabs=3, thenocalcul='')
        if f[0] == '\\sin':
            r = sin((v2[1][3] * pi) / 180)
        elif f[0] == '\\cos':
            r = cos((v2[1][3] * pi) / 180)
        else:
            r = tan((v2[1][3] * pi) / 180)
        r = r * v2[1][2]
        ecrit_tex(f1, '%s=%s%s\\times %s\\simeq\\unit[%s]{cm}' % (v2[0][f[1]],
                  f[0], v2[1][3], nombre(v2[1][2]), nombre(int(r * 100) /
                  100.0)), tabs=3, cadre=1, thenocalcul='')
    else:
        ecrit_tex(f1, '%s%s=\\cfrac{%s}{%s}' % (f[0], v2[1][3], nombre(v2[1][1]),
                  v2[0][f[2]]), tabs=3, thenocalcul='')
        if f[0] == '\\sin':
            r = sin((v2[1][3] * pi) / 180)
        elif f[0] == '\\cos':
            r = cos((v2[1][3] * pi) / 180)
        else:
            r = tan((v2[1][3] * pi) / 180)
        r = v2[1][1] / r
        ecrit_tex(f1, '%s=\\cfrac{%s}{%s%s}\\simeq\\unit[%s]{cm}' % (v2[0][f[2]],
                  nombre(v2[1][1]), f[0], v2[1][3], nombre(int(r * 100) /
                  100.0)), tabs=3, cadre=1, thenocalcul='')


def tex_angle(s, n):  # renvoie \\widehat{ABC} où s est la liste des 3 sommets du triangle et n est le rang du sommet de l'angle dans cette liste
    return '\\widehat{%s%s%s}' % (s[(n + 2) % 3], s[n], s[(n + 1) % 3])


def valeurs_trigo():
    l = [random.randrange(10, 121) / 10.0 for i in xrange(3)]
    l.sort()
    l.append(random.randrange(15, 76))
    trigo = random.randrange(3)
    if random.randrange(2):  # on choisit en 1er une longueur et un angle
        if random.randrange(2):  # on connait la première des deux longueurs
            v = (trigo, l[0], 0, l[3])
        else:
            v = (trigo, 0, l[0], l[3])
        trigo = (trigo + 1 + random.randrange(2)) % 3
        v = (v, (trigo, l[1], l[2], 0))
    else:

        # on choisit en 1er deux longueurs

        v = (trigo, l[1], l[2], 0)
        trigo = (trigo + 1 + random.randrange(2)) % 3
        if random.randrange(2):  # on connait la première des deux longueurs
            v = (v, (trigo, l[0], 0, l[3]))
        else:
            v = (v, (trigo, 0, l[0], l[3]))
    return v


