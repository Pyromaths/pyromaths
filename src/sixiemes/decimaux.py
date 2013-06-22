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

import random
from ..outils import Affichage, Arithmetique
#===============================================================================
# Écrire un nombre en lettres ou en chiffres
#===============================================================================


def NombreEnLettres(n, France=True):
    unite = {
        1: "un",
        2: 'deux',
        3: 'trois',
        4: 'quatre',
        5: 'cinq',
        6: 'six',
        7: 'sept',
        8: 'huit',
        9: 'neuf',
        10: 'dix',
        11: 'onze',
        12: 'douze',
        13: 'treize',
        14: 'quatorze',
        15: 'quinze',
        16: 'seize',
        17: 'dix-sept',
        18: 'dix-huit',
        19: 'dix-neuf',
        }
    dizaineF = {2: 'vingt', 3: 'trente', 4: 'quarante', 5: 'cinquante',
                6: 'soixante', 7: "", 8: 'quatre-vingt', 9: ""}
    dizaineB = {2: 'vingt', 3: 'trente', 4: 'quarante', 5: 'cinquante',
                6: 'soixante', 7: 'septante', 8: 'octante', 9: 'nonante'}
    coefs = {0: 'cent', 1: 'mille', 2: 'million', 3: 'milliard'}
    result = ""

  # Cas particulier de zéro
    if n == 0:
        result = u'zéro'
    else:
        coef = 0

        while n > 0:

        # Récupération de l'unité du bloc de trois chiffres en cours

            u = n % 10
            n = n // 10

        # Récupération de la dizaine du bloc de trois chiffres en cours

            d = n % 10
            n = n // 10
        # Traitement des dizaines

            temp = ""

        # Passage sur la dizaine inférieure pour 10 à 19
        # et pour 70-79 90-99 dans le cas de la France

            if d == 1 or (d == 7 or d == 9) and France:
                d = d - 1
                u = u + 10
            if d > 1:
                if France:
                    if n:
                        temp = '-' + dizaineF[d]
                    else:
                        temp = dizaineF[d]

            # Ajout du cas particulier de 'et' entre la dizaine et 1

                    if d < 8 and (u == 1 or u == 11):
                        temp = temp + '-et'
                else:
                    if n:
                        temp = '-' + dizaineB[d]
                    else:
                        temp = dizaineB[d]

              # Ajout du cas particulier de 'et' entre la dizaine et 1

                    if u == 1:
                        temp = temp + '-et'

        # ajout du texte de l'unité

            if u > 0 and (d or n):
                temp = temp + '-' + unite[u]
            elif u > 0:
                temp = unite[u]

        # ajout du 's' à Quatre-vingt si rien ne suit
        #if (result == '') and (d == 8) and (u == 0) and France : result = 's'

            if d == 8 and u == 0 and France:
                temp = temp + 's'
            result = temp + result


        # Récupération de la centaine du bloc de trois chiffres en cours

            c = n % 10
            n = n // 10
            if c > 0:
                temp = ""
                if c > 1 and n:
                    temp = '-' + unite[c]
                elif c > 1:
                    temp = unite[c]
                if c == 1 and not n:
                    temp = coefs[0]
                else:
                    temp = temp + '-' + coefs[0]

          # Traitement du cas particulier du 's' à cent si rien ne suit

                if result == "" and c > 1:
                    result = 's'
                result = temp + result

        # Traitement du prochain groupe de 3 chiffres

            if n > 0:
                coef = coef + 1
                i = n % 1000
                if i > 1 and coef > 1:
                    result = 's' + result

          # Traitement du cas particulier 'mille' ( non pas 'un mille' )

                if i == 1 and coef == 1:
                    n = n - 1
                    result = coefs[coef] + result
                elif i > 0:

                    result = '-' + coefs[coef] + result
    return result

def NombreEnLettres_es(n):
    unite = {
        1: 'uno',
        2: 'dos',
        3: 'tres',
        4: 'cuatro',
        5: 'cinco',
        6: 'seis',
        7: 'siete',
        8: 'ocho',
        9: 'nueve',
        10: 'diez',
        11: 'once',
        12: 'doce',
        13: 'trece',
        14: 'catorce',
        15: 'quince',
        16: u'dieciséis',
        17: 'diecisiete',
        18: 'dieciocho',
        19: 'diecinueve',
        20: 'veinte',
        21: 'veintiun',             #Está bien así, NO CORREGIR
        22: u'veintidós',
        23: u'veintitrés',
        24: 'veinticuatro',
        25: 'veinticinco',
        26: u'veintiséis',
        27: 'veintisiete',
        28: 'veintiocho',
        29: 'veintinueve',
        }
    dizaineE = {3: 'treinta', 4: 'cuarenta', 5: 'cincuenta',
                6: 'sesenta', 7: 'setenta', 8: 'ochenta', 9: 'noventa'}
    coefs = {0: 'cien', 1: 'mil', 2: 'mill', 3:'mil'}
    coefc = {0: 'un', 1: 'ciento', 2: 'dosci', 3: 'tresci', 4:'cuatroci', 5:'quini',
                6: 'seisci', 7: 'seteci', 8: 'ochoci', 9: 'noveci'}
    result = ""

  # Cas particulier de zéro
    if n == 0:
        result = u'cero'
    else:
        coef = 0
        
        while n > 0:

        # Récupération de l'unité du bloc de trois chiffres en cours

            u = n % 10
            n = n // 10

        # Récupération de la dizaine du bloc de trois chiffres en cours

            d = n % 10
            n = n // 10
        # Traitement des dizaines

            temp = ""

        # Passage sur la dizaine inférieure pour 10 à 19
        # et pour 70-79 90-99 dans le cas de la France

            if d == 1:                  # Escribe los nº del 10 al 19 de la tabla
                d = d - 1
                u = u + 10
            if d == 2:                  # Escribe los nº del 20 al 21 de la tabla
                d = d - 1
                u = u + 20
            if d > 2:

            # Ajout du cas particulier de 'et' entre la dizaine et 1

                    if n:               # Escribe el resto del 30 al 99
                        temp = ' ' + dizaineE[d]    # Añade espacio si es > 100
                    else:
                        temp = dizaineE[d]

        # ajout du texte de l'unité

            if u > 0 and d > 2:                         # Añade "y" de los nº entre 30 a 99
                if u == 1 and coef > 0:                 # Usa "un" en lugar de "uno"
                    temp = temp + ' y ' + coefc[0]
                else:
                    temp = temp + ' y ' + unite[u]
            elif u > 0 and n:                           # Añade espacio si es > 100
                if u == 21 and coef == 0: # Usa "veintiuno" en lugar de "veintiun" si <1000
                    temp = temp + ' ' + unite[u] + 'o'
                elif u == 1 and (coef > 0 and coef < 4):    # Usa "un" en lugar de "uno"
                    if coef == 3:
                        temp = temp                         # Usa "mil millones" en lugar de "un mil"
                    else:
                        temp = ' ' + coefc[0]
                else:
                    temp = temp + ' ' + unite[u]
            elif u == 21 and d == 1 and coef == 0:  # Usa "veintiuno" cuando es 21
                temp = unite[u] + 'o'
            elif u == 1 and d == 0 and coef > 0:  # Usa "un" son numeros > 1000
                temp = coefc[0]
            elif u > 0:
                temp = unite[u]

            result = temp + result


        # Récupération de la centaine du bloc de trois chiffres en cours

            c = n % 10
            n = n // 10
            if c > 0:
                temp = ""
                if c == 1 and not d and not u:  # Usa "cien" en lugar de "un cien"
                    temp = coefs[0]
                elif c == 1:                      # Usa "ciento" para >100
                    temp = coefc[1]
                else:                           # Compone los nº > 200
                    temp = coefc[c] + 'entos'

          # Traitement du cas particulier du 's' à cent si rien ne suit

                if n > 0 :                      # Añade espacio si es > 1000
                    result = ' ' + temp + result
                else:
                    result = temp + result

        # Traitement du prochain groupe de 3 chiffres

            if n > 0:
                coef = coef + 1
                i = n % 1000

          # Traitement du cas particulier 'mille' ( non pas 'un mille' )

                if coef == 1 and i==1:        # No añade espacio en "mil"
                    n = n - 1
                    if n == 0:
                        result = coefs[coef] + result
                    else:
                        result = ' ' + coefs[coef] + result
                elif coef == 2:      # Usa "millones" en lugar de "millón"
                    if i == 1 and n == 1:
                        result = ' ' + coefs[coef] + u'ón' + result
                    else:
                        result = ' ' + coefs[coef] + 'ones' + result
                elif i == 1 and coef == 3:      # No añade espacio en "mil millones"
                    result = coefs[coef] + result
                elif i > 0:
                    result = ' ' + coefs[coef] + result

    return result

def nombreATrouver():
    """a contient la liste des nombres à créer où il peut ne pas y avoir de
    centaines, de centaines de milliers, d'unités ou de milliers"""

    a = [random.randrange(100) + random.randrange(1000) * 10 ** 3,
         random.randrange(1000) + random.randrange(100) * 10 ** 3,
         random.randrange(1000) * 10 ** 3, random.randrange(1000)]
    (lnb, list) = ([], [])
    for i in range(4):
        lnb.append(random.randrange(1, 1000) * 10 ** 6 + a[i])
    for i in range(4):
        n = a[i]
        if n % 1000:  # il y a des unités dans le nombre
            e = random.randrange(1, 4)
            lnb.append(n * 10 ** (-e))
        else:
            e = random.randrange(4, 7)
            lnb.append(n * 10 ** (-e))
    for i in range(8):
        list.append(lnb.pop(random.randrange(len(lnb))))
    return list

def EcritNombreDecimal(n):
    txt = ""
    if n != int(n):
        #n n'est pas un nombre entier
        (e, d) = str(n).split('.')
        (e, d) = (int(e), int(d))
    else:
        (e, d) = (int(n), 0)
    if not d:
        txt = NombreEnLettres(e)
    elif e:
        txt = NombreEnLettres(e)
    if d:
        partieDec = [u" dixième", u" centième", u" millième"]
        if txt.rfind("un") == len(txt) - 2:

        # le texte se finit par un. On l'accorde en genre avec unité

            txt = txt + "e"
        if e == 1:
            txt = txt + u' unité et '
        if e > 1:
            txt = txt + u' unités et '
        txt = txt + NombreEnLettres(d) + partieDec[len(str(n).split('.')[1]) -
                1]
        if d > 1:
            txt = txt + 's'
    return txt

def EcritNombreDecimal_es(n):
    txt = ""
    if n != int(n):
        #n n'est pas un nombre entier
        (e, d) = str(n).split('.')
        (e, d) = (int(e), int(d))
    else:
        (e, d) = (int(n), 0)
    if not d:
        txt = NombreEnLettres_es(e)
    elif e:
        txt = NombreEnLettres_es(e)
    if d:
        partieDec = [u" décima", u" centésima", u" milésima"]
        if e == 1:
            txt = txt + u' unidad con '
        if e > 1:
            txt = txt + u' unidades con '
        txt = txt + NombreEnLettres_es(d) + partieDec[len(str(n).split('.')[1]) -
                1]
        if d > 1:
            txt = txt + 's'
        txt = txt.replace("uno", "una")     # Cambio a femenino para decimales
        txt = txt.replace("un ", "una ")    # Cambio a femenino para decimales
        txt = txt.replace("tos", "tas")    # Cambio a femenino para decimales
    return txt

def EcritEnChiffre(exo, cor, lang = ""):
    lnb = nombreATrouver()
    for i in range(len(lnb)):
        exo.append("\\item " + eval('EcritNombreDecimal'+lang+'(lnb[i])') +
                 _(" : \\dotfill"))
        cor.append("\\item " + eval('EcritNombreDecimal'+lang+'(lnb[i])') +
                   " : ")
        cor.append(Affichage.decimaux(lnb[i], 0) + '')


def EcritEnLettre(exo, cor, lang = ""):
    lnb = nombreATrouver()
    for i in range(8):
        exo.append("\\item " + Affichage.decimaux(lnb[i], 0) +
                 _(" : \\dotfill"))
        cor.append("\\item " + Affichage.decimaux(lnb[i], 0) +
                " : ")
        cor.append(eval('EcritNombreDecimal'+lang+'(lnb[i])') + '')


def EcrireNombreLettre(langue):
    if langue == "fr" or langue == "":
        lang = ""
    else:
        lang = "_" + langue
        try:
            eval('EcritNombreDecimal'+lang+'(1)')
        except NameError:
            lang = ""

    exo = ["\\exercice", "\\begin{enumerate}",
            _(u'\\item Écrire en chiffres les nombres suivants.'),
            '\\begin{enumerate}']
    cor = ["\\exercice*", "\\begin{enumerate}",
            _(u'\\item Écrire en chiffres les nombres suivants.'),
            '\\begin{enumerate}']

    EcritEnChiffre(exo, cor, lang)

    exo.append('\\end{enumerate}')
    exo.append(_(u'\\item Écrire en lettres les nombres suivants (sans utiliser le mot ``virgule").'))
    exo.append('\\begin{enumerate}')
    cor.append('\\end{enumerate}')
    cor.append(_(u'\\item Écrire en lettres les nombres suivants (sans utiliser le mot ``virgule").'))
    cor.append('\\begin{enumerate}')

    EcritEnLettre(exo, cor, lang)

    exo.append('\\end{enumerate}')
    exo.append('\\end{enumerate}')
    cor.append('\\end{enumerate}')
    cor.append('\\end{enumerate}')

    return (exo, cor)

#===============================================================================
# Conversions
#===============================================================================

units = [_("L"), _("m"), _("g")]
division = [_("k"), _("h"), _("da"), "", _("d"), _("c"), _("m")]

#paramétrage des flèches : mofifie le paramétrage par défaut de PSTricks  s'il n'est pas limité par un environnement ou {groupe}
## nodesepA = -1.5mm  : décale le départ de la flèche
## linewidth = 0.6pt  : épaisseur de la flèches
## linestyle = dotted : style pointillé
## vref = -0.8mm      : décale la flèche vers le bas, sous les chiffres
PSSET_FLECHE = '\\psset{nodesepA = -1.5mm, linewidth = 0.6pt, linestyle = dotted, vref = -0.8mm}'


def Conversions(n):
    if n == 1:#Conversions de L, m ou g
        #le module sixiemes.sixiemes va appeler Conversions(1)()
        return tex_units

    #exo_conversion(exo, cor, 1) #le choix des valeurs prises, l'absence de grammes et litres ne rendent pas cette rédaction pertinente
    else:  #conversions de m² ou m³
        return exo_conversion(n)

def valeurs_units():
    """
    renvoie les valeurs pour les conversions d'unités
    """

    a = Arithmetique.valeur_alea(101, 999)
    p = random.randrange(-2, 0)
    unit = random.randrange(3)
    if unit:
        #mètres ou grammes, on peut utiliser les k
        imax = 7
    else:
        #Litres, donc pas de kL
        imax = 6

    div0 = random.randrange(imax + p)

    while 1:
        div1 = random.randrange(imax)
        if div0 != div1:
            break

    if not unit: #Litres, donc pas de kL donc on décale d'un rang
        div0, div1 = div0 + 1, div1 + 1

    return (a, p, unit, div0, div1)
        #101< a <999 ex a = 245
        #p = {-2,-1} donne 2,45 ou 24,5
        #unit = {0, 1, 2} => {L, m, g}
        #div0 unité 0
        #div1 unité converti

def tex_units():
    """
    Écrit l'exercice sur les conversions d'unités et le corrigé au format
    LaTeX
    @param exo: fichier exercices
    @param cor: fichier corrige
    """

    exo = ["\\exercice", _('Effectuer les conversions suivantes :'),
            '\\begin{multicols}{3}\\noindent', '\\begin{enumerate}']
    cor = ["\\exercice*",
            #paramétrage des flèches, ce paramétrage est limité à l'exercice
            # et ne modifie pas le paramétrage PSTricks du document car sa portée est limité par le groupe ouvert par "{"
           "{",
            PSSET_FLECHE,
           _('Effectuer les conversions suivantes :'),
            '\\begin{multicols}{2}\\noindent', '\\begin{enumerate}']

    #Construit les 6 questions de l'exercice
    for i in range(6):
        (a, p, unit, div0, div1) = valeurs_units()
        if unit:
            u = tuple([units[unit] for i in range(7)])
        else:
            u = tuple([units[unit] for i in range(6)])
        nb0 = Affichage.decimaux(a * 10 ** p, 0)
        nb1 = Affichage.decimaux(a * 10 ** ((p + div1) - div0),
                0)
        exo.append(_("\\item %s~%s%s=\dotfill~%s%s") % (nb0, division[div0],
                 units[unit], division[div1], units[unit]))
        cor.append("\\item %s~%s%s=%s~%s%s\\par" % (nb0, division[div0],
                 units[unit], nb1, division[div1], units[unit]))
        nblist = [nb0[i] for i in range(len(nb0))]
        if nblist.count(','):
            chf_unite = nblist.index(',') - 1
            nblist.pop(chf_unite + 1)
        else:
            chf_unite = len(nblist) - 1

        tex_tableau(cor, div0, div1, u, nblist, chf_unite)

        cor.append("\\end{tabular}")
        cor.append("\\ncline{->}{virg0}{virg1}")

    exo.append('\\end{enumerate}')
    exo.append('\\end{multicols}')
    cor.append('\\end{enumerate}')
    cor.append('\\end{multicols}')
    #ferme le groupe limitant la portée de PSSET_FLECHE
    cor.append('{')
    return (exo, cor)


def tex_tableau(cor, div0, div1, u, nblist, chf_unite):
    """tableau de conversion pour les unités simples : L, g ou m"""

    #Si len(u) == 6, on a des Litres, on ne doit pas avoir la colonne kL
    if len(u) == 6:
        cor.append("\\begin{tabular}{c|c|c|c|c|c}")
        cor.append(_("h%s & da%s & %s & d%s & c%s & m%s \\\\ \\hline") %u )
        #décale d'une colonne pour supprimer kL
        delta = 1
        div0 = div0 - 1
        div1 = div1 - 1

    else:
        cor.append("\\begin{tabular}{c|c|c|c|c|c|c}")
        cor.append(_("k%s & h%s & da%s & %s & d%s & c%s & m%s \\\\ \\hline") % u)
        #ne supprime pas le kg, km
        delta = 0
    for i in range(-div0 + chf_unite):
        tmp = nblist.pop(0)
        nblist[0] = tmp + nblist[0]

    for i in range(div0 - chf_unite):
        nblist.insert(0, '0')


    for i in range(-len(u) + len(nblist)):
        tmp = nblist.pop(7)
        nblist[6] = nblist[6] + tmp

    #les zéros à droites des chiffres significatifs
    for i in range(len(u) - len(nblist)):
        nblist.append('0')

    #place les \nodes et la virgule dans le tableau
    nblist[div0] =  "%s\\Rnode{virg0}{\\ }"%(nblist[div0])
    nblist[div1] = "{%s\\Rnode{virg1}{\\textcolor{red}{ \\LARGE ,}}}"%(nblist[div1])

    #ajoute au tabular la ligne avec 6 ou 7 colonnes
    cor.append(("%s "+("& %s"*(6-delta))) % tuple(nblist))



def exo_conversion(exposant):
    """construit l'exercice de conversion d'unité d'aire ou de volume
    exposant 2 pour m²
    exposant 3 pour m³"""

    exo = ["\\exercice", _('Effectuer les conversions suivantes :'),
            '\\begin{multicols}{3}\\noindent', '\\begin{enumerate}']
    cor = ["\\exercice*",
            #la portée de \psset est par le group ouvert par "{"
            "{",
            PSSET_FLECHE,
            '\\def\\virgule{\\textcolor{red}{ \\LARGE ,}}',
            _('Effectuer les conversions suivantes :'),
            '\\begin{multicols}{2}\\noindent', '\\begin{enumerate}']

    #ajoute le ² ou ³ si nécessaire
    str_exposant=(u"^%s"%(exposant))*(exposant > 1)

    u = tuple([division[i]+"m%s"%str_exposant for i in range(7)])
    entete_tableau = ((" \\multicolumn{%s}{c|}"%exposant +"{$\\rm %s$} &")*6 +"\\multicolumn{%s}{c}"%exposant+"{$\\rm %s$}" )%u
    ligne_tab = []

    for i in range(6):
        #imprime la correction et sauvegarde la ligne et la flèche pour le tableau imprimé ensuite
        ligne_tab += tex_conversion(exo, cor,exposant, u) + ["\\ncline{->}{virg0}{virg1} \\\\"]

    #ferme la correction et l'énoncé
    cor.append('\\end{enumerate}')
    cor.append('\\end{multicols}')
    exo.append('\\end{enumerate}')
    exo.append('\\end{multicols}')

    #impression du tableau et des lignes sauvegardées précédemment
    cor.append("\\begin{tabular}{*{%s}{p{3.5mm}|}p{3.5mm}}"%(exposant*7-1))
    cor.append(entete_tableau + "\\\\ \\hline")
    #ajoute les lignes affichant les conversions
    cor += ligne_tab
    cor.append("\\end{tabular}")
    #ferme le groupe dans lequel PSSET_FLECHE portait
    cor.append("}")
    #C'est fini
    return (lambda: (exo, cor))


def tex_conversion(exo, cor, exposant, u):
    """Écrit une question sur les conversions d'unités d'aires ou de volume
    et le corrigé au format LaTeX
    @param exo: fichier exercices
    @param cor: fichier corrige
    exposant = 2 ou 3 pour les aires ou les volumes
    """

    a = random.randint(101,999)
    p = random.randint(-2,-1)
    while True:
        (div0,div1)=(random.randrange(6),random.randrange(7),)
        #Pas de mm³ par ce que ça sort du tableau
        if (div0-div1) in [-2,-1,1,2]:
            #pas trop loin car ça fait de très longs nombres
            break
    nb0 = a * 10 ** p
    nb1 = nb0 * 10 ** ( exposant * ( div1- div0))

    exo.append(_("\\item $\\unit[%s]{%s}=\\unit[\\dotfill]{%s}$")%
            (Affichage.decimaux(nb0), u[div0], u[div1]))
    cor.append("\\item $\\unit[%s]{%s}=\\unit[%s]{%s}$\\vspace{1ex}\\par" %
            (Affichage.decimaux(nb0), u[div0],
                Affichage.decimaux(nb1), u[div1]))

    return tex_tableau_conversion(div0, div1, nb0, u, exposant)


def tex_tableau_conversion(div0, div1, nb0, u, exposant):
    nb_dict = nbre_to_dict(nb0,div0,div1,exposant)
    nblist = [str(nb_dict.get(i,"")) for i in range(7*exposant)]
    nblist[exposant*(div0 + 1)-1] =  "%s\\Rnode{virg0}{\\ }"% nb_dict.get(exposant*(div0+1)-1,"0")
    nblist[exposant*(div1 + 1)-1] = "{%s\\Rnode{virg1}{\\virgule}}"% nb_dict.get(exposant*(div1+1)-1,"0")
    return [("%s " + "& %s"*(7*exposant-1)) % tuple(nblist)]


def nbre_to_dict(nbre ,div0,div1,exposant):
    #exposant peut être 2 ou 3 pour les m² ou les m³
    nbre = int(round(nbre*100))
    nb_dict = {}
    for i in range(min(exposant*(div0+1),exposant*(div1+1))-1,max(exposant*(div0+1),exposant*(div1+1))):
            nb_dict[i] = "\\textcolor{red}{0}"
    curseur = 1+exposant*(div0+1)
    while nbre % 10 == 0:
        nbre = nbre / 10
        curseur -= 1
    while nbre > 0:
        chiffre = nbre % 10
        nbre = (nbre-chiffre)/10
        nb_dict[curseur] = "\\textcolor{blue}{%s}"%chiffre
        curseur -= 1
    return nb_dict


#===============================================================================
# Placer une virgule
#===============================================================================

valeurs = [_("milliers"), _("centaines"), _("dizaines"), _(u"unités"),
           _(u"dixièmes"), _(u"centièmes"), _(u"millièmes")]


def valeurs_decimaux():
    """
    Choisit les valeurs
    """

    nb = 0
    chiffres = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    for i in range(6):
        nb = nb + chiffres.pop(random.randrange(len(chiffres))) * 10 ** \
            i
    return nb


def tex_place_virgule(exo, cor):
    """
    Écrit un exercices demandant de placer une virgule dans un nombre.
    @param exo: fichier exerices
    @param cor:fichier corrigé
    """

    valeurs_index = [0, 1, 2, 3, 4, 5, 6]
    nb = valeurs_decimaux()
    exo.append(_(u"Placer une virgule (en ajoutant éventuellement des zéros) dans\
            le nombre %s de telle sorte que :") % nb)
    exo.append('\\begin{enumerate}')
    cor.append(_(u"Placer une virgule (en ajoutant éventuellement des zéros) dans\
            le nombre %s de telle sorte que :") % nb)
    cor.append('\\begin{enumerate}')
    for i in range(6):
        dec = [str(nb)[i] for i in range(len(str(nb)))]
        index_dec = random.randrange(6)
        index_valeurs = valeurs_index.pop(random.randrange(len(valeurs_index)))
        exo.append(_(u"\\item le chiffre %s soit le chiffre des %s : ") \
                 % (dec[index_dec], valeurs[index_valeurs]))
        cor.append(_(u"\\item le chiffre %s soit le chiffre des %s : ") \
                 % (dec[index_dec], valeurs[index_valeurs]))
        resultat = ecrit_nombre_decimal(dec, (index_dec + 4) -
                index_valeurs)
        exo.append(_('\\dotfill'))
        cor.append(Affichage.decimaux(resultat, 0) + '')
    exo.append('\\end{enumerate}')
    cor.append('\\end{enumerate}')


def ecrit_nombre_decimal(dec, index):
    """
    Renvoie une chaine de caractère représentant le nombre dec avec la
    virgule à la place index.
    Ajoute les zéros nécessaires.
    @param dec: décomposition d'un nombre entier
    @param index: place de la virgule dans la liste dec
    """

    if index < 1:
        dec.insert(0, '0')
        dec.insert(1, '.')
        for i in range(-index):
            dec.insert(2, '0')
    elif index < len(dec):
        dec.insert(index, '.')
    else:
        for i in range(index - len(dec)):
            dec.append('0')
    strnb = ""
    for i in range(len(dec)):
        strnb = strnb + dec[i]
    return strnb


def PlaceVirgule():
    exo = ["\\exercice"]
    cor = ["\\exercice*"]

    tex_place_virgule(exo, cor)
    return (exo, cor)

#===============================================================================
#    Écriture fractionnaire
#===============================================================================


def valeurs_frac():
    n1 = random.randrange(11, 10000)
    p1 = random.randrange(1, 4)
    return (n1, p1)


def choix_trou_frac(exo, cor, n1, p1):
    i = random.randrange(3)
    p2 = random.randrange(2)  #sert à compliquer un peu l'exercice
    if i > 1:
        exo.append(_('\\item $\\cfrac{%s}{%s}=\\ldots$') %
                (Affichage.decimaux(n1 * 10 ** p2),
                    Affichage.decimaux(10 ** (p1 + p2))))
        cor.append('\\item $\\cfrac{%s}{%s}=\\mathbf{%s}$' %
                (Affichage.decimaux(n1 * 10 ** p2),
                    Affichage.decimaux(10 ** (p1 + p2)),
                    Affichage.decimaux(n1 * 10 ** (-p1), 1)))
    elif i > 0:
        exo.append(_('\\item $\\cfrac{%s}{\ldots}=%s$') %
                (Affichage.decimaux(n1 * 10 ** p2),
        Affichage.decimaux(n1 * 10 ** (-p1), 1)))
        cor.append('\\item $\\cfrac{%s}{\\mathbf{%s}}=%s$' %
                (Affichage.decimaux(n1 * 10 ** p2),
        Affichage.decimaux(10 ** (p1 + p2)),\
                Affichage.decimaux(n1 * 10 ** (-p1), 1)))
    else:
        exo.append(_('\\item $\\cfrac{\ldots}{%s}=%s$') %
                (Affichage.decimaux(10 ** (p1 + p2)),
        Affichage.decimaux(n1 * 10 ** (-p1), 1)))
        cor.append('\\item $\\cfrac{\\mathbf{%s}}{%s}=%s$' %
                (Affichage.decimaux(n1 * 10 ** p2),
                    Affichage.decimaux(10 ** (p1 + p2)),
                    Affichage.decimaux(n1 * 10 ** (-p1), 1)))

def tex_frac(exo, cor):
    for i in range(6):
        (nombre, puissance) = valeurs_frac()
        choix_trou_frac(exo, cor, nombre, puissance)


def EcritureFractionnaire():
    exo = ["\\exercice", _(u"Compléter :"), '\\begin{multicols}{3}\\noindent',
            '\\begin{enumerate}']
    cor = ["\\exercice*", _(u"Compléter :"), '\\begin{multicols}{3}\\noindent',
            '\\begin{enumerate}']

    tex_frac(exo, cor)

    exo.append('\\end{enumerate}')
    exo.append('\\end{multicols}')
    cor.append('\\end{enumerate}')
    cor.append('\\end{multicols}')
    return (exo, cor)

#===============================================================================
#    Décomposition des nombres décimaux
#===============================================================================


def valeurs_dec():
    lpuissances = [3, 2, 1, 0, -1, -2, -3]
    p = []
    v = []
    for i in range(3):
        p.append(lpuissances.pop(random.randrange(len(lpuissances))))
        v.append(random.randrange(1, 10))
    return (v, p)


def tex_decomposition(v, p):
    exo, cor = [], []
    for i in range(3):
        if p[i] < 0:
            exo.append(_('%s\\times \\cfrac{1}{%s}') % (v[i],
                Affichage.decimaux(10 ** (-p[i]), 1)))
            cor.append(_('%s\\times \\cfrac{1}{%s}') % (v[i],
                Affichage.decimaux(10 ** (-p[i]), 1)))
        else:
            exo.append(_('%s\\times %s') % (v[i], Affichage.decimaux(10 **
                     p[i], 1)))
            cor.append(_('%s\\times %s') % (v[i], Affichage.decimaux(10 **
                     p[i], 1)))
        if i < 2:
            exo.append('+')
            cor.append('+')
        else:
            exo.append('=')
            cor.append('=')
    exo.append(_('\\dotfill$'))
    cor.append('%s$' % Affichage.decimaux(v[0] * 10 ** p[0] +
             v[1] * 10 ** p[1] + v[2] * 10 ** p[2], 1))
    return " ".join(exo), " ".join(cor)


def tex_dec(exo, cor):
    for i in range(6):
        txt = '\\item $'
        (chiffres, puissances) = valeurs_dec()
        txt_exo, txt_cor = tex_decomposition(chiffres, puissances)
        exo.append(txt + txt_exo)
        cor.append(txt + txt_cor)

def Decomposition():
    exo = ["\\exercice", _(u"Compléter avec un nombre décimal :"),
            '\\begin{multicols}{2}\\noindent', '\\begin{enumerate}']
    cor = ["\\exercice*", _(u"Compléter avec un nombre décimal :"),
            '\\begin{multicols}{2}\\noindent', '\\begin{enumerate}']

    tex_dec(exo, cor)

    exo.append('\\end{enumerate}')
    exo.append('\\end{multicols}')
    cor.append('\\end{enumerate}')
    cor.append('\\end{multicols}')
    return (exo, cor)

#===============================================================================
# Classer des nombres dans l'ordre
#===============================================================================


def choix_nombres():
    nb = []
    unite = random.randrange(10)
    for i in range(3):
        n = unite
        for j in range(i + 1):
            n = n + random.randrange(1, 10) * 10 ** (-(j + 1))
        nb.append(n)
    n = random.randrange(10) + random.randrange(10) / 10.0
    while n == nb[0]:
        n = random.randrange(10) + random.randrange(10) / 10.0
    nb.append(n)
    return nb


def classer(exo, cor):
    lnb = choix_nombres()
    random.shuffle(lnb)
    if random.randrange(2):
        ordre = _("croissant")
    else:
        ordre = _(u"décroissant")
    exo.append(_("\\item Classer les nombres suivants dans l'ordre %s.\\par    ") %
             ordre)
    cor.append(_("\\item Classer les nombres suivants dans l'ordre %s.\\par    ") %
             ordre)
    str=""
    for i in range(len(lnb)):
        if i:
            str += " \\kern1cm ; \\kern1cm "
        str += Affichage.decimaux(lnb[i], 0)
    exo.append(str)
    cor.append(str + "\\par")
    lnb.sort()
    if ordre == _("croissant"):
        ordre = "\\textless"
    else:
        ordre = "\\textgreater"
        lnb.reverse()
    str=""
    for i in range(len(lnb)):
        if i:
            str +=" \\kern1cm %s \\kern1cm " % ordre
        str += Affichage.decimaux(lnb[i], 0)
    cor.append(str)



def ClasserNombres():
    exo = ["\\exercice", '\\begin{enumerate}']
    cor = ["\\exercice*", '\\begin{enumerate}']
    classer(exo, cor)
    classer(exo, cor)
    exo.append('\\end{enumerate}')
    cor.append('\\end{enumerate}')
    return (exo, cor)
