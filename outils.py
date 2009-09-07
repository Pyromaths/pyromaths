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
# ------------------- OUTILS -------------------

from random import randrange
import string
import os,  sys
import math
from lxml import etree
from lxml import _elementpath as DONTUSE # Astuce pour inclure lxml dans Py2exe
from re import sub, findall



def ecrit_tex(file, formule, cadre=None, thenocalcul='\\thenocalcul = ',
              tabs=1):

                        # ecrit la ligne dans le fichier

    if formule != '':
        if cadre == None or not cadre:
            file.write(('  \\[ %s%s \\] \n').expandtabs(2 * tabs) % (thenocalcul,
                       formule))
        else:
            file.write(('  \\[ \\boxed{%s%s} \\] \n').expandtabs(2 *
                       tabs) % (thenocalcul, formule))


def pgcd(a, b):  # calcule le pgcd positif des nombres entiers a et b
    (a, b) = (abs(a), abs(b))
    if a < b:
        (a, b) = (b, a)
    while b > 0:
        (a, b) = (b, a % b)
    return abs(a)


def ppcm(a, b):  # calcule le ppcm positif des nombres entiers a et b
    return abs((a * b) / pgcd(a, b))


def signe(a):  # renvoie 1 si a est>0, -1 si a<0
    if a < 0:
        return -1
    else:
        return 1


def valeur_alea(a, b):  # choisit une valeur comprise entre a et b non nulle
    while True:
        alea = randrange(a, b + 1)
        if alea != 0:
            return alea
            break


def tex_entete(fichier):  #ecrit l'entete du document tex
    fichier.write('\\documentclass[a4paper,11pt]{article}\n')
    fichier.write('\\usepackage[latin1]{inputenc}\n')
    fichier.write('\\usepackage[frenchb]{babel}\n')
    fichier.write('\\usepackage[fleqn]{amsmath}\n')
    fichier.write('\\usepackage{amssymb,multicol,calc,vmargin,cancel,fancyhdr,units,pst-eucl,wrapfig,lastpage,wasysym,pst-plot,tabularx}\n')
    fichier.write('\\setmarginsrb{1.5cm}{1.5cm}{1.5cm}{1.5cm}{.5cm}{.5cm}{.5cm}{1.cm}\n')
    fichier.write('\\newcounter{exo}\n')
    fichier.write('\\setlength{\\headheight}{18pt}\n')
    fichier.write('\\setlength{\\fboxsep}{1em}\n')
    fichier.write('\\setlength\\parindent{0em}\n')
    fichier.write('\\setlength\\mathindent{0em}\n')
    fichier.write('\\setlength{\\columnsep}{30pt}\n')
    fichier.write('\\usepackage[ps2pdf,pagebackref=true,colorlinks=true,linkcolor=blue,plainpages=true]{hyperref}\n')
    fichier.write('\\hypersetup{pdfauthor={J\xe9r\xf4me Ortais},pdfsubject={Exercices de math\xe9matiques},')
    fichier.write('pdftitle={Exercices cr\xe9\xe9s par Pyromaths, un programme en Python de J\xe9r\\^ome Ortais}}\n')
    fichier.write('\\makeatletter\n')
    fichier.write('\\newcommand\\styleexo[1][]{\n')
    fichier.write('  \\renewcommand{\\theenumi}{\\arabic{enumi}}\n')
    fichier.write('  \\renewcommand{\\labelenumi}{$\\blacktriangleright$\\textbf{\\theenumi.}}\n')
    fichier.write('  \\renewcommand{\\theenumii}{\\alph{enumii}}\n')
    fichier.write('  \\renewcommand{\\labelenumii}{\\textbf{\\theenumii)}}\n')
    fichier.write('  {\\fontfamily{pag}\\fontseries{b}\\selectfont \\underline{#1 \\theexo}}\n')
    fichier.write('  \\par\\@afterheading\\vspace{0.5\\baselineskip minus 0.2\\baselineskip}}\n')

    fichier.write('\\newcommand*\\exercice{%\n')
    fichier.write('  \\psset{unit=1cm}\n')
    fichier.write('  \\ifthenelse{\\equal{\\theexo}{0}}{}{\\filbreak}\n')
    fichier.write('  \\refstepcounter{exo}%\n')
    fichier.write('  \\par\\addvspace{1.5\\baselineskip minus 1\\baselineskip}%\n')
    fichier.write('  \\@ifstar%\n')
    fichier.write('  {\\penalty-130\\styleexo[Corrig\xe9 de l\'exercice]}%\n')
    fichier.write('  {\\filbreak\\styleexo[Exercice]}%\n')
    fichier.write('  }\n')

    fichier.write('\\makeatother\n')
    fichier.write('\\count1=\\year \\count2=\\year \\ifnum\\month<8\\advance\\count1by-1\\else\\advance\\count2by1\\fi\n')
    fichier.write('\\pagestyle{fancy}\n')
    fichier.write('\\cfoot{\\textsl{\\footnotesize{Ann\xe9e \\number\\count1/\\number\\count2}}}\n')
    fichier.write('\\rfoot{\\textsl{\\tiny{http://www.pyromaths.org}}}\n')
    fichier.write('\\lhead{\\textsl{\\footnotesize{Page \\thepage/ \\pageref{LastPage}}}}\n')
    fichier.write('\\begin{document}\n')
    fichier.write('\\newcounter{nocalcul}[exo]\n')
    fichier.write('''\\renewcommand{\\thenocalcul}{\\Alph{nocalcul}}
\\raggedcolumns
''')


#def pyromin(a, b):
#    if a < b:
#        return a
#    else:
#        return b
#
#
#def pyromax(a, b):
#    if a > b:
#        return a
#    else:
#        return b


def sepmilliers(nb, mathenvironment=0):

    # Insère les espaces fines pour séparer les milliers et remplace le point
    # décimal par une virgule

    dec = [str(nb)[i] for i in xrange(len(str(nb)))]
    if dec.count('e'):  #nb ecrit en notation scientifique
        exposant = int(('').join(dec[dec.index('e') + 1:]))
        dec = dec[:dec.index('e')]
        lg = len(dec)
        if dec.count('.'):
            virg = dec.index('.')
            dec.remove('.')
        else:
            virg = len(dec)
        if virg + exposant < 0:  #L'ecriture decimale du nombre commence par 0,...
            dec2 = ['0', '.']
            for i in xrange(-virg - exposant):
                dec2.append('0')
            dec2.extend(dec)
            dec = dec2
        elif virg + exposant > lg:

            #L'ecriture decimale du nombre finit par des 0

            for i in xrange(-((lg - virg) - 1) + exposant):
                dec.append('0')
    dec2 = []
    if dec.count('.'):
        lavtvirg = dec.index('.')
        laprvirg = (len(dec) - dec.index('.')) - 1
    else:
        lavtvirg = len(dec)
        laprvirg = 0
    nbsep = lavtvirg // 3 + 1
    if lavtvirg > 3:
        cpt = lavtvirg % 3
        if cpt:
            dec2 = dec[0:cpt]
            dec2.append('\\,')
            nbsep = nbsep - 1
        for i in xrange(nbsep):
            dec2.extend(dec[cpt:cpt + 3])
            if nbsep - i > 1:
                dec2.append('\\,')
            cpt = cpt + 3
    else:
        if dec.count('.'):
            dec2 = dec[0:dec.index('.')]
        else:
            dec2 = dec
    if dec.count('.'):
        cpt = dec.index('.')
    else:
        cpt = len(dec)
    if laprvirg <= 3:
        dec2.extend(dec[cpt:])
    else:
        nbsep = laprvirg // 3 - 1
        dec2.extend(dec[cpt:cpt + 4])
        dec2.append('\\,')
        cpt = cpt + 4
        for i in xrange(nbsep):
            dec2.extend(dec[cpt:cpt + 3])
            if cpt + 3 < len(dec):
                dec2.append('\\,')
            cpt = cpt + 3
        dec2.extend(dec[cpt:])
    nb = ('').join(dec2)
    if nb.endswith('.0'):
        nb = string.rsplit(nb, '.0')[0]
    if mathenvironment:
        return string.join(string.rsplit(nb, sep='.'), ',')
    else:
        return string.join(string.rsplit(nb, sep='.'), '{,}')


def tex_coef(coef, var, bplus=0, bpn=0, bpc=0):

    # coef est le coefficient à écrire devant la variable var
    # bplus est un booleen : s'il est vrai, il faut ecrire le signe +
    # bpn est un booleen : s'il est vrai, il faut mettre des parentheses autour de l'ecriture si coef est negatif.
    # bpc est un booleen : s'il est vrai, il faut mettre des parentheses autour de l'ecriture si coef =! 0 ou 1 et var est non vide

    if coef != 0 and abs(coef) != 1:
        if var == '':
            if abs(coef) >= 1000:
                a = '\\nombre{%s}' % coef
            else:
                a = '%s' % coef
        else:
            if abs(coef) >= 1000:
                a = '\\nombre{%s}\\,%s' % (coef, var)
            else:
                a = '%s\\,%s' % (coef, var)
        if bplus and coef > 0:
            a = '+' + a
    elif coef == 1:
        if var == '':
            a = '1'
        else:
            a = '%s' % var
        if bplus:
            a = '+' + a
    elif coef == 0:
        a = ''
    elif coef == -1:
        if var == '':
            a = '-1'
        else:
            a = '-%s' % var
    if bpn and coef < 0 or bpc and coef != 0 and coef != 1 and var != '':
        a = '\\left( ' + a + '\\right)'
    return a


def choix_points(n):
    """
    choisit n points parmi A, B, C, ..., Z
    @param n: nombre de points \xc3\xa0 choisir
    @type n: integer
    """

    points = [unichr(i + 65) for i in xrange(26)]
    liste = []
    for i in xrange(n):
        liste.append(points.pop(randrange(len(points))))
    return liste


def melange_liste(list):
    """M\xc3\xa9lange de fa\xc3\xa7on al\xc3\xa9atoire les \xc3\xa9l\xc3\xa8ment de la liste list
    @param list: liste
    """

    tmp = []
    lg = len(list)
    for i in xrange(lg):
        tmp.append(list.pop(randrange(len(list))))
    return tmp


def fusion(liste1, liste2):
    (i1, i2) = (0, 0)
    liste = []
    while i1 < len(liste1) and i2 < len(liste2):
        if liste1[i1] < liste2[i2]:
            liste.append(liste1[i1])
            i1 = i1 + 1
        else:
            liste.append(liste2[i2])
            i2 = i2 + 1
    if i1 == len(liste1):
        liste.extend(liste2[i2:])
    else:
        liste.extend(liste1[i1:])
    return liste


def trie_liste_croissant(liste):
    if len(liste) == 1:
        return liste
    else:
        milieu = len(liste) / 2
        liste_a_trier = fusion(trie_liste_croissant(liste[:milieu]),
                               trie_liste_croissant(liste[milieu:]))
        return liste_a_trier


def detecter_modules(repertoire):
    modules = [nom[:-3] for nom in os.listdir(repertoire) if nom.enswith(".py")]
    liste = []
    for module in modules:
        m = __import__(module)
        if hasattr(m, "main"):
            liste.append(m.main)
    return liste


def radians(alpha):
    # convertit un angle en degré en radians
    return alpha*math.pi/180

def degres(alpha):
    return alpha*180/math.pi
#==============================================================
#        Vérifie la présence des programmes nécessaires à la compilation des fichiers TeX
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
    f0 = open( exo, 'w')
    f1 = open( cor, 'w')
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

    # Dossiers et fichiers d'enregistrement, définitions qui doivent rester avant le if suivant.
    dir0=os.path.dirname(exo)
    dir1=os.path.dirname(cor)
    f0noext=os.path.splitext(exo)[0]
    f1noext=os.path.splitext(cor)[0]

    if parametres['creer_pdf']:
        from subprocess import call

        for i in xrange(2):
            os.chdir(dir0)
            log = open('pyromaths.log', 'w')
            call(["latex", "-interaction=batchmode", str(exo)],
                    env={"PATH": os.path.expandvars('$PATH')},
                    stdout=log)
            if parametres['corrige']:
                os.chdir(dir1)
                call(["latex", "-interaction=batchmode", str(cor)],
                        env={"PATH": os.path.expandvars('$PATH')},
                        stdout=log)
        call(["dvips", "-q", "%s.dvi" % (f0noext)],
                env={"PATH": os.path.expandvars('$PATH')},
                stdout=log)
        if parametres['corrige']:
            call(["dvips", "-q", "%s.dvi" % (f1noext)],
                    env={"PATH": os.path.expandvars('$PATH')},
                    stdout=log)
        call(["ps2pdf", "-sPAPERSIZE#a4", "%s.ps" % (f0noext),
                    "%s.pdf" % (f0noext)],
                    env={"PATH": os.path.expandvars('$PATH')},
                    stdout=log)
        if parametres['corrige']:
            call(["ps2pdf", "-sPAPERSIZE#a4", "%s.ps" % (f1noext),
                "%s.pdf" % (f1noext)],
                env={"PATH": os.path.expandvars('$PATH')},
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
            os.remove(os.path.join(dir0, 'pyromaths.log'))
            for ext in ('.aux', '.dvi', '.log', '.out', '.ps'):
                os.remove(os.path.join(dir0,  f0noext + ext))
                if parametres['corrige']:
                    os.remove(os.path.join(dir1,  f1noext + ext))
        except OSError:
            print u"Le fichier %s ou %s n'a pas été supprimé." % (os.path.join(dir0,  f0noext + ext),
                                                                  os.path.join(dir1,  f1noext + ext))
                                                                  #le fichier à supprimer n'existe pas.
    if not parametres['corrige']:
        os.remove(os.path.join(dir1,  f1noext + '.tex'))

#==============================================================
#        Gestion du fichier de configuration de Pyromaths
#==============================================================
def create_config_file():
    """Crée le fichier de configuration au format xml"""
    root = etree.Element(u"pyromaths")

    child = etree.SubElement(root, u"options")
    etree.SubElement(child, u"nom_fichier").text=u"exercices"
    etree.SubElement(child, u"chemin_fichier").text=u"%s" % home()
    etree.SubElement(child, u"titre_fiche").text=u"Fiche de révision"
    etree.SubElement(child, u"corrige").text=u"True"
    etree.SubElement(child, u"pdf").text=u"True"
    etree.SubElement(child, u"modele").text=u"pyromaths.tex"

    child = etree.SubElement(root, u"informations")
    etree.SubElement(child, u"version").text=u"09.08"
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

    return os.path.dirname(unicode(__file__,
                                    sys.getfilesystemencoding( )))

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
    titre = parametres['titre'].encode('latin1')
    niveau = parametres['niveau']
    for line in open(source, 'r'):
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
    return

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

