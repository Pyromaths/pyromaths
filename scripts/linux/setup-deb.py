#!/usr/bin/python
# -*- coding: utf-8 -*-

from glob import glob
from py2deb import Py2deb

version = "10.06"
changelog = open("README.txt", "r").read()

p = Py2deb("pyromaths")
p.author = "J\xe9r\xf4me Ortais"
p.mail = "jerome.ortais@pyromaths.org"
p.description = \
    """G\xe9n\xe9rateur d'exercices
Pyromaths g\xe9n\xe8re des exercices types de math\xe9matiques de coll\xe8ge et\nleur corrig\xe9 au format LaTeX."""
p.url = "http://www.pyromaths.org"
p.depends = "python-qt4, python-lxml, texlive-pstricks, texlive-latex-base, texlive-latex-extra, texlive-fonts-recommended, texlive-latex-recommended"
p.licence = "gpl"
p.section = "math"
p.arch = "all"
p["/usr/share/applications"] = ["data/pyromaths.desktop|pyromaths.desktop"]
p["/usr/share/pixmaps"] = ["data/pyromaths.png|pyromaths.png",
                           "data/pyromaths-banniere.png|pyromaths-banniere.png"]
p["/usr/lib/pyromaths"] = glob("sixiemes/*.py") + glob("cinquiemes/*.py") + \
                          glob("quatriemes/*.py") + glob("troisiemes/*.py") +\
                          glob("classes/*.py") + glob("lycee/*.py") +\
                          glob("modeles/*.tex") + glob("outils/*.py") + \
                          ["interface.py", ]
p["/usr/bin"] = ["pyromaths.py|pyromaths"]
p["/usr/share/doc/pyromaths"] = ["README.txt", "licence.txt"]

p.generate(version, changelog, rpm=True, src=True)
