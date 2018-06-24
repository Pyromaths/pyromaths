#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# pylint: disable=invalid-name

"""Crée et met à jour les vignettes des exercices."""

import gettext
import hashlib
import json
import logging
import os
import random
import shutil
import sys
import tempfile
from subprocess import call
from contextlib import contextmanager

# Définition de `_()` comme la fonction identité.
# Pour le moment, les vignettes des exercices ne sont pas traduites.
gettext.install('pyromaths', unicode=1)

ROOTDIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
PYROMATHSPATH = os.path.join(ROOTDIR, "src")

sys.path.insert(0, os.path.realpath(PYROMATHSPATH))
# pylint: disable=wrong-import-position
import pyromaths
from pyromaths.Values import data_dir, configdir
from pyromaths.outils.System import creation

THUMBDIR = os.path.join(data_dir(), "ex", "img")
MD5PATH = os.path.join(THUMBDIR, "md5sum.json")

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(message)s',
    )

@contextmanager
def md5file():
    """Contexte pour lire et écrire les md5sum des exercices."""
    # Création du fichier s'il n'existe pas déjà.
    if not os.path.exists(MD5PATH):
        with open(MD5PATH, mode="w") as fichier:
            json.dump({}, fichier)

    logging.info("Lecture du fichier '%s'.", MD5PATH)
    with open(MD5PATH, mode="r") as fichier:
        md5sums = json.loads(fichier.read())

    yield md5sums

    logging.info("Écriture du fichier '%s'.", MD5PATH)
    with open(MD5PATH, mode="w") as fichier:
        json.dump(md5sums, fichier, sort_keys=True, indent=4)

@contextmanager
def create_temp_dir():
    """Contexte pour la création et la suppression du répertoire temporaire."""
    name = tempfile.mkdtemp()

    yield name

    shutil.rmtree(name)

def parametres_exo(exo, tempdir):
    """Renvoit les paramètres de la création d'un unique exercice."""
    return {
        'creer_pdf': True,
        'creer_unpdf': False,
        'titre': u"Thumbnail",
        'corrige': False,
        'niveau': "",
        'nom_fichier': u'thumb.tex',
        'chemin_fichier': tempdir,
        'fiche_exo': os.path.join(tempdir, 'thumb.tex'),
        'fiche_cor': os.path.join(tempdir, 'thumb-corrige.tex'),
        'configdir': configdir(),
        'datadir': data_dir(),
        'modele': 'pyromaths.tex',
        'openpdf': 0,
        'liste_exos': [exo()],
    }


def create_thumbnail(exercise, tempdir):
    """Crée la vignette de l'exercice"""
    outfile = exercise.thumb()

    logging.info("Compilation de l'exercice.")
    random.seed(0)
    creation(parametres_exo(exercise, tempdir))

    logging.info("Extraction de la vignette.")
    call([
        "convert",
        "-density", "288",
        os.path.join(tempdir, "thumb.pdf"),
        "-resize", "25%",
        "-crop", "710x560+0+85",
        "-flatten", "-trim",
        os.path.join(tempdir, "thumb.png"),
        ])

    logging.info("Appel de `pngnq` sur la vignette.")
    call([
        "pngnq", "-f", "-s1", "-n32", os.path.join(tempdir, "thumb.png"),
        ])
    shutil.copyfile(os.path.join(tempdir, "thumb-nq8.png"), outfile)

    logging.info("Optimisation de la vignette.")
    call(args=["optipng", "-o7", outfile])

def md5sum(exo):
    """Calcule et renvoit le hash md5sum de l'énoncé 0 de l'exercice."""
    random.seed(0)
    return hashlib.md5(
        "\n"
        .join(exo().tex_statement())
        .encode(errors="backslashreplace")
        ).hexdigest()

def main(tempdir):
    """Fonction principale"""
    with md5file() as md5sums:
        levels = pyromaths.ex.load_levels()
        for level in levels:
            for exo in levels[level]:
                logging.info("Exercice '%s'.", exo.name())
                if md5sums.get(exo.name(), "0") == md5sum(exo):
                    logging.info("L'exercice n'a pas été modifié.")
                    continue
                create_thumbnail(exo, tempdir)
                md5sums[exo.name()] = md5sum(exo)

if __name__ == "__main__":
    with create_temp_dir() as temp:
        main(temp)
