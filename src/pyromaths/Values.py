#!/usr/bin/python
# -*- coding: utf-8 -*-
#
from time import strftime
from os.path import normpath, dirname, exists, abspath, join
from os import environ, name
from sys import executable, getfilesystemencoding
import sys
# import pkgutil, types
import ex

def we_are_frozen():
    """Returns whether we are frozen via py2exe.
    This will affect how we find out where we are located."""
    return hasattr(sys, "frozen")

def data_dir():
    """Renvoie le dossier data, selon qu'on utilise pyromaths à partir des
    sources, de l'exécutable win32 ou du paquet deb"""
    if we_are_frozen():
        if   sys.platform == 'win32':
            path = 'data'
        elif sys.platform == 'darwin':
            path = '../Resources/data'
        return join(normpath(dirname(unicode(executable,
                                             getfilesystemencoding()))), path)
    # We're alive
    # Are we running from the sources?
    data = join(abspath(dirname(__file__)), '../../data/')
    if exists(data): return normpath(data)
    # Are we running from an egg?
    data = join(abspath(dirname(__file__)), '../share/pyromaths/')
    if exists(data): return normpath(data)
    # Assume we're installed system-wide
    return '/usr/share/pyromaths/'

def icon_dir():
    """Renvoie le dossier où se trouve l'icône, selon qu'on utilise pyromaths à
    partir des sources, de l'exécutable win32 ou du paquet deb"""
    if we_are_frozen() or exists(join(abspath(dirname(__file__)), '../../data/')):
        return join(DATADIR, 'images', 'pyromaths.png')
    return join('/usr/share/pixmaps', 'pyromaths.png')
        
if name == 'nt':
    def home():
        return unicode(environ['USERPROFILE'], getfilesystemencoding())
    def configdir():
        return join(unicode(environ['APPDATA'], getfilesystemencoding()),
                "pyromaths")
elif sys.platform == "darwin":  # Cas de Mac OS X.
    def home():
        return unicode(environ['HOME'], getfilesystemencoding())
    def configdir():
        return join(home(), "Library", "Application Support", "Pyromaths")
else:
    def home():
        try:
            return unicode(environ['HOME'], getfilesystemencoding())
        except KeyError:
            # Pyromaths en ligne, l'user apache n'a pas de $HOME
            return ""
    def configdir():
        return join(home(), ".config", "pyromaths")

VERSION = '14.05'
COPYRIGHT_YEAR = strftime('%Y')
COPYRIGHTS = u'© 2006 – %s Jérôme Ortais<br/>\n' \
        u'<span style=" font-size:small;">Pyromaths est distribué sous ' \
        u'licence GPL.</span>' % (COPYRIGHT_YEAR)
WEBSITE = 'http://www.pyromaths.org/'
DATADIR = data_dir()
ICONDIR = icon_dir()
HOME = home()
CONFIGDIR = configdir()

LESFICHES = []
ex.load()
for level, exercices in ex.levels.iteritems():
    LESFICHES.append([level, '', exercices])
