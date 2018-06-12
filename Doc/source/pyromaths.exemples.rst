API par l'exemple
=================


Cette section est à lire si vous vous posez la question : *« Quels outils existent pour me faciliter l'écriture de nouveaux exercices ? »*

.. warning::

   L'utilisation des outils présentés ici est à double tranchant.

   - C'est un gain de temps. Ils implémentent des procédures techniques et longues (pas forcément compliquées, mais avec des tas de cas particuliers à prendre en compte) ; ils existent depuis des années, et sont déjà utilisés par d'autres exercices, donc fonctionnent plus ou moins.
   - Ils ont été écrit il y a longtemps, par des personnes qui n'ont pas forcément une solide formation ou une grande expérience en informatique, et ils souffrent d'une dette technologique. Leurs auteurs ne sont plus forcément actifs dans le projet, donc seule la lecture du code et des trop rares commentaires permettent de les comprendre. Ils n'ont pas ou très peu de tests unitaires, donc il est très risqué de les modifier (même pour corriger un bug), car il est difficile de savoir ce qui sera cassé par ce changement.

   À vous de voir ce que vous en faîtes !

.. note::

    Le type de la valeur retournée par plusieurs de ces méthodes est soit une classe (:class:`Fraction`, :class:`Polynome`, etc.), soit une chaîne de caractère, qui peut ensuite être manipulée avec le module :mod:`pyromaths.outils.Priorites3`.

.. contents::
   :local:

Fractions
---------

.. currentmodule:: pyromaths.classes.Fractions

.. testsetup:: fraction

   from pyromaths.classes.Fractions import *
   from pyromaths.outils.Fractions import *


Création
""""""""

* Constructeur (:class:`Fraction`)

  .. doctest:: fraction

    >>> repr(Fraction(5, 6))
    Fraction(5, 6)
    >>> repr(Fraction("x", 8))
    Fraction("x", 8)
    >>> repr(Fraction(3.14))
    Fraction(314, 100)
    >>> repr(Fraction(Fraction(1,3)))
    Fraction(1, 3)

* L'option `code` permet de préciser sur la décomposition a pour objectif une simplification ``"s"`` ou une mise au même dénominateur ``"r"``.

  .. doctest:: fraction

    >>> repr(Fraction("3*4", "3*7", "r").traitement())
    Fraction(12, 21)
    >>> repr(Fraction("3*4", "3*7", "s").traitement())
    Fraction(4, 7)


Opérations mathématiques
""""""""""""""""""""""""

.. note::

    Pour la plupart des opérations, le résultat n'est pas simplifié. Voir la partie :ref:`operations_specifiques_fractions`.

* Somme (:func:`Fraction.__add__` et :func:`Fraction.__radd__`).

  .. doctest:: fraction

    >>> Fraction(2,20) + Fraction(2,10)
    Fraction(2, 20)+Fraction("2*2", "10*2", "r")
    >>> repr(Fraction(5,10) + Fraction(2,10))
    Fraction(7, 10)
    >>> Fraction(5,7) + Fraction(2,10)
    Fraction("5*10", "7*10", "r")+Fraction("2*7", "10*7", "r")

* Différence (:func:`Fraction.__sub__` et :func:`Fraction.__rsub__`)

  .. doctest:: fraction

    >>> Fraction(2,20) - Fraction(2,10)
    Fraction(2, 20)-Fraction("2*2", "10*2", "r")
    >>> repr(Fraction(5,10) - Fraction(2,10))
    Fraction(3, 10)
    >>> Fraction(5,7) - Fraction(2,10)
    Fraction("5*10", "7*10", "r")-Fraction("2*7", "10*7", "r")

* Produit (:func:`Fraction.__mul__`)

  .. doctest:: fraction

    >>> repr(Fraction(2,5) * Fraction(2,10))
    Fraction("2*2", "5*2*5", "s")
    >>> repr(Fraction(2,5) * 4)
    Fraction(8, 5)

* Quotient (:func:`Fraction.__div__` et :func:`Fraction.__rdiv__`)

  .. doctest:: fraction

    >>> Fraction(2,5) / Fraction(10,2)
    Fraction(2, 5)*Fraction(2, 10)
    >>> Fraction(2,5) / 4
    Fraction(2, 5)*Fraction(1, 4)

* Puissance (:func:`Fraction.__pow__`)

  .. doctest:: fraction

    >>> repr(Fraction(2,3)**4)
    Fraction(16, 81)

* Opposé (:func:`Fraction.__neg__`)

  .. doctest:: fraction

    >>> repr(-Fraction(8,27))
    Fraction(-8, 27)

* Opérateur unaire *+* (:func:`Fraction.__pos__`)

  .. doctest:: fraction

    >>> repr(+Fraction(8,27))
    Fraction(8, 27)

* Inverse (:func:`Fraction.__invert__`)

  .. doctest:: fraction

    >>> repr(~Fraction(8,27))
    Fraction(27, 8)

* Valeur absolue (:func:`Fraction.__abs__`)

  .. doctest:: fraction

      >>> repr(abs(Fraction(-5, 6)))
      Fraction(5, 6)
      >>> repr(abs(-Fraction(5, 6)))
      Fraction(5, 6)

* Troncature (:func:`Fraction.__trunc__`)

  .. doctest:: fraction

      >>> import math
      >>> math.trunc(Fraction(7, 6))
      1

* Comparaison (:func:`Fraction.__eq__`, :func:`Fraction.__ge__`, :func:`Fraction.__gt__`, :func:`Fraction.__le__`, :func:`Fraction.__lt__`, :func:`Fraction.__ne__`)

  .. doctest:: fraction

      >>> Fraction(5, 6) < 1
      True
      >>> Fraction(6, 6) == 1
      True
      >>> Fraction(3, 4) >= Fraction(6, 7)
      False

.. _operations_specifiques_fractions:

Opérations spécifiques aux fractions
""""""""""""""""""""""""""""""""""""

* Changer le dénominateur (:func:`Fraction.choix_denominateur`). L'argument ``denominateur`` doit être un diviseur du dénominateur de la fraction, sans quoi le résultat sera aberrant.

  .. doctest:: fraction

      >>> repr(Fraction(5, 6).choix_denominateur(12))
      Fraction("5*2", "6*2", "r")
      >>> repr(Fraction(5, 6).choix_denominateur(4)) # Résultat aberrant.
      Fraction("5*0", "6*0", "r")

* Réduction du numérateur et du dénominateur (:func:`Fraction.reduit`)

  .. doctest:: fraction

    >>> repr(Fraction(2*4,5*4).reduit())
    Fraction(8, 20)
    >>> repr(Fraction('2*4', '5*4').reduit())
    Fraction(8, 20)

* Simplification (:func:`Fraction.simplifie`)

  .. doctest:: fraction

    >>> repr(Fraction(8, 20).simplifie())
    Fraction(2, 5)
    >>> repr(Fraction('2*4','5*4').simplifie())
    Fraction(2, 5)

* Décomposition (:func:`Fraction.decompose`)

  .. doctest:: fraction

    >>> repr(Fraction(8,20).decompose())
    Fraction("2*4", "5*4", "s")

* Mise au même dénominateur, ou simplification (:func:`Fraction.traitement`)

  .. doctest:: fraction

        >>> repr(Fraction("3*4", "3*7", "r").traitement())
        Fraction(12, 21)
        >>> repr(Fraction("3*4", "3*7", "s").traitement())
        Fraction(4, 7)
        >>> repr(Fraction(12, 21).traitement())
        Fraction(12, 21)
        >>> repr(Fraction(12, 21).traitement(True))
        Fraction("4*3", "7*3", "s")

Conversions
"""""""""""

* Conversion en flottant (:func:`Fraction.__float__`)

  .. doctest:: fraction

      >>> float(Fraction(5, 6))
      0.833333333333

* Conversion en entier (:func:`Fraction.__int__`). Cette méthode ne fonctionne que si la fraction est égale à un nombre entier. Sinon, elle lève une exception.

  .. doctest:: fraction

      >>> int(Fraction(15, 5))
      3
      >>> int(Fraction(15, 6))
      Traceback (most recent call last):
        ...
      AssertionError: La fraction n'est pas un nombre entier !



LaTeX
"""""

* Conversion d'une fraction en LaTeX (:func:`Fraction.__str__`).

  .. doctest:: fraction

     >>> str(Fraction(8, 3))
     \dfrac{8}{3}
     >>> str(Fraction(8, 1))
     8
     >>> str(Fraction('-5*2', '3*2', 'r'))
     \dfrac{-5_{\times 2}}{3_{\times 2}}

.. _polynomes:

Polynômes
---------

.. currentmodule:: pyromaths.classes.Polynome

.. testsetup:: polynome

   from pyromaths.classes.Polynome import *

.. note::

    Deux autres classes permettent de manipuler des polynômes :

    - :ref:`polynomes_college` : orienté vers la résolution de problèmes de collège (avec davantage de détails lors des calculs, par exemple) ;
    - :ref:`polynomes_degre2` : pour la manipulation exclusive des polynômes du second degré.

Création
""""""""

* Constructeur (:class:`Polynome`)

  .. doctest:: polynome

      >>> repr(Polynome("x^2-3x+1"))
      Polynome({0: 1, 1: -3, 2: Fraction(1, 1)}, var="x")
      >>> repr(Polynome({2: 4, 1:8, 0:1, 3:0}))
      Polynome({0: Fraction(1, 1), 1: Fraction(8, 1), 2: Fraction(4, 1)}, var="x")

* Si l'argument est une liste, les coefficients sont donnés dans l'ordre des degrés des monômes (plus bas degré en premier), ce qui est l'inverse du sens de lecture habituel (plus haut degré en premier).

  .. doctest:: polynome

      >>> str(Polynome([1, 2, 3, 4]))
      4x^3+3x^2+2x+1

* L'argument ``var`` permet de changer le nom de la variable

  .. doctest:: polynome

      >>> str(Polynome([2, 3], var="z"))
      3z+2
      >>> str(Polynome([2, 3]))
      3x+2

Paramètres
""""""""""

* Taille (nombre de monômes, éventuellement nuls) (:func:`Polynome.__len__`).

  .. doctest:: polynome

     >>> len(Polynome([2, -3]))
     2
     >>> len(Polynome([2, 0, -3]))
     3

* Degré (:func:`Polynome.degre`).

  .. doctest:: polynome

     >>> Polynome([2, -3]).degre()
     1

* Accès à chacun des coefficients, en fonction du degré (:func:`Polynome.__getitem__`).

  .. doctest:: polynome

     >>> str(Polynome([2, -3]))
     -3x+2
     >>> Polynome([2, -3])[0]
     2
     >>> Polynome([2, -3])[1]
     -3


Opérations
""""""""""

* Somme (:func:`Polynome.__add__` et :func:`Polynome.__radd__`).

  .. doctest:: polynome

     >>> repr(Polynome([2, -3]) + Polynome([1, 2, 3]))
     Polynome({0: 3, 1: -1, 2: 3}, var="x")
     >>> repr(Polynome([2, -3]) + 1)
     Polynome({0: 3, 1: -3}, var="x")


* Produit (:func:`Polynome.__mul__`).

  .. doctest:: polynome

     >>> repr(Polynome([2, -3]) * Polynome([1, 2, 3]))
     Polynome({0: 2, 1: Fraction(1, 1), 3: Fraction(-9, 1)}, var="x")

* Puissance (:func:`Polynome.__pow__`).

  .. doctest:: polynome

     >>> repr(Polynome([2, -3])**2)
     Polynome({0: 4, 1: Fraction(-12, 1), 2: Fraction(9, 1)}, var="x")

* Différence (:func:`Polynome.__sub__` et :func:`Polynome.__rsub__`).

  .. doctest:: polynome

    >>> repr(Polynome([2, -3]) - Polynome([7, 3]))
    Polynome({0: -5, 1: -6}, var="x")

* Opposé (:func:`Polynome.__neg__`).

  .. doctest:: polynome

     >>> repr(-Polynome([2, -3]))
     Polynome({0: -2, 1: Fraction(3, 1)}, var="x")

* Division euclidienne (renvoit un tuple `(dividende, reste)`) (:func:`Polynome.__div__`).

  .. doctest:: polynome

     >>> repr(Polynome([2, -3]) / 2)
     Polynome({0: 1, 1: Fraction(-3, 2)}, var="x")
     >>> Polynome([1, 2, 3]) / Polynome([-2, 1])
     (Polynome({0: 8, 1: Fraction(3, 1)}, var="x"), Polynome({0: Fraction(17, 1)}, var="x"))
     >>> (Polynome([1, 2, 3]) * Polynome([3, -1])) / Polynome([3, -1])
     (Polynome({0: 1, 1: Fraction(2, 1), 2: 3}, var="x"), Polynome({0: 0}, var="x"))

* Comparaison (:func:`Polynome.__eq__` et :func:`Polynome.__ne__`).

  .. doctest:: polynome

     >>> Polynome([2, -3]) == Polynome("-3x+2")
     True
     >>> Polynome([2, -3]) != Polynome("-3x+2")
     False

Opérations spécifiques
""""""""""""""""""""""

* Simplification (:func:`Polynome.simplifie`).

  .. doctest:: polynome

     >>> repr(Polynome([2, Fraction(12, 4)]).simplifie())
     Polynome({0: Fraction(2, 1), 1: Fraction(3, 1)}, var="x")

* Calcul d'image (:func:`Polynome.__call__`).

  .. doctest:: polynome

     >>> Polynome([2, -3])(1)
     -1
     >>> Polynome([2, -3])(float("inf"))
     -inf
     >>> Polynome([2, -3])("z")
     -3z+2
     >>> # Attention : Cette fonction n'ajoute pas les parenthèses nécessaires.
     >>> Polynome([2, -3])("z+1")
     -3z+1+2

* Recherche de racines évidentes (:func:`Polynome.racine_evidente`).

  .. doctest:: polynome

     >>> # Remarquons que la racine `-6/5` n'a pas été trouvée.
     >>> (Polynome([1, 1]) * Polynome([6, 5]) * Polynome([0, -2])).racine_evidente()
     [-1, 0]

* Factorise (:func:`Polynome.factorise`).

  .. note::

     Je ne suis pas l'auteur de cette fonction ; je ne sais pas comment elle est utilisée. Vu les exemples ci-dessous, son utilité doit être assez restreinte :

     - Apparemment, si un polynôme de degré `n` a moins de `n` racines (ou qu'une des racines n'est pas évidente, c'est à dire n'est pas un entier plus petit que 2 en valeur absolue), alors elle lève une exception.
     - Quand elle fonctionne, elle renvoit la liste des facteurs, mais elle renvoit plusieurs facteurs `Polynome({0: 1})`, c'est-à-dire égaux à la constante 1, ce qui est inutile.

  .. doctest:: polynome

     >>> Polynome([-2, -1, 1]).factorise()
     [Polynome({0: 1}, var="x"), Polynome({0: Fraction(1, 1), 1: Fraction(1, 1)}, var="x"), Polynome({0: Fraction(-2, 1), 1: Fraction(1, 1)}, var="x"), Polynome({0: 1}, var="x")]
     >>> # Polynôme de degré 3 avec une seule racine (pas évidente)
     >>> Polynome([-6, -7, -8, 15]).factorise()
     Traceback (most recent call last):
         ...
     TypeError: ...


* Dérivation (:func:`Polynome.derive`).

  .. doctest:: polynome

     >>> repr(Polynome([1, 2, 3, 4]).derive())
     Polynome({0: 2, 1: 6, 2: 12}, var="x")

* Calcul de primitive (:func:`Polynome.primitive`).

  .. doctest:: polynome

     >>> repr(Polynome([2, -3]).primitive())
     Polynome({1: 2, 2: Fraction(-3, 2)}, var="x")

.. _polynomes_college:

Conversion en LaTeX
"""""""""""""""""""

* Conversion en LaTeX, avec les options par défaut (:func:`Polynome.__str__`).

  .. doctest:: polynome

     >>> str(Polynome([2, -3]))
     -3x+2
     >>> str(Polynome([2, 0, 0, -3]))
     -3x^3+2

* Conversion en LaTeX, avec plus d'options (:func:`Polynome.TeX`).

  .. doctest:: polynome

     >>> Polynome([2, -3]).TeX()
     -3x+2
     >>> Polynome([2, -3]).TeX(var="z")
     -3z+2
     >>> Polynome([2, -3]).TeX(parenthese=True)
     \left(-3x+2\right)


Polynômes (collège)
-------------------

Cette classe vise à manipuler les polynômes avec un niveau collège. Elle inclut par exemple des outils pour détailler des calculs.

.. testsetup:: polynomescollege

   from pyromaths.classes.PolynomesCollege import *

Constructeur
""""""""""""

* Constructeur (:func:`Polynome.__init__`).

  .. doctest:: polynomescollege

     >>> repr(Polynome([[-3, 2], [2, 1], [1, 0]]))
     Polynome([[-3, 2], [2, 1], [1, 0]], "x", 0)
     >>> repr(Polynome("2x^4-3+x^3"))
     Polynome([[2, 4], [-3, 0], [1, 3]], "x", 0)

* Les monômes peuvent se repéter.

  .. doctest:: polynomescollege

     >>> repr(Polynome([[-3, 2], [2, 2], [1, 2]]))
     Polynome([[-3, 2], [2, 2], [1, 2]], "x", 0)

* La variable du polynôme peut être changée avec l'argument ``var``.

  .. doctest:: polynomescollege

     >>> str(Polynome([[-3, 2], [2, 1], [1, 0]]))
     -3\,x^{2}+2\,x+1
     >>> str(Polynome([[-3, 2], [2, 1], [1, 0]], var="z"))
     -3\,z^{2}+2\,z+1

* L'argument ``details`` décrit le niveau de détails voulus dans les développements et réductions.

  .. doctest:: polynomescollege

     >>> repr(Polynome([[-3, 2], [2, 2], [1, 0]], details=0).nreduction())
     Polynome([[-1, 2], [1, 0]], "x", 0)
     >>> repr(Polynome([[-3, 2], [2, 2], [1, 0]], details=3).nreduction())
     Polynome([['-3+2', 2], [1, 0]], "x", 3)
     >>> repr(Polynome([[2, 1], [1, 0]], details=0) + Polynome([[2, 1], [1, 0]], details=0))
     Polynome([[4, 1], [2, 0]], "x", 0)
     >>> repr(Polynome([[2, 1], [1, 0]], details=3) + Polynome([[2, 1], [1, 0]], details=3))
     Polynome([[2, 1], [2, 1], [1, 0], [1, 0]], "x", 3)

* Constructeur à partir d'une liste de points, en utilisant l'interpolation de Lagrange (:func:`Lagrange`). Ce polynôme est davantage destiné à être tracé qu'à être utilisé pour des calculs.

  .. doctest:: polynomescollege

    >>> Lagrange(((2,0), (4,2)))
    0+Fraction(2, 2)*Polynome("x-2", details = 0)
    >>> # Tracé d'un polynôme avec psplot
    >>> from pyromaths.outils.Priorites3 import plotify, priorites
    >>> plotify(priorites(Lagrange(((2,0), (4,2))))[-1])
    1*x^1-2

* Choix de points pour un polynôme de Lagrange (:func:`choix_points`).
  Renvoie un tuple contenant `nb` coordonnées sous forme de tuple telles que les abscisses et ordonnées sont distinctes, comprises entre `min` et `max`, une abscisse n'est jamais égale à une ordonnée et la coordonnée (b, a) n'est pas listée si la coordonnée (a, b) existe.

  .. doctest:: polynomescollege

    >>> import random
    >>> random.seed(0)
    None
    >>> choix_points(-4, 4, nb=5)
    ((-4, 1), (-3, -1), (-1, -4), (0, -3), (1, 0))


Caractéristiques
""""""""""""""""

* Accès aux coefficients (:func:`Polynome.__getitem__`, :func:`Polynome.__delitem__`).

  .. doctest:: polynomescollege

     >>> Polynome([[-3, 2], [2, 1], [1, 0]])[0]
     [-3, 2]
     >>> Polynome([[-3, 2], [2, 1], [1, 0]])[1]
     [2, 1]

* Nombre de monômes (:func:`Polynome.__len__`).

  .. doctest:: polynomescollege

     >>> len(Polynome([[-3, 1], [2, 1], [1, 0]]))
     3

* Degré (:func:`Polynome.degre`).

  .. doctest:: polynomescollege

     >>> Polynome([[-3, 2], [2, 1], [1, 0]]).degre()
     2

Opérations
""""""""""

* Somme (:func:`Polynome.__add__`, :func:`Polynome.__radd__`, :func:`Polynome.__iadd__`).

  .. doctest:: polynomescollege

     >>> repr(Polynome([[-3, 2], [2, 1], [1, 0]]) + Polynome([[2, 2], [-1, 0]]))
     Polynome([[-1, 2], [2, 1]], "x", 0)

* Comparaison (:func:`Polynome.__eq__`, :func:`Polynome.__ne__`). Les polynômes sont ordonnés avant comparaison, mais pas réduits.

  .. doctest:: polynomescollege

     >>> Polynome([[-3, 2], [2, 1], [1, 0]]) == Polynome([[-3, 2], [1, 0], [2, 1]])
     True
     >>> Polynome([[1, 1], [1, 1]]) == Polynome([[2, 1]])
     False

* Différence (:func:`Polynome.__sub__`, :func:`Polynome.__rsub__`).

  .. doctest:: polynomescollege

     >>> repr(Polynome([[-3, 2], [2, 1], [1, 0]]) - Polynome([[2, 1]]))
     Polynome([[-3, 2], [1, 0]], "x", 0)

* Opposé (:func:`Polynome.__neg__`).

  .. doctest:: polynomescollege

     >>> repr(-Polynome([[-3, 2], [2, 1], [1, 0]]))
     Polynome([[3, 2], [-2, 1], [-1, 0]], "x", 0)

* Positif (:func:`Polynome.__pos__`).

  .. doctest:: polynomescollege

     >>> repr(+Polynome([[-3, 2], [2, 1], [1, 0]]))
     Polynome([[-3, 2], [2, 1], [1, 0]], "x", 0)

* Produit (:func:`Polynome.__mul__`, :func:`Polynome.__rmul__`). Le résultat dépend de la valeur de l'attribut ``details`` (définit dans le constructeur). Le résultat n'est pas réduit.

  .. doctest:: polynomescollege

     >>> Polynome([[2, 1], [1, 0]]) * Polynome([[1, 1], [1, 0]])
     Polynome([[2, 2]], "x", 0)+Polynome([[2, 1]], "x", 0)+Polynome([[1, 1]], "x", 0)+Polynome([[1, 0]], "x", 0)
     >>> Polynome([[2, 1], [1, 0]], details=0) * Polynome([[1, 1], [1, 0]])
     Polynome([[2, 2]], "x", 0)+Polynome([[2, 1]], "x", 0)+Polynome([[1, 1]], "x", 0)+Polynome([[1, 0]], "x", 0)
     >>> Polynome([[2, 1], [1, 0]], details=1) * Polynome([[1, 1], [1, 0]])
     Polynome([[2, 1]], "x", 1)*Polynome([[1, 1]], "x", 1)+Polynome([[2, 1]], "x", 1)*Polynome([[1, 0]], "x", 1)+Polynome([[1, 0]], "x", 1)*Polynome([[1, 1]], "x", 1)+Polynome([[1, 0]], "x", 1)*Polynome([[1, 0]], "x", 1)

* Modulo (:func:`Polynome.__mod__`).

  .. doctest:: polynomescollege

     >>> Polynome([[-3, 2], [2, 1], [1, 0]]) % Polynome([[1, 1]])
     1

* Dividende (:func:`Polynome.__floordiv__`).

  .. doctest:: polynomescollege

     >>> repr(Polynome([[-3, 2], [2, 1], [1, 0]]) // Polynome([[1, 1]]))
     Polynome([[-3, 1], [2, 0]], "x", 0)

* Puissance (:func:`Polynome.__pow__`).

  .. doctest:: polynomescollege

     >>> Polynome([[2, 1], [1, 0]])**2
     Polynome([[2, 1]], "x", 0)**2+2*Polynome([[2, 1]], "x", 0)*Polynome([[1, 0]], "x", 0)+Polynome([[1, 0]], "x", 0)**2



Opérations spécifiques
""""""""""""""""""""""

* Calcul d'images (:func:`Polynome.__call__`). Cette méthode ne calcule rien, mais renvoie le calcul à effectuer.

  .. doctest:: polynomescollege

     >>> Polynome([[-3, 2], [2, 1], [1, 0]])(2)
     -3*2**2+2*2+1
     >>> Polynome([[-3, 2], [2, 1], [1, 0]])("z")
     -3*'z'**2+2*'z'+1
     >>> # Les parenthèses ne sont pas ajoutées pour les arguments « composés »
     >>> Polynome([[-3, 2], [2, 1], [1, 0]])("z+1")
     -3*'z+1'**2+2*'z+1'+1


* Dérivée (:func:`Polynome.derive`).

  .. doctest:: polynomescollege

     >>> repr(Polynome([[-3, 2], [2, 1], [1, 0]]).derive())
     Polynome([[-6, 1], [2, 0]], "x", 0)



* Caractère réductible ou ordonnable (:func:`Polynome.reductible`).

  .. doctest:: polynomescollege

     >>> Polynome([[-3, 2], [2, 1], [1, 1]]).reductible()
     True
     >>> Polynome([[-3, 2], [2, 1], [1, 0]]).reductible()
     False

* Caractère ordonnable (:func:`Polynome.ordonnable`).

  .. doctest:: polynomescollege

     >>> Polynome([[-3, 2], [2, 1], [1, 0]]).ordonnable()
     False
     >>> Polynome([[-3, 1], [2, 2], [1, 0]]).ordonnable()
     True

* Ordonne (:func:`Polynome.ordonne`).

  .. doctest:: polynomescollege

     >>> repr(Polynome([[-3, 2], [2, 3], [1, 0]]))
     Polynome([[-3, 2], [2, 3], [1, 0]], "x", 0)


* Réduction (partielle) (:func:`Polynome.nreduction`). Le résultat dépend de la valeur de l'attribut ``details`` du constructeur.

  .. doctest:: polynomescollege

     >>> repr(Polynome([[-3, 2], [2, 2], [1, 0]], details=0).nreduction())
     Polynome([[-1, 2], [1, 0]], "x", 0)
     >>> repr(Polynome([[-3, 2], [2, 2], [1, 0]], details=1).nreduction())
     Polynome([[-1, 2], [1, 0]], "x", 1)
     >>> repr(Polynome([[-3, 2], [2, 2], [1, 0]], details=2).nreduction())
     Polynome([['-3+2', 2], [1, 0]], "x", 2)
     >>> repr(Polynome([[-3, 2], [2, 2], [1, 0]], details=3).nreduction())
     Polynome([['-3+2', 2], [1, 0]], "x", 3)

* Factorisation (:func:`factoriser`).

  .. doctest:: polynomescollege

     >>> factoriser("Polynome('4x^2+12x+9')")
     Polynome([[2.0, 1]], "x", 0)**2+2*Polynome([[2.0, 1]], "x", 0)*Polynome([[3.0, 0]], "x", 0)+Polynome([[3.0, 0]], "x", 0)**2
     >>> factoriser("Polynome('-4x^2+12x-9')")
     -(Polynome([[2.0, 1]], "x", 0)**2-2*Polynome([[2.0, 1]], "x", 0)*Polynome([[3.0, 0]], "x", 0)+Polynome([[3.0, 0]], "x", 0)**2)
     >>> factoriser("Polynome('4x^2-9')")
     Polynome([[SquareRoot([[1, 4]]), 1]], "x", 0)**2-Polynome([[SquareRoot([[1, 9]]), 0]], "x", 0)**2
     >>> factoriser("Polynome('3x^2-5')")
     Polynome([[SquareRoot([[1, 3]]), 1]], "x", 0)**2-Polynome([[SquareRoot([[1, 5]]), 0]], "x", 0)**2
     >>> factoriser("Polynome('4x^2')")
     Polynome([[2.0, 1]], "x", 0)**2
     >>> factoriser("Polynome('4x')")
     None
     >>> factoriser("Polynome('x+1')*Polynome('x+2')+Polynome('x+1')*Polynome('x+3')")
     Polynome([[1, 1], [1, 0]], "x", 0)*(Polynome([[1, 1], [2, 0]], "x", 0)+Polynome([[1, 1], [3, 0]], "x", 0))
     >>> factoriser("Polynome('x+1')*Polynome('x+2')+Polynome('x+1')")
     Polynome([[1, 1], [1, 0]], "x", 0)*Polynome([[1, 1], [2, 0]], "x", 0)+Polynome([[1, 1], [1, 0]], "x", 0)*1
     >>> factoriser("Polynome('x+1')*Polynome('x+2')+Polynome('x+1')**2")
     Polynome([[1, 1], [1, 0]], "x", 0)*Polynome([[1, 1], [2, 0]], "x", 0)+Polynome([[1, 1], [1, 0]], "x", 0)*Polynome([[1, 1], [1, 0]], "x", 0)
     >>> factoriser("Polynome('x+1')**2-Polynome([[81, 0]], 'x', 3)")
     Polynome([[1, 1], [1, 0]], "x", 0)**2-Polynome([[9.0, 0]], "x", 3)**2

LaTeX
"""""

* Conversion en LaTeX (:func:`Polynome.__str__`).

  .. doctest:: polynomescollege

     >>> str(Polynome([[-3, 2], [2, 1], [1, 0]]))
     -3\,x^{2}+2\,x+1
     >>> str(Polynome([[-3, 2], [2, 1], [1, 0]], var="z"))
     -3\,z^{2}+2\,z+1


.. _polynomes_degre2:

Polynômes du second degré
-------------------------

Cette classe est moins générique que la classe :ref:`polynomes` décrite plus haut, mais elle permet de faire des opérations spécifiques aux polynômes de degré 2.

.. testsetup:: polynomedegre2

   from pyromaths.classes.SecondDegre import *

Constructeur
""""""""""""

* Constructeur (:func:`Poly2.__init__`). Les arguments sont les valeurs des coefficients `a`, `b`, `c` du polynôme noté `ax²+bx+c`.

  .. doctest:: polynomedegre2

     >>> repr(Poly2(2, 3, 4))
     Poly2(2, 3, 4)

* L'argument `a` doit être non nul.

  .. doctest:: polynomedegre2

     >>> Poly2(0, 3, 4)
     Traceback (most recent call last):
         ...
     AssertionError: "Erreur de définition ! a doit être différent de 0."

Opérations
""""""""""

* Somme (:func:`Poly2.__add__`, :func:`Poly2.__radd__`).

  .. doctest:: polynomedegre2

     >>> repr(Poly2(2, 3, 4) + Poly2(1, 1, 0))
     Poly2(3, 4, 4)

* Différence (:func:`Poly2.__sub__`, :func:`Poly2.__rsub__`).

  .. doctest:: polynomedegre2

     >>> repr(Poly2(2, 3, 4) - Poly2(1, 0, 1))
     Poly2(1, 3, 3)

LaTeX
"""""

* Conversion en LaTeX (:func:`Poly2.__str__`).

  .. doctest:: polynomedegre2

     >>> str(Poly2(2, 3, 4))
     2x^2+3x+4

* Comparaison (:func:`Poly2.print_signe`).

  .. doctest:: polynomedegre2

     >>> Poly2(2, 3, 4).print_signe("\leq")
     2x^2+3x+4 \leq 0

Conversion en LaTeX
-------------------

Nombres
"""""""

.. currentmodule:: pyromaths.outils.decimaux

* Nombres entiers (:func:`suppr0`) : Convertit en entier un flottant égal à un entier.

  .. doctest::

     >>> from pyromaths.outils.decimaux import suppr0
     >>> suppr0(2.2)
     2.2
     >>> suppr0(2.0)
     2
     >>> suppr0(2)
     2

* Conversion de décimaux en chaîne de caractères (:func:`decimaux`). Avec l'option `mathenv`, le décimal est destiné à être affiché dans un environnement mathématique. L'argument peut être une chaîne de caractères ou un :class:`Float`.

  .. doctest::

     >>> from pyromaths.outils.decimaux import decimaux
     >>> decimaux(-2.8)
     -2,8
     >>> decimaux("2")
     2
     >>> decimaux("-2.67")
     -2,67
     >>> decimaux("2e1")
     20
     >>> decimaux("34e-1")
     3,4
     >>> decimaux("34e-1", mathenv=True)
     3{,}4
     >>> decimaux("1234567890")
     1\,234\,567\,890
     >>> # Le "e" est optionnel, mais considérez cela comme un bug.
     >>> decimaux("34-1")
     3,4

.. currentmodule:: pyromaths.outils.Affichage

.. testsetup:: affichage

   from pyromaths.outils.Affichage import *

* Affichage d'un monôme de degré 1 (:func:`tex_coef`). Les options (avec les valeurs par défaut) sont :

  - ``var=""`` : Variable. Par défaut, aucune variable n'est utilisée ;
  - ``bplus=False``: Ajouter un "+" devant, si nécessaire ;
  - ``bpn=False``: Ajouter des parenthèses, si nécessaire pour un produit (n'ajoute pas de parenthèses autour de `5x`, mais le fait pour `-5x`) ;
  - ``bpc=False``: Ajouter des parenthèses, si nécessaire pour une puissance (n'ajoute pas de parenthèses autour de `x`, mais le fait pour `5x`).

  .. doctest:: affichage

     >>> # Variable
     >>> tex_coef(5)
     5
     >>> tex_coef(5, var='x')
     5\,x
     >>> tex_coef(5, var='y')
     5\,y
     >>> # Signe +
     >>> tex_coef(5, var='x', bplus=True)
     +5\,x
     >>> tex_coef(-5, var='x', bplus=True)
     -5\,x
     >>> # Parenthèses, si nécessaire pour un produit
     >>> tex_coef(5, var='x', bpn=True)
     5\,x
     >>> tex_coef(-5, var='x', bpn=True)
     \left( -5\,x\right)
     >>> # Parenthèses, si nécessaire pour une puissance
     >>> tex_coef(1, var='x', bpn=True, bpc=True)
     x
     >>> tex_coef(5, var='x', bpn=True, bpc=True)
     \left( 5\,x\right)

* Affichage de nombres décimaux, radicaux, fractionnaires, infini (:func:`TeX`). Des raccourcis sont disponibles avec les commandes suivantes. Les arguments (avec les valeurs par défaut) sont :

  - ``parenthese=False`` : Affiche des parenthèses si nécessaire (autour d'un nombre négatif, par exemple).
  - ``terme=False`` : Affiche le signe ``+`` pour un nombre positif.
  - ``fractex='\dfrac'`` : Définit la commande à utiliser pour afficher les fractions.

  .. doctest:: affichage

     >>> TeX(Fraction(7,3)).strip()
     \dfrac{7}{3}
     >>> TeX(Fraction(7,3), fractex='\\frac').strip()
     \frac{7}{3}
     >>> TeX(3).strip()
     3
     >>> TeX(3, terme=True)
     +3
     >>> TeX(-1).strip()
     -1
     >>> TeX(-1, parenthese=True)
     \left(-1\right)

* Formate le nombre avec :func:`TeX`, sauf s'il est égal à 0 (:func:`TeXz`).

  .. doctest:: affichage

     >>> TeXz(0) == ""
     True
     >>> TeXz(2.4)
     2,4

* Raccourci pour `TeX(nombre, terme=True)` (:func:`tTeX`)

  .. doctest:: affichage

     >>> TeX(3)
     3
     >>> tTeX(3)
     +3

* Raccourci pour `TeX(nombre, parenthese=True) (:func:`pTeX`)

  .. doctest:: affichage

     >>> TeX(-2)
     -2
     >>> pTeX(-2)
     \left(-2\right)
     >>> pTeX(2)
     2

* Raccourci pour `TeX(nombre, fractex="\\frac")` (:func:`fTeX`)

  .. doctest:: affichage

     >>> TeX(Fraction(6, 7)).strip()
     \dfrac{6}{7}
     >>> fTeX(Fraction(6, 7)).strip()
     \frac{6}{7}

* Racine carrée (:func:`radicalTeX`)

  .. doctest:: affichage

     >>> radicalTeX("4.12")
     \sqrt{4,12}
     >>> radicalTeX(4.12)
     \sqrt{4,12}
     >>> radicalTeX(4000000000000)
     \sqrt{4\,000\,000\,000\,000}

Calculs avec étapes
-------------------

.. currentmodule:: pyromaths.outils.Priorites3

.. testsetup:: priorites3

   from pyromaths.outils.Priorites3 import *

* Teste si l'argument est une valeur, c'est à dire un entier, un réel, un polynôme, une fraction, une racine carrée.  (:func:`EstNombre`) Attention : (-11) est considéré comme un nombre.

  .. doctest:: priorites3

    >>> EstNombre('-15')
    True
    >>> EstNombre('Polynome([[-4, 2]], "x")')
    True

* Partitionne la chaîne de caractères pour obtenir une liste d'opérateurs, de parenthèses, de polynômes et de nombres puis arrange la liste des opérandes et opérateurs (:func:`splitting`)

  .. doctest:: priorites3

    >>> splitting('-Polynome([[-4, 2]], "x")*6**2+3')
    ['-', 'Polynome([[-4, 2]], "x")', '*', '6', '**', '2', '+', '3']
    >>> splitting('-6*(-11)*(-5)')
    ['-6', '*', '(-11)', '*', '(-5)']
    >>> splitting("Fraction(1,7)x^2-Fraction(3,8)x-1")
    ['Fraction(1,7)', 'x', '^', '2', '-', 'Fraction(3,8)', 'x', '-', '1']
    >>> splitting('-7**2')
    ['-', '7', '**', '2']

* Recherche les premières parenthèses (éventuellement intérieures) dans une expression (:func:`recherche_parentheses`)

  .. doctest:: priorites3

    >>> recherche_parentheses(['-6', '*', '(-11)', '*', '(-5)'])
    None
    >>> recherche_parentheses(['-9', '-', '6', '*', '(', '(-2)', '-', '4', ')'])
    (4, 9)

* Effectue une étape du calcul en respectant les priorités (:func:`effectue_calcul`).

  .. warning::

    Je (auteur de cette documentation) ne sais pas comment s'utilise la valeur de retour de cette fonction. Dans les cas très simple, elle peut être convertie en LaTeX en concaténant les chaînes de caractères ; les cas compliqués ne semblent pas être utilisés dans les exercices déjà écrits.

  .. doctest:: priorites3

    >>> effectue_calcul(['-5', '-', '(', '(-6)', '-', '1', '+', '(-3)', ')', '*', '(-1)'])
    ['-5', '-', '(', '-7', '-', '3', ')', '*', '(-1)']
    >>> effectue_calcul(['-5', '-', '(', '-7', '-', '3', ')', '*', '(-1)'])
    ['-5', '-', '-10', '*', '(-1)']
    >>> effectue_calcul(['-5', '-', '-10', '*', '(-1)'])
    ['-5', '-', '10']
    >>> effectue_calcul(['-5', '-', '10'])
    ['-15']
    >>> effectue_calcul(['-', 'Polynome("x-1")', '*', '2'])
    ['-', '(', 'Polynome([[2, 1]], "x", 0)', '+', 'Polynome([[-2, 0]], "x", 0)', ')']
    >>> effectue_calcul(['4', '*', 'Polynome("x+1")', '**', '2'])
    ['4', '*', '(', 'Polynome([[1, 1]], "x", 0)', '**', '2', '+', '2', '*', 'Polynome([[1, 1]], "x", 0)', '*', 'Polynome([[1, 0]], "x", 0)', '+', 'Polynome([[1, 0]], "x", 0)', '**', '2', ')']

* Effectue un enchaînement d'opérations contenues dans calcul en respectant les priorités et en détaillant les étapes (:func:`priorites`). La valeur de retour peut ensuite être convertie en LaTeX en utilisant la fonction :ref:`texify() <texify>`, décrite ci-après.

  .. doctest:: priorites3

    >>> priorites('-1+5-(-5)+(-6)*1')
    [['4', '+', '5', '-', '6'], ['9', '-', '6'], ['3']]
    >>> priorites('-5**2+6')
    [['-', '25', '+', '6'], ['-25', '+', '6'], ['-19']]
    >>> priorites('Polynome([[Fraction(6, 7), 0]], "x")*Polynome([[Fraction(1,3), 1], [1,0]], "x")')
    [['Polynome([[Fraction(6, 21, "s"), 1]], "x", 0)', '+', 'Polynome([[Fraction(6, 7), 0]], "x", 0)'], ['Polynome([[Fraction(2, 7), 1], [Fraction(6, 7), 0]], "x", 0)']]
    >>> priorites('-Fraction(-6,1)/Fraction(-4,1)')
    [['-', '(', 'Fraction(-6, 1)', '*', 'Fraction(1, -4)', ')'], ['-', 'Fraction("2*-3", "2*-2", "s")'], ['Fraction(-3, 2)']]

.. _texify:

* Convertit la liste de chaînes de caractères contenant des polynômes en liste de chaînes de caractères au format TeX (:func:`texify`)

  .. doctest:: priorites3

    >>> from pyromaths.classes.PolynomesCollege import Polynome
    >>> texify([['4', '+', '5', '-', '6'], ['9', '-', '6'], ['3']])
    ['4+5-6', '9-6', '3']
    >>> texify(priorites('(-7)+8-Polynome([[-4, 1], [-9, 2], [-5, 0]], "x")'))
    ['1-\\left( -4\\,x-9\\,x^{2}-5\\right) ', '1+4\\,x+9\\,x^{2}+5', '9\\,x^{2}+4\\,x+6']
    >>> texify([['Fraction(5,6)', '**', '2']])
    ['\\left(  \\dfrac{5}{6} \\right) ^{2}']

* Convertit la chaîne de caractères contenant des polynômes en une chaîne de caractères au format psplot (:func:`plotify`)

  .. doctest:: priorites3

    >>> plotify('Polynome([[Fraction(-5, 192), 4], [Fraction(2, 96), 3], [Fraction(41, 48), 2], [Fraction(-7, 12), 1], [-4, 0]], "x", False)')
    -5/192*x^4+2/96*x^3+41/48*x^2-7/12*x^1-4

Jinja2
------

:ref:`Ce module <pyromaths.outils.jinja2>` fournit des outils à utiliser avec les templates `jinja2 <http://jinja2.pocoo.org>`__ (voir le :ref:`tutoriel de création d'exercices <ecrire>` pour plus d'informations).

.. currentmodule:: pyromaths.outils.jinja2

.. testsetup:: jinja2

   from pyromaths.outils.jinja2 import *

* Affichage de facteurs


  - Cas de base

      .. doctest:: jinja2

        >>> facteur(2)
        '\\numprint{2}'
        >>> facteur(2.0)
        '\\numprint{2}'
        >>> facteur(2.3)
        '\\numprint{2.3}'

  - Arrondi

      .. doctest:: jinja2

        >>> facteur(12345.6789, arrondi=None)
        '\\numprint{12345.6789}'
        >>> facteur(12345.6789, arrondi=0)
        '\\numprint{12346}'
        >>> facteur(12345.6789, arrondi=2)
        '\\numprint{12345.68}'
        >>> facteur(.6789, arrondi=0)
        '\\numprint{1}'
        >>> facteur(.6789, arrondi=2)
        '\\numprint{0.68}'

    - Affichage (ou non) des zéros à la fin du nombre

      .. doctest:: jinja2

        >>> facteur(12345.6789, arrondi=None, zero=True)
        '\\numprint{12345.6789}'
        >>> facteur(12345, arrondi=2, zero=True)
        '\\numprint{12345.00}'
        >>> facteur(12345, arrondi=2, zero=False)
        '\\numprint{12345}'
        >>> facteur(12345.7, arrondi=2, zero=True)
        '\\numprint{12345.70}'
        >>> facteur(12345.7, arrondi=2, zero=False)
        '\\numprint{12345.7}'

    - Ajout de parenthèses si le nombre est négatif

      .. doctest:: jinja2

        >>> facteur(-2, parentheses=True)
        '\\left(\\numprint{-2}\\right)'
        >>> facteur(2, parentheses=True)
        '\\numprint{2}'

    - Affichage du signe `+`

      .. doctest:: jinja2

        >>> facteur(-2, signe=True)
        '\\numprint{-2}'
        >>> facteur(2, signe=True)
        '\\numprint{+2}'
        >>> facteur(2, signe=False)
        '\\numprint{2}'

    - Si le signe est une opération (et non pas un opérateur unaire, l'afficher à l'extérieur de ``\numprint{}``.

      .. doctest:: jinja2

        >>> facteur(-2, operation=False)
        '\\numprint{-2}'
        >>> facteur(2, signe=True, operation=False)
        '\\numprint{+2}'
        >>> facteur(-2, operation=True)
        '-\\numprint{2}'
        >>> facteur(2, signe=True, operation=True)
        '+\\numprint{2}'

    - Ne pas afficher un produit par 1 ; seulement le signe avec -1 ; ou rien avec 0.

      .. doctest:: jinja2

        >>> facteur(1, produit=True, variable="x")
        '+x'
        >>> facteur(-1, produit=True, variable="x")
        '-x'
        >>> facteur(0, produit=True, variable="x")
        ''

    - Variable

      .. doctest:: jinja2

        >>> facteur(2, variable='x')
        '\\numprint{2}x'
        >>> facteur(-1, produit=True, variable='x')
        '-x'

    - Version courte des arguments

      .. doctest:: jinja2

        >>> facteur(-2, court="2zXo")
        '-\\numprint{2.00}x^2'
        >>> facteur(-2, court="2zXp")
        '\\left(\\numprint{-2.00}x^2\\right)'
        >>> facteur(-2, court="2zY")
        '\\numprint{-2.00}y^2'
        >>> facteur(-1, court="y*")
        '-y'
        >>> facteur(1, court="p*x")
        'x'
        >>> facteur(-1, court="p*x")
        '\\left(-x\\right)'
        >>> facteur(-2, court="p*x")
        '\\left(\\numprint{-2}x\\right)'
        >>> facteur(2, court="p*x")
        '\\numprint{2}x'

* Affichage de matrices

    .. doctest:: jinja2
        >>> matrice([[1, 2], [3, 4]])
        u'\\begin{pmatrix}\\numprint{1} & \\numprint{2}\\\\\\numprint{3} & \\numprint{4}\\\\\\end{pmatrix}'

.. TODO::

    Liste des fichiers dans lesquels aller chercher des classes et fonctions à documenter.

    - ``classes/Racine.py``
    - ``classes/SquareRoot.py``
    - ``classes/Vecteurs.py``
    - ``outils/Arithmetique.py``
    - ``outils/Conversions.py``
    - ``outils/Geometrie.py``
    - ``outils/Polynomes.py``
