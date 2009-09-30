# -*- coding: utf-8 -*-

from classes/SecondDegre import Poly2
from outils/Affichage import printlist
from outils/Polynomes import choix_coeffs

def exo_second_degre():
    """Créer une exercice comprenant des équations et inéquations du second degré. PAS FINI."""
    exo = ["\\exercice",
           "\\begin{multicols}{4}", "  \\noindent", "Question 1 : Chercher les racines des polyn\\^omes suivants :"]
    cor = ["\\exercice*",
           "\\begin{multicols}{4}", "  \\noindent", "Question 1 : Chercher les racines des polyn\\^omes suivants :"]

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

    exo.append("a)" + pol1[1].print_signe("="))
    exo.append("b)" + pol2[1].print_signe("="))
    exo.append("c)" + pol3[1].print_signe("="))
    exo.append("d)" + pol4[1].print_signe("="))

    cor.append("a)" + pol1[1].print_signe("="))
    cor.append("b)" + pol2[1].print_signe("="))
    cor.append("c)" + pol3[1].print_signe("="))
    cor.append("d)" + pol4[1].print_signe("="))

    cor.append("a) On calcule le discriminant : Delta = " + str(pol1[1].delta) + ".")
    cor.append("Comme le discrimimant est " + pol1[1].signedelta + ", on en déduit que ce polyn\\^ome poss\\`ede " + str(pol1[1].nbrac) + " racines.")

    exo.append("Question 2 : R\\'esoudre les in\\'equations suivantes : ")
    cor.append("Question 2 : R\\'esoudre les in\\'equations suivantes : ")

    exo.append("a)" + pol5[1].print_signe("\\le"))
    exo.append("b)" + pol6[1].print_signe("\\ge"))
    exo.append("c)" + pol7[1].print_signe(">"))
    exo.append("d)" + pol8[1].print_signe("<"))

    cor.append("a)" + pol5[1].print_signe("\\le"))
    cor.append("b)" + pol6[1].print_signe("\\ge"))
    cor.append("c)" + pol7[1].print_signe(">"))
    cor.append("d)" + pol8[1].print_signe("<"))

    exo.append("Question 3 : Trouver deux nombres sachant que leur somme est " + str(pol9[1].b) + " et leur produit " + str(pol9[1].c) + ".")
    cor.append("Question 3 : Trouver deux nombres sachant que leur somme est " + str(pol9[1].b) + " et leur produit " + str(pol9[1].c) + ".")

    exo.append("Question 4 : Trouver les dimensions d'un rectangle, sachant que son p\\'erim\\`etre est " + str(pol9[1].b) + " et son aire " + str(pol9[1].c) + ".")
    cor.append("Question 4 : Trouver les dimensions d'un rectangle, sachant que son p\\'erim\\`etre est " + str(pol9[1].b) + " et son aire " + str(pol9[1].c) + ".")

    return (exo, cor)

result = exo_second_degre()

printlist(result[0])

print "#" * 100

printlist(result[1])














    