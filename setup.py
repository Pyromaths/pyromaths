#!/usr/bin/python
# -*- coding: utf-8 -*-
#
from distutils.core import setup
import glob

setup(name = "Pyromaths",
    version = "10.10",
    description = "Génère des exercices types de mathématiques de collège et leur corrigé au format LaTeX.",
    author = "Jérôme Ortais",
    author_email = "jerome.ortais@pyromaths.org",
    url = "http://www.pyromaths.org",
    packages=['', 'troisiemes', 'quatriemes', 'cinquiemes', 'sixiemes', 'lycee',
        'outils', 'classes'],
    data_files=[('img', ['img/pyromaths.ico', 'img/pyromaths.png',
        'img/pyromaths-banniere.png', 'img/whatsthis.png']),
        (r'modeles', glob.glob(r'modeles/*')),
        (r'img/vignettes', glob.glob(r'img/vignettes/*')),
        ],
    scripts = ["runner/pyromaths"],
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
