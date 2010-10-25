#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys, os
from subprocess import call, Popen

datadir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "..")
sys.path.append(datadir)
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
        'datadir': datadir,
        'modele': 'pyromaths.tex',
        'liste_exos': [],
        'les_fiches': LesFiches,
        }

for j in range(100):
    print('Test n° %03d' % (j+1))
    lst = []
    for n in range(len(LesFiches)):
        for i in range(len(LesFiches[n][2])):
            lst.append([n,i])
    parametres['liste_exos'] = lst
    creation(parametres)
