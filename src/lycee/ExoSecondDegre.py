# -*- coding: utf-8 -*-

import sys, os, codecs
from ..classes.SecondDegre import Poly2
from ..outils.Affichage import printlist
from ..outils.Polynomes import choix_coeffs
from ..outils.Arithmetique import *

def exo_second_degre():
    """Créer une exercice comprenant des équations et inéquations du second degré. PAS FINI."""
    exo = "\\exercice\n\
           \\begin{multicols}{2}\n\
           \\noindent "+ u"Question 1 : Chercher les racines des polynômes suivants :\\par\n"
    cor = "\\exercice*\n\
           \\begin{multicols}{2}\n\ \\noindent "+ u"Question 1 : Chercher les racines des polynômes suivants :\\par\n"

    ## Equations
    pol1 = choix_coeffs(False, 2, True)
    pol2 = choix_coeffs(False, 1, False)
    pol3 = choix_coeffs(False, 0, True)
    pol4 = choix_coeffs(False, 2, False)

    ## Inequations
    pol5 = choix_coeffs(True, 0, True)
    pol6 = choix_coeffs(False, 2, True)
    pol7 = choix_coeffs(False, 1, False)
    pol8 = choix_coeffs(False, 2, False)

    ## Somme et produit des racines
    pol9 = choix_coeffs(True, 2, False)

    ## Problème du rectangle
    pol10 = choix_coeffs(True, 2, False)

    exo+="\\par a)$" + pol1[1].print_signe("=")+"$\n"
    exo+="\\par b)$" + pol2[1].print_signe("=")+"$\n"
    exo+="\\par c)$" + pol3[1].print_signe("=")+"$\n"
    exo+="\\par d)$" + pol4[1].print_signe("=")+"$\n"

    cor+="\\par a)$" + pol1[1].print_signe("=")+"$\n"
    cor+="\\par b)$" + pol2[1].print_signe("=")+"$\n"
    cor+="\\par c)$" + pol3[1].print_signe("=")+"$\n"
    cor+="\\par d)$" + pol4[1].print_signe("=")+"$\n"

    cor+="\\par a) On calcule le discriminant : $\\Delta = " + str(pol1[1].delta) + "$.\n"
    cor+="\\par Comme le discrimimant est $" + pol1[1].signedelta + u"$, on en déduit que ce polynôme possède $" + str(pol1[1].nbrac) + "$ racines."

    exo+=u"\\par Question 2 : Résoudre les inéquations suivantes : "
    cor+=u"\\par Question 2 : Résoudre les inéquations suivantes : "

    exo+="\\par a)$" + pol5[1].print_signe("\\le")+"$\n"
    exo+="\\par b)$" + pol6[1].print_signe("\\ge")+"$\n"
    exo+="\\par c)$" + pol7[1].print_signe(">")+"$\n"
    exo+="\\par d)$" + pol8[1].print_signe("<")+"$\n"

    cor+="\\par a)$" + pol5[1].print_signe("\\le")+"$\n"
    cor+="\\par b)$" + pol6[1].print_signe("\\ge")+"$\n"
    cor+="\\par c)$" + pol7[1].print_signe(">")+"$\n"
    cor+="\\par d)$" + pol8[1].print_signe("<")+"$\n"

    exo+="\\par Question 3 : Trouver deux nombres sachant que leur somme est " + str(pol9[1].b) + " et leur produit " + str(pol9[1].c) + ".\n"
    cor+="\\par Question 3 : Trouver deux nombres sachant que leur somme est " + str(pol9[1].b) + " et leur produit " + str(pol9[1].c) + ".\n"

    exo+=u"\\par Question 4 : Trouver les dimensions d'un rectangle, sachant que son périmètre est " + str(pol9[1].b) + " et son aire " + str(pol9[1].c) + "."
    cor+=u"\\par Question 4 : Trouver les dimensions d'un rectangle, sachant que son périmètre est " + str(pol9[1].b) + " et son aire " + str(pol9[1].c) + "."

    exo+="\\end{multicols}\n"
    cor+="\\end{multicols}\n"
    return (exo, cor)

if __name__=="__main__":
    from TEST.imprimetest import *
    exo,cor=exo_second_degre()
    imprime_TeX(exo+"\\pagebreak"+cor,"secondegre.tex")
