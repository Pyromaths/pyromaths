#!/usr/bin/python
# -*- coding: utf8 -*-
"""
Build script for pyromaths.

This script is internally based on setuptools, with platform-specific extensions
for special tasks (py2app, py2exe, innosetup).
It builds different types of packages (source, binary, self-contained) on
several platforms. Packages should be functional, although further optimization
may be operated by other scripts (see: pkg/README).

Python source and bynary eggs (all platforms):
    $ python setup.py [sdist|bdist|bdist_egg] [options...]

RPM package (UNIX/Linux):
    $ ./setup.py bdist_rpm [options...]

Self-contained application (Mac OS X):
    $ python setup.py py2app [options...]

Self-contained application (Windows):
    $ python setup.py py2exe [options...]
    $ python setup.py innosetup [options...]

Help and options:
    $ python setup.py --help
    $ python setup.py --help-commands

Created on 13 avr. 2013
@author: Olivier Cornu <o.cornu@gmail.com>

"""
import os
import sys
from glob import glob

from setuptools import setup, find_packages

# Import pyromaths VERSION from source
sys.path.append('src')
from pyromaths.Values import VERSION

def _unix_opt():
    '''UNIX/Linux: generate Python eggs and RPM packages.'''
    return dict(
            platforms  = ['unix'],
            scripts    = ['pyromaths'],
            data_files = [
            ('share/applications',     ['data/linux/pyromaths.desktop']),
            ('share/man/man1',         ['data/linux/pyromaths.1']),
            ('share/pixmaps/',         ['data/images/pyromaths.png']),
            ('share/pyromaths/images', ['data/images/pyromaths-banniere.png',
                                        'data/images/whatsthis.png']),
            ('share/pyromaths/images/vignettes',
                                          glob('data/images/vignettes/*.png')),
            ('share/pyromaths/templates', glob('data/templates/*.tex')),
            ('share/pyromaths/packages',  glob('data/packages/*'))
            ],
            install_requires = ["lxml>=2.2.2"],
    )

def _mac_opt():
    '''MacOS: py2app helps generate a self-contained app.'''
    plist = dict(CFBundleIdentifier  = "org.pyromaths.pyromaths",
                 CFBundleName        = "Pyromaths",
                 CFBundleDisplayName = "Pyromaths",
                 CFBundleVersion     = VERSION,
                 CFBundleShortVersionString = VERSION,
                 NSHumanReadableCopyright = u"© Jérôme Ortais",
                 CFBundleDevelopmentRegion = "French",
                 CFBundleIconFile    = "pyromaths",
                 CFBundleExecutable  = "pyromaths",
                 CFBundlePackageType = "APPL",
                 CFBundleSignature   = "PYTS",
                 )
    # Unused Qt libraries/frameworks
    qt_unused = ['QtDBus', 'QtDeclarative', 'QtDesigner', 'QtHelp',
                 'QtMultimedia', 'QtNetwork', 'QtOpenGL', 'QtScript',
                 'QtScriptTools', 'QtSql', 'QtSvg', 'QtTest', 'QtWebKit',
                 'QtXml', 'QtXmlPatterns', 'phonon']
    # py2app
    py2app = dict(plist    = plist,
                  iconfile = 'data/images/pyromaths.icns',
                  includes = ['gzip'],
                  excludes = ['PyQt4.%s' % f for f in qt_unused],
                  dylib_excludes = qt_unused,
                  argv_emulation = True,
                  )
    return dict(
        app        = ['src/pyromaths.py'],
        data_files = [('data', glob('data/*'))],
        setup_requires = ['py2app>=0.7.3', 'lxml>=2.2.2'],
        options    = {'py2app': py2app},
    )

def _win_opt():
    '''M$ Win: py2exe helps generate a self-contained app.'''
    inno_script = '''
[Setup]
Compression=lzma/max
OutputBaseFilename=pyromaths-%s-win32
[Languages]
Name:         "french";
MessagesFile: "compiler:Languages\French.isl"
[Tasks]
Name:         "desktopicon";
Description:  "{cm:CreateDesktopIcon}";
GroupDescription: "{cm:AdditionalIcons}";
Flags:        unchecked
[Icons]
Name:         "{commondesktop}\Pyromaths";
Filename:     "{app}\pyromaths.exe"
''' % VERSION
    return dict(
        platforms  = ['windows'],
        app        = ["src/pyromaths.py"],
        data_files = [('data', glob('data/*'))],
        zipfile = None,
        windows = [dict(script="Pyromaths.py",
                        icon_resources=[(1, 'data/images/pyromaths.ico')],
                        )
                   ],
        setup_requires = ['py2exe'],
        options = dict(py2exe=dict(compressed   = 1,
                                   optimize     = 2,
                                   bundle_files = 3,
                                   includes     = ["sip", "gzip"],
                                   ),
                       innosetup=dict(inno_script=inno_script, compressed=True)
                       )
    )

# Set platform-specific options
if "py2app" in sys.argv:
    options = _mac_opt()
elif sys.platform == 'win32':
    options = _win_opt()
else:
    options = _unix_opt()

# Long description is copied from README file
with open('README') as file:
    README = file.read()

setup(
    # project metadata
    name        = "pyromaths",
    version     = VERSION,
    description = "Create maths exercises in LaTeX and PDF format",
    long_description = README,
    license     = "GPL",
    url         = "http://www.pyromaths.org",
    download_url = "http://pyromaths.org/telecharger/",
    author      = u"Jérôme Ortais",
    author_email = "jerome.ortais@pyromaths.org",
    # python packages
    packages    = find_packages('src'),
    package_dir = {'': 'src'},
    # dependencies
    provides    = ["pyromaths"],
    # platform-specific options
    **options
)

# Post-processing
if "py2app" in sys.argv:
    # py2app/setenv hack: replace executable with one appending several LaTeX
    # distributions locations to the path.
    mactex   = "/usr/texbin:/usr/local/bin"
    macports = "/opt/local/bin:/opt/local/sbin"
    fink     = "/sw/bin"
    path     = "%s:%s:%s" % (mactex, macports, fink)
    f = open('dist/Pyromaths.app/Contents/MacOS/setenv.sh', 'w')
    f.write('''#!/bin/sh
PWD=$(dirname "$0"); /usr/bin/env PATH="$PATH:%s" $PWD/pyromaths''' % path)
    os.system("chmod +x dist/Pyromaths.app/Contents/MacOS/setenv.sh")
    os.system("sed -i '' '23s/pyromaths/setenv.sh/' dist/Pyromaths.app/Contents/Info.plist")
