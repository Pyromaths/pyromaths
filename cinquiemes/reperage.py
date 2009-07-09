# Pyromaths
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
# along with this program; if notPopen, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301 USA

import random
from outils import sepmilliers

def noms_sommets(nb):
    """Renvoie nb noms de sommets"""
    (listenb, listepts) = ([], [])
    for i in xrange(26):
        listenb.append(i + 65)
    for i in xrange(nb):
        listepts.append(str(unichr(listenb.pop(random.randrange(26 - i)))))
    listepts.sort()
    return tuple(listepts)

def angle(coordo):
    """Angle pour placer le nom du point en fonction du quadrant"""
    l=[]
    for coord in coordo:
        if coord[0]>=0 and coord[1]>=0:
            ang='45'
        if coord[0]>=0 and coord[1]<0:
            ang='-45'
        if coord[0]<0 and coord[1]<0:
            ang='-135'
        if coord[0]<0 and coord[1]>=0:
            ang='135'


        l.append(ang)
    return l

def place_points(coordo,points):
    """coordo: liste de coordonnées ;
    points : noms des points associés
    génère le code latex pour placer tous les points"""
    l= angle(coordo)
    text="\\pstGeonode[PointSymbol=x,PosAngle={"
    for ang in l :
        text=text+ang+','
    text=text+"},PointNameSep=0.4]"
    i=0
    while i<len(coordo):
        text=text+str(coordo[i])+"{"+str(points[i])+"}"
        i=i+1
    return text

def valide(coord,liste_coord):
    """Évite deux points trop proches l'un de l'autre"""
    rep=True
    for c in liste_coord:
        if abs(coord[0]-c[0])<=0.5 and abs(coord[1]-c[1])<=0.5:
            rep=False
            break
    return rep

def quadrant(coord,liste_coord):
    """Évite 2 points dans le même quadrant"""
    rep= True
    for c in liste_coord:
        if coord[0]*c[0]>=0 and coord[1]*c[1]>=0:
            rep=False
            break
    return rep


def coordo_pts(nb):
    """Génère une liste de nb coordonnées. Je m'arrange pour avoir des points sur les 4 quadrants
    et sur les deux axes"""
    j=0
    k=0
    l=[]
    i=0
    while i<4 and i<nb:
        j=j+1
        if j==600:
            break
        a=float(random.randrange(-9,10))/2
        b=float(random.randrange(-9,10))/2
        if ((a,b) not in l) and valide((a,b),l)and quadrant((a,b),l):
            l.append((a,b))
            i=i+1
    if nb>=4:
        a=float(random.randrange(-9,10))/2
        while not valide((0,a),l):
            a=float(random.randrange(-9,10))/2
        rg=random.randrange(0,len(l)-1)
        l[rg:rg]=[(0,a)]
        i=i+1

    if nb>=5:
        b=float(random.randrange(-9,10))/2
        while not valide((b,0),l):
            b=float(random.randrange(-9,10))/2
        rg=random.randrange(0,len(l)-1)
        l[rg:rg]=[(b,0)]
        i=i+1


    while i>=6 and i<nb and i<10:
        a=float(random.randrange(-9,10))/2
        b=float(random.randrange(-9,10))/2
        j=j+1
        if j==600:
            break
        if ((a,b) not in l) and valide((a,b),l)and quadrant((a,b),l[6:i]):
            l.append((a,b))
            i=i+1
    if nb>=11 and len(l)==10:
        a=float(random.randrange(-9,10))/2
        while not valide((0,a),l):
            a=float(random.randrange(-9,10))/2
        rg=random.randrange(6,len(l)-1)
        l[rg:rg]=[(0,a)]
        i=i+1
    if nb>=11 and len(l)==11:
        b=float(random.randrange(-9,10))/2
        while not valide((b,0),l):
            b=float(random.randrange(-9,10))/2
        rg=random.randrange(6,len(l)-1)
        l[rg:rg]=[(b,0)]
        i=i+1

    while i>=12 and i<nb :
        a=float(random.randrange(-9,10))/2
        b=float(random.randrange(-9,10))/2
        k=k+1
        if k==600:
            break
        if ((a,b) not in l) and valide((a,b),l):
            l.append((a,b))
            i=i+1
    return l


def affiche_coord(coord):
    """Affiche les coordonnées des points au format LaTeX"""
    return '\\hbox{('+sepmilliers(str(coord[0]))+'~;~'+sepmilliers(str(coord[1]))+')}'

def tex_liste_co(liste_coord):
    """prend une liste de coordonnées et renvoie la liste en string prête pour latex
    #\hbox évite que les coordonnées soient coupées à l'affichage"""
    i=0
    tlc=[]
    while i < len(liste_coord):
        tlc.append('\\hbox{('+sepmilliers(str(liste_coord[i][0]))+'~;~'+sepmilliers(str(liste_coord[i][1]))+')}')
        i=i+1
    return tlc

def main():
    nbpts = 13
    noms_pts=(noms_sommets(nbpts))
    coord_pts=coordo_pts(nbpts)
    voc=['ordonn\\\'ee','abscisse']
    rg1=random.randrange(0,2)
    rg2=abs(rg1-1)
    while len(coord_pts)<nbpts:
        coord_pts=coordo_pts(nbpts)
    exo=["\\exercice",
         "\\parbox{0.4\\linewidth}{",
         "\\begin{enumerate}",
         "\\item Donner les coordonn\\\'ees des points %s, %s, %s, %s, %s et %s." % tuple(noms_pts[0:6]),
         "\\item Placer dans le rep\\`ere les points %s, %s, %s, %s, %s et %s" %noms_pts[6:12] +" de cordonn\\\'ees respectives %s, %s, %s, %s, %s et %s. " %tuple(tex_liste_co(coord_pts[6:12])),
         "\\item Placer dans le rep\\`ere le point %s d'%s %s et d'%s %s" %(noms_pts[12],voc[rg1],sepmilliers(str(coord_pts[12][rg1])),voc[rg2],sepmilliers(str(coord_pts[12][rg2]))),
         "\\end{enumerate}}\\hfill ",
         "\\parbox{0.55\\linewidth}{",
         "\\psset{unit=0.8cm}",
         "\\begin{pspicture}(-4.95,-4.95)(4.95,4.95)",
         "\\psgrid[subgriddiv=2, subgridcolor=lightgray, gridlabels=8pt](0,0)(-5,-5)(5,5)",
         "\\psline[linewidth=1.2pt]{->}(-5,0)(5,0)",
         "\\psline[linewidth=1.2pt]{->}(0,-5)(0,5)",
         place_points(coord_pts[0:6],noms_pts[0:6]),
         "\\end{pspicture}}"]
    cor=["\\exercice",
         "\\parbox{0.4\\linewidth}{",
         "\\psset{unit=0.8cm}",
         "\\begin{pspicture}(-5,-5)(5,5)",
         "\\psgrid[subgriddiv=2, subgridcolor=lightgray, gridlabels=8pt](0,0)(-5,-5)(5,5)",
         "\\psline[linewidth=1.2pt]{->}(-5,0)(5,0)",
         "\\psline[linewidth=1.2pt]{->}(0,-5)(0,5)",
         place_points(coord_pts[0:13],noms_pts[0:13]),
         "\\end{pspicture}}\\hfill",
         "\\parbox{0.5\\linewidth}{",
         "\\begin{enumerate}",
         "\\item Donner les coordonn\\\'ees des points %s, %s, %s, %s, %s et %s." % tuple(noms_pts[0:6])]
    i=0
    while i<6:
        cor.append("Les coordonn\\\'ees du point %s sont %s \n"%(noms_pts[i],affiche_coord(coord_pts[i])))
        i=i+1
    cor[len(cor):len(cor)]=["\\item Placer dans le rep\\`ere les points %s, %s, %s, %s, %s et %s" %noms_pts[6:12] +" de cordonn\\\'ees respectives %s, %s, %s, %s, %s et %s. " %tuple(tex_liste_co(coord_pts[6:12])),
         "\\item Placer dans le rep\\`ere le point %s d'%s %s et d'%s %s" %(noms_pts[12],voc[rg1],sepmilliers(str(coord_pts[12][rg1])),voc[rg2],sepmilliers(str(coord_pts[12][rg2]))),
         "\\end{enumerate}"]
    cor.append("}")
    return(exo,cor)

