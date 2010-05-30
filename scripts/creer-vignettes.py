#!/usr/bin/python
# -*- coding: utf-8 -*-
import os, sys, codecs, shutil
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from pyromaths import LesFiches
from outils.System import creation
from subprocess import call, Popen
d =os.path.join(sys.path[0], "..", "img", "vignettes")

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
    'modele': 'pyromaths.tex',
    'liste_exos': [],
    'les_fiches': LesFiches,
}

#for n in range(1):
    #for i in range(1):
for n in range(len(LesFiches)):
    for i in range(len(LesFiches[n][2])):
        lst = [[n, i]]
        parametres['liste_exos'] = lst
        creation(parametres)
        call(["convert", "-density", "288", "/tmp/test.pdf", "-resize", "25%",
            "-crop", "710x560+0+89", "-trim", "/tmp/%se-%02d.png" % (6-n, i)],
            stdout=log)
        call(["pngnq", "-f", "-s1", "-n32", "/tmp/%se-%02d.png" % (6-n, i)],
                stdout=log)
        shutil.copyfile( "/tmp/%se-%02d-nq8.png" % (6-n, i), "%s/%se-%02d.png" % (d, 6-n, i))
        Popen(args=["optipng", "-o7", "%s/%se-%02d.png" % (d, 6-n, i)])
log.close()

