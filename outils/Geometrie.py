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

from random import randrange
def choix_points(n):
    """
    choisit n points parmi A, B, C, ..., Z
    @param n: nombre de points \xc3\xa0 choisir
    @type n: integer
    """
    points = [chr(i + 65) for i in range(26)]
    liste = []
    for i in range(n):
        liste.append(points.pop(randrange(len(points))))
    return liste

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

def trouve_couples_pythagore(max):
    ls = []
    for i in xrange(26):
        for j in xrange(i-1):
            a = i
            b = j+1
            for k in xrange(140):
                x = (2*k+1)*(a**2-b**2)
                y = (2*k+1)*(2*a*b)
                z = (2*k+1)*(a**2+b**2)
                if z > max:
                    break
                ls.append(tuple(sorted([x,y,z])))
    ls.sort(key = operator.itemgetter(2))
    cpt = 1
    while cpt < len(ls):
        if ls[cpt]==ls[cpt-1]:
            ls.pop(cpt)
        else:
            cpt += 1
    return tuple(ls)

#----------------------------------------------------
# Cotation des longeurs sur une figure psTricks
# A, B sont les coordonnées de deux points
# cotation_h écrit au dessus du segment
#----------------------------------------------------

def cotation(A,B,longueur,couleur="",unite="cm"):
    (xA,yA)=A
    (xB,yB)=B
    if couleur!="":
        couleur="\\color{%s}"%couleur
    return u"\\pcline[linestyle=none](%s,%s)(%s,%s)  \\bput{:U}{%s\\unit[%s]{%s}}" %(xA,yA,xB,yB,couleur,longueur,unite)

def cotation_h(A,B,longueur,couleur="",unite="cm"):
    (xA,yA)=A
    (xB,yB)=B
    if couleur!="":
        couleur="\\color{%s}"%couleur
    return u"\\pcline[linestyle=none](%s,%s)(%s,%s)  \\aput{:U}{%s\\unit[%s]{%s}}" %(xA,yA,xB,yB,couleur,longueur,unite)

#def trouve_couples_pythagore(valeurmax):
#    (liste, listecouples) = ([], [])
#    for a in range(valeurmax):
#        liste.append(a ** 2)
#    for c in range(valeurmax):
#        for b in range(int((c + 1) / 2 ** .5)):
#            if liste.count((c + 1) ** 2 - (b + 1) ** 2):
#                a = liste.index((c + 1) ** 2 - (b + 1) ** 2)
#                listeinter = [c + 1, b + 1, a]
#                listeinter.sort()
#                if listeinter[0] > 9:
#                    listecouples.append(tuple(listeinter))
#
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
#
#    return tuple(listecouples)
class Metapost:

    def __init__(self):
        self.text = []
        self.num = 1

    def fin(self):
        self.text.append("end;")
        return self

    def triangle(
        self,
        A,
        B,
        C,
        a=0,
        b=0,
        c=0,
        alpha=0,
        beta=0,
        gamma=0,
        rotation=0,
        angledroit=0,
        ):
        """Construit un triangle en metapost quelles que soient les données.
        La base est le côté [AB] de longueur c.

        @param A, b, C : nom des trois sommets (obligatoire)
        @param a, b, c : longueurs des trois côtés opposés au sommet de même nom
        @param alpha, beta, gamma : mesure des 3 angles de sommets A, B et C
        @param rotation: mesure en degrés de l'angle de la rotation de centre A
                         appliquée au triangle
        @param angledroit: doit-on afficher l'angle droit ?
        """

        self.text.append("beginfig(%s);\n" % self.num)
        self.text.append("u:=1cm;\n")
        self.text.append("pair %s, %s, %s, m[];\n" % (A, B, C))
        self.text.append("picture $;\n")
        self.text.append("  %s=origin;\n" % A)
        if angledroit:
            marques=[0, 0, 0, "%s \degres" % alpha, "%s \degres" % beta, "%s \degres" % gamma]
            if a: marques[0]="%s cm" % a
            if b: marques[1]="%s cm" % b
            if c: marques[2]="%s cm" % c
            points=[A, B, C]
        #on donne les trois longueurs des 3 côtés

        if a and b and c:
            alpha = degres(math.acos(((b ** 2 + c ** 2) - a ** 2 * 1.) / ((2 *
                     b) * c)))
            beta = degres(math.acos(((c ** 2 + a ** 2) - b ** 2 * 1.) / ((2 *
                    c) * a)))
        elif a and b and gamma:

        # Un angle et les deux côtés adjacents

            (c, beta, alpha) = self.triangle_angle_cotes_adjacents(a, b,
                    gamma)
        elif b and c and alpha:
            (a, gamma, beta) = self.triangle_angle_cotes_adjacents(b, c,
                    alpha)
        elif c and a and beta:
            (b, alpha, gamma) = self.triangle_angle_cotes_adjacents(c, a,
                    beta)
        elif b and c and beta:

        # Un angle, le côté opposé et un côté adjacent

            (a, alpha, gamma) = self.triangle_angle_cote_adjacent_cote_oppose(b,
                    c, beta)
        elif b and a and beta:
            (c, gamma, alpha) = self.triangle_angle_cote_adjacent_cote_oppose(b,
                    a, beta)
        elif a and b and alpha:
            (c, gamma, beta) = self.triangle_angle_cote_adjacent_cote_oppose(a,
                    b, alpha)
        elif a and c and alpha:
            (b, beta, gamma) = self.triangle_angle_cote_adjacent_cote_oppose(a,
                    c, alpha)
        elif c and a and gamma:
            (b, beta, alpha) = self.triangle_angle_cote_adjacent_cote_oppose(c,
                    a, gamma)
        elif c and b and gamma:
            (a, alpha, beta) = self.triangle_angle_cote_adjacent_cote_oppose(c,
                    b, gamma)
        elif alpha and beta and c:

        # Deux angles et le côté commun

            pass  # on sait faire
        elif beta and gamma and a:
            c = (a * math.sin((gamma * math.pi) / 180)) / math.sin(((beta +
                    gamma) * math.pi) / 180)
            alpha = (180 - beta) - gamma
        elif alpha and gamma and b:
            c = (b * math.sin((gamma * math.pi) / 180)) / math.sin(((alpha +
                    gamma) * math.pi) / 180)
            beta = (180 - alpha) - gamma
        elif a and alpha and beta:

        # Deux angles et un côté non commun

            c = (a * math.sin(((alpha + beta) * math.pi) / 180)) / math.sin((alpha *
                    math.pi) / 180)
        elif a and alpha and gamma:
            c = (a * math.sin((gamma * math.pi) / 180)) / math.sin((alpha *
                    math.pi) / 180)
            beta = (180 - alpha) - gamma
        elif b and beta and alpha:
            c = (b * math.sin(((alpha + beta) * math.pi) / 180)) / math.sin((beta *
                    math.pi) / 180)
        elif b and beta and gamma:
            c = (b * math.sin((gamma * math.pi) / 180)) / math.sin((beta *
                    math.pi) / 180)
            alpha = (180 - beta) - gamma
        elif c and alpha and gamma:
            beta = (180 - alpha) - gamma
        elif c and beta and gamma:
            alpha = (180 - beta) - gamma
        alpha = alpha + rotation
        beta = beta - rotation


        self.text.append("  %s= (%s*u, 0) rotated %s;\n" % (B, c, rotation))
        self.text.append("  %s = %s + whatever*dir(%s);\n" % (C, A, alpha))
        self.text.append("  %s = %s + whatever*dir(180-%s);\n" % (C, B, beta))
        self.text.append("  draw %s -- %s -- %s -- cycle;\n" % (A, B, C))

        # Codage de l'angle droit s'il y en a un.

        if angledroit:
            if alpha - rotation == 90:
                self.text.append("  draw (%s+5*unitvector(%s-%s))--(%s+5*unitvector(%s-%s)+\n" % (A, B, A, A, B, A))
                self.text.append("      5*unitvector(%s-%s))--(%s+5*unitvector(%s-%s));\n" % ( C, A, A, C, A))
            elif beta + rotation == 90:
                self.text.append("  draw (%s+5*unitvector(%s-%s))--(%s+5*unitvector(%s-%s)+\n" % (B, A, B, B, A, B))
                self.text.append("      5*unitvector(%s-%s))--(%s+5*unitvector(%s-%s));\n" % (C, B, B, C, B))
            elif gamma == 90:
                self.text.append("  draw (%s+5*unitvector(%s-%s))--(%s+5*unitvector(%s-%s)+\n" % (C, A, C, C, A, C))
                self.text.append("      5*unitvector(%s-%s))--(%s+5*unitvector(%s-%s));\n" % ( B, C, C, B, C))
            for i in range(3):
                if marques[i]:
                    self.text.append("  m3:=unitvector(%s-%s) rotated 90;\n" % (points[(i+1)%3], points[(i+2)%3]))
                    self.text.append("  $:=image(\n")
                    self.text.append("    label(btex %s etex rotated angle(%s-%s),(%s+%s)/2+2mm*m3);\n" % (marques[i], points[(i+1)%3], points[(i+2)%3], points[(i+1)%3], points[(i+2)%3]))
                    self.text.append("    );\n  draw $;\n")
        self.text.append("  label.llft(btex $%s$ etex, %s);\n" % (A, A))
        self.text.append("  label.lrt(btex $%s$ etex, %s);\n" % (B, B))
        self.text.append("  label.top(btex $%s$ etex, %s);\n" % (C, C))
        self.text.append("""endfig;

""")
        self.num = self.num + 1
        return self

    def triangle_angle_cotes_adjacents(self, a, b, gamma):
        c = math.sqrt(a ** 2 + b ** 2 - 2 * a * b * math.cos(radians(gamma)))
        alpha = 90. - gamma / 2 + degres(math.atan((((a - b) * 1.) / (a + b)) /
                math.tan(radians(gamma / 2))))
        beta = 90. - gamma / 2 - degres(math.atan((a - b) * 1. / (a + b) /
                math.tan(radians(gamma / 2))))
        return (c, beta, alpha)

    def triangle_angle_cote_adjacent_cote_oppose(self, b, c, beta):
        if b <= c * math.sin((beta * math.pi) / 180):
            alpha = gamma = a = 0  # Pas possible de résoudre
        else:
            gamma = degres(math.asin(((c * math.sin((beta * math.pi) / 180)) /
                     b) * 1.))
            alpha = (180 - beta) - gamma
            a = math.sqrt(b ** 2 - c ** 2 * math.sin((beta * math.pi) /
                          180) ** 2) + c * math.cos((beta * math.pi) /
                    180)
        return (a, alpha, gamma)


#fig = Metapost()
#fig = Metapost.triangle(
    #fig, "A", "B",  "C", a=3, b=4.2, c=4.2, rotation=10, angledroit=1)
#fig = Metapost.triangle(
    #fig, "D", "E",  "F", a=4, b=5.7, c=6.5, rotation=90, angledroit=1)
#fig = Metapost.triangle(
    #fig, "G", "H",  "I", a=3.5, b=3.5, c=3.5, rotation=0, angledroit=1)
#fig = Metapost.triangle(
    #fig, "J", "K",  "L", a=4, b=4.5, c=4.5, rotation=30, angledroit=1)
#fig = Metapost.fin(fig)
#print string.join(fig.text, "")
