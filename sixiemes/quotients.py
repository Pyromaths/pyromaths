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


def valeurs_diviseurs():
    diviseurs = [2, 3, 5, 9, 10]
    liste = []
    for i in xrange(5):
        liste.append(diviseurs.pop(random.randrange(len(diviseurs))) *
                     random.randrange(11, 100))
    return liste


def liste_diviseurs(l):
    diviseurs = (2, 3, 5, 9, 10)
    reponse = []
    for i in xrange(len(l)):
        reponse.extend([[l[i]]])
        for j in xrange(len(diviseurs)):
            if l[i] % diviseurs[j]:  # n'est pas divisible
                reponse[i].append("$\\Square$")
            else:
                reponse[i].append("$\\CheckedBox$")
    return reponse


def tex_divisible(f0, f1):
    l = valeurs_diviseurs()
    reponse = liste_diviseurs(l)
    f0.write("""\\begin{tabular}{c@{ est divisible : \kern1cm}r@{ par 2\\kern1cm}r@{ par
  3\\kern1cm}r@{ par 5\\kern1cm}r@{ par 9\\kern1cm}r@{ par 10}}
""")
    f1.write("""\\begin{tabular}{c@{ est divisible : \kern1cm}r@{ par 2\\kern1cm}r@{ par
  3\\kern1cm}r@{ par 5\\kern1cm}r@{ par 9\\kern1cm}r@{ par 10}}
""")
    for i in xrange(len(l)):
        f0.write("  %s & $\\square$ & $\\square$ & $\\square$ & $\\square$ & $\\square$ \\\\\n" %
                 l[i])
        f1.write("  %s & %s & %s & %s & %s & %s \\\\\n" % tuple(reponse[i]))
    f0.write("\\end{tabular}\n")
    f1.write("\\end{tabular}\n")


