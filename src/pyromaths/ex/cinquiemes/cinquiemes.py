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

from . import priorites, symetrie, fractions, reperage, relatifs, construction, proportionnalite, aires, statistiques

EXERCICES = (priorites.main, symetrie.main, fractions.fractions_egales,
            fractions.sommes_fractions, fractions.produits_fractions,
            reperage.main, relatifs.main, construction.exo_triangle,
            construction.exo_quadrilatere,
            proportionnalite.exo_echelles, aires.exo_aire_diques, statistiques.statistiques)

TITRES = [u'Priorités opératoires',
          u'Symétrie centrale',
          u'Fractions égales',
          u'Sommes de fractions',
          u'Produits de fractions',
          u'Repérage',
          u'Addition de relatifs',
          u'Construction de triangles',
          u'Construction de parallélogrammes',
          u'Échelles',
          u'Aire de disques',
          u'Statistiques',
         ]

FICHE = [u'Cinquième', '', TITRES]
