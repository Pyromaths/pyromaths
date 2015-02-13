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
# along with this program; if notPopen, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301 USA

from PyQt4 import QtGui, QtCore
from PyQt4 import Qt  # Cas de Mac OS X, QTBUG-36212
import os, lxml, codecs, sys
from outils import System
from Values import CONFIGDIR, DATADIR, COPYRIGHTS, VERSION, ICONDIR
from Values import lesfiches
from operator import itemgetter

class Ui_MainWindow(object):
    def __init__(self, *args, **kwargs):
        super(Ui_MainWindow, self).__init__(*args, **kwargs)
        self.lesfiches = lesfiches()

    def setupUi(self, MainWindow):
        self.configfile = os.path.join(CONFIGDIR, "pyromaths.xml")
        self.liste_creation = []
        if sys.platform != "darwin":  # Cas de Mac OS X.
            MainWindow.setStyleSheet("background-color: rgb(251, 245, 225);")
            MainWindow.setWindowIcon(QtGui.QIcon(ICONDIR))
        MainWindow.setWindowTitle("Pyromaths")
        MainWindow.setGeometry(0, 44, 500, 200)
        font = QtGui.QFont()
        font.setPointSize(10)
        MainWindow.setFont(font)

#         sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setMargin(9)

        #============================================================
        #        lecture du fichier de configuration
        #============================================================
        self.config = self.lire_config('options')

        #============================================================
        #        Boutons créer, quitter et annuler
        #============================================================
        self.pushButton_ok = QtGui.QPushButton(self.centralwidget)
        self.verticalLayout.addWidget(self.pushButton_ok)
        self.pushButton_ok.setText(u"Créer")
        if sys.platform != "darwin":  # Cas de Mac OS X.
            self.pushButton_ok.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(243, 165, 30, 255), stop:1 rgba(255, 247, 177, 255));")

        self.pushButton_quit = QtGui.QPushButton(self.centralwidget)
        self.verticalLayout.addWidget(self.pushButton_quit)
        self.pushButton_quit.setText("Quitter")
        if sys.platform != "darwin":  # Cas de Mac OS X.
            self.pushButton_quit.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(243, 165, 30, 255), stop:1 rgba(255, 247, 177, 255));")

        self.pushButton_erase = QtGui.QPushButton(self.centralwidget)
        self.verticalLayout.addWidget(self.pushButton_erase)
        self.pushButton_erase.setText(u"Réinitialiser")
        if sys.platform != "darwin":  # Cas de Mac OS X.
            self.pushButton_erase.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(243, 165, 30, 255), stop:1 rgba(255, 247, 177, 255));")


        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)

        #============================================================
        #        Onglets de la zone centrale
        #============================================================

        self.gridLayout.addLayout(self.verticalLayout, 0, 1, 1, 1)
        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget.setAutoFillBackground(True)
        if sys.platform != "darwin":  # Cas de Mac OS X.
            self.tabWidget.setStyleSheet("background-color: rgb(251, 231, 178);")

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

        ############## Onglet options

        self.tab_options = QtGui.QWidget()
        self.tabWidget.addTab(self.tab_options, "")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_options), "Options")
        self.gridLayout_2 = QtGui.QGridLayout(self.tab_options)
        self.horizontalLayout_options1 = QtGui.QHBoxLayout()

        ############## Layout pour les noms d'options, en haut à gauche

        self.verticalLayout_16 = QtGui.QVBoxLayout()

        ############## Label nom du fichier

        self.opt_nom_fichier = QtGui.QLabel(self.tab_options)
        self.opt_nom_fichier.setText(u"Nom par défaut du fichier : ")
        self.verticalLayout_16.addWidget(self.opt_nom_fichier)

        ############## Label chemin par défaut pour l'enregistrement des fichiers

        self.opt_chemin_fichier = QtGui.QLabel(self.tab_options)
        self.opt_chemin_fichier.setText(u"Chemin par défaut pour enregistrer les fichiers : ")
        self.verticalLayout_16.addWidget(self.opt_chemin_fichier)

        ############## Label titre des fiches

        self.opt_titre_fiche = QtGui.QLabel(self.tab_options)
        self.opt_titre_fiche.setText("Titre de la fiche d'exercices : ")
        self.verticalLayout_16.addWidget(self.opt_titre_fiche)
        self.horizontalLayout_options1.addLayout(self.verticalLayout_16)

        ############## Layout pour les noms d'options, en haut à droite

        self.verticalLayout_17 = QtGui.QVBoxLayout()

        ############## LineEdit nom du fichier

        self.nom_fichier = QtGui.QLineEdit(self.tab_options)
        self.nom_fichier.setText(self.config['nom_fichier'])
        self.verticalLayout_17.addWidget(self.nom_fichier)

        ############## LineEdit chemin par défaut pour l'enregistrement des fichiers

        self.horizontalLayout_chemin_fichier = QtGui.QHBoxLayout()
        self.chemin_fichier = QtGui.QLineEdit(self.tab_options)
        self.chemin_fichier.setText(self.config['chemin_fichier'])
        self.horizontalLayout_chemin_fichier.addWidget(self.chemin_fichier)

        ############## Bouton parcourir

        self.pushButton_parcourir = QtGui.QPushButton(self.tab_options)
        self.pushButton_parcourir.setText("Parcourir")
        self.horizontalLayout_chemin_fichier.addWidget(self.pushButton_parcourir)
        self.verticalLayout_17.addLayout(self.horizontalLayout_chemin_fichier)

        ############## LineEdit titre des fiches

        self.titre_fiche = QtGui.QLineEdit(self.tab_options)
        self.titre_fiche.setText(self.config['titre_fiche'])
        self.verticalLayout_17.addWidget(self.titre_fiche)
        self.horizontalLayout_options1.addLayout(self.verticalLayout_17)
        self.gridLayout_2.addLayout(self.horizontalLayout_options1, 0, 0, 1, 2)

        ############## Ligne de séparation

        self.line = QtGui.QFrame(self.tab_options)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.gridLayout_2.addWidget(self.line, 1, 0, 1, 2)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.verticalLayout_21 = QtGui.QVBoxLayout()

        ############## CheckBox "corrigés ou non"

        self.checkBox_corrige = QtGui.QCheckBox(self.tab_options)
        self.checkBox_corrige.setText(u"Créer le corrigé")
        self.checkBox_corrige.setToolTip(u"Pyromaths doit-il créer la fiche de correction détaillée?")
        self.checkBox_corrige.setChecked(int(self.config['corrige']))
        self.verticalLayout_21.addWidget(self.checkBox_corrige)

        ############## CheckBox "pdf ou non"

        self.checkBox_pdf = QtGui.QCheckBox(self.tab_options)
        self.checkBox_pdf.setText(u"Créer le pdf")
        self.checkBox_pdf.setToolTip(u"Pyromaths doit-il créer les fiches au format pdf ?")
        self.checkBox_pdf.setChecked(int(self.config['pdf']))
        self.verticalLayout_21.addWidget(self.checkBox_pdf)

        ############## CheckBox "pdf ou non"

        self.checkBox_unpdf = QtGui.QCheckBox(self.tab_options)
        self.checkBox_unpdf.setText(u"Créer un seul pdf")
        self.checkBox_unpdf.setToolTip(u"Le corrigé et les exercices doivent-ils être dans le même document ?")
        self.checkBox_unpdf.setChecked(int(self.config['unpdf']))
        self.verticalLayout_21.addWidget(self.checkBox_unpdf)

        ############## Espace

        self.horizontalLayout_3.addLayout(self.verticalLayout_21)
        spacerItem13 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem13)
        self.verticalLayout_20 = QtGui.QVBoxLayout()
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.verticalLayout_18 = QtGui.QVBoxLayout()

        ############## Label niveau

        self.opt_niveau = QtGui.QLabel(self.tab_options)
        self.opt_niveau.setText("Niveau :")
        self.verticalLayout_18.addWidget(self.opt_niveau)

        ############## Label Modèle

        self.label_modele = QtGui.QLabel(self.tab_options)
        self.label_modele.setText(u"Modèle de mise en page :")
        # self.label_modele.setEnabled(False)
        self.verticalLayout_18.addWidget(self.label_modele)
        self.horizontalLayout_2.addLayout(self.verticalLayout_18)

        ############## Layout pour les noms d'options, en bas à droite

        self.verticalLayout_19 = QtGui.QVBoxLayout()

        ############## ComboBox niveau

        self.comboBox_niveau = QtGui.QComboBox(self.tab_options)
        self.comboBox_niveau.setEditable(True)  # l’utilisateur peut entrer son propre texte
        self.comboBox_niveau.addItem("Classe de 6\\ieme")
        self.comboBox_niveau.addItem("Classe de 5\\ieme")
        self.comboBox_niveau.addItem("Classe de 4\\ieme")
        self.comboBox_niveau.addItem("Classe de 3\\ieme")
        self.comboBox_niveau.addItem("Classe de 2\\up{nde}")
        self.verticalLayout_19.addWidget(self.comboBox_niveau)

        ############## ComboBox modèles

        self.comboBox_modele = QtGui.QComboBox(self.tab_options)

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
                self.comboBox_modele.addItem(QtCore.QString())
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

        self.pushButton_enr_opt = QtGui.QPushButton(self.tab_options)
        self.pushButton_enr_opt.setText(u"Enregistrer dans les préférences")
        if sys.platform != "darwin":  # Cas de Mac OS X.
            self.pushButton_enr_opt.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(243, 165, 30, 255), stop:1 rgba(255, 247, 177, 255));")

        self.gridLayout_2.addWidget(self.pushButton_enr_opt, 4, 1, 1, 1)
        spacerItem14 = QtGui.QSpacerItem(20, 177, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem14, 3, 1, 1, 1)
        spacerItem15 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem15, 4, 0, 1, 1)

        #============================================================
        #        Barre de menus et de status
        #============================================================
        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 700, 22))
        if sys.platform != "darwin":
            self.menubar.setStyleSheet("background-color: rgb(251, 231, 178);")
        MainWindow.setMenuBar(self.menubar)

        if sys.platform != "darwin":  # Cas de Mac OS X.
                self.menuFichier = QtGui.QMenu(self.menubar)
                self.menuFichier.setTitle("Fichier")

        self.menu_propos = QtGui.QMenu(self.menubar)
        self.menu_propos.setTitle("Aide")

        self.statusbar = QtGui.QStatusBar(MainWindow)
        MainWindow.setStatusBar(self.statusbar)
        self.statusbar.showMessage(u"Pour avoir un aperçu d'un exercice, positionner le curseur de la souris sur le point d'interrogation.")
        if sys.platform != "darwin":  # Cas de Mac OS X.
            self.statusbar.setStyleSheet("background-color: rgb(251, 231, 178);")

        #============================================================
        #        Menus de la barre de menus
        #============================================================
        self.actionQuitter = QtGui.QAction(MainWindow)
        self.actionQuitter.setText("Quitter")

        self.actionAcceder_au_site = QtGui.QAction(MainWindow)
        self.actionAcceder_au_site.setText(u"Accéder au site")

        self.action_a_propos = QtGui.QAction(MainWindow)
        self.action_a_propos.setText(u"À propos")
        self.action_a_propos.setMenuRole(QtGui.QAction.AboutRole)

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
        #    Raccourcis clavier
        #============================================================
        keyQuit = QtGui.QShortcut("Ctrl+Q", MainWindow)
        QtCore.QObject.connect(keyQuit, QtCore.SIGNAL("triggered()"), QtGui.qApp,
                                                                 QtCore.SLOT("quit()"))

        #============================================================
        #    Actions des boutons et menus
        #============================================================
        QtCore.QObject.connect(self.actionQuitter, QtCore.SIGNAL("triggered()"), QtGui.qApp,
                                                                 QtCore.SLOT("quit()"))
        QtCore.QObject.connect(self.actionAcceder_au_site, QtCore.SIGNAL("triggered()"), self.site)
        QtCore.QObject.connect(self.action_a_propos, QtCore.SIGNAL("triggered()"), self.about)
        QtCore.QObject.connect(self.pushButton_quit, QtCore.SIGNAL("clicked()"), QtGui.qApp,
                                                                 QtCore.SLOT("quit()"))
        QtCore.QObject.connect(self.pushButton_erase, QtCore.SIGNAL("clicked()"), self.effacer_choix_exercices)
        QtCore.QObject.connect(self.pushButton_ok, QtCore.SIGNAL("clicked()"), self.creer_les_exercices)
        QtCore.QObject.connect(self.pushButton_enr_opt, QtCore.SIGNAL("clicked()"), self.enregistrer_config)
        QtCore.QObject.connect(self.pushButton_parcourir, QtCore.SIGNAL("clicked()"), self.option_parcourir)
        QtCore.QObject.connect(self.checkBox_corrige, QtCore.SIGNAL("stateChanged(int)"), self.option_corrige)

        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    #============================================================
    #        Début des fonctions
    #============================================================

    # ## Gestion des erreurs
    def erreur_critique(self, message):
        """Dialogue si pyromaths.xml est défectueux."""
        reply = QtGui.QMessageBox.critical(self, "Erreur critique", message)
        if reply:
            sys.exit(1)


    def about(self):
        """Crée la boîte de dialogue "À propos de..." """
        text = u"""<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd">
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
      <span style=" font-weight:600;">Nicolas Bissonnier</span> pour son arrivée dans l'équipe de développement&nbsp;;
      </li>
      <li>
      <span style=" font-weight:600;">Didier Roche</span> pour l'intégration de Pyromaths dans les dépôts Ubuntu&nbsp;;
      </li>
      <li>
      <span style=" font-weight:600;">Olivier Cornu</span> pour son travail sur l'API exercice et sur la diffusion de Pyromaths via Makefile et Setup.py&nbsp;;
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
</html>"""
        if sys.platform == "darwin":  # Cas de Mac OS X.
            banniere = os.path.join(DATADIR, 'images', 'pyromaths.png')
        else:
            banniere = os.path.join(DATADIR, 'images', 'pyromaths-banniere.png')
        QtGui.QMessageBox.about(None, u'À propos de Pyromaths', text % (banniere, VERSION, COPYRIGHTS))

    def creer_les_exercices(self):
        """Vérifie si la liste d'exercices n'est pas vide puis sélectionne les noms des fichiers exercices et
        corrigés"""
        self.valide_options()
        if self.liste_creation == [] :
            QtGui.QMessageBox.warning(None, 'Attention !',
                    u"Veuillez sélectionner des exercices...",
                    QtGui.QMessageBox.Ok)
        else:
            parametres = {
                'creer_pdf': self.checkBox_pdf.isChecked(),
                'creer_unpdf': self.checkBox_unpdf.isChecked() and self.checkBox_unpdf.isEnabled(),
                'titre': unicode(self.titre_fiche.text()),
                'corrige': self.checkBox_corrige.isChecked(),
                'niveau': unicode(self.comboBox_niveau.currentText()),
                'nom_fichier': unicode(self.nom_fichier.text()),
                'chemin_fichier': unicode(self.chemin_fichier.text()),
                'modele': unicode(self.comboBox_modele.currentText() + '.tex'),
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
            self.List = QtGui.QListWidget()
            for i in range(len(liste)):
                item = QtGui.QListWidgetItem(liste[i].description)
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
                form = ChoixOrdreExos(self.List, self.lesfiches, parametres)
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
        options .find('nom_fichier').text = unicode(self.nom_fichier.text())
        options .find('chemin_fichier').text = unicode(self.chemin_fichier.text())
        options .find('titre_fiche').text = unicode(self.titre_fiche.text())
        options .find('corrige').text = str(self.checkBox_corrige.isChecked())
        options .find('pdf').text = str(self.checkBox_pdf.isChecked())
        options .find('unpdf').text = str(self.checkBox_unpdf.isChecked())
        options .find('modele').text = unicode(self.comboBox_modele.currentText() + '.tex')

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
        d0 = QtGui.QFileDialog().getExistingDirectory (None, u"Dossier où créer les fiches",
                                                       self.config['chemin_fichier'], QtGui.QFileDialog.ShowDirsOnly)
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

class ChoixOrdreExos(QtGui.QDialog):
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
        QtGui.QDialog.__init__(self, parent)
        self.setWindowTitle("Choisissez l'ordre des exercices")
        layout = QtGui.QHBoxLayout()

        buttonBox = QtGui.QDialogButtonBox()
        buttonBox.setOrientation(QtCore.Qt.Vertical)
        buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel | QtGui.QDialogButtonBox.Ok)

        self.List.setAlternatingRowColors(True)
        self.List.setDragEnabled(True)
        self.List.setAcceptDrops(True)
        self.List.setDragDropMode(QtGui.QAbstractItemView.InternalMove)
        self.List.setDropIndicatorShown(True)

        layout.addWidget(self.List)
        layout.addWidget(buttonBox)
        self.setLayout(layout)

        QtCore.QObject.connect(buttonBox, QtCore.SIGNAL("accepted()"), self.accept)
        QtCore.QObject.connect(buttonBox, QtCore.SIGNAL("rejected()"), self.close)

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
    saveas = QtGui.QFileDialog()
    filename = System.supprime_extension(parametres['nom_fichier'],
                                         '.tex')
    if sys.platform == "darwin":  # Cas de Mac OS X, QTBUG-36212
        f0 = unicode(saveas.getSaveFileName(None, "Enregistrer sous...",
                    os.path.join(parametres['chemin_fichier'],
                             u'%s.tex' % filename), "Documents Tex (*.tex)", '', Qt.QFileDialog.DontUseNativeDialog))
    else:
        f0 = unicode(saveas.getSaveFileName(None, "Enregistrer sous...",
                os.path.join(parametres['chemin_fichier'],
                             u'%s.tex' % filename), "Documents Tex (*.tex)"))
    if f0:
        System.ajoute_extension(f0, '.tex')
        if corrige and not parametres['creer_unpdf']:
            if sys.platform == "darwin":  # Cas de Mac OS X, QTBUG-36212
                f1 = unicode(saveas.getSaveFileName(None, "Enregistrer sous...",
                    os.path.join(os.path.dirname(f0),
                    u"%s-corrige.tex" % os.path.splitext(os.path.basename(f0))[0]),
                    "Documents Tex (*.tex)", '', Qt.QFileDialog.DontUseNativeDialog))
            else:
                f1 = unicode(saveas.getSaveFileName(None, "Enregistrer sous...",
                os.path.join(os.path.dirname(f0),
                u"%s-corrige.tex" % os.path.splitext(os.path.basename(f0))[0]),
                "Documents Tex (*.tex)"))
        else:
            f1 = os.path.join(os.path.dirname(f0), u"%s-corrige.tex" %
                              os.path.splitext(os.path.basename(f0))[0])
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

class Tab(QtGui.QWidget):
    """Gère les onglets permettant de sélectionner des exercices"""

    def __init__(self, parent, level, onchange):
        QtGui.QWidget.__init__(self)  # Initialise la super-classe
        self.titre = level[0]
        self.exos = level[2]
        self.layout = QtGui.QGridLayout(self)
        self.spinBox = []
        # Crée les widgets des exercices
        nb_exos = len(self.exos)
        spacer = QtGui.QSpacerItem(20, 0, QtGui.QSizePolicy.Minimum,
                                    QtGui.QSizePolicy.Expanding)
        for i in range(nb_exos):
            self.add_exercise(i, onchange)
            self.layout.addItem(spacer, (nb_exos + 1) / 2, 0, 1, 1)
            self.layout.addItem(spacer, (nb_exos + 1) / 2, 1, 1, 1)
        # Ajoute ce tab au widget parent
        parent.addTab(self, self.titre)

    def add_exercise(self, i, onchange):
        """Ajoute l'exercice n°i à cet onglet"""
        layout = QtGui.QHBoxLayout()
        # SpinBox
        spinBox = QtGui.QSpinBox(self)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(40)
        sizePolicy.setVerticalStretch(30)
        sizePolicy.setHeightForWidth(spinBox.sizePolicy().hasHeightForWidth())
        spinBox.setSizePolicy(sizePolicy)
        spinBox.setToolTip(u"Choisissez le nombre d\'exercices de ce type à créer.")
        QtCore.QObject.connect(spinBox, QtCore.SIGNAL("valueChanged(int)"),
                               onchange)
        self.spinBox.append(spinBox)
        layout.addWidget(spinBox)
        # Image
        img = QtGui.QLabel(self)
        img.setText(r'<img src="%s"/>' %
                    os.path.join(DATADIR, 'images', 'whatsthis.png'))
        img.setToolTip(r'<img src="%s"/>' % self.exos[i].thumb)
        layout.addWidget(img)
        # Label
        label = QtGui.QLabel(self)
        label.setText(self.exos[i].description)
        layout.addWidget(label)
        # Espacements
        spacer = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        layout.addItem(spacer)
        layout.addItem(spacer)
        # Ajoute cet exercice à l'onglet
        self.layout.addLayout(layout, i / 2, i % 2, 1, 1)

    def reset(self):
        """Remet les compteurs à zéro"""
        for i in range(len(self.exos)):
            self.spinBox[i].setValue(0)
