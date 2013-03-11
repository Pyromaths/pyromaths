#!/usr/bin/python
# -*- coding: utf-8 -*-
import os, sys, codecs, shutil
from os.path import dirname, normpath, join, abspath, realpath, split

_path = normpath(join(abspath(dirname(__file__)), ".."))
sys.path[0] = realpath(_path)
from src import pyromaths

#datadir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
#sys.path.append(datadir)
from src.Values import LESFICHES, data_dir, configdir
from src.outils.System import creation

from subprocess import call, Popen
d =os.path.join(dirname(os.path.abspath(__file__)), "..", "data", "images", "vignettes")

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

log = open('/tmp/preview-pyromaths.log' , 'w')
parametres = {
    'creer_pdf': True,
    'creer_unpdf': False,
    'titre': u"Fiche de révisions",
    'corrige': False,
    'niveau': "test",
    'nom_fichier': u'test.tex',
    'chemin_fichier': "/tmp/",
    'fiche_exo': '/tmp/test.tex',
    'fiche_cor': '/tmp/test-corrige.tex',
    'configdir': configdir(),
    'datadir': data_dir(),
    'modele': 'pyromaths.tex',
    'liste_exos': [],
    'les_fiches': LESFICHES,
    'openpdf': 0,
}

#for n in range(1):
    #for i in range(1):
for n in range(len(LESFICHES)):
    for i in range(len(LESFICHES[n][2])):
        lst = [[n, i]]
        parametres['liste_exos'] = lst
        creation(parametres)
        call(["convert", "-density", "288", "/tmp/test.pdf", "-resize", "25%",
            "-crop", "710x560+0+85", "-flatten", "-trim", "/tmp/%se-%02d.png" % (6-n, i)],
            stdout=log)
        call(["pngnq", "-f", "-s1", "-n32", "/tmp/%se-%02d.png" % (6-n, i)],
                stdout=log)
        shutil.copyfile( "/tmp/%se-%02d-nq8.png" % (6-n, i), "%s/%se-%02d.png" % (d, 6-n, i))
        Popen(args=["optipng", "-o7", "%s/%se-%02d.png" % (d, 6-n, i)])
log.close()

