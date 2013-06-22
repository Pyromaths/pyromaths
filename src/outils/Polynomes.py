# -*- coding: utf-8 -*-
from ..classes.Polynome import Polynome
from .Arithmetique import pgcd

from random import randint,randrange
from math import *


#--------------outils pour la class Polynome----------------------

def TeX_division(dividende,diviseur):
    '''renvoie une chaine de caractere TeX pour afficher la division en détail'''
    quotient=Polynome({0:0})
    texquotient,restera= dividende/diviseur
    reste=dividende
    diviseur_degre=diviseur.deg
    sauve=min(dividende.puiss+restera.puiss)
    longueur=dividende.degre_max-sauve
    string= "$$\\renewcommand\\arraycolsep{0cm}\n\\begin{array}{c"
    for i in range(longueur):
        string+= "c"
    string+= "|c}\n"
    string+=tab_print(dividende,longueur+1)
    string+= str(diviseur)+ "\\\\\n"
    string+= "\\cline{"+str(dividende.deg+2-sauve)+"-"+str(dividende.deg+2-sauve)+"}\n"
    i=0
    while reste.deg>=diviseur.deg:
        for k in range(i):
            string+= " &"
        ajout_quotient_deg=reste.deg-diviseur_degre
        facteur= reste.dictio[max(0,reste.deg)]/diviseur.dictio[diviseur.deg]
        ajout_quotient=Polynome({ajout_quotient_deg:facteur},var=dividende.var)
        soustrait_reste=ajout_quotient*diviseur
        string +=tab_print(soustrait_reste,diviseur_degre+1-sauve,parenthese=True)
        for k in range(longueur-i-diviseur.deg+sauve):
            string+= " & "
        if i ==0:
            string+= str(texquotient)
        string+= "\\\\\n"
        string+= "\\cline{"+str(i+1) +"-"+str(i+diviseur.deg+1-sauve) +"}\n"
        avant=reste.deg
        reste=reste-soustrait_reste
        delta=avant-reste.degre_max
        for k in range(i):
            string+= " &"
        i=i+delta
        prochain=1
        string +=tab_print(reste,min(diviseur.deg+1,reste.degre_max+1)+delta-sauve,debut=delta)
        #fait descendre les monome du dividende
        for k in range(longueur-i-diviseur.deg+sauve):
            string+= " & "
        string+= "\\\\ \n"
    string+= "\\end{array}\n$$"

    string+=_("\n On a $$")+dividende.TeX()+" = \\left(" + texquotient.TeX()+_("\\right) \\times \\left(")+diviseur.TeX()+"\\right)"
    if restera!=Polynome(0):
        if len(restera.puiss)==1 and restera[restera.deg]>0:#monome
            string +="+"+restera.TeX()
        else:
            string+="+\\left("+restera.TeX()+"\\right)"
    string+="$$"
    return string

def tab_print(polynome,longueur=0,parenthese=False,debut=0):
    '''utilisé par TeX_division pour décaler le reste dans la partie gauche'''
    degre=polynome.degre_max+debut
    string=''
    if parenthese:
        string = "-("
        fin=")"
    else:
        fin=""
    if polynome==0:
        string += "+"+str(0)+ " &"
    else:
        for i in range(longueur):
            k=degre-i
            coeff=polynome.dictio.get(k,0)
            if coeff>=0:
                string+= "+"
            string += str(coeff)
            if k!=0:
                string+= polynome.var
            if k != 1 and k!=0:
                string+= u"^" + str(k)
            if longueur-i==1:
                    string+= fin
            string+= " & "
    return string

########################################################
#
#  construction de polynôme de degré 2
#  X est un Polynome
#  X=Polynome("x","x") donnera un polynome de degré 2
#  X=Polynome("x^2",x) donnera un polynôme bicarrée
#
########################################################
def poly_racines_quelconques(abs_a,abs_b,abs_c,X):
    '''renvoie un polynome de degré 2'''
    '''abs_a,abs_b,abs_c sont des entiers positifs majorant les valeurs absolues de a, b ,c'''
    
    a3=(2*randrange(2)-1)*randrange(1,abs_a+1)
    b3=randrange(abs_b)
    c3=randrange(-abs_c,abs_c)
    return a3*X**2+b3*X+c3
def poly_racines_fractionnaires(rac_min,rac_max,denom1,X):
    '''renvoie un polynome de degré2 à racines fractionnaires '''
    '''les racines sont comprises entre rac_min et rac_max'''
    '''denom1 majore le dénominateur des racines'''
    while 1:
        #pour éviter P=77x^2
        a2=2*randrange(2)-1 #a2=-1 ou 1
        p2facteur=[randint(1,denom1)*X-randint(rac_min,rac_max)for i in range(2)]
        pol2=a2*p2facteur[0]*p2facteur[1]
        if pol2[1]!=0 and pol2[0]!=0:
            break
    pol2=pol2.simplifie()
    simplifie=abs(pgcd(pgcd(int(pol2[0]),int(pol2[1])),int(pol2[2])))
    pol2= pol2/simplifie
    pol2=pol2.simplifie()
    pol2.var = X.var
    return pol2

def poly_racines_entieres(rac_min,rac_max,X,a1=1):
    
    while 1:
        p1facteur=[X-randrange(rac_min,rac_max) for i in range(2)]
        pol1=a1*p1facteur[0]*p1facteur[1]
        if pol1[1]!=0 or pol1[1]!=0:
            break
    return pol1

def poly_id_remarquables(rac_min,rac_max,X):
    '''Renvoie un polynome obtenu par une identité remarquable'''
    '''et sgns 
         -2 => (a-b)²
         +2 => (a+b)²
          0 => (a-b)(a+b)'''
    a=randint(1,10)
    while 1:
        coeff=randrange(rac_min,rac_max)
        racine=randrange(rac_min,rac_max)
        if coeff!=0 and racine!=0:
            break
    sgns=[[-1,1][randrange(2)]for i in range(2)]
    p1facteur=[coeff*X+sgns[i]*racine for i in range(2)]
    return a*p1facteur[0]*p1facteur[1],sum(sgns)   
        #sum(sgns) permet de connaître l'identité remarquable
        # -2 => (a-b)²
        # +2 => (a+b)²
        # 0 => (a-b)(a+b)

 #----------polynome de degré 3-------------
def poly_degre3_racines_entieres(rac_min,rac_max,X,racines=[-2,-1,0,1,2]):
    racine_evidente=racines[randrange(len(racines))]
    return (X-racine_evidente)*poly_racines_entieres(rac_min,rac_max,X)
def poly_degre3_racines_fractionnaires(rac_min,rac_max,denom1,X,racines=[-2,-1,0,1,2]):
    racine_evidente=racines[randrange(len(racines))]
    return (X-racine_evidente)*poly_racines_fractionnaires(rac_min,rac_max,denom1,X)
def poly_degre3_racines_quelconques(abs_a,abs_b,abs_c,X,racines=[-2,-1,0,1,2]):
    racine_evidente=racines[randrange(len(racines))]
    return (X-racine_evidente)*poly_racines_quelconques(abs_a=1,abs_b=10,abs_c=10,X=X)


