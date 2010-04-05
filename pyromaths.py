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

from PyQt4 import QtGui, QtCore
import sys, os, codecs
from outils.TestEnv import test

#================================================================
# Cas d'une installation de Pyromaths via deb ou rpm, il faut
# ajouter les modules au PATH
#================================================================
if os.name == "posix" and os.path.basename(__file__)=="pyromaths":
    sys.path.append(os.path.join( os.path.dirname(__file__),
        "../lib/pyromaths"))

#================================================================
# Imports spécifiques à Pyromaths
#=========================== QtGui ========================
import interface
import outils.System
import troisiemes.troisiemes, quatriemes.quatriemes, cinquiemes.cinquiemes
import sixiemes.sixiemes
import lycee.lycee

#================================================================
# Dossier des icones
#================================================================
if os.name == "posix" and os.path.basename(__file__) == "pyromaths":
    iconesdir="/usr/share/pixmaps"
else:
    pathname = os.path.dirname((sys.argv)[0])
    iconesdir=os.path.join(outils.System.module_path(),  'img')


LesFiches = [[u'Sixième', sixiemes.sixiemes, [
u'Calcul mental',
u'Écrire un nombre décimal',
u'Placer une virgule',
u'Écriture fractionnaire ou décimale',
u'Décomposition de nombres décimaux',
u'Conversions unités',
u'Poser des opérations (sauf divisions)',
u'Produits et quotients par 10, 100, 1000',
u'Classer des nombres décimaux',
u'Droites, demi-droites, segments',
u'Droites perpendiculaires et parallèles',
u'Propriétés sur les droites',
u'Multiples de 2, 3, 5, 9, 10',
u'Fractions partage',
u'Fractions et abscisses',
u'Symétrie et quadrillages',
u'Mesurer des angles',
u'Arrondir des nombres décimaux'
]],
[u'Cinquième', cinquiemes.cinquiemes, [
u'Priorités opératoires',
u'Symétrie centrale',
u'Fractions égales',
u'Sommes de fractions',
u'Produits de fractions',
u'repérage',
]],
[u'Quatrième', quatriemes.quatriemes, [
u'Calcul mental',
u'Sommes de fractions',
u'Produits et quotients de fractions',
u'Fractions et priorités',
u'Propriétés sur les puissances',
u'Propriétés sur les puissances de 10',
u'Écritures scientifiques',
u'Puissances de 10',
u'Distributivité',
u'Double distributivité',
u'Théorème de Pythagore',
u'Réciproque du théorème de Pythagore',
u'Cercle et théorème de Pythagore',
u'Théorème de Thalès',
u'Trigonométrie',
]],
[u'Troisième', troisiemes.troisiemes, [
u'Fractions',
u'Puissances',
u'PGCD',
u'Développements',
u'Factorisations',
u'Dévt, factorisat°, calcul et éq° produit',
u'Équation',
u'Racines carrées',
u'Système d\'équations',
u'Fonctions affines',
u'Probabilités',
u'Théorème de Pythagore',
u'Réciproque du théorème de Pythagore',
u'Cercle et théorème de Pythagore',
u'Théorème de Thalès',
u'Réciproque du théorème de Thalès',
u'Trigonométrie',
u'Arithmétique'
]],
[u'Lycée', lycee.lycee, [
u'Équations 2° degré',
u'Factorisations 2° degré',
u'Factorisations degré 3',
u'Étude de signe',
u"Sens de variations",
]],
]

class StartQT4(QtGui.QMainWindow, interface.Ui_MainWindow):
    def __init__(self, LesFiches, configdir, iconesdir, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = interface.Ui_MainWindow()
        self.ui.setupUi(self, LesFiches, configdir, iconesdir)

    
if __name__ == "__main__":
#================================================================
# Création du fichier de configuration si inexistant
#================================================================
    if not os.access(os.path.join(outils.System.configdir(), "pyromaths.xml"), os.R_OK):
        if not os.path.isdir(outils.System.configdir()):
            os.makedirs(outils.System.configdir())
        f = codecs.open(os.path.join(outils.System.configdir(), "pyromaths.xml"), encoding='utf-8', mode='w')
        f.write(u"" + outils.System.create_config_file())
        f.close()
    outils.System.modify_config_file(os.path.join(outils.System.configdir(), "pyromaths.xml"))

#================================================================
# Création du dossier "modeles" local
#================================================================
    modeledir = os.path.join(outils.System.configdir(),  "modeles")
    if not os.path.isdir(modeledir):
        os.makedirs(modeledir)

    app = QtGui.QApplication(sys.argv)
    pyromaths = StartQT4(LesFiches,  outils.System.configdir(), iconesdir)
    pyromaths.show()   
    
    #test(pyromaths)
    
    sys.exit(app.exec_())
