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

### Pour tester la boite de dialogue
## Fichier à compléter par les tests d'environnement

### Tests à faire ?
# installation d'une distribution latex
# installation des bonnes extensions latex
# lecture de pyromaths.xml
# écriture dans le dossier de destination

from os.path import isfile, join

def test(gui):
    from ..Values import CONFIGDIR
    if not isfile(join(CONFIGDIR, "pyromaths.xml")):
        gui.erreur_critique(u"Impossible de lire le fichier de configuration." \
                u"Veuillez vérifier ce dernier ou faire remonter l'erreur " \
                u"sur le forum de Pyromaths.")
