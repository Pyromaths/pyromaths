#!/usr/bin/python
# -*- coding: utf-8 -*-
#
from time import strftime
from os.path import normpath, dirname, exists, abspath, join
from os import environ, name
from sys import executable, getfilesystemencoding
import sys
#import troisiemes.troisiemes, quatriemes.quatriemes, cinquiemes.cinquiemes
#import sixiemes.sixiemes, lycee.lycee

def we_are_frozen():
    """Returns whether we are frozen via py2exe.
    This will affect how we find out where we are located."""
    return hasattr(sys, "frozen")

def data_dir():
    """Renvoie le dossier data, selon qu'on utilise pyromaths à partir des
    sources, de l'exécutable win32 ou du paquet deb"""
    if we_are_frozen():
        return join(normpath(dirname(unicode(executable,
            getfilesystemencoding()))), 'data')
    elif exists(join(abspath(dirname(__file__)),'../data/')):
        return normpath(join(abspath(dirname(__file__)),'../data/'))
    else:
        return '/usr/share/pyromaths/'

if name == 'nt':
    def home():
        return unicode(environ['USERPROFILE'], getfilesystemencoding())
    def configdir():
        return join(unicode(environ['APPDATA'], getfilesystemencoding()),
                "pyromaths")
elif sys.platform == "darwin":  #Cas de Mac OS X.
    def home():
        return unicode(environ['HOME'], getfilesystemencoding())
    def configdir():
        return join(home(), "Library", "Application Support", "Pyromaths")
else:
    def home():
        try:
            return unicode(environ['HOME'], getfilesystemencoding())
        except KeyError:
            # Pyromaths en ligne, l'user apache n'a pas de $HOME
            return ""
    def configdir():
        return join(home(), ".config", "pyromaths")

VERSION = '11.05.1b1'
COPYRIGHT_YEAR = strftime('%Y')
COPYRIGHTS = u'© 2006 – %s Jérôme Ortais<br/>\n' \
        u'<span style=" font-size:small;">Pyromaths est distribué sous ' \
        u'licence GPL.</span>' % (COPYRIGHT_YEAR)
WEBSITE = 'http://www.pyromaths.org/'
DATADIR = data_dir()
HOME = home()
CONFIGDIR = configdir()

LESFICHES = [[u'Sixième', '', [
u'Calcul mental',
u'Écrire un nombre décimal',
u'Placer une virgule',
u'Écriture fractionnaire ou décimale',
u'Décomposition de décimaux',
u'Conversions unités',
u"Conversions unités d'aires",
u"Conversions unités de volumes",
u'Poser des opérations (sauf divisions)',
u'Produits, quotients par 10, 100, 1000',
u'Classer des nombres décimaux',
u'Droites, demi-droites, segments',
u'Droites perpendiculaires et parallèles',
u'Propriétés sur les droites',
u'Multiples de 2, 3, 5, 9, 10',
u'Fractions partage',
u'Fractions et abscisses',
u'Aires et quadrillage',
u'Symétrie et quadrillages',
u'Mesurer des angles',
u'Représentation dans l\'espace',
u'Arrondir des nombres décimaux'
]],
[u'Cinquième', '', [
u'Priorités opératoires',
u'Symétrie centrale',
u'Fractions égales',
u'Sommes de fractions',
u'Produits de fractions',
u'Repérage',
u'Addition de relatifs',
u'Construction de triangles',
u'Construction de parallélogrammes',
u'Échelles',
u'Aire de disques',
u'Représentation de données',
]],
[u'Quatrième', '', [
u'Calcul mental',
u'Sommes de fractions',
u'Produits et quotients de fractions',
u'Fractions et priorités',
u'Bases du calcul littéral',
u'Réduire des expressions littérales',
u'Propriétés sur les puissances',
u'Propriétés sur les puissances de 10',
u'Écritures scientifiques',
u'Puissances de 10',
u'Distributivité',
u'Double distributivité',
u'Théorème de Pythagore',
u'Réciproque du théorème de Pythagore',
u'Cercle et théorème de Pythagore',
u'Théorème de Thalès',
u'Trigonométrie',
]],
[u'Troisième', '', [
u'Fractions',
u'Puissances',
u'PGCD',
u'Développements',
u'Factorisations',
u'Dévt, factorisat°, calcul et éq° produit',
u'Équation',
u'Racines carrées',
u'Système d\'équations',
u'Fonctions affines',
u'Probabilités',
u'Théorème de Thalès',
u'Réciproque du théorème de Thalès',
u'Trigonométrie',
u'Arithmétique'
]],
[u'Lycée', '', [
u'Équations 2° degré',
u'Factorisations 2° degré',
u'Factorisations degré 3',
u'Étude de signe',
u"Sens de variations",
u"Étude de fonctions",
u"Vecteurs",
], [
u'Niveau 1èreS',
u'Niveau 1èreS',
u'Niveau 1èreS',
u'Niveau 1èreS',
u"Niveau 1èreS, Term STG",
u"Niveau Term S",
u"Niveau Seconde",
]],
]

