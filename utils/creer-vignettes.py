#!/usr/bin/python
# -*- coding: utf-8 -*-
import os, sys, codecs, shutil
from os.path import dirname, normpath, join, abspath, realpath, split

_path = normpath(join(abspath(dirname(__file__)), "../src"))
sys.path[0] = realpath(_path)
from pyromaths import pyromaths, ex

#datadir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
#sys.path.append(datadir)
from pyromaths.Values import data_dir, configdir, LESFICHES
from pyromaths.outils.System import creation

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

def __thumb(exercise, imgdir, i):
    parametres['liste_exos'] = [exercise()]
    creation(parametres)
    call(["convert", "-density", "288", "/tmp/test.pdf", "-resize", "25%",
        "-crop", "710x560+0+85", "-flatten", "-trim", "/tmp/ex-%02d.png" % i],
        stdout=log)
    call(["pngnq", "-f", "-s1", "-n32", "/tmp/ex-%02d.png" % i],
            stdout=log)
    shutil.copyfile( "/tmp/ex-%02d-nq8.png" % i, "%s/ex-%02d.png" % (imgdir, i))
    Popen(args=["optipng", "-o7", "%s/ex-%02d.png" % (imgdir, i)])

def __thumbs(pkg):
    imgdir = join(pkg.__path__[0], "img")
    i = 0
    for e in ex._exercises(pkg):
        __thumb(e, imgdir, i)
        i += 1

def thumbs(pkg=ex, recursive=True):
    __thumbs(pkg)
    if not recursive: return
    for pk in ex._subpackages(pkg):
        thumbs(pk)

thumbs()
log.close()

