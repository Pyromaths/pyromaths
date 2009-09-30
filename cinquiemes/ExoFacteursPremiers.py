# -*- coding: utf-8 -*-
import math, sys, random

from outils/Arithmetique import premier, pgcd, factorise

def simpl_fractions_decomp():
    """Base pour un exercice de simplifications de fractions et de factorisation d'un nombre en facteurs premiers. PAS FINI."""
    exo = ["\\exercice",
           "Mettre les fractions suivantes sous une forme irr\\'eductible :",
           "\\begin{multicols}{4}", "  \\noindent"]
    cor = ["\\exercice*",
           "Mettre les fractions suivantes sous une forme irr\\'eductible :",
           "\\begin{multicols}{4}", "  \\noindent"]

    for k in range(8):
	a = b = 1

	while pgcd(a, b) == 1 :
	    a=random.randrange(1,150)
	    b=random.randrange(2,150)

	afact = factorise(a)[0]
	bfact = factorise(b)[0]

	c = pgcd(a, b)

	exo.append("  \\[ \\thenocalcul = \\dfrac{%s}{%s} \\]" % (a, b))
	cor.append("  \\[ \\thenocalcul = \\dfrac{%s}{%s} \\]" % (a, b))

	count = 0
	num = ''
	den = ''

	for element in afact:
	    if (count % 2):
		cancel = '\\cancel'
	    else:
		cancel = '\\bcancel'

	    count += 1

	    for item in bfact:
		if element > item:
		    den += '{' + str(item) +'} \\times '
		    bfact.remove(item)

	    if element in bfact:
		num += cancel + '{' + str(element) +'} \\times '
		den += cancel + '{' + str(element) +'} \\times '
		bfact.remove(element)
	    else:
		num += '{' + str(element) +'} \\times '
		den += '{' + str(element) +'} \\times '

	cor.append("  \\[ \\thenocalcul = \\dfrac{%s}{%s} \\]" % (num, den))
	cor.append("  \\[ \\thenocalcul = \\dfrac{%s}{%s} \\]" % (a / c, b / c))
	exo.append("\\stepcounter{nocalcul}%")
	cor.append("\\stepcounter{nocalcul}%")

    exo.append("\\end{multicols}")
    cor.append("\\end{multicols}")

    return (exo, cor, a/c, b/c)
