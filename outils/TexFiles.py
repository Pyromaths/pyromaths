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
import codecs
def mise_en_forme(file):
    """
    \begin => +2 espaces si pas \begin{document}
    \item => +2 espaces après sauf si c'est \item
    \end => -2 espaces avant sauf si \end{document}
    Si longueur de ligne >80, retour ligne au dernier espace précédent et
        indentation de la ligne suivante.
    Couper la ligne après un \\begin{}[]{} ou un \\end{}
    lline : last line
    cline : current line
    """
    f = codecs.open(file, encoding='utf-8', mode='r')
    old_tex = f.readlines()
    new_tex=[]
    indent = 0
    item = False
    for cline in old_tex:
        if new_tex:
            lline = new_tex[-1]
        else:
            lline = ""
        cline = cline.strip()
        indent = trouve_indentation(cline, indent, lline)
        if indent < 0:
            print "problème"
        if cline:
            chaine, indent = traite_chaine(cline, indent)
            new_tex.extend(chaine)
        else:
            new_tex.append("")
    f.close()
    f = codecs.open(file, encoding='utf-8', mode='w')
    f.write("\n".join(new_tex))
    f.close()

def trouve_indentation(cline, indent, lline):
    if lline.find(r"\begin{")>=0:
        "indente tout ce qui suit \begin{...}"
        indent += 2
    if cline.find(r"\end{")==0:
        "desindente tout ce qui suit \end{...}"
        indent -= 2
    if lline.find(r"\begin{enumerate}")>=0 or lline.find(r"\begin{itemize}")>=0:
        "n'indente pas ce qui suit un environnement itemize"
        indent -= 2
    if cline.find(r"\item") == 0 and lline.find(r"\begin{enumerate}") < 0 \
                                  and lline.find(r"\begin{itemize}") < 0:
        indent -= 2
    if lline.find(r"\item") >= 0:
        indent += 2
    indent += compte_paires_ouvertes(lline)
    return indent

def traite_chaine(cline,  indent):
    """indente la chaine txt en fonction du paramètre indent"""
    list = []
    cline = " "*indent + cline
    list.append(cline)
    while len(list[-1]) > 80:
        if list[-1].find(" ", 2*indent + 1, 80) > 0:
            for i in range(79, 2*indent + 1, -1):
                if list[-1][i] == " ":
                    list.append(list[-1][:i])
                    indent = trouve_indentation(list[-2][i+1:], indent, list[-1])
                    list.append(" "*indent + list[-2][i+1:])
                    list.pop(-3)
                    break
        else:
            break
    return list, indent

def trouve_paire(txt):
    """Trouve le caractère fermant pour les symboles {, [, ( qui est le 1er
    caractère de txt"""
    ouvrant = ["{", "[", "("]
    fermant = ["}", "]", ")"]
    index = ouvrant.index(txt[0])
    compte = 0
    for i in range(len(txt)):
        if txt[i] == ouvrant[index]:
            compte += 1
        elif txt[i] == fermant[index]:
            compte -= 1
        if compte == 0:
            return i
    return None

def compte_paires_ouvertes(txt):
    """Compte le nombres de paires {...}, \[...\] qui ne sont pas fermées dans
    la string txt"""
    diff = 0
    for i in ["{", r"\["]:
        diff += txt.count(i)
    for i in ["}", r"\]"]:
        diff -= txt.count(i)
    return 2*diff

#mise_en_forme("/home/jerome/Documents/projets/pyromaths/exemples/3e-corrige.tex")
#mise_en_forme("/tmp/4e.tex")
