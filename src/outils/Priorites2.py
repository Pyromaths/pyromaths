# -*- coding: utf-8 -*-
import re

## TODO Gestion des signes qui se suivent ( 3+-5 ou 3*-5 ) --> à mon avis inutile si le calcul généré contient des parenthèses - Arnaud
## TODO Problème avec l'opposé d'un nombre -(-5)+(+2)

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
      [\+\-]?                       #un éventuel signe
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
                             str(sous_resultat) +
                             sous_calcul[2][1:] +
                             post])
        else:
            solution.extend([pre +
                             sous_calcul[0] +
                             str(sous_resultat) +
                             sous_calcul[2] +
                             post])
        calcul = sous_calcul[0] + str(sous_resultat) + sous_calcul[2]
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

for element in priorites("(2-5)**2+(5-2)**3+((3*4+5)*2+3*(32-5*7)**2)*5+17*(12-3*5)"):
  print element 
  
#print priorites("((-(-1)+-2)++3)")
#print priorites("4-((-1+-2)+3)")
#print priorites('8-(-5*(2-4))')
#print priorites("1+2+3+4")
#print priorites("-3**+2")
#print priorites("9+8*7")
#print priorites("8+1.3e+2")
