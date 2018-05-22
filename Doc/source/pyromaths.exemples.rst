API par l'exemple
=================

.. contents::
   :local:

Cette section est à lire si vous vous posez la question : *« Quels outils existent pour me faciliter l'écriture de nouveaux exercices ? »*

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

    * Pour la plupart des opérations, le résultat n'est pas simplifié. Voir la partie :ref:`operations_specifiques_fractions`.
    * Le type de la valeur retournée par ces méthode est soit une :class:`Fraction`, soit une chaîne de caractère, qui peut ensuite être manipulée avec le module :mod:`pyromaths.outils.Priorites3`.

La partie :ref:`calculs_etapes_fractions` décrit quelques fonctions utiles pour détailler les calculs de certaines opérations sur les fractions.

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

* Conversion en entier (:func:`Fraction.__int__`)

  .. warning::

     Bizarre, bizarre… Voir `la discussion sur le forum <http://forum.pyromaths.org/viewtopic.php?f=19&t=398>`__.

  .. doctest:: fraction

      >>> int(Fraction(15, 6))
      15


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

.. _calculs_etapes_fractions:

Calculs avec étapes
"""""""""""""""""""

.. currentmodule:: pyromaths.outils.Fractions

.. warning::

    Ces fonctions sont peut-être obsolètes. Voir `la discussion sur le forum <http://forum.pyromaths.org/viewtopic.php?f=19&t=399>`__.

    Si ces fonctions sont supprimées, supprimer aussi la référence à cette partie plus haut dans la page.

* Somme et Différence (:func:`EffectueSommeFractions`). Pour choisir l'opération, utiliser comme argument ``s="+"`` ou ``s="-"``.

  .. code-block:: python

    >>> EffectueSommeFractions(Fraction(5, 6), Fraction(2, 3), "+", "AVANT", u"APRÈS")
    ???


.. TODO::

   À supprimer, ou compléter avec :func:`EffectueProduitFractions` et :func:`EffectueQuotientFractions`.

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

.. TODO::

   À compléter

.. testsetup:: polynomescollege

   from pyromaths.classes.PolynomesCollege import *

* TODO (:func:`Polynome.TODO`).

  .. doctest:: polynomescollege

     >>> repr(Polynome([[-3, 2], [2, 1], [1, 0]]))
     Polynome([[-3, 2], [2, 1], [1, 0]], "x", 0)

.. _polynomes_degre2:

Polynômes du second degré
-------------------------

.. TODO::

   À compléter

.. testsetup:: polynomedegre2

   from pyromaths.classes.SecondDegre import *

* TODO (:func:`Polynome.TODO`).

  .. doctest:: polynomedegre2

     >>> repr(Poly2(2, 3, 4))
     Poly2(2, 3, 4)

.. TODO::

    Liste des fichiers dans lesquels aller chercher des classes et fonctions à documenter.

    - ``classes/PolynomesCollege.py``
    - ``classes/Racine.py``
    - ``classes/SecondDegre.py``
    - ``classes/SquareRoot.py``
    - ``classes/Terme.py``
    - ``classes/Vecteurs.py``
    - ``outils/Affichage.py``
    - ``outils/Arithmetique.py``
    - ``outils/Conversions.py``
    - ``outils/Geometrie.py``
    - ``outils/Polynomes.py``
    - ``outils/Priorites3.py``
    - ``outils/TeXMiseEnForme.py``
    - ``outils/decimaux.py``
