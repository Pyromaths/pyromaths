# -*- coding: utf-8 -*-
import sys, os, codecs
import re
from subprocess import call

def imprime_TeX(string,fichier="fichier.tex",chemin_fichier="",borne=["entete","pied de page"]):
    '''crée et affiche une sortie fichier.ps de l'exercice string'''
    if not(chemin_fichier):
        chemin_fichier,tail=os.path.split(os.getcwd())
        while tail!="pyromaths":
            chemin_fichier,tail=os.path.split(chemin_fichier)
        modeletest = os.path.join(chemin_fichier,"pyromaths","TEST","modeletest.tex")
        chemin_fichier=os.path.join(chemin_fichier,"pyromaths","TEST","sortietest")
    else:
        ##modeletest.tex est dans le dossier chemin_fichier indiqué
        modeletest=chemin_fichier
    f0noext=fichier[:-4]
    essai = os.path.join(chemin_fichier,fichier)
    sortie = codecs.open(essai, encoding='utf-8', mode='w')
    master_fin = '% fin ' + borne[0]
    master = '% ' + borne[0]
    n = 0
    modeletex = codecs.open(modeletest, encoding='utf-8', mode='r')
    ## Les variables à remplacer :
    titre = "Fiche d'essai"
    niveau = u"testeur"
    preambule = "\\RequirePackage{alterqcm,tkz-fct,tkz-tab}\n\
	\\usetikzlibrary{arrows,patterns}\n"
    for line in modeletex:
        if master_fin in line:
            break
        if n > 0:
            temp = re.findall('##{{[A-Z]*}}##',line)
            if temp:
                occ = temp[0][4:len(temp)-5].lower()
                line = re.sub('##{{[A-Z]*}}##',eval(occ),line)
            sortie.write(line)
        if master in line:
            n = 1
    sortie.write(string)
    master_fin = '% fin ' + borne[1]
    master = '% ' + borne[1]
    n = 0
    for line in modeletex:
        if master_fin in line:
            break
        if n > 0:
            temp = re.findall('##{{[A-Z]*}}##',line)
            if temp:
                occ = temp[0][4:len(temp)-5].lower()
                line = re.sub('##{{[A-Z]*}}##',eval(occ),line)
            sortie.write(line)
        if master in line:
            n = 1
    modeletex.close()
    sortie.close()
    from subprocess import call
    os.chdir(chemin_fichier)
    call(["latex", "-interaction=batchmode", fichier])
    call(["dvips", "-q", "%s.dvi" % (f0noext), "-o%s.ps" % (f0noext)])
    #call(["ps2pdf", "-sPAPERSIZE#a4", "%s.ps" % (f0noext),"%s.pdf" % (f0noext)])
    os.system('xdg-open %s.ps' % (f0noext))
    #os.system('xdg-open %s.ps' % (f0noext))
