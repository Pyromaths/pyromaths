from setuptools import setup

APP = ['../../src/pyromaths/pyromaths.py']
DATA_FILES = ['pyromaths.icns', 'qt.conf', '../../src/pyromaths/sixiemes', '../../src/pyromaths/cinquiemes', '../../src/pyromaths/quatriemes', '../../src/pyromaths/troisiemes', '../../src/pyromaths/classes', '../../src/pyromaths/lycee', '../../src/pyromaths/outils', '../../src/pyromaths/__init__.py', '../../src/pyromaths/interface.py']
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