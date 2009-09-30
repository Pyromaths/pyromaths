#!/usr/bin/python
# -*- coding: utf-8 -*-

from pyro_classes import Fractions
import outils
import random
import math

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
            l = ["%s%s%s" % (pre, outils.sepmilliers(nb1 + nb2, 1), post)]
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
            l = ["%s%s%s" % (pre, outils.sepmilliers(nb1 - nb2, 1), post)]
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
            l = ["%s%s%s" % (pre, outils.sepmilliers(nb1 * nb2, 1), post)]
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
                l = ["%s%s%s" % (pre, outils.sepmilliers((nb1 * 1.0) /
                     nb2, 1), post)]
                resultat = (nb1 * 1.0) / nb2
                if resultat - math.floor(resultat) == 0.0:
                    programme = 6
                elif resultat * 100 - math.floor(resultat * 100) == 0.0:
                    programme = 5
                else:
                    programme = 2
    return (l, resultat, programme)


def Affichage(l):
    """\xc3\x89crit une expressions contenant des d\xc3\xa9cimaux et des fractions au format TeX
    
    @param l: liste contenant l'expression [3, '+', 5, '*', 2]
    """

    expr = ""  # résultat
    for i in range(len(l)):  # on parcourt la liste
        if ["+", "-", "*", "/", '(', ')'].count(l[i]):  # Un opérateur
            if l[i] == "*":
                expr = expr + " \\times "
            elif l[i] == "/":
                expr = expr + " \\div "
            elif l[i] == ")" and type(l[i-1]) == type(Fractions(1, 1)):
                expr = expr + " \\big) "
            elif i<len(l)-2 and l[i] == "(":
                if type(l[i+1]) == type(Fractions(1, 1)):
                    expr = expr + " \\big( "
            else:
                expr = expr + " " + l[i] + " "
        elif type(l[i]) == type(Fractions(1, 1)):

            # C'est une fraction

            expr = expr + "%s" % Fractions.TeX(l[i], signe = 0)
        else:

              # C'est un nombre

            expr = expr + "%s" % outils.sepmilliers(l[i], 1)
    return expr


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

#===============================================================================
# Gère le calcul fractionnaire
#===============================================================================


def EffectueSommeFractions(fr1, fr2, s, pre, post):
    if s == "+":
        fr = fr1 + fr2
    else:
        fr = fr1 - fr2
    cor = []
    if fr1.n and fr2.n:
        ppcm = outils.ppcm(fr2.d, fr1.d)
        if abs(fr1.d) - abs(fr2.d):
            cor.append("%s%s%s%s%s" % (pre, Fractions.TeX(fr1, True,
                       coef=ppcm / abs(fr1.d)), s, Fractions.TeX(fr2,
                       True, coef=ppcm / abs(fr2.d)), post))
        if pre.rstrip().endswith('(') and post.lstrip().startswith(')'):
            pre = pre.rstrip()[:len(pre.rstrip()) - 1]
            post = post.lstrip()[1:]
        cor.append("%s%s%s" % (pre, Fractions.TeX(fr, True), post))
        if fr.n:
            frs = Fractions.simplifie(fr)
            if abs(frs.n) != abs(fr.n):
                cor.append("%s%s%s" % (pre, Fractions.TeX(frs, True,
                           coef=fr.d / frs.d), post))
                cor.append("%s%s%s" % (pre, Fractions.TeX(frs, True),
                           post))
    else:
        cor.append("%s%s%s" % (pre, Fractions.TeX(fr, True), post))
    return cor


def EffectueProduitFractions(fr1, fr2, pre, post):
    fr1s = Fractions.simplifie(fr1)
    fr2s = Fractions.simplifie(fr2)
    cor = []
    if fr1.n and fr2.n:
        if abs(fr1s.d) < abs(fr1.d) or abs(fr2s.d) < abs(fr2.d):
            cor.append("%s%s \\times %s%s" % (pre, Fractions.TeXSimplifie(fr1),
                       Fractions.TeXSimplifie(fr2), post))
            cor.append("%s%s \\times %s%s" % (pre, Fractions.TeX(fr1s,
                       True), Fractions.TeX(fr2s, True), post))
        fr = fr1s * fr2s
        frs = Fractions.simplifie(fr)
        if abs(frs.d - fr.d):
            cor.append("%s%s%s" % (pre, Fractions.TeXProduit(fr1s, fr2s),
                       post))
        cor.append("%s%s%s" % (pre, Fractions.TeX(frs, True), post))
    else:
        cor.append("%s%s%s" % (pre, Fractions.TeX(Fractions(0), True),
                   post))
    return cor


def EffectueQuotientFractions(fr1, fr2, pre, post):
    fr2 = Fractions(1, 1) / fr2
    cor = ["%s%s \\times %s%s" % (pre, Fractions.TeX(fr1, True),
           Fractions.TeX(fr2, True), post)]
    cor.extend(EffectueProduitFractions(fr1, fr2, pre, post))
    return cor


