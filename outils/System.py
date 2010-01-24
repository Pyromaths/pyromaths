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

import sys,  os,  codecs
from lxml import etree
from lxml import _elementpath as DONTUSE # Astuce pour inclure lxml dans Py2exe
from re import sub, findall
from outils.TexFiles import mise_en_forme

## Création des chemins suivant les OS
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

#==============================================================
#        Gestion des extensiosn de fichiers
#==============================================================
def supprime_extension(filename,  ext):
    """supprime l'éventuelle extension ext du nom de fichier filename.
    ext est de la forme '.tex'"""
    if os.path.splitext(filename)[1].lower():
        return os.path.splitext(filename)[0]
    return filename

def ajoute_extension(filename,  ext):
    """ajoute si nécessaire l'extension ext au nom de fichier filename.
    ext est de la forme '.tex'"""
    if os.path.splitext(filename)[1].lower() == ext:
        return filename
    return filename + ext

#==============================================================
#        Gestion du fichier de configuration de Pyromaths
#==============================================================
def create_config_file():
    """Crée le fichier de configuration au format xml"""
    root = etree.Element("pyromaths")

    child = etree.SubElement(root, "options")
    etree.SubElement(child, "nom_fichier").text="exercices"
    etree.SubElement(child, "chemin_fichier").text="%s" % home()
    etree.SubElement(child, "titre_fiche").text=u"Fiche de révisions"
    etree.SubElement(child, "corrige").text="True"
    etree.SubElement(child, "pdf").text="True"
    etree.SubElement(child, "modele").text="pyromaths.tex"

    child = etree.SubElement(root, "informations")
    etree.SubElement(child, "version").text="10.01"
    etree.SubElement(child, "description").text=u"Pyromaths est un programme qui permet de générer des fiches d’exercices de mathématiques de collège ainsi que leur corrigé. Il crée des fichiers au format pdf qui peuvent ensuite être imprimés ou lus sur écran."
    etree.SubElement(child, "icone").text="pyromaths.ico"

    subchild= etree.SubElement(child, "auteur")
    etree.SubElement(subchild, "nom").text=u"Jérôme Ortais"
    etree.SubElement(subchild, "email").text=u"jerome.ortais@pyromaths.org"
    etree.SubElement(subchild, "site").text="http://www.pyromaths.org"

    return etree.tostring(root, pretty_print=True, encoding="UTF-8", xml_declaration=True).decode('utf-8', 'strict')

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
            for i in range(1, len(parents)):
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
        f = codecs.open(os.path.join(configdir(), "pyromaths.xml"), encoding='utf-8', mode = 'w')
        f.write(etree.tostring(indent(oldroot), pretty_print=True, encoding="utf-8", xml_declaration=True).decode('utf-8', 'strict'))
        f.close()

#==============================================================
#        Créer et lance la compilation des fichiers TeX
#==============================================================
def creation(parametres):
    """Création et compilation des fiches d'exercices.
    parametres = {'fiche_exo': f0,
                  'fiche_cor': f1,
                  'liste_exos': self.lesexos,
                  'creer_pdf': self.checkBox_create_pdf.checkState(),
                  'titre': unicode(self.lineEdit_titre.text()),
                  'niveau': unicode(self.comboBox_niveau.currentText()),
                }"""
    exo = parametres['fiche_exo']
    cor = parametres['fiche_cor']
    f0 = codecs.open(unicode(exo), encoding='utf-8', mode='w')
    f1 = codecs.open(unicode(cor), encoding='utf-8', mode='w')
    titre = parametres['titre']
    fiche_metapost = os.path.splitext(exo)[0] + '.mp'

    if parametres['creer_pdf']:
        copie_tronq_modele(f0, parametres, 'entete')
        copie_tronq_modele(f1, parametres, 'entete')

    for exercice in parametres['liste_exos']:
        parametres['les_fiches'][exercice[0]][1].main(exercice[1], f0, f1)

    if parametres['creer_pdf']:
        copie_tronq_modele(f0, parametres, 'pied')
        copie_tronq_modele(f1, parametres, 'pied')

    f0.close()
    f1.close()

    # indentation des fichiers teX créés
    mise_en_forme(unicode(exo))
    if parametres['corrige']:
        mise_en_forme(unicode(cor))

    # Dossiers et fichiers d'enregistrement, définitions qui doivent rester avant le if suivant.
    dir0=os.path.dirname(exo)
    dir1=os.path.dirname(cor)
    f0noext=os.path.splitext(exo)[0]
    f1noext=os.path.splitext(cor)[0]

    if parametres['creer_pdf']:
        from subprocess import call

        for i in range(2):
            os.chdir(dir0)
            log = open('pyromaths.log', 'w')
            call(["latex", "-interaction=batchmode", str(exo)],
                    #env={"PATH": os.path.expandvars('$PATH')},
                    stdout=log)
            if parametres['corrige']:
                os.chdir(dir1)
                call(["latex", "-interaction=batchmode", str(cor)],
                        #env={"PATH": os.path.expandvars('$PATH')},
                        stdout=log)
        call(["dvips", "-q", "%s.dvi" % (f0noext), "-o%s.ps" % (f0noext)],
                #env={"PATH": os.path.expandvars('$PATH')},
                stdout=log)
        if parametres['corrige']:
            call(["dvips", "-q", "%s.dvi" % (f1noext), "-o%s.ps" % (f1noext)],
                    #env={"PATH": os.path.expandvars('$PATH')},
                    stdout=log)
        call(["ps2pdf", "-sPAPERSIZE#a4", "%s.ps" % (f0noext),
                    "%s.pdf" % (f0noext)],
                    #env={"PATH": os.path.expandvars('$PATH')},
                    stdout=log)
        if parametres['corrige']:
            call(["ps2pdf", "-sPAPERSIZE#a4", "%s.ps" % (f1noext),
                "%s.pdf" % (f1noext)],
                #env={"PATH": os.path.expandvars('$PATH')},
                stdout=log)
        log.close()
        if os.name == "nt":  #Cas de Windows.
            os.startfile('%s.pdf' % (f0noext))
            if parametres['corrige']:
                os.startfile('%s.pdf' % (f1noext))
        else:
            os.system('xdg-open %s.pdf' % (f0noext))
            if parametres['corrige']:
                os.system('xdg-open %s.pdf' % (f1noext))
        #Supprime les fichiers temporaires créés par LaTeX
        try:
            for ext in ('.aux', '.dvi', '.log', '.out', '.ps'):
                os.remove(os.path.join(dir0,  f0noext + ext))
                if parametres['corrige']:
                    os.remove(os.path.join(dir1,  f1noext + ext))
            os.remove(os.path.join(dir0, 'pyromaths.log'))
        except OSError:
            print(("Le fichier %s ou %s n'a pas été supprimé." % \
                   (os.path.join(dir0,  f0noext + ext),
                   os.path.join(dir1,  f1noext + ext))))
                   #le fichier à supprimer n'existe pas.
    if not parametres['corrige']:
        os.remove(os.path.join(dir1,  f1noext + '.tex'))

def copie_tronq_modele(dest, parametres, master):
    """Copie des morceaux des modèles, suivant le schéma du master."""
    master_fin = '% fin ' + master
    master = '% ' + master
    n = 0

    ## Liste des modèles pyromaths
    liste_modeles_pyromaths = ['evaluation.tex', 'pyromaths.tex']

    ## Le fichier source doit être un modèle, donc il se trouve dans le dossier 'modeles' de pyromaths.
    source = parametres['modele']

    if source in liste_modeles_pyromaths:
        source = os.path.join(module_path(), 'modeles', source)
    else:
        source = os.path.join(parametres['configdir'], 'modeles', source)

    ## La destination est le fichier temporaire.

    ## Les variables à remplacer :
    titre = parametres['titre']
    niveau = parametres['niveau']
    modele = codecs.open(source, encoding='utf-8', mode='r')
    for line in modele:
        if master_fin in line:
            break
        if n > 0:
            temp = findall('##{{[A-Z]*}}##',line)
            if temp:
                occ = temp[0][4:len(temp)-5].lower()
                line = sub('##{{[A-Z]*}}##',eval(occ),line)
            dest.write(line)

        if master in line:
            n = 1

    modele.close()
    return

#==============================================================
#        Compilation de la version win32
#==============================================================

def we_are_frozen():
    """Returns whether we are frozen via py2exe.
    This will affect how we find out where we are located."""
    return hasattr(sys, "frozen")

def module_path():
    """ This will get us the program's directory,
    even if we are frozen using py2exe"""

    if we_are_frozen():
        return os.path.dirname(unicode(sys.executable,
                                sys.getfilesystemencoding( )))

    #return os.path.dirname(str(__file__,
    #                                sys.getfilesystemencoding( )))
    return os.path.join(os.path.dirname(str(__file__)),  '..')

