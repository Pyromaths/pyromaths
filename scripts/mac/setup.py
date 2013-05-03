# -*- coding: utf-8 -*-
from glob import glob
from setuptools import setup, find_packages

import sys
sys.path.append('../../src/pyromaths/')
from Values import VERSION

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
