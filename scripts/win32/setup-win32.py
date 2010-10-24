#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

from distutils.core import setup
import py2exe
import glob
#glob sert à chercher tous les fichiers d'un dossier
#import py2app

setup(
    name='Pyromaths',
    version='10.10',
    package_dir={'': 'pyromaths'},
    packages=['', 'troisiemes', 'quatriemes', 'cinquiemes', 'sixiemes', 'lycee',
        'outils', 'classes', 'img'],
    data_files=[('img', ['pyromaths/img/pyromaths.ico',
        'pyromaths/img/pyromaths.png', 'img/whatsthis.png',
        'pyromaths/img/pyromaths-banniere.png']),
        (r'modeles', glob.glob(r'pyromaths/modeles/*')),
        (r'img/vignettes', glob.glob(r'pyromaths/img/vignettes/*')),
        'pyromaths/msvcp71.dll', 'pyromaths/README.txt'],
    author = 'Jérôme Ortais',
    author_email = 'jerome.ortais@pyromaths.org',
    url = 'http://www.pyromaths.org',
    description = 'Génère des exercices types de mathématiques de collège et leur corrigé au format LaTeX.',
    platforms = ['unix', 'macOS', 'windows'],
    license = 'GPL',
    
    options = {"py2exe": {"compressed": 1,
    #"optimize": 0, "bundle_files": 1, "includes":["sip"], "packages": ["lxml"]} },
    "optimize": 0, "bundle_files": 1, "includes":["sip"]} },
    zipfile = None,
    windows=[
      {'script': "pyromaths\pyromaths.py",
       'icon_resources': [(1, 'pyromaths/img/pyromaths.ico')]},
        ]
    )
