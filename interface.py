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

from PyQt4 import QtCore, QtGui
from os.path import isfile, basename
import os , sys
from string import lower
from lxml import etree
import tempfile

class Ui_MainWindow(object):
    def setupUi(self, MainWindow, LesFiches,  configdir, iconesdir):
        from outils import module_path
        self.LesFiches = LesFiches
        self.configdir = configdir
        self.iconesdir=iconesdir
        self.configfile = os.path.join(configdir,  "pyromaths.xml")
        self.liste_creation=[]
        MainWindow.setStyleSheet("background-color: rgb(251, 245, 225);")
        MainWindow.setWindowIcon(QtGui.QIcon(os.path.join(iconesdir,
                'pyromaths.png')))
        MainWindow.setWindowTitle(u"Pyromaths")
        MainWindow.setGeometry(300,600, 500, 200)

        font = QtGui.QFont()
        font.setPointSize(10)
        MainWindow.setFont(font)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
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
        self.pushButton_ok.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(243, 165, 30, 255), stop:1 rgba(255, 247, 177, 255));")

        self.pushButton_quit = QtGui.QPushButton(self.centralwidget)
        self.verticalLayout.addWidget(self.pushButton_quit)
        self.pushButton_quit.setText(u"Quitter")
        self.pushButton_quit.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(243, 165, 30, 255), stop:1 rgba(255, 247, 177, 255));")

        self.pushButton_erase = QtGui.QPushButton(self.centralwidget)
        self.verticalLayout.addWidget(self.pushButton_erase)
        self.pushButton_erase.setText(u"Réinitialiser")
        self.pushButton_erase.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(243, 165, 30, 255), stop:1 rgba(255, 247, 177, 255));")

        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)

        #============================================================
        #        Onglets de la zone centrale
        #============================================================

        self.gridLayout.addLayout(self.verticalLayout, 0, 1, 1, 1)
        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget.setAutoFillBackground(True)
        self.tabWidget.setStyleSheet("background-color: rgb(251, 231, 178);")

        #============================================================
        #        Remplissage des 4 niveaux
        #============================================================

        for level in xrange(4):
            exec "self.tab_%se = QtGui.QWidget()" % (6-level)
            exec "self.gridLayout_%se = QtGui.QGridLayout(self.tab_%se)" % (6-level, 6-level)
            nb_exos = len(self.LesFiches[level][2])
            for i in xrange(nb_exos):
                self.insert_spinbox(6-level, i)
                for col in xrange(2):
                    exec "spacerItem_%s_%s = QtGui.QSpacerItem(20, 0, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)" % (6-level, col)
                    exec "self.gridLayout_%se.addItem(spacerItem_%s_%s, %s, %s, 1, 1)" % (6-level, 6-level, col, (nb_exos+1)/2, col)
            exec "self.tabWidget.addTab(self.tab_%se, \"\")" % (6-level)

        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_6e), u"6e")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_5e), u"5e")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4e), u"4e")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3e), u"3e")

        #============================================================
        #        Onglet options
        #============================================================

        ############## Onglet options

        self.tab_options = QtGui.QWidget()
        self.tabWidget.addTab(self.tab_options, "")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_options), u"Options")
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
        self.opt_titre_fiche.setText(u"Titre de la fiche d'exercices : ")
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
        self.pushButton_parcourir.setText(u"Parcourir")
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
        #self.checkBox_corrige.setEnabled(False)
        self.verticalLayout_21.addWidget(self.checkBox_corrige)

        ############## CheckBox "pdf ou non"

        self.checkBox_pdf = QtGui.QCheckBox(self.tab_options)
        self.checkBox_pdf.setText(u"Créer le pdf")
        self.checkBox_pdf.setToolTip(u"Pyromaths doit-il créer les fiches au format pdf ?")
        self.checkBox_pdf.setChecked(int(self.config['pdf']))
        self.verticalLayout_21.addWidget(self.checkBox_pdf)

        ############## Espace

        self.horizontalLayout_3.addLayout(self.verticalLayout_21)
        spacerItem13 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem13)
        self.verticalLayout_20 = QtGui.QVBoxLayout()
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.verticalLayout_18 = QtGui.QVBoxLayout()

        ############## Label niveau

        self.opt_niveau = QtGui.QLabel(self.tab_options)
        self.opt_niveau.setText(u"Niveau :")
        self.verticalLayout_18.addWidget(self.opt_niveau)

        ############## Label Modèle

        self.label_modele = QtGui.QLabel(self.tab_options)
        self.label_modele.setText(u"Modèle de mise en page :")
        #self.label_modele.setEnabled(False)
        self.verticalLayout_18.addWidget(self.label_modele)
        self.horizontalLayout_2.addLayout(self.verticalLayout_18)

        ############## Layout pour les noms d'options, en bas à droite

        self.verticalLayout_19 = QtGui.QVBoxLayout()

        ############## ComboBox niveau

        self.comboBox_niveau = QtGui.QComboBox(self.tab_options)
        self.comboBox_niveau.setEditable(True) # l’utilisateur peut entrer son propre texte
        self.comboBox_niveau.addItem(QtCore.QString())
        self.comboBox_niveau.setItemText(0, u"6\\ieme")
        self.comboBox_niveau.addItem(QtCore.QString())
        self.comboBox_niveau.setItemText(1, u"5\\ieme")
        self.comboBox_niveau.addItem(QtCore.QString())
        self.comboBox_niveau.setItemText(2, u"4\\ieme")
        self.comboBox_niveau.addItem(QtCore.QString())
        self.comboBox_niveau.setItemText(3, u"3\\ieme")
        self.comboBox_niveau.addItem(QtCore.QString())
        self.comboBox_niveau.setItemText(4, u"2$^{nde}$")
        self.verticalLayout_19.addWidget(self.comboBox_niveau)

        ############## ComboBox modèles

        self.comboBox_modele = QtGui.QComboBox(self.tab_options)

        modeles = os.listdir(os.path.join(module_path(), 'modeles'))
        modeles_home = os.listdir(os.path.join(configdir,  'modeles'))

        count = 0

        for element in modeles:
          if element[len(element)-3:] == "tex":
             self.comboBox_modele.addItem(QtCore.QString())
             self.comboBox_modele.setItemText(count, unicode(element[:len(element)-4]))
             if element == self.config['modele']:
               self.comboBox_modele.setCurrentIndex(count)
             count += 1


	for element in modeles_home:
          if element[len(element)-3:] == "tex":
             self.comboBox_modele.addItem(QtCore.QString())
             self.comboBox_modele.setItemText(count, unicode(element[:len(element)-4]))
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
        self.menubar.setStyleSheet("background-color: rgb(251, 231, 178);")
        MainWindow.setMenuBar(self.menubar)

        self.menuFichier = QtGui.QMenu(self.menubar)
        self.menuFichier.setTitle(u"Fichier")

        self.menu_propos = QtGui.QMenu(self.menubar)
        self.menu_propos.setTitle(u"Aide")

        self.statusbar = QtGui.QStatusBar(MainWindow)
        MainWindow.setStatusBar(self.statusbar)
        self.statusbar.setStyleSheet("background-color: rgb(251, 231, 178);")

        #============================================================
        #        Menus de la barre de menus
        #============================================================
        self.actionTous_les_exercices = QtGui.QAction(MainWindow)
        self.actionTous_les_exercices.setText(u"Tous les exercices")

        self.actionQuitter = QtGui.QAction(MainWindow)
        self.actionQuitter.setText(u"Quitter")

        self.actionAcceder_au_site = QtGui.QAction(MainWindow)
        self.actionAcceder_au_site.setText(u"Accéder au site")

        self.action_a_propos = QtGui.QAction(MainWindow)
        self.action_a_propos.setText(u"À propos")

        self.menuFichier.addAction(self.actionTous_les_exercices)
        self.menuFichier.addSeparator()
        self.menuFichier.addAction(self.actionQuitter)
        self.menu_propos.addAction(self.actionAcceder_au_site)
        self.menu_propos.addSeparator()
        self.menu_propos.addAction(self.action_a_propos)
        self.menubar.addAction(self.menuFichier.menuAction())
        self.menubar.addAction(self.menu_propos.menuAction())

        #============================================================
        #    Raccourcis clavier
        #============================================================
        keyQuit = QtGui.QShortcut("Ctrl+Q", MainWindow)
        QtCore.QObject.connect(keyQuit, QtCore.SIGNAL("activated()"), QtGui.qApp,
                                                                 QtCore.SLOT("quit()"))

        #============================================================
        #    Actions des boutons et menus
        #============================================================
        QtCore.QObject.connect(self.actionTous_les_exercices, QtCore.SIGNAL("activated()"), self.creer_tous_les_exercices)
        QtCore.QObject.connect(self.actionQuitter, QtCore.SIGNAL("activated()"), QtGui.qApp,
                                                                 QtCore.SLOT("quit()"))
        QtCore.QObject.connect(self.actionAcceder_au_site, QtCore.SIGNAL("activated()"), self.site)
        QtCore.QObject.connect(self.action_a_propos, QtCore.SIGNAL("activated()"), self.about)
        QtCore.QObject.connect(self.pushButton_quit, QtCore.SIGNAL("clicked()"), QtGui.qApp,
                                                                 QtCore.SLOT("quit()"))
        QtCore.QObject.connect(self.pushButton_erase, QtCore.SIGNAL("clicked()"), self.effacer_choix_exercices)
        QtCore.QObject.connect(self.pushButton_ok,QtCore.SIGNAL("clicked()"), self.creer_les_exercices)
        QtCore.QObject.connect(self.pushButton_enr_opt,QtCore.SIGNAL("clicked()"), self.enregistrer_config)
        QtCore.QObject.connect(self.pushButton_parcourir,QtCore.SIGNAL("clicked()"), self.option_parcourir)
        #============================================================
        #        Actions des spinBox
        #============================================================
        for level in xrange(4):
            for box in xrange(len(self.LesFiches[level][2])):
                exec "QtCore.QObject.connect(self.spinBox_%s_%s, QtCore.SIGNAL(\"valueChanged(int)\"), self.setNbExos)" % (6-level, box)

        for level in xrange(4):
            nb_exos = len(self.LesFiches[level][2])
            for i in xrange(nb_exos):
                exec "self.label_%s_%s.setText(u\"%s\")" % (6-level,i,self.LesFiches[level][2][i])
                exec "self.spinBox_%s_%s.setToolTip(u\"Choisissez le nombre d\'exercices de ce type \xe0 cr\xe9er.\")"% (6-level,i)

        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    #============================================================
    #        Début des fonctions
    #============================================================

    def about(self):
        """Crée la boîte de dialogue "À propos de..." """
        version = self.lire_config('informations')['version']
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
    <span style=" text-decoration: underline;">Remerciements à :</span>
    </p>
    <p>
    <ul style="-qt-list-indent: 1;">
      <li>
      <span style=" font-weight:600;">David Robert</span> pour l'idée de départ ;
      </li>
      <li>
      <span style=" font-weight:600;">Yves Gesnel</span> pour le portage de Pyromaths sous MacOS ;
      </li>
      <li>
      <span style=" font-weight:600;">Arnaud Kientz</span> pour ses graphismes, son implication dans le code de Pyromaths et son amitié ;
      </li>
      <li>
      <span style=" font-weight:600;">Nicolas Pourcelot</span> pour ses conseils et son implication prochaine dans le code de Pyromaths ;
      </li>
      <li>
      <span style=" font-weight:600;">Guillaume Barthélémy</span> pour ses exercices ;
      </li>
      <li>
      <span style=" font-weight:600;">Jacqueline Gouguenheim-Desloy</span> a porté Pyromaths sous MacOS à ses débuts. Son soutien et son amitié nous ont été précieux. Sa disparition est une perte douloureuse pour la communauté du logiciel libre.
      </li>
    </ul>
    </p>
    <p align="center">
    <span style=" font-weight:600;">Pyromaths</span> a été développé par <span style=" font-weight:600;">Jérôme Ortais</span>.
    <br />Copyright (c) 2006.<br />
    <span style=" font-size:small;">Pyromaths est distribué sous licence GPL.</span>
    </p>
  </body>
</html>"""
        banniere = os.path.join(self.iconesdir, 'pyromaths-banniere.png')
        QtGui.QMessageBox.about(None,QtCore.QString.fromUtf8(
            'À propos de Pyromaths'), text % (banniere,  version))

    def creer_les_exercices(self):
        """Vérifie si la liste d'exercices n'est pas vide puis sélectionne les noms des fichiers exercices et
        corrigés"""
        self.valide_options()
        if self.liste_creation == [] :
            QtGui.QMessageBox.warning(None,
                                    'Attention !',  u"Veuillez sélectionner des exercices...",
                                    QtGui.QMessageBox.Ok )
        else:
            parametres = {
                                    'creer_pdf': self.checkBox_pdf.isChecked(),
                                    'titre': unicode(self.titre_fiche.text()),
                                    'corrige': self.checkBox_corrige.isChecked(),
                                    'niveau': unicode(self.comboBox_niveau.currentText()),
                                    'nom_fichier': unicode(self.nom_fichier.text()),
                                    'chemin_fichier': unicode(self.chemin_fichier.text()),
				    'modele': unicode(self.comboBox_modele.currentText() + '.tex'),
				    'configdir': self.configdir
                                    }
            #============================================================
            #        Choix de l'ordre des exercices
            #============================================================
	    list=[]
            for i in xrange(len(self.liste_creation)):
                niveau = self.liste_creation[i][0]
                exo = self.liste_creation[i][1]
                list.append("%se: %s" % (6-niveau,  self.LesFiches[niveau][2][exo]))
            form = ChoixOrdreExos(list,  self.LesFiches,  parametres)
            form.exec_()

    def creer_tous_les_exercices(self):
        """
        Créer des fiches exemples pour tous les niveaux avec tous les exercices
        dans le dossier /home/jerome/workspace/Pyromaths/src/exemples
        """
        self.valide_options()
        (f0, f1) = ("", "")
        f0 = QtGui.QFileDialog().getExistingDirectory (None, u"Dossier où créer les fiches",
                                                         self.config['chemin_fichier'], QtGui.QFileDialog.ShowDirsOnly)
        i = 0
        if f0:
            from outils import creation
            for niveau in xrange(4):
                liste = []
                for i in xrange(len(self.LesFiches[niveau][2])):
                    liste.append((niveau,  i))
                exo = os.path.join(unicode(f0), "%se.tex" % (6 - niveau))
                cor = os.path.join(unicode(f0), "%se-corrige.tex" % (6 - niveau))
                parametres = {
                                        'les_fiches': self.LesFiches,
                                        'fiche_exo': exo,
                                        'fiche_cor': cor,
                                        'liste_exos': liste,
                                        'creer_pdf': '1',
                                        'titre': u"Exemple de fiche",
                                        'niveau': "%s\\ieme" % (6-niveau),
                                        'modele': unicode(self.comboBox_modele.currentText() + '.tex'),
                                        'corrige': True,
					'configdir': self.configdir
                                        }
                creation(parametres)

    def effacer_choix_exercices(self):
        """Remet toutes les SpinBox à zéro et vide la liste d'exercices sélectionnés"""
        self.liste_creation=[]
        for level in xrange(4):
            for box in xrange(len(self.LesFiches[level][2])):
                exec "self.spinBox_%s_%s.setValue(0)" % (6-level, box)

    def enregistrer_config(self):
        """Fonction qui se charge d'enregistrer les options de l'interface dans le fichier de configuration
        après avoir complété le dictionnaire."""
        tree = etree.parse(self.configfile)
        root = tree.getroot()
        options = root.find('options')
        options .find('nom_fichier').text = unicode(self.nom_fichier.text())
        options .find('chemin_fichier').text = unicode(self.chemin_fichier.text())
        options .find('titre_fiche').text = unicode(self.titre_fiche.text())
        options .find('corrige').text = unicode(self.checkBox_corrige.isChecked())
        options .find('pdf').text  = unicode(self.checkBox_pdf.isChecked())
        options .find('modele').text = unicode(self.comboBox_modele.currentText() + '.tex')

        f = open(self.configfile,'w')
        f.write(etree.tostring(root, pretty_print=True, encoding="UTF-8", xml_declaration=True))
        f.close()

    def insert_spinbox(self, level, box):
        """Place autant de SpinBox que d'exercices pour chaque niveau et les nomme"""
        treated="%s_%s" % (level, box)
        exec "self.horizontalLayout_%s = QtGui.QHBoxLayout()" % (treated)
        exec "self.spinBox_%s = QtGui.QSpinBox(self.tab_%se)" % (treated, level)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(40)
        sizePolicy.setVerticalStretch(30)
        exec "sizePolicy.setHeightForWidth(self.spinBox_%s.sizePolicy().hasHeightForWidth())" % (treated)
        exec "self.spinBox_%s.setSizePolicy(sizePolicy)" % (treated)
        exec "self.horizontalLayout_%s.addWidget(self.spinBox_%s)" % (treated, treated)
        exec "self.label_%s = QtGui.QLabel(self.tab_%se)" % (treated, level)
        exec "self.horizontalLayout_%s.addWidget(self.label_%s)" % (treated, treated)

        exec "spacerItem_%s = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)" % (treated)
        exec "self.horizontalLayout_%s.addItem(spacerItem_%s)" % (treated, treated)
        exec "self.horizontalLayout_%s.addItem(spacerItem_%s)" % (treated, treated)

        exec "self.gridLayout_%se.addLayout(self.horizontalLayout_%s, %s, %s, 1, 1)" % (level, treated, box/2, box%2)

    def lire_config(self,  section):
        """Lis le fichier de configuration pyromaths.conf, enregistre les données dans un dictionnaire config"""
        config = {}
        tree = etree.parse(self.configfile)
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

    def setNbExos(self):
        """Modifie le nombre d'exercices dans la variable liste_creation lorsqu'on  modifie une spinBox
        et adapte le niveau affiché dans l'en-tête de la fiche en fonction du plus haut niveau d'exercice"""
        niveau=0
        self.liste_creation = []
        for level in xrange(4):
            for box in xrange(len(self.LesFiches[level][2])):
                exec "qte = self.spinBox_%s_%s.value()" % (6 - level, box)
                for i in xrange(qte):
                    exec "self.liste_creation.append((%s, %s))" % (level, box)
                    if level > niveau:
                        niveau = level
        self.comboBox_niveau.setCurrentIndex(niveau)

    def site(self):
        """Ouvre le navigatuer internet par défaut sur la page d'accueil du site http://www.pyromaths.org"""
        import webbrowser
        webbrowser.open('http://www.pyromaths.org')


    def valide_options(self):
        """Synchronise les options éventuellement saisies par l'utilisateur avec le dictionnaire de config"""
        self.config['chemin_fichier'] = self.chemin_fichier.text()
        self.config['nom_fichier'] = self.nom_fichier.text()
        self.config['titre_fiche'] = self.titre_fiche.text()
        self.config['corrige'] = self.checkBox_corrige.isChecked()
        self.config['pdf'] = self.checkBox_pdf.isChecked()


#================================================================
#        Classe ChoixOrdreExos
#================================================================

class ChoixOrdreExos(QtGui.QDialog):
    """À appeler de la façon suivante :
    form = ChoixOrdreExos(list, LesFiches, parametres)
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

    def __init__(self, list, LesFiches, parametres,  parent=None):
        self.LesFiches = LesFiches
        self.parametres = parametres
        self.lesexos = list
        #Vérifie s'il n'y a pas un seul type d'exercices
        self.bmono=True
        for i in xrange(len(list)):
            if list[0] != list[i]: self.bmono=False
        if self.bmono: #S'il ny a qu'un seul type d'exercices, pas la peine de choisir l'ordre
            self.List=QtGui.QListWidget()
            for i in xrange(len(list)):
                item = QtGui.QListWidgetItem(list[i])
                item.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable |
                              QtCore.Qt.ItemIsDragEnabled)
                self.List.addItem(item)
            self.accept()
        else:
            QtGui.QDialog.__init__(self, parent)
            self.setWindowTitle("Choisissez l'ordre des exercices")
            layout = QtGui.QHBoxLayout()

            buttonBox = QtGui.QDialogButtonBox()
            buttonBox.setOrientation(QtCore.Qt.Vertical)
            buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)

            self.List=QtGui.QListWidget()
            self.List.setAlternatingRowColors(True)
            self.List.setDragEnabled(True)
            self.List.setAcceptDrops(True)
            self.List.setDragDropMode(QtGui.QAbstractItemView.InternalMove)
            self.List.setDropIndicatorShown(True)

            for i in xrange(len(list)):
                item = QtGui.QListWidgetItem(list[i])
                item.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable |
                              QtCore.Qt.ItemIsDragEnabled)
                self.List.addItem(item)

            layout.addWidget(self.List)
            layout.addWidget(buttonBox)
            self.setLayout(layout)

            QtCore.QObject.connect(buttonBox, QtCore.SIGNAL("accepted()"), self.accept)
            QtCore.QObject.connect(buttonBox, QtCore.SIGNAL("rejected()"), self.close)

    def accept(self):
        """Écrit une liste contenant la liste des exercices dans l'ordre choisit par l'utilisateur et demande à
        celui-ci les noms de fichiers pour les exercices et les corrigés"""
	corrige = self.parametres['corrige']
        l=[]
        self.lesexos = []
        for i in xrange(self.List.count()):
            l.append(unicode(self.List.item(i).text()))
        for text in l:
            niveau = 6 - int(text[0])
            pos = self.LesFiches[niveau][2].index(text[4:])
            self.lesexos.append((niveau,  pos))

        #============================================================
        #        Choix des noms des fichiers exercices et corrigés
        #============================================================
        (f0, f1) = ("", "")
        saveas = QtGui.QFileDialog()
        if lower(os.path.splitext(self.parametres['nom_fichier'])[1]) == '.tex':
                self.parametres['nom_fichier'] = os.path.splitext(self.parametres['nom_fichier'])[0]
        f0 = unicode(saveas.getSaveFileName(None, "Enregistrer sous...",
                                            os.path.join(self.parametres['chemin_fichier'],
                                                         '%s.tex' % self.parametres['nom_fichier']),
                                            "Documents Tex (*.tex)"))
        if f0:
            if lower(os.path.splitext(f0)[1]) != '.tex':
                f0 = f0 + '.tex'
            if corrige:
                f1 = unicode(saveas.getSaveFileName(None, "Enregistrer sous...",
                                                    os.path.join(os.path.dirname(f0),
                                                    "%s-corrige.tex"  % os.path.splitext(os.path.basename(f0))[0]),
                                                    "Documents Tex (*.tex)"))
            else:
                f1 = os.path.join(os.path.dirname(f0), 'temp.tex')
            if f1:
                if corrige:
                  if lower(os.path.splitext(f1)[1]) != '.tex':
                    f1 = f1 + '.tex'
                from outils import creation
                self.parametres ['fiche_exo'] = f0
                self.parametres ['fiche_cor'] = f1
                self.parametres ['liste_exos'] = self.lesexos
                self.parametres ['les_fiches'] =  self.LesFiches
                creation(self.parametres)
                if not self.bmono:
                  self.close()
            elif not self.bmono:
                self.close()
        elif not self.bmono:
            self.close()

