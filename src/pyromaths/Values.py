#!/usr/bin/python
# -*- coding: utf-8 -*-
#
from time import strftime
from os.path import normpath, dirname, exists, abspath, join
from os import environ, name
from sys import executable, getfilesystemencoding
import sys
import pkgutil, types
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
    data = join(abspath(dirname(__file__)),'../../data/')
    if exists(data): return normpath(data)
    # Are we running from an egg?
    data = join(abspath(dirname(__file__)),'../share/pyromaths/')
    if exists(data): return normpath(data)
    # Assume we're installed system-wide
    return '/usr/share/pyromaths/'

def icon_dir():
    """Renvoie le dossier où se trouve l'icône, selon qu'on utilise pyromaths à
    partir des sources, de l'exécutable win32 ou du paquet deb"""
    if we_are_frozen() or exists(join(abspath(dirname(__file__)),'../../data/')):
        return join(DATADIR, 'images', 'pyromaths.png')
    return join('/usr/share/pixmaps', 'pyromaths.png')
        
if name == 'nt':
    def home():
        return unicode(environ['USERPROFILE'], getfilesystemencoding())
    def configdir():
        return join(unicode(environ['APPDATA'], getfilesystemencoding()),
                "pyromaths")
elif sys.platform == "darwin":  #Cas de Mac OS X.
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

VERSION = '13.03'
COPYRIGHT_YEAR = strftime('%Y')
COPYRIGHTS = u'© 2006 – %s Jérôme Ortais<br/>\n' \
        u'<span style=" font-size:small;">Pyromaths est distribué sous ' \
        u'licence GPL.</span>' % (COPYRIGHT_YEAR)
WEBSITE = 'http://www.pyromaths.org/'
DATADIR = data_dir()
ICONDIR = icon_dir()
HOME = home()
CONFIGDIR = configdir()

def _exercices(pkg):
    ''' Discover package exercises. '''
    exercices = []
    # search package modules
    for _, name, ispkg in pkgutil.iter_modules(pkg.__path__, pkg.__name__+'.'):
        # skip sub-packages (discovery is not recursive)
        if ispkg: continue
        # import discovered module
        module = __import__(name, fromlist=pkg.__name__)
        # search module for exercises: functions with a 'description' attribute
        # of UnicodeType
        for element in dir(module):
            # list module elements
            element = module.__dict__[element]
            if not type(element) is types.FunctionType: continue
            if 'description' not in dir(element): continue
            description = element.__dict__['description']
            if not type(description) is types.UnicodeType: continue
            # store discovered exercise
            exercices.append(element)
    return exercices

def _packages(pkg):
    ''' Discover all packages located in pkg. '''
    packages = []
    # search packages
    for _, name, ispkg in pkgutil.iter_modules(pkg.__path__, pkg.__name__+'.'):
        # skip modules
        if not ispkg: continue
        # import discovered package
        package = __import__(name, fromlist=pkg.__name__)
        # exercise packages must have a description property
        if 'description' not in dir(package): continue
        description = package.__dict__['description']
        # description property must be Unicode
        if not type(description) is types.UnicodeType: continue
        # valid exercise package
        packages.append(package)
    return packages

# Packages d'exercices
PACKAGES = _packages(ex)

LESFICHES = []
for pkg in PACKAGES:
    pkg.EXERCICES = _exercices(pkg)
    titles = [ex.description for ex in pkg.EXERCICES]
    LESFICHES.append([pkg.description, '', titles])
