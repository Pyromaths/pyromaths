#!/bin/bash

# Installe les exercices de tests pour qu'ils puissent être compilés

DOCDIR=$(pwd)/$(dirname $0)
ROOT=$DOCDIR/../../..
TEMPLATEDIR=$ROOT/data/ex/templates
EXERCICEDIR=$ROOT/src/pyromaths/ex/troisiemes

cd $TEMPLATEDIR
for template in $DOCDIR/*/*tex
do
  ln $template
done

cd $EXERCICEDIR
for exercice in $DOCDIR/*/*py
do
  ln $exercice
done
