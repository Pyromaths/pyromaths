#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
from __future__ import unicode_literals
from builtins import object
import collections
import inspect
import os
import pkgutil
import types
import sys
import importlib
import jinja2

class TexExercise:
    """Exercise with TeX support."""

    @classmethod
    def name(cls):
        return cls.__name__

    @classmethod
    def description(cls):
        return cls.__doc__.splitlines()[0]

    @classmethod
    def thumb(cls):
        from pyromaths.Values import data_dir
        return os.path.join(data_dir(), 'ex', 'img', "%s.png" % cls.name())

    def tex_statement(self):
        ''' Return problem statement in TeX format. '''
        raise NotImplementedError()

    def tex_answer(self):
        ''' Return full answer in TeX format. '''
        raise NotImplementedError()


class LegacyExercise(TexExercise):
    """Base class for legacy format exercise proxies.

    This class is deprecated. Do not use it to write new exercises.
    """

    def __init__(self):
        self.stat, self.ans = self.__class__.function()

    def tex_statement(self):
        return "\n".join(self.stat)

    def tex_answer(self):
        return "\n".join(self.ans)

def __module(filename):
    """Expect an absolute path, subpath of this module's path. Return a relative path."""
    # Get root of this application
    root = '/'.join(__file__.split('/')[:-len(__name__.split('.')) - 1])
    # Get filename, relative to said root
    relative = filename[len(root)+1:]
    # Remove extension
    relative = relative[:-len('.py')]
    # Turn file system path into python package
    relative = relative.replace('/', '.')

    return relative

def __import(name=__name__, parent=None):
    ''' Import 'name' from 'parent' package. '''
    if not isinstance(name, str):
        name = name.__name__
    # parent is None: assume 'name' is a package name
    # hack tout moche pour l'import des exercices dans la version Windows de Pyromaths :
    # Les modules sixiemes, quatriemes doivent être appelés avec le chemin complet,
    # alors que les exercices cinquiemes.aires ne doivent être appelés qu'ainsi.
    if "." not in name and hasattr(sys, "frozen"): name = "pyromaths.ex." + name
    if parent is None: parent = name
    elif not isinstance(parent, str):
        # assume 'parent' is a package instance
        parent = parent.__name__
    return importlib.import_module(name)
    # return __import__(name, fromlist=parent)

def iter_exercises(pkg):
    ''' List exercises in 'pkg' modules. '''
    # level defaults to description, then unknown
    if 'level' not in dir(pkg): pkg.level = "Inconnu"
    for _, name, ispkg in pkgutil.iter_modules(pkg.__path__, pkg.__name__ + '.'):
        # skip packages
        if ispkg: continue;
        # import module
        mod = __import(name, pkg)
        # search exercises in module
        for name in dir(mod):
            cls = getattr(mod, name)
            if name.startswith("_"):
                continue
            if not isinstance(cls, type):
                continue
            if not issubclass(cls, TexExercise):
                continue
            if cls.__module__ == "pyromaths.ex":
                continue
            yield cls

def _subpackages(pkg):
    ''' List 'pkg' sub-packages. '''
    for _, name, ispkg in pkgutil.iter_modules(pkg.__path__, pkg.__name__ + '.'):
        # skip modules
        if not ispkg: continue;
        yield __import(name, pkg)

def load_levels(pkg=None, recursive=True):
    ''' Discover exercises. '''
    levels = collections.defaultdict(list)
    # target package defaults to this package (pyromaths.ex)
    if pkg is None: pkg = __import()
    # load package exercises
    for ex in iter_exercises(pkg):
        for lvl in ex.tags:
            levels[lvl].append(ex)

    if recursive:
        # load sub-packages
        for pk in _subpackages(pkg):
            sublevels = load_levels(pk)
            for lvl in sublevels:
                if lvl in levels:
                    levels[lvl].extend(sublevels[lvl])
                else:
                    levels[lvl] = sublevels[lvl]

    return levels

################################################################################
# Exercices créés à partir de templates Jinja2

def templatedir():
    from pyromaths import Values
    return os.path.join(
        Values.data_dir(),
        "ex",
        "templates",
        )

class Jinja2Exercise(TexExercise):
    """Exercice utilisant un template jinja2."""

    def __init__(self):
        super().__init__()
        self.context = {}

    @property
    def environment(self):
        """Création de l'environnement Jinja2, duquel sera chargé le template."""
        environment = jinja2.Environment(
            loader=jinja2.FileSystemLoader(templatedir())
        )
        environment.block_start_string = '(*'
        environment.block_end_string = '*)'
        environment.variable_start_string = '(('
        environment.variable_end_string = '))'
        environment.comment_start_string = '(% '
        environment.comment_end_string = ' %)'
        environment.trim_blocks = True
        environment.lstrip_blocks = True

        return environment

    @property
    def statement_name(self):
        """Nom du fichier de l'énoncé (sans le répertoire)."""
        return os.path.join("{}-statement.tex".format(self.__class__.__name__))

    @property
    def answer_name(self):
        """Nom du fichier du corrigé (sans le répertoire)."""
        return os.path.join("{}-answer.tex".format(self.__class__.__name__))

    def tex_statement(self):
        """Génération de l'énoncé"""
        return self.environment.get_template(self.statement_name).render(self.context)

    def tex_answer(self):
        """Génération du corrigé"""
        return self.environment.get_template(self.answer_name).render(self.context)

