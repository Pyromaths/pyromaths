# -*- coding: utf-8 -*-

import re, sys
from Affichage import decimaux
from . import Arithmetique, Affichage
import math
from .Fractions import EffectueSommeFractions, EffectueQuotientFractions, EffectueProduitFractions

def EffectueCalcul(op, nb1, nb2, pre="", post=""):
    denominateur_max = 20
    programme = 6  # Faisable pour toutes les classes
    fr = Fractions(1, 1)  # Une fraction type pour vérifier le type de nb1 et nb2
    bfr = type(nb1) == type(nb2) == type(fr)  # bfr est vrai si on calcul avec des fractions
    if type(nb1) == type(fr) and type(nb2) != type(fr):
        nb2 = Fractions(nb2)
        bfr = True
    if type(nb2) == type(fr) and type(nb1) != type(fr):
        nb1 = Fractions(nb1)
        bfr = True
    if not bfr and pre.rstrip().endswith('(') and post.lstrip().startswith(')'):
        pre = pre.rstrip()[:len(pre.rstrip()) - 1]
        post = post.lstrip()[1:]
    if op == "+":
        if bfr:
            l = EffectueSommeFractions(nb1, nb2, op, pre, post)
            resultat = Fractions.simplifie(nb1 + nb2)
            if abs(resultat.d) > denominateur_max:
                programme = 2
        else:
            l = ["%s%s%s" % (pre, Affichage.decimaux(nb1 + nb2, 1), post)]
            resultat = nb1 + nb2
    elif op == "-":
        if bfr:
            l = EffectueSommeFractions(nb1, nb2, op, pre, post)
            resultat = Fractions.simplifie(nb1 - nb2)
            n = nb1 - nb2
            if n.n < 0:
                programme = 4
            if resultat.n * resultat.d < 0:
                programme = 4
            if abs(resultat.d) > denominateur_max:
                programme = 2
        else:
            l = ["%s%s%s" % (pre, Affichage.decimaux(nb1 - nb2, 1), post)]
            resultat = nb1 - nb2
            if resultat < 0:
                programme = 4
    elif op == "*":
        if bfr:
            l = EffectueProduitFractions(nb1, nb2, pre, post)
            resultat = Fractions.simplifie(nb1 * nb2)
            if abs(resultat.d) > denominateur_max:
                programme = 2
        else:
            l = ["%s%s%s" % (pre, Affichage.decimaux(nb1 * nb2, 1), post)]
            resultat = nb1 * nb2
    else:
        if bfr:
            if nb2.n:  # Pas de division par zéro
                l = EffectueQuotientFractions(nb1, nb2, pre, post)
                resultat = Fractions.simplifie(nb1 / nb2)
                if abs(resultat.d) > denominateur_max:
                    programme = 2
            else:
                (l, resultat, programme) = ([], 1, 1)
        else:
            if nb2 == 0:  # division par zéro
                (l, resultat, programme) = ([], 1, 1)
            else:
                l = ["%s%s%s" % (pre, Affichage.decimaux((nb1 * 1.0) /
                     nb2, 1), post)]
                resultat = (nb1 * 1.0) / nb2
                if resultat - math.floor(resultat) == 0.0:
                    programme = 6
                elif resultat * 100 - math.floor(resultat * 100) == 0.0:
                    programme = 5
                else:
                    programme = 2
    return (l, resultat, programme)


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
                ^.*?[\+\-]?         #il y a des calculs avant, le 1er signe +/-
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
        print(sous_calcul)
        print(pre, post)
        sous_resultat = eval(sous_calcul[1])
        if isinstance(sous_resultat, list):
            for element in sous_resultat:
                solution.extend([pre +
                             sous_calcul[0] +
                             str(element) +
                             sous_calcul[2] +
                             post])
            a = sous_resultat[-1]
            sous_resultat = 'a'
        elif (sous_calcul[0] and sous_calcul[0][-1] == '(') and \
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
    for string in ["\*\*", "[\*/]", "[\+\-]"]:
        calcul, pre, post, solution = traite_operation(string, calcul, pre,
                                                   post, solution)
    #calcul, pre, post, solution = traite_operation("\*\*", calcul, pre,
                                                   #post, solution)
    #calcul, pre, post, solution = traite_operation("[\*/]", calcul, pre,
                                                   #post, solution)
    #calcul, pre, post, solution = traite_operation("[\+\-]", calcul, pre,
                                                   #post, solution)
    return (calcul, solution)

##
##print(priorites("(12-15)**2+(15-12)**3"))
##print("_" * 40)
###print(priorites("((-(-1)+-2)++3)"))
###print("_" * 40)
###print(priorites("4-((-1+-2)+3)"))
###print("_" * 40)
###print(priorites('8-(-5*(2-4))'))
###print("_" * 40)
##print(priorites("1+2+3+4"))
##print("_" * 40)
###print(priorites("-3**+2"))
###print("_" * 40)
###print(priorites("9+8*7"))
###print("_" * 40)
###print(priorites("8+1.3e+2"))
###print("_" * 40)
##a, b, c = Racine(5), Racine(5, 3), Racine(5, 2)
##print(priorites("2*(a+b+c)"))
##print("_" * 40)
##a, b = Racine(5), Racine(5, 3)
##print(priorites("a*b*2"))
###print("_" * 40)
###c, d = Terme(5, 2), Terme(-6, 2)
###print(priorites("c*d"))
###print("_" * 40)
##print(priorites("8+1.3e+2"))
##print(priorites("755*(12-15)**2+(15-12)**3"))
##print(priorites("((-(-1)+-2)++3)"))
##print(priorites("4-((-1+-2)+3)"))
##print(priorites('8-(-5*(2-4))'))
##print(priorites("1+2+3+4"))
##print(priorites("-3**+2"))
##print(priorites("9+8*7"))

from ..classes.Fractions import Fractions
from . import Arithmetique, Affichage
import random
import math
from TeXMiseEnForme import Affichage

#===============================================================================
# Gère les priorités opératoires pour le calcul décimal et fractionnaire
#===============================================================================


def OperateurPrioritaire(exercice, niveau, pre="", post="", solution=[]):
    '''Renvoie un tuple contenant :
    - la liste solution contenant la liste des instructions TeX \xc3\xa0 \xc3\xa9crire dans le corrig\xc3\xa9
    - le r\xc3\xa9sultat de l\'expression.
    La liste exercice peut contenir des nombres ou des objets Fractions.
    Ex : OperateurPrioritaire([3,"+",5,"*",2]) => [\'3 + 10\', \'13\'] , 13
    Ex : OperateurPrioritaire([Fractions(15,4),\'*\',Fractions(14,25),\'-\',Fractions(3,2)])
         => [ \'\\dfrac{3 \\times \\cancel{5}}{2 \\times \\bcancel{2}} \\times \\dfrac{7 \\times \\bcancel{2}}{5 \\times \\cancel{5}} - \\dfrac{3}{2}\',
              \'\\dfrac{21}{10} - \\dfrac{3}{2}\',
              \'\\dfrac{21}{10}-\\dfrac{3_{\\times 5}}{2_{\\times 5}}\',
              \'\\dfrac{3_{\\times 2}}{5_{\\times 2}}\',
              \'\\dfrac{3}{5}\'
            ],
            <pyro_classes.Fractions instance at 0xb7ddddec> (Fractions(3,5))

    @param exercice: liste contenant la succession d\'op\xc3\xa9rations [3, \'+\', 5, \'*\', 2]
    @param niveau: niveau auquel doit se situer l\'exercice : 6: entiers, 5: d\xc3\xa9cimaux positifs, 4: d\xc3\xa9cimaux relatifs
    @param pre: chaine contenant ce qui doit \xc3\xaatre ajouter avant la solution
    @param post: chaine contenant ce qui doit \xc3\xaatre ajouter apr\xc3\xa8s la solution
    @param solution: liste contenant chaque ligne \xc3\xa0 \xc3\xa9crire dans le fichier TeX pour
                     le corrig\xc3\xa9
    '''

    if len(exercice) == 1:  # il ne reste plus qu'un nombre (le résultat) donc c'est fini
        return (solution, exercice[0], niveau)
    else:

          # Trouvons l'opérateur prioritaire :

        nbpar = exercice.count('(')
        nbmul = exercice.count("*")
        nbdiv = exercice.count("/")
        if nbpar:  # Des parenthèses oui, mais y-a-t-il des parenthèses à l'intérieur des parenthèses ?
            i0 = TrouveParentheseInterieure(exercice)
            i1 = exercice[i0:].index(')') + i0
            pre1 = Affichage(exercice[:i0 + 1])
            post1 = Affichage(exercice[i1:])
            (cor, res, programme) = OperateurPrioritaire(exercice[i0 + 1:i1],
                    niveau, pre + pre1, post + post1, solution)
            suite_exo = exercice[:i0]
            suite_exo.append(res)
            suite_exo.extend(exercice[i1 + 1:])
            return OperateurPrioritaire(suite_exo, programme, pre, post,
                    solution)
        else:
            if nbmul or nbdiv:

                # Priorité à la multiplication et à la division

                if nbmul and not nbdiv:
                    i0 = exercice.index("*")
                elif nbdiv and not nbmul:
                    i0 = exercice.index("/")
                elif exercice.index("*") < exercice.index("/"):
                    i0 = exercice.index("*")
                else:
                    i0 = exercice.index("/")
            else:

                # Il ne reste que des additions et des soustractions

                nbadd = exercice.count("+")
                nbsub = exercice.count("-")
                if nbadd and not nbsub:
                    i0 = exercice.index("+")
                elif nbsub and not nbadd:
                    i0 = exercice.index("-")
                elif exercice.index("+") < exercice.index("-"):
                    i0 = exercice.index("+")
                else:
                    i0 = exercice.index("-")
            pre1 = Affichage(exercice[:i0 - 1])  # Ce qui est avant le calcul en cours
            post1 = Affichage(exercice[i0 + 2:])  # Ce qui est après le calcul en cours
            (l, res, programme) = EffectueCalcul(exercice[i0], exercice[i0 -
                    1], exercice[i0 + 1], pre + pre1, post + post1)
            for i in l:
                solution.append(i)
            suite_exo = exercice[:i0 - 1]
            suite_exo.append(res)
            suite_exo.extend(exercice[i0 + 2:])
            programme = min(programme, niveau)
            return OperateurPrioritaire(suite_exo, programme, pre, post,
                    solution)



def TrouveParentheseInterieure(l):
    """Trouve la position de la parenth\xc3\xa8se la plus \xc3\xa0 l'int\xc3\xa9rieur

    @param l: liste d'op\xc3\xa9rations
    """

    nbpar = l.count('(')
    if nbpar > 1:
        if l[l.index('(') + 1:].index('(') < l[l.index('(') + 1:].index(')'):  # Il existe une parenthèse dans les parenthèses
            return l.index('(') + 1 + TrouveParentheseInterieure(l[l.index('(') +
                    1:])
        else:
            return l.index('(')
    else:
        return l.index('(')


def valeurs_priorites_decimaux(nb, entier=1):  # renvoie les 2 listes contenant les opérateurs et les opérandes.
    listoperateurs = [
        "+",
        "*",
        "-",
        "/",
        '(',
        '(',
        '(',
        '(',
        ')',
        ')',
        ')',
        ')',
        ]
    loperateurs = []
    loperandes = []
    i = 0  #nombre d'opérateurs créés
    p = 0  #nombre de parenthèses ouvertes
    cpt = 0  #compteur pour éviter que le programme ne boucle.
    while i < nb - 1:
        cpt = cpt + 1
        if cpt > 10:  #On recommence
            (cpt, i, p, loperateurs) = (0, 0, 0, [])
        if p:
            if loperateurs[-1] == '(':  # On n'écrit pas 2 parenthèses à suivre
                operateur = listoperateurs[random.randrange(4)]
            else:
                operateur = listoperateurs[random.randrange(12)]
        elif loperateurs == []:

            # On ne commence pas par une parenthèse

            operateur = listoperateurs[random.randrange(4)]
        else:
            operateur = listoperateurs[random.randrange(8)]
        if nb > 3:
            test = ('-*/').find(operateur) >= 0 and loperateurs.count(operateur) < \
                1 or operateur == "+" and loperateurs.count(operateur) < \
                2
        else:
            test = ('-*/+').find(operateur) >= 0 and loperateurs.count(operateur) < \
                1
        if test:

            #On n'accepte pas plus de 1 produit, différence, quotient et de 2 sommes ou parenthèses par calcul.

            if i == 0 or loperateurs[-1] != '(' or ('*/').find(operateur) < \
                0:  #pas de * ou / dans une parenthèse.
                i = i + 1
                loperateurs.append(operateur)
        elif operateur == '(' and (')+').find(loperateurs[-1]) < 0:

            #Il ne peut y avoir de ( après une ) ou après un +

            p = p + 1
            loperateurs.append(operateur)
        elif operateur == ')':
            p = p - 1
            loperateurs.append(operateur)
    while p > 0:
        loperateurs.append(')')
        p = p - 1
    if entier:
        loperandes = [random.randrange(12) + 2 for i in range(nb)]
    else:
        loperandes = [((random.randrange(88) + 12) * 1.0) / 10 for i in
                      range(nb)]
    exercice = [loperandes[0]]
    i = 1
    j = 0
    while i < len(loperandes) or j < len(loperateurs):
        if j < len(loperateurs):
            exercice.append(loperateurs[j])
            j = j + 1
        while j < len(loperateurs) and (loperateurs[j] == '(' or
                loperateurs[j - 1] == ')'):
            exercice.append(loperateurs[j])
            j = j + 1
        if i < len(loperandes):
            exercice.append(loperandes[i])
            i = i + 1
    return exercice


#for i in xrange(1):
#    l=valeurs_priorites_fractions(3, 1)
#    cor,res, programme=OperateurPrioritaire(l,6,pre="", post="",solution=[])
#    while programme<5:
#        l=valeurs_priorites_fractions(3, 1)
#        cor,res,programme=OperateurPrioritaire(l,6,pre="", post="",solution=[])
#    print "$" + Affichage(l)+"$\\par"
#    for i in cor:
#        print "$" + i +"$\\par"




