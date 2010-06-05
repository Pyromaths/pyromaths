from setuptools import setup

APP = ['../../pyromaths.py']
DATA_FILES = ['pyromaths.icns', '../../sixiemes', '../../cinquiemes', '../../quatriemes', '../../troisiemes', '../../classes', '../../lycee', '../../outils']
OPTIONS = dict(
        plist='Info.plist',
        argv_emulation=True,
        includes=['sip', 'PyQt4._qt']
    )
setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)