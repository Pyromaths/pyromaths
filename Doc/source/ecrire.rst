===================================
Tutoriel : Créer un nouvel exercice
===================================

Cette article décrit la procédure pour créer un nouvel exercice pour Pyromaths. Nous prendrons comme exemple la création d'un exercice de résolution d'équations du premier degré du type :math:`ax+b=cx+d` où les nombres :math:`a`, :math:`b`, :math:`c`, :math:`d` sont des entiers relatifs.

.. note::

   Certains termes techniques anglais
   (comme `template`, `merge`, etc.)
   n'ont volontairement pas été traduits.
   Cette documentation renvoit à d'autres documentation en anglais,
   et pour que la personne lisant ces lignes s'y retrouve d'une documentation à l'autre,
   nous avons fait le choix de conserver les termes anglais plutôt que d'utiliser leur équivalent français.

.. contents::
   :local:
   :depth: 1

Prérequis
=========

Loi
---

Pyromaths est publié sous licence publique GNU version 3 (`GPLv3 <https://fr.wikipedia.org/wiki/Licence_publique_g%C3%A9n%C3%A9rale_GNU>`__). Si vous souhaitez contribuer à Pyromaths en partageant votre exercice, celui-ci devra impérativement être également publié sous cette même licence.

Connaissances
-------------

Créer un exercice pour Pyromaths nécessite de savoir utiliser un minimum :

- LaTeX ;
- Python (version 2) ;
- git.

Une connaissance de la bibliothèque Python `jinja2 <http://jinja2.pocoo.org>`__ est un plus, mais les bases s'apprennent rapidement et sont décrites plus loins dans ce document.

Outils
------

Tous les outils nécessaires pour créer un exercice sont des dépendances de Pyromaths. `Installez <http://www.pyromaths.org/installer/>`__, et faites fonctionner Pyromath : les outils nécessaires pour ce tutoriel seront alors disponibles.

Environnement de travail
========================

Commençons par télécharger les sources de Pyromaths, en utilisant le logiciel `git`. Si vous avez un compte `Github <http://github.com>`__, utilisez :

.. code-block:: shell

   $ git clone git@github.com:Pyromaths/pyromaths.git

Si vous n'avez pas de tel compte, utilisez :

.. code-block:: shell

   $ git clone https://github.com/Pyromaths/pyromaths.git

Puis déplacez vous dans le répertoire `pyromaths` ainsi créé. À partir de maintenant, sauf mention contraire, toutes les commandes sont à exécuter depuis ce répertoire.

Brouillon
=========

La première étape est d'écrire un exercice en LaTeX, sans passer par Python, sans aléa : juste pour observer le rendu final. Utilisez l'outil :ref:`pyromaths-cli.py <pyromaths-cli>`.

.. code-block:: shell

   utils/pyromaths-cli.py dummy

Cette commande a pour effet de créer un modèle d'exercice, sous la forme d'un PDF qui est affiché à l'écran, et d'un fichier LaTeX :file:`exercices.tex`.

Déplacez ce fichier dans un répertoire temporaire, et modifiez-le pour écrire le sujet de votre énoncé, à la place de ``ÉNONCÉ DE L'EXERCICE`` et ``CORRIGÉ DE L'EXERCICE``. Ne vous souciez pas de la manière dont cela sera intégré à Pyromaths ; ne vous souciez pas de la manière dont l'aléa sera intégré : nous verrons cela plus tard. C'est l'occasion de travailler la formulation de l'énoncé et de la solution pour qu'ils soient le plus clair possible.

Ne modifiez que les lignes qui correspondent à l'énoncé ou au corrigé. En particulier, ne modifiez pas le préambule.

Ce fichier doit être compilé avec `latex`, puis converti en pdf avec `dvipdf`. À la fin de cette étape, nous obtenons l'énoncé suivant (:download:`tex <ecrire/1/exercices.tex>`, :download:`pdf <ecrire/1/exercices.pdf>`).

.. literalinclude::  ecrire/1/exercices.tex
   :language: latex
   :linenos:
   :lineno-start: 115
   :lines: 115-146

Première version (sans aléa)
============================

Nous allons maintenant intégrer cet exercice à Pyromaths, sans aléa pour le moment.

Choisissez un identifiant pour votre exercice : un nom composé uniquement de lettres sans accents et de chiffres, sans espaces, comme `ConversionDegresRadians`, `TheoremeDePythagore`, `CoordonneesDuMilieu`, etc. Pour notre exemple, nous choissons `EquationPremierDegre`.

Code Python
-----------

Le code Python de l'exercice doit être placé dans un des sous-dossiers de ``src/pyromaths/ex/``. Dans notre cas, ce sera ``src/pyromaths/ex/troisiemes``. Ensuite, modifiez un des fichiers `.py` déjà existant, ou créez-en un nouveau. Gardez une certaine logique : un exercice sur Pythagore a sa place dans le même fichier qu'un autre exercice sur Pythagore ; un exercice de trigonométrie n'a pas sa place dans un fichier ``matrices.py``. Dans notre cas, nous crréons un nouveau fichier contenant le code suivant.

.. literalinclude:: ecrire/2/equation.py
   :language: python
   :linenos:

Modifiez les parties suivantes :

- ligne 8 : votre nom, et l'année courante ;
- ligne 29 : l'identifiant de l'exercice ;
- ligne 31 : la description de l'exercice ;
- ligne 32 : le niveau de l'exercice (le nombre avant le point sert à trier les niveaux ; celui après le point est le texte qui sera visible à l'utilisateur).

Code LaTeX
----------

Le code LaTeX, quant à lui, doit être placé dans le répertoire ``data/ex/templates``, dans deux fichiers au nom de votre exercices. Reprenez votre fichier :download:`exercices.tex <ecrire/1/exercices.tex>`, et extrayez les lignes correspondant à l'énoncé, que vous écrivez dans le fichier :download:`EquationPremierDegre-statement.tex <ecrire/2/EquationPremierDegre-statement.tex>`, et celles correspondant au corrigé dans le fichier :download:`EquationPremierDegre-answer.tex <ecrire/2/EquationPremierDegre-answer.tex>`.

L'énoncé est alors dans le fichier :download:`EquationPremierDegre-statement.tex <ecrire/2/EquationPremierDegre-statement.tex>`.

.. literalinclude:: ecrire/2/EquationPremierDegre-statement.tex
   :language: latex
   :linenos:

Le corrigé est dans le fichier :download:`EquationPremierDegre-answer.tex <ecrire/2/EquationPremierDegre-answer.tex>`

.. literalinclude:: ecrire/2/EquationPremierDegre-answer.tex
   :language: latex
   :linenos:

Génération de l'exercice
------------------------

Vous pouvez maintenant tester la génération de votre exercice, en exécutant la commande suivante.

.. code-block:: shell

   utils/pyromaths-cli.py generate EquationPremierDegre

Vous obtenez alors le fichier :download:`exercice.pdf <ecrire/2/exercices.pdf>`.

Bilan
-----

Nous avons écrit notre premier exercice, qui est intégré à Pyromaths. Par contre, il n'y a pas d'aléa : les valeurs numériques sont toujours les mêmes. Cela sera résolu dans la partie suivante.

Ajout du hasard
===============

Préambule
---------

Dans cette partie, pour générer l'exercice et suivre votre travail, la commande à utiliser est la suivante.

.. code-block:: shell

   utils/pyromaths-cli.py generate EquationPremierDegre:0

Remarquez que par rapport à la commande utilisée dans la partie précédente, un ``:0`` a été ajouté à la fin de la ligne. Il correspond à la graine (`seed`) du générateur pseudo-aléatoire.

.. note::

  Un ordinateur ne sait pas générer du hasard. Il faut ruser.

  Dans notre exercice, nous avons besoin de nombres entiers entre 0 et 9. Pour avoir des nombres aléatoires, à chaque fois que nous utilisons un nombre aléatoire, nous prenons une décimale de π : d'abord `1`, puis `4`, puis `1`, puis `5`, et ainsi de suite. Cela à l'aire aléatoire à première vue, mais deux exécutions successives donneront exactement le même exercice. Améliorons cela.

  Nous gardons le même système, mais au lieu de commencer à la première décimale de π, nous utilisons désormais sur l'heure courante : si le programme est lancé à 13h37, nous utilisons alors les décimales de π à partir de la 1337e. Ainsi, deux exécutions successives donneront deux exercices différents.

  C'est mieux. Mais quand nous créerons notre exercices, nous allons générer encore et encore un exercice, et nous aimerions toujours générer le même (cela facilitera le développement, pour ne pas être perturbé par des valeurs numériques qui changent ; pour qu'un bug introduit par une valeur numérique spécifique n'apparaisse et ne disparaisse pas aléatoirement). Du coup, nous imposons le début de la séquence aléatoire : c'est la signification du ``:0`` ajouté à la fin de la ligne de commande.

  C'est un peu plus compliqué en réalité, mais dans les grande lignes, c'est ainsi qu'un ordinateur génère du hasard. Plus d'informations, par exemple, dans l'article de Wikipédia `Pseudorandom generator <https://en.wikipedia.org/wiki/Pseudorandom_generator>`__.

Si nous voulons générer un autre exercice, il suffit de transformer le ``EquationPremierDegre:0`` en ``EquationPremierDegre:1729``, ``EquationPremierDegre:0123456789``, ou n'importe quel nombre de votre choix.

Code Python
-----------

TODO

Code LaTeX
----------

TODO

Débuggage
---------

TODO

- Expliquer comment afficher la source avant compilation

Gestion des cas particuliers
============================

TODO

- Erreurs (`1x`, `2x+0`, division par 0)
  - Prendre en compte les cas particuliers avec jinja2
  - Prendre en compte les cas particuliers en python
  - S'arranger pour qu'il n'y ait pas de cas particuliers

Finalisation
============

TODO

Créer les vignettes
-------------------

TODO

Ajouter des tests
-----------------

TODO

Publication !
=============

TODO
