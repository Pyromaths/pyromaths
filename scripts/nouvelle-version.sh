#!/bin/bash
DATE=`date +%y.%m`

#---- NETTOYER LES SOURCES ----
find . -iname '*~' | xargs rm
find . -iname '*.pyc' | xargs rm

#---- RÉCUPÉRER LE NUMERO DE VERSION ----
echo "Quel est le numéro de version ? (Par défaut : ${DATE})"
read touche
case "$touche" in
  "" )
  ;;
  * )
  DATE="$touche"
  ;;
esac

#---- CHANGE LE NUMÉRO DE VERSION DE PYROMATHS ----
sed -i "s/    etree.SubElement(child, \"version\").text=\".*\"/    etree.SubElement(child, \"version\").text=\"$DATE\"/" ./outils/System.py

#---- CHANGE LE NUMÉRO DE VERSION DE PY2APP ----
sed -i "s/<string>[0-9][0-9]\.[0-9][0-9]-*[0-9]*<\/string>/<string>${DATE}<\/string>/g" ./scripts/mac/info.plist

#---- CHANGE LE NUMÉRO DE VERSION DE PYEXE ----
sed -i "s/AppVerName=Pyromaths.*/AppVerName=Pyromaths $DATE/" ./scripts/win32/setup-win32.iss
sed -i "s/version=.*/version='$DATE',/" ./scripts/win32/setup-win32.py

#---- CHANGE LE NUMÉRO DE VERSION DE PY2DEB ----
sed -i "s/version = \".*/version = \"$DATE\"/" ./scripts/linux/setup-deb.py
