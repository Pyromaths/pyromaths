Les tests des exercices
=======================

L'outil ``testexo.py`` est conçu pour tester les exercises durant leur
conception, et plus tard, pour vérifier la non régression.

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
  Compile un exercice. Cette commande est utile pour tester un exercice en cours de rédaction, plutôt que de passer par l'interface graphique.


Description des exercices
^^^^^^^^^^^^^^^^^^^^^^^^^

Les exercices sur lesquels s'appliquent les commandes de ``testexo.py`` sont
décrits comme ``pyromaths/ex/sixiemes/arrondi.py:4,6``, où
``pyromaths/ex/sixiemes/arrondi.py`` est le chemin vers le module Python
contenant l'exercice à tester, et ``4,6`` sont les graines du générateur
aléatoire qui nous intéressent.

Si le chemin est incomplet, tous les sous-modules sont testés. Si les graines
sont omises, suivant le cas, soit tous les tests enregistrés sont considérés,
soit la graine 0 est utilisée.

Description complète
^^^^^^^^^^^^^^^^^^^^

.. argparse::
    :module: testexo
    :func: argument_parser
    :prog: testexo.py
