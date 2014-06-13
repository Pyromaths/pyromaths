#!/usr/bin/python
# -*- coding: utf-8 -*-
import os, sys, codecs, shutil, glob
from os.path import dirname, normpath, join, abspath, realpath, split
from subprocess import call, Popen

_path = normpath(join(abspath(dirname(__file__)), "../src"))
sys.path[0] = realpath(_path)
from pyromaths import pyromaths, ex
from pyromaths.Values import data_dir, configdir
from pyromaths.outils.System import creation

_param = {
    'creer_pdf': True,
    'creer_unpdf': False,
    'titre': u"Thumbnail",
    'corrige': False,
    'niveau': "",
    'nom_fichier': u'thumb.tex',
    'chemin_fichier': "/tmp/",
    'fiche_exo': '/tmp/thumb.tex',
    'fiche_cor': '/tmp/thumb-corrige.tex',
    'configdir': configdir(),
    'datadir': data_dir(),
    'modele': 'pyromaths.tex',
    'liste_exos': [],
    'openpdf': 0,
}

def _thumb(exercise, outfile=None):
    ''' Create a thumbnail for this 'exercise'. '''
    if outfile is None: outfile = exercise.thumb
    # create pdf
    _param['liste_exos'] = [exercise()]
    creation(_param)
    # extract optimized thumbnail
    call(["convert", "-density", "288", "/tmp/thumb.pdf",
          "-resize", "25%", "-crop", "710x560+0+85",
          "-flatten", "-trim", "/tmp/thumb.png"],
         stdout=log)
    call(["pngnq", "-f", "-s1", "-n32", "/tmp/thumb.png"], stdout=log)
    shutil.copyfile( "/tmp/thumb-nq8.png", exercise.thumb)
    Popen(args=["optipng", "-o7", exercise.thumb])

def thumbs(pkg=ex, recursive=True):
    ''' Create all exercise thumbnails. '''
    dirlevel = os.path.split(pkg.__path__[0])[1]
    imgdir = join(_param['datadir'], 'ex', dirlevel, 'img')
    print imgdir
    #raise ValueError('voila')
    for fl in glob.glob(join(imgdir, "ex-??.png")):
       #Do what you want with the file
       os.remove(fl)
    for e in ex._exercises(pkg):
        _thumb(e)
    if not recursive: return
    for pk in ex._subpackages(pkg):
        thumbs(pk)

log = open('/tmp/preview-pyromaths.log' , 'w')
thumbs()
log.close()
