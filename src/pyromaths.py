#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Pyromaths
# Un programme en Python qui permet de créer des fiches d'exercices types de
# mathématiques niveau collège ainsi que leur corrigé en LaTeX.
# Copyright (C) 2006 -- Jérôme Ortais (jerome.ortais@pyromaths.org)
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301 USA

from sys import argv, exit, getfilesystemencoding
import sys, os
from os import access, R_OK, makedirs, chdir, environ, name
from os.path import join, isdir, dirname, realpath, split, exists, abspath, normpath
from codecs import open
##

def we_are_frozen():
    """Returns whether we are frozen via py2exe.
    This will affect how we find out where we are located."""
    return hasattr(sys, "frozen")

def data_dir():
    """Renvoie le dossier data, selon qu'on utilise pyromaths à partir des
    sources, de l'exécutable win32 ou du paquet deb"""
    if we_are_frozen():
        return join(normpath(dirname(unicode(executable,
            getfilesystemencoding()))), 'data')
    elif exists(join(abspath(dirname(__file__)),'../data/')):
        return normpath(join(abspath(dirname(__file__)),'../data/'))
    else:
        return '/usr/share/pyromaths/'

def icon_dir():
    """Renvoie le dossier où se trouve l'icône, selon qu'on utilise pyromaths à
    partir des sources, de l'exécutable win32 ou du paquet deb"""
    if we_are_frozen() or exists(join(abspath(dirname(__file__)),'../data/')):
        return join(DATADIR, 'images', 'pyromaths.png')
    else:
        return join('/usr/share/pixmaps', 'pyromaths.png')

def home():
    if name == 'nt':
        return unicode(environ['USERPROFILE'], getfilesystemencoding())
    elif sys.platform == "darwin":  #Cas de Mac OS X.
        return unicode(environ['HOME'], getfilesystemencoding())
    else:
	try:
            return unicode(environ['HOME'], getfilesystemencoding())
        except KeyError:
            # Pyromaths en ligne, l'user apache n'a pas de $HOME
            return ""
    
def configdir():
    if name == 'nt':
        return join(unicode(environ['APPDATA'], getfilesystemencoding()),
                "pyromaths")
    elif sys.platform == "darwin":  #Cas de Mac OS X.
        return join(home(), "Library", "Application Support", "Pyromaths")
    else:
	return join(home(), ".config", "pyromaths")

def langue(LANG_NOM):
    if sys.platform.startswith('win'):
        import locale
        if os.getenv('LANG') is None:
            lang, enc = locale.getdefaultlocale()
            os.environ['LANG'] = lang
    else:
        lang = os.getenv('LANG')
    LANG_temp = [LANG_NOM[i][0] for i in range(len(LANG_NOM))]
    LANG_txt = lang[0:2]
    try:
        LANG = LANG_temp.index(LANG_txt)
    except ValueError:
        LANG = "0"
    return LANG 

DATADIR = data_dir()
ICONDIR = icon_dir()
HOME = home()
CONFIGDIR = configdir()
LANG_NOM = [["fr", u"Frances"], ["es", u"Español"]]
DIR_LANG = join(DATADIR, "locale")

def main():
#===============================================================================
# Imports spécifiques à Pyromaths
#===============================================================================
    from outils.System import create_config_file, modify_config_file
    from outils.TestEnv import test

    
    
    #===========================================================================
    # Création du fichier de configuration si inexistant
    #===========================================================================
    if not access(join(CONFIGDIR, "pyromaths.xml"), R_OK):
        if not isdir(CONFIGDIR): makedirs(CONFIGDIR)
        f = open(join(CONFIGDIR, "pyromaths.xml"), encoding='utf-8', mode='w')
        LANG = langue(LANG_NOM)
        f.write(u"" + create_config_file(HOME, DIR_LANG, LANG_NOM, LANG))
        f.close()
    modify_config_file(join(CONFIGDIR, "pyromaths.xml"), HOME, CONFIGDIR, DIR_LANG, LANG_NOM)
    templatesdir = join(CONFIGDIR,  "templates")
    if not isdir(templatesdir): makedirs(templatesdir)
    packagesdir = join(CONFIGDIR,  "packages")
    if not isdir(packagesdir): makedirs(packagesdir)

    import interface
    from PyQt4 import QtGui, QtCore
    class StartQT4(QtGui.QMainWindow, interface.Ui_MainWindow):
        def __init__(self, parent=None):
            QtGui.QWidget.__init__(self, parent)
            self.ui = interface.Ui_MainWindow()
            self.ui.setupUi(self, CONFIGDIR, DATADIR, ICONDIR, LANG_NOM)

    app = QtGui.QApplication(argv)
    pyromaths = StartQT4()

    pyromaths.show()
    test(pyromaths, CONFIGDIR)

    exit(app.exec_())

if __name__ == "__main__":
    basedir = dirname(realpath(__file__))
    _path, _dir = split(basedir)
    sys.path[0] = realpath(_path)
    exec("from %s import pyromaths" % _dir)
    pyromaths.main()
