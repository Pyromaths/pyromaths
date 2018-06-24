#!/usr/bin/env python3
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
# along with this program; if notPopen, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301 USA

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals
from __future__ import print_function
from builtins import str
from builtins import range
from past.utils import old_div
from builtins import object
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QMessageBox
import os, lxml, codecs, sys
from .outils import System
from .Values import CONFIGDIR, DATADIR, COPYRIGHTS, VERSION, ICONDIR
from .Values import lesfiches
from operator import itemgetter

try:
    QString = str
except NameError:
    # Python 3
    QString = str

class Ui_MainWindow(object):
    def __init__(self, *args, **kwargs):
        super(Ui_MainWindow, self).__init__(*args, **kwargs)
        self.lesfiches = lesfiches()

    def setupUi(self, MainWindow):
        #============================================================
        #        Initialisation
        #============================================================
        ## Lecture du fichier de configuration
        self.configfile = os.path.join(CONFIGDIR, "pyromaths.xml")
        self.liste_creation = []
        self.config = self.lire_config('options')
        ## Fenètre principale
        if sys.platform != "darwin":  # Cas de Mac OS X.
            MainWindow.setWindowIcon(QtGui.QIcon(ICONDIR))
        MainWindow.setWindowTitle("Pyromaths")
        MainWindow.setGeometry(0, 44, 900, 600)
        font = QtGui.QFont()
        font.setPointSize(10)
        MainWindow.setFont(font)
#         sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        ## Widget principal
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        MainWindow.setCentralWidget(self.centralwidget)
        ## Grille principale
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)

        #============================================================
        #        Boutons créer, quitter et annuler
        #============================================================
        ## Conteneur vertical
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setContentsMargins(9, 9, 9, 9)
        self.gridLayout.addLayout(self.verticalLayout, 0, 1, 1, 1)
        ## Bouton Créer
        self.pushButton_ok = QtWidgets.QPushButton(self.centralwidget)
        self.verticalLayout.addWidget(self.pushButton_ok)
        self.pushButton_ok.setText(_(u"Créer"))
        if sys.platform != "darwin":  # Cas de Mac OS X.
            self.pushButton_ok.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(243, 165, 30, 255), stop:1 rgba(255, 247, 177, 255));")
        self.pushButton_ok.clicked.connect(self.creer_les_exercices)
        ## Bouton Quitter
        self.pushButton_quit = QtWidgets.QPushButton(self.centralwidget)
        self.verticalLayout.addWidget(self.pushButton_quit)
        self.pushButton_quit.setText(_("Quitter"))
        if sys.platform != "darwin":  # Cas de Mac OS X.
            self.pushButton_quit.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(243, 165, 30, 255), stop:1 rgba(255, 247, 177, 255));")
        self.pushButton_quit.clicked.connect(QtWidgets.QApplication.quit)
        ## Bouton Réinitialiser
        self.pushButton_erase = QtWidgets.QPushButton(self.centralwidget)
        self.verticalLayout.addWidget(self.pushButton_erase)
        self.pushButton_erase.setText(_(u"Réinitialiser"))
        if sys.platform != "darwin":  # Cas de Mac OS X.
            self.pushButton_erase.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(243, 165, 30, 255), stop:1 rgba(255, 247, 177, 255));")
        self.pushButton_erase.clicked.connect(self.effacer_choix_exercices)
        ## Espace Vertical
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)

        #============================================================
        #        Onglets de la zone centrale
        #============================================================
        ## Construction d'une zone d'onglet
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setAutoFillBackground(True)
        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)

        #============================================================
        #        Remplissage des 4 niveaux
        #============================================================
        self.tabs = []
        self.lesfiches.sort(key=itemgetter(0), reverse=True)
        MESFICHES = [[self.lesfiches[i][0][2:], '', self.lesfiches[i][2]] for i in range(len(self.lesfiches))]

        for level in MESFICHES:
            self.tabs.append(Tab(self.tabWidget, level, self.setNbExos))

        #============================================================
        #        Onglet options
        #============================================================
        ## Creation d'une zone de scroll
        self.tab_option_scroll = QtWidgets.QScrollArea(self.tabWidget)
        self.tab_option_scroll.setFrameStyle(QtWidgets.QFrame.StyledPanel)
        self.tab_option_scroll.setWidgetResizable(True)
        self.tabWidget.addTab(self.tab_option_scroll, _("Options"))
        ############## Onglet options

        self.tab_options = QtWidgets.QWidget(self.tab_option_scroll)
        if sys.platform != "darwin":  # Cas de Mac OS X.
            self.tab_options.setStyleSheet("background-color: rgb(251, 245, 225);")
        self.tab_option_scroll.setWidget(self.tab_options)




        self.gridLayout_2 = QtWidgets.QGridLayout(self.tab_options)
        self.horizontalLayout_options1 = QtWidgets.QHBoxLayout()

        ############## Layout pour les noms d'options, en haut à gauche

        self.verticalLayout_16 = QtWidgets.QVBoxLayout()

        ############## Label nom du fichier

        self.opt_nom_fichier = QtWidgets.QLabel(self.tab_options)
        self.opt_nom_fichier.setText(_(u"Nom par défaut du fichier : "))
        self.verticalLayout_16.addWidget(self.opt_nom_fichier)

        ############## Label chemin par défaut pour l'enregistrement des fichiers

        self.opt_chemin_fichier = QtWidgets.QLabel(self.tab_options)
        self.opt_chemin_fichier.setText(_(u"Chemin par défaut pour enregistrer les fichiers : "))
        self.verticalLayout_16.addWidget(self.opt_chemin_fichier)

        ############## Label titre des fiches

        self.opt_titre_fiche = QtWidgets.QLabel(self.tab_options)
        self.opt_titre_fiche.setText(_("Titre de la fiche d'exercices : "))
        self.verticalLayout_16.addWidget(self.opt_titre_fiche)
        self.horizontalLayout_options1.addLayout(self.verticalLayout_16)

        ############## Layout pour les noms d'options, en haut à droite

        self.verticalLayout_17 = QtWidgets.QVBoxLayout()

        ############## LineEdit nom du fichier

        self.nom_fichier = QtWidgets.QLineEdit(self.tab_options)
        self.nom_fichier.setText(self.config['nom_fichier'])
        self.nom_fichier.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.verticalLayout_17.addWidget(self.nom_fichier)

        ############## LineEdit chemin par défaut pour l'enregistrement des fichiers

        self.horizontalLayout_chemin_fichier = QtWidgets.QHBoxLayout()
        self.chemin_fichier = QtWidgets.QLineEdit(self.tab_options)
        self.chemin_fichier.setText(self.config['chemin_fichier'])
        self.chemin_fichier.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.horizontalLayout_chemin_fichier.addWidget(self.chemin_fichier)

        ############## Bouton parcourir

        self.pushButton_parcourir = QtWidgets.QPushButton(self.tab_options)
        self.pushButton_parcourir.setText(_("Parcourir"))
        if sys.platform != "darwin":  # Cas de Mac OS X.
            self.pushButton_parcourir.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(243, 165, 30, 255), stop:1 rgba(255, 247, 177, 255));")
        self.horizontalLayout_chemin_fichier.addWidget(self.pushButton_parcourir)
        self.verticalLayout_17.addLayout(self.horizontalLayout_chemin_fichier)
        self.pushButton_parcourir.clicked.connect(self.option_parcourir)

        ############## LineEdit titre des fiches

        self.titre_fiche = QtWidgets.QLineEdit(self.tab_options)
        self.titre_fiche.setText(self.config['titre_fiche'])
        self.titre_fiche.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.verticalLayout_17.addWidget(self.titre_fiche)
        self.horizontalLayout_options1.addLayout(self.verticalLayout_17)
        self.gridLayout_2.addLayout(self.horizontalLayout_options1, 0, 0, 1, 2)

        ############## Ligne de séparation

        self.line = QtWidgets.QFrame(self.tab_options)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.gridLayout_2.addWidget(self.line, 1, 0, 1, 2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.verticalLayout_21 = QtWidgets.QVBoxLayout()

        ############## CheckBox "corrigés ou non"

        self.checkBox_corrige = QtWidgets.QCheckBox(self.tab_options)
        self.checkBox_corrige.setText(_(u"Créer le corrigé"))
        self.checkBox_corrige.setToolTip(_(u"Pyromaths doit-il créer la fiche de correction détaillée?"))
        self.checkBox_corrige.setChecked(int(self.config['corrige']))
        self.verticalLayout_21.addWidget(self.checkBox_corrige)
        self.checkBox_corrige.stateChanged[int].connect(self.option_corrige)

        ############## CheckBox "pdf ou non"

        self.checkBox_pdf = QtWidgets.QCheckBox(self.tab_options)
        self.checkBox_pdf.setText(_(u"Créer le pdf"))
        self.checkBox_pdf.setToolTip(_(u"Pyromaths doit-il créer les fiches au format pdf ?"))
        self.checkBox_pdf.setChecked(int(self.config['pdf']))
        self.verticalLayout_21.addWidget(self.checkBox_pdf)

        ############## CheckBox "pdf ou non"

        self.checkBox_unpdf = QtWidgets.QCheckBox(self.tab_options)
        self.checkBox_unpdf.setText(_(u"Créer un seul pdf"))
        self.checkBox_unpdf.setToolTip(_(u"Le corrigé et les exercices doivent-ils être dans le même document ?"))
        self.checkBox_unpdf.setChecked(int(self.config['unpdf']))
        self.verticalLayout_21.addWidget(self.checkBox_unpdf)

        ############## Espace

        self.horizontalLayout_3.addLayout(self.verticalLayout_21)
        spacerItem13 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem13)
        self.verticalLayout_20 = QtWidgets.QVBoxLayout()
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.verticalLayout_18 = QtWidgets.QVBoxLayout()

        ############## Label niveau

        self.opt_niveau = QtWidgets.QLabel(self.tab_options)
        self.opt_niveau.setText(_("Niveau :"))
        self.verticalLayout_18.addWidget(self.opt_niveau)

        ############## Label Modèle

        self.label_modele = QtWidgets.QLabel(self.tab_options)
        self.label_modele.setText(_(u"Modèle de mise en page :"))
        # self.label_modele.setEnabled(False)
        self.verticalLayout_18.addWidget(self.label_modele)
        self.horizontalLayout_2.addLayout(self.verticalLayout_18)

        ############## Layout pour les noms d'options, en bas à droite

        self.verticalLayout_19 = QtWidgets.QVBoxLayout()

        ############## ComboBox niveau

        self.comboBox_niveau = QtWidgets.QComboBox(self.tab_options)
        self.comboBox_niveau.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.comboBox_niveau.setEditable(True)  # l’utilisateur peut entrer son propre texte
        self.comboBox_niveau.addItem(_("Classe de 6\\ieme"))
        self.comboBox_niveau.addItem(_("Classe de 5\\ieme"))
        self.comboBox_niveau.addItem(_("Classe de 4\\ieme"))
        self.comboBox_niveau.addItem(_("Classe de 3\\ieme"))
        self.comboBox_niveau.addItem(_("Classe de 2\\up{nde}"))
        self.verticalLayout_19.addWidget(self.comboBox_niveau)

        ############## ComboBox modèles

        self.comboBox_modele = QtWidgets.QComboBox(self.tab_options)
        self.comboBox_modele.setStyleSheet("background-color: rgb(255, 255, 255);")
        modeles = os.listdir(os.path.join(DATADIR, 'templates'))
        modeles_home = os.listdir(os.path.join(CONFIGDIR, 'templates'))

        count = 0
        for element in modeles:
            if os.path.splitext(element)[1] == ".tex":
                self.comboBox_modele.addItem(str(element[:len(element) - 4]))
                if element == self.config['modele']:
                    self.comboBox_modele.setCurrentIndex(count)
                count += 1
        for element in modeles_home:
            if os.path.splitext(element)[1] == ".tex":
                self.comboBox_modele.addItem(QString())
                self.comboBox_modele.setItemText(count, str(element[:len(element) - 4]))
                if element == self.config['modele']:
                    self.comboBox_modele.setCurrentIndex(count)
                count += 1

        self.verticalLayout_19.addWidget(self.comboBox_modele)
        self.horizontalLayout_2.addLayout(self.verticalLayout_19)
        self.verticalLayout_20.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3.addLayout(self.verticalLayout_20)
        self.gridLayout_2.addLayout(self.horizontalLayout_3, 2, 0, 1, 2)

        ############## Bouton enregistrer

        self.pushButton_enr_opt = QtWidgets.QPushButton(self.tab_options)
        self.pushButton_enr_opt.setText(_(u"Enregistrer dans les préférences"))
        if sys.platform != "darwin":  # Cas de Mac OS X.
            self.pushButton_enr_opt.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(243, 165, 30, 255), stop:1 rgba(255, 247, 177, 255));")
        self.pushButton_enr_opt.clicked.connect(self.enregistrer_config)

        self.gridLayout_2.addWidget(self.pushButton_enr_opt, 4, 1, 1, 1)
        spacerItem14 = QtWidgets.QSpacerItem(20, 177, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem14, 3, 1, 1, 1)
        spacerItem15 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem15, 4, 0, 1, 1)

        #============================================================
        #        Barre de menus et de status
        #============================================================
        ## Construction de la barre
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 700, 22))
        MainWindow.setMenuBar(self.menubar)
        ## Menu Fichier
        if sys.platform != "darwin":  # Cas de Mac OS X.
                self.menuFichier = QtWidgets.QMenu(self.menubar)
                self.menuFichier.setTitle(_("Fichier"))
        ## Action Quitter
        self.actionQuitter = QtWidgets.QAction(MainWindow)
        self.actionQuitter.setText(_("Quitter"))
        self.actionQuitter.setShortcut('Ctrl+Q')
        self.actionQuitter.triggered.connect(QtWidgets.QApplication.quit)
        ## Menu Aide
        self.menu_propos = QtWidgets.QMenu(self.menubar)
        self.menu_propos.setTitle(_("Aide"))
        ## Action Accéder au site
        self.actionAcceder_au_site = QtWidgets.QAction(MainWindow)
        self.actionAcceder_au_site.setText(_(u"Accéder au site"))
        self.actionAcceder_au_site.triggered.connect(self.site)
        ## Action À propos
        self.action_a_propos = QtWidgets.QAction(MainWindow)
        self.action_a_propos.setText(_(u"À propos"))
        self.action_a_propos.setMenuRole(QtWidgets.QAction.AboutRole)
        self.action_a_propos.triggered.connect(self.about)
        ## Construction du menu
        if sys.platform != "darwin":
            self.menuFichier.addSeparator()
            self.menuFichier.addAction(self.actionQuitter)
        self.menu_propos.addAction(self.actionAcceder_au_site)
        self.menu_propos.addSeparator()
        self.menu_propos.addAction(self.action_a_propos)
        if sys.platform != "darwin":
            self.menubar.addAction(self.menuFichier.menuAction())
        self.menubar.addAction(self.menu_propos.menuAction())

        #============================================================
        #        Barre d'état
        #============================================================
        ## Construction de la barre d'état
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        MainWindow.setStatusBar(self.statusbar)
        ## Message d'aide
        self.statusbar_label= QtWidgets.QLabel(self.statusbar)
        self.statusbar_label.setText(_(u"Pour avoir un aperçu d'un exercice, positionner le curseur de la souris sur le point d'interrogation."))
        self.statusbar.addWidget(self.statusbar_label,1)

        #QtCore.QMetaObject.connectSlotsByName(MainWindow) #inutile ???

    #============================================================
    #        Début des fonctions
    #============================================================

    # ## Gestion des erreurs
    def erreur_critique(self, message):
        """Dialogue si pyromaths.xml est défectueux."""
        reply = QtWidgets.QMessageBox.critical(self, "Erreur critique", message)
        if reply:
            sys.exit(1)


    def about(self):
        """Crée la boîte de dialogue "À propos de..." """
        text = _(u"""<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd">
<html>
  <head>
    <meta name="qrichtext" content="1" />
    <style type="text/css">
      p, li { white-space: pre-wrap; align:"justify"; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:5px; -qt-block-indent:0; text-indent:0px; }
    </style>
  </head>
  <body style=" font-family:'DejaVu Sans'; font-size:9pt; font-weight:400; font-style:normal;" bgcolor="#f9efbe">
    <p align="center">
    <img src="%s" />
    <br /><br />
    <span style="font-weight:600;">Version %s</span>
    </p>
    <p>
    <span style=" font-weight:600;">Pyromaths</span> est un programme qui permet de créer des  fiches d'exercices types de mathématiques niveau collège avec leur corrigé.
    </p>
    <p>
    Les fiches sont produites au format LaTeX. Pyromaths lance ensuite les commandes nécessaires à la production de fichiers pdf (latex - dvips - ps2pdf) et les ouvre.
    </p>
    <p align="center">
    <span style=" text-decoration: underline;">Remerciements à&nbsp;:</span>
    </p>
    <p>
    <ul style="-qt-list-indent:1;">
      <li>
      <span style=" font-weight:600;">David Robert</span> pour l'idée de départ&nbsp;;
      </li>
      <li>
      <span style=" font-weight:600;">Yves Gesnel</span> pour le portage de Pyromaths sur Mac OS X et la conception d'exercices&nbsp;;
      </li>
      <li>
      <span style=" font-weight:600;">Arnaud Kientz</span> pour ses graphismes, son implication dans le code de Pyromaths et son amitié&nbsp;;
      </li>
      <li>
      <span style=" font-weight:600;">Guillaume Barthélémy</span> pour ses exercices&nbsp;;
      </li>
      <li>
      <span style=" font-weight:600;">Didier Roche</span> pour l'intégration de Pyromaths dans les dépôts Ubuntu&nbsp;;
      </li>
      <li>
      <span style=" font-weight:600;">Olivier Cornu</span> pour son travail sur l'API exercice et sur la diffusion de Pyromaths via Makefile et Setup.py&nbsp;;
      </li>
      <li>
      <span style=" font-weight:600;">Louis Paternault</span> pour son travail sur Pyromaths&nbsp;;
      </li>
      <li>
      <span style=" font-weight:600;">Jacqueline Gouguenheim-Desloy</span> a porté Pyromaths sur Mac OS X à ses débuts. Son soutien et son amitié nous ont été précieux. Sa disparition est une perte douloureuse pour la communauté du logiciel libre.
      </li>
    </ul>
    </p>
    <p align="center">
    %s
    </p>
  </body>
</html>""")
        if sys.platform == "darwin":  # Cas de Mac OS X.
            banniere = os.path.join(DATADIR, 'images', 'pyromaths.png')
        else:
            banniere = os.path.join(DATADIR, 'images', 'pyromaths-banniere.png')
        # self.setGeometry(10,10,620,200)
        QtWidgets.QMessageBox.about(None, _(u'À propos de Pyromaths'), text % (banniere, VERSION, COPYRIGHTS))

    def creer_les_exercices(self):
        """Vérifie si la liste d'exercices n'est pas vide puis sélectionne les noms des fichiers exercices et
        corrigés"""
        self.valide_options()
        if self.liste_creation == [] :
            QtWidgets.QMessageBox.warning(None, _('Attention !'),
                    _(u"Veuillez sélectionner des exercices..."),
                    QtWidgets.QMessageBox.Ok)
        else:
            parametres = {
                'creer_pdf': self.checkBox_pdf.isChecked(),
                'creer_unpdf': self.checkBox_unpdf.isChecked() and self.checkBox_unpdf.isEnabled(),
                'titre': str(self.titre_fiche.text()),
                'corrige': self.checkBox_corrige.isChecked(),
                'niveau': str(self.comboBox_niveau.currentText()),
                'nom_fichier': str(self.nom_fichier.text()),
                'chemin_fichier': str(self.chemin_fichier.text()),
                'modele': str(self.comboBox_modele.currentText() + '.tex'),
                'datadir': DATADIR,
                'configdir': CONFIGDIR
                         }
            #============================================================
            #        Choix de l'ordre des exercices
            #============================================================
            liste = []
            for i in range(len(self.liste_creation)):
                niveau = self.liste_creation[i][0]
                exo = self.liste_creation[i][1]
                liste.append(self.lesfiches[niveau][2][exo])
            self.List = QtWidgets.QListWidget()
            for i in range(len(liste)):
                item = QtWidgets.QListWidgetItem(liste[i].description)
                item.setFlags(QtCore.Qt.ItemIsEnabled |
                              QtCore.Qt.ItemIsSelectable |
                              QtCore.Qt.ItemIsDragEnabled)
                item.exercice = liste[i]
                self.List.addItem(item)
            bmono = True
            for i in range(len(liste)):
                if liste[0] != liste[i]: bmono = False
            if bmono:
                # S'il ny a qu'un seul type d'exercices, pas la peine de choisir
                # l'ordre
                valide(self.List, self.lesfiches, parametres)
            else:
                form = ChoixOrdreExos(self.List, self.lesfiches, parametres, self.centralwidget)
                form.exec_()

    def effacer_choix_exercices(self):
        """Remet toutes les SpinBox à zéro et vide la liste d'exercices sélectionnés"""
        self.liste_creation = []
        for tab in self.tabs:
            tab.reset()

    def enregistrer_config(self):
        """Fonction qui se charge d'enregistrer les options de l'interface dans le fichier de configuration
        après avoir complété le dictionnaire."""
        tree = lxml.etree.parse(self.configfile)
        root = tree.getroot()
        options = root.find('options')
        options .find('nom_fichier').text = str(self.nom_fichier.text())
        options .find('chemin_fichier').text = str(self.chemin_fichier.text())
        options .find('titre_fiche').text = str(self.titre_fiche.text())
        options .find('corrige').text = str(self.checkBox_corrige.isChecked())
        options .find('pdf').text = str(self.checkBox_pdf.isChecked())
        options .find('unpdf').text = str(self.checkBox_unpdf.isChecked())
        options .find('modele').text = str(self.comboBox_modele.currentText() + '.tex')

        f = codecs.open(self.configfile, encoding='utf-8', mode='w')
        f.write(lxml.etree.tostring(root, pretty_print=True, encoding="UTF-8",
                               xml_declaration=True).decode('utf-8', 'strict'))
        f.close()

    def lire_config(self, section):
        """Lis le fichier de configuration pyromaths.conf, enregistre les données dans un dictionnaire config"""
        config = {}
        tree = lxml.etree.parse(self.configfile)
        root = tree.getroot()
        options = root.find(section)
        for child in options:
            if child.text == 'True': text = '1'
            elif child.text == 'False': text = '0'
            else : text = child.text
            config[child.tag] = text
        return config

    def option_parcourir(self):
        d0 = QtWidgets.QFileDialog().getExistingDirectory (None, _(u"Dossier où créer les fiches"),
                                                       self.config['chemin_fichier'], QtWidgets.QFileDialog.ShowDirsOnly)
        if d0:
            self.chemin_fichier.setText(d0)

    def option_corrige(self):
        if not self.checkBox_corrige.isChecked():
            self.checkBox_unpdf.setChecked(False)
            self.checkBox_unpdf.setEnabled(False)
        else:
            self.checkBox_unpdf.setEnabled(True)

    def setNbExos(self):
        """Modifie le nombre d'exercices dans la variable liste_creation lorsqu'on  modifie une spinBox
        et adapte le niveau affiché dans l'en-tête de la fiche en fonction du plus haut niveau d'exercice"""
        niveau = 0
        self.liste_creation = []
        for pkg_no in range(len(self.tabs)):
            for box in range(len(self.lesfiches[pkg_no][2])):
                qte = self.tabs[pkg_no].spinBox[box].value()
                for dummy in range(qte):
                    self.liste_creation.append((pkg_no, box))
                    if pkg_no > niveau:
                        niveau = pkg_no
        self.comboBox_niveau.setCurrentIndex(niveau)

    def site(self):
        """Ouvre le navigatuer internet par défaut sur la page d'accueil du site http://www.pyromaths.org"""
        import webbrowser
        webbrowser.open('http://www.pyromaths.org')


    def valide_options(self):
        """Synchronise les options éventuellement saisies par l'utilisag
QCoreApplication::exec: The event loop is already runningteur avec le dictionnaire de config"""
        self.config['chemin_fichier'] = self.chemin_fichier.text()
        self.config['nom_fichier'] = self.nom_fichier.text()
        self.config['titre_fiche'] = self.titre_fiche.text()
        self.config['corrige'] = self.checkBox_corrige.isChecked()
        self.config['pdf'] = self.checkBox_pdf.isChecked()
        self.config['unpdf'] = self.checkBox_unpdf.isChecked()and self.checkBox_unpdf.isEnabled()

#================================================================
#        Classe ChoixOrdreExos
#================================================================

class ChoixOrdreExos(QtWidgets.QDialog):
    """À appeler de la façon suivante :
    form = ChoixOrdreExos(liste, LesFiches, parametres)
    Permet de choisir l'ordre dans lequel les exercices vont apparaître
    parametres = {'fiche_exo':
                  'fiche_cor':
                  'liste_exos':
                  'creer_pdf':
                  'titre':
                  'corrige':
                  'niveau':
                  'nom_fichier':
                  'chemin_fichier':
                 }"""

    def __init__(self, liste, LesFiches, parametres, parent=None):
        self.lesfiches = LesFiches
        self.parametres = parametres
        self.List = liste
        QtWidgets.QDialog.__init__(self, parent)
        self.setWindowTitle(_("Choisissez l'ordre des exercices"))
        layout = QtWidgets.QHBoxLayout()

        buttonBox = QtWidgets.QDialogButtonBox()
        buttonBox.setOrientation(QtCore.Qt.Vertical)
        buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)

        self.List.setAlternatingRowColors(True)
        self.List.setDragEnabled(True)
        self.List.setAcceptDrops(True)
        self.List.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)
        self.List.setDropIndicatorShown(True)

        layout.addWidget(self.List)
        layout.addWidget(buttonBox)
        self.setLayout(layout)

        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.close)

    def accept(self):
        """Écrit une liste contenant la liste des exercices dans l'ordre choisit par l'utilisateur et demande à
        celui-ci les noms de fichiers pour les exercices et les corrigés"""
        valide(self.List, self.lesfiches, self.parametres)
        self.close()

def valide(liste, LesFiches, parametres):
    """ Permet de choisir les noms et emplacements des fichiers tex, les écrits
    et lance la compilation LaTex"""
    corrige = parametres['corrige']
    lesexos = []
    for i in range(liste.count()):
        lesexos.append(liste.item(i).exercice())

    #============================================================
    #        Choix des noms des fichiers exercices et corrigés
    #============================================================
    filename = System.supprime_extension(parametres['nom_fichier'], '.tex')
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    f0, _ = QFileDialog.getSaveFileName(None,"Enregistrer sous...",
        os.path.join(parametres['chemin_fichier'], u'%s.tex' % filename),
        "Documents Tex (*.tex);;All Files(*)",
        options=options)
    # f0 = unicode(saveas.getSaveFileName(None, "Enregistrer sous...",
                # os.path.join(parametres['chemin_fichier'],
                             # u'%s.tex' % filename), "Documents Tex (*.tex)"))[0]
    print(f0)
    print(os.path.splitext(os.path.basename(f0))[0])
    if f0:
        System.ajoute_extension(f0, '.tex')
        if corrige and not parametres['creer_unpdf']:
            f1 = str(saveas.getSaveFileName(None, "Enregistrer sous...",
                os.path.join(os.path.dirname(f0),
                _(u"%s-corrige.tex") % os.path.splitext(os.path.basename(f0))[0]),
                _("Documents Tex (*.tex)")))[0]
        else:
            f1 = os.path.join(os.path.dirname(f0),
                    os.path.splitext(os.path.basename(f0))[0] + "-corrige.tex")
        if f1:
            if corrige:
                System.ajoute_extension(f1, '.tex')
            parametres ['fiche_exo'] = f0
            parametres ['fiche_cor'] = f1
            parametres ['liste_exos'] = lesexos
            parametres ['les_fiches'] = LesFiches
            System.creation(parametres)

#================================================================
#        Classe Tab
#================================================================

class Tab(QtWidgets.QWidget):
    """Gère les onglets permettant de sélectionner des exercices"""

    def __init__(self, parent, level, onchange):
        QtWidgets.QWidget.__init__(self)  # Initialise la super-classe
        self.titre = level[0]
        self.exos = level[2]
        self.scroll = QtWidgets.QScrollArea(self)
        self.scroll.setFrameStyle(QtWidgets.QFrame.StyledPanel)
        self.scroll.setWidgetResizable(True)
        self.widget = QtWidgets.QWidget(self.scroll)
        self.scroll.setWidget(self.widget)
        if sys.platform != "darwin":  # Cas de Mac OS X.
            self.widget.setStyleSheet("background-color: rgb(251, 245, 225);")
        self.layout = QtWidgets.QGridLayout(self.widget)
        self.spinBox = []
        # Crée les widgets des exercices
        nb_exos = len(self.exos)
        spacer = QtWidgets.QSpacerItem(20, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        for i in range(nb_exos):
            self.add_exercise(i, onchange)
            self.layout.addItem(spacer, old_div((nb_exos + 1), 2), 0, 1, 1)
            self.layout.addItem(spacer, old_div((nb_exos + 1), 2), 1, 1, 1)
        # Ajoute ce tab au widget parent
        parent.addTab(self.scroll, self.titre)



    def add_exercise(self, i, onchange):
        """Ajoute l'exercice n°i à cet onglet"""
        layout = QtWidgets.QHBoxLayout()
        # SpinBox
        spinBox = QtWidgets.QSpinBox(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(40)
        sizePolicy.setVerticalStretch(30)
        sizePolicy.setHeightForWidth(spinBox.sizePolicy().hasHeightForWidth())
        spinBox.setSizePolicy(sizePolicy)
        spinBox.setToolTip(_(u"Choisissez le nombre d\'exercices de ce type à créer."))
        spinBox.setStyleSheet("background-color: rgb(255, 255, 255);")
        spinBox.valueChanged[int].connect(onchange)
        self.spinBox.append(spinBox)
        layout.addWidget(spinBox)
        # Image
        img = QtWidgets.QLabel(self.widget)
        img.setText(r'<img src="%s"/>' % os.path.join(DATADIR, 'images', 'whatsthis.png'))
        img.setToolTip(r'<img src="%s"/>' % self.exos[i].thumb())
        layout.addWidget(img)
        # Label
        label = QtWidgets.QLabel(self.widget)
        label.setText(self.exos[i].description)
        layout.addWidget(label)
        # Espacements
        spacer = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        layout.addItem(spacer)
        layout.addItem(spacer)
        # Ajoute cet exercice à l'onglet
        self.layout.addLayout(layout, old_div(i, 2), i % 2, 1, 1)

    def reset(self):
        """Remet les compteurs à zéro"""
        for i in range(len(self.exos)):
            self.spinBox[i].setValue(0)
