# -*- coding: utf-8 -*-

import re
from Affichage import decimaux
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



#a=testfraction.fraction(5,7)
#b=testfraction.fraction(4,3)
#c=testfraction.fraction(8,9)
#
#
#c=split_calc('(a+b)*c')


#calcul = raw_input("Un autre calcul ?\nIl faut mettre des parenthèses à chaque opération, même si inutiles.\n")

#split_calc(calcul)

#TODO : étendre à des nombres avec plusieurs chiffres
#---------------------------------------------------------------------
#autre version des priorités
#---------------------------------------------------------------------

import re

def priorites(calcul, pre = "", post = "", solution = []):
    if not solution: solution = [calcul]
    recherche_parentheses = r"""
    ^(.*)                           #des calculs dans le groupe 0
    (                               #début du groupe 1
      \(                            #commence par une parenthèse ouvrante
      (?:                           #regroupement 0 (non groupe)
        [\+\-]?                     #un éventuel signe
        (?:                         #regroupement 1 (non groupe)
          \(                        #une parenthèse ouvrante
          [\+\-]?                   #un éventuel signe
          \d+\.?\d*(?:e[\+\-]\d+)?  #on cherche un nombre avec une éventuelle
                                    #partie décimale et un éventuel exposant
          \)                        #une parenthèse fermante
        |                           #ou
          \d+\.?\d*(?:e[\+\-]\d+)?  #on cherche un nombre avec une éventuelle
                                    #partie décimale et un éventuel exposant
        |                           #ou
          \w+                       #un littéral
        )                           #fin du regroupement 1
        [\+\-\*/]+                  #un opérateur
      )+                            #fin du regroupement 0 (présent au moins
                                    #un fois)
      [\+\-]?                     #un éventuel signe
      (?:                           #regroupement 0 (non groupe)
          \(                        #une parenthèse ouvrante
          [\+\-]?                   #un éventuel signe
          \d+\.?\d*(?:e[\+\-]\d+)?  #on cherche un nombre avec une éventuelle
                                    #partie décimale et un éventuel exposant
          \)                        #une parenthèse fermante
        |                           #ou
          \d+\.?\d*(?:e[\+\-]\d+)?  #on cherche un nombre avec une éventuelle
                                    #partie décimale et un éventuel exposant
        |                           #ou
        \w+                         #un littéral
      )                             #fin du regroupement 0 présent une seule fois
      \)                            #fini par une parenthèse fermante
    )                               #fin du groupe 1
    (.*)$                           #des calculs pour finir
    """
    test = re.search(recherche_parentheses, calcul, re.VERBOSE)
    while test:
        sous_calcul = test.groups()
        (calcul, solution) = priorites_operations(sous_calcul[1],
                                                  sous_calcul[0],
                                                  sous_calcul[2],
                                                  solution)
        calcul = solution[-1]
        test = re.search(recherche_parentheses, calcul, re.VERBOSE)
    calcul, solution = priorites_operations(calcul, pre, post, solution)
    return(solution)

def traite_operation(operateur, calcul, pre, post, solution):
    pattern = r"""
            (                   #groupe 0
                ^\(*                #le calcul est au début (aux parenthèses près)
                                    #les signes +/- font parti du groupe 2
            |                   #ou
                ^.*?[\+\-]?         #il y a des calculs avant, le 1e signe +/-
                                    #est un opérateur
            )                   #fin du groupe 0
            (                   #groupe 1
                (?:                 #regroupement 1 (non groupe)
                    [\+\-]?                 #un éventuel signe
                    \(                      #une parenthèse ouvrante
                    [\+\-]?                 #un éventuel signe
                    \d+\.?\d*(?:e[\+\-]\d+)? #on cherche un nombre avec une
                                            #éventuelle partie décimale et un
                                            #éventuel exposant
                    \)                     #une parenthèse fermante
                |                   #ou
                    [\+\-]?                 #un éventuel signe
                    \d+\.?\d*(?:e[\+\-]\d+)? #on cherche un nombre avec une
                                            #éventuelle partie décimale et un
                                            #éventuel exposant
                |                   #ou
                    \w+                     #un littéral
                )                   #fin du regroupement 1
                {0}                 #opération
                (?:                 #regroupement 2 (non groupe)
                    [\+\-]?                 #un éventuel signe
                    \(                     #une parenthèse ouvrante
                    [\+\-]?                 #un éventuel signe
                    \d+\.?\d*(?:e[\+\-]\d+)? #on cherche un nombre avec une
                                            #éventuelle partie décimale et un
                                            #éventuel exposant
                    \)                     #une parenthèse fermante
                |                   #ou
                    [\+\-]?                 #un éventuel signe
                    \d+\.?\d*(?:e[\+\-]\d+)? #on cherche un nombre avec une
                                            #éventuelle partie décimale et un
                                            #éventuel exposant
                |                           #ou
                    \w+                     #un littéral
                )                   #fin du regroupement 2
            )                   #fin du groupe 1
            (.*?)$              #tout le reste
            """.format(operateur)
    test = re.search(pattern, calcul, re.VERBOSE)
    while test:
        sous_calcul = test.groups()
        sous_resultat = eval(sous_calcul[1])
        if (sous_calcul[0] and sous_calcul[0][-1] == '(') and \
           (sous_calcul[2][0] and sous_calcul[2][0] == ')') and \
           (post[:2] != '**' or sous_resultat > 0):
            #permet de supprimer les parenthèses
            solution.extend([pre +
                             sous_calcul[0][:-1] +
                             decimaux(sous_resultat, True) +
                             sous_calcul[2][1:] +
                             post])
        else:
            solution.extend([pre +
                             sous_calcul[0] +
                             decimaux(sous_resultat, True) +
                             sous_calcul[2] +
                             post])
        calcul = sous_calcul[0] + decimaux(sous_resultat, True) + sous_calcul[2]
        test = re.search(pattern, calcul, re.VERBOSE)
    return (calcul, pre, post, solution)

def priorites_operations(calcul, pre = "", post = "", solution = []):
    calcul, pre, post, solution = traite_operation("\*\*", calcul, pre,
                                                   post, solution)
    calcul, pre, post, solution = traite_operation("[\*/]", calcul, pre,
                                                   post, solution)
    calcul, pre, post, solution = traite_operation("[\+\-]", calcul, pre,
                                                   post, solution)
    return (calcul, solution)

print(priorites("8+1.3e+2"))
print(priorites("755*(12-15)**2+(15-12)**3"))
print(priorites("((-(-1)+-2)++3)"))
print(priorites("4-((-1+-2)+3)"))
print(priorites('8-(-5*(2-4))'))
print(priorites("1+2+3+4"))
print(priorites("-3**+2"))
print(priorites("9+8*7"))
