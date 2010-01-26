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
