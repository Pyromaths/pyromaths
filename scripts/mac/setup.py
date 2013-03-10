from setuptools import setup

APP = ['../../src/pyromaths.py']
DATA_FILES = ['pyromaths.icns', 'qt.conf', '../../src/sixiemes', '../../src/cinquiemes', '../../src/quatriemes', '../../src/troisiemes', '../../src/classes', '../../src/lycee', '../../src/outils', '../../src/__init__.py', '../../src/interface.py', '../../src/Values.py']
OPTIONS = dict(
        plist='Info.plist',
        argv_emulation=True,
        packages=['lxml'],
        includes=['gzip', 'sip', 'PyQt4'],
    )
setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)