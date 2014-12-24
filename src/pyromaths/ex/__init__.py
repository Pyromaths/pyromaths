#!/usr/bin/python
# -*- coding: utf-8 -*-
#
import inspect
import os
import pkgutil
import types
import sys

levels = {}


class Exercise(object):
    ''' Base class for all exercise types. '''

    def __str__(self):
        return self.description


class TexExercise(Exercise):
    ''' Exercise with TeX support. '''

    def tex_statement(self):
        ''' Return problem statement in TeX format. '''
        raise NotImplementedError()
        return ["\\exercice TODO"]

    def tex_answer(self):
        ''' Return full answer in TeX format. '''
        return ["\\exercice* TODO"]


class __LegacyExercise(TexExercise):
    ''' Base class for legacy format exercise proxies. '''

    _id = 0
    function = []

    def __init__(self):
        self.stat, self.ans = self.function[0]()

    def tex_statement(self):
        return self.stat

    def tex_answer(self):
        return self.ans


def __legacy(function, thumb):
    ''' Create a new class proxying for a legacy exercise 'function'. '''
    __LegacyExercise._id += 1
    # Create a proxy class inheriting from LegacyExercise for this function
    return type('LegacyExercise%u' % __LegacyExercise._id,
                (__LegacyExercise,),
                dict(description=function.description,
                     level=function.level,
                     thumb=thumb,
                     function=(function,),
                     )
                )

def __hasdescription(obj):
    ''' Has 'obj' a legit description? '''
    if 'description' not in dir(obj): return False
    description = obj.__dict__['description']
    # description must be some kind of string (preferably unicode)
    if not isinstance(description, basestring): return False
    return True

def __islegacy(obj):
    ''' Is target object an exercise in legacy format? '''
    return inspect.isfunction(obj) and __hasdescription(obj)

def __isexercise(obj):
    ''' Is target object an exercise (in new format)? '''
    return inspect.isclass(obj) and issubclass(obj, Exercise) and __hasdescription(obj)

def __level(level):
    ''' Format academic level(s). '''
    # level may be a string or a list (default)
    if not isinstance(level, list): level = [level]
    level.sort()
    return level

def __import(name=__name__, parent=None):
    ''' Import 'name' from 'parent' package. '''
    if not isinstance(name, basestring):
        name = name.__name__
    # parent is None: assume 'name' is a package name
    # hack tout moche pour l'import des exercices dans la version Windows de Pyromaths :
    # Les modules sixiemes, quatriemes doivent être appelés avec le chemin complet,
    # alors que les exercices cinquiemes.aires ne doivent être appelés qu'ainsi.
    if "." not in name and hasattr(sys, "frozen"): name = "pyromaths.ex." + name
    if parent is None: parent = name
    elif not isinstance(parent, basestring):
        # assume 'parent' is a package instance
        parent = parent.__name__
    return __import__(name, fromlist=parent)

def _exercises(pkg):
    ''' List exercises in 'pkg' modules. '''
    from pyromaths.Values import data_dir
    # level defaults to description, then unknown
    if 'level' not in dir(pkg): pkg.level = u"Inconnu"
    n = 0
    for _, name, ispkg in pkgutil.iter_modules(pkg.__path__, pkg.__name__ + '.'):
        # skip packages
        if ispkg: continue;
        # import module
        mod = __import(name, pkg)
        if 'level' not in dir(mod): mod.level = pkg.level
        # search exercises in module
        for element in dir(mod):
            element = mod.__dict__[element]
            level = __level(element.level if 'level' in dir(element)
                              else mod.level)

            dirlevel = os.path.split(pkg.__path__[0])[1]
            thumb = os.path.join(data_dir(), 'ex', dirlevel, 'img', 'ex-%02d.png' % n)
            if __isexercise(element):
                element.level = level
                element.thumb = thumb
                yield element
                n += 1
            elif __islegacy(element):
                element.level = level
                yield __legacy(element, thumb)
                n += 1

def _subpackages(pkg):
    ''' List 'pkg' sub-packages. '''
    for _, name, ispkg in pkgutil.iter_modules(pkg.__path__, pkg.__name__ + '.'):
        # skip modules
        if not ispkg: continue;
        yield __import(name, pkg)

def load(pkg=None, recursive=True):
    ''' Discover exercises. '''
    # target package defaults to this package (pyromaths.ex)
    if pkg is None: pkg = __import()
    # load package exercises
    for ex in _exercises(pkg):
        for lvl in ex.level:
            # new level? create its exercise list
            if lvl not in levels.keys(): levels[lvl] = []
            levels[lvl].append(ex)

    if not recursive: return
    # load sub-packages
    for pk in _subpackages(pkg): load(pk)
