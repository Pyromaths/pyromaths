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
import codecs
from glob import glob, has_magic
from os.path import dirname, normpath, join, abspath, realpath

from setuptools import setup, find_packages

import gettext
locale_dir = join(dirname(__file__), 'locale/')
locale_dir = realpath(locale_dir)

gettext.install('pyromaths', localedir=locale_dir, unicode=1)

py2exe, innosetup = None, None
try:
    import py2exe
    import innosetup
except ImportError:
    pass

# Import pyromaths VERSION from source
_path = normpath(join(abspath(dirname(__file__)), "./src"))
sys.path[0] = realpath(_path)
#sys.path.append('src')
from pyromaths.Values import VERSION
print "Version ", VERSION

COMMON_INSTALL_REQUIRES = ['jinja2']

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
            ('share/pyromaths/templates', glob('data/templates/*.tex')),
            # ('share/pyromaths/packages',  glob('data/packages/*'))
            ] + \
            find_data_files('data/ex','share/pyromaths/ex/',['img/*.png', 'templates/*.tex']),
            install_requires = COMMON_INSTALL_REQUIRES + ["lxml>=2.2.2"],
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
    lib_dynload_unused = ['_AE', '_codecs_cn', '_codecs_hk', '_codecs_2022',
                          '_codecs_iso2022', '_codecs_jp', '_codecs_kr',
                          '_codecs_tw', '_Evt', '_File', '_heapq',
                          '_locale', '_multibytecodec', '_Res','_ssl', 'array',
                          'bz2', 'cPickle', 'datetime', 'gestalt', 'MacOS',
                          'pyexpat', 'rurce', 'strop', 'unicodedata']
    site_packages_unused = ['_osx_support', '_builtinSuites', 'Carbon',
                            'distutils', 'Finder', 'StdSuites','xml','getopt', 
                            'repr', '_strptime', 'sets', '_threading_local',
                            'base64', 'sre', 'bdb', 'optparse.', 'ssl',
                            'calendar', 'pdb', 'stringprep', 'cmd',
                            'pkg_resources', 'platform', 'threading',
                            'dummy_thread', 'plistlib', 'quopri', 'doctest',
                            'ntpath', 'OpenSSL','os2emxpath', 'PyQt4.uic']
    excludes = lib_dynload_unused + site_packages_unused + ['PyQt4.%s' % f for f in qt_unused]
    # py2app
    py2app = dict(plist    = plist,
                  iconfile = 'data/images/pyromaths.icns',
                  includes = ['gzip', 'threading', 'cPickle', 'base64'],
                  packages = ['pyromaths.ex'],
                  excludes = excludes,
                  argv_emulation = True,
                  )
    return dict(
        app        = ['src/pyromaths.py'],
        data_files = [
            ( 'data', ['data/qtmac_fr.qm']),
            ( 'data/images', ['data/images/pyromaths.png',
                     'data/images/whatsthis.png']),
            ('data/templates',        glob('data/templates/*.tex')),
            # ('data/packages',         glob('data/packages/*')),
        ] + find_data_files('data/ex','data/ex/',['img/*.png', 'templates/*.tex']),
        setup_requires = ['py2app>=0.7.3', 'lxml>=2.2.2'],
        install_requires = COMMON_INSTALL_REQUIRES,
        options    = {'py2app': py2app},
    )

def _win_opt():
    '''M$ Win: py2exe helps generate a self-contained app.'''
#   import py2exe, innosetup
    inno_script = '''
[Setup]
Compression = lzma/max
OutputBaseFilename = pyromaths-%s-win32
[Languages]
Name: "french"; MessagesFile: "compiler:Languages\French.isl"
[Tasks]
Name: "desktopicon"; Description:  "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
[Icons]
Name: "{commondesktop}\Pyromaths"; Filename: "{app}\pyromaths.exe"
''' % VERSION
    return dict(
        platforms  = ['windows'],
        data_files=[
          ('data/images', ['data/images/pyromaths.ico',
            'data/images/pyromaths.png', 'data/images/pyromaths-banniere.png',
            'data/images/whatsthis.png']
           ),
          (r'data/templates', glob(r'data/templates/*.tex')),
          # (r'data/packages', glob(r'data/packages/*')),
        ] + find_data_files('data/ex','data/ex/',['img/*.png', 'templates/*.tex']),
        zipfile = None,
        windows = [dict(script="pyromaths",
                        icon_resources=[(1, 'data/images/pyromaths.ico')],
                        )
                   ],
        setup_requires = ['py2exe'],
        install_requires = COMMON_INSTALL_REQUIRES,
        options = dict(py2exe=dict(compressed   = True,
                                   optimize     = 2,
                                   bundle_files = 3,
                                   packages = ['pyromaths.ex', ],
                                   includes     = ['sip', 'gzip', ],
                                   dll_excludes = ['msvcr90.dll', 'msvcp90.dll'],
                                   ),
                       innosetup=dict(inno_script=inno_script,
                                      bundle_vcr = False,
                                      )
                       )
    )

def find_data_files(source,target,patterns):
  if has_magic(source) or has_magic(target):
    raise ValueError("Magic not allowed in src, target")
  ret = {}
  for pattern in patterns:
    pattern = os.path.join(source,pattern)
    for filename in glob(pattern):
      if os.path.isfile(filename):
        targetpath = os.path.join(target, os.path.relpath(filename, source))
        path = os.path.dirname(targetpath)
        ret.setdefault(path,[]).append(filename)
  return sorted(ret.items())

# Set platform-specific options
if "py2app" in sys.argv:
    options = _mac_opt()
elif sys.platform == 'win32':
    options = _win_opt()
else:
    options = _unix_opt()

# Long description is copied from README file
if innosetup:
    # innosetup fails with generated multiline long description
    README = "Create maths exercises in LaTeX and PDF format"
else:
    with codecs.open('README', encoding='utf-8', mode='r') as file:
        README = file.read()

setup(
    # project metadata
    name        = "pyromaths",
    version     = VERSION,
    description = "Create maths exercises in LaTeX and PDF format",
    long_description = README,
    license     = "GPL",
    url         = "http://www.pyromaths.org",
    download_url = "http://www.pyromaths.org/telecharger/",
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
    mactex   = "/Library/TeX/texbin:/usr/texbin:/usr/local/bin"
    macports = "/opt/local/bin:/opt/local/sbin"
    fink     = "/sw/bin"
    path     = "%s:%s:%s" % (mactex, macports, fink)
    f = open('dist/Pyromaths.app/Contents/MacOS/setenv.sh', 'w')
    f.write('''#!/bin/sh
PWD=$(dirname "$0"); /usr/bin/env PATH="$PATH:%s" $PWD/pyromaths''' % path)
    os.system("chmod +x dist/Pyromaths.app/Contents/MacOS/setenv.sh")
    os.system("sed -i '' '23s/pyromaths/setenv.sh/' dist/Pyromaths.app/Contents/Info.plist")
