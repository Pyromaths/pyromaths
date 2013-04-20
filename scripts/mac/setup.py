from glob import glob
from setuptools import setup, find_packages

OPTIONS = dict(
        plist='Info.plist',
        argv_emulation=True,
        packages=['lxml'],
        includes=['gzip', 'sip', 'PyQt4'],
    )
setup(
    app         = ['../../src/pyromaths.py'],
    packages    = find_packages('../../src'),
    package_dir = {'': '../../src'},
    data_files  = ['pyromaths.icns', 'qt.conf', ('data', glob('../../data/*'))],
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)