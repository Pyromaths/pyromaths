# -*- coding: utf-8 -*-
import sys,os
from glob import glob
from setuptools import setup, find_packages

sys.path.append('../../src')
from pyromaths.Values import VERSION

plist = dict(
        CFBundleIdentifier = "org.pyromaths.pyromaths",
        CFBundleName = "Pyromaths",
        CFBundlePackageType = "APPL",
        CFBundleShortVersionString = "%s" % VERSION,
        CFBundleVersion = "%s" % VERSION,
        NSHumanReadableCopyright = u"© Jérôme Ortais",
        CFBundleIconFile = "pyromaths",
        CFBundleDevelopmentRegion = "French",
        CFBundleExecutable = "pyromaths",
        CFBundleDisplayName = "pyromaths",
        CFBundleSignature = "PYTS"
        )

qt_unused = ['QtDBus', 'QtDeclarative', 'QtDesigner', 'QtHelp', 'QtMultimedia',
             'QtNetwork', 'QtOpenGL', 'QtScript', 'QtScriptTools', 'QtSql',
             'QtSvg', 'QtTest', 'QtWebKit', 'QtXml', 'QtXmlPatterns', 'phonon']
OPTIONS = dict(
        plist=plist,
        argv_emulation=True,
        iconfile='pyromaths.icns',
        includes=['gzip'],
        excludes=['PyQt4.%s'%f for f in qt_unused],
        dylib_excludes=qt_unused,
)

setup(
    app         = ['../../src/pyromaths.py'],
    packages    = find_packages('../../src'),
    package_dir = {'': '../../src'},
    data_files  = [('data', glob('../../data/*'))],
    options={'py2app': OPTIONS},
    setup_requires=['py2app>=0.7.3', 'lxml>=2.2.2'],
)

# setenv.sh hack
# Define a custom executable in order to pass an updated path
# with the location of several LaTeX distributions
file = open('dist/Pyromaths.app/Contents/MacOS/setenv.sh', 'w')
file.write('#!/bin/sh\n\n# Path to several LaTeX distributions\nMACTEX="/usr/texbin:/usr/local/bin"\nMACPORTS="/opt/local/bin:/opt/local/sbin"\nFINK="/sw/bin"\n\n# Launch Pyromaths with updated path\nPWD=$(dirname "$0")\n/usr/bin/env PATH="$PATH:$MACTEX:$MACPORTS:$FINK" $PWD/pyromaths\n')
os.system("chmod +x dist/Pyromaths.app/Contents/MacOS/setenv.sh")
os.system("sed -i '' '23s/pyromaths/setenv.sh/' dist/Pyromaths.app/Contents/Info.plist")
