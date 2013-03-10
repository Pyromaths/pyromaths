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
import codecs, tempfile


def nettoyage(dt):
    for file in ["exercices.tex", "exercices.pdf"]:
        os.remove(os.path.join(dt, file))
    os.rmdir(dt)

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
dt = tempfile.mkdtemp(prefix = 'pyromaths_tests-', dir = '/tmp')
parametres = {
        'creer_pdf': True,
        'creer_unpdf': True,
        'titre': u"Fiche de révisions",
        'corrige': True,
        'niveau': "test",
        'nom_fichier': u'test.tex',
        'chemin_fichier': dt,
        'fiche_exo': os.path.join(dt, 'exercices.tex'),
        'fiche_cor': os.path.join(dt, 'exercices-corrige.tex'),
        'datadir': data_dir(),
        'configdir': configdir(),
        'modele': 'pyromaths.tex',
        'liste_exos': [],
        'les_fiches': LESFICHES,
        'openpdf': 0,
        }

if (len(sys.argv) == 4):
    lst = []
    for i in range(int(sys.argv[3])):
      lst.append([int(sys.argv[1]),int(sys.argv[2])])
    parametres['liste_exos'] = lst
    creation(parametres)
    nettoyage(dt)

elif (len(sys.argv) == 1):
    os.rmdir(dt)
    for j in range(1000):
        print('Test n° %03d' % (j+1))
        dt = tempfile.mkdtemp(prefix = 'pyromaths_tests-', dir = '/tmp')
        parametres['chemin_fichier'] = dt
        parametres['fiche_exo'] = os.path.join(dt, 'exercices.tex')
        parametres['fiche_cor'] = os.path.join(dt, 'exercices-corrige.tex')
        lst = []
        for n in range(len(LESFICHES)):
            for i in range(len(LESFICHES[n][2])):
                lst.append([n,i])
        parametres['liste_exos'] = lst
        creation(parametres)
        nettoyage(dt)
else:
    print(usage)

