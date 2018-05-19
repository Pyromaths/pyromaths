#!/usr/bin/python
# -*- coding: utf-8 -*-
import os, sys, codecs, shutil, glob
from os.path import dirname, normpath, join, abspath, realpath, split
from subprocess import call, Popen

_path = normpath(join(abspath(dirname(__file__)), "../src"))
sys.path[0] = realpath(_path)
import hashlib
import gettext

def main():
#===============================================================================
# Imports spécifiques à Pyromaths
#===============================================================================

    locale_dir = join(dirname(__file__), '../locale/')
    locale_dir = realpath(locale_dir)

    gettext.install('pyromaths', localedir=locale_dir, unicode=1)
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


    def md5check(exercise, imgdir, newfile=None):
        ''' Check if the file has been changed or renamed. '''
        if newfile is None:
            newfile = os.path.join(imgdir,'tmp', os.path.basename(exercise.thumb()))
        # open md5sums file
        md = open(os.path.join(imgdir, 'md5sums'), 'r')
        thesum = hashlib.md5(open(newfile, 'rb').read()).hexdigest()
        print thesum
        originalfile=''
        newname=True
        for l in md:
            if thesum in l:
                originalfile=os.path.join(imgdir, l.lstrip(thesum).lstrip())
            if os.path.basename(newfile) in l:
                newname=False
        md.close()
        shutil.copyfile(newfile, exercise.thumb())
        os.chdir(imgdir)
        #raise ValueError('asked to stop')
        if originalfile:
            if originalfile!=exercise.thumb():
                log.write('%s renamed to %s' % (originalfile, exercise.thumb()))
                call(['git', 'mv', originalfile, exercise.thumb()], stdout=log)
        else:
            if newname:
                log.write('Created file %s' % (exercise.thumb()))
                call(['git', 'add', exercise.thumb()], stdout=log)
            else:
                log.write('%s replaced by %s' % (originalfile, exercise.thumb()))
        os.remove(os.path.join(newfile))

    def _thumb(exercise, outfile=None):
        ''' Create a thumbnail for this 'exercise'. '''
        if outfile is None:
            print("EXERCICE.THUMB : ",exercise.thumb())
            outfile = os.path.join(os.path.dirname(exercise.thumb()), 'tmp', os.path.basename(exercise.thumb()))
        print outfile
        # create pdf
        _param['liste_exos'] = [exercise()]
        creation(_param)
        # extract optimized thumbnail
        call(["convert", "-density", "288", "/tmp/thumb.pdf",
            "-resize", "25%", "-crop", "710x560+0+85",
            "-flatten", "-trim", "/tmp/thumb.png"],
            stdout=log)
        call(["pngnq", "-f", "-s1", "-n32", "/tmp/thumb.png"], stdout=log)
        log.write(outfile)
        shutil.copyfile( "/tmp/thumb-nq8.png", outfile)
        call(args=["optipng", "-o7", outfile])
        md5check(exercise, os.path.dirname(exercise.thumb()))

    def thumbs(pkg=ex, recursive=True):
        ''' Create all exercise thumbnails. '''
        import random
        random.seed(0)
        imgdir = join(_param['datadir'], 'ex', 'img')
        print "IMGDIR : ", imgdir
        try:
            os.mkdir(os.path.join(imgdir, 'tmp'))
        except OSError:
            pass
        #raise ValueError('voila')
        for fl in glob.glob(join(imgdir, "ex-??.png")):
            #Do what you want with the file
            os.remove(fl)
        for e in ex._exercises(pkg):
            _thumb(e)
        if not recursive: return
        try:
            os.chdir(imgdir)
            mdfile=open('md5sums','w')
            for fl in glob.glob(join(imgdir, "ex-??.png")):
                #Do what you want with the file
                thesum = hashlib.md5(open(fl, 'rb').read()).hexdigest()
                mdfile.write(thesum + '  ' + os.path.basename(fl) + '\n')
            mdfile.close()
            os.rmdir(os.path.join(imgdir, 'tmp'))
        except OSError:
            pass
        for pk in ex._subpackages(pkg):
            thumbs(pk)

    log = open('/tmp/preview-pyromaths.log' , 'w')
    thumbs()
    log.close()


if __name__ == "__main__":
    main()
