#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Pyromaths
# Un programme en Python qui permet de créer des fiches d'exercices types de
# mathématiques niveau collège ainsi que leur corrigé en LaTeX.
# Copyright (C) 2006 -- Jérôme Ortais (jerome.ortais@pyromaths.org)
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301 USA
#

from pyromaths import ex
from math import sqrt
import random
from pyromaths.outils import Priorites3
import textwrap
from pyromaths.classes.Fractions import Fraction
from pyromaths.classes.PolynomesCollege import Polynome, factoriser
from pyromaths.classes.SquareRoot import SquareRoot
from pyromaths.outils.Arithmetique import carrerise, pgcd, valeur_alea

FRANCAIS_ORDINAL = {
    1: u"premier",
    2: u"deuxième",
    3: u"troisième",
    4: u"quatrième",
    5: u"cinquième",
    }
FRANCAIS_INVERSE = {
    2: u"à la moitié du",
    3: u"au tiers du",
    4: u"au quart du",
    5: u"au cinquième du",
    6: u"au sixième du",
    7: u"au septième du",
    8: u"au huitième du",
    9: u"au neuvième du",
    10: u"au dixième du",
    }
FRANCAIS_MULTIPLE = {
    2: u"au double du",
    3: u"au triple du",
    4: u"au quadruple du",
    5: u"à cinq fois le",
    6: u"à six fois le",
    7: u"à sept fois le",
    8: u"à huit fois le",
    9: u"à neuf fois le",
    10: u"à dix fois le",
    }

class Fraction:
    def __init__(self, numerateur, denominateur):
        self.numerateur = numerateur
        self.denominateur = denominateur

    def latex(self):
        if self.denominateur == 1:
            return str(self.numerateur)
        else:
            return ur"\frac{{ {} }}{{ {} }}".format(
                    self.numerateur,
                    self.denominateur,
                    )

class Entier:
    def __init__(self, valeur):
        self.valeur = valeur

    def __int__(self):
        return self.valeur

    def __neg__(self):
        return self.__class__(- self.valeur)

    def latex(self, signe="-"):
        if signe == "+":
            if self.valeur > 0:
                return "+" + str(self.valeur)
            else:
                return "-" + str(abs(self.valeur))
        else:
            if self.valeur > 0:
                return str(self.valeur)
            else:
                return "-" + str(abs(self.valeur))

FRACTIONS = [
        Fraction(2, 1),
        Fraction(3, 1),
        Fraction(4, 1),
        Fraction(5, 1),
        Fraction(10, 1),
        Fraction(1, 2),
        Fraction(1, 3),
        Fraction(1, 4),
        Fraction(1, 5),
        Fraction(1, 10),
        Fraction(2, 3),
        Fraction(1, 4),
        Fraction(3, 4),
        Fraction(2, 5),
        Fraction(3, 5),
        Fraction(4, 5),
        ]

class Fonction:

    def calcule(self, x):
        raise NotImplementedError()

    def resultat(self, variable):
        raise NotImplementedError()

    def expression(self, variable):
        raise NotImplementedError()

class Lineaire(Fonction):

    def __init__(self):
        self.coeff = random.choice(FRACTIONS)

    def expression(self, variable):
        return ur"{coeff}{variable}".format(
            coeff=self.coeff.latex(),
            variable=variable,
            )

class Affine(Fonction):

    def __init__(self):
        self.coeff = random.choice(FRACTIONS)
        ordonnee = random.randint(1, 10)
        if random.randint(1, 2) == 1:
            ordonnee = -ordonnee
        self.ordonnee = Entier(ordonnee)

    def expression(self, variable):
        return ur"{coeff}{variable}{ordonnee}".format(
            coeff=self.coeff.latex(),
            ordonnee=self.ordonnee.latex("+"),
            variable=variable,
            )

class FractionProduit(Fonction):

    def __init__(self):
        self.numerateur = Entier(random.randint(2, 10))
        self.denominateur = Entier(random.randint(2, 10))

    def expression(self, variable):
        return ur"\frac{{ {numerateur}^{variable} }}{{ {denominateur}{variable} }}".format(
                numerateur=self.numerateur.latex("-"),
                denominateur=self.denominateur.latex("-"),
                variable=variable,
            )

class PolynomeCarre(Fonction):

    def __init__(self):
        coef = [0]*3
        for i in [0, 1, 2]:
            coef[i] = random.randint(2, 5)
            if random.randint(0,1) == 0:
                coef[i] = -coef[i]
        self.coef = [Entier(i) for i in coef]

    def expression(self, variable):
        return ur"{coef[2]}{variable}^2{coef[1]}{variable}{coef[0]}".format(
            coef=[self.coef[2]("-"), self.coef[1]("+"), self.coef[0]("+")],
            variable=variable,
            )

class Harmonique(Fonction):

    def __init__(self):
        for attr in ["numerateur", "denominateur"]:
            binome = [0, 0]
            for i in [0, 1]:
                binome[i] = random.randint(2, 5)
                if random.randint(0,1) == 0:
                    binome[i] = -binome[i]
            setattr(self, attr, [Entier(i) for i in binome])

    def expression(self, variable):
        return ur"\frac{{ {numerateur[1]}{variable}{numerateur[0]} }}{{ {denominateur[1]}{variable}{denominateur[0]} }}".format(
                numerateur=[self.numerateur[0].latex("-"), self.numerateur[0].latex("+")],
                denominateur=[self.denominateur[0].latex("-"), self.denominateur[0].latex("+")],
                variable=variable,
                )

class IdentiteTranslatee(Fonction):

    def __init__(self):
        ordonnee = random.randint(1, 10)
        if random.randint(1, 2) == 1:
            ordonnee = -ordonnee
        self.ordonnee = Entier(ordonnee)

    def expression(self, variable):
        return ur"{variable}{ordonnee}".format(
            variable=variable,
            ordonnee=self.ordonnee.latex("+"),
            )

class FrancaisGeometrique(Fonction):

    def __init__(self):
        if random.randint(1, 2) == 1:
            self.raison = Fraction(1, random.randint(2, 10))
        else:
            self.raison = Fraction(random.randint(2, 10), 1)

    @property
    def francais(self):
        if self.raison.numerateur == 1:
            return u"{} du précédent".format(FRANCAIS_INVERSE[self.raison.denominateur])
        else:
            return u"{} précédent".format(FRANCAIS_MULTIPLE[self.raison.numerateur])

class FrancaisArithmetique(Fonction):

    def __init__(self):
        self.raison = random.randint(1, 10)
        if random.randint(1, 2) == 1:
            self.raison = -self.raison

    @property
    def francais(self):
        if self.raison > 0:
            return u"au terme précédent auquel on ajoute {}".format(self.raison)
        else:
            return u"au terme précédent auquel on soustrait {}".format(-self.raison)

class FrancaisOppose(Fonction):

    @property
    def francais(self):
        return u"à l'opposé du précédent"

    def expression(self, variable):
        # L'argument est forcément un entier
        if variable < 0:
            return ur"-\left({}\right)".format(variable)
        else:
            return ur"-{}".format(variable)

    def etapes(self, argument):
        yield Entier(-argument.valeur).latex("-")

    def calcul(self, argument):
        if not isinstance(argument, Entier):
            raise TypeError("Argument must be an instance of `Entier`.")
        return - argument

class FrancaisInverse(Fonction):

    @property
    def francais(self):
        return u"à l'inverse du précédent"

class FrancaisCarre(Fonction):

    @property
    def francais(self):
        return u"au carré du précédent"

class Question:
    pass

class Francais(Question):

    def __init__(self, index0max):
        self.indice0 = random.randint(0, index0max-1)
        self.terme0 = Entier(random.randint(-10, 10))
        self.fonction = random.choice([ # TODO S'assurer que tout fonctionne
            FrancaisGeometrique,
            FrancaisArithmetique,
            FrancaisOppose,
            FrancaisInverse,
            FrancaisCarre,
            ])()

    @property
    def latex_params(self):
        return {
            'indice0': self.indice0,
            'terme0': self.terme0.latex("-"),
            'suivant': self.fonction.francais,
            }

class General(Question):

    def __init__(self, index0max):
        self.indice0 = random.randint(0, index0max-1)
        self.fonction = random.choice([ # TODO S'assurer que toutes les fonctions fonctionnent
            FractionProduit,
            PolynomeCarre,
            Affine,
            Lineaire,
            IdentiteTranslatee,
            Harmonique,
            ])()

    @property
    def latex_params(self):
        return {
            'indice0': self.indice0,
            'fonction': self.fonction.expression(ur"n"),
            }

class Recursif(Question):

    def __init__(self, index0max):
        self.indice0 = random.randint(0, index0max-1)
        self.terme0 = Entier(random.randint(-10, 10))
        self.fonction = random.choice([ # TODO S'assurer que tout fonctionne
            Affine,
            IdentiteTranslatee,
            Lineaire,
            ])()

    @property
    def latex_params(self):
        return {
            'indice0': self.indice0,
            'terme0': self.terme0.latex("-"),
            'fonction': self.fonction.expression(ur"u_n"),
            }

class TermesDUneSuite(ex.TexExercise):

    description = u"Termes d'une suite"
    level = u"1.1èreS"

    def __init__(self):
        random.seed(9)
        self.rang = [0,0,0]
        while self.rang[0] == self.rang[1]:
            self.rang = [random.randint(2, 5), random.randint(2, 5), random.randint(3, 6)]

        self.questions = [
                Francais(index0max=min(self.rang[1:3])),
                General(index0max=min(self.rang[1:3])),
                Recursif(index0max=min(self.rang[1:3])),
                ]

    def tex_statement(self):
        exo = [r'\exercice']
        exo.append(ur'Pour chacune des suites $u$ suivantes, calculer :')
        exo.append(ur' (a) le {} terme ;'.format(FRANCAIS_ORDINAL[self.rang[0]]))
        exo.append(ur' (b) le terme de rang {} ;'.format(self.rang[1]))
        exo.append(ur' (c) $u_{}$.'.format(self.rang[2]))

        exo.append(ur'\begin{enumerate}')
        exo.append(ur'  \item $u$ est une suite de premier terme $u_{indice0}={terme0}$, et dont chaque terme (sauf le premier) est égal {suivant}.'.format(**self.questions[0].latex_params))
        exo.append(ur'  \item $u$ est la suite définie pour $n\geq{indice0}$ par $u_n={fonction}$.'.format(**self.questions[1].latex_params))
        exo.append(textwrap.dedent(ur"""
            \item $u$ est la suite définie pour $n\geq{indice0}$ par :
                \[\left\{{\begin{{array}}{{l}}
                  u_{indice0}={terme0}\\
                  \text{{Pour tout $n\geq{indice0}$ : }} u_{{n+1}}={fonction}.
              \end{{array}}\right.\]
              """).format(**self.questions[2].latex_params))
        exo.append(ur'\end{enumerate}')
        return exo

    def tex_answer(self):
        exo = [r'\exercice*']
        exo.append(ur'\begin{enumerate}')
        #for question in self.questions: #TODO
        for question in [self.questions[0]]:
            if question == self.questions[0]:
                exo.append(ur"  \item Selon l'énoncé, le premier terme est $u_{indice0}={terme0}$. Puisque chaque terme (sauf le premier) est égal {suivant}, on a :".format(**question.latex_params))
            else:
                exo.append(ur"TODO")
            if question != self.questions[1]:
                termes = dict([(question.indice0, question.terme0)])
                calcul_termes = []
                for indice in xrange(question.indice0, max(question.indice0 + self.rang[0], self.rang[1], self.rang[2])-1):
                    calcul = ur"$u_{indice}={fonction}".format(
                        indice=indice+1,
                        fonction=question.fonction.expression("u_{}".format(indice)),
                        )
                    for etape in question.fonction.etapes(termes[indice]):
                        calcul += " =" + etape
                    calcul += "$"
                    termes[indice+1] = question.fonction.calcul(termes[indice])
                    calcul_termes.append(calcul)
                exo.append(" ; ".join(calcul_termes) + ".")
            else:
                exo.append(ur"TODO")
            exo.append(ur'\begin{enumerate}')
            exo.append(ur' \item \emph{{ {} terme :}}'.format(FRANCAIS_ORDINAL[self.rang[0]]))
            enumeration = []
            for indice in range(question.indice0, self.rang[0]+1):
                enumeration.append(u"le {ordinal} terme est $u_{indice}$".format(ordinal=FRANCAIS_ORDINAL[indice], indice=indice))
            exo.append(" ; ".join(enumeration) + ".")
            exo.append(ur"Le terme demandé est donc \fbox{{$u_{}={}$}}.".format(self.rang[0], termes[self.rang[0]].latex()))
            exo.append(ur'\item Le terme de rang {indice} est \fbox{{$u_{indice}={valeur}$}}.'.format(indice=self.rang[1], valeur=termes[self.rang[1]].latex()))
            exo.append(ur'\item Nous avons calculé que \fbox{{$u_{indice}={valeur}$}}.'.format(indice=self.rang[2], valeur=termes[self.rang[2]].latex()))
            exo.append(ur'\end{enumerate}')
        exo.append(ur'\end{enumerate}')
        return exo
