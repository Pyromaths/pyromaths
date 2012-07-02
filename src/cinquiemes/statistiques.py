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
from math import cos, sin, radians
from ..outils.decimaux import decimaux
from ..outils.Arithmetique import pgcd

def tableau_tex(titres, eff=1, freq=1, val=[[],[]],total=1):
    """Génère le tableau des effectifs (liste val[1]) et fréquences (liste val[2])."""
    cols = len(titres)
    tableau_tex = u"\\begin{tabular}{|>{\\centering\\bfseries}c|*{"+str(cols-1)+"}{c|}"
    
    if total:
        tableau_tex += ">{\\centering\\bfseries\\arraybackslash}p{2cm}|}\n"
    else:
        tableau_tex += "}\n"
        
    tableau_tex += u"\\hline\n"
    
    for titre in titres: # Ligne de titre, avec astuce pour éviter le cadre sur la dernière cellule "Total"
        tableau_tex += u"\\textbf{"+titre+"} & "
    
    if total:    
        tableau_tex += u"\\textbf{Total} \\\\\\hline\n"
    else:
        tableau_tex = tableau_tex[:-2]+u"\\\\\\hline\n"
    
    if eff:
        tableau_tex += "Effectifs"
        if len(val[0])>0:
            somme = 0
            for effectif in val[0]:
                if effectif < 0:
                    tableau_tex += " & "
                else:
                    tableau_tex += " & "+decimaux(effectif)
                    somme += effectif
        else:
            tableau_tex += " & " * (cols-1)
            somme = ""
        
        if total:    
            tableau_tex += " & "+str(somme)+"\\\\\\hline\n"
        else:
            tableau_tex += "\\\\\\hline\n"

    if freq:
        tableau_tex += u"Fréquences ( \\% )"
        if len(val[1])>0:
            for frequence in val[1]:
                somme = "100"
                if frequence < 0:
                    tableau_tex += " & "
                else:
                    tableau_tex += " & "+decimaux(frequence)
        else:
            tableau_tex += " & " * (cols-1)
            somme = ""
            
        if total:    
            tableau_tex += " & "+somme+"\\\\\\hline\n"
        else:
            tableau_tex += "\\\\\\hline\n"
    
    tableau_tex += "\\end{tabular}\n"    
    
    return tableau_tex

def diagramme_tex(typed=2,val=[[],[]],aide=0):
    """Génère un diagramme en bâtons (type 1), circulaire (type2) ou semi-circulaire (type3) à partir des fréquences (liste val[1]) et son tableau de calculs."""
    diag = ""
    
    couleur = ["yellow", "blue", "orange", "green", "red", "gray", "pink", "purple", "brown", "white", "cyan", "olive"]
    
    if typed == 1: # Diagramme en bâtons
        
        grad = len(val[1])+1
        diag += u"\\begin{pspicture}(-1,-1)("+str(grad)+",11)\n"
        diag += u"\\psset{xunit=1cm,yunit=1cm}\n"
        diag += u"\\psgrid[subgriddiv=1,griddots=5,gridlabels=0]("+str(grad)+",11)\n"
        diag += u"\\psaxes[Dx=1,dx=1,Dy=10,dy=1]{->}(0,0)("+str(grad)+",11)\n"
        
        for f in range(len(val[1])):
            diag += u"\\psline[linewidth=0.1,linecolor=green]("+val[0][f+1]+",0)("+val[0][f+1]+","+str(val[1][f]/10.0)+")\n"
            
        diag += u"\\rput(0,11.2){\\small Fréquences (\\%)}\n"
        diag += u"\\rput("+str(grad+0.5)+",0){\\small "+val[0][0]+"}\n"
        diag += u"\\end{pspicture}\n"
        
    elif typed == 2: # Diagramme circulaire
        grad = len(val[1])
        diag += u"\\begin{pspicture}(-3,-3)(3,3)\n"
        diag_texte = ""
        
        debut = 0
        fin = round(val[1][0]*3.6,0)
        liste_fin = [fin] # Pour éviter d'avoir les pointillés superposés sur des lignes
        

        for v in range(len(val[1])-1):
            diag += u"\\pswedge[fillstyle=solid,fillcolor="+couleur[v%12]+"](0,0){3}{"+str(debut)+"}{"+str(fin)+"}\n"
            diag_texte += u"\\rput("+str(3*round(cos(radians((debut+fin)/2.0)),2))+","+str(3*round(sin(radians((debut+fin)/2.0)),2))+"){\\small \\bfseries{"+val[0][v+1]+"}}\n"
            debut = fin
            fin += round(val[1][v+1]*3.6,0)
            liste_fin.append(fin)
        diag += u"\\pswedge[fillstyle=solid,fillcolor="+couleur[(len(val[1])-1)%12]+"](0,0){3}{"+str(debut)+"}{360}\n"
        diag_texte += u"\\rput("+str(3*round(cos(radians((debut+fin)/2.0)),2))+","+str(3*round(sin(radians((debut+fin)/2.0)),2))+"){\\small \\bfseries{"+val[0][-1]+"}}\n"
                
        if aide != 0:        
            temp = [int(3.6*v) for v in val[1]]
            temp2 = [pgcd(temp[i],temp[i+1]) for i in range(len(val[1])-1)]
            temp2.sort()
            ecart = temp2[0]
            angle = ecart
                  
            while angle < 360:
                if angle not in liste_fin:
                    diag += u"\\psline[linestyle=dashed,linecolor=gray](0,0)("+str(3*round(cos(radians(angle)),2))+","+str(3*round(sin(radians(angle)),2))+")\n"
                angle += ecart   
        
        diag += diag_texte
        diag += u"\\end{pspicture}\n"
        
    elif typed == 3: # Diagramme semi-circulaire
        grad = len(val[1])
        diag += u"\\begin{pspicture}(0,0)(3,3)\n"
        diag_texte = ""
        
        debut = 0
        fin = round(val[1][0]*1.8,0)
        liste_fin = [fin] # Pour éviter d'avoir les pointillés superposés sur des lignes
        
        for v in range(len(val[1])-1):
            diag += u"\\pswedge[fillstyle=solid,fillcolor="+couleur[v%12]+"](0,0){3}{"+str(debut)+"}{"+str(fin)+"}\n"
            diag_texte += u"\\rput("+str(3*round(cos(radians((debut+fin)/2.0)),2))+","+str(3*round(sin(radians((debut+fin)/2.0)),2))+"){\\small \\bfseries{"+val[0][v+1]+"}}\n" # FIX problème hauteur textes superposés
            debut = fin
            fin += round(val[1][v+1]*1.8,0)
            liste_fin.append(fin)
        diag += u"\\pswedge[fillstyle=solid,fillcolor="+couleur[(len(val[1])-1)%12]+"](0,0){3}{"+str(debut)+"}{180}\n"
        diag_texte += u"\\rput("+str(3*round(cos(radians((debut+fin)/2.0)),2))+","+str(3*round(sin(radians((debut+fin)/2.0)),2))+"){\\small \\bfseries{"+val[0][-1]+"}}\n"
        
        if aide != 0:        
            temp = [int(1.8*v) for v in val[1]]
            temp2 = [pgcd(temp[i],temp[i+1]) for i in range(len(val[1])-1)]
            temp2.sort()
            ecart = temp2[0]
            angle = ecart

            while angle < 180:
                if angle not in liste_fin:
                    diag += u"\\psline[linestyle=dashed,linecolor=gray](0,0)("+str(3*round(cos(radians(angle)),2))+","+str(3*round(sin(radians(angle)),2))+")\n"
                angle += ecart   
        
        diag += diag_texte
        diag += u"\\end{pspicture}\n"
        
    
    return diag

def tableau_diagramme_tex(typed=2,val=[[],[]]):
    """Génère le tableau de calculs des angles ou des longueurs pour le corrigé de la construction des diagrammes."""
    tab = ""
    cols = len(val[0])
    tab = u"\\begin{tabular}{|>{\\bfseries}c|*{"+str(cols-1)+"}{c|}>{\\centering\\bfseries\\arraybackslash}p{2cm}|}\n"
    tab += u"\\cline{1-"+str(cols)+"}\n"
    
    for titre in val[0]: # Ligne de titre, avec astuce pour éviter le cadre sur la dernière cellule "Total"
        tab += u"\\textbf{"+titre+"} & "
    tab += u"\\multicolumn{1}{c}{\\textbf{Total}} \\\\\\hline\n"
    
    tab += u"Fréquences ( \\% )"

    for frequence in val[1]:
        tab += " & "+decimaux(frequence)
       
    tab += " & 100 \\\\\\hline\n"
      
    if typed == 1: # Diagramme en bâtons
        texte = u"Comme 10\\% sont représentés par 1cm, il faut diviser chaque fréquence par 10 pour obtenir la longueur ( arrondie au dixième ) du bâton à dessiner :\\par\n"
        tab = texte + tab
        tab += u"Hauteur ( cm )"
        for frequence in val[1]:
            tab += " & "+decimaux(round(frequence/10.0,1))
        tab += " & 10 \\\\\\hline\n"
        
    elif typed == 2: # Diagramme circulaire
        texte = u"Comme il y a $360^{\circ}$ dans un cercle pour représenter 100\\%, il faut multiplier chaque fréquence par 3,6 pour connaître son angle ( arrondi au degré ) de représentation dans le diagramme :\\par\n"
        tab = texte + tab
        tab += u"Angle ( Degrés )"        
        for frequence in val[1]:
            tab += " & "+decimaux(round(frequence*3.6,0))
        tab += " & 360 \\\\\\hline\n"
        
    elif typed == 3: # Diagramme semi-circulaire
        texte = u"Comme il y a $180^{\circ}$ dans un cercle pour représenter 100\\%, il faut multiplier chaque fréquence par 1,8 pour connaître son angle ( arrondi au degré ) de représentation dans le diagramme :\\par\n"
        tab = texte + tab
        tab += u"Angle ( Degrés )"        
        for frequence in val[1]:
            tab += " & "+decimaux(round(frequence*1.8,0))
        tab += " & 180 \\\\\\hline\n"        
    
    tab += "\\end{tabular}\\par\n"
    
    return tab

def exo_pi():
    """Exercice sur les décimales de Pi."""
    global exo, cor
    
    pi = "14159265358979323846264338327950288419716939937510582097494459230781640628620899862803482534211706798214808651328230664709384460955058223172535940812848111745028410270193852110555964462294895493038196442881097566593344612847564823378678316527120190914564856692346034861045432664821339360726024914127372458700660631558817488152092096282925409171536436789259036001133053054882046652138414695194151160943305727036575959195309218611738193261179310511854807446237996274956735188575272489122793818301194912983367336244065664308602139494639522473719070217986094370277053921717629317675238467481846766940513200056812714526356082778577134275778960917363717872146844090122495343014654958537105079227968925892354201995611212902196086403441815981362977477130996051870721134999999837297804995105973173281609631859502445945534690830264252230825334468503526193118817101000313783875288658753320838142061717766914730359825349042875546873115956286388235378759375195778185778053217122680661300192787661119590921642019893809525720106548586327886593615338182796823030195203530185296899577362259941389124972177528347913151557485724245415069595082953311686172785588907509838175463746493931925506040092770167113900984882401285836160356370766010471018194295559619894676783744944825537977472684710404753464620804668425906949129331367702898915210475216205696602405803815019351125338243003558764024749647326391419927260426992279678235478163600934172164121992458631503028618297455570674983850549458858692699569092721079750930295532116534498720275596023648066549911988183479775356636980742654252786255181841757467289097777279380008164706001614524919217321721477235014144197356854816136115735255213347574184946843852332390739414333454776241686251898356948556209921922218427255025425688767179049460165346680498862723279178608578438382796797668145410095388378636095068006422512520511739298489608412848862694560424196528502221066118630674427862203919494504712371378696095636437191728746776465757396241389086583264599581339047802759009" # 2000 décimales de Pi après la virgule
    
    nb_dec = random.randint(50,100)
    idx_dec = random.randint(0,2000-nb_dec)
    dec_str = list(pi[idx_dec:(idx_dec+nb_dec)])
    dec = [int(d) for d in dec_str]
    dec_tex = "\\begin{center}\n\\begin{tabular}{|*{20}{p{0.2cm}}|}\n\\hline\n"
    
    for d in range(len(dec_str)):
        dec_tex += dec_str[d] + " & "
        if ((d+1) % 20 == 0):
            dec_tex = dec_tex[:-3]+"\\\\\n"
    dec_tex += " & "*(19-len(dec_str)%20)+"\\\\\n"
    dec_tex += "\\hline\n\\end{tabular}\n\\end{center}"
     
    effectifs = [dec.count(i) for i in range(10)]    
    frequences = [round(i*100.0/nb_dec,2) for i in effectifs] # FIX somme pas toujours égale à 100%
    
    tableau = tableau_tex([u"Chiffres", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]) 
    tableau_cor = tableau_tex([u"Chiffres", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"],1,1,[effectifs,frequences])
    
    exo.append(u"Voici une liste de chiffres choisis au hasard dans les décimales de $\\pi$ :\\par")    
    cor.append(u"Voici une liste de chiffres choisis au hasard dans les décimales de $\\pi$ :\\par")
    exo.append(dec_tex) 
    cor.append(dec_tex)
    exo.append("\\begin{enumerate}")
    cor.append("\\begin{enumerate}")
    exo.append(u"\\item Compléter le tableau ci-dessous, sachant que les fréquences doivent être arrondies au centième.\\par")
    cor.append(u"\\item Compléter le tableau ci-dessous, sachant que les fréquences doivent être arrondies au centième.\\par")   
    exo.append(tableau)
    cor.append(u"Chaque effectif se complète en comptant le nombre d'apparition de chaque chiffre dans la liste de l'énoncé.")
    cor.append(u"Comme les chiffres sont rangés par 20, on voit assez rapidement que le nombre total de chiffres est de "+str(nb_dec)+".\\par")
    cor.append(u"Pour le calcul des fréquences, on multiplie l'effectif par 100, et on divise par le nombre total de chiffres, puis il ne faut pas oublier d'arrondir au centième.\\par\n")
    cor.append(u"Par exemple pour la fréquence du chiffre 1 : $\\dfrac{"+decimaux(effectifs[0])+"\\times 100}{"+str(nb_dec)+"} \\approx "+decimaux(frequences[0])+"$.\\par")
    cor.append(tableau_cor)
    exo.append(u"\\item Représenter la répartition des chiffres dans un diagramme en bâtons avec 1~cm pour 10\\%.\\par")
    cor.append(u"\\item Représenter la répartition des chiffres dans un diagramme en bâtons avec 1~cm pour 10\\%.\\par") 
    
    diagramme = diagramme_tex(1,[[u"Valeurs", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"],frequences])
    diagramme_tableau = tableau_diagramme_tex(1,[[u"Valeurs", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"],frequences])
    
    cor.append(diagramme_tableau)  
    cor.append("\\bigskip")
    cor.append(diagramme)
    
    exo.append("\n\\end{enumerate}")
    cor.append("\n\\end{enumerate}")    
    
    return False

def exo_notes():
    """Exercice sur les notes."""
    global exo, cor
 
    len_classe = [4,5][random.randint(0,1)] # Classes de longueur 4 ou 5
    classes = []
    val = 0
    while val+len_classe <= 20:
        classes += [[val,val+len_classe]]
        val = val+len_classe
    
    titres = [u"Classes de notes"]+[u"$" +str(f[0])+u" \leq n < "+str(f[1])+u"$" for f in classes[:-1]]+[u"$" +str(classes[-1][0])+u" \leq n \leq 20$"]
    
    exo.append(u"Voici un tableau regroupant les notes d'une classe lors d'un contrôle :\\par")
    cor.append(u"Voici un tableau regroupant les notes d'une classe lors d'un contrôle :\\par")
    
    nb_eleves = random.randint(25,35)
    notes_tpl = [str(i) for i in range(21)]
    notes = [random.randint(1,20) for i in range(nb_eleves)]
    notes_effectifs = [notes.count(i) for i in range(21)]
    tableau_notes = tableau_tex([u"Notes"]+notes_tpl,1,0,[notes_effectifs,[]],0)
    
    exo.append(tableau_notes)
    cor.append(tableau_notes)
    exo.append(u"\\begin{enumerate}")
    cor.append(u"\\begin{enumerate}")
    exo.append(u"\\item Compléter le tableau ci-dessous afin de regrouper les notes par classes et effectuer le calcul des fréquences arrondies au centième :\\par")
    cor.append(u"\\item Compléter le tableau ci-dessous afin de regrouper les notes par classes et effectuer le calcul des fréquences arrondies au centième :\\par")
    exo.append(tableau_tex(titres))
    
    classes_effectifs=[0 for f in classes]
    
    for n in notes:
        if n == 20:
            classes_effectifs[-1] += 1
        else:
            for c in classes:
                if c[0] <= n < c[1]:
                    classes_effectifs[classes.index(c)] += 1            

    frequences = [round(i*100.0/nb_eleves,2) for i in classes_effectifs]   
    
    cor.append(u"Chaque effectif se complète en comptant le nombre d'apparition de chaque note dans le tableau de l'énoncé.")
    cor.append(u"Le nombre de notes du contrôle, qui est aussi le nombre d'élèves, est donc de "+str(nb_eleves)+".\\par")
    cor.append(u"Pour le calcul des fréquences, on multiplie l'effectif par 100, et on divise par le nombre total de notes, puis il ne faut pas oublier d'arrondir au centième.\\par\n")
    cor.append(u"Par exemple pour la fréquence des notes dans la première classe : $\\dfrac{"+decimaux(classes_effectifs[0])+"\\times 100}{"+str(nb_eleves)+"} \\approx "+decimaux(frequences[0])+"$.\\par")    
    cor.append(tableau_tex(titres,1,1,[classes_effectifs,frequences]))
    
    note1_rand = random.randint(0,len(classes)-2)
    note1 = classes[note1_rand][1]
    note2 = 20 - note1
    note2_rand = len(classes)-1-note1_rand
    
    exo.append(u"\\item Combien d'élèves ont une note strictement inférieure à "+str(note1)+u" ? Supérieure ou égale à "+str(note2)+" ?\\par")
    cor.append(u"\\item Combien d'élèves ont une note strictement inférieure à "+str(note1)+u" ? Supérieure ou égale à "+str(note2)+" ?\\par")    
    
    card_note1 = 0
    card_note2 = 0

    if note1_rand == 0:
        card_note1 = classes_effectifs[0]
        card_note2 = classes_effectifs[-1]
        texte_note1 = str(card_note1)
        texte_note2 = str(card_note2)
    else:
        tmp = 0
        texte_note1 = ""
        
        while tmp <= note1_rand:
            card_note1 += classes_effectifs[tmp]
            texte_note1 += str(classes_effectifs[tmp]) + " + " 
            tmp += 1
        
        tmp = note2_rand
        texte_note2 = ""
        
        while tmp < len(classes):
            card_note2 += classes_effectifs[tmp]
            texte_note2 += str(classes_effectifs[tmp]) + " + " 
            tmp += 1

        texte_note1 =  texte_note1[:-3]+" = "+str(card_note1)
        texte_note2 =  texte_note2[:-3]+" = "+str(card_note2)
    
    cor.append(u"D'après le tableau rempli précédemment, le nombre d'élèves ayant une note strictement inférieure à "+str(note1)
               +u" sont tous les élèves comptés dans les classes situées à gauche de "+str(note1)
               +u". En effectuant le total des élèves de ces classes, on obtient : "+texte_note1+u" élèves.\\par")
    
    cor.append(u"La réponse à la seconde question se fait de même en comptant tous les effectifs des élèves se situant à droite de "+str(note2)+u".\\par")
    cor.append(u"Le résultat est donc : "+texte_note2+u" élèves.\\par")
    
    exo.append(u"\n\\end{enumerate}")
    cor.append(u"\n\\end{enumerate}")
    
    return False

def exo_de():
    """Exercice sur le lancer d'un dé."""
    global exo, cor
    
    nb_simul = random.randint(50,80)
    simul = []
    simul_tex = "\\par"
    for f in range(nb_simul): # Simulation de nb_simul lancés d'un dé
        temp = random.randint(1,6)
        simul.append(temp)
        simul_tex += str(temp) + " "
        if ((f+1) % 25 == 0):
            simul_tex += "\\par"
        
    effectifs = [simul.count(i+1) for i in range(6)]    
    frequences = [round(i*100.0/nb_simul,2) for i in effectifs] # FIX somme pas toujours égale à 100%
    
    tableau = tableau_tex([u"Valeurs", "1", "2", "3", "4", "5", "6"]) 
    tableau_cor = tableau_tex([u"Valeurs", "1", "2", "3", "4", "5", "6"],1,1,[effectifs,frequences])
    
    exo.append(u"Voici une liste des résultats obtenus en lançant plusieurs fois un dé à six faces :\\par")    
    cor.append(u"Voici une liste des résultats obtenus en lançant plusieurs fois un dé à six faces :\\par")
    exo.append(simul_tex)
    cor.append(simul_tex)
    exo.append("\\begin{enumerate}")
    cor.append("\\begin{enumerate}")
    exo.append(u"\\item Compléter le tableau ci-dessous, sachant que les fréquences doivent être arrondies au centième.\\par")
    cor.append(u"\\item Compléter le tableau ci-dessous, sachant que les fréquences doivent être arrondies au centième.\\par")   
    exo.append(tableau)
    cor.append(u"Chaque effectif se complète en comptant le nombre d'apparition de chaque chiffre dans la liste de l'énoncé.")
    cor.append(u"Comme les chiffres sont rangés par 25, on voit assez rapidement que le nombre total de chiffres est de "+str(nb_simul)+".\\par")
    cor.append(u"Pour le calcul des fréquences, on multiplie l'effectif par 100, et on divise par le nombre total de chiffres, puis il ne faut pas oublier d'arrondir au centième.\\par\n")
    cor.append(u"Par exemple pour la fréquence du chiffre 1 : $\\dfrac{"+str(effectifs[0])+"\\times 100}{"+str(nb_simul)+"} \\approx "+decimaux(frequences[0])+"$.\\par")
    cor.append(tableau_cor)
    exo.append(u"\\item Représenter la répartition des chiffres dans un diagramme en bâtons avec 1cm pour 10\\%.\\par")
    cor.append(u"\\item Représenter la répartition des chiffres dans un diagramme en bâtons avec 1cm pour 10\\%.\\par") 
    
    diagramme = diagramme_tex(1,[[u"Valeurs", "1", "2", "3", "4", "5", "6"],frequences])
    diagramme_tableau = tableau_diagramme_tex(1,[[u"Valeurs", "1", "2", "3", "4", "5", "6"],frequences])
    
    cor.append(diagramme_tableau)  
    cor.append("\\bigskip")
    cor.append(diagramme)
    
    exo.append("\n\\end{enumerate}")
    cor.append("\n\\end{enumerate}")
    
    return False

def exo_ages():
    """Exercice sur la répartition des âges dans une population."""
    global exo, cor
    
    # Partitions de 20
    partitions = [[4, 4, 4, 4, 4], [3, 4, 4, 4, 5], [3, 3, 4, 5, 5], [2, 4, 4, 5, 5], [2, 3, 5, 5, 5], [1, 4, 5, 5, 5], 
                  [3, 3, 4, 4, 6], [2, 4, 4, 4, 6], [3, 3, 3, 5, 6], [2, 3, 4, 5, 6], [1, 4, 4, 5, 6], [2, 2, 5, 5, 6], 
                  [1, 3, 5, 5, 6], [2, 3, 3, 6, 6], [2, 2, 4, 6, 6], [1, 3, 4, 6, 6], [1, 2, 5, 6, 6], [1, 1, 6, 6, 6], 
                  [3, 3, 3, 4, 7], [2, 3, 4, 4, 7], [1, 4, 4, 4, 7], [2, 3, 3, 5, 7], [2, 2, 4, 5, 7], [1, 3, 4, 5, 7], 
                  [1, 2, 5, 5, 7], [2, 2, 3, 6, 7], [1, 3, 3, 6, 7], [1, 2, 4, 6, 7], [1, 1, 5, 6, 7], [2, 2, 2, 7, 7], 
                  [1, 2, 3, 7, 7], [1, 1, 4, 7, 7], [3, 3, 3, 3, 8], [2, 3, 3, 4, 8], [2, 2, 4, 4, 8], [1, 3, 4, 4, 8], 
                  [2, 2, 3, 5, 8], [1, 3, 3, 5, 8], [1, 2, 4, 5, 8], [1, 1, 5, 5, 8], [2, 2, 2, 6, 8], [1, 2, 3, 6, 8], 
                  [1, 1, 4, 6, 8], [1, 2, 2, 7, 8], [1, 1, 3, 7, 8], [1, 1, 2, 8, 8], [2, 3, 3, 3, 9], [2, 2, 3, 4, 9], 
                  [1, 3, 3, 4, 9], [1, 2, 4, 4, 9], [2, 2, 2, 5, 9], [1, 2, 3, 5, 9], [1, 1, 4, 5, 9], [1, 2, 2, 6, 9], 
                  [1, 1, 3, 6, 9], [1, 1, 2, 7, 9], [1, 1, 1, 8, 9], [2, 2, 3, 3, 10], [1, 3, 3, 3, 10], [2, 2, 2, 4, 10], 
                  [1, 2, 3, 4, 10], [1, 1, 4, 4, 10], [1, 2, 2, 5, 10], [1, 1, 3, 5, 10], [1, 1, 2, 6, 10], [1, 1, 1, 7, 10], 
                  [2, 2, 2, 3, 11], [1, 2, 3, 3, 11], [1, 2, 2, 4, 11], [1, 1, 3, 4, 11], [1, 1, 2, 5, 11], [1, 1, 1, 6, 11], 
                  [2, 2, 2, 2, 12], [1, 2, 2, 3, 12], [1, 1, 3, 3, 12], [1, 1, 2, 4, 12], [1, 1, 1, 5, 12], [1, 2, 2, 2, 13], 
                  [1, 1, 2, 3, 13], [1, 1, 1, 4, 13], [1, 1, 2, 2, 14], [1, 1, 1, 3, 14], [1, 1, 1, 2, 15], [1, 1, 1, 1, 16]]
    
    choix_diagramme = random.randint(0,1)
    if choix_diagramme == 0:
        diagramme_texte = "circulaire"
    else:
        diagramme_texte = "semi-circulaire"
    hasard = partitions[random.randint(0,len(partitions)-1)]
    frequences = [5*v for v in hasard] 
    random.shuffle(frequences)
    
    population = 20*random.randint(100,2000)
    
    titres = [u"Moins de 20 ans", u"Entre 20 et 40 ans", u"Entre 40 et 60 ans", u"Entre 60 et 80 ans", u"Plus de 80 ans"]
    diagramme = diagramme_tex(choix_diagramme+2,[[u"Ages", u"<20","20 - 40","40 - 60","60 - 80",u">80"],frequences],1) 
    exo.append(u"\\begin{center}")
    cor.append(u"\\begin{center}")
    exo.append(diagramme)
    cor.append(diagramme)
    exo.append(u"\\end{center}")
    cor.append(u"\\end{center}")
    exo.append(u"Le diagramme "+diagramme_texte+u" ci-dessus représente les différentes fréquences des classes d'âges dans une certaine région.\\par")
    cor.append(u"Le diagramme "+diagramme_texte+u" ci-dessus représente les différentes fréquences des classes d'âges dans une certaine région.\\par")
    exo.append("\\begin{enumerate}")
    cor.append("\\begin{enumerate}")
    exo.append(u"\\item Calculer les fréquences de chaque classe d'âges.\\par")
    cor.append(u"\\item Calculer les fréquences de chaque classe d'âges.\\par")
    
    titres = [u"Classes d'âges", u"$0 \\leq n \\leq 20$", u"$20 \\leq n \\leq 40$", u"$40 \\leq n \\leq 60$", u"$60 \\leq n \\leq 80$", u"$80 \\geq n$"]
    
    liste_pgcd = [pgcd(frequences[i],frequences[i+1]) for i in range(len(frequences)-2)]
    liste_pgcd.sort()
    pourcent = liste_pgcd[0]    
    parts = 100 / pourcent
    effectifs = [f*population/100 for f in frequences]
    
    cor.append(u"Le diagramme "+diagramme_texte+u" est partagé en "+str(parts)+u" parts symbolisées par des lignes grises en pointillés.\\par")
    cor.append(u"On en déduit que chacune de ces parts représente $\\dfrac{100}{"+str(parts)+"}="+str(pourcent)+u"\\%$, puis en comptant le nombre de parts dans chaque classe, on obtient le tableau suivant :\\par" )
    cor.append(tableau_tex(titres,0,1,[[],frequences]))
    
    exo.append(u"\\item Sachant que la population étudiée est composée de "+str(population)+u" personnes, calculer les effectifs de chaque classe d'âges.\\par")
    cor.append(u"\\item Sachant que la population étudiée est composée de "+str(population)+u" personnes, calculer les effectifs de chaque classe d'âges.\\par")
    
    cor.append(u"Sachant que la classe des moins de vingt ans est composée de "+str(frequences[0])+u" \\% de "+str(population)+u" personnes, on peut calculer l'effectif concerné :\\par")
    cor.append(u"$\\dfrac{"+str(frequences[0])+u" \\times "+str(population)+u"}{100}="+str(effectifs[0])+u"$.\\par")
    cor.append(u"Avec le même type de calcul, on obtient les effectifs des autres classes, résumés dans le tableau ci-dessous : \\par")
    cor.append(tableau_tex(titres,1,1,[effectifs,frequences]))
    
    
    exo.append("\n\\end{enumerate}")
    cor.append("\n\\end{enumerate}")
    return False


def exo_vote():
    """Exercice sur un vote en classe."""
    global exo, cor
    
    exo.append("\\begin{enumerate}")
    cor.append("\\begin{enumerate}")
    exo.append(u"\\item Les données du vote du délégué de classe ont été malheureusement partiellement perdues, mais on a réussi à regrouper les informations du tableau ci-dessous ( sachant que chaque élève a voté ) :\\par\n")
    cor.append(u"\\item Les données du vote du délégué de classe ont été malheureusement partiellement perdues, mais on a réussi à regrouper les informations du tableau ci-dessous ( sachant que chaque élève a voté ) :\\par\n")
    
    eff1 = random.randint(0,15)
    eff2 = random.randint(0,25-eff1)
    freq1 = 4*random.randint(0,25-eff1-eff2)
    effectifs = [eff1,eff2,-1,-1]
    random.shuffle(effectifs)
    idx = effectifs.index(-1)
    frequences = []
    
    for f in range(4):
        if f == idx:
            frequences.append(freq1)
        else:
            frequences.append(-1)    
    prenoms = [u"Vincent", u"Sophia", u"Karim", u"Denise", u"Aline", u"Jonathan", u"Isabelle", u"Thomas", u"Léna", u"Matteo", u"Céline", u"Antoine", u"Julie", u"Rémy", u"Caroline", u"Yann", u"Muriel", u"Patrick", u"Mélanie"]
    random.shuffle(prenoms)
    titres = [u"Elève"] + prenoms[:4] 
    valeurs = [effectifs,frequences]
    
    exo.append(tableau_tex(titres,1,1,valeurs,0))
    cor.append(tableau_tex(titres,1,1,valeurs,0))
    exo.append("\\bigskip")
    cor.append("\\bigskip")
    exo.append(u"Sachant qu'il y a 25 élèves dans la classe, compléter alors le tableau ci-dessus.\\par")
    cor.append(u"Sachant qu'il y a 25 élèves dans la classe, compléter alors le tableau ci-dessus.\\par")    

    effectifs[idx] = freq1 / 4
    idx2 = effectifs.index(-1)
    effectifs[idx2] = 25 - eff1 - eff2 - freq1 / 4
    frequences = [ 4 * f for f in effectifs ]
    
    cor.append("\\par")
    cor.append(u"Comme il y a 25 élèves dans la classe, ce qui représente 100 \\% des votes, il faut diviser la fréquence connue pour trouver l'effectif d'élèves ayant voté pour "+titres[idx+1]+" et on trouve : ")
    cor.append(u"$\\dfrac{"+str(freq1)+"}{4}="+str(freq1/4)+u"$ élève(s) pour "+titres[idx+1]+".\\par")
    cor.append(u"Ensuite, pour trouver l'effectif d'élèves ayant voté pour "+titres[idx2+1]+u", il suffit de soustraire à 25 les effectifs connus :\\par")
    cor.append(u"$25 - "+str(eff1)+" - "+str(eff2)+" - "+str(freq1/4)+" = "+str(effectifs[idx2])+u"$ élève(s) pour "+titres[idx2+1]+".\\par")
    cor.append(u"Enfin, pour le calcul des fréquences manquantes, il faut multiplier chaque effectif par 4, ce qui fourni le tableau ci-dessous.\\par")

    cor.append(tableau_tex(titres,1,1,[effectifs,frequences]))
    cor.append("\\bigskip")
    exo.append(u"\\item Représenter la répartition des votes dans un diagramme circulaire de rayon 3 cm.\\par")
    cor.append(u"\\item Représenter la répartition des votes dans un diagramme circulaire de rayon 3 cm.\\par") 

    diagramme = diagramme_tex(2,[titres,frequences])
    diagramme_tableau = tableau_diagramme_tex(2,[titres,frequences])
    
    cor.append(diagramme_tableau)  
    cor.append("\\bigskip")
    cor.append(diagramme)    
    
    exo.append("\n\\end{enumerate}")
    cor.append("\n\\end{enumerate}")
    return exo,cor

def exo_sport():
    global exo, cor
    
    h1 = random.randrange(2) + 5
    h2 = 8
    h3 = random.randrange(2) + 7
    h5 = random.randrange(4) + 1
    h6 = random.randrange(3)
    h7 = random.randrange(2) + 1
    h4 = 30 - h1 - h2 - h3 - h5 - h6 - h7
    basket = random.randrange(7) + 3
    tennis = random.randrange(7) + 3
    judo = random.randrange(7) + 3
    football = 30 - tennis - basket - judo
    question1 = \
        u"""\\renewcommand{\\arraystretch}{1.8}
        \\item On a demandé aux élèves d'une classe de cinquième combien de temps par semaine était consacré à leur sport favori.\\par
        \\begin{tabular}{|c|c|c|c|c|c|c|c|}\\hline Durée t (en h)&  $0 \\le t < 1$ & $1 \\le t  < 2$ & $2 \\le t  < 3$ & $3 \\le t  < 4$ &  $4 \\le t  < 5$ & $5 \\le t  < 6$ & $6 \\le t  < 7$ \\\\\\hline Effectif & %s & %s & %s & %s & %s & %s & %s \\\\\\hline \\end{tabular}\\par
        À partir de ce tableau, construire un  histogramme pour représenter ces données.\\par""" % (h1, h2, h3, h4, h5, h6, h7)
    question2 = \
        u"""\\item On a demandé aux élèves quel était leur sport préféré. %s élèves préfèrent le basket-ball, %s le tennis, %s le football et %s le judo. Construire un diagramme circulaire représentant cette répartion.\\par""" % (basket, tennis, football, judo)
    exo.append("\\begin{enumerate}")
    exo.append(question1)
    exo.append(question2)
    exo.append("\\end{enumerate}")
    cor.append("\\begin{enumerate}")
    cor.append(question1)
    cor.append(u"""\\begin{minipage}{10cm}
    \\begin{pspicture}(0,-1)(8.5,9.5)
    \\psaxes[showorigin=false]{->}(7.5,8.5)
    \\psset{fillstyle=solid, linewidth=0.5pt}
    \\psframe(0,0)(1,%s)
    \\psframe(1,0)(2,%s)
    \\psframe(2,0)(3,%s)
    \\psframe(3,0)(4,%s)
    \\psframe(4,0)(5,%s)
    \\psframe(5,0)(6,%s)
    \\psframe(6,0)(7,%s)
    \\rput(-0.2,-0.425){$0$}
    \\rput(8.3,0){Durée}
    \\rput(0,8.8){Effectif}
    \\end{pspicture}
    \\end{minipage}
    \\begin{minipage}{6cm}
    Sur l'axe horizontal, on représente les durées en heures et, sur l'axe vertical, on représente les effectifs.
    \\end{minipage}""" % (h1, h2, h3, h4, h5, h6, h7))
    cor.append(question2)
    cor.append(u"L'effectif total est égal à $ %s + %s + %s + %s = 30$. La mesure d'angle d'un secteur circulaire est proportionnelle à l'effectif du sport qu'il représente. Le coefficient de proportionnalité est égal au quotient de l'effectif total par 360\\degre c'est à dire $360 \\div 30=12$.\\par" % (basket, tennis, football, judo))
    cor.append(u"""\\renewcommand\\tabcolsep{10pt}
    \\begin{tabular}{|l|c|c|c|c|c|c}
    \\cline{1-6}
    Sport favori  & Basket-ball & Tennis & Football & Judo & Total &\\rnode{plan1}{}\\\\
    \\cline{1-6}
    Effectif & %s & %s & %s & %s & 30 &\\rnode{plan1}{}\\\\
    \\cline{1-6}
    Mesure (en degré)  & \\bf%s & \\bf%s & \\bf%s & \\bf%s & 360 &\\rnode{plan2}{}\\\\
    \\cline{1-6}
    \\end{tabular}
    \\ncbar{->}{plan1}{plan2}\\Aput{$\\times 12$}\\par
    \\begin{minipage}{6cm}
    En utilisant les mesures d'angles obtenues dans le tableau de proportionnalité, on trace le diagramme circulaire.
    \\end{minipage}""" % (basket, tennis, football, judo, basket*12, tennis*12, football*12, judo*12))
    cor.append(u"""\\begin{minipage}{13cm}
    \\psset{unit=3cm,fillstyle=solid}
    \\pspicture(-1.5,-1)(1,1.5)
    \\pswedge[fillcolor=Bisque]{1}{0}{%s}
    \\pswedge[fillcolor=LightSalmon]{1}{%s}{%s}
    \\pswedge[fillcolor=Chocolate]{1}{%s}{%s}
    \\pswedge{1}{%s}{360}
    \\rput(.6;%s){Basket}
    \\rput(.6;%s){Tennis}
    \\rput(.6;%s){\\white Football}
    \\rput(.6;%s){Judo}
    \\endpspicture
    \\end{minipage}""" %(basket*12, basket*12, basket*12+tennis*12, basket*12+tennis*12, basket*12+tennis*12+football*12, basket*12+tennis*12+football*12, basket*6, basket*12+tennis*6, basket*12+tennis*12+football*6, basket*6+tennis*6+football*6+180 ))
    cor.append(u"\\end{enumerate}")
    return (exo, cor)

def statistiques():
    """Construit au hasard l'un des six types d'exos de statistiques."""
    global exo, cor
    
    exo = ["\\exercice"]
    cor = ["\\exercice*"]
    
    exo.append("\\renewcommand{\\arraystretch}{2}")
    cor.append("\\renewcommand{\\arraystretch}{2}")
    
    hasard = random.randint(0,5)
    exo_pi()
    #if hasard == 0:
        #exo_pi()
    #elif hasard == 1:
        #exo_notes()
    #elif hasard == 2:
        #exo_de()
    #elif hasard == 3:
        #exo_vote()
    #elif hasard == 4:
        #exo_sport()    
    #else:
        #exo_ages()
    return (exo, cor)