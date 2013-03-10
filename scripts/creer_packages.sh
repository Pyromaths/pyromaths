#!/bin/bash
VERSION=`date +%y.%m`
PYROPATH=$(cd `dirname $0` && cd .. && pwd)
ARCHIVEPATH=$( cd ${PYROPATH} && cd .. && pwd)

echo "#-------------------------------------
#---- CHANGE LE NUMERO DE VERSION ----
#-------------------------------------"
echo "Quel est le numéro de version ? (Par défaut : ${VERSION})"
read touche
case "$touche" in
  "" )
  ;;
  * )
  VERSION="$touche"
  ;;
esac

#---- CHANGE LE NUMÉRO DE VERSION DE PYROMATHS ----
sed -i "s/VERSION = '.*/VERSION = '${VERSION}'/" ${PYROPATH}/src/Values.py

#---- CHANGE LE NUMÉRO DE VERSION DE PY2APP ----
sed -i "s/<string>[0-9][0-9]\.[0-9][0-9]-*[0-9]*<\/string>/<string>${VERSION}<\/string>/g" ${PYROPATH}/scripts/mac/Info.plist

echo "#-------------------------------------------
#---- SUPPRIME LES FICHIERS TEMPORAIRES ----
#-------------------------------------------"
find ${PYROPATH} -iname '*~' | xargs rm
find ${PYROPATH} -iname '*.pyc' | xargs rm
rm /tmp/pyromaths_*

echo "#--------------------------------------------
#---------- CRÉATION DES SOURCES ------------
#--------------------------------------------"
[ -d /tmp/building_pyromaths ] && rm -r /tmp/building_pyromaths
mkdir /tmp/building_pyromaths
cd /tmp/building_pyromaths
cp -r ${PYROPATH}/src ${PYROPATH}/data .
cp ${PYROPATH}/* .
cp -r ${PYROPATH}/scripts/linux/* .
python setup.py sdist --formats=bztar
cp dist/pyromaths-${VERSION}.tar.bz2 ${ARCHIVEPATH}/pyromaths-${VERSION}-sources.tar.bz2
mv dist/pyromaths-${VERSION}.tar.bz2 /tmp/pyromaths_${VERSION}.orig.tar.bz2

echo "#--------------------------------------------
#--------- CRÉATION DU PAQUET DEB -----------
#--------------------------------------------"
debuild clean
debuild
cp /tmp/pyromaths_${VERSION}-?_all.deb  ${ARCHIVEPATH}

echo "#--------------------------------------------
#--------- CRÉATION DU PAQUET RPM -----------
#--------------------------------------------"
python setup.py bdist --formats=rpm
mv dist/pyromaths-${VERSION}*.noarch.rpm ${ARCHIVEPATH}
cd ${PYROPATH}

echo "#--------------------------------------------
#---------- CRÉATION DU DÉPÔT DEB -----------
#--------------------------------------------"
rm -r /tmp/building_pyromaths
[ -d /tmp/repo_debian ] && rm -r /tmp/repo_debian
mkdir -p /tmp/repo_debian/dists
mv /tmp/pyromaths_${VERSION}* /tmp/repo_debian/dists
cd /tmp/repo_debian
sudo dpkg-scanpackages . /dev/null > Packages &&
sudo dpkg-scanpackages . /dev/null | gzip -c9 > Packages.gz &&
sudo dpkg-scanpackages . /dev/null | bzip2 -c9 > Packages.bz2 &&
apt-ftparchive release . > /tmp/Release.tmp &&
mv /tmp/Release.tmp Release &&
gpg --default-key "Jérôme Ortais" -bao Release.gpg Release &&
tar vjcf ${ARCHIVEPATH}/debs-${VERSION}.tar.bz2 dists/ Packages Packages.gz Packages.bz2 Release Release.gpg &&
cd ${PYROPATH} &&
rm -r /tmp/repo_debian

echo "#-------------------------------------------
#------- CRÉATION DU BINAIRE WINDOWS -------
#-------------------------------------------"
echo "Appuyer sur une touche pour continuer quand le paquet Windows est prêt..."
read touche

#---- LIENS POUR LE SITE PYROMATHS ----
cat > ${ARCHIVEPATH}/pyrosite.txt << EOF

* !/media/img/debian.png(Linux)! "Pyromaths pour Linux - deb":/telecharger/pyromaths_${VERSION}_all.deb
* !/media/img/redhat.png(Linux)! "Pyromaths pour Linux - rpm":/telecharger/pyromaths-${VERSION}-1.noarch.rpm
* !/media/img/macosx.png(Mac OS X)! "Pyromaths pour Mac OS X":/telecharger/pyromaths-${VERSION}-macos.dmg
* !/media/img/winvista.png(Windows)! "Pyromaths pour Windows":/telecharger/pyromaths-${VERSION}-win32.exe
* !/media/img/source.png(Sources)! "Sources de Pyromaths":/telecharger/pyromaths-${VERSION}-sources.tar.bz2

<hr/>

h4. Nouveautés de cette version :

EOF
