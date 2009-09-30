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

#from . import decimaux
#from . import operations
#from . import droites
#from . import quotients
#from . import fractions
#from . import angles
#from . import symetrie
#from outils import tex_entete
import sixiemes.angles, sixiemes.decimaux, sixiemes.droites, sixiemes.fractions
import sixiemes.operations, sixiemes.quotients, sixiemes.symetrie
import random


def tex_ecrit_nombre(f0, f1):
    f0.write("""
\\exercice
""")
    f0.write('\\begin{enumerate}\n')
    f0.write('  \\item Écrire en chiffres les nombres suivants.\n')
    f0.write('    \\begin{enumerate}\n')
    f1.write("""
\\exercice*
""")
    f1.write('\\begin{enumerate}\n')
    f1.write('  \\item Écrire en chiffres les nombres suivants.\n')
    f1.write('    \\begin{enumerate}\n')
    sixiemes.decimaux.EcritEnChiffre(f0, f1)
    f0.write('    \\end{enumerate}\n')
    f0.write('  \\item Écrire en lettres les nombres suivants (sans utiliser le mot ``virgule").\n')
    f0.write('    \\begin{enumerate}\n')
    f1.write('    \\end{enumerate}\n')
    f1.write('  \\item Écrire en lettres les nombres suivants (sans utiliser le mot ``virgule").\n')
    f1.write('    \\begin{enumerate}\n')
    sixiemes.decimaux.EcritEnLettre(f0, f1)
    f0.write('    \\end{enumerate}\n')
    f0.write('\\end{enumerate}\n')
    f1.write('    \\end{enumerate}\n')
    f1.write('\\end{enumerate}\n')


def tex_operations(f0, f1):
    nb_exos = 3
    tex_exos = (sixiemes.operations.tex_somme,
                sixiemes.operations.tex_difference,
                sixiemes.operations.tex_produit)
    ordre_exos = [i for i in range(nb_exos)]
    f0.write("""
\\exercice
""")
    f0.write('Poser et effectuer les opérations suivantes.\n')
    f0.write('\\begin{multicols}{2}\\noindent\n')
    f0.write('  \\begin{enumerate}\n')
    f1.write("""
\\exercice*
""")
    f1.write('Poser et effectuer les opérations suivantes.\n')
    f1.write('\\begin{multicols}{2}\\noindent\n')
    f1.write('  \\begin{enumerate}\n')
    for i in range(nb_exos):
        a = random.randrange(nb_exos - i)
        j = ordre_exos.pop(a)
        tex_exos[j](f0, f1)
    f0.write('  \\end{enumerate}\n')
    f0.write('\\end{multicols}\n')
    f1.write('  \\end{enumerate}\n')
    f1.write('\\end{multicols}\n')


def tex_calcul_mental(f0, f1):
    f0.write("""
\\exercice
""")
    f0.write('Effectuer sans calculatrice :\n')
    f0.write('\\begin{multicols}{4}\\noindent\n')
    f0.write('  \\begin{enumerate}\n')
    f1.write("""
\\exercice*
""")
    f1.write('Effectuer sans calculatrice :\n')
    f1.write('\\begin{multicols}{4}\\noindent\n')
    f1.write('  \\begin{enumerate}\n')
    sixiemes.operations.tex_calcul_mental(f0, f1)
    f0.write('  \\end{enumerate}\n')
    f0.write('\\end{multicols}\n')
    f1.write('\\end{enumerate}\n')
    f1.write('\\end{multicols}\n')


def tex_dix(f0, f1):
    f0.write("""
\\exercice
""")
    f0.write('Compléter sans calculatrice :\n')
    f0.write('\\begin{multicols}{2}\\noindent\n')
    f0.write('  \\begin{enumerate}\n')
    f1.write("""
\\exercice*
""")
    f1.write('Compléter sans calculatrice :\n')
    f1.write('\\begin{multicols}{2}\\noindent\n')
    f1.write('  \\begin{enumerate}\n')
    sixiemes.operations.tex_dix(f0, f1)
    f0.write('  \\end{enumerate}\n')
    f0.write('\\end{multicols}\n')
    f1.write('  \\end{enumerate}\n')
    f1.write('\\end{multicols}\n')


def tex_conversions(f0, f1):
    f0.write("""
\\exercice
""")
    f0.write('Effectuer les conversions suivantes :\n')
    f0.write('\\begin{multicols}{3}\\noindent\n')
    f0.write('  \\begin{enumerate}\n')
    f1.write("""
\\exercice*
""")
    f1.write('Effectuer les conversions suivantes :\n')
    f1.write('\\begin{multicols}{2}\\noindent\n')
    f1.write('  \\begin{enumerate}\n')
    sixiemes.decimaux.tex_units(f0, f1)
    f0.write('  \\end{enumerate}\n')
    f0.write('\\end{multicols}\n')
    f1.write('  \\end{enumerate}\n')
    f1.write('\\end{multicols}\n')


def tex_decimaux(f0, f1):
    f0.write("""
\\exercice
""")
    f1.write("""
\\exercice*
""")
    sixiemes.decimaux.tex_place_virgule(f0, f1)


def tex_frac(f0, f1):
    f0.write("""
\\exercice
""")
    f1.write("""
\\exercice*
""")
    f0.write("Compl\xe9ter :\n")
    f0.write('\\begin{multicols}{3}\\noindent\n')
    f0.write('  \\begin{enumerate}\n')
    f1.write("Compl\xe9ter :\n")
    f1.write('\\begin{multicols}{3}\\noindent\n')
    f1.write('  \\begin{enumerate}\n')
    sixiemes.decimaux.tex_frac(f0, f1)
    f0.write('  \\end{enumerate}\n')
    f0.write('\\end{multicols}\n')
    f1.write('  \\end{enumerate}\n')
    f1.write('\\end{multicols}\n')


def tex_decomposition(f0, f1):
    f0.write("""
\\exercice
""")
    f1.write("""
\\exercice*
""")
    f0.write("Compl\xe9ter avec un nombre d\xe9cimal :\n")
    f0.write('\\begin{multicols}{2}\\noindent\n')
    f0.write('  \\begin{enumerate}\n')
    f1.write("Compl\xe9ter avec un nombre d\xe9cimal :\n")
    f1.write('\\begin{multicols}{2}\\noindent\n')
    f1.write('  \\begin{enumerate}\n')
    sixiemes.decimaux.tex_dec(f0, f1)
    f0.write('  \\end{enumerate}\n')
    f0.write('\\end{multicols}\n')
    f1.write('  \\end{enumerate}\n')
    f1.write('\\end{multicols}\n')


def tex_classer(f0, f1):
    f0.write("""
\\exercice
""")
    f0.write('\\begin{enumerate}\n')
    f0.write('  \\item ')
    f1.write("""
\\exercice*
""")
    f1.write('\\begin{enumerate}\n')
    f1.write('  \\item ')
    sixiemes.decimaux.classer(f0, f1)
    f0.write('\n  \\item ')
    f1.write('\n  \\item ')
    sixiemes.decimaux.classer(f0, f1)
    f0.write('\\end{enumerate}\n')
    f1.write('\\end{enumerate}\n')


def tex_droites(f0, f1):
    f0.write("""
\\exercice
""")
    f1.write("""
\\exercice*
""")
    f0.write("Compl\xe9ter :\\par\n")
    f0.write('\\begin{tabular}{|p{3cm}|p{5cm}|c|}\n')
    f0.write('  \\hline\n')
    f0.write('  \\hfill{} \\textbf{Nom} \\hfill{} & \\hfill{}\\textbf{Catégorie}\\hfill{} & \\textbf{Figure} \\\\\n \\hline\n')
    f1.write("Compl\xe9ter :\\par\n")
    f1.write('\\begin{tabular}{|p{3cm}|p{5cm}|c|}\n')
    f1.write('  \\hline\n')
    f1.write('  \\hfill{} \\textbf{Nom} \\hfill{} & \\hfill{}\\textbf{Catégorie}\\hfill{} & \\textbf{Figure} \\\\\n \\hline\n')
    sixiemes.droites.tex_droites(f0, f1)
    f0.write('\\end{tabular}\n')
    f1.write('\\end{tabular}\n')


def tex_perpendiculaires(f0, f1):
    f0.write("""
\\exercice
""")
    f1.write("""
\\exercice*
""")
    f0.write("R\xe9aliser les figures suivantes :\\par\n")
    f0.write('\\begin{multicols}{2}\n')
    f1.write("R\xe9aliser les figures suivantes :\\par\n")
    f1.write('\\begin{multicols}{2}\n')
    sixiemes.droites.enonce_perp(f0, f1)
    f0.write('  \\columnbreak\n')
    f1.write('  \\columnbreak\n')
    sixiemes.droites.enonce_perp(f0, f1)
    f0.write('\\end{multicols}\n')
    f1.write('\\end{multicols}\n')


def tex_proprietes(f0, f1):
    f0.write("""
\\exercice
""")
    f1.write("""
\\exercice*
""")
    f0.write("""Compl\xe9ter le tableau suivant :\\par
Les droites en gras sont parall\xe8les.\\par
""")
    f1.write("""Compl\xe9ter le tableau suivant :\\par
Les droites en gras sont parall\xe8les.\\par
""")
    sixiemes.droites.enonce_prop(f0, f1)


def tex_divisibles(f0, f1):
    f0.write("""
\\exercice
""")
    f0.write('Cocher les bonnes r\xe9ponses :\\par\n')
    f1.write("""
\\exercice*
""")
    f1.write('Cocher les bonnes r\xe9ponses :\\par\n')
    sixiemes.quotients.tex_divisible(f0, f1)


def fractions_partage(f0, f1):
    f0.write("""
\\exercice
""")
    f0.write('\\begin{multicols}{2}\n')
    f0.write('  \\begin{enumerate}\n')
    f1.write("""
\\exercice*
""")
    f1.write('\\begin{multicols}{2}\n')
    f1.write('  \\begin{enumerate}\n')
    sixiemes.fractions.exo_fraction_partage(f0, f1)
    f0.write('  \\end{enumerate}\n')
    f0.write('\\end{multicols}\n')
    f1.write('  \\end{enumerate}\n')
    f1.write('\\end{multicols}\n')


def fractions_abscisses(f0, f1):
    f0.write("""
\\exercice
""")
    f1.write("""
\\exercice*
""")
    sixiemes.fractions.questions_fractions_abscisses(f0, f1)


def symetrie_quadrillage(f0, f1):
    f0.write("""
\\exercice
""")
    f1.write("""
\\exercice
""")
    f0.write("Construire la sym\xe9trique de chacune des figures par rapport à la droite en\n")
    f0.write("utilisant le quadrillage :\\par\n")
    f0.write("\\psset{unit=.9cm}\n")
    f1.write("Construire la sym\xe9trique de chacune des figures par rapport à la droite en\n")
    f1.write("utilisant le quadrillage :\\par\n")
    f1.write("\\psset{unit=.9cm}\n")
    sixiemes.symetrie.exo_quadrillage(f0, f1)


def mesures_angles(f0, f1):
    f0.write("""
\\exercice
""")
    f1.write("""
\\exercice*
""")
    f0.write('Nommer, mesurer et donner la nature de chacun des angles suivants :\\par \n')
    f1.write('Nommer, mesurer et donner la nature de chacun des angles suivants :\\par \n')
    sixiemes.angles.mesure_angles(f0, f1)


def main(exo, f0, f1):
    modules = (
        tex_calcul_mental,
        tex_ecrit_nombre,
        tex_decimaux,
        tex_frac,
        tex_decomposition,
        tex_conversions,
        tex_operations,
        tex_dix,
        tex_classer,
        tex_droites,
        tex_perpendiculaires,
        tex_proprietes,
        tex_divisibles,
        fractions_partage,
        fractions_abscisses,
        symetrie_quadrillage,
        mesures_angles,
        )
    modules[exo](f0, f1)
