API par l'exemple
=================

.. testsetup::

   from pyromaths.classes.Fractions import *
   from pyromaths.outils.Fractions import *

.. contents::
   :local:

Cette section est à lire si vous vous posez la question : *« Quels outils existent pour me faciliter l'écriture de nouveaux exercices ? »*

Fractions
---------

.. currentmodule:: pyromaths.classes.Fractions

Création de fractions
"""""""""""""""""""""

* Création d'une fraction (:class:`Fraction`)

  .. doctest::

    >>> repr(Fraction(5, 6))
    Fraction(5, 6)
    >>> repr(Fraction("x", 8))
    Fraction("x", 8)
    >>> repr(Fraction(3.14))
    Fraction(314, 100)
    >>> repr(Fraction(Fraction(1,3)))
    Fraction(1, 3)

* L'option `code` permet de préciser sur la décomposition a pour objectif une simplification ``"s"`` ou une mise au même dénominateur ``"r"``.

  .. doctest::

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

  .. doctest::

    >>> Fraction(2,20) + Fraction(2,10)
    Fraction(2, 20)+Fraction("2*2", "10*2", "r")
    >>> repr(Fraction(5,10) + Fraction(2,10))
    Fraction(7, 10)
    >>> Fraction(5,7) + Fraction(2,10)
    Fraction("5*10", "7*10", "r")+Fraction("2*7", "10*7", "r")

* Différence (:func:`Fraction.__sub__` et :func:`Fraction.__rsub__`)

  .. doctest::

    >>> Fraction(2,20) - Fraction(2,10)
    Fraction(2, 20)-Fraction("2*2", "10*2", "r")
    >>> repr(Fraction(5,10) - Fraction(2,10))
    Fraction(3, 10)
    >>> Fraction(5,7) - Fraction(2,10)
    Fraction("5*10", "7*10", "r")-Fraction("2*7", "10*7", "r")

* Produit (:func:`Fraction.__mul__`)

  .. doctest::

    >>> repr(Fraction(2,5) * Fraction(2,10))
    Fraction("2*2", "5*2*5", "s")
    >>> repr(Fraction(2,5) * 4)
    Fraction(8, 5)

* Quotient (:func:`Fraction.__div__` et :func:`Fraction.__rdiv__`)

  .. doctest::

    >>> Fraction(2,5) / Fraction(10,2)
    Fraction(2, 5)*Fraction(2, 10)
    >>> Fraction(2,5) / 4
    Fraction(2, 5)*Fraction(1, 4)

* Puissance (:func:`Fraction.__pow__`)

  .. doctest::

    >>> repr(Fraction(2,3)**4)
    Fraction(16, 81)

* Opposé (:func:`Fraction.__neg__`)

  .. doctest::

    >>> repr(-Fraction(8,27))
    Fraction(-8, 27)

* Opérateur unaire *+* (:func:`Fraction.__pos__`)

  .. doctest::

    >>> repr(+Fraction(8,27))
    Fraction(8, 27)

* Inverse (:func:`Fraction.__invert__`)

  .. doctest::

    >>> repr(~Fraction(8,27))
    Fraction(27, 8)

* Valeur absolue (:func:`Fraction.__abs__`)

  .. doctest::

      >>> repr(abs(Fraction(-5, 6)))
      Fraction(5, 6)
      >>> repr(abs(-Fraction(5, 6)))
      Fraction(5, 6)

* Troncature (:func:`Fraction.__trunc__`)

  .. doctest::

      >>> import math
      >>> math.trunc(Fraction(7, 6))
      1

.. _operations_specifiques_fractions:

Opérations spécifiques aux fractions
""""""""""""""""""""""""""""""""""""

* Changer le dénominateur (:func:`Fraction.choix_denominateur`). L'argument ``denominateur`` doit être un diviseur du dénominateur de la fraction, sans quoi le résultat sera aberrant.

  .. doctest::

      >>> repr(Fraction(5, 6).choix_denominateur(12))
      Fraction("5*2", "6*2", "r")
      >>> repr(Fraction(5, 6).choix_denominateur(4)) # Résultat aberrant.
      Fraction("5*0", "6*0", "r")

* Réduction du numérateur et du dénominateur (:func:`Fraction.reduit`)

  .. doctest::

    >>> repr(Fraction.reduit(Fraction(2*4,5*4)))
    Fraction(8, 20)
    >>> repr(Fraction.reduit(Fraction('2*4', '5*4')))
    Fraction(8, 20)

* Simplification (:func:`Fraction.simplifie`)

  .. doctest::

    >>> repr(Fraction.simplifie(Fraction(8, 20)))
    Fraction(2, 5)
    >>> repr(Fraction.simplifie(Fraction('2*4','5*4')))
    Fraction(2, 5)

* Décomposition (:func:`Fraction.decompose`)

  .. doctest::

    >>> repr(Fraction.decompose(Fraction(8,20)))
    Fraction("2*4", "5*4", "s")

* Mise au même dénominateur, ou simplification (:func:`Fraction.traitement`)

  .. doctest::

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

  .. doctest::

      >>> float(Fraction(5, 6))
      0.833333333333

* Conversion en entier (:func:`Fraction.__int__`)

  .. note::

     Bizarre, bizarre… Voir `la discussion sur le forum <http://forum.pyromaths.org/viewtopic.php?f=19&t=398>`__.

  .. doctest::

      >>> int(Fraction(15, 6))
      15


Comparaisons
""""""""""""

* Comparaison (:func:`Fraction.__eq__`, :func:`Fraction.__ge__`, :func:`Fraction.__gt__`, :func:`Fraction.__le__`, :func:`Fraction.__lt__`, :func:`Fraction.__ne__`)

  .. doctest::

      >>> Fraction(5, 6) < 1
      True
      >>> Fraction(6, 6) == 1
      True
      >>> Fraction(3, 4) >= Fraction(6, 7)
      False

LaTeX
"""""

* Conversion d'une fraction en LaTeX (:func:`Fraction.__str__`).

  .. doctest::

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

  .. doctest::

    >>> EffectueSommeFractions(Fraction(5, 6), Fraction(2, 3), "+", "AVANT", u"APRÈS")
    ???


.. TODO::

   À supprimer, ou compléter avec :func:`EffectueProduitFractions` et :func:`EffectueQuotientFractions`.

Polynômes
---------

.. TODO::

   À compléter

.. TODO::

    Liste des fichiers dans lesquels aller chercher des classes et fonctions à documenter.

    - ``classes/Polynome.py``
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
