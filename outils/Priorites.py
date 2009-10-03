# -*- coding: utf-8 -*-

import re

def split_calc(calcul):

    """Test de gestion et affichage des priorités de calcul, détaillées. PAS
    FINI."""

    liste_op = []
    liste_result = []

    init = calcul  # Sauvegarde du calcul de départ

    # Construction d'une liste comportant la liste de toutes les opérations
    i = 0

    while calcul.count('(') > 0:
        current = 'l' + str(i)
        liste_op.append(re.search('\(\w+[\+\-/\*]\w+\)',
            calcul).group().strip('()'))
        calcul = re.sub('\(\w+[\+\-/\*]\w+\)', current, calcul, 1)
        i += 1

    liste_op.append(re.search('\w+[\+\-/\*]\w+', calcul).group())

    # Calcul des différentes opérations contenues dans liste_op et
    # enregistrement des résultats dans liste_result

    for index in range(len(liste_op)):
        element = liste_op[index]
        m = re.findall('l(\d+)', element)

        for k in range(len(m)):
            motif = 'liste_result[' + m[k] + ']'
            element = re.sub('l\d+', motif , element, 1)

        liste_op[index] = element

        liste_result.append(eval(liste_op[index]))

    print liste_op
    print liste_result, liste_result[0]

    # On sert de la sauvegarde pour afficher le déroulement du calcul
    j = 0

    print init, " = ",
    longueur = len(init) + 2

    while init.count('(') > 0:
        current = 'l' + str(i)
        init = re.sub('\(\w+[\+\-/\*]\w+\)', str(eval(liste_op[j])), init, 1)
        j += 1

        print(init + "\n" + " " * longueur + "= ",)

    # Afficher le résultat du calcul
    print(liste_result[-1])



a=testfraction.fraction(5,7)
b=testfraction.fraction(4,3)
c=testfraction.fraction(8,9)


c=split_calc('(a+b)*c')


#calcul = raw_input("Un autre calcul ?\nIl faut mettre des parenthèses à chaque opération, même si inutiles.\n")

#split_calc(calcul)

#TODO : étendre à des nombres avec plusieurs chiffres
