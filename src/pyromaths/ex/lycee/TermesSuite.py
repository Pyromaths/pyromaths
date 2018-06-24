#!/usr/bin/env python3
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

from __future__ import division
from __future__ import unicode_literals
from builtins import str
from builtins import range
from builtins import object
import functools
import random
import textwrap

from pyromaths import ex
from pyromaths.outils.Arithmetique import pgcd

FRANCAIS_ORDINAL = {
    1: u"premier",
    2: u"deuxième",
    3: u"troisième",
    4: u"quatrième",
    5: u"cinquième",
    6: u"sixième",
    7: u"septième",
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
NOTATIONS = [
    "u",
    r"\left(u_n\right)",
    r"\left(u_n\right)_{n\in\mathbb{N}}",
    ]

def signe(nombre):
    if nombre > 0:
        return 1
    if nombre < 0:
        return -1
    raise ValueError

class Fraction(object):
    def __init__(self, numerateur, denominateur, signe=1):
        self.signe = signe
        self.numerateur = numerateur
        self.denominateur = denominateur

    def latex(self):
        if self.denominateur == 1:
            return str(self.numerateur)
        else:
            if self.signe == 1:
                signe = ""
            else:
                signe = "-"
            return r"{}\frac{{ {} }}{{ {} }}".format(
                    signe,
                    self.numerateur,
                    self.denominateur,
                    )

    def simplifie(self):
        if self.numerateur % self.denominateur == 0:
            return Entier(self.signe * self.numerateur / self.denominateur)
        diviseur = pgcd(self.numerateur, self.denominateur)
        return Fraction(
                self.numerateur // diviseur,
                self.denominateur // diviseur,
                self.signe,
                )

    def __float__(self):
        return float(self.signe * self.numerateur / self.denominateur)



@functools.total_ordering
class Entier(object):
    def __init__(self, valeur):
        self.valeur = valeur

    def __int__(self):
        return self.valeur

    def __neg__(self):
        return self.__class__(- self.valeur)

    def __lt__(self, other):
        if isinstance(other, int):
            return self.valeur < other
        elif isinstance(other, Entier):
            return self.valeur < other.valeur
        else:
            raise TypeError()

    def __eq__(self, other):
        if isinstance(other, int):
            return self.valeur == other

        elif isinstance(other, Entier):
            return self.valeur == other.valeur
        else:
            raise TypeError()

    def latex(self, signe="-"):
        if signe == "+":
            if self.valeur >= 0:
                return "+" + str(self.valeur)
            else:
                return "-" + str(abs(self.valeur))
        else:
            if self.valeur >= 0:
                return str(self.valeur)
            else:
                return "-" + str(abs(self.valeur))

    def __float__(self):
        return float(self.valeur)

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

class Fonction(object):

    def calcul(self, argument):
        raise NotImplementedError()

    def resultat(self, variable):
        raise NotImplementedError()

    def expression(self, variable):
        raise NotImplementedError()

class Lineaire(Fonction):

    def __init__(self):
        self.coeff = random.choice(FRACTIONS)

    def expression(self, variable):
        return r"{coeff}{variable}".format(
            coeff=self.coeff.latex(),
            variable=variable,
            )

    def calcul(self, argument):
        if isinstance(argument, Entier):
            if float(argument) < 0:
                arg = r"\left( {} \right)".format(argument.latex())
            else:
                arg = argument.latex()
            yield self.expression(r"\times " + arg)
            if isinstance(self.coeff.simplifie(), Fraction):
                yield Fraction(
                            self.coeff.numerateur * argument.valeur,
                            self.coeff.denominateur,
                            ).latex()
                if pgcd(self.coeff.numerateur * argument.valeur, self.coeff.denominateur) != 1:
                    yield self.resultat(argument).latex()
            else:
                yield self.resultat(argument).latex()
        else:
            yield self.expression(r"\times " + argument.latex())
            yield Fraction(
                self.coeff.numerateur * argument.numerateur,
                self.coeff.denominateur * argument.denominateur,
                ).latex()
            if pgcd(
                self.coeff.numerateur * argument.numerateur,
                self.coeff.denominateur * argument.denominateur,
                ) != 1:
                yield self.resultat(argument).latex()

    def resultat(self, variable):
        if isinstance(variable, Entier):
            variable = Fraction(variable.valeur, 1)
        return Fraction(
            self.coeff.numerateur * variable.numerateur,
            self.coeff.denominateur * variable.denominateur,
            ).simplifie()

class Affine(Fonction):

    def __init__(self):
        self.coeff = random.choice(FRACTIONS)
        ordonnee = random.randint(1, 10)
        if random.randint(1, 2) == 1:
            ordonnee = -ordonnee
        self.ordonnee = Entier(ordonnee)

    def expression(self, variable):
        return r"{coeff}{variable}{ordonnee}".format(
            coeff=self.coeff.latex(),
            ordonnee=self.ordonnee.latex("+"),
            variable=variable,
            )

    def calcul(self, argument):
        if float(argument) < 0:
            arg = r"\left( {} \right)".format(argument.latex())
        else:
            arg = argument.latex()
        yield self.expression(r"\times " + arg)
        if isinstance(argument, Entier):
            if isinstance(self.coeff.simplifie(), Fraction):
                yield r"{fraction} {signe} \frac{{ {ordonnee} \times {denom} }}{{ {denom} }}".format(
                        fraction=Fraction(
                            self.coeff.numerateur * argument.valeur,
                            self.coeff.denominateur,
                            ).latex(),
                        ordonnee=abs(self.ordonnee.valeur),
                        denom=self.coeff.denominateur,
                        signe=Entier(self.coeff.denominateur * self.ordonnee.valeur).latex("+")[0],
                        )
                yield r"\frac{{ {gauche} {droite} }}{{ {denom} }}".format(
                        gauche=self.coeff.numerateur * argument.valeur,
                        droite=Entier(self.coeff.denominateur * self.ordonnee.valeur).latex("+"),
                        denom=self.coeff.denominateur,
                        )
        else:
            yield r"{} + \frac{{ {} \times {} }}{{ {} }}".format(
                Fraction(
                    self.coeff.numerateur * argument.numerateur,
                    self.coeff.denominateur * argument.denominateur,
                    ).latex(),
                self.ordonnee.valeur,
                self.coeff.denominateur * argument.denominateur,
                self.coeff.denominateur * argument.denominateur,
                )
            yield r"\frac{{ {} {} }}{{ {} }}".format(
                self.coeff.numerateur * argument.numerateur,
                Entier(self.ordonnee.valeur * self.coeff.denominateur * argument.denominateur).latex("+"),
                self.coeff.denominateur * argument.denominateur,
                )
        yield self.resultat(argument).latex()

    def resultat(self, variable):
        if isinstance(variable, Entier):
            variable = Fraction(variable.valeur, 1)
        return Fraction(
            self.coeff.numerateur * variable.numerateur + self.ordonnee.valeur * self.coeff.denominateur * variable.denominateur,
            self.coeff.denominateur * variable.denominateur,
            ).simplifie()

class FractionProduit(Fonction):

    def __init__(self):
        self.numerateur = Entier(random.randint(2, 10))
        self.denominateur = Entier(random.randint(2, 10))

    def expression(self, variable):
        return r"\frac{{ {numerateur}^{variable} }}{{ {denominateur}{variable} }}".format(
                numerateur=self.numerateur.latex("-"),
                denominateur=self.denominateur.latex("-"),
                variable=variable,
            )

    def calcul(self, argument):
        if argument.valeur < 0:
            arg2 = r"\left( {} \right)".format(argument.latex())
        else:
            arg2 = argument.latex()
        yield r"\frac{{ {numerateur}^{{ {argument} }}}}{{ {denominateur}\times{arg2} }}".format(
                numerateur=self.numerateur.latex(),
                denominateur=self.denominateur.latex(),
                argument=argument.latex(),
                arg2=arg2,
            )
        yield r"\frac{{ {} }}{{ {} }}".format(
                self.numerateur.valeur ** argument.valeur,
                self.denominateur.valeur * argument.valeur,
                )
        if pgcd(
                self.numerateur.valeur ** argument.valeur,
                self.denominateur.valeur * argument.valeur,
                ) != 1:
            yield self.resultat(argument).latex()

    def resultat(self, argument):
        return Fraction(
                self.numerateur.valeur ** argument.valeur,
                self.denominateur.valeur * argument.valeur,
                ).simplifie()

class Trinome(Fonction):

    def __init__(self):
        coef = [0]*3
        for i in [0, 1, 2]:
            coef[i] = random.randint(2, 5)
            if random.randint(0,1) == 0:
                coef[i] = -coef[i]
        self.coef = [Entier(i) for i in coef]

    def expression(self, variable):
        return r"{coef[2]}{variable}^2{coef[1]}{variable}{coef[0]}".format(
            coef=[self.coef[0].latex("+"), self.coef[1].latex("+"), self.coef[2].latex("-")],
            variable=variable,
            )

    def calcul(self, argument):
        if argument < 0:
            texargument = r"\left{{ {variable} }}".format(argument.latex())
        else:
            texargument = argument.latex()
        yield r"{coef[2]}\times{argument}^2{coef[1]}\times{argument}{coef[0]}".format(
            coef=[self.coef[0].latex("+"), self.coef[1].latex("+"), self.coef[2].latex("-")],
            argument=texargument,
            )
        yield r"{}{}{}".format(
            Entier(self.coef[2].valeur * argument.valeur**2).latex(),
            Entier(self.coef[1].valeur * argument.valeur).latex("+"),
            Entier(self.coef[0].valeur).latex("+")
            )
        yield Entier(
            (self.coef[2].valeur * argument.valeur**2) +
            (self.coef[1].valeur * argument.valeur) +
            (self.coef[0].valeur)
            ).latex()

    def resultat(self, argument):
        return Entier(self.coef[2].valeur * argument.valeur**2 + self.coef[1].valeur * argument.valeur + self.coef[0].valeur)


class IdentiteTranslatee(Fonction):

    def __init__(self):
        ordonnee = random.randint(1, 10)
        if random.randint(1, 2) == 1:
            ordonnee = -ordonnee
        self.ordonnee = Entier(ordonnee)

    def expression(self, variable):
        return r"{variable}{ordonnee}".format(
            variable=variable,
            ordonnee=self.ordonnee.latex("+"),
            )

    def calcul(self, argument):
        yield self.expression(argument.latex())
        yield self.resultat(argument).latex()

    def resultat(self, variable):
        return Entier(variable.valeur + self.ordonnee.valeur)

class FrancaisGeometrique(Fonction):

    def __init__(self):
        if random.randint(1, 2) == 1:
            self.raison = Fraction(1, random.randint(2, 10))
        else:
            self.raison = Entier(random.randint(2, 10))

    @property
    def francais(self):
        if isinstance(self.raison, Fraction):
            return u"{} précédent".format(FRANCAIS_INVERSE[self.raison.denominateur])
        else:
            return u"{} précédent".format(FRANCAIS_MULTIPLE[self.raison.valeur])

    def expression(self, variable):
        # L'argument est du code LaTeX
        return r"{} {}".format(self.raison.latex(), variable)

    def calcul(self, argument):
        yield r"{} \times {}".format(self.raison.latex(), argument.latex())
        resultat = self.resultat(argument).latex()
        if isinstance(resultat, Entier):
            yield self.resultat(argument).latex()
        else:
            if isinstance(argument, Entier):
                argument = Fraction(argument.valeur, 1)
            raison = self.raison
            if isinstance(raison, Entier):
                raison = Fraction(raison.valeur, 1)
            numerateur = argument.numerateur * raison.numerateur
            denominateur = raison.denominateur * argument.denominateur
            yield r"\frac{{ {} }}{{ {} }}".format(numerateur, denominateur)
            if numerateur % denominateur == 0:
                yield Entier(numerateur //  denominateur).latex()
                return

            diviseur = pgcd(numerateur, denominateur)
            if diviseur == 1:
                return

            yield Fraction(numerateur // diviseur, denominateur // diviseur).latex()

    def resultat(self, argument):
        if isinstance(argument, Entier) and isinstance(self.raison, Entier):
            return Entier(argument.valeur * self.raison.valeur)
        else:
            if isinstance(argument, Entier):
                argument = Fraction(argument.valeur, 1)
            if isinstance(self.raison, Entier):
                raison = Fraction(self.raison.valeur, 1)
            else:
                raison = self.raison
            numerateur = argument.numerateur * raison.numerateur
            denominateur = raison.denominateur * argument.denominateur
            if numerateur % denominateur == 0:
                return Entier(numerateur //  denominateur)
            diviseur = pgcd(numerateur, denominateur)
            return Fraction(numerateur // diviseur, denominateur // diviseur)

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

    def expression(self, variable):
        # L'argument est du code LaTeX
        return r"{} {}".format(variable, Entier(self.raison).latex("+"))

    def calcul(self, argument):
        yield self.expression(argument.latex())
        yield self.resultat(argument).latex()

    def resultat(self, argument):
        return Entier(argument.valeur + self.raison)

class FrancaisOppose(Fonction):

    @property
    def francais(self):
        return u"à l'opposé du précédent"

    def expression(self, variable):
        # L'argument est du code LaTeX
        if variable.startswith("-"):
            return r"-\left({}\right)".format(variable)
        else:
            return r"-{}".format(variable)

    def calcul(self, argument):
        yield Entier(-argument.valeur).latex("-")

    def resultat(self, argument):
        if not isinstance(argument, Entier):
            raise TypeError("Argument must be an instance of `Entier`.")
        return - argument

class FrancaisInverse(Fonction):

    @property
    def francais(self):
        return u"à l'inverse du précédent"

    def expression(self, variable):
        # L'argument est du code LaTeX
        return r"\frac{{1}}{{ {} }}".format(variable)

    def calcul(self, argument):
        yield self.expression(argument.latex())
        if isinstance(argument, Entier) and argument > 0:
            pass
        elif isinstance(argument, Entier) and argument < 0:
            yield r"-{}".format(self.expression((-argument).latex()))
        elif isinstance(argument, Fraction):
            yield self.resultat(argument).latex()
        else:
            raise TypeError("Argument must be an instance of `Entier` or `Fraction`.")

    def resultat(self, argument):
        if isinstance(argument, Fraction):
            if argument.numerateur == 1:
                return Entier(argument.denominateur * argument.signe)
            else:
                return Fraction(
                    abs(argument.denominateur),
                    abs(argument.numerateur),
                    signe(argument.numerateur * argument.denominateur),
                    )
        elif isinstance(argument, Entier):
            return Fraction(1, abs(argument.valeur), signe(argument.valeur))
        raise TypeError("Argument must be an instance of `Entier` or `Fraction`.")


class Question(object):

    def __init__(self, indice0):
        self.indice0 = indice0
        if self.indice0 == 0:
            self.notation = NOTATIONS[random.randint(0, 2)]
        else:
            self.notation = NOTATIONS[random.randint(0, 1)]

class Francais(Question):

    def __init__(self, indice0):
        super(Francais, self).__init__(indice0)
        self.terme0 = Entier(random.randint(-10, 10))
        self.fonction = random.choice([
            FrancaisGeometrique,
            FrancaisArithmetique,
            FrancaisOppose,
            FrancaisInverse,
            ])()

    @property
    def latex_params(self):
        return {
            'indice0': self.indice0,
            'terme0': self.terme0.latex("-"),
            'suivant': self.fonction.francais,
            'notation': self.notation,
            }

class General(Question):

    def __init__(self, indice0):
        super(General, self).__init__(indice0)
        self.fonction = random.choice([
            FractionProduit,
            Trinome,
            Affine,
            Lineaire,
            IdentiteTranslatee,
            ])()

    @property
    def latex_params(self):
        return {
            'indice0': self.indice0,
            'fonction': self.fonction.expression(r"n"),
            'notation': self.notation,
            }

class Recursif(Question):

    def __init__(self, indice0):
        super(Recursif, self).__init__(indice0)
        self.terme0 = Entier(random.randint(-10, 10))
        self.fonction = random.choice([
            Affine,
            IdentiteTranslatee,
            Lineaire,
            ])()

    @property
    def latex_params(self):
        return {
            'indice0': self.indice0,
            'terme0': self.terme0.latex("-"),
            'fonction': self.fonction.expression(r"u_n"),
            'notation': self.notation,
            }

class TermesDUneSuite(ex.TexExercise):

    description = u"Termes d'une suite"
    level = "1.1reS"

    def __init__(self):
        # * `self.rang[0]` désigne l'ordinal du premier terme demandé (pour la
        #   première question de chacune des trois suites) ;
        # * `self.rang[1]` et `self.rang[2]` sont les rangs demandés pour les
        #   deux questions suivantes dans chacune des trois suites.
        self.rang = [random.randint(2, 7)] + random.sample(list(range(3, 7)), 2)

        self.questions = [
                Francais(random.randint(0, min(self.rang[1:])-1)),
                General(random.randint(0, min(self.rang[1:])-1)),
                Recursif(random.randint(0, min(self.rang[1:])-1)),
                ]

    def tex_statement(self):
        exo = [r'\exercice']
        exo.append(r'Pour chacune des suites $u$ suivantes, calculer :')
        exo.append(r' (a) le {} terme ;'.format(FRANCAIS_ORDINAL[self.rang[0]]))
        exo.append(r' (b) le terme de rang {} ;'.format(self.rang[1]))
        exo.append(r' (c) $u_{}$.'.format(self.rang[2]))

        exo.append(r'\begin{enumerate}')
        exo.append(r'  \item ${notation}$ est une suite de premier terme $u_{indice0}={terme0}$, et dont chaque terme (sauf le premier) est égal {suivant}.'.format(**self.questions[0].latex_params))
        exo.append(r'  \item ${notation}$ est la suite définie pour $n\geq{indice0}$ par : $u_n={fonction}$.'.format(**self.questions[1].latex_params))
        exo.append(textwrap.dedent(r"""
            \item ${notation}$ est la suite définie pour $n\geq{indice0}$ par :
                \[\left\{{\begin{{array}}{{l}}
                  u_{indice0}={terme0}\\
                  \text{{Pour tout $n\geq{indice0}$ : }} u_{{n+1}}={fonction}.
              \end{{array}}\right.\]
              """).format(**self.questions[2].latex_params))
        exo.append(r'\end{enumerate}')
        return exo

    def tex_answer(self):
        exo = [r'\exercice*']
        exo.append(r'\begin{enumerate}')
        # Question 0
        exo.append(r"  \item Selon l'énoncé, le premier terme de ${notation}$ est $u_{indice0}={terme0}$. Puisque chaque terme (sauf le premier) est égal {suivant}, on a :".format(**self.questions[0].latex_params))
        termes = dict([(self.questions[0].indice0, self.questions[0].terme0)])
        calcul_termes = []
        for indice in range(self.questions[0].indice0, max(self.rang[0] + self.questions[0].indice0 - 1, self.rang[1], self.rang[2])):
            calcul = r"$u_{indice}={fonction}".format(
                indice=indice+1,
                fonction=self.questions[0].fonction.expression("u_{}".format(indice)),
                )
            for etape in self.questions[0].fonction.calcul(termes[indice]):
                calcul += " =" + etape
            calcul += "$"
            termes[indice+1] = self.questions[0].fonction.resultat(termes[indice])
            calcul_termes.append(calcul)
        exo.append(" ; ".join(calcul_termes) + ".")
        exo.append(r'\begin{enumerate}')
        exo.append(r' \item Calcul du {} terme :'.format(FRANCAIS_ORDINAL[self.rang[0]]))
        enumeration = []
        for indice in range(0, self.rang[0]):
            enumeration.append(u"le {ordinal} terme est $u_{indice}$".format(ordinal=FRANCAIS_ORDINAL[indice+1], indice=self.questions[0].indice0+indice))
        exo.append(" ; ".join(enumeration) + ".")
        exo.append(r"Le terme demandé est donc : $u_{}={}$.".format(self.rang[0] + self.questions[0].indice0 - 1, termes[self.rang[0] + self.questions[0].indice0 - 1].latex()))
        exo.append(r'\item Le terme de rang {indice} est : $u_{indice}={valeur}$.'.format(indice=self.rang[1], valeur=termes[self.rang[1]].latex()))
        exo.append(r'\item Nous avons calculé que : $u_{indice}={valeur}$.'.format(indice=self.rang[2], valeur=termes[self.rang[2]].latex()))
        exo.append(r'\end{enumerate}')

        # Question 1
        exo.append(r'  \item La suite ${notation}$ est définie pour $n\geq{indice0}$ par : $u_n={fonction}$.'.format(**self.questions[1].latex_params))
        exo.append(r"Elle est donc définie par son terme général : pour calculer un terme de rang $n$, on peut calculer directement l'image de $n$ par la suite.")
        exo.append(r'\begin{enumerate}')
        exo.append(r' \item Calcul du {} terme :'.format(FRANCAIS_ORDINAL[self.rang[0]]))
        enumeration = []
        for indice in range(0, self.rang[0]):
            enumeration.append(u"le {ordinal} terme est $u_{indice}$".format(ordinal=FRANCAIS_ORDINAL[indice+1], indice=self.questions[1].indice0+indice))
        exo.append(" ; ".join(enumeration) + ".")
        exo.append(r"Le terme demandé est donc : $u_{}=".format(self.rang[0] + self.questions[1].indice0 - 1))
        calcul = []
        for etape in self.questions[1].fonction.calcul(Entier(self.rang[0] + self.questions[1].indice0 - 1)):
            calcul.append(etape)
        exo.append(u" = ".join(calcul) + r"$.")
        exo.append(r"La solution est $u_{{ {} }}={}$.".format(self.rang[0] + self.questions[1].indice0 - 1, self.questions[1].fonction.resultat(Entier(self.rang[0] + self.questions[1].indice0 - 1)).latex()))
        exo.append(r"\item Le terme de rang {rang} est $u_{{ {rang} }}$.".format(rang=self.rang[1]))
        if self.rang[0] + self.questions[1].indice0 - 1 == self.rang[1]:
            exo.append(r"Ce terme a déjà été calculé, et $u_{{ {} }}={}$.".format(self.rang[1], self.questions[1].fonction.resultat(Entier(self.rang[1])).latex()))
        else:
            calcul = []
            for etape in self.questions[1].fonction.calcul(Entier(self.rang[1])):
                calcul.append(etape)
            exo.append(r"Le terme demandé est donc : $u_{{ {} }}=".format(self.rang[1]) + " = ".join(calcul) + r"$.")
            exo.append(r"La solution est donc  : $u_{{ {} }}={}$.".format(self.rang[1], self.questions[1].fonction.resultat(Entier(self.rang[1])).latex()))
        exo.append(r"\item")
        if self.rang[0] + self.questions[1].indice0 - 1 == self.rang[2]:
            exo.append(r"Ce terme a déjà été calculé, et $u_{{ {} }}={}$.".format(self.rang[2], self.questions[1].fonction.resultat(Entier(self.rang[2])).latex()))
        else:
            calcul = []
            for etape in self.questions[1].fonction.calcul(Entier(self.rang[2])):
                calcul.append(etape)
            exo.append(r"On a : $u_{{ {} }}=".format(self.rang[2]) + " = ".join(calcul) + r"$.")
            exo.append(r"La solution est donc  : $u_{{ {} }}={}$.".format(self.rang[2], self.questions[1].fonction.resultat(Entier(self.rang[2])).latex()))
        exo.append(r'\end{enumerate}')

        # Question 2
        exo.append(textwrap.dedent(r"""
            \item La suite ${notation}$ est définie par récurrence, pour $n\geq{indice0}$, par :
                \[\left\{{\begin{{array}}{{l}}
                  u_{indice0}={terme0}\\
                  \text{{Pour tout $n\geq{indice0}$ : }} u_{{n+1}}={fonction}.
              \end{{array}}\right.\]
              """).format(**self.questions[2].latex_params))
        termes = dict([(self.questions[2].indice0, self.questions[2].terme0)])
        calcul_termes = []
        for indice in range(self.questions[2].indice0, max(self.rang[0] + self.questions[2].indice0 - 1, self.rang[1], self.rang[2])):
            calcul = r"u_{indice} &= {fonction}".format(
                indice=indice+1,
                fonction=self.questions[2].fonction.expression("u_{}".format(indice)),
                )
            for etape in self.questions[2].fonction.calcul(termes[indice]):
                calcul += " =" + etape
            termes[indice+1] = self.questions[2].fonction.resultat(termes[indice])
            calcul_termes.append(calcul)
        exo.append(r"\begin{align*}")
        exo.append(r" \\".join(calcul_termes))
        exo.append(r"\end{align*}")
        exo.append(r'\begin{enumerate}')
        exo.append(r' \item Calcul du {} terme :'.format(FRANCAIS_ORDINAL[self.rang[0]]))
        enumeration = []
        for indice in range(0, self.rang[0]):
            enumeration.append(u"le {ordinal} terme est $u_{indice}$".format(ordinal=FRANCAIS_ORDINAL[indice+1], indice=self.questions[2].indice0+indice))
        exo.append(" ; ".join(enumeration) + ".")
        exo.append(r"Le terme demandé est donc : $u_{}={}$.".format(self.rang[0] + self.questions[2].indice0 - 1, termes[self.rang[0] + self.questions[2].indice0 - 1].latex()))
        exo.append(r'\item Le terme de rang {indice} est : $u_{indice}={valeur}$.'.format(indice=self.rang[1], valeur=termes[self.rang[1]].latex()))
        exo.append(r'\item Nous avons calculé que : $u_{indice}={valeur}$.'.format(indice=self.rang[2], valeur=termes[self.rang[2]].latex()))
        exo.append(r'\end{enumerate}')

        exo.append(r'\end{enumerate}')
        return exo
