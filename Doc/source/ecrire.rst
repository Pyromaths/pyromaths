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

Dans cette partie, pour générer l'exercice et suivre votre travail, la commande à utiliser est la suivante.

.. code-block:: shell

   utils/pyromaths-cli.py generate EquationPremierDegre:1

Remarquez que par rapport à la commande utilisée dans la partie précédente, un ``:1`` a été ajouté à la fin de la ligne. Il correspond à la graine (`seed`) du générateur pseudo-aléatoire.

.. note::

  Un ordinateur ne sait pas générer du hasard. Il faut ruser.

  Dans notre exercice, nous avons besoin de nombres entiers entre 0 et 9. Pour avoir des nombres aléatoires, à chaque fois que nous utilisons un nombre aléatoire, nous prenons une décimale de π : d'abord `1`, puis `4`, puis `1`, puis `5`, et ainsi de suite. Cela à l'aire aléatoire à première vue, mais deux exécutions successives donneront exactement le même exercice. Améliorons cela.

  Nous gardons le même système, mais au lieu de commencer à la première décimale de π, nous utilisons désormais sur l'heure courante : si le programme est lancé à 13h37, nous utilisons alors les décimales de π à partir de la 1337e. Ainsi, deux exécutions successives donneront deux exercices différents.

  C'est mieux. Mais quand nous créerons notre exercices, nous allons générer encore et encore un exercice, et nous aimerions toujours générer le même (cela facilitera le développement, pour ne pas être perturbé par des valeurs numériques qui changent ; pour qu'un bug introduit par une valeur numérique spécifique n'apparaisse et ne disparaisse pas aléatoirement). Du coup, nous imposons le début de la séquence aléatoire : c'est la signification du ``:1`` ajouté à la fin de la ligne de commande.

  C'est un peu plus compliqué en réalité, mais dans les grande lignes, c'est ainsi qu'un ordinateur génère du hasard. Plus d'informations, par exemple, dans l'article de Wikipédia `Pseudorandom generator <https://en.wikipedia.org/wiki/Pseudorandom_generator>`__.

Si nous voulons générer un autre exercice, il suffit de transformer le ``EquationPremierDegre:1`` en ``EquationPremierDegre:1729``, ``EquationPremierDegre:0123456789``, ou n'importe quel nombre de votre choix.

Code Python
-----------

Du côté de Python, il faut tirer au hasard quatre nombres entiers entre -10 et 10 (sauf 0), et les rendre disponible depuis le code LaTeX. Cela se fait avec le contexte. Toutes les variables présentes dans ce dictionnaire seront accessibles depuis le `template` jinja2.

.. literalinclude::  ecrire/3/equation.py
   :linenos:
   :lineno-start: 27
   :lines: 27-44

Code LaTeX
----------

Du côté de LaTeX, nous allons profiter de la bibliothèque jinja2 pour utiliser les variables rendues disponibles dans le contexte.

.. note::

   Cette note se veut une courte introduction à Jinja2. Pour aller plus loins, rendez-vous sur `le site du projet <http://jinja.pocoo.org/docs/2.10/templates/>`__.

   Un template jinja2 est du code LaTeX qui sera reproduit tel quel dans le document final, sauf que :

   - les variables peuvent être évaluées avec des doubles parenthèses. Pour insérer la valeur de la variable ``a`` du contexte, il faut utiliser ``(( a ))`` ;
   - des structures de contrôle (condition, boucle) peuvent être utilisées entourées par ``(*`` et ``*)``.

L'énoncé est assez simple : il suffit de faire appel aux variables du contexte.

.. literalinclude::  ecrire/3/EquationPremierDegre-statement.tex
   :linenos:

Dans ce code, ``(( a ))`` et ``(( c ))`` sont remplacés par les valeurs des variables ``a`` et ``c`` du contexte, et ``(( "%+d"|format(b) ))`` est remplacé par le résultat du code Python ``"%+d" % b``, ce qui a pour effet d'écrire l'entier ``b`` *avec son signe* (qu'il soit positif ou négatif).

La rédaction du corrigé se fait de la même manière, en remarquant que le code ``(( d - b ))``, par exemple, est remplacé par le résultat du calcul ``d - b``. Notons également l'utilisation de ``(( ((d-b)/(a-c)) | round(2) ))``, qui permet d'arrondir le résultat du calcul ``(d-b)/(a-c)`` à deux chiffres après la virgule. L'ensemble de ces fonctions (``format``, ``round``, etc.), que jinja2 appelle `filters`, est décrit `dans la documentation officielle <http://jinja.pocoo.org/docs/2.10/templates/#list-of-builtin-filters>`__.

.. literalinclude::  ecrire/3/EquationPremierDegre-answer.tex
   :linenos:

Débuggage
---------

Durant cette phase, il est probable que le code LaTeX produit soit un peu compliqué, et contienne des erreurs. Il serait alors pratique de pouvoir observer (si ce n'est plus) ce code avant compilation. C'est possible avec l'option ``--pipe`` de :ref:`pyromaths-cli.py <pyromaths-cli>`.

Cette option permet de définir des commandes (du shell) qui seront executées sur le fichier LaTeX, avant sa compilation. Par exemple :

- ``--pipe cat`` exécute ``cat FICHIER.tex``, et permet d'observer le fichier avant compilation ;
- ``--pipe vim`` exécute ``vim FICHIER.tex``, et permet de modifier le fichier avant compilation ;
- ``--pipe "cp {} draft.tex"`` exécute ``cp FICHIER.tex draft.tex``, et permet d'obtenir une copie du fichier LaTeX, si le problème est trop complexe pour pouvoir être résolu avec les options ci-dessous ;
- et n'importe quelle commande du shell peut-être exécutée, au gré de votre imagination.

Bilan
-----

Nous avons produit l'exercice :download:`exercice.pdf <ecrire/3/exercice.pdf>`. Il fonctionne, mais il y a un petit problème dans le corrigé : le résultat (arrondi) est écrit à l'anglaise, avec un point au lieu d'une virgule.

.. image:: ecrire/3/corrige.png

Cela peut se corriger en utilisant un `filter` personnalisé.

Utilisation de `filters` personnalisées
=======================================

Deux problèmes existent dans le corrigé défini précédemment.

- Le nombre à virgule est écrit avec un point et (cela se voit dans certains cas), dans le cas d'un résultat entier, le code produit ``2.0`` plutôt que ``2`` (cela est dû à Python qui manipule des flottants, et écrit donc la première version pour insister sur le type flottant plutôt qu'entier).
- Le signe utilisé pour donner la solution est :math:`\approx`, que la solution soit exacte ou non.

.. currentmodule:: pyromaths.outils.decimaux

Heureusement, deux fonctions du module :mod:`pyromaths.outils.decimaux` existent dans Pyromaths pour corriger le premier problème : :func:`suppr0` permet de supprimer le `.0` à la fin d'un flottant lorsque c'est utile, et :func:`decimaux` permet de représenter un nombre décimal en respectant les conventions françaises. Encore faut-il que ces fonctions soient accessibles depuis le `template` LaTeX.

TODO

http://jinja.pocoo.org/docs/2.10/api/#custom-filters

Pour corriger le second, TODO.

http://jinja.pocoo.org/docs/2.10/api/#custom-tests


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
