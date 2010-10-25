#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys, os, shutil
from subprocess import call, Popen

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from pyromaths import LesFiches
from outils.System import creation
import codecs

if os.name == 'nt':
    def home():
        return unicode(os.environ['USERPROFILE'],sys.getfilesystemencoding())
    def configdir():
        return os.path.join(os.environ['APPDATA'],"pyromaths")
else:
    def home():
        return unicode(os.environ['HOME'],sys.getfilesystemencoding())
    def configdir():
        return os.path.join(home(), ".config", "pyromaths")

parametres = {
        'creer_pdf': True,
        'creer_unpdf': True,
        'titre': u"Fiche de révisions",
        'corrige': True,
        'niveau': "test",
        'nom_fichier': u'test.tex',
        'chemin_fichier': "/tmp/",
        'fiche_exo': '/tmp/test.tex',
        'fiche_cor': '/tmp/test-corrige.tex',
        'configdir': configdir(),
        'modele': 'pyromaths.tex',
        'liste_exos': [],
        'les_fiches': LesFiches,
        }

if not os.path.isdir("/tmp/modeles"):
    shutil.copytree("modeles","/tmp/modeles" ) 

if (len(sys.argv) == 4):

    lst = []

    for i in range(int(sys.argv[3])):
      lst.append([int(sys.argv[1]),int(sys.argv[2])])
      
    parametres['liste_exos'] = lst
    creation(parametres)

elif (len(sys.argv) == 1):
    for j in range(100):
	print('Test n° %03d' % (j+1))
	lst = []
	for n in range(len(LesFiches)):
	    for i in range(len(LesFiches[n][2])):
		lst.append([n,i])
	parametres['liste_exos'] = lst
	creation(parametres)
else:
    print "\n###################################"
    print "###            USAGE            ###"
    print "###################################\n"
    print u"Sans argument, ce script génère un exemplaire de chaque exercice et leurs corrigés en tex et pdf.\n"
    print u"Sinon, \"python test_creation_fichiers_tex.py i j k\" génère k exercices n° j du niveau i."
    print u"Par exemple, \"python test_creation_fichiers_tex.py 1 5 10\" génère 10 exercices de \"Repérage\" du niveau cinquième.\n"