#!/usr/bin/python
# -*- coding: utf-8 -*-

from distutils.core import setup
import glob
from src.Values import VERSION

setup(name = "pyromaths",
    version = VERSION,
    description = "Exerciseur de mathématiques créant des fiches aux formats " \
            + "LaTeX et PDF.",
    license = "GPL",
    author = "Jérôme Ortais",
    author_email = "jerome.ortais@pyromaths.org",
    url = "http://www.pyromaths.org",
    package_dir={'pyromaths': 'src'},
    packages=['pyromaths', 'pyromaths.troisiemes', 'pyromaths.quatriemes',
        'pyromaths.cinquiemes', 'pyromaths.sixiemes', 'pyromaths.lycee',
        'pyromaths.outils', 'pyromaths.classes'],
    data_files=[
        ('share/pyromaths/images', [ 'data/images/pyromaths.png',
            'data/images/pyromaths-banniere.png', 'data/images/whatsthis.png' ]
        ),
        ('share/applications', ['data/linux/pyromaths.desktop']),
        ('share/man/man1', ['data/linux/pyromaths.1']),
        (r'share/pyromaths/images/vignettes',
            glob.glob(r'data/images/vignettes/*.png')),
        (r'share/pyromaths/templates', glob.glob(r'data/templates/*.tex')),
        (r'share/pyromaths/packages', glob.glob(r'data/packages/*')),
        ],
    scripts = ["pyromaths"],
    platforms = ['unix'],
    long_description = """Pyromaths est un programme qui a pour but de créer
    des exercices type de mathématiques niveau collège et lycée ainsi que leur
    corrigé. C’est ce qu’on appelle parfois un exerciseur.  Contrairement à de
    nombreux autres projets, Pyromaths a pour objectif de proposer une
    correction véritablement détaillée des exercices proposés et pas seulement
    une solution.

    Il permet par exemple de proposer des devoirs maison aux élèves et de leur
    distribuer ensuite la correction. Il peut aussi servir à des familles afin
    qu’un élève puisse travailler un point du programme et se corriger
    ensuite."""
    )
