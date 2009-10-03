# -*- coding: utf-8 -*-

import re

def printlist(liste):
    """Affiche chaque élément d'une liste, ligne par ligne."""
    for element in liste:
        print(element)
    return False

def suppr0(nombre):
    """Supprime le zéro inutile après la virgule d'un float, si c'est possible."""
    if round(nombre, 0) == nombre:
        return int(nombre)
    else:
        return nombre

def suppr0list(liste):
    """Supprime le zéro inutile après la virgule des éléments d'une liste de floats, si c'est possible."""
    for element in liste:
        element = suppr0(element)
    return liste

def decomp3(nombre):
    """Affiche un nombre entier avec les chiffres par 3."""
    i = 0 ## 1
    result = ''
    nombrestr = repr(nombre)
    longueur = len(nombrestr)
    reste = longueur % 3

    while (i < longueur):
        if i == reste:
            caract = ' '
            reste += 3
        else:
            caract = nombrestr[i]
            i += 1
        result += caract

    return result

def ecrire_par3(nombre):
    """Affiche un nombre quelconque avec les chiffres par 3."""
    intvir = re.findall( '(\d+)\.*(\d*)', repr(nombre))

    if (re.findall('\.', repr(nombre)) and ((intvir[0][1]) != '0')):
      secondterm = decomp3(intvir[0][1])
      separateur = ', '
    else:
      secondterm = ''
      separateur = ' '

    return decomp3(intvir[0][0]) + separateur + secondterm

#---------------------------------------------------------------------
# Affichages des nombres décimaux
#---------------------------------------------------------------------
def decimaux(nb, mathenv = 0):
    pattern = re.compile(r"^(-?\d+)\.*(\d*)e?([\+\-]?\d*)$")
    entiere,  decimale,  exposant = pattern.search(str(nb)).groups()
    if exposant:
        if int(exposant) > 0:
            if int(exposant) < len(decimale):
                entiere = entiere + decimale[:int(exposant)]
                decimale = decimale[int(exposant):]
            else:
                entiere = entiere + decimale + "0"*(int(exposant)-len(decimale))
                decimale = ''
        else:
            if -int(exposant) < len(entiere):
                decimale = entiere[len(entiere)+int(exposant):] + decimale
                entiere = entiere[:len(entiere)+int(exposant)]
            else:
                decimale = "0"*(-int(exposant)-len(entiere)) + entiere + decimale
                entiere = "0"
    pattern = re.compile(r"^(-?\d{1,3}?)" + "(\d{3})" * ((len(entiere) - 1) // 3) \
                         + "$")
    partie_entiere = pattern.search(entiere).groups()
    if decimale:
        pattern = re.compile(r"^" + "(\d{3})" * ((len(decimale) - 1)  // 3) + \
                             "(\d{1,3})?$")
        partie_decimale = pattern.search(decimale).groups()
        if mathenv:
            return "{,}".join(("\,".join(partie_entiere),
                               "\,".join(partie_decimale)))
        else:
            return ",".join(("\,".join(partie_entiere),
                             "\,".join(partie_decimale)))
    else:
        return "\,".join(partie_entiere)
