#!/usr/bin/python
# -*- coding: utf-8 -*-

from distutils.core import setup
import py2exe, glob, os, innosetup
# Cruft dedicating to importing version number
import sys
from os.path import dirname, join, realpath
basedir = dirname(realpath(__file__))
sys.path.insert(0, join(basedir,'src'))
from pyromaths.Values import VERSION

setup_iss = '''
[Setup]
Compression=lzma/max
OutputBaseFilename=pyromaths-%s-win32
[Languages]
Name: "french"; MessagesFile: "compiler:Languages\French.isl"
[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
[Icons]
Name: "{commondesktop}\Pyromaths"; Filename: "{app}\pyromaths.exe"
''' % VERSION

setup(name = "Pyromaths",
    version = "%s" % VERSION,
    description = u"Exerciseur de mathématiques créant des fiches aux formats " \
            + u"LaTeX et PDF.",
    license = "GPL",
    author = u"Jérôme Ortais",
    author_email = "jerome.ortais@pyromaths.org",
    url = "http://www.pyromaths.org",
    package_dir={'': 'src'},
    packages=['pyromaths', 'pyromaths.troisiemes', 'pyromaths.quatriemes',
        'pyromaths.cinquiemes', 'pyromaths.sixiemes', 'pyromaths.lycee',
        'pyromaths.outils', 'pyromaths.classes'],
    data_files=[
        ('data/images', ['data/images/pyromaths.ico',
            'data/images/pyromaths.png', 'data/images/pyromaths-banniere.png',
            'data/images/whatsthis.png']
        ),
        (r'data/images/vignettes',
            glob.glob(r'data/images/vignettes/*.png')),
        (r'data/templates', glob.glob(r'data/templates/*.tex')),
        (r'data/packages', glob.glob(r'data/packages/*')),
        ],
    platforms = ['windows'],
    options =
    {
        'py2exe':
        {
            "compressed": 1, "optimize": 2, "bundle_files": 3,
            "includes":["sip", "gzip"]
        },
       'innosetup':
       {
           'inno_script': setup_iss,
           'compressed': True,
       }
    },
    zipfile = None,
    windows=[
      {'script': "Pyromaths.py",
       'icon_resources': [(1, 'data/images/pyromaths.ico')],
       }]
    )
