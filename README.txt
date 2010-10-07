Version 10.10
* Représentation de données niveau cinquième
* Calcul d'aire de disques niveau cinquième
* Amélioration de la version Mac
** icône 512 pixels par 512 pixels
** Retour du look Aqua
** Position de la fenêtre à l'ouverture améliorée
** Ouverture automatique des fichiers pdf générés
** Pyromaths n'est plus lancé par un applescript
** Diverses améliorations cosmétiques
** Compatibilité avec Mac OS X 10.4
* Exercices de proportionnalités en cinquièmes
** Calcul de la quatrième proportionnelle
** Calculs avec les échelles
* Conversions d'unités
** Exercices de conversions d'unités de volume
** Amélioration de la présentation du tableau de conversions
* Exercice de géométrie dans l'espace niveau sixième
* Visualisation des exercices grâce au bouton "Présentation"

Version 10.06-1
* Correction d’un bug (il manquait un retour ligne après certains \par) dans les exercices de géométrie troisième.
* Ajout de l’utilisation du paquet textcomp pour enjoliver les \degres

Version 10.06
* Exercice de calcul d'aires niveau sixième
* Correction d'un non sens dans les tableaux de conversion niveau sixième : le tableau de conversion se retrouvait parfois avec plusieurs chiffres dans la colonne des mL, mm ou mg.
* Correction d'un bug dans l'affichage de la résolution d'une équation du second degré (merci à Marty de l'avoir signalé)

Version 10.05
* Exercice de construction niveau cinquièmes :
** de triangles
** de parallélogrammes
* Exercice sur les polynomes niveau Lycée
** Équation du second degré
** Factorisation degré 2 et degré 3.
** Étude de fonctions : sens de variation et calcul de limite
*** Polynômes de degré 3
*** Fonction rationnelle
* Exercice de conversion d'unités d'aire niveau sixième
* Exercice sur les arrondis niveau sixième ( par défaut, par excès )
* Exercice sur l'arithmétique niveau troisième :
** Décomposition en facteurs premiers
** PGCD et PPCM avec plusieurs méthodes
** Réflexion sur la décomposition en facteurs premiers
** Applications aux fractions.
* Suppression des exercices autour de Pythagore, niveau troisième
* Amélioration de l'exercice sur les fonctions, niveau troisième
* Correction d'un bug lié à l'encodage sous Windows

Version 10.01
* Un exercice sur les probabilités niveau 3e - par Guillaume Barthélémy
* Modification de l'exercice sur le théorème de Pythagore, niveau 4e :
** la figure n'est plus dessinée
** deux questions dans le même exercice : un calcul de l'hypoténuse et un calcul d'un côté de l'angle droit
* Correction d'une erreur dans le corrigé de l'exercice "Écrire un nombre décimal" - merci à Samuel Coupey pour avoir signalé l'erreur
* Correction d'une erreur dans le corrigé de l'exercice "Fonctions affines" - merci à Nicolas Bissonnier pour avoir signalé l'erreur
* Passage à Python 2.6
** Gestion des caractères accentués dans les noms de fichiers
** Passage à l'utf-8 pour l'encodage des fichiers.
* Nouvelles fonctions et classes pour une utilisation prochaine dans de nouveaux exercices

Version 09.09-1
* Ajout de python-lxml à la liste des dépendances pour le paquet deb de Pyromaths (merci à Cedrick)
* Correction du chemin des icônes pour la version deb de Pyromaths

Version 09.09
* Correction d'un bug de numérotation des calculs sur le niveau troisième
* Correction d'un bug de chemin avec Windows Vista et Windows 7
* Envoi des logs de latex dans un fichier temporaire pour éviter l'ouverture de nombreuses fenêtres sous Windows
* Permet le téléchargement automatique des paquets MikTeX sous Windows.

Version 09.08
* Création de modèles pour choisir l'apparence des fiches - par Arnaud Kientz
* Refonte complète de l'interface graphique :
** Passage à PyQt4
** Possibilité de choisir le niveau affiché sur la fiche
** Utilisation d'un fichier de configuration pour enregistrer les options utilisateurs :
*** Chemin par défaut
*** Nom de fichier par défaut
*** Titre de la fiche
*** Créer un fichier pdf
*** Créer ou non le corrigé
*** Choix du modèle
** Choix de l'ordre des exercices
* Niveau sixième :
** Correction d'un bug dans produits et quotients par 10, 100, 1000
* Niveau cinquième :
** Exercice sur le repérage dans le plan - par Guillaume Barthélémy
* Niveau quatrième :
** Améliorations sur le choix des valeurs dans les exercices sur les fractions
* Niveau troisième :
** Exercice sur les fonctions affines - par Guillaume Barthélémy

Version 08.11
* Niveau sixième :
** Construction de l'image d'un pentagone par une symétrie axiale en utilisant un quadrillage
* Niveau cinquième :
** Construction de l'image d'un pentagone par une symétrie centrale en utilisant un quadrillage
** Fractions égales
** Sommes et différences de fractions (dénominateur de l'une multiple de l'autre)
** Produits de fractions
* Niveau quatrième :
** Sommes et différences de fractions
** Produits et quotients de fractions
** Priorités et fractions

Version 08.05
* Niveau sixième :
** Écrire un nombre décimal en lettres ou en chiffres
** Fractions partage : colorier une fraction d'un rectangle quadrillé.
** Fractions et abscisses : donner l'abscisse de points et placer des points d'abscisse donnée.
** Mesurer, nommer et donner la nature d'angles construits.
** Classer des nombres décimaux dans l'ordre croissant ou décroissant.

Version 08.03
* Niveau sixième :
** QCM : les nombres donnés sont-ils divisibles par 2, 3, 5, 9 ou 10.
** constructions de parallèles et de perpendiculaires.
** Propriétés sur les droites paralèles et perpendiculaires.
* Niveau quatrième :
** trois nouveaux modules sur les puissances.
* Ajout de l'appel au module "wasysym" dans les fichiers LaTeX afin de créer les cases à cocher du QCM.

Version 08.01
* Niveau sixième :
** Donner l'écriture fractionnaire d'un nombre décimal ou l'inverse ;
** Écrire un nombre décimale à partir de sa décomposition décimale.
** Tracer et reconnaître des droites, demi-droites et segments.
* Niveau quatrième :
** Modification du calcul mental pour que les opérations soient parfois des opérations à trous.

Version 07.12.14
  - Niveau sixième :
    . Convertir des unités de masse, contenance et longueur.
    . Placer une virgule dans un nombre entier pour que le chiffre x soit le chiffre des ...
    . Correction d'un bug dans les multiplications posées qui faisait planter Pyromaths quand le produit était inférieur à 1.
    . Modification du calcul mental pour que les opérations soient parfois des opérations à trous.

Version 07.11.23
  - Niveau sixième :
    . produits par 10 ; 100 ; 1000 et 0,1 ; 0,01 ; 0,001 et quotients par 10 ; 100 ; 1000.
    . correction d'un bug sur le calcul mental : la répartition des 4 opérations n'était pas correcte.
    . correction d'un bug sur les opérations à poser : les nombres dans l'énoncé pour la multiplication n'étaient pas les bons.
  - Niveau quatrième :
    . correction d'un bug sur le calcul mental : la répartition des 4 opérations n'était pas correcte.

version 07.11.03
  - Niveau troisième :
    . Correction d'un bug concernant les développements.

version 07.11.01
  - Niveau quatrième :
    . calcul mental sur les nombres entiers relatifs.
  - Niveau sixième :
    . calcul mental sur les nombres entiers ;
    . sommes, différence et produits à effectuer.

version 07.02.23
  - Le nom du fichier contenant le corrigé proposé par défaut est celui du
    fichier d'exercices auquel on ajoute '-corrige'.
  - Ajout du lien http://pyromaths.apinc.org dans le pied de page inférieur
    droit.
  - Des exercices ont été ajoutés au niveau quatrième :
    . fractions (copie du niveau 3e),
    . puissances de 10 (copie du niveau 3e),
    . développements (a+b)(c+d),
    . théorème de Pythagore (copie du niveau 3e),
    . triangle rectangle et cercle (copie du niveau 3e),
    . théorème de Thalès dans le triangle,
    . calcul de mesure d'angle et de longueur à l'aide du cosinus.
  - Un exercice a été ajouté au niveau cinquième :
    . priorités opératoires.
