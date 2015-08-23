Les tests des exercices
=======================

L'outil ``testexo.py`` est conçu pour tester les exercises durant leur
conception, et plus tard, pour vérifier la non régression.

.. contents::
   :local:

Principe
--------

Les exercices de Pyromaths sont générés aléatoirement. Néanmoins, en fixant la
graine (:meth:`random.seed`) du générateur aléatoire, il est possible de
générer deux fois de suite exactement le même exercice.

Le principe de ``testexo.py`` est le suivant : la personne concevant un
exercice peut en valider un énoncé particulier. Plus tard, il sera possible de
vérifier que l'exercice produit toujours exactement la même sortie.

Cet outil est conçu de telle manière à ce que l'appel au module :mod:`unittest`
de Python (par exemple avec ``python -m unittest discover``) effectue tous ces
tests.

Commandes
---------

Description rapide
^^^^^^^^^^^^^^^^^^

Les commandes détaillées sont décrites ci-après. En voici une version
simplifiée.

* Création (``testexo.py create``), suppression des tests (``testexo.py remove``)

* Mise à jour des tests (``testexp.py update``) :
  Effectue les tests, et propose de mettre à jour les tests qui ont changé. Utile si le code LaTeX généré a changé, mais l'exercice reste valide pour autant.

* Exécution des tests (``testexo.py check``) :
  Effectue les tests. Les tests sont aussi exécutés lorsqu'``unittest`` est appelé.

* Compilation d'un exercice (``testexo.py compile``) :
  Compile un exercice, et crée le PDF correspondant (énoncé et solution) dans le dossier courant. Cette commande est utile pour tester un exercice en cours de rédaction, plutôt que de passer par l'interface graphique.

  Il est également possible de fournir des commandes à exécuter sur les fichiers LaTeX avant leur compilation. Ceci est utile pour déceler des erreurs de code LaTeX. Par exemple, la commande ``testexo.py compile -p more EXERCICE`` affiche le code LaTeX dans `more` avant compilation; la commande ``testexo.py compile -p vim EXERCICE`` édite le fichier avec `vim` avant compilation.

* Liste des identifiants des exercices disponibles (``testexo.py lsexos``) :
  Affiche la liste des identifiants des exercices, pour retrouver facilement l'exercice en cours de travail.


Description des exercices
^^^^^^^^^^^^^^^^^^^^^^^^^

Les exercices sur lesquels s'appliquent les commandes de ``testexo.py`` sont
décrits comme ``quatriemes.exo_pythagore:4,6``, où :

* ``quatriemes`` est le niveau de l'exercice ;
* ``exo_pythagore`` est l'identifiant de l'exercice (le nom de la fonction ou
  de la classe qui le définit) ;
* ``4,6`` sont les graines du générateur
  aléatoire qui nous intéressent. Si les graines sont omises, suivant le cas,
  soit tous les tests enregistrés sont considérés, soit la graine 0 est
  utilisée.

La liste des exercices disponibles peut être obtenue avec la commande
``testexp.py lsexos``.

Description complète
^^^^^^^^^^^^^^^^^^^^

.. argparse::
    :module: testexo
    :func: argument_parser
    :prog: testexo.py
