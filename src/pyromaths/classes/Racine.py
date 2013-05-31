# -*- coding: utf-8 -*-

from pyromaths.outils.decimaux import decimaux
from pyromaths.outils.Arithmetique import carrerise, pgcd, ppcm, factor
from math import sqrt
from Fractions import Fractions

def produitfacteurs(facteurs):
    """Affiche sous forme de produit les éléments d'une liste."""
    prodfacteurs = ''
    for element in facteurs:
        prodfacteurs += str(element) + ' \\times '
    return prodfacteurs[:-7]

class Racine:
    def __init__(self, radicande, coeff = 1, indice = 2):
        if (radicande < 0) or not (isinstance(indice, int)):
            print "Erreur de définition ! Le radicande doit être positif et l'indice un nombre entier !"
        self.radicande = radicande
        self.indice = indice # Nombre entier
        self.coeff = coeff # Coeff devant la racine

    def __add__(self, other):
        if not (isinstance(other, Racine)):
            return str(self) + " + " + str(other)
        if (self.radicande == other.radicande) and (self.indice == other.indice):
            return [str(self.simplifie()[0]) + "+" + str(other.simplifie()[0]), Racine(self.radicande, self.coeff + other.coeff, self.indice)]
        else:
            return str(self) + " + " + str(other)

    def __radd__(self, other):
        return self + other

    def __sub__(self, other):
        if not (isinstance(other, Racine)):
            return str(self) + " + " + str(other)
        if (self.radicande == other.radicande) and (self.indice == other.indice):
            return Racine(self.radicande, self.coeff - other.coeff, self.indice)
        else:
            return (str(self) + " - " + str(other), "tset")

    def __rsub__(self, other):
        return -(self - other)

    def __mul__(self, other):
        if (isinstance(other, float)) or (isinstance(other, int)):
            return Racine(self.radicande, self.coeff * other, self.indice)
        elif self.indice == other.indice:
            return Racine(self.radicande * other.radicande, self.coeff * other.coeff, self.indice)
        else:
            return str(self) + ' x ' + str(other)

    def __rmul__(self, other):
        return self * other

    def __div__(self, other):
        if (isinstance(other, float)) or (isinstance(other, int)):
            return Racine(self.radicande, self.coeff / other, self.indice)
        elif self.indice == other.indice:
            return Racine(self.radicande / float(other.radicande), self.coeff / float(other.coeff), self.indice)
        else:
            return str(self) + ' / ' + str(other)

    def __rdiv__(self, other):
        if (isinstance(other, float)) or (isinstance(other, int)):
            return Racine(self.radicande, other / float(self.coeff * self.radicande), self.indice)
        elif self.indice == other.indice:
            return Racine(other.radicande / float(self.radicande), other.coeff / float(self.coeff), self.indice)
        else:
            return str(other) + ' / ' + str(self)

    def __str__(self):
        if self.coeff == 0:
            return "0"
        else:
            if self.coeff == 1:
                coeff = ""
            else:
                coeff = decimaux(self.coeff, 1) + " \\, "
            if self.radicande == 0:
                coeff = ""
                racine = ""
                radicande = "0"
            elif self.indice == 2:
                racine = "\\sqrt{"
                radicande = decimaux(self.radicande, 1) + "}"
            else:
                racine = "\\sqrt[{0}]{{".format(self.indice)
                radicande = decimaux(self.radicande, 1) + "}"
            return coeff + racine + radicande

    def simplifie(self):
        facteurs = factor(self.radicande)
        prodfacteurs = produitfacteurs(facteurs)
        if self.indice == 2:
            racine = "\\sqrt{"
        else:
            racine = "\\sqrt[{0}]{{".format(self.indice)
        coeff = self.coeff
        radicande = self.radicande
        detail = [str(self), ' = ', str(coeff) + racine + prodfacteurs + '}']
        for element in facteurs:
            if facteurs.count(element) % self.indice == 0:
                coeff *= element
                for n in range(self.indice):
                    facteurs.remove(element)
                radicande = radicande // (element**(self.indice))
                prodfacteurs = produitfacteurs(facteurs)
                detail.append(' = ')
                detail.append(str(coeff) + ' \\times ' + racine + prodfacteurs + '}')
        if radicande == 1:
            return (coeff, detail)
        else:
            return (Racine(radicande, coeff, self.indice), detail)

def simplifie_racine(n):
    '''renvoie coeff,radicande où sqrt(n)=coeff*sqrt(radicande)'''
    if n==0:
        return 0,0
    else:
        ncar=carrerise(n)
        return int(sqrt(n//ncar)),ncar


def pTeX(n):
    """renvoie (n) si n<0"""
    if n<0:
        return "("+decimaux(n)+")"
    else:
        return decimaux(n)
    
def tTeX(n):
    if n==1:
        return ""
    elif n==-1:
        return "-"
    elif n>=0:
        return "+"+decimaux(n)
    else:
        return decimaux(n)



class RacineDegre2:
    def __init__(self,numerateur=0,denominateur=1,coeff=1,radicande=0):
        """Constructeur de la forme (a+c*racine(d))/b"""
        self.numerateur=numerateur # a
        self.denominateur=denominateur # b
        self.coeff=coeff # c
        self.radicande=radicande # d

    def __str__(self):
        if isinstance(self.numerateur,str):
            #utilisé dans le détail de la simplification
            numerateur=self.numerateur
        else:
            numerateur=decimaux(self.numerateur)*(self.numerateur!=0)   #renvoie "" si self.numerateur=0
        if self.radicande!=0:
            if isinstance(self.coeff,str):#utilisé dans le détail de la simplification
                if self.coeff[0]!="-" and self.coeff[0]!="+":
                    numerateur+="+"
                numerateur+=self.coeff+"\\sqrt{"+decimaux(self.radicande)+"}"
            elif self.coeff==1:
                numerateur+="+\\sqrt{"+decimaux(self.radicande)+"}"
            elif self.coeff==-1:
                numerateur+="-\\sqrt{"+decimaux(self.radicande)+"}"
            else:
                numerateur+=tTeX(self.coeff)+"\\sqrt{"+decimaux(self.radicande)+"}"
        if numerateur=='':
            numerateur = '0'
        if self.denominateur==1:
            result=numerateur
        else:
            result="\\dfrac{%s}{%s}"%(numerateur,self.denominateur)

        if result[0]=='+':
            return result[1:]
        else:
            return result

    def simplifie(self,detail=False):
        liste_detail=[]
        coeff,radicande=simplifie_racine(self.radicande)
        numerateur=self.numerateur
        if self.radicande!=0:
            if self.coeff==1:
                    det_coeff="+ "
            elif self.coeff==-1:
                det_coeff="- "
            else:
                det_coeff="%s\\times "%(self.coeff)
            if coeff!=1 or radicande==1:
                det_coeff+=str(coeff)
        else:
            det_coeff="0"
        if radicande==1:
            #det_coeff="%s\\times%s"%(tTeX(self.coeff),coeff)
            liste_detail.append("\\dfrac{%s %s}{%s}"%\
                                    (self.numerateur,det_coeff ,self.denominateur))
            radicande=0
            numerateur=self.numerateur+(self.coeff)*int(coeff)
            coeff=0

        if coeff!=1:
            liste_detail.append(str(RacineDegre2(numerateur,
                                                 self.denominateur,
                                                 det_coeff,
                                                 radicande)))

        coeff=(self.coeff)*int(coeff)

        simplifie=pgcd(pgcd(coeff,numerateur),self.denominateur)
        numerateur=numerateur//simplifie
        coeff=coeff//simplifie
        denominateur=self.denominateur//simplifie
        if simplifie!=1:
            if radicande!=0 or denominateur!=1:
                det_numerateur="%s_{\\times %s}"%(numerateur,pTeX(simplifie))
                det_denominateur="%s_{\\times %s}"%(denominateur,pTeX(simplifie))
                det_coeff="%s_{\\times %s}"%(coeff,pTeX(simplifie))
                liste_detail.append(str(RacineDegre2(det_numerateur,det_denominateur,det_coeff,radicande)))
            liste_detail.append(str(RacineDegre2(numerateur,denominateur,coeff,radicande)))
        if detail:
            return RacineDegre2(numerateur,denominateur,coeff,radicande),liste_detail
        return RacineDegre2(numerateur,denominateur,coeff,radicande)

    def __add__(self,other):
        if isinstance(other,RacineDegre2):
            if self.radicande==other.radicande or self.radicande==0 or other.radicande==0:
                radicande=max(self.radicande,other.radicande)
                premier,second=self,other
            else:
                premier=self.simplifie()
                second=other.simplifie()
                if self.radicande==other.radicande or self.radicande==0 or other.radicande==0:
                    radicande=max(self.radicande,other.radicande)
                else:
                    return NotImplemented

            denominateur=ppcm(premier.denominateur,second.denominateur)
            facteur1=denominateur/premier.denominateur
            facteur2=denominateur/second.denominateur
            #if self.radicande==other.radicande:
            coeff=premier.coeff*facteur1*(premier.radicande!=0)+second.coeff*facteur2*(second.radicande!=0)
            if coeff==0:
                radicande=0
            return RacineDegre2(premier.numerateur*facteur1+second.numerateur*facteur2,
                                denominateur,
                                coeff,
                                radicande)
        elif isinstance(other,int):
            return self + RacineDegre2(other)
        elif isinstance(other,Fractions):
            return self + RacineDegre2(other.numerateur,other.denominateur)

    def __radd__(self,other):
        return self+other
    def __neg__(self):
        return RacineDegre2(-self.numerateur,self.denominateur,-self.coeff,self.radicande)

    def __sub__(self,other):
        return self+(-other)

    def __rsub__(self,other):
        return -self + other

    def __mul__(self,other):
        if isinstance(other,Fractions):
            return self*RacineDegre2(other.numerateur,other.denominateur,0,self.radicande)
        elif isinstance(other,int):
            return self*RacineDegre2(other,1,0,self.radicande)
        else:
            radicande=max(self.radicande,other.radicande)#cela autorise d'avoir un radicande=0 mais n'efface pas l'autre
            coeff=self.numerateur*(other.coeff*(other.radicande!=0))+(self.coeff*(self.radicande!=0))*other.numerateur
            if coeff==0:
                radicande=0
            numerateur=self.numerateur*other.numerateur+(self.coeff*other.coeff)*(not(self.radicande==0 or other.radicande==0))*self.radicande
            return RacineDegre2(numerateur,
                            self.denominateur*other.denominateur,
                            coeff,
                            radicande)
    def __invert__(self):
        return self.denominateur*RacineDegre2(self.numerateur,self.numerateur**2-self.coeff**2*self.radicande,-self.coeff,self.radicande)
    def __div__(self,other):
        return self*~other
    def __rdiv__(self,other):
        return ~self*other
    def __rmul__(self,other):
        return self*other
    def __pow__(self,n):
        result=1
        for i in range(n):
            result=result*self
        return result
    def __float__(self):
        return (self.numerateur+self.coeff*sqrt(self.radicande))/self.denominateur
    def __cmp__(self,other):
        comp=float(self)-float(other)
        if comp>0:
            return 1
        elif comp<0:
            return -1
        else:
            return 0

