import inspect
import os
import types
import pkgutil

levels = {}


class Exercise(object):
    ''' Base class for all exercise types. '''

    description = u'Description'
    levels      = u'Academic level'
    thumb       = 'path/to/thumbnail.png'

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


def __legacy(path, i, function):
    ''' Create a new class proxying for a legacy exercise 'function'. '''
    __LegacyExercise._id += 1
    # Create a proxy class inheriting from LegacyExercise for this function
    return type('LegacyExercise%u' % __LegacyExercise._id,
                (__LegacyExercise,),
                dict(description=function.description,
                     levels=function.level,
                     thumb=os.path.join(path, 'img', 'ex-%02d.png' % i),
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

def __isexercise(obj):
    ''' Is target object an exercise in legacy format? '''
    return inspect.isfunction(obj) and __hasdescription(obj)

def __levels(level):
    ''' Format academic level(s). '''
    # level may be a string or a list (default)
    if not isinstance(level, list): level = [level]
    return level

def __import(name=__name__, parent=None):
    ''' Import 'name' from 'parent' package. '''
    if not isinstance(name, basestring):
        name = name.__name__
    # parent is None: assume 'name' is a package name
    if parent is None: parent = name
    elif not isinstance(parent, basestring):
        # assume 'parent' is a package instance
        parent = parent.__name__
    return __import__(name, fromlist=parent)

def _exercises(pkg):
    ''' List exercises in 'pkg' modules. '''
    # level defaults to description, then unknown
    if 'level' not in dir(pkg): pkg.level = u"Inconnu"
    n = 0
    for _, name, ispkg in pkgutil.iter_modules(pkg.__path__, pkg.__name__+'.'):
        # skip packages
        if ispkg: continue;
        # import module
        mod = __import(name, pkg)
        if 'level' not in dir(mod): mod.level = pkg.level
        for element in dir(mod):
            element = mod.__dict__[element]
            if not __isexercise(element): continue
            # found an exercise: work out what level it is
            element.level = __levels(element.level if 'level' in dir(element)
                                     else mod.level)
            yield __legacy(pkg.__path__[0], n, element)
            n+=1

def _subpackages(pkg):
    ''' List 'pkg' sub-packages. '''
    for _, name, ispkg in pkgutil.iter_modules(pkg.__path__, pkg.__name__+'.'):
        # skip modules
        if not ispkg: continue;
        yield __import(name, pkg)

def load(pkg=None, recursive=True):
    ''' Discover exercises. '''
    # target package defaults to this package (pyromaths.ex)
    if pkg is None: pkg = __import()
    # load package exercises
    for ex in _exercises(pkg):
        for lvl in ex.levels:
            # new level? create its exercise list
            if lvl not in levels.keys(): levels[lvl] = []
            levels[lvl].append(ex)
    if not recursive: return
    # load sub-packages
    for pk in _subpackages(pkg): load(pk)
