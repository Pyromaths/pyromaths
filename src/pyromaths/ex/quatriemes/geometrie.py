#!/usr/bin/env python3

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

import random
from builtins import range
from builtins import str
from decimal import Decimal
from math import acos, asin, atan, pi, sin, cos, tan

from fractions import Fraction
from pyromaths.outils.Geometrie import couples_pythagore, choix_points
from pyromaths.ex import LegacyExercise


#
# ------------------- THEOREME DE PYTHAGORE -------------------
def fig_tr_rect(lg):
    # renvoie les angles au centre des trois sommets du triangle ABC rectange en C
    a = random.randrange(360)
    if a < 180:
        b = a + 180
    else:
        b = a - 180
    c = float(Fraction(int((180 - 2 * acos(lg[1] * 1 / lg[2]) * 180 / pi) * 100), 100) + a)
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
            nom_tr,
            noms[2],
            cotes[long0],
            nombre(longueurs[long0]),
            cotes[long1],
            nombre(longueurs[long1]),
            cotes[(3 - long0) - long1],
        )


def _exo_pythagore():
    types_exercice = [[2, random.randrange(2)], [0, 1]]
    random.shuffle(types_exercice)
    random.shuffle(types_exercice[0])
    random.shuffle(types_exercice[1])
    exo = ["\\exercice\n\\begin{multicols}{2}\n  \\begin{enumerate}"]
    cor = ["\\exercice*\n\\begin{multicols}{2}\n  \\begin{enumerate}"]
    for j in range(2):
        while True:
            longueurs = couples_pythagore[random.randrange(len(couples_pythagore))]
            longueurs = [longueurs[i] / 10 for i in range(3)]
            if inegalite_triangulaire(longueurs):
                break
        noms = choix_points(3)
        angles = fig_tr_rect(longueurs)
        nom_tr = nom_triangle(noms)
        long0, long1 = types_exercice[j]
        cotes = cotes_sommets(noms)
        enonce = \
            """    \\item Soit $%s$ un triangle rectangle en $%s$ tel que :\\par
$%s=\\unit[%s]{cm}$ et $%s=\\unit[%s]{cm}$.\\par
Calculer la longueur $%s$.""" % \
            enonce_pythagore(noms, angles, longueurs, cotes, nom_tr, long0, long1)
        exo.append(enonce)
        cor.append(enonce)
        cor.append("\\par\\dotfill{}\\par\n")
        cor.append(u"Le triangle $%s$ est rectangle en $%s$.\\par" % \
                   (nom_tr, noms[2]))
        cor.append(u"Son hypoténuse est $[%s]$.\\par" % (cotes[2]))
        cor.append(u"D'après le \\textbf{théorème de Pythagore} :")
        cor.append("\\[%s^2=%s^2+%s^2\\]" % (cotes[2], cotes[0], cotes[1]))
        if long0 == 2 or long1 == 2:
            cor.append("\\[%s^2=%s^2-%s^2\\kern1cm\\text{(On cherche }%s)\\]" %
                       (cotes[(3 - long0) - long1], cotes[2], cotes[((4 -
                                                                      long0) - long1) % 2], cotes[(3 - long0) - long1]))
        if long0 == 2 or long1 == 2:
            cor.append("\\[%s^2=%s^2-%s^2\\]" % (cotes[(3 - long0) - long1],
                                                 nombre(longueurs[2]), nombre(longueurs[((4 - long0) -
                                                                                         long1) % 2])))
        else:
            cor.append("\\[%s^2=%s^2+%s^2\\]" % (cotes[2], nombre(longueurs[0]),
                                                 nombre(longueurs[1])))
        if long0 == 2 or long1 == 2:
            cor.append("\\[%s^2=%s-%s\\]" % (cotes[(3 - long0) - long1],
                                             nombre(longueurs[2] ** 2), nombre(longueurs[((4 -
                                                                                           long0) - long1) % 2] ** 2)))
        else:
            cor.append("\\[%s^2=%s+%s\\]" % (cotes[2], nombre(longueurs[0] **
                                                              2), nombre(longueurs[1] ** 2)))
        if long0 == 2 or long1 == 2:
            cor.append("\\[%s^2=%s\\]" % (cotes[(3 - long0) - long1],
                                          nombre(longueurs[2] ** 2 - longueurs[((4 - long0) -
                                                                                long1) % 2] ** 2)))
        else:
            cor.append("\\[%s^2=%s\\]" % (cotes[2], nombre(longueurs[0] **
                                                           2 + longueurs[1] ** 2)))
        if long0 == 2 or long1 == 2:
            cor.append("\\[ \\boxed{\\text{Donc }%s=\\sqrt{%s}=\\unit[%s]{cm}}\\]" %
                       (cotes[(3 - long0) - long1], nombre(longueurs[2] ** 2 -
                                                           longueurs[((4 - long0) - long1) % 2] ** 2),
                        nombre(longueurs[(3 -
                                          long0) - long1])))
        else:
            cor.append("\\[\\boxed{\\text{Donc }%s=\\sqrt{%s}=\\unit[%s]{cm}}\\]" %
                       (cotes[2], nombre(longueurs[0] ** 2 + longueurs[1] **
                                         2), nombre(longueurs[2])))
        if j == 0:
            exo.append("\\columnbreak")
            cor.append("\\columnbreak")
    exo.append("\\end{enumerate}\n\\end{multicols}\n")
    cor.append("\\end{enumerate}\n\\end{multicols}\n")
    return (exo, cor)

class exo_pythagore(LegacyExercise):
    """Théorème de Pythagore"""

    tags = ["quatrième"]
    function = _exo_pythagore


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


def _exo_triangle_cercle():
    exo = ["\\exercice"]
    cor = ["\\exercice*"]
    while True:
        longueurs = couples_pythagore[random.randrange(len(couples_pythagore))]
        longueurs = [longueurs[i] / 10 for i in range(3)]
        if inegalite_triangulaire(longueurs):
            break
    noms = choix_points(3)
    angles = fig_tr_rect(longueurs)
    nom_tr = nom_triangle(noms)
    long0 = random.randrange(3)
    long1 = (random.randrange(2) + 1 + long0) % 3
    cotes = cotes_sommets(noms)
    enonce = \
        u"""\\begin{minipage}{4cm}
\\begin{pspicture}(-2,-2)(2,2)
\\SpecialCoor\\psset{PointSymbol=none}
\\pstGeonode[PointName=%s,PosAngle=%s](1.5;%s){a}
\\pstGeonode[PointName=%s,PosAngle=%s](1.5;%s){b}
\\pstGeonode[PointName=%s,PosAngle=%s](1.5;%s){c}
\\pspolygon(a)(b)(c)\\pscircle(0,0){1.5}
\\rput(1.8;%s){$\\big(\\mathcal{C}\\big)$}
\\end{pspicture}
\\end{minipage}\\hfill
\\begin{minipage}{13cm}
$\\big(\\mathcal{C}\\big)$ est un cercle de diamètre $[%s]$ et $%s$ est un point de $\\big(\\mathcal{C}\\big)$.\\par
On donne $%s=\\unit[%s]{cm}$ et $%s=\\unit[%s]{cm}$.\\par
Calculer la longueur $%s$.""" % \
        enonce_pythagore(noms, angles, longueurs, cotes, nom_tr, long0, long1, diam=1)
    exo.append(enonce)
    cor.append(enonce)
    cor.append("\\par\\dotfill{}\\\\\n")
    cor.append(u"$[%s]$ est le diamètre du cercle circonscrit au triangle $%s$.\\par" %
               (cotes[2], nom_tr))
    cor.append("\\fbox{Donc le triangle %s est rectangle en %s.}\\\\\n" %
               (nom_tr, noms[2]))
    cor.append(u"D'après le \\textbf{théorème de Pythagore} :")
    cor.append(u"\\[%s^2=%s^2+%s^2\\kern1cm\\text{(car }[%s]\\text{ est \\emph{l'hypoténuse})}\\]" %
               (cotes[2], cotes[0], cotes[1], cotes[2]))
    if long0 == 2 or long1 == 2:
        cor.append("\\[%s^2=%s^2-%s^2\\kern1cm\\text{(On cherche }%s)\\]" %
                   (cotes[(3 - long0) - long1], cotes[2], cotes[((4 -
                                                                  long0) - long1) % 2], cotes[(3 - long0) - long1]))
    if long0 == 2 or long1 == 2:
        cor.append("\\[%s^2=%s^2-%s^2\\]" % (cotes[(3 - long0) - long1],
                                             nombre(longueurs[2]), nombre(longueurs[((4 - long0) -
                                                                                     long1) % 2])))
    else:
        cor.append("\\[%s^2=%s^2+%s^2\\]" % (cotes[2], nombre(longueurs[0]),
                                             nombre(longueurs[1])))
    if long0 == 2 or long1 == 2:
        cor.append("\\[%s^2=%s-%s\\]" % (cotes[(3 - long0) - long1],
                                         nombre(longueurs[2] ** 2), nombre(longueurs[((4 -
                                                                                       long0) - long1) % 2] ** 2)))
    else:
        cor.append("\\[%s^2=%s+%s\\]" % (cotes[2], nombre(longueurs[0] **
                                                          2), nombre(longueurs[1] ** 2)))
    if long0 == 2 or long1 == 2:
        cor.append("\\[%s^2=%s\\]" % (cotes[(3 - long0) - long1],
                                      nombre(longueurs[2] ** 2 - longueurs[((4 - long0) -
                                                                            long1) % 2] ** 2)))
    else:
        cor.append("\\[%s^2=%s\\]" % (cotes[2], nombre(longueurs[0] **
                                                       2 + longueurs[1] ** 2)))
    if long0 == 2 or long1 == 2:
        cor.append("\\[\\boxed{\\text{Donc }%s=\\sqrt{%s}=\\unit[%s]{cm}}\\]" %
                   (cotes[(3 - long0) - long1], nombre(longueurs[2] ** 2 -
                                                       longueurs[((4 - long0) - long1) % 2] ** 2), nombre(longueurs[(3 -
                                                                                                                     long0) - long1])))
    else:
        cor.append("\\[\\boxed{\\text{Donc }%s=\\sqrt{%s}=\\unit[%s]{cm}}\\]" %
                   (cotes[2], nombre(longueurs[0] ** 2 + longueurs[1] **
                                     2), nombre(longueurs[2])))
    exo.append("\\end{minipage}\n")
    cor.append("\\end{minipage}\n")
    return (exo, cor)

class exo_triangle_cercle(LegacyExercise):
    """Cercle et théorème de Pythagore"""

    tags = ["quatrième"]
    function = _exo_triangle_cercle


#
# ------------------- RECIPROQUE DU THEOREME DE PYTHAGORE -------------------
#


def _exo_reciproque_pythagore():
    exo = ["\\exercice"]
    cor = ["\\exercice*"]
    while True:
        longueurs = couples_pythagore[random.randrange(len(couples_pythagore))]
        longueurs = [longueurs[i] / 10 for i in range(3)]
        if inegalite_triangulaire(longueurs):
            break
    noms = choix_points(3)
    nom_tr = nom_triangle(noms)
    l = [i for i in range(3)]
    n = [l.pop(random.randrange(3 - i)) for i in range(3)]
    c = cotes_sommets(noms)
    recip = (nom_tr, c[n[0]], nombre(longueurs[n[0]]), c[n[1]], nombre(longueurs[n[1]]),
             c[n[2]], nombre(longueurs[n[2]]), nom_tr)
    enonce = \
        """Soit $%s$ un triangle tel que : $\\quad %s=\\unit[%s]{cm}\\quad$, $\\quad %s=\\unit[%s]{cm}\\quad$ et $\\quad %s=\\unit[%s]{cm}$.\\par
Quelle est la nature du triangle $%s$?
""" % \
        recip
    exo.append(enonce)
    cor.append(enonce)
    cor.append("\\par\\dotfill{}\\\\\n")
    cor.append(u"Le triangle %s n'est ni isocèle, ni équilatéral.\\par\n" %
               nom_tr)
    cor.append("$\\left.")
    cor.append("\\renewcommand{\\arraystretch}{2}")
    cor.append("\\begin{array}{l}")

    cor.append(u"\\bullet %s^2=%s^2=%s\\qquad\\text{(}[%s]\\text{ est le plus grand côté.)}\\\\\n" %
               (c[2], nombre(longueurs[2]), nombre(longueurs[2] ** 2), c[2]))
    cor.append("\\bullet  %s^2+%s^2=%s^2+%s^2=%s \n" % (c[0], c[1],
                                                        nombre(longueurs[0]), nombre(longueurs[1]),
                                                        nombre(longueurs[0] **
                                                               2 + longueurs[1] ** 2)))
    cor.append("\\end{array}")
    cor.append("\\right\\rbrace$")
    cor.append(u"""Donc $%s^2=%s^2+%s^2$.\\par
D'après la \\textbf{réciproque du théorème de Pythagore},
\\fbox{le triangle $%s$ est rectangle en $%s$.}""" %
               (c[2], c[0], c[1], nom_tr, noms[2]))
    return (exo, cor)

class exo_reciproque_pythagore(LegacyExercise):
    """Réciproque du théorème de Pythagore"""

    tags = ["quatrième"]
    function = _exo_reciproque_pythagore


#
# ------------------- THEOREME DE THALES -------------------
#


def valeurs_thales(pyromax):
    liste = [0, 0, 0, 0, 0, 0, 0, 0]
    while liste == [0, 0, 0, 0, 0, 0, 0, 0]:
        for i in range(3):
            liste[i] = random.randrange(2)
    a = random.randrange(liste.count(1))
    for i in range(3):
        if liste[i]:
            if not a:
                liste[i + 3] = 1
            a = a - 1
        else:
            liste[i + 3] = 1  # on doit connaitre le numeratuer ou le denominateur
    for i in range(2):  # AB et AE  ou  AB et BE  ou  AE et EB
        if liste[i] and liste[i + 3]:  # i est le rapport complet. On choisit une des 3 formes ci-dessus
            a = random.randrange(2)
            liste[i + 6] = 1
            liste[i + 3 * a] = 0
            rapport = [i + 3 * ((a + 1) % 3), i + 3 * ((a + 2) % 3)]
            rapport.sort()
    if liste[2] and liste[5]:
        rapport = [2, 5]
    valeurs = [0, 0, 0, 0, 0, 0, 0, 0]
    for i in range(3):
        if liste[i]:
            valeurs[i] = random.randrange(15, pyromax)
        if liste[i + 3] and liste[i]:
            valeurs[i + 3] = random.randrange(5, valeurs[i] - 9)
        elif liste[i + 3]:
            valeurs[i + 3] = random.randrange(5, pyromax)
    if liste[6]:
        valeurs[6] = random.randrange(5, pyromax)
    if liste[7]:
        valeurs[7] = random.randrange(5, pyromax)

    # --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # type_thales=valeur_alea(-1,1) # -1 si papillon, 1 si triangle

    type_thales = 1
    valeurs.append((rapport, type_thales))
    if test_valeurs_thales(valeurs, rapport, type_thales):
        return valeurs
    else:
        return 0


def test_valeurs_thales(valeurs, rapport, type_thales):
    v = [valeurs[i] for i in range(8)]
    if rapport[0] // 3 == 0 and rapport[1] // 3 == 2:  # On donne AB et EB
        v[rapport[0] + 3] = (v[rapport[0]] - v[rapport[1]]) * type_thales
    elif rapport[0] // 3 == 1 and rapport[1] // 3 == 2:  # On donne AE et EB
        v[rapport[0] - 3] = v[rapport[0]] * type_thales + v[rapport[1]]
    if v[rapport[0] % 3]:  # rapport est AE/AB
        rapp = Fraction(v[rapport[0] % 3 + 3], v[rapport[0] % 3])
    else:
        rapp = 0
    for i in range(3):
        if not v[i] and rapp:
            v[i] = v[i + 3] / rapp
        elif not v[i + 3]:
            v[i + 3] = v[i] * rapp
    if inegalite_triangulaire(v[0:3]) and inegalite_triangulaire(v[3:6]) and .3 < rapp < .7:
        return v
    else:
        return 0


def inegalite_triangulaire(a):  # renvoie 1 si c'est un triangle, 0 sinon
    vrai = 0
    coef = Fraction(12, 10)  # evite les triangles trop ecrases
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


def _exo_thales():
    exo = ["\\exercice"]
    cor = ["\\exercice*"]
    noms = choix_points(5)  # les noms des sommets
    arrondi = random.randrange(1, 4)
    text_arrondi = ['dix', 'cent', 'mill'][arrondi - 1] + u'ième'
    while True:
        valeurs = valeurs_thales(70)  # les longueurs en mm
        if valeurs:
            break
    exo.append(tex_fig_thales(noms, valeurs))
    exo.append(tex_enonce_thales(noms, valeurs, text_arrondi))
    cor.append(tex_fig_thales(noms, valeurs))
    cor.append(tex_enonce_thales(noms, valeurs, text_arrondi))
    cor.append(tex_resolution_thales0(noms, valeurs))
    cor.append(tex_resolution_thales1(noms, valeurs))
    cor.append(tex_resolution_thales2(noms, valeurs))
    cor.append(tex_resolution_thales3(noms, valeurs, arrondi))
    return (exo, cor)

class exo_thales(LegacyExercise):
    """Théorème de Thalès"""

    tags = ["quatrième"]
    function = _exo_thales


def long_val(noms,
             valeurs):  # renvoie un tuple contenant les noms des segments et leur longueur puis les noms des longueurs a calculer
    liste = []
    for i in range(8):
        if valeurs[i]:
            liste.append(creer_noms(noms, i))
            liste.append(nombre(valeurs[i]))
    for i in range(6):
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


def tex_enonce_thales(noms, valeurs, arrondi):
    texte = \
        u'{Sur la figure ci-contre, les droites $(%s)$ et $(%s)$ sont parallèles.\\par\n' % \
        (lAB(noms[1:3]), lAB(noms[3:5]))
    liste = long_val(noms, valeurs)
    texte = texte + \
            'On donne $%s=\\unit[%s]{cm}$,$\\quad %s=\\unit[%s]{cm}$, $\\quad %s=\\unit[%s]{cm}\\quad$ et $\\quad %s~=~\\unit[%s]{cm}$.\\par\n' % \
            tuple(liste[0:8])
    texte = texte + 'Calculer $%s$ et $%s$, ' % tuple(liste[8:10])
    texte = texte + 'arrondies au %s}\n' % arrondi
    return texte


def tex_resolution_thales0(n, v):
    return u"""Dans le triangle $%s$,~ $%s$ est sur le côté $[%s]$,~
$%s$ est sur le côté $[%s]$ et les droites $(%s)$ et $(%s)$ sont
parallèles.\\par
D'après le \\textbf{théorème de Thalès} :
$\\qquad\\mathbf{\\cfrac{%s}{%s}=\\cfrac{%s}{%s}=\\cfrac{%s}{%s}}$""" % \
           (
               n[0] + n[1] + n[2],
               n[3],
               n[0] + n[1],
               n[4],
               n[0] + n[2],
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
        return '\\vspace{1ex}\\par De plus $%s=%s%s%s=\\unit[%s]{cm}$\n' % donnees
    else:
        return ''


def tex_resolution_thales2(n, v):
    donnees = []
    for i in range(3):
        if v[i]:
            donnees.append(nombre(v[i]))
        else:
            donnees.append(creer_noms(n, i))
        if v[i + 3]:
            donnees.append(nombre(v[i + 3]))
        else:
            donnees.append(creer_noms(n, i + 3))
    return '\\[\\frac{%s}{%s}=\\frac{%s}{%s}=\\frac{%s}{%s}\\]' % tuple(donnees)


def nom_ou_valeur(n, v, i):
    if v[i]:
        return nombre(v[i])
    else:
        return creer_noms(n, i)


def valeur_exacte(a, approx=3, unit=1):
    nb = nombre(a)
    if unit:
        if nb.count(',') and (len(nb) - nb.find(',')) - 1 > approx:
            return '\\simeq\\unit[' + nombre(round(a, approx)) + ']{cm}'
        else:
            return '=\\unit[' + nombre(a) + ']{cm}'
    else:
        if nb.count(',') and (len(nb) - nb.find(',')) - 1 > approx:
            return '\\simeq' + nombre(round(a, approx))
        else:
            return '=' + nombre(a)


def tex_resolution_thales3(n, v, arrondi):
    r = v[8][0][0] % 3  # grand rapport
    donnees = []
    for i in range(3):
        if i != r:
            donnees.extend([nom_ou_valeur(n, v, r), nom_ou_valeur(n, v, r + 3), nom_ou_valeur(n, v, i),
                            nom_ou_valeur(n, v, i + 3)])
            if v[i]:  # on cherche i+3
                donnees.extend([creer_noms(n, i + 3), nombre(v[i]), nombre(v[r + 3]), nombre(v[r]),
                                valeur_exacte(v[i] * v[r + 3] / v[r], approx=arrondi)])
            else:
                donnees.extend([creer_noms(n, i), nombre(v[i + 3]), nombre(v[r]), nombre(v[r + 3]),
                                valeur_exacte(v[r] * v[i + 3] / v[r + 3], approx=arrondi)])
    texte = \
        '$\\cfrac{%s}{%s}=\\cfrac{%s}{%s}\\quad$ donc $\\quad \\boxed{%s=\\cfrac{%s\\times %s}{%s}%s}$\\par\n ' % tuple(
            donnees[0:9])
    texte = texte + \
            '$\\cfrac{%s}{%s}=\\cfrac{%s}{%s}\\quad$ donc $\\quad\\boxed{%s=\\cfrac{%s\\times %s}{%s}%s}$\\par\n' % tuple(
        donnees[9:18])
    return texte


# def pyromax(a):
#    maxi = a[0]
#    for i in xrange(len(a)):
#        if a[i] > maxi:
#            maxi = a[i]
#    return maxi
#
#
# def pyromin(a):
#    mini = a[0]
#    for i in xrange(len(a)):
#        if a[i] < mini:
#            mini = a[i]
#    return mini


def fig_thales(noms, valeurs):
    v = test_valeurs_thales(valeurs[0:8], valeurs[8][0], valeurs[8][1])
    type_thales = valeurs[8][1]
    angle = Decimal(int(100 * acos((v[0] ** 2 + v[1] ** 2 - v[2] ** 2) / (2 * v[0] * v[1])) * 180 / pi)) / 100
    v = [int(v[i] * 100) / 100 for i in range(8)]
    mini_x = int(100 * min(0, v[1] * cos(float(angle) * pi / 180), v[3] * type_thales,
                           (v[4] * cos(float(angle) * pi / 180)) * type_thales)) / 100 - 1.5
    mini_y = int(100 * min(0, v[4] * sin(float(angle) * pi / 180) * type_thales)) / 100 - 1.5
    maxi_x = int(100 * max(v[0], v[1] * cos(float(angle) * pi / 180))) / 100 + 1.5
    maxi_y = int(100 * v[1] * sin(float(angle) * pi / 180)) / 100 + .5
    echelle = int(400 / max(abs(mini_x) + maxi_x, abs(mini_y) + maxi_y)) / 100
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
            - 45,
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
            - v[3],
            - v[4],
            angle,
        )


def tex_fig_thales(noms, valeurs):
    donnees = fig_thales(noms, valeurs)
    enonce = \
        '''\\figureadroite{
  \\psset{PointSymbol=none,unit=%s}
  \\begin{pspicture}(%s,%s)(%s,%s)
    \\SpecialCoor
    \\pstTriangle[PosAngleA=%s,PosAngleB=-45,PosAngleC=%s,PointNameA=%s,
      PointNameB=%s,PointNameC=%s](0,0){a}(%s,0){b}(%s;%s){c}
    \\pstTriangle[PosAngleB=%s,PosAngleC=%s,PointSymbolA=none,
      PointName=none,PointNameB=%s,PointNameC=%s](0,0){a}(%s,0){b}(%s;%s){c}
  \\end{pspicture}
}''' % \
        donnees
    return enonce


#
# ------------------- TRIGONOMETRIE -------------------
#


def _exo_trigo():
    exo = ["\\exercice"]
    cor = ["\\exercice*"]
    s = choix_points(6)
    n1 = cotes_sommets(s[0:3])
    n2 = cotes_sommets(s[3:6])
    v = valeurs_trigo()
    (l1, l2) = enonce_trigo(((s[0:3], n1, v[0]), (s[3:6], n2, v[1])))
    exo.extend(l1)
    cor.extend(l2)
    return (exo, cor)

class exo_trigo(LegacyExercise):
    """Cosinus d\'un angle aigu"""

    tags = ["quatrième"]
    function = _exo_trigo


def enonce_trigo(v):
    (exo, cor) = ([], [])
    (l, lt) = ([], [])
    for j in range(2):
        f = (('\\sin', 1, 0), ('\\cos', 2, 0), ('\\tan', 1, 2))[v[j][2][0]]
        for i in range(2):
            l.append(v[j][1][f[i + 1]])
            l.append(v[j][2][i + 1])
        l.append(angle(v[j][0], 1))
        l.append(v[j][2][3])
    for j in range(2):
        tmp = []
        for i in range(3):
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
    exo.append('\\begin{multicols}{2}')
    exo.append('\\begin{enumerate}')
    cor.append('\\begin{multicols}{2}')
    cor.append('\\begin{enumerate}')
    arrondi = random.randrange(1, 4)
    text_arrondi = ['dix', 'cent', 'mill'][arrondi - 1] + u'ième'
    tr = nom_triangle(v[0][0])
    exo.append('\\item $%s$ est un triangle rectangle en $%s$ tel que :\\par' %
               (tr, v[0][0][0]))
    exo.append('%s et %s.\\par\nCalculer %s, arrondie au %s.\\par' % tuple(lt[0:3] + [text_arrondi]))
    cor.append('\\item $%s$ est un triangle rectangle en $%s$ tel que :\\par' %
               (tr, v[0][0][0]))
    cor.append('%s et %s.\\par\nCalculer %s, arrondie au %s.\\par' % tuple(lt[0:3] + [text_arrondi]))
    cor.append('Dans le triangle $%s$ rectangle en $%s$,' % (tr, v[0][0][0]))  # résolution
    v2 = (v[0][1], v[0][2])
    l2 = l[0:6]
    cor.extend(resolution_trigo(v2, l2, arrondi))
    tr = nom_triangle(v[1][0])
    exo.append('\\columnbreak')
    cor.append('\\columnbreak')
    arrondi = random.randrange(1, 4)
    text_arrondi = ['dix', 'cent', 'mill'][arrondi - 1] + u'ième'
    exo.append('\\item $%s$ est un triangle rectangle en $%s$ tel que :\\par' %
               (tr, v[1][0][0]))
    exo.append('''%s et %s.\\par
Calculer %s, arrondie au %s.\\par''' %
               tuple(lt[3:6] + [text_arrondi]))
    cor.append('\\item $%s$ est un triangle rectangle en $%s$ tel que :\\par' %
               (tr, v[1][0][0]))
    cor.append('%s et %s.\\par\nCalculer %s, arrondie au %s.\\par' % tuple(lt[3:6] + [text_arrondi]))
    #    cor.append("""\\dotfill{}\\par\\vspace{2ex}")
    cor.append('Dans le triangle $%s$ rectangle en $%s$,' % (tr, v[1][0][0]))  # résolution
    v2 = (v[1][1], v[1][2])
    l2 = l[6:12]
    cor.extend(resolution_trigo(v2, l2, arrondi))
    exo.append('\\end{enumerate}')
    exo.append('\\end{multicols}')
    cor.append('\\end{enumerate}')
    cor.append('\\end{multicols}')
    return (exo, cor)


def resolution_trigo(v2, l2, arrondi):
    cor = []
    f = (('\\sin', 1, 0), ('\\cos', 2, 0), ('\\tan', 1, 2))[v2[1][0]]
    cor.append('\\[ %s%s=\\cfrac{%s}{%s} \\]' % (f[0], l2[4], v2[0][f[1]],
                                                 v2[0][f[2]]))
    if not v2[1][3]:
        cor.append('\\[ %s%s=\\cfrac{%s}{%s} \\]' % (f[0], l2[4],
                                                     nombre(v2[1][1]), nombre(v2[1][2])))
        if f[0] == '\\sin':
            r = asin(v2[1][1] / v2[1][2]) * 180 / pi
        elif f[0] == '\\cos':
            r = acos(v2[1][1] / v2[1][2]) * 180 / pi
        else:
            r = atan(v2[1][1] / v2[1][2]) * 180 / pi
        cor.append(r'\[ \boxed{%s=%s^{-1}\left(\cfrac{%s}{%s}\right) %s\degres} \]' %
                   (l2[4], f[0], nombre(v2[1][1]), nombre(v2[1][2]),
                    valeur_exacte(r, approx=arrondi, unit=0)))
    elif not v2[1][1]:
        cor.append('\\[ %s%s=\\cfrac{%s}{%s} \\]' % (f[0], v2[1][3],
                                                     v2[0][f[1]], nombre(v2[1][2])))
        if f[0] == '\\sin':
            r = sin(v2[1][3] * pi / 180)
        elif f[0] == '\\cos':
            r = cos(v2[1][3] * pi / 180)
        else:
            r = tan(v2[1][3] * pi / 180)
        r = r * v2[1][2]
        cor.append(r'\[ \boxed{%s=%s%s\times %s %s} \]' %
                   (v2[0][f[1]], f[0], v2[1][3], nombre(v2[1][2]),
                    valeur_exacte(r, approx=arrondi)))
    else:
        cor.append('\\[ %s%s=\\cfrac{%s}{%s} \\]' % (f[0], v2[1][3],
                                                     nombre(v2[1][1]), v2[0][f[2]]))
        if f[0] == '\\sin':
            r = sin(v2[1][3] * pi / 180)
        elif f[0] == '\\cos':
            r = cos(v2[1][3] * pi / 180)
        else:
            r = tan(v2[1][3] * pi / 180)
        r = v2[1][1] / r
        cor.append(r'\[ \boxed{%s=\cfrac{%s}{%s%s} %s} \]' %
                   (v2[0][f[2]], nombre(v2[1][1]), f[0], v2[1][3],
                    valeur_exacte(r, approx=arrondi)))
    return cor


def angle(s,
          n):  # renvoie \\widehat{ABC} où s est la liste des 3 sommets du triangle et n est le rang du sommet de l'angle dans cette liste
    return '\\widehat{%s%s%s}' % (s[(n + 2) % 3], s[n], s[(n + 1) % 3])


def valeurs_trigo():
    l = [random.randrange(10, 121) / 10 for dummy in range(3)]
    l.sort()
    l.append(random.randrange(15, 76))
    trigo = 1
    if random.randrange(2):  # on choisit en 1er une longueur et un angle
        if random.randrange(2):  # on connait la première des deux longueurs
            v = (trigo, l[0], 0, l[3])
        else:
            v = (trigo, 0, l[0], l[3])
        v = (v, (trigo, l[1], l[2], 0))
    else:

        # on choisit en 1er deux longueurs

        v = (trigo, l[1], l[2], 0)
        if random.randrange(2):  # on connait la première des deux longueurs
            v = (v, (trigo, l[0], 0, l[3]))
        else:
            v = (v, (trigo, 0, l[0], l[3]))
    return v

# TODO: utils/pyromaths-cli.py generate exo_thales:1 plante sur l'arcos (ligne 605)
