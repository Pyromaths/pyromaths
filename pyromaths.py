#!/usr/bin/python3
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

from PyQt4 import QtGui, QtCore
import sys,  os

#================================================================
# Imports spécifiques à Pyromaths
#=========================== QtGui ========================
import interface,  outils
import troisiemes.troisiemes, quatriemes.quatriemes, cinquiemes.cinquiemes
import sixiemes.sixiemes

#================================================================
# Cas d'une installation de Pyromaths via deb ou rpm, il faut
# ajouter les modules au PATH
#================================================================
if os.name == "posix" and os.path.basename(__file__)=="pyromaths":
    sys.path.append(os.path.join( os.path.dirname(__file__),
        "../lib/pyromaths"))

#================================================================
# Dossier des icones
#================================================================
if os.name == "posix" and os.path.basename(__file__) == "pyromaths":
    iconesdir="/usr/share/pixmaps"
else:
    pathname = os.path.dirname((sys.argv)[0])
    iconesdir=os.path.join(outils.module_path(), 'img')


LesFiches = [['Sixième', sixiemes.sixiemes, [
'Calcul mental',
'Écrire un nombre décimal',
'Placer une virgule',
'Écriture fractionnaire ou décimale',
'Décomposition de nombres décimaux',
'Conversions unités',
'Poser des opérations (sauf divisions)',
'Produits et quotients par 10, 100, 1000',
'Classer des nombres décimaux',
'Droites, demi-droites, segments',
'Droites perpendiculaires et parallèles',
'Propriétés sur les droites',
'Multiples de 2, 3, 5, 9, 10',
'Fractions partage',
'Fractions et abscisses',
'Symétrie et quadrillages',
'Mesurer des angles',
]],
['Cinquième', cinquiemes.cinquiemes, [
'Priorités opératoires',
'Symétrie centrale',
'Fractions égales',
'Sommes de fractions',
'Produits de fractions',
'repérage',
]],
['Quatrième', quatriemes.quatriemes, [
'Calcul mental',
'Sommes de fractions',
'Produits et quotients de fractions',
'Fractions et priorités',
'Propriétés sur les puissances',
'Propriétés sur les puissances de 10',
'Écritures scientifiques',
'Puissances de 10',
'Distributivité',
'Double distributivité',
'Théorème de Pythagore',
'Réciproque du théorème de Pythagore',
'Cercle et théorème de Pythagore',
'Théorème de Thalès',
'Trigonométrie',
]],
['Troisième', troisiemes.troisiemes, [
'Fractions',
'Puissances',
'PGCD',
'Développements',
'Factorisations',
'Dévt, factorisat°, calcul et éq° produit',
'Équation',
'Racines carrées',
'Système d\'équations',
'Fonctions affines',
'Probabilités',
'Théorème de Pythagore',
'Réciproque du théorème de Pythagore',
'Cercle et théorème de Pythagore',
'Théorème de Thalès',
'Réciproque du théorème de Thalès',
'Trigonométrie',
]]]

class StartQT4(QtGui.QMainWindow):
    def __init__(self, LesFiches, configdir, iconesdir, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = interface.Ui_MainWindow()
        self.ui.setupUi(self, LesFiches, configdir, iconesdir)


if __name__ == "__main__":
#================================================================
# Création du fichier de configuration si inexistant
#================================================================
    if not os.access(os.path.join(outils.configdir(),  "pyromaths.xml"), os.R_OK):
        if not os.path.isdir(outils.configdir()):
            os.makedirs(outils.configdir())
        f = open(os.path.join(outils.configdir(),  "pyromaths.xml"), encoding='utf-8', mode='w')
        f.write(outils.create_config_file())
        f.close()
    outils.modify_config_file(os.path.join(outils.configdir(),  "pyromaths.xml"))

#================================================================
# Création du dossier "modeles" local
#================================================================
    modeledir = os.path.join(outils.configdir(),  "modeles")
    if not os.path.isdir(modeledir):
        os.makedirs(modeledir)

    app = QtGui.QApplication(sys.argv)
    pyromaths = StartQT4(LesFiches,  outils.configdir(), iconesdir)
    pyromaths.show()
    sys.exit(app.exec_())
