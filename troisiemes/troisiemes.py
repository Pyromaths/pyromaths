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

import random
import string
import pythagore
import equations
import racines
import systemes
import puissances
import developpements
from fractions import tex_somme_prod, tex_prod_parenth, \
    tex_quotient_frac, valeurs_somme_prod, valeurs_prod_parenth, \
    valeurs_quotient_frac, tex_frac
from pgcd import valeurs_pgcd, tex_trouve_diviseur, algo_euclide, \
    tex_algo_euclide, tex_simplifie_fraction_pgcd, \
    simplifie_fraction_pgcd
from outils import ecrit_tex, tex_entete
from pyro_classes import WriteFiles

def tex_fractions(f0, f1):
    nb_exos = 3
    tex_exos = (tex_somme_prod, tex_prod_parenth, tex_quotient_frac)
    valeurs_exos = (valeurs_somme_prod, valeurs_prod_parenth,
                    valeurs_quotient_frac)
    ordre_exos = [i for i in xrange(nb_exos)]
    f0.write('''\\exercice
  \\stepcounter{nocalcul}%
''')
    f0.write("  Calculer les expressions suivantes et donner le r\xe9sultat sous la forme d'une fraction irr\xe9ductible.\n")
    f0.write('  \\begin{multicols}{3}\\noindent\n')
    f1.write('''\\exercice*
  \\stepcounter{nocalcul}
''')
    f1.write("  Calculer les expressions suivantes et donner le r\xe9sultat sous la forme d'une fraction irr\xe9ductible.\n")
    f1.write('  \\begin{multicols}{3}\\noindent\n')
    for i in xrange(nb_exos):
        a = random.randrange(nb_exos - i)
        tex_exos[ordre_exos[a]](valeurs_exos[ordre_exos.pop(a)](), f0,
                                f1)
        if i < nb_exos - 1:
            f0.write('    \\columnbreak\\stepcounter{nocalcul}\n')
            f1.write('    \\columnbreak\\stepcounter{nocalcul}\n')
        else:
            f0.write('  \\end{multicols}\n')
            f1.write('  \\end{multicols}\n')


def tex_puissances(f0, f1):
    from math import floor, log10
    sd = string.maketrans('.', ',')  # convertit les . en , (separateur decimal)
    valeurs = puissances.valeurs_puissances()
    i = random.randrange(2)
    f0.write('''\\exercice
  \\stepcounter{nocalcul}%
''')
    f0.write("  Calculer les expressions suivantes et donner l'\xe9criture scientifique du r\xe9sultat.\n")
    f0.write('  \\begin{multicols}{2}\\noindent\n')
    f1.write('''\\exercice*
  \\stepcounter{nocalcul}%
''')
    f1.write("  Calculer les expressions suivantes et donner l'\xe9criture scientifique du r\xe9sultat.\n")
    f1.write('  \\begin{multicols}{2}\\noindent\n')
    ecrit_tex(f0, puissances.tex_puissances_0(valeurs[i]).translate(sd),
              tabs=2)
    ecrit_tex(f1, puissances.tex_puissances_0(valeurs[i]).translate(sd),
              tabs=2)
    ecrit_tex(f1, puissances.tex_puissances_1(valeurs[i]).translate(sd),
              tabs=2)
    ecrit_tex(f1, puissances.tex_puissances_2(valeurs[i]).translate(sd),
              tabs=2)
    if int(floor(log10(((valeurs[i][0] * valeurs[i][1]) * 1.) / valeurs[i][2]))) != \
        0:
        ecrit_tex(f1, puissances.tex_puissances_3(valeurs[i]).translate(sd),
                  tabs=2)
    ecrit_tex(f1, puissances.tex_puissances_4(valeurs[i]).translate(sd),
              cadre=True, tabs=2)
    f0.write('    \\columnbreak\\stepcounter{nocalcul}%\n')
    f1.write('    \\columnbreak\\stepcounter{nocalcul}%\n')
    ecrit_tex(f0, puissances.tex_puissances_0(valeurs[1 - i]).translate(sd),
              tabs=2)
    ecrit_tex(f1, puissances.tex_puissances_0(valeurs[1 - i]).translate(sd),
              tabs=2)
    ecrit_tex(f1, puissances.tex_puissances_1(valeurs[1 - i]).translate(sd),
              tabs=2)
    ecrit_tex(f1, puissances.tex_puissances_2(valeurs[1 - i]).translate(sd),
              tabs=2)
    if int(floor(log10(((valeurs[1 - i][0] * valeurs[1 - i][1]) * 1.) /
           valeurs[1 - i][2]))) != 0:
        ecrit_tex(f1, puissances.tex_puissances_3(valeurs[1 - i]).translate(sd),
                  tabs=2)
    ecrit_tex(f1, puissances.tex_puissances_4(valeurs[1 - i]).translate(sd),
              cadre=True, tabs=2)
    f0.write('  \\end{multicols}\n')
    f1.write('  \\end{multicols}\n')


def tex_pgcd(f0, f1):
    nombres = valeurs_pgcd()
    f0.write('\\exercice\n')
    f0.write('''  \\begin{enumerate}
  \\item Les nombres \\nombre{%s} et \\nombre{%s} sont-ils premiers entre eux ?
''' %
             nombres)
    f0.write('  \\item Calculer le plus grand commun diviseur (\\textsc{pgcd}) de \\nombre{%s} et \\nombre{%s}.\n' %
             nombres)
    f0.write('  \\item Simplifier la fraction $\\cfrac{\\nombre{%s}}{\\nombre{%s}}$ pour la rendre irr\xe9ductible en indiquant la m\xe9thode.\n' %
             nombres)
    f0.write('  \\end{enumerate}\n')
    f1.write('\\exercice*\n')
    f1.write('''  \\begin{enumerate}
  \\item Les nombres \\nombre{%s} et \\nombre{%s} sont-ils premiers entre eux ?\\par
''' %
             nombres)
    f1.write(tex_trouve_diviseur(nombres) + '\n')
    f1.write('  \\item Calculer le plus grand commun diviseur (\\textsc{pgcd}) de \\nombre{%s} et \\nombre{%s}.\\par\n' %
             nombres)
    f1.write('    On calcule le \\textsc{pgcd} des nombres \\nombre{%s} et \\nombre{%s} en utilisant l\'algorithme d\'Euclide.\n' %
             nombres)
    l = algo_euclide(nombres)
    tex_liste = tex_algo_euclide(l)
    for i in xrange(len(l)):
        ecrit_tex(f1, '%s' % tex_liste[i], thenocalcul='', tabs=2)
    f1.write('    ' + tex_liste[len(l)])
    f1.write('  \\item Simplifier la fraction $\\cfrac{\\nombre{%s}}{\\nombre{%s}}$ pour la rendre irr\xe9ductible en indiquant la m\xe9thode.\n' %
             nombres)
    f1.write(tex_simplifie_fraction_pgcd(simplifie_fraction_pgcd(l)) +
             '\n')
    f1.write('  \\end{enumerate}\n')


def tex_developpements(f0, f1):
    nb_exos = 4
    liste_exos = (developpements.valeurs_apb2, developpements.valeurs_amb2,
                  developpements.valeurs_apbamb, developpements.valeurs_distr)
    exo = []
    ordre_exos = [i for i in xrange(nb_exos)]
    for i in xrange(nb_exos):
        a = random.randrange(nb_exos - i)
        exo.append(liste_exos[ordre_exos.pop(a)](10))
    f0.write('''\\exercice
  \\stepcounter{nocalcul}%
''')
    f0.write('  D\xe9velopper et r\xe9duire les expressions suivantes.\n')
    f0.write('  \\begin{multicols}{2}\\noindent\n')
    f1.write('''\\exercice*
  \\stepcounter{nocalcul}%
''')
    f1.write('  D\xe9velopper et r\xe9duire les expressions suivantes.\n')
    f1.write('  \\begin{multicols}{2}\\noindent\n')
    developpements.tex_developpe1(exo[0], f0, f1)
    f0.write('    \\stepcounter{nocalcul}%\n')
    f1.write('    \\stepcounter{nocalcul}%\n')
    developpements.tex_developpe1(exo[1], f0, f1)
    f0.write('    \\stepcounter{nocalcul}%\n')
    f1.write('    \\columnbreak\\stepcounter{nocalcul}%\n')
    developpements.tex_developpe1(exo[2], f0, f1)
    f0.write('    \\stepcounter{nocalcul}%\n')
    f1.write('    \\stepcounter{nocalcul}%\n')
    developpements.tex_developpe1(exo[3], f0, f1)
    f1.write('  \\end{multicols}%\n')
    exo = []
    sig = [random.randrange(2) for i in xrange(4)]
    ordre_exos = [i for i in xrange(nb_exos)]
    for i in xrange(nb_exos):
        a = random.randrange(nb_exos - i)
        exo.append(liste_exos[ordre_exos.pop(a)](10))
    f0.write('    \\stepcounter{nocalcul}%\n')
    f1.write('  \\stepcounter{nocalcul}%\n')
    developpements.tex_developpe2(exo[0], sig[0], exo[1], sig[1], f1, f0)
    f0.write('    \\stepcounter{nocalcul}%\n')
    f1.write('  \\stepcounter{nocalcul}%\n')
    developpements.tex_developpe2(exo[2], sig[2], exo[3], sig[3], f1, f0)
    f0.write('  \\end{multicols}\n')


def tex_factorisations(f0, f1):
    (nb_exos, ordre_exos, ordre) = (6, [], [])
    for i in xrange(nb_exos):
        ordre.append(str(i))
    for i in xrange(nb_exos):
        ordre_exos.append(ordre.pop(random.randrange(nb_exos - i)))
    del ordre
    f0.write('''\\exercice
  \\stepcounter{nocalcul}%
''')
    f0.write('  Factoriser les expressions suivantes.\n')
    f0.write('  \\begin{multicols}{2}\\noindent\n')
    f1.write('''\\exercice*
  \\stepcounter{nocalcul}%
''')
    f1.write('  Factoriser les expressions suivantes.\n')
    f1.write('  \\begin{multicols}{2}\\noindent\n')
    for i in xrange(nb_exos):
        exec 'developpements.factorisation' + str(ordre_exos[i]) + \
            '(f1,f0)'
        f0.write('    \\stepcounter{nocalcul}%\n')
        f1.write('    \\stepcounter{nocalcul}%\n')
    f0.write('  \\end{multicols}\n')
    f1.write('  \\end{multicols}\n')


def tex_devfacteq(f0, f1):
    exo = [0, 1, 2, 3, 6][random.randrange(5)]
    expr = developpements.choix_exo(exo)
    valeurx = developpements.valeur_quotient()
    fact = developpements.fin_fact(expr)
    f0.write('''\\exercice
  \\stepcounter{nocalcul}
''')
    f0.write('  On donne $A=%s$\\,.\n' % developpements.tex_initial(exo,
             expr))
    f0.write('  \\begin{enumerate}\n')
    f0.write('  \\item D\xe9velopper et r\xe9duire $A$\\,.\n')
    f0.write('  \\item Factoriser $A$\\,.\n')
    f0.write('  \\item Calculer $A$ pour $x=%s$\\,.\n' % tex_frac(valeurx))
    f0.write("  \\item R\xe9soudre l'\xe9quation $A=0$\\,.\n")  # % developpements.tex_dev0(fact))
    f0.write('  \\end{enumerate}\n')
    f1.write('''\\exercice*
  \\stepcounter{nocalcul}
''')
    f1.write('  On donne $A=%s$\\,.\n' % developpements.tex_initial(exo,
             expr))
    f1.write('  \\begin{enumerate}\n')
    f1.write('  \\item D\xe9velopper et r\xe9duire $A$\\,.\n')
    developpements.developpements(expr, exo, f1)
    f1.write('  \\item Factoriser $A$\\,.\n')
    exec 'developpements.factorisation' + str(exo) + '(f1,valeurs=expr)'
    f1.write('  \\item Calculer $A$ pour $x=%s$\\,.\\par\n' % tex_frac(valeurx))
    developpements.tex_fractions(expr, valeurx, f1)
    f1.write("  \\item R\xe9soudre l'\xe9quation $A=0$\\,.\\par\n")  # % developpements.tex_dev0(fact))
    developpements.tex_equations(fact, f1)
    f1.write('  \\end{enumerate}\n')


def tex_equations(f0, f1):
    valeurs = equations.valeurs(10)
    f0.write('\\exercice\n')
    f1.write('\\exercice*\n')
    equations.equations(f0, f1, valeurs)


def tex_racines(f0, f1):
    f0.write('''\\exercice
  \\stepcounter{nocalcul}%
''')
    f0.write('  \\begin{enumerate}\n')
    f0.write('  \\item Calculer les expressions suivantes et donner le r\xe9sultat sous la forme $a\\,\\sqrt{b}$ avec $a$ et $b$ entiers, $b$ le plus petit possible.\n')
    f0.write('  \\begin{multicols}{2}\\noindent\n')
    f1.write('''\\exercice*
  \\stepcounter{nocalcul}%
''')
    f1.write('  \\begin{enumerate}\n')
    f1.write('  \\item Calculer les expressions suivantes et donner le r\xe9sultat sous la forme $a\\,\\sqrt{b}$ avec $a$ et $b$ entiers, $b$ le plus petit possible.\n')
    mymax = 5
    f1.write('    \\begin{multicols}{2}\\noindent\n')
    valeurs = racines.valeurs_aRb0(mymax)
    racines.exoaRb0(f0, f1, valeurs)
    f0.write('      \\columnbreak\\stepcounter{nocalcul}%\n')
    f1.write('      \\columnbreak\\stepcounter{nocalcul}%\n')
    valeurs = racines.valeurs_aRb1(mymax)
    racines.exoaRb1(f0, f1, valeurs)
    f0.write('    \\end{multicols}\\vspace{-3ex}\n')
    f1.write('    \\end{multicols}\n')
    f0.write('  \\item Calculer les expressions suivantes et donner le r\xe9sultat sous la forme $a+b\\,\\sqrt{c}$ avec $a$, $b$ et $c$ entiers.\n')
    f0.write('''    \\stepcounter{nocalcul}%
    \\begin{multicols}{2}\\noindent
''')
    f1.write('  \\item Calculer les expressions suivantes et donner le r\xe9sultat sous la forme $a+b\\,\\sqrt{c}$ avec $a$, $b$ et $c$ entiers.\n')
    f1.write('''    \\stepcounter{nocalcul}%
    \\begin{multicols}{2}\\noindent
''')
    valeurs = racines.valeurs_aPbRc(mymax)
    racines.exo_aPbRc(f0, f1, valeurs)
    f0.write('      \\columnbreak\\stepcounter{nocalcul}%\n')
    f1.write('      \\columnbreak\\stepcounter{nocalcul}%\n')
    valeurs = racines.valeurs_aPbRc(mymax)
    racines.exo_aPbRc(f0, f1, valeurs)
    f0.write('    \\end{multicols}\\vspace{-3ex}\n')
    f1.write('    \\end{multicols}\n')
    f0.write("  \\item Calculer les expressions suivantes et donner le r\xe9sultat sous la forme d'un nombre entier.\n")
    f0.write('''    \\stepcounter{nocalcul}%
    \\begin{multicols}{2}\\noindent
''')
    f1.write("  \\item Calculer les expressions suivantes et donner le r\xe9sultat sous la forme d'un nombre entier.\n")
    f1.write('''    \\stepcounter{nocalcul}%
    \\begin{multicols}{2}\\noindent
''')
    valeurs = racines.valeurs_entier0(mymax)
    racines.exo_entier0(f0, f1, valeurs)
    f0.write('      \\columnbreak\\stepcounter{nocalcul}%\n')
    f1.write('      \\columnbreak\\stepcounter{nocalcul}%\n')
    valeurs = racines.valeurs_entier1(mymax)
    racines.exo_entier1(f0, f1, valeurs)
    f0.write('    \\end{multicols}\\vspace{-3ex}\n')
    f0.write('  \\end{enumerate}\n')
    f1.write('    \\end{multicols}\n')
    f1.write('  \\end{enumerate}\n')


def tex_systemes(f0, f1):
    valeurs = systemes.choix_valeurs(10)
    f0.write('\\exercice\n')
    f1.write('\\exercice*\n')
    f0.write("  R\xe9soudre le syst\xe8me d'\xe9quations suivant :\n")
    f1.write("  R\xe9soudre le syst\xe8me d'\xe9quations suivant :\n")
    systemes.systemes(f0, f1, valeurs)


def tex_pythagore(f0, f1):
    while True:
        longueurs = (pythagore.couples_pythagore)[random.randrange(120)]
        longueurs = [longueurs[i] / 10.0 for i in xrange(3)]
        if pythagore.inegalite_triangulaire(longueurs):
            break
    noms = pythagore.noms_sommets(3)
    angles = pythagore.fig_tr_rect(longueurs)
    f0.write('\\exercice\n')
    f1.write('\\exercice*\n')
    pythagore.tex_pythagore(f0, f1, noms, angles, longueurs)


def tex_reciproque_pythagore(f0, f1):
    while True:
        longueurs = (pythagore.couples_pythagore)[random.randrange(120)]
        longueurs = [longueurs[i] / 10.0 for i in xrange(3)]
        if pythagore.inegalite_triangulaire(longueurs):
            break
    noms = pythagore.noms_sommets(3)
    f0.write('''\\exercice
  \\stepcounter{nocalcul}%
''')
    f1.write('''\\exercice*
  \\stepcounter{nocalcul}%
''')
    pythagore.tex_reciproque_pythagore(f0, f1, noms, longueurs)


def tex_triangle_cercle(f0, f1):
    while True:
        longueurs = (pythagore.couples_pythagore)[random.randrange(120)]
        longueurs = [longueurs[i] / 10.0 for i in xrange(3)]
        if pythagore.inegalite_triangulaire(longueurs):
            break
    noms = pythagore.noms_sommets(3)
    angles = pythagore.fig_tr_rect(longueurs)
    f0.write('\\exercice\n')
    f1.write('\\exercice*\n')
    pythagore.tex_triangle_cercle(f0, f1, noms, angles, longueurs)


def tex_thales(f0, f1):
    f0.write('\\exercice\n')
    f1.write('\\exercice*\n')
    pythagore.thales(f0, f1)


def tex_reciproque_thales(f0, f1):
    f0.write('\\exercice\n')
    f1.write('\\exercice*\n')
    pythagore.rec_thales(f0, f1)


def tex_trigo(f0, f1):
    f0.write('\\exercice\n')
    f1.write('\\exercice*\n')
    pythagore.trigo_init(f0, f1)


def main(exo, files):
    modules = (
        tex_fractions,
        tex_puissances,
        tex_pgcd,
        tex_developpements,
        tex_factorisations,
        tex_devfacteq,
        tex_equations,
        tex_racines,
        tex_systemes,
        tex_pythagore,
        tex_reciproque_pythagore,
        tex_triangle_cercle,
        tex_thales,
        tex_reciproque_thales,
        tex_trigo,
        )

    modules[exo](files.f0, files.f1)
