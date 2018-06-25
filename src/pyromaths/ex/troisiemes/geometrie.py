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
from builtins import str
from builtins import range
from past.utils import old_div
import random
from math import acos, asin, atan, pi, sin, cos, tan

from . import fractions
from pyromaths.outils.Arithmetique import valeur_alea, pgcd
from pyromaths.outils.Geometrie import choix_points
#---------------------------------------------------------------------
# -                    THÉORÈME DE THALÈS                             -
#---------------------------------------------------------------------
def cotes_sommets(noms):  # renvoie les noms des 3 cotes du triangle en finissant par l'hypotenuse
    return (noms[1] + noms[2], noms[0] + noms[2], noms[0] + noms[1])

def nom_triangle(noms):  # renvoie le nom du triangle dans un ordre aleatoire
    a = random.randrange(3)
    b = (random.randrange(2) + 1 + a) % 3
    c = (3 - a) - b
    return '%s%s%s' % (noms[a], noms[b], noms[c])

def valeurs_thales(valeurmax, typeexo):
    """typeexo est égal à 1 pour la version triangle, -1 pour la version papillon"""
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
            valeurs[i] = old_div(random.randrange(15, valeurmax), 10.0)
        if liste[i + 3] and liste[i]:
            valeurs[i + 3] = old_div(random.randrange(5, valeurs[i] * 10 - 9), \
                10.0)
        elif liste[i + 3]:
            valeurs[i + 3] = old_div(random.randrange(5, valeurmax), 10.0)
    if liste[6]:
        valeurs[6] = old_div(random.randrange(5, valeurmax), 10.0)
    if liste[7]:
        valeurs[7] = old_div(random.randrange(5, valeurmax), 10.0)

    valeurs.append((rapport, typeexo))
    if test_valeurs_thales(valeurs, rapport, typeexo):
        return valeurs
    else:
        return 0


def test_valeurs_thales(valeurs, rapport, type_thales):
    v = [valeurs[i] for i in range(8)]
    if rapport[0] // 3 == 0 and rapport[1] // 3 == 2:  # On donne AB et EB
        v[rapport[0] + 3] = (v[rapport[0]] - v[rapport[1]]) * \
            type_thales
    elif rapport[0] // 3 == 1 and rapport[1] // 3 == 2:

                                                # On donne AE et EB

        v[rapport[0] - 3] = v[rapport[0]] * type_thales + v[rapport[1]]
    if v[rapport[0] % 3]:  # rapport est AE/AB
        rapp = old_div((v[rapport[0] % 3 + 3] * 1.0), v[rapport[0] % 3])
    else:
        rapp = 0
    for i in range(3):
        if not v[i] and rapp:
            v[i] = old_div(v[i + 3], rapp)
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


def thales(exo, cor):
    typeexo = [-1, 1]
    random.shuffle(typeexo)
    for i in range(2):
        arrondi = random.randrange(1, 4)
        text_arrondi = ['dix', 'cent', 'mill'][arrondi - 1] + u'ième'
        noms = choix_points(5)  # les noms des sommets
        while True:
            valeurs = valeurs_thales(70, typeexo[i])  # les longueurs en mm
            if valeurs:
                break
        exo.append(r"\figureadroite{%")
        cor.append(r"\figureadroite{%")
        exo.append(tex_fig_thales(noms, valeurs))
        cor.append(tex_fig_thales(noms, valeurs))
        exo.append("}{%")
        cor.append("}{%")
        exo.append(tex_enonce_thales(noms, valeurs, text_arrondi))
        cor.append(tex_enonce_thales(noms, valeurs, text_arrondi))
        exo.append(r"}\par")
        cor.append(r"}\par")
        cor.append(tex_resolution_thales0(noms))
        cor.append(tex_resolution_thales1(noms, valeurs))
        cor.append(tex_resolution_thales2(noms, valeurs))
        cor.append(tex_resolution_thales3(noms, valeurs, arrondi))

def long_val(noms, valeurs):  # renvoie un tuple contenant les noms des segments et leur longueur puis les noms des longueurs a calculer
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


def tex_enonce_thales(noms, valeurs, text_arrondi):
    texte = \
            u'Sur la figure ci-contre, les droites $(%s)\\text{ et }(%s)$ sont parallèles.\\par\n' % \
        (lAB(noms[1:3]), lAB(noms[3:5]))
    liste = long_val(noms, valeurs)
    texte += \
        'On donne $%s=\\unit[%s]{cm}$ \\quad $%s=\\unit[%s]{cm}$ \\quad $%s=\\unit[%s]{cm}$ \\quad $%s~=~\\unit[%s]{cm}$.\\par\n' % \
        tuple(liste[0:8])
    texte += 'Calculer $%s$ et $%s$, ' % tuple(liste[8:10])
    texte += u'arrondies au %s.' % text_arrondi
    return texte


def tex_resolution_thales0(n):
    return u"""Les points $%s$, $%s$, $%s$ et $%s$, $%s$, $%s$ sont alignés et les droites $(%s)$ et $(%s)$ sont parallèles.\\par
D'après le \\textbf{théorème de Thalès} : $\\quad\\mathbf{\\cfrac{%s}{%s}=\\cfrac{%s}{%s}=\\cfrac{%s}{%s}}$""" % \
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
        return u'\\par\\medskip\nDe plus $%s=%s%s%s=\\unit[%s]{cm}$, d\'où' % \
            donnees
    else:
        return u'\\quad d\'où'


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
    return '$\\cfrac{%s}{%s}=\\cfrac{%s}{%s}=\\cfrac{%s}{%s}$\\par' % \
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
            donnees.extend([nom_ou_valeur(n, v, r), nom_ou_valeur(n, v,
                           r + 3), nom_ou_valeur(n, v, i), nom_ou_valeur(n,
                           v, i + 3)])
            if v[i]:  # on cherche i+3
                donnees.extend([creer_noms(n, i + 3), nombre(v[i]),
                               nombre(v[r + 3]), nombre(v[r]),
                               valeur_exacte(old_div(((v[i] * 1.0) * v[r + 3]),
                               v[r]), approx=arrondi)])
            else:
                donnees.extend([creer_noms(n, i), nombre(v[i + 3]),
                               nombre(v[r]), nombre(v[r + 3]),
                               valeur_exacte(old_div(((v[r] * 1.0) * v[i + 3]),
                               v[r + 3]), approx=arrondi)])
    texte = \
        '$\\cfrac{%s}{%s}=\\cfrac{%s}{%s}\\quad$ donc $\\boxed{%s=\\cfrac{%s\\times %s}{%s}%s}$\\hfill' % \
        tuple(donnees[0:9])
    texte = texte + \
        '$\\cfrac{%s}{%s}=\\cfrac{%s}{%s}\\quad$ donc $\\boxed{%s=\\cfrac{%s\\times %s}{%s}%s}$\\par\n' % \
        tuple(donnees[9:18])
    return texte



def fig_thales(noms, valeurs):
    v = test_valeurs_thales(valeurs[0:8], valeurs[8][0], valeurs[8][1])
    type_thales = valeurs[8][1]
    angle = old_div(int(old_div(((100.0 * acos(old_div(((v[0] ** 2 + v[1] ** 2) - v[2] ** 2), ((2 *
                v[0]) * v[1])))) * 180), pi)), 100.0)
    v = [old_div(int(v[i] * 100), 100.0) for i in range(8)]
    mini_x = old_div(int(100.0 * min(0, v[1] * cos(old_div((angle * pi), 180)), v[3] *
                 type_thales, (v[4] * cos(old_div((angle * pi), 180))) *
                 type_thales)), 100.0) - 1.5
    mini_y = old_div(int(100.0 * min(0, (v[4] * sin(old_div((angle * pi), 180))) *
                 type_thales)), 100.0) - 1.5
    maxi_x = old_div(int(100.0 * max(v[0], v[1] * cos(old_div((angle * pi), 180)))), \
        100.0) + 1.5
    maxi_y = old_div(int((100.0 * v[1]) * sin(old_div((angle * pi), 180))), 100.0) + .5
    echelle = old_div(int(old_div(400, max(abs(mini_x) + maxi_x, abs(mini_y) + maxi_y))), \
        100.0)
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
        '''\\psset{PointSymbol=none,unit=%s}
\\begin{pspicture}(%s,%s)(%s,%s)
\\SpecialCoor
\\pstTriangle[PosAngleA=%s, PosAngleB=-45, PosAngleC=%s, PointNameA=%s, PointNameB=%s, PointNameC=%s](0,0){a}(%s,0){b}(%s;%s){c}
\\pstTriangle[PosAngleB=%s, PosAngleC=%s, PointSymbolA=none, PointNameA=none, PointNameB=%s, PointNameC=%s](0,0){a}(%s,0){b}(%s;%s){c}
\\end{pspicture}''' % donnees
    return enonce


def tex_thales():
    exo = ['\\exercice']
    cor = ['\\exercice*']
    thales(exo, cor)
    return (exo, cor)

tex_thales.description = u'Théorème de Thalès'


#
# ------------------- RECIPROQUE DU THEOREME DE THALES -------------------
#


def valeurs_reciproque_thales():
    while True:
        (a, b, c, d) = (random.randrange(2, 50), random.randrange(2, 50),
                        random.randrange(2, 20), random.randrange(2, 20))
        p1 = pgcd(a, b)
        (a, b) = (old_div(a, p1), old_div(b, p1))
        if c < d:
            (c, d) = (d, c)
        if a != b and int(old_div(c, d)) != old_div((c * 1.0), d) and 10 < a * c < 200 and \
            10 < a * d < 200 and 10 < b * c < 200 and 10 < b * d < 200 and \
            .3 < old_div((d * 1.0), c) < .7:
            break
    t = valeur_alea(-1, 1)  # -1 si papillon, 1 si triangle
    r = random.randrange(5)
    while r == 2:
        r = random.randrange(5)
    angle = random.randrange(15, 105)
    valeurs = (
        old_div((a * c), 10.0),
        old_div((b * c), 10.0),
        0,
        old_div((a * d), 10.0),
        old_div((b * d), 10.0),
        0,
        old_div((a * c - (t * a) * d), 10.0),
        old_div((b * c - (t * b) * d), 10.0),
        angle,
        t,
        r,
        )
    return valeurs


def fig_rec_thales(noms, v):
    type_thales = v[9]
    angle = v[8]
    mini_x = old_div(int(100.0 * min(0, v[1] * cos(old_div((angle * pi), 180)), v[3] *
                 type_thales, (v[4] * cos(old_div((angle * pi), 180))) *
                 type_thales)), 100.0) - 1.5
    mini_y = old_div(int(100.0 * min(0, (v[4] * sin(old_div((angle * pi), 180))) *
                 type_thales)), 100.0) - 1.5
    maxi_x = old_div(int(100.0 * max(v[0], v[1] * cos(old_div((angle * pi), 180)))), \
        100.0) + 1.5
    maxi_y = old_div(int((100.0 * v[1]) * sin(old_div((angle * pi), 180))), 100.0) + .5
    echelle = old_div(int(old_div(400, max(abs(mini_x) + maxi_x, abs(mini_y) + maxi_y))), \
        100.0)
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


def tex_fig_rec_thales(noms, valeurs):
    donnees = fig_rec_thales(noms, valeurs)
    enonce = \
        '''{\\begin{wrapfigure}{r}{4cm}
\\psset{PointSymbol=none,unit=%s}
\\begin{pspicture}(%s,%s)(%s,%s)
\\SpecialCoor
\\pstTriangle[PosAngleA=%s,PosAngleB=-45,PosAngleC=%s,PointNameA=%s,PointNameB=%s,PointNameC=%s](0,0){a}(%s,0){b}(%s;%s){c}
\\pstTriangle[PosAngleB=%s,PosAngleC=%s,PointSymbolA=none,PointNameA=none,PointNameB=%s,PointNameC=%s](0,0){a}(%s,0){b}(%s;%s){c}
\\end{pspicture}
\\end{wrapfigure}\\par
''' % \
        donnees
    return enonce


def rec_thales(exo, cor):
    noms = choix_points(5)  # les noms des sommets
    valeurs = valeurs_reciproque_thales()
    exo.append(tex_fig_rec_thales(noms, valeurs))
    exo.append(tex_enonce_rec_thales(noms, valeurs) + '\\vspace{2cm}}')  # le dernier '}' ferme le bloc exercice
    cor.append(tex_fig_rec_thales(noms, valeurs))
    cor.append(tex_enonce_rec_thales(noms, valeurs) +
             "\\par\\dotfill{}\\\\}\n")
    cor.append(tex_resolution_rec_thales0(noms, valeurs))
    cor.append(tex_resolution_rec_thales1(noms, valeurs))


    #  cor.append(tex_resolution_rec_thales2(noms, valeurs))
    # cor.append(tex_resolution_rec_thales3(noms, valeurs))


def enonce_rec_thales(n, v):
    (r, l) = (v[10], [])
    for i in range(5):
        if i != 2:
            if i == r:
                l.extend([creer_noms(n, 6 + i % 3), nombre(v[6 + i % 3])])
            else:
                l.extend([creer_noms(n, i), nombre(v[i])])
    l1 = [i for i in range(4)]
    l2 = []
    for i in range(4):
        a = l1.pop(random.randrange(4 - i))
        l2.extend([l[2 * a], l[2 * a + 1]])
    l2.extend([creer_noms(n, 2), creer_noms(n, 5)])
    return tuple(l2)


def tex_enonce_rec_thales(n, v):
    d = enonce_rec_thales(n, v)
    texte = \
        u'''Sur la figure ci-contre, on donne $%s=\\unit[%s]{cm}$, $%s=\\unit[%s]{cm}$, $%s=\\unit[%s]{cm}$ et $%s=\\unit[%s]{cm}$.\\par
Démontrer que les droites $(%s)$ et $(%s)$ sont parallèles.
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
    return u"""Les points $%s$, $%s$, $%s$ et $%s$, $%s$, $%s$ sont alignés dans le même ordre.\\par
De plus $%s=%s%s%s=\\unit[%s]{cm}$.\\par
""" % \
        resolution_rec_thales0(n, v)


def resolution_rec_thales1(n, v):
    (d, t) = ([], '')
    for i in range(2):
        d.extend([creer_noms(n, i), creer_noms(n, i + 3), nombre(v[i]),
                 nombre(v[i + 3])])
        if valeur_exacte(old_div(v[i], v[i + 3]), approx=5).count('='):
            d.append(valeur_exacte(old_div(v[i], v[i + 3]), approx=5, unit=0))
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
    return u"""$\\left.
\\renewcommand{\\arraystretch}{2}
\\begin{array}{l}
\\bullet\\cfrac{%s}{%s}=\\cfrac{%s}{%s}%s\\\\\n    \\bullet\\cfrac{%s}{%s}=\\cfrac{%s}{%s}%s
\\end{array}
\\right\\rbrace$
Donc $\\cfrac{%s}{%s}=\\cfrac{%s}{%s}$\\,.\\par
D'après la \\textbf{réciproque du théorème de Thalès}, \\fbox{les droites $(%s)$ et $(%s)$ sont parallèles.}
""" % \
        d

def tex_reciproque_thales():
    exo = ['\\exercice']
    cor = ['\\exercice*']
    rec_thales(exo, cor)
    return (exo, cor)

tex_reciproque_thales.description = u'Réciproque du théorème de Thalès'


#
# ------------------- TRIGONOMETRIE -------------------
#


def trigo_init(exo, cor):
    s = choix_points(6)
    n1 = cotes_sommets(s[0:3])
    n2 = cotes_sommets(s[3:6])
    v = valeurs_trigo()
    enonce_trigo(exo, cor, ((s[0:3], n1, v[0]), (s[3:6], n2, v[1])))


def enonce_trigo(exo, cor, v):
    (l, lt) = ([], [])
    arrondi = random.randrange(1, 4)
    text_arrondi = ['dix', 'cent', 'mill'][arrondi - 1] + u'ième'
    for j in range(2):
        f = (('\\sin', 1, 0), ('\\cos', 2, 0), ('\\tan', 1, 2))[v[j][2][0]]
        for i in range(2):
            l.append(v[j][1][f[i + 1]])
            l.append(v[j][2][i + 1])
        l.append(tex_angle(v[j][0], 1))
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
    tr = nom_triangle(v[0][0])
    exo.append('\\item $%s$ est un triangle rectangle en $%s$ tel que :\\par ' %
             (tr, v[0][0][0]))
    exo.append('%s et %s.\\par\nCalculer %s, arrondie au %s.\\par' % tuple(lt[0:3] + [text_arrondi]))
    cor.append('\\item $%s$ est un triangle rectangle en $%s$ tel que :\\par ' %
             (tr, v[0][0][0]))
    cor.append('%s et %s.\\par\nCalculer %s, arrondie au %s.\\par' % tuple(lt[0:3] + [text_arrondi]))
    cor.append("\\dotfill{}\\par\\vspace{2ex}")
    cor.append('Dans le triangle $%s$ rectangle en $%s$,' % (tr, v[0][0][0]))  # résolution
    v2 = (v[0][1], v[0][2])
    l2 = l[0:6]
    resolution_trigo(cor, v2, l2, arrondi)
    tr = nom_triangle(v[1][0])
    exo.append('\\columnbreak')
    cor.append('\\columnbreak')
    arrondi = random.randrange(1, 4)
    text_arrondi = ['dix', 'cent', 'mill'][arrondi - 1] + u'ième'
    exo.append('\\item $%s$ est un triangle rectangle en $%s$ tel que :\\par' %
             (tr, v[1][0][0]))
    exo.append('%s et %s.\\par\nCalculer %s, arrondie au %s.\\par' % tuple(lt[3:6] + [text_arrondi]))
    cor.append('\\item $%s$ est un triangle rectangle en $%s$ tel que :\\par' %
             (tr, v[1][0][0]))
    cor.append('%s et %s.\\par\nCalculer %s, arrondie au %s.\\par' % tuple(lt[3:6] + [text_arrondi]))
    cor.append("\\dotfill{}\\par\\vspace{2ex}")
    cor.append('Dans le triangle $%s$ rectangle en $%s$,' % (tr, v[1][0][0]))  # résolution
    v2 = (v[1][1], v[1][2])
    l2 = l[6:12]
    resolution_trigo(cor, v2, l2, arrondi)
    exo.append('\\end{enumerate}')
    exo.append('\\end{multicols}')
    cor.append('\\end{enumerate}')
    cor.append('\\end{multicols}')


def resolution_trigo(cor, v2, l2, arrondi):
    f = (('\\sin', 1, 0), ('\\cos', 2, 0), ('\\tan', 1, 2))[v2[1][0]]
    cor.append(u'\\[%s%s=\\cfrac{%s}{%s}' % (f[0], l2[4], v2[0][f[1]], v2[0][f[2]]) + '\\] ')
    if not v2[1][3]:
        cor.append(u'\\[ %s%s=\\cfrac{%s}{%s}' % (f[0], l2[4], nombre(v2[1][1]),
                  nombre(v2[1][2])) + '\\] ')
        if f[0] == '\\sin':
            r = old_div((asin(old_div(v2[1][1], v2[1][2])) * 180), pi)
        elif f[0] == '\\cos':
            r = old_div((acos(old_div(v2[1][1], v2[1][2])) * 180), pi)
        else:
            r = old_div((atan(old_div(v2[1][1], v2[1][2])) * 180), pi)
        cor.append(r'\[ \boxed{%s=%s^{-1}\left(\cfrac{%s}{%s}\right) %s\degres} \]' %
                  (l2[4], f[0], nombre(v2[1][1]), v2[1][2], valeur_exacte(r, approx=arrondi, unit=0)))
    elif not v2[1][1]:
        cor.append(u'\\[ %s%s=\\cfrac{%s}{%s}' % (f[0], v2[1][3], v2[0][f[1]],
                  nombre(v2[1][2])) + '\\] ')
        if f[0] == '\\sin':
            r = sin(old_div((v2[1][3] * pi), 180))
        elif f[0] == '\\cos':
            r = cos(old_div((v2[1][3] * pi), 180))
        else:
            r = tan(old_div((v2[1][3] * pi), 180))
        r = r * v2[1][2]
        cor.append(r'\[ \boxed{%s=%s%s\times %s %s } \]' % (v2[0][f[1]],
                  f[0], v2[1][3], nombre(v2[1][2]), valeur_exacte(r, approx=arrondi)))
    else:
        cor.append(u'\\[ %s%s=\\cfrac{%s}{%s}' % (f[0], v2[1][3], nombre(v2[1][1]),
                  v2[0][f[2]]) + '\\] ')
        if f[0] == '\\sin':
            r = sin(old_div((v2[1][3] * pi), 180))
        elif f[0] == '\\cos':
            r = cos(old_div((v2[1][3] * pi), 180))
        else:
            r = tan(old_div((v2[1][3] * pi), 180))
        r = old_div(v2[1][1], r)
        cor.append(r'\[ \boxed{%s=\cfrac{%s}{%s%s} %s} \]' % (v2[0][f[2]],
                  nombre(v2[1][1]), f[0], v2[1][3], valeur_exacte(r, approx=arrondi)))


def tex_angle(s, n):  # renvoie \\widehat{ABC} où s est la liste des 3 sommets du triangle et n est le rang du sommet de l'angle dans cette liste
    return '\\widehat{%s%s%s}' % (s[(n + 2) % 3], s[n], s[(n + 1) % 3])


def valeurs_trigo():
    l = [old_div(random.randrange(10, 121), 10.0) for i in range(3)]
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

def tex_trigo():
    exo = ['\\exercice']
    cor = ['\\exercice*']
    trigo_init(exo, cor)
    return (exo, cor)

tex_trigo.description = u'Trigonométrie'
