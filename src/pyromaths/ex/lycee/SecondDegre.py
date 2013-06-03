# -*- coding:utf8 -*-

from random import randint, choice
from math import sqrt
from pyromaths.classes.Racine import RacineDegre2
from pyromaths.outils.Affichage import tex_coef, TeX

a = choice(range(1,11)+range(-11,-1))
s1 = randint(-8,8)
s2 = randint(-12,12)

def affiche_formes(a,s1,s2):
    """Affiche les formes canoniques et développées du polynôme."""
    if s1:
        canonique = u"$%s(x %s)^2 %s$" % (tex_coef(a," "),tex_coef(-s1,"",bplus=1),tex_coef(s2,"",bplus=1))
        develop = u"$%s x^2 %s x %s$" % (tex_coef(a," "),tex_coef(2*a*s1,"",bplus=1),tex_coef(a*s1*s1+s2,"",bplus=1))
    else:
        canonique = u"$%s x^2 %s$" % (tex_coef(a," "),tex_coef(s2,"",bplus=1))
        develop = u"$%s x^2 %s$" % (tex_coef(a," "),tex_coef(a*s1*s1+s2,"",bplus=1))
    return [develop,canonique]

def orientation(a):
    """Détermine l'orientation d'une parabole suivant le signe de son coefficient dominant."""
    if a > 0:
        return u"La parabole de la fonction $f$ est tournée vers le haut."
    else :
        return u"La parabole de la fonction $f$ est tournée vers le bas."

def cherche_racines(a,s1,s2):
    """Cherche les racines d'un polynôme du second degré, et fourni une liste de racines."""
    if s2 == 0:
        result = u"Une racine double : $" + str(s1) + u"$."
        racines = [s1]
    elif a*s2 < 0:
        racines = [RacineDegre2(s1*abs(a),abs(a),-1,abs(a*s2)),RacineDegre2(s1*abs(a),abs(a),1,abs(a*s2))]
        result = u"Il y a deux racines :\n"
        result += u"Première racine : $" + str(racines[0].simplifie()) + u"$.\n"
        result += u"Seconde racine : $" + str(racines[1].simplifie()) + u"$.\n"
    else:
        result = u"Aucune racine."
        racines = []
    return [result,racines]

def variations(a,s1,s2):
    """Affiche les variations d'une fonction du second degré."""
    if a > 0:
        result = u"La courbe est décroissante sur l'intervalle $]-\infty,%s[$, \
atteint un minimum qui vaut %s en %s puis est croissante sur l'intervalle $]%s;+\infty[$." % (s1,s2,s1,s1)
    else:
        result = u"La courbe est croissante sur l'intervalle $]-\infty,%s[$, \
atteint un maximum qui vaut %s en %s puis est décroissante sur l'intervalle $]%s;+\infty[$." % (s1,s2,s1,s1)    
    return result

def signe(a,racines):
    """Affiche le signe d'une fonction du second degré.""" # Tableau de signes ?
    if a > 0:
        if len(racines)==2:
            result = u"La fonction est positive dans les intervalles $]-\infty;%s[$ et $]%s;+\infty[$, \
et négative dans l'intervalle $]%s;%s[$." % (str(racines[0]),str(racines[1]),str(racines[0]),str(racines[1]))
        elif len(racines)==1:
            result = u"La fonction est toujours positive et s'annule en %s." % (str(racines[0]))
        else:
            result = u"La fonction est toujours strictement positive."
    else:
        if len(racines)==2:
            result = u"La fonction est négative dans les intervalles $]-\infty;%s[$ et $]%s;\+infty[$, \
et positive dans l'intervalle $]%s;%s[$." % (str(racines[0]),str(racines[1]),str(racines[0]),str(racines[1]))
        elif len(racines)==1:
            result = u"La fonction est toujours négative et s'annule en %s." % (str(racines[0]))
        else:
            result = u"La fonction est toujours strictement négative."
    return result

def factorisation(a,racines):
    """Fourni la forme factorisée d'un polynôme du second degré."""
    if len(racines)>1:
        result = u"La forme factorisée de la fonction est : $f(x)=%s(x-%s)(x-%s)$" % (tex_coef(a," "),racines[0].simplifie(),racines[1].simplifie())
    elif len(racines)==1:
        result = u"La forme factorisée de la fonction est : $f(x)=%s(x-%s)^2$" % (tex_coef(a," "),racines[0])
    else:
        result = u"Comme le discriminant est négatif, il n'y a pas de racine, donc pas de factorisation possible."
    return result

def correction_forme_canonique(a,s1,s2):
    """Prépare la factorisation complète du polynôme pour obtenir la forme canonique."""
    if s1 == 0 and s2 == 0:
        result = u"$%s x^2 %s = %s (x - 0)^2 + 0$" % (tex_coef(a," "),tex_coef(s2,"",bplus=1),tex_coef(a," "))
    elif s1 == 0:
        result = u"$%s x^2 %s = %s (x - 0)^2 %s$" % (tex_coef(a," "),tex_coef(s2,"",bplus=1),tex_coef(a," "),tex_coef(s2,"",bplus=1))
    else:
        result = u"$\\begin{array}[rcl]\n" # Problème si s1 = 0
        result += u"%sx^2 %s x %s & = & %s[x^2 %s x]%s\n" % (tex_coef(a," "),tex_coef(-2*a*s1,"",bplus=1),tex_coef(a*s1**2+s2,"",bplus=1),a,tex_coef(-2*s1,"",bplus=1),tex_coef(a*s1**2+s2,"",bplus=1))
        result += u" & = & %s[(x %s)^2-%s]%s\n" % (tex_coef(a," "),tex_coef(-s1,"",bplus=1),s1**2,tex_coef(a*s1**2+s2,"",bplus=1))
        result += u" & = & %s (x %s)^2 %s %s\n" % (tex_coef(a," "),tex_coef(-s1,"",bplus=1),tex_coef(-a*s1**2,"",bplus=1),tex_coef(a*s1**2+s2,"",bplus=1))
        result += u" & = & %s (x %s)^2 %s\n" %(tex_coef(a," "),tex_coef(-s1,"",bplus=1),tex_coef(s2,"",bplus=1))
        result += u"\\end{array}$\n"
    return result

def FormeCanonique():
    """Compléter"""

    global a, s1, s2
    formes = affiche_formes(a,s1,s2)
    print formes[0]
    print correction_forme_canonique(a,s1,s2)
    print formes[1]
    print orientation(a)
    racines = cherche_racines(a,s1,s2)
    print racines[0]
    print signe(a, racines[1])
    print variations(a,s1,s2)
    print factorisation(a,racines[1])
    cor = exo = ["1","2","3"]
    return exo, cor

FormeCanonique.description = u"Forme canonique"
