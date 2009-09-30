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

#import random
#import string
##import pythagore
#from . import equations
#from . import racines
#from . import systemes
#from . import affine
#from . import proba
#
#from outils import ecrit_tex, tex_entete
import random, math
import outils
import troisiemes.fractions, troisiemes.puissances, troisiemes.pgcd
import troisiemes.developpements, troisiemes.equations, troisiemes.racines
import troisiemes.systemes, troisiemes.proba, troisiemes.affine
import troisiemes.pythagore

def tex_fractions(f0, f1):
    nb_exos = 3
    tex_exos = (troisiemes.fractions.tex_somme_prod,
                troisiemes.fractions.tex_prod_parenth,
                troisiemes.fractions.tex_quotient_frac)
    valeurs_exos = (troisiemes.fractions.valeurs_somme_prod,
                    troisiemes.fractions.valeurs_prod_parenth,
                    troisiemes.fractions.valeurs_quotient_frac)
    ordre_exos = [i for i in range(nb_exos)]
    f0.write('''\\exercice
''')
    f0.write("  Calculer les expressions suivantes et donner le résultat sous la forme d'une fraction irréductible.\n")
    f0.write('  \\begin{multicols}{3}\\noindent\n')
    f1.write('''\\exercice*
''')
    f1.write("  Calculer les expressions suivantes et donner le résultat sous la forme d'une fraction irréductible.\n")
    f1.write('  \\begin{multicols}{3}\\noindent\n')
    for i in range(nb_exos):
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
    sd = str.maketrans('.', ',')  # convertit les . en , (separateur decimal)
    valeurs = troisiemes.puissances.valeurs_puissances()
    i = random.randrange(2)
    f0.write('''\\exercice
''')
    f0.write("  Calculer les expressions suivantes et donner l'écriture scientifique du résultat.\n")
    f0.write('  \\begin{multicols}{2}\\noindent\n')
    f1.write('''\\exercice*
''')
    f1.write("  Calculer les expressions suivantes et donner l'écriture scientifique du résultat.\n")
    f1.write('  \\begin{multicols}{2}\\noindent\n')
    outils.ecrit_tex(f0, troisiemes.puissances.tex_puissances_0(valeurs[i]).translate(sd),
              tabs=2)
    outils.ecrit_tex(f1, troisiemes.puissances.tex_puissances_0(valeurs[i]).translate(sd),
              tabs=2)
    outils.ecrit_tex(f1, troisiemes.puissances.tex_puissances_1(valeurs[i]).translate(sd),
              tabs=2)
    outils.ecrit_tex(f1, troisiemes.puissances.tex_puissances_2(valeurs[i]).translate(sd),
              tabs=2)
    if int(math.floor(math.log10(((valeurs[i][0] * valeurs[i][1]) * 1.) / valeurs[i][2]))) != \
        0:
        outils.ecrit_tex(f1, troisiemes.puissances.tex_puissances_3(valeurs[i]).translate(sd),
                  tabs=2)
    outils.ecrit_tex(f1, troisiemes.puissances.tex_puissances_4(valeurs[i]).translate(sd),
              cadre=True, tabs=2)
    f0.write('    \\columnbreak\\stepcounter{nocalcul}%\n')
    f1.write('    \\columnbreak\\stepcounter{nocalcul}%\n')
    outils.ecrit_tex(f0, troisiemes.puissances.tex_puissances_0(valeurs[1 - i]).translate(sd),
              tabs=2)
    outils.ecrit_tex(f1, troisiemes.puissances.tex_puissances_0(valeurs[1 - i]).translate(sd),
              tabs=2)
    outils.ecrit_tex(f1, troisiemes.puissances.tex_puissances_1(valeurs[1 - i]).translate(sd),
              tabs=2)
    outils.ecrit_tex(f1, troisiemes.puissances.tex_puissances_2(valeurs[1 - i]).translate(sd),
              tabs=2)
    if int(math.floor(math.log10(((valeurs[1 - i][0] * valeurs[1 - i][1]) * 1.) /
           valeurs[1 - i][2]))) != 0:
        outils.ecrit_tex(f1, troisiemes.puissances.tex_puissances_3(valeurs[1 - i]).translate(sd),
                  tabs=2)
    outils.ecrit_tex(f1, troisiemes.puissances.tex_puissances_4(valeurs[1 - i]).translate(sd),
              cadre=True, tabs=2)
    f0.write('  \\end{multicols}\n')
    f1.write('  \\end{multicols}\n')


def tex_pgcd(f0, f1):
    nombres = troisiemes.pgcd.valeurs_pgcd()
    f0.write('\\exercice\n')
    f0.write('''  \\begin{enumerate}
  \\item Les nombres \\nombre{%s} et \\nombre{%s} sont-ils premiers entre eux ?
''' %
             nombres)
    f0.write('  \\item Calculer le plus grand commun diviseur (\\textsc{pgcd}) de \\nombre{%s} et \\nombre{%s}.\n' %
             nombres)
    f0.write('  \\item Simplifier la fraction $\\cfrac{\\nombre{%s}}{\\nombre{%s}}$ pour la rendre irréductible en indiquant la méthode.\n' %
             nombres)
    f0.write('  \\end{enumerate}\n')
    f1.write('\\exercice*\n')
    f1.write('''  \\begin{enumerate}
  \\item Les nombres \\nombre{%s} et \\nombre{%s} sont-ils premiers entre eux ?\\par
''' %
             nombres)
    f1.write(troisiemes.pgcd.tex_trouve_diviseur(nombres) + '\n')
    f1.write('  \\item Calculer le plus grand commun diviseur (\\textsc{pgcd}) de \\nombre{%s} et \\nombre{%s}.\\par\n' %
             nombres)
    f1.write('    On calcule le \\textsc{pgcd} des nombres \\nombre{%s} et \\nombre{%s} en utilisant l\'algorithme d\'Euclide.\n' %
             nombres)
    l = troisiemes.pgcd.algo_euclide(nombres)
    tex_liste = troisiemes.pgcd.tex_algo_euclide(l)
    for i in range(len(l)):
        outils.ecrit_tex(f1, '%s' % tex_liste[i], thenocalcul='', tabs=2)
    f1.write('    ' + tex_liste[len(l)])
    f1.write('  \\item Simplifier la fraction $\\cfrac{\\nombre{%s}}{\\nombre{%s}}$ pour la rendre irréductible en indiquant la méthode.\n' %
             nombres)
    f1.write(troisiemes.pgcd.tex_simplifie_fraction_pgcd(troisiemes.pgcd.simplifie_fraction_pgcd(l)) +
             '\n')
    f1.write('  \\end{enumerate}\n')


def tex_developpements(f0, f1):
    nb_exos = 4
    liste_exos = (troisiemes.developpements.valeurs_apb2,
                  troisiemes.developpements.valeurs_amb2,
                  troisiemes.developpements.valeurs_apbamb,
                  troisiemes.developpements.valeurs_distr)
    exo = []
    ordre_exos = [i for i in range(nb_exos)]
    for i in range(nb_exos):
        a = random.randrange(nb_exos - i)
        exo.append(liste_exos[ordre_exos.pop(a)](10))
    f0.write('''\\exercice
''')
    f0.write('  Développer et réduire les expressions suivantes.\n')
    f0.write('  \\begin{multicols}{2}\\noindent\n')
    f1.write('''\\exercice*
''')
    f1.write('  Développer et réduire les expressions suivantes.\n')
    f1.write('  \\begin{multicols}{2}\\noindent\n')
    troisiemes.developpements.tex_developpe1(exo[0], f0, f1)
    f0.write('    \\stepcounter{nocalcul}%\n')
    f1.write('    \\stepcounter{nocalcul}%\n')
    troisiemes.developpements.tex_developpe1(exo[1], f0, f1)
    f0.write('    \\stepcounter{nocalcul}%\n')
    f1.write('    \\columnbreak\\stepcounter{nocalcul}%\n')
    troisiemes.developpements.tex_developpe1(exo[2], f0, f1)
    f0.write('    \\stepcounter{nocalcul}%\n')
    f1.write('    \\stepcounter{nocalcul}%\n')
    troisiemes.developpements.tex_developpe1(exo[3], f0, f1)
    f1.write('  \\end{multicols}%\n')
    exo = []
    sig = [random.randrange(2) for i in range(4)]
    ordre_exos = [i for i in range(nb_exos)]
    for i in range(nb_exos):
        a = random.randrange(nb_exos - i)
        exo.append(liste_exos[ordre_exos.pop(a)](10))
    f0.write('    \\stepcounter{nocalcul}%\n')
    f1.write('  \\stepcounter{nocalcul}%\n')
    troisiemes.developpements.tex_developpe2(exo[0], sig[0], exo[1], sig[1], f1, f0)
    f0.write('    \\stepcounter{nocalcul}%\n')
    f1.write('  \\stepcounter{nocalcul}%\n')
    troisiemes.developpements.tex_developpe2(exo[2], sig[2], exo[3], sig[3], f1, f0)
    f0.write('  \\end{multicols}\n')


def tex_factorisations(f0, f1):
    (nb_exos, ordre_exos, ordre) = (6, [], [])
    for i in range(nb_exos):
        ordre.append(str(i))
    for i in range(nb_exos):
        ordre_exos.append(ordre.pop(random.randrange(nb_exos - i)))
    del ordre
    f0.write('''\\exercice
''')
    f0.write('  Factoriser les expressions suivantes.\n')
    f0.write('  \\begin{multicols}{2}\\noindent\n')
    f1.write('''\\exercice*
''')
    f1.write('  Factoriser les expressions suivantes.\n')
    f1.write('  \\begin{multicols}{2}\\noindent\n')
    for i in range(nb_exos):
        exec('troisiemes.developpements.factorisation' + str(ordre_exos[i]) + \
            '(f1,f0)')
        f0.write('    \\stepcounter{nocalcul}%\n')
        f1.write('    \\stepcounter{nocalcul}%\n')
    f0.write('  \\end{multicols}\n')
    f1.write('  \\end{multicols}\n')


def tex_devfacteq(f0, f1):
    exo = [0, 1, 2, 3, 6][random.randrange(5)]
    expr = troisiemes.developpements.choix_exo(exo)
    valeurx = troisiemes.developpements.valeur_quotient()
    fact = troisiemes.developpements.fin_fact(expr)
    f0.write('''\\exercice
''')
    f0.write('  On donne $A=%s$\\,.\n' % troisiemes.developpements.tex_initial(exo,
             expr))
    f0.write('  \\begin{enumerate}\n')
    f0.write('  \\item Développer et réduire $A$\\,.\n')
    f0.write('  \\item Factoriser $A$\\,.\n')
    f0.write('  \\item Calculer $A$ pour $x=%s$\\,.\n' % \
             troisiemes.fractions.tex_frac(valeurx))
    f0.write("  \\item Résoudre l'équation $A=0$\\,.\n")  # % developpements.tex_dev0(fact))
    f0.write('  \\end{enumerate}\n')
    f1.write('''\\exercice*
''')
    f1.write('  On donne $A=%s$\\,.\n' % troisiemes.developpements.tex_initial(exo,
             expr))
    f1.write('  \\begin{enumerate}\n')
    f1.write('  \\item Développer et réduire $A$\\,.\n')
    troisiemes.developpements.developpements(expr, exo, f1)
    f1.write('  \\item Factoriser $A$\\,.\n')
    exec('troisiemes.developpements.factorisation' + str(exo) + '(f1,valeurs=expr)')
    f1.write('  \\item Calculer $A$ pour $x=%s$\\,.\\par\n' % \
             troisiemes.fractions.tex_frac(valeurx))
    troisiemes.developpements.tex_fractions(expr, valeurx, f1)
    f1.write("  \\item Résoudre l'équation $A=0$\\,.\\par\n")  # % developpements.tex_dev0(fact))
    troisiemes.developpements.tex_equations(fact, f1)
    f1.write('  \\end{enumerate}\n')


def tex_equations(f0, f1):
    valeurs = troisiemes.equations.valeurs(10)
    f0.write('\\exercice\n')
    f1.write('\\exercice*\n')
    troisiemes.equations.equations(f0, f1, valeurs)


def tex_racines(f0, f1):
    f0.write('''\\exercice
''')
    f0.write('  \\begin{enumerate}\n')
    f0.write('  \\item Calculer les expressions suivantes et donner le résultat sous la forme $a\\,\\sqrt{b}$ avec $a$ et $b$ entiers, $b$ le plus petit possible.\n')
    f0.write('  \\begin{multicols}{2}\\noindent\n')
    f1.write('''\\exercice*
''')
    f1.write('  \\begin{enumerate}\n')
    f1.write('  \\item Calculer les expressions suivantes et donner le résultat sous la forme $a\\,\\sqrt{b}$ avec $a$ et $b$ entiers, $b$ le plus petit possible.\n')
    mymax = 5
    f1.write('    \\begin{multicols}{2}\\noindent\n')
    valeurs = troisiemes.racines.valeurs_aRb0(mymax)
    troisiemes.racines.exoaRb0(f0, f1, valeurs)
    f0.write('      \\columnbreak\\stepcounter{nocalcul}%\n')
    f1.write('      \\columnbreak\\stepcounter{nocalcul}%\n')
    valeurs = troisiemes.racines.valeurs_aRb1(mymax)
    troisiemes.racines.exoaRb1(f0, f1, valeurs)
    f0.write('    \\end{multicols}\\vspace{-3ex}\n')
    f1.write('    \\end{multicols}\n')
    f0.write('  \\item Calculer les expressions suivantes et donner le résultat sous la forme $a+b\\,\\sqrt{c}$ avec $a$, $b$ et $c$ entiers.\n')
    f0.write('''    \\stepcounter{nocalcul}%
    \\begin{multicols}{2}\\noindent
''')
    f1.write('  \\item Calculer les expressions suivantes et donner le résultat sous la forme $a+b\\,\\sqrt{c}$ avec $a$, $b$ et $c$ entiers.\n')
    f1.write('''    \\stepcounter{nocalcul}%
    \\begin{multicols}{2}\\noindent
''')
    valeurs = troisiemes.racines.valeurs_aPbRc(mymax)
    troisiemes.racines.exo_aPbRc(f0, f1, valeurs)
    f0.write('      \\columnbreak\\stepcounter{nocalcul}%\n')
    f1.write('      \\columnbreak\\stepcounter{nocalcul}%\n')
    valeurs = troisiemes.racines.valeurs_aPbRc(mymax)
    troisiemes.racines.exo_aPbRc(f0, f1, valeurs)
    f0.write('    \\end{multicols}\\vspace{-3ex}\n')
    f1.write('    \\end{multicols}\n')
    f0.write("  \\item Calculer les expressions suivantes et donner le résultat sous la forme d'un nombre entier.\n")
    f0.write('''    \\stepcounter{nocalcul}%
    \\begin{multicols}{2}\\noindent
''')
    f1.write("  \\item Calculer les expressions suivantes et donner le résultat sous la forme d'un nombre entier.\n")
    f1.write('''    \\stepcounter{nocalcul}%
    \\begin{multicols}{2}\\noindent
''')
    valeurs = troisiemes.racines.valeurs_entier0(mymax)
    troisiemes.racines.exo_entier0(f0, f1, valeurs)
    f0.write('      \\columnbreak\\stepcounter{nocalcul}%\n')
    f1.write('      \\columnbreak\\stepcounter{nocalcul}%\n')
    valeurs = troisiemes.racines.valeurs_entier1(mymax)
    troisiemes.racines.exo_entier1(f0, f1, valeurs)
    f0.write('    \\end{multicols}\\vspace{-3ex}\n')
    f0.write('  \\end{enumerate}\n')
    f1.write('    \\end{multicols}\n')
    f1.write('  \\end{enumerate}\n')


def tex_systemes(f0, f1):
    valeurs = troisiemes.systemes.choix_valeurs(10)
    f0.write('\\exercice\n')
    f1.write('\\exercice*\n')
    f0.write("  Résoudre le système d'équations suivant :\n")
    f1.write("  Résoudre le système d'équations suivant :\n")
    troisiemes.systemes.systemes(f0, f1, valeurs)


def tex_pythagore(f0, f1):
    while True:
        longueurs = (troisiemes.pythagore.couples_pythagore)[random.randrange(120)]
        longueurs = [longueurs[i] / 10.0 for i in range(3)]
        if troisiemes.pythagore.inegalite_triangulaire(longueurs):
            break
    noms = troisiemes.pythagore.noms_sommets(3)
    angles = troisiemes.pythagore.fig_tr_rect(longueurs)
    f0.write('\\exercice\n')
    f1.write('\\exercice*\n')
    troisiemes.pythagore.tex_pythagore(f0, f1, noms, angles, longueurs)


def tex_reciproque_pythagore(f0, f1):
    while True:
        longueurs = (troisiemes.pythagore.couples_pythagore)[random.randrange(120)]
        longueurs = [longueurs[i] / 10.0 for i in range(3)]
        if troisiemes.pythagore.inegalite_triangulaire(longueurs):
            break
    noms = troisiemes.pythagore.noms_sommets(3)
    f0.write('''\\exercice
''')
    f1.write('''\\exercice*
''')
    troisiemes.pythagore.tex_reciproque_pythagore(f0, f1, noms, longueurs)


def tex_triangle_cercle(f0, f1):
    while True:
        longueurs = (troisiemes.pythagore.couples_pythagore)[random.randrange(120)]
        longueurs = [longueurs[i] / 10.0 for i in range(3)]
        if troisiemes.pythagore.inegalite_triangulaire(longueurs):
            break
    noms = troisiemes.pythagore.noms_sommets(3)
    angles = troisiemes.pythagore.fig_tr_rect(longueurs)
    f0.write('\\exercice\n')
    f1.write('\\exercice*\n')
    troisiemes.pythagore.tex_triangle_cercle(f0, f1, noms, angles, longueurs)


def tex_thales(f0, f1):
    f0.write('\\exercice\n')
    f1.write('\\exercice*\n')
    troisiemes.pythagore.thales(f0, f1)


def tex_reciproque_thales(f0, f1):
    f0.write('\\exercice\n')
    f1.write('\\exercice*\n')
    troisiemes.pythagore.rec_thales(f0, f1)


def tex_trigo(f0, f1):
    f0.write('\\exercice\n')
    f1.write('\\exercice*\n')
    troisiemes.pythagore.trigo_init(f0, f1)

def tex_affine(f0,f1):
    f0.write('\\exercice\n')
    f1.write('\\exercice*\n')
    troisiemes.affine.affine(f0,f1)

def tex_proba(f0,f1):
    f0.write('\\exercice\n')
    f1.write('\\exercice*\n')
    troisiemes.proba.proba(f0,f1)

def main(exo, f0, f1):
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
        tex_affine,
        tex_proba,
        tex_pythagore,
        tex_reciproque_pythagore,
        tex_triangle_cercle,
        tex_thales,
        tex_reciproque_thales,
        tex_trigo,
        )

    modules[exo](f0, f1)
