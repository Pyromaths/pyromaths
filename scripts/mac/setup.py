from glob import glob
from setuptools import setup, find_packages

qt_unused = ['QtDBus', 'QtDeclarative', 'QtDesigner', 'QtHelp', 'QtMultimedia',
             'QtNetwork', 'QtOpenGL', 'QtScript', 'QtScriptTools', 'QtSql',
             'QtSvg', 'QtTest', 'QtWebKit', 'QtXml', 'QtXmlPatterns', 'phonon']
OPTIONS = dict(
        plist='Info.plist',
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
