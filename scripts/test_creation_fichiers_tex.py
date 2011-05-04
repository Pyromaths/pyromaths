#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys, os, shutil
from subprocess import call, Popen
from os.path import dirname, normpath, join, abspath, realpath, split

_path = normpath(join(abspath(dirname(__file__)), ".."))
sys.path[0] = realpath(_path)
from src import pyromaths

from src.Values import LESFICHES, data_dir, configdir
from src.outils.System import creation
import codecs

usage = u"""
###################################
###            USAGE            ###
###################################

Sans argument, ce script génère cent fiches contenant chacune un exemplaire de
chaque exercice et leurs corrigés en tex et pdf.

Sinon, "python test_creation_fichiers_tex.py i j k" génère k exercices n° j du
niveau i.

Par exemple, "python test_creation_fichiers_tex.py 1 5 10" génère 10 exercices
de "Repérage" du niveau cinquième.
"""

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
        'datadir': data_dir(),
        'configdir': configdir(),
        'modele': 'pyromaths.tex',
        'liste_exos': [],
        'les_fiches': LESFICHES,
        }

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
        for n in range(len(LESFICHES)):
            for i in range(len(LESFICHES[n][2])):
                lst.append([n,i])
        parametres['liste_exos'] = lst
        creation(parametres)
else:
    print(usage)
