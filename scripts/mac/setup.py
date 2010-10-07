from setuptools import setup

APP = ['../../pyromaths.py']
DATA_FILES = ['pyromaths.icns', '../../sixiemes', '../../cinquiemes', '../../quatriemes', '../../troisiemes', '../../classes', '../../lycee', '../../outils', 'qt.conf']
OPTIONS = dict(
        plist='Info.plist',
        argv_emulation=True,
        includes=['gzip', 'sip', 'PyQt4']
    )
setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)