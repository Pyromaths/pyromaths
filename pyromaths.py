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

from PyQt4 import QtCore, QtGui
import sys,  os,  string,  codecs
from lxml import etree
from re import sub, findall

from interface import Ui_MainWindow
from pyro_classes import WriteFiles
import troisiemes.troisiemes
import quatriemes.quatriemes
import cinquiemes.cinquiemes
import sixiemes.sixiemes

#================================================================
#        Cas d'une installation de Pyromaths via deb ou rpm, il faut ajouter les modules au PATH
#================================================================

if os.name == "posix":
    if os.path.basename(__file__)=="pyromaths":
        sys.path.append(os.path.join( os.path.dirname(__file__),
                        "../lib/pyromaths"))

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
u'Théorème de Pythagore',
u'Réciproque du théorème de Pythagore',
u'Cercle et théorème de Pythagore',
u'Théorème de Thalès',
u'Réciproque du théorème de Thalès',
u'Trigonométrie',
]]]

#================================================================
#        Vérifie la présence des programmes nécessaires à la compilation des fichiers TeX
#================================================================
def creation(parametres):
    """Création et compilation des fiches d'exercices.
    parametres = {'fiche_exo': f0,
                            'fiche_cor': f1,
                            'liste_exos': self.lesexos,
                            'creer_pdf': self.checkBox_create_pdf.checkState(),
                            'titre': unicode(self.lineEdit_titre.text()),
                            'niveau': unicode(self.comboBox_niveau.currentText()),
                            }"""
    f0 = parametres['fiche_exo']
    f1 = parametres['fiche_cor']
    creer_pdf = parametres['creer_pdf']
    fiche_metapost = os.path.splitext(f0)[0] + '.mp'
    files = WriteFiles(f0, f1, fiche_metapost, creer_pdf)
    if creer_pdf:
        files.f0.write(u"\\chead{\\Large{\\textsc{")
        files.f0.write(parametres['titre'].encode('latin1'))
        files.f0.write(u"}}}\n")
        files.f1.write("\\chead{\\Large{\\textsc{")
        files.f1.write(parametres['titre'].encode('latin1'))
        files.f1.write(u" - corrigé}}}\n".encode('latin1'))
        files.f0.write(u"\\rhead{\\textsl{\\footnotesize{Classe de %s}}}\n" % parametres['niveau'])
        files.f1.write(u"\\rhead{\\textsl{\\footnotesize{Classe de %s}}}\n" % parametres['niveau'])

    for exo in parametres['liste_exos']:
        print exo
        LesFiches[exo[0]][1].main(exo[1], files)
    WriteFiles.close(files)
    if parametres['creer_pdf']:
        from subprocess import call
        dir0=os.path.dirname(f0)
        f0noext=os.path.splitext(f0)[0]
        dir1=os.path.dirname(f1)
        f1noext=os.path.splitext(f1)[0]

        for i in xrange(2):
            os.chdir(dir0)
            call(["latex", "-interaction=batchmode", str(f0)], env={"PATH": os.path.expandvars('$PATH')})
            os.chdir(dir1)
            call(["latex", "-interaction=batchmode", str(f1)],
                                                         env={"PATH": os.path.expandvars('$PATH')})
        call(["dvips", "-q", "%s.dvi" % (f0noext)], env={"PATH": os.path.expandvars('$PATH')})
        call(["dvips", "-q", "%s.dvi" % (f1noext)], env={"PATH": os.path.expandvars('$PATH')})
        call(["ps2pdf", "-sPAPERSIZE#a4", "%s.ps" % (f0noext), "%s.pdf" % (f0noext)],
                                                                            env={"PATH": os.path.expandvars('$PATH')})
        call(["ps2pdf", "-sPAPERSIZE#a4", "%s.ps" % (f1noext), "%s.pdf" % (f1noext)],
                                                                            env={"PATH": os.path.expandvars('$PATH')})
        if os.name == "nt":  #Cas de Windows.
            os.startfile('%s.pdf' % (f0noext))
            os.startfile('%s.pdf' % (f1noext))
        else:
            os.system('xdg-open %s.pdf' % (f0noext))
            os.system('xdg-open %s.pdf' % (f1noext))
        #Supprime les fichiers temporaires créés par LaTeX
        try:
            for ext in ('.aux', '.dvi', '.log', '.out', '.ps'):
                os.remove(os.path.join(dir0,  f0noext + ext))
                os.remove(os.path.join(dir1,  f1noext + ext))
        except OSError:
            print u"Le fichier %s ou %s n'a pas été supprimé." % (os.path.join(dir0,  f0noext + ext),
                                                                  os.path.join(dir1,  f1noext + ext))
                                                                  #le fichier à supprimer n'existe pas.

#================================================================
#        Gestion du fichier de configuration de Pyromaths
#================================================================
def create_config_file():
    """Crée le fichier de configuration au format xml"""
    root = etree.Element(u"pyromaths")

    child = etree.SubElement(root, u"options")
    etree.SubElement(child, u"nom_fichier").text=u"exercices"
    etree.SubElement(child, u"chemin_fichier").text=u"%s" % home()
    etree.SubElement(child, u"titre_fiche").text=u"Fiche de révision"
    etree.SubElement(child, u"corrige").text=u"True"
    etree.SubElement(child, u"pdf").text=u"True"
    etree.SubElement(child, u"numeroter").text=u"True"
    etree.SubElement(child, u"modele").text=u"Défaut"

    child = etree.SubElement(root, u"informations")
    etree.SubElement(child, u"version").text=u"09.03"
    etree.SubElement(child, u"description").text=u"Pyromaths est un programme qui permet de générer des fiches d’exercices de mathématiques de collège ainsi que leur corrigé. Il crée des fichiers au format pdf qui peuvent ensuite être imprimés ou lus sur écran."
    etree.SubElement(child, u"icone").text=u"pyromaths.ico"

    subchild= etree.SubElement(child, u"auteur")
    etree.SubElement(subchild, u"nom").text=u"Jérôme Ortais"
    etree.SubElement(subchild, u"email").text=u"jerome.ortais@pyromaths.org"
    etree.SubElement(subchild, u"site").text=u"http://www.pyromaths.org"

    return etree.tostring(root, pretty_print=True, encoding="UTF-8", xml_declaration=True)

def indent(elem, level=0):
    """Indente correctement les fichiers xml.
    By Filip Salomonsson; published on February 06, 2007.
    http://infix.se/2007/02/06/gentlemen-indent-your-xml"""
    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        for e in elem:
            indent(e, level+1)
            if not e.tail or not e.tail.strip():
                e.tail = i + "  "
        if not e.tail or not e.tail.strip():
            e.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i
    return elem

def modify_config_file(file):
    """Modifie le fichier de configuration si besoin, excepté les options utilisateur déjà configurées"""
    modifie = False
    oldtree = etree.parse(file)
    oldroot = oldtree.getroot()
    newroot = etree.XML(create_config_file())
    for element in newroot.iter(tag=etree.Element):
        if not len(element):
            parents = [element]
            e = element.getparent()
            while e is not None:
                parents.insert(0,e)
                e = e.getparent()
            oldtag = oldroot
            for i in xrange(1, len(parents)):
                if oldtag.find(parents[i].tag) is None and i < len(parents) - 1 :
                    if i > 1:
                        etree.SubElement(oldroot.find(parents[i-1].tag), parents[i].tag)
                    else:
                        etree.SubElement(oldroot, parents[i].tag)
                    oldtag = oldtag.find(parents[i].tag)
                else:
                    oldtag = oldtag.find(parents[i].tag)
                if i == len(parents)-2: oldparent = oldtag
            if oldtag is None:
                # Ajoute un nouvel item dans le fichier xml
                modifie = True
                etree.SubElement(oldparent, element.tag).text =  element.text
            elif oldtag.text != element.text and parents[1].tag != "options":
                # Modifie un item existant s'il ne s'agit pas des options
                modifie = True
                oldtag.text =  element.text
    if modifie:
        f = open(os.path.join(configdir(),  "pyromaths.xml"),'w')
        f.write(etree.tostring(indent(oldroot), pretty_print=True, encoding="UTF-8", xml_declaration=True))
        f.close()

def copie_modele(source, destination):
    """Copie le contenu d'un modèle dans un nouveau fichier tex, en remplaçant les mots-clés par leur valeur, soit dans le fichier de config, soit les exercices."""
    fs = open(source, 'r')
    fd = open(destination, 'w')
    while 1:
        txt = fs.readline()
        if txt =="":
            break
        temp = re.findall('##{{[A-Z]*}}##',txt)
        if temp:
          occ = temp[0][4:len(temp)-5].lower()
        else:
          occ = ""
        ### Il faut encore ajouter un filtre pour différencier mots-clés du dico et exercices
        txt = re.sub('##{{[A-Z]*}}##',occ,txt)
        fd.write(txt)
    fs.close()
    fd.close()
    return

class StartQT4(QtGui.QMainWindow):
    def __init__(self, LesFiches, configdir,  parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self, LesFiches,  configdir)

if __name__ == "__main__":
    if os.name == 'nt':
        def home():
            return os.environ['HOMEPATH']
        def configdir():
            return os.path.join(os.environ['APPDATA'],"pyromaths")
    else:
        def home():
            return os.environ['HOME']
        def configdir():
            return os.path.join(home(),  ".config", "pyromaths")
    if not os.access(os.path.join(configdir(),  "pyromaths.xml"), os.R_OK):
        if not os.path.isdir(configdir()):
            os.makedirs(configdir())
        f = open(os.path.join(configdir(),  "pyromaths.xml"),'w')
        f.write(create_config_file())
        f.close()
    modify_config_file(os.path.join(configdir(),  "pyromaths.xml"))
    app = QtGui.QApplication(sys.argv)
    #Traduction de l'interface dans la langue de l'OS
    locale = QtCore.QLocale.system().name()
    translator=QtCore.QTranslator ()
    translator.load(QtCore.QString("qt_") + locale,
                    QtCore.QLibraryInfo.location(QtCore.QLibraryInfo.TranslationsPath))
    app.installTranslator(translator)

    pyromaths = StartQT4(LesFiches,  configdir())
    pyromaths.show()
    sys.exit(app.exec_())

#FIXED: drag&drop - problème de fenêtres
#TODO: modèles
#TODO: numérotation
#TODO: créer le corrigé
#TODO: créer le pdf
