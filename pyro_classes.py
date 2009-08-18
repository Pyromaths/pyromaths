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

import outils
import string
import math
import os
from outils import radians, degres


class Fractions:

    """Classe permettant d'op\xc3\xa9rer sur les fractions.
    Une fraction est stock\xc3\xa9e ainsi : (num\xc3\xa9rateur, d\xc3\xa9nominateur)"""

    def __init__(self, n, d=1):
        self.n = n
        self.d = d

    def simplifie(self):

        # retourne la fraction rendue irréductible

        pgcd = outils.pgcd(self.n, self.d)
        return Fractions(self.n / pgcd, self.d / pgcd)

    def TeX(self, signe=0, coef=None):
        """Permet d'\xc3\xa9crire une fraction au format TeX.

        @param signe: Si vrai, \xc3\xa9crit la fraction avec un d\xc3\xa9nominateur positif
        @param coef: Multiplie le num\xc3\xa9rateur et le d\xc3\xa9nominateur par un m\xc3\xaame nombre
        """

        if signe:
            (self.n, self.d) = ((self.n * abs(self.d)) / self.d, abs(self.d))
        if self.n:
            if coef and coef != 1:
                text = "\\dfrac{%s_{\\times %s}}{%s_{\\times %s}}" % (self.n,
                        coef, self.d, coef)
            elif self.d != 1:
                text = "\\dfrac{%s}{%s}" % (self.n, self.d)
            else:
                text = "%s" % self.n
        else:
            text = "0"
        return text

    def TeXProduit(self, fraction):
        if self.d < 0:
            (self.n, self.d) = (-self.n, -self.d)
        if fraction.d < 0:
            (fraction.n, fraction.d) = (-fraction.n, -fraction.d)
        c1 = abs(outils.pgcd(self.n, fraction.d))
        c2 = abs(outils.pgcd(self.d, fraction.n))
        simplifiable = 0  # permet de savoir si on a simplifiée le produit
        if c1 > 1:
            n1 = "%s \\times \\cancel{%s}" % (self.n / c1, c1)
            d2 = "%s \\times \\cancel{%s}" % (fraction.d / c1, c1)
        else:
            n1 = self.n
            d2 = fraction.d
        if c2 > 1:
            d1 = "%s \\times \\bcancel{%s}" % (self.d / c2, c2)
            n2 = "%s \\times \\bcancel{%s}" % (fraction.n / c2, c2)
        else:
            d1 = self.d
            n2 = fraction.n
        return "%s \\times %s" % (Fractions.TeX(Fractions(n1, d1), signe=
                                  None), Fractions.TeX(Fractions(n2, d2),
                                  signe=None))

    def TeXSimplifie(self):
        frs = Fractions.simplifie(self)
        coef = abs(self.n / frs.n)
        if coef > 1:
            texte = \
                "\\dfrac{%s_{\\times \\cancel %s}}{%s_{\\times \\cancel %s}}" % \
                (self.n / coef, coef, self.d / coef, coef)
        else:
            texte = Fractions.TeX(self, signe=None)
        return texte

    def __add__(self, fraction):
        ppcm = outils.ppcm(self.d, fraction.d)
        return Fractions((self.n * ppcm) / self.d + (fraction.n * ppcm) /
                         fraction.d, ppcm)

    def __sub__(self, fraction):
        ppcm = outils.ppcm(self.d, fraction.d)
        return Fractions((self.n * ppcm) / self.d - (fraction.n * ppcm) /
                         fraction.d, ppcm)

    def __mul__(self, fraction):
        return Fractions(self.n * fraction.n, self.d * fraction.d)

    def __div__(self, fraction):
        return Fractions(self.n * fraction.d, self.d * fraction.n)


class Litteral:

    """Classe permettant d'op\xc3\xa9rer sur des expressions litt\xc3\xa9rales
    Une expression litt\xc3\xa9rale est stock\xc3\xa9e ainsi :
    [(coeff1, variable1, exposant1), (coeff2, variable2, exposant2), ...]"""

    def __init__(self, expression):
        self.e = expression

    def reduit(self):

        # retourne l'expression réduite, en supprimant les coefficients nuls,
        # excepté s'il est de degré 0.

        expression = sorted(self.e, key=lambda x: (x[1], -x[2]))
        (expr, i) = ([expression[0]], 1)
        for i in xrange(1, len(expression)):
            if expr:
                if expr[-1][1] == expression[i][1] and expr[-1][2] == \
                    expression[i][2]:
                    if expr[-1][0] + expression[i][0] or expr[-1][2] == \
                        0:
                        expr.append((expr.pop(-1)[0] + expression[i][0],
                                    expression[i][1], expression[i][2]))
                    else:
                        expr.pop(-1)
                else:
                    expr.append(expression[i])
            else:
                expr.append(expression[i])

        return Litteral(expr)

    def oppose(self):

        # retourne l'opposé d'une expression littérale

        expr = self.e
        expression = []
        for i in xrange(len(expr)):
            expression.append((-expr[i][0], expr[i][1], expr[i][2]))
        return Litteral(expression)

    def __add__(self, expression):
        expr1 = self.e
        expr2 = expression.e
        expr1.extend(expr2)
        return Litteral.reduit(Litteral(expr1))

    def __sub__(self, expression):
        expr1 = self.e
        expr2 = Litteral.oppose(expression).e
        expr1.extend(expr2)
        return Litteral.reduit(Litteral(expr1))

    def __mul__(self, expression):
        expr1 = self.e
        expr2 = expression.e
        expression = []
        for i in xrange(len(expr1)):
            for j in xrange(len(expr2)):
                if expr1[i][1] == expr2[j][1]:
                    expression.append((expr1[i][0] * expr2[j][0], expr1[i][1],
                            expr1[i][2] + expr2[j][2]))
                else:
                    pass

                    # TODO: Cas du produit de deux expressions à plusieurs variables

        return Litteral.reduit(Litteral(expression))


class Metapost:

    def __init__(self):
        self.text = []
        self.num = 1

    def fin(self):
        self.text.append("end;")
        return self

    def triangle(
        self,
        A,
        B,
        C,
        a=0,
        b=0,
        c=0,
        alpha=0,
        beta=0,
        gamma=0,
        rotation=0,
        angledroit=0,
        ):
        """Construit un triangle en metapost quelles que soient les donn\xc3\xa9es.
        La base est le c\xc3\xb4t\xc3\xa9 [AB] de longueur c.

        @param A, b, C : nom des trois sommets (obligatoire)
        @param a, b, c : longueurs des trois c\xc3\xb4t\xc3\xa9s oppos\xc3\xa9s au sommet de m\xc3\xaame nom
        @param alpha, beta, gamma : mesure des 3 angles de sommets A, B et C
        @param rotation: mesure en degr\xc3\xa9s de l'angle de la rotation de centre A
                         appliqu\xc3\xa9e au triangle
        @param angledroit: doit-on afficher l'angle droit ?
        """

        self.text.append("beginfig(%s);\n" % self.num)
        self.text.append("u:=1cm;\n")
        self.text.append("pair %s, %s, %s, m[];\n" % (A, B, C))
        self.text.append("picture $;\n")
        self.text.append("  %s=origin;\n" % A)
        if angledroit:
            marques=[0, 0, 0, "%s \degres" % alpha, "%s \degres" % beta, "%s \degres" % gamma]
            if a: marques[0]="%s cm" % a
            if b: marques[1]="%s cm" % b
            if c: marques[2]="%s cm" % c
            points=[A, B, C]
        #on donne les trois longueurs des 3 côtés

        if a and b and c:
            alpha = degres(math.acos(((b ** 2 + c ** 2) - a ** 2 * 1.) / ((2 *
                     b) * c)))
            beta = degres(math.acos(((c ** 2 + a ** 2) - b ** 2 * 1.) / ((2 *
                    c) * a)))
        elif a and b and gamma:

        # Un angle et les deux côtés adjacents

            (c, beta, alpha) = self.triangle_angle_cotes_adjacents(a, b,
                    gamma)
        elif b and c and alpha:
            (a, gamma, beta) = self.triangle_angle_cotes_adjacents(b, c,
                    alpha)
        elif c and a and beta:
            (b, alpha, gamma) = self.triangle_angle_cotes_adjacents(c, a,
                    beta)
        elif b and c and beta:

        # Un angle, le côté opposé et un côté adjacent

            (a, alpha, gamma) = self.triangle_angle_cote_adjacent_cote_oppose(b,
                    c, beta)
        elif b and a and beta:
            (c, gamma, alpha) = self.triangle_angle_cote_adjacent_cote_oppose(b,
                    a, beta)
        elif a and b and alpha:
            (c, gamma, beta) = self.triangle_angle_cote_adjacent_cote_oppose(a,
                    b, alpha)
        elif a and c and alpha:
            (b, beta, gamma) = self.triangle_angle_cote_adjacent_cote_oppose(a,
                    c, alpha)
        elif c and a and gamma:
            (b, beta, alpha) = self.triangle_angle_cote_adjacent_cote_oppose(c,
                    a, gamma)
        elif c and b and gamma:
            (a, alpha, beta) = self.triangle_angle_cote_adjacent_cote_oppose(c,
                    b, gamma)
        elif alpha and beta and c:

        # Deux angles et le côté commun

            pass  # on sait faire
        elif beta and gamma and a:
            c = (a * math.sin((gamma * math.pi) / 180)) / math.sin(((beta +
                    gamma) * math.pi) / 180)
            alpha = (180 - beta) - gamma
        elif alpha and gamma and b:
            c = (b * math.sin((gamma * math.pi) / 180)) / math.sin(((alpha +
                    gamma) * math.pi) / 180)
            beta = (180 - alpha) - gamma
        elif a and alpha and beta:

        # Deux angles et un côté non commun

            c = (a * math.sin(((alpha + beta) * math.pi) / 180)) / math.sin((alpha *
                    math.pi) / 180)
        elif a and alpha and gamma:
            c = (a * math.sin((gamma * math.pi) / 180)) / math.sin((alpha *
                    math.pi) / 180)
            beta = (180 - alpha) - gamma
        elif b and beta and alpha:
            c = (b * math.sin(((alpha + beta) * math.pi) / 180)) / math.sin((beta *
                    math.pi) / 180)
        elif b and beta and gamma:
            c = (b * math.sin((gamma * math.pi) / 180)) / math.sin((beta *
                    math.pi) / 180)
            alpha = (180 - beta) - gamma
        elif c and alpha and gamma:
            beta = (180 - alpha) - gamma
        elif c and beta and gamma:
            alpha = (180 - beta) - gamma
        alpha = alpha + rotation
        beta = beta - rotation


        self.text.append("  %s= (%s*u, 0) rotated %s;\n" % (B, c, rotation))
        self.text.append("  %s = %s + whatever*dir(%s);\n" % (C, A, alpha))
        self.text.append("  %s = %s + whatever*dir(180-%s);\n" % (C, B, beta))
        self.text.append("  draw %s -- %s -- %s -- cycle;\n" % (A, B, C))

        # Codage de l'angle droit s'il y en a un.

        if angledroit:
            if alpha - rotation == 90:
                self.text.append("  draw (%s+5*unitvector(%s-%s))--(%s+5*unitvector(%s-%s)+\n" % (A, B, A, A, B, A))
                self.text.append("      5*unitvector(%s-%s))--(%s+5*unitvector(%s-%s));\n" % ( C, A, A, C, A))
            elif beta + rotation == 90:
                self.text.append("  draw (%s+5*unitvector(%s-%s))--(%s+5*unitvector(%s-%s)+\n" % (B, A, B, B, A, B))
                self.text.append("      5*unitvector(%s-%s))--(%s+5*unitvector(%s-%s));\n" % (C, B, B, C, B))
            elif gamma == 90:
                self.text.append("  draw (%s+5*unitvector(%s-%s))--(%s+5*unitvector(%s-%s)+\n" % (C, A, C, C, A, C))
                self.text.append("      5*unitvector(%s-%s))--(%s+5*unitvector(%s-%s));\n" % ( B, C, C, B, C))
            for i in xrange(3):
                if marques[i]:
                    self.text.append("  m3:=unitvector(%s-%s) rotated 90;\n" % (points[(i+1)%3], points[(i+2)%3]))
                    self.text.append("  $:=image(\n")
                    self.text.append("    label(btex %s etex rotated angle(%s-%s),(%s+%s)/2+2mm*m3);\n" % (marques[i], points[(i+1)%3], points[(i+2)%3], points[(i+1)%3], points[(i+2)%3]))
                    self.text.append("    );\n  draw $;\n")
        self.text.append("  label.llft(btex $%s$ etex, %s);\n" % (A, A))
        self.text.append("  label.lrt(btex $%s$ etex, %s);\n" % (B, B))
        self.text.append("  label.top(btex $%s$ etex, %s);\n" % (C, C))
        self.text.append("""endfig;

""")
        self.num = self.num + 1
        return self

    def triangle_angle_cotes_adjacents(self, a, b, gamma):
        c = math.sqrt(a ** 2 + b ** 2 - 2 * a * b * math.cos(radians(gamma)))
        alpha = 90. - gamma / 2 + degres(math.atan((((a - b) * 1.) / (a + b)) /
                math.tan(radians(gamma / 2))))
        beta = 90. - gamma / 2 - degres(math.atan((a - b) * 1. / (a + b) /
                math.tan(radians(gamma / 2))))
        return (c, beta, alpha)

    def triangle_angle_cote_adjacent_cote_oppose(self, b, c, beta):
        if b <= c * math.sin((beta * math.pi) / 180):
            alpha = gamma = a = 0  # Pas possible de résoudre
        else:
            gamma = degres(math.asin(((c * math.sin((beta * math.pi) / 180)) /
                     b) * 1.))
            alpha = (180 - beta) - gamma
            a = math.sqrt(b ** 2 - c ** 2 * math.sin((beta * math.pi) /
                          180) ** 2) + c * math.cos((beta * math.pi) /
                    180)
        return (a, alpha, gamma)


class WriteFiles:

    def __init__(self, f0, f1, mp, entete=1):
        WriteFiles.f0 = open(f0, 'w', -1)  # fichier exercices
        WriteFiles.f1 = open(f1, 'w', -1)  # fichier corrige
        WriteFiles.mp = open(mp, 'w', -1)  # fichier metapost
        self.entete = entete
        entete = []
        if os.name == 'mac':
            fichier.write('%%!TEX TS-program = latex\n')
        entete.append('\\documentclass[a4paper,11pt]{article}\n')
        entete.append('\\usepackage[latin1]{inputenc}\n')
        entete.append('\\usepackage[T1]{fontenc}\n')
        entete.append('\\usepackage[frenchb]{babel}\n')
        entete.append('\\usepackage[fleqn]{amsmath}\n')
        entete.append('\\usepackage{amssymb,multicol,calc,vmargin,cancel,fancyhdr,units,pst-eucl,wrapfig,lastpage,wasysym,pst-plot,tabularx}\n')
        entete.append('\\setmarginsrb{1.5cm}{1.5cm}{1.5cm}{1.5cm}{.5cm}{.5cm}{.5cm}{1.cm}\n')
        entete.append('\\newcounter{exo}\n')
        entete.append('\\setlength{\\headheight}{18pt}\n')
        entete.append('\\setlength{\\fboxsep}{1em}\n')
        entete.append('\\setlength\\parindent{0em}\n')
        entete.append('\\setlength\\mathindent{0em}\n')
        entete.append('\\setlength{\\columnsep}{30pt}\n')
        entete.append('\\usepackage[ps2pdf,pagebackref=true,colorlinks=true,linkcolor=blue,plainpages=true]{hyperref}\n')
        entete.append('\\hypersetup{pdfauthor={J\xe9r\xf4me Ortais},pdfsubject={Exercices de math\xe9matiques},')
        entete.append('pdftitle={Exercices cr\xe9\xe9s par Pyromaths, un programme en Python de J\xe9r\\^ome Ortais}}\n')
        entete.append('\\makeatletter\n')
        entete.append('\\newcommand\\styleexo[1][]{\n')
        entete.append('  \\renewcommand{\\theenumi}{\\arabic{enumi}}\n')
        entete.append('  \\renewcommand{\\labelenumi}{$\\blacktriangleright$\\textbf{\\theenumi.}}\n')
        entete.append('  \\renewcommand{\\theenumii}{\\alph{enumii}}\n')
        entete.append('  \\renewcommand{\\labelenumii}{\\textbf{\\theenumii)}}\n')
        entete.append('  {\\fontfamily{pag}\\fontseries{b}\\selectfont \\underline{#1 \\theexo}}\n')
        entete.append('  \\par\\@afterheading\\vspace{0.5\\baselineskip minus 0.2\\baselineskip}}\n')
        entete.append('\\newcommand*\\exercice{%\n')
        entete.append('  \\psset{unit=1cm}\n')
        entete.append('  \\ifthenelse{\\equal{\\theexo}{0}}{}{\\filbreak}\n')
        entete.append('  \\refstepcounter{exo}%\n')
        entete.append('  \\stepcounter{nocalcul}%\n')
        entete.append('  \\par\\addvspace{1.5\\baselineskip minus 1\\baselineskip}%\n')
        entete.append('  \\@ifstar%\n')
        entete.append('  {\\penalty-130\\styleexo[Corrig\xe9 de l\'exercice]}%\n')
        entete.append('  {\\filbreak\\styleexo[Exercice]}%\n')
        entete.append('  }\n')
        entete.append('\\makeatother\n')
        entete.append('\\newlength{\\ltxt}\n')
        entete.append('\\newcounter{fig}\n')
        entete.append('\\newcommand{\\figureadroite}[2]{\n')
        entete.append(  '\\setlength{\\ltxt}{\\linewidth}\n')
        entete.append('  \\setbox\\thefig=\\hbox{#1}\n')
        entete.append('  \\addtolength{\\ltxt}{-\\wd\\thefig}\n')
        entete.append('  \\addtolength{\\ltxt}{-10pt}\n')
        entete.append('  \\begin{minipage}{\\ltxt}\n')
        entete.append('    #2\n')
        entete.append('  \\end{minipage}\n')
        entete.append('  \\hfill\n')
        entete.append('  \\begin{minipage}{\\wd\\thefig}\n')
        entete.append('    #1\n')
        entete.append('  \\end{minipage}\n')
        entete.append('  \\refstepcounter{fig}\n')
        entete.append('}\n')
        entete.append('\\count1=\\year \\count2=\\year \\ifnum\\month<8\\advance\\count1by-1\\else\\advance\\count2by1\\fi\n')
        entete.append('\\pagestyle{fancy}\n')
        entete.append('\\cfoot{\\textsl{\\footnotesize{Ann\xe9e \\number\\count1/\\number\\count2}}}\n')
        entete.append('\\rfoot{\\textsl{\\tiny{http://www.pyromaths.org}}}\n')
        entete.append('\\lhead{\\textsl{\\footnotesize{Page \\thepage/ \\pageref{LastPage}}}}\n')
        entete.append('\\begin{document}\n')
        entete.append('\\newcounter{nocalcul}[exo]\n')
        entete.append('\\renewcommand{\\thenocalcul}{\\Alph{nocalcul}}\n')
        entete.append('\\raggedcolumns\n')
        if self.entete:
            WriteFiles.f0.write(string.join(entete, ""))
            WriteFiles.f1.write(string.join(entete, ""))
            WriteFiles.f1.write('\\setlength{\\columnseprule}{0.5pt}\n')

    def write(self, exos):
        self.f0.write("\n")
        self.f1.write("\n")
        self.f0.writelines(x + "\n" for x in exos[0])
        self.f1.writelines(x + "\n" for x in exos[1])
        if len(exos) > 2:
            self.mp.writelines(x + "\n" for x in exos[2])

    def close(self):
        if self.entete:
            self.f0.write("\n\\end{document}")
            self.f1.write("\n\\end{document}")
        self.f0.close()
        self.f1.close()
        if self.mp.tell():
            self.mp.write("\n\\end;")
            self.mp.close()
        else:
            self.mp.close()
            os.remove(self.mp.name)

    def ecrit_enonce(self, formule, cadre=None, numcalcul=""):
        if numcalcul:
            numcalcul = '\\thenocalcul = '
        if formule:
            if cadre:
                self.f0.write('  \\[ \\boxed{%s%s} \\] \n' % (numcalcul,
                              formule))
            else:
                self.f0.write('  \\[ %s%s \\] \n' % (numcalcul, formule))

    def ecrit_corrige(self, formule, cadre=None, numcalcul=""):
        if numcalcul:
            numcalcul = '\\thenocalcul = '
        if formule:
            if cadre:
                self.f1.write('  \\[ \\boxed{%s%s} \\] \n' % (numcalcul,
                              formule))
            else:
                self.f1.write('  \\[ %s%s \\] \n' % (numcalcul, formule))

    def ecrit_metapost(self, formule):
        self.mp.write(formule)


    def copie_modele(self, source, destination):
        """Copie le contenu d'un modèle dans un nouveau fichier tex, en remplaçant les mots-clés par leur valeur, soit dans le fichier de config, soit les exercices."""
        fs = open(source, 'r')
        fd = open(destination, 'w')
        while 1:
            txt = fs.readline()
            if txt =="":
                break
            temp = re.findall('##{{[A-Z]*}}##',txt)
            if temp:
              occ = temp[0][4:len(temp)-5].lower()
            else:
              occ = ""
            ### Il faut encore ajouter un filtre pour différencier mots-clés du dico et exercices
            txt = re.sub('##{{[A-Z]*}}##',occ,txt)
            fd.write(txt)
        fs.close()
        fd.close()
        return


class TeXMiseEnForme:

    def __init__(self, text):
        self.text = text

    def monome(self, coef, var, bplus=0, bpn=0, bpc=0):

        # coef est le coefficient à écrire devant la variable var
        # bplus est un booleen : s'il est vrai, il faut ecrire le signe +
        # bpn est un booleen : s'il est vrai, il faut mettre des parentheses autour de l'ecriture si coef est negatif.
        # bpc est un booleen : s'il est vrai, il faut mettre des parentheses autour de l'ecriture si coef =! 0 ou 1 et var est non vide

        if coef != 0 and abs(coef) != 1:
            if var == "":
                if abs(coef) >= 1000:
                    a = '\\nombre{%s}' % coef
                else:
                    a = "%s" % coef
            else:
                if abs(coef) >= 1000:
                    a = '\\nombre{%s}\\,%s' % (coef, var)
                else:
                    a = '%s\\,%s' % (coef, var)
            if bplus and coef > 0:
                a = '+' + a
        elif coef == 1:
            if var == "":
                a = '1'
            else:
                a = "%s" % var
            if bplus:
                a = '+' + a
        elif coef == 0:
            a = ""
        elif coef == -1:
            if var == "":
                a = '-1'
            else:
                a = '-%s' % var
        if bpn and coef < 0 or bpc and coef != 0 and coef != 1 and var != \
            "":
            a = '\\left( ' + a + '\\right)'
        return a

    def sepmilliers(self, nb, mathenvironment=0):

        # Insère les espaces fines pour séparer les milliers et remplace le point
        # décimal par une virgule

        dec = [str(nb)[i] for i in xrange(len(str(nb)))]
        if dec.count('e'):  #nb ecrit en notation scientifique
            exposant = int(("").join(dec[dec.index('e') + 1:]))
            dec = dec[:dec.index('e')]
            lg = len(dec)
            if dec.count('.'):
                virg = dec.index('.')
                dec.remove('.')
            else:
                virg = len(dec)
            if virg + exposant < 0:  #L'ecriture decimale du nombre commence par 0,...
                dec2 = ["0", '.']
                for i in xrange(-virg - exposant):
                    dec2.append("0")
                dec2.extend(dec)
                dec = dec2
            elif virg + exposant > lg:

                #L'ecriture decimale du nombre finit par des 0

                for i in xrange(-((lg - virg) - 1) + exposant):
                    dec.append("0")
        dec2 = []
        if dec.count('.'):
            lavtvirg = dec.index('.')
            laprvirg = (len(dec) - dec.index('.')) - 1
        else:
            lavtvirg = len(dec)
            laprvirg = 0
        nbsep = lavtvirg // 3 + 1
        if lavtvirg > 3:
            cpt = lavtvirg % 3
            if cpt:
                dec2 = dec[0:cpt]
                dec2.append('\\,')
                nbsep = nbsep - 1
            for i in xrange(nbsep):
                dec2.extend(dec[cpt:cpt + 3])
                if nbsep - i > 1:
                    dec2.append('\\,')
                cpt = cpt + 3
        else:
            if dec.count('.'):
                dec2 = dec[0:dec.index('.')]
            else:
                dec2 = dec
        if dec.count('.'):
            cpt = dec.index('.')
        else:
            cpt = len(dec)
        if laprvirg <= 3:
            dec2.extend(dec[cpt:])
        else:
            nbsep = laprvirg // 3 - 1
            dec2.extend(dec[cpt:cpt + 4])
            dec2.append('\\,')
            cpt = cpt + 4
            for i in xrange(nbsep):
                dec2.extend(dec[cpt:cpt + 3])
                if cpt + 3 < len(dec):
                    dec2.append('\\,')
                cpt = cpt + 3
            dec2.extend(dec[cpt:])
        nb = ("").join(dec2)
        if nb.endswith('.0'):
            nb = string.rsplit(nb, '.0')[0]
        if mathenvironment:
            return string.join(string.rsplit(nb, sep='.'), '{,}')
        else:
            return string.join(string.rsplit(nb, sep='.'), ',')


#a = Fractions(1, 2)
#b = Fractions(1, 4)
#c = Fractions(5, 6)
#d = (a + b) / c

#print a>b
#print (c.n,c.d)
#a=Litteral([(3,'x',0),(2,'x',1)])
#b=Litteral([(3,'x',0),(-2,'x',1)])
#print (a*b).e

fig = Metapost()
fig = Metapost.triangle(
    fig, "A", "B",  "C", a=7, b=5, c=6, rotation=0, angledroit=1)
fig = Metapost.triangle(
    fig, "D", "E",  "F", alpha=55, b=4, c=5, rotation=0, angledroit=1)
fig = Metapost.triangle(
    fig, "G", "H",  "I", beta=55, b=5, c=4, rotation=0, angledroit=1)
fig = Metapost.triangle(
    fig, "J", "K",  "L", alpha=40, beta=75, c=5, rotation=0, angledroit=1)
fig = Metapost.triangle(
    fig, "M", "N",  "O", alpha=35, beta=110, b=5, rotation=0, angledroit=1)

fig = Metapost.fin(fig)
#print string.join(fig.text, "")
