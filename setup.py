#!/usr/bin/python
# -*- coding: utf-8 -*-
#
from distutils.core import setup
#from distutils.cmd import Command
#from setuptools import setup

import glob
setup(name = "Pyromaths",
    #install_requires=['distribute'],
    version = "10.10",
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
        ('share/pyromaths/images', ['data/images/pyromaths.ico',
            'data/images/pyromaths.png', 'data/images/pyromaths-banniere.png',
            'data/images/whatsthis.png']
        ),
        (r'share/pyromaths/images/vignettes',
            glob.glob(r'data/images/vignettes/*.png')),
        (r'share/pyromaths/templates', glob.glob(r'data/templates/*.tex')),
        (r'share/pyromaths/packages', glob.glob(r'data/packages/*')),
        ],
    scripts = ["pyromaths"],
    long_description = """Pyromaths est un programme initié par Jérôme Ortais,
    qui a pour but de créer des exercices type de mathématiques niveau collège
    et lycée ainsi que leur corrigé. C’est ce qu’on appelle parfois un
    exerciseur. Contrairement à de nombreux autres projets, Pyromaths a pour
    objectif de proposer une correction véritablement détaillée des exercices
    proposés et pas seulement une solution.

    Il permet par exemple de proposer des devoirs maison aux élèves et de leur
    distribuer ensuite la correction. Il peut aussi servir à des familles afin
    qu’un élève puisse travailler un point du programme et se corriger
    ensuite."""
)
