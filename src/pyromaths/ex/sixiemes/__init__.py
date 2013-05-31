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


from . import angles, decimaux, droites, fractions, operations, quotients
from . import symetrie, arrondi, aires, espace
import random

EXERCICES = (
        operations.CalculMental,
        decimaux.EcrireNombreLettre,
        decimaux.PlaceVirgule,
        decimaux.EcritureFractionnaire,
        decimaux.Decomposition,
        decimaux.Conversions(1),
        decimaux.Conversions(2),
        decimaux.Conversions(3),
        operations.Operations,
        operations.ProduitPuissanceDix,
        decimaux.ClasserNombres,
        droites.Droites,
        droites.Perpendiculaires,
        droites.Proprietes,
        quotients.Divisible,
        fractions.FractionPartage,
        fractions.QuestionsAbscisses,
        aires.main,
        symetrie.SymetrieQuadrillage,
        angles.MesureAngles,
        espace.main,
        arrondi.ArrondirNombreDecimal
        )

TITRES = [u'Calcul mental',
          u'Écrire un nombre décimal',
          u'Placer une virgule',
          u'Écriture fractionnaire ou décimale',
          u'Décomposition de décimaux',
          u'Conversions unités',
          u"Conversions unités d'aires",
          u"Conversions unités de volumes",
          u'Poser des opérations (sauf divisions)',
          u'Produits, quotients par 10, 100, 1000',
          u'Classer des nombres décimaux',
          u'Droites, demi-droites, segments',
          u'Droites perpendiculaires et parallèles',
          u'Propriétés sur les droites',
          u'Multiples de 2, 3, 5, 9, 10',
          u'Fractions partage',
          u'Fractions et abscisses',
          u'Aires et quadrillage',
          u'Symétrie et quadrillages',
          u'Mesurer des angles',
          u'Représentation dans l\'espace',
          u'Arrondir des nombres décimaux'
         ]

FICHE = [u'Sixième', '', TITRES]
