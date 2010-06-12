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
        return unicode(os.environ['USERPROFILE'],sys.getfilesystemencoding())
    def configdir():
        return os.path.join(os.environ['APPDATA'],"pyromaths")
elif sys.platform == "darwin":  #Cas de Mac OS X.
    def home():
        return unicode(os.environ['HOME'],sys.getfilesystemencoding())
    def configdir():
        return os.path.join(home(),  "Library", "Application Support", "Pyromaths")
else:
    def home():
        return unicode(os.environ['HOME'],sys.getfilesystemencoding())
    def configdir():
        return os.path.join(home(),  ".config", "pyromaths")

#==============================================================
#        Gestion des extensions de fichiers
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
    etree.SubElement(child, "unpdf").text="False"
    etree.SubElement(child, "modele").text="pyromaths.tex"

    child = etree.SubElement(root, "informations")
    etree.SubElement(child, "version").text="10.06-1"
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
                  'creer_unpdf': self.checkBox_unpdf.isChecked() and self.checkBox_unpdf.isEnabled(),
                  'titre': unicode(self.lineEdit_titre.text()),
                  'niveau': unicode(self.comboBox_niveau.currentText()),
                }"""
    exo = unicode(parametres['fiche_exo'])
    cor = unicode(parametres['fiche_cor'])
    print cor
    f0 = codecs.open(exo, encoding='utf-8', mode='w')
    f1 = codecs.open(cor, encoding='utf-8', mode='w')
    titre = parametres['titre']
    fiche_metapost = os.path.splitext(exo)[0] + '.mp'

    if parametres['creer_pdf']:
        copie_tronq_modele(f0, parametres, 'entete')
        if not parametres['creer_unpdf']:
            copie_tronq_modele(f1, parametres, 'entete')

    for exercice in parametres['liste_exos']:
        parametres['les_fiches'][exercice[0]][1].main(exercice[1], f0, f1)

    if parametres['creer_pdf']:
        if parametres['creer_unpdf']:
            f0.write("\\label{LastPage}\n")
            f0.write("\\newpage\n")
            f0.write("\\lhead{\\textsl{\\footnotesize{Page \\thepage/ \\pageref{LastCorPage}}}}\n")
            f0.write("\\setcounter{page}{1} ")
            f0.write("\\setcounter{exo}{0}\n")
            f1.write("\\label{LastCorPage}\n")
            copie_tronq_modele(f1, parametres, 'pied')
        else:
            f0.write("\\label{LastPage}\n")
            f1.write("\\label{LastPage}\n")
            copie_tronq_modele(f0, parametres, 'pied')
            copie_tronq_modele(f1, parametres, 'pied')

    f0.close()
    f1.close()

    if parametres['creer_unpdf']:
        f0 = codecs.open(exo, encoding='utf-8', mode='a')
        f1 = codecs.open(cor, encoding='utf-8', mode='r')
        for line in f1:
            f0.write(line)
        f0.close()
        f1.close()

    # indentation des fichiers teX créés
    mise_en_forme(exo)
    if parametres['corrige'] and not parametres['creer_unpdf']:
        mise_en_forme(cor)

    # Dossiers et fichiers d'enregistrement, définitions qui doivent rester avant le if suivant.
    dir0=os.path.dirname(exo)
    dir1=os.path.dirname(cor)
    f0noext=os.path.splitext(os.path.basename(exo))[0].encode(sys.getfilesystemencoding())
    f1noext=os.path.splitext(os.path.basename(cor))[0].encode(sys.getfilesystemencoding())

    if parametres['creer_pdf']:
        from subprocess import call

        os.chdir(dir0)
        log = open('%s-pyromaths.log' % f0noext, 'w')
        for i in range(2):
            call(["latex", "-interaction=batchmode", "%s.tex" % f0noext], stdout=log)
        call(["dvips", "-q", "%s.dvi" % f0noext, "-o%s.ps" % f0noext], stdout=log)
        call(["ps2pdf", "-sPAPERSIZE#a4", "%s.ps" % f0noext, "%s.pdf" % f0noext], stdout=log)
        log.close()
        nettoyage(f0noext)
        if os.name == "nt":  #Cas de Windows.
            os.startfile('%s.pdf' % f0noext)
        elif sys.platform == "darwin":  #Cas de Mac OS X.
            os.system('open %s.pdf' % f0noext)
        else:
            os.system('xdg-open %s.pdf' % f0noext)

        if parametres['corrige'] and not parametres['creer_unpdf']:
            os.chdir(dir1)
            log = open('%s-pyromaths.log' % f1noext, 'w')
            for i in range(2):
                call(["latex", "-interaction=batchmode", "%s.tex" % f1noext], stdout=log)
            call(["dvips", "-q", "%s.dvi" % f1noext, "-o%s.ps" % f1noext], stdout=log)
            call(["ps2pdf", "-sPAPERSIZE#a4", "%s.ps" % f1noext, "%s.pdf" % f1noext], stdout=log)
            log.close()
            nettoyage(f1noext)
            if os.name == "nt":  #Cas de Windows.
                os.startfile('%s.pdf' % f1noext)
            elif sys.platform == "darwin":  #Cas de Mac OS X.
                os.system('open %s.pdf' % f1noext)
            else:
                os.system('xdg-open %s.pdf' % f1noext)
        else:
            os.remove(cor)

def nettoyage(basefilename):
    """Supprime les fichiers temporaires créés par LaTeX"""
    try:
        for ext in ('.aux', '.dvi', '.out', '.ps'):
            os.remove(basefilename+ext)
        if os.path.getsize('%s.pdf' % basefilename) > 1000 :
            os.remove('%s.log' % basefilename)
            os.remove('%s-pyromaths.log' % basefilename)
    except OSError:
        pass
        #le fichier à supprimer n'existe pas et on s'en fout.


def copie_tronq_modele(dest, parametres, master):
    """Copie des morceaux des modèles, suivant le schéma du master."""
    master_fin = '% fin ' + master
    master = '% ' + master
    n = 0

    ## Le fichier source doit être un modèle, donc il se trouve dans le dossier 'modeles' de pyromaths.
    source = parametres['modele']

    if os.path.isfile(os.path.join(parametres['configdir'], 'modeles',source)):
        source = os.path.join(parametres['configdir'], 'modeles', source)
    elif os.path.isfile(os.path.join(module_path(), 'modeles', source)):
        source = os.path.join(module_path(), 'modeles', source)
    else:
        #TODO: Message d'erreur, le modèle demandé n'existe pas
        print(u"Le fichier modèle n'a pas été trouvé dans %s" %
                os.path.join(module_path(), 'modeles'))

    ## Les variables à remplacer :
    titre = parametres['titre']
    niveau = parametres['niveau']
    if os.name == 'nt':
        os.environ['TEXINPUTS']= os.path.normpath(os.path.join(module_path(),
            'modeles'))
        tabvar = 'tabvar.tex'
    else:
        tabvar = os.path.normpath(os.path.join(module_path(), 'modeles',
            'tabvar.tex'))
    #rawstring pour \tabvar -> tab + abvarsous windows
    modele = codecs.open(source, encoding='utf-8', mode='r')
    for line in modele:
        if master_fin in line:
            break
        if n > 0:
            temp = findall('##{{[A-Z]*}}##',line)
            if temp:
                occ = temp[0][4:len(temp)-5].lower()
                #line = sub('##{{[A-Z]*}}##',eval(occ),line)
                line = line.replace(temp[0], eval(occ))
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
        return os.path.normpath(os.path.dirname(unicode(sys.executable,
            sys.getfilesystemencoding())))

    #return os.path.dirname(str(__file__,
    #                                sys.getfilesystemencoding( )))
    return os.path.normpath(os.path.join(os.path.dirname(str(__file__)), '..'))

