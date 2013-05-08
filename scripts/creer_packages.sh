#!/bin/bash
VERSION=`date +%y.%m`
PYROPATH=$(cd `dirname $0` && cd .. && pwd)
BUILD="${PYROPATH}/build"
DIST="${PYROPATH}/dist"
ARCHIVEPATH=$( cd ${PYROPATH} && cd .. && pwd)
if [ ! -f /usr/bin/debuild ];
then
    sudo apt-get install devscripts
fi
if [ ! -f /usr/bin/rpm ];
then
    sudo apt-get install rpm
fi

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
sed -i "s/VERSION = '.*/VERSION = '${VERSION}'/" ${PYROPATH}/src/pyromaths/Values.py

echo "#-------------------------------------------
#---- SUPPRIME LES FICHIERS TEMPORAIRES ----
#-------------------------------------------"
find ${PYROPATH} -iname '*~' | xargs rm
find ${PYROPATH} -iname '*.pyc' | xargs rm
rm ${BUILD}/pyromaths_${VERSION}* ${DIST}/pyromaths_${VERSION}-*.deb

echo "#--------------------------------------------
#---------- CRÉATION DES SOURCES ------------
#--------------------------------------------"
[ -d ${BUILD}/building_pyromaths ] && rm -r ${BUILD}/building_pyromaths
mkdir ${BUILD}/building_pyromaths
cd ${BUILD}/building_pyromaths
cp -r ${PYROPATH}/src ${PYROPATH}/data .
cp ${PYROPATH}/* .
cp -r ${PYROPATH}/scripts/linux/* .
python setup.py sdist --formats=bztar -d $BUILD
rm -rf src/*.egg-info
rm MANIFEST
cp ${BUILD}/pyromaths-${VERSION}.tar.bz2 ${ARCHIVEPATH}/pyromaths-${VERSION}-sources.tar.bz2
mv ${BUILD}/pyromaths-${VERSION}.tar.bz2 ${BUILD}/pyromaths_${VERSION}.orig.tar.bz2

echo "#--------------------------------------------
#--------- CRÉATION DU PAQUET DEB -----------
#--------------------------------------------"
debuild clean
debuild -kB39EE5B6
sleep 30
cp ${BUILD}/pyromaths_${VERSION}-?_all.deb ${ARCHIVEPATH}
mv ${BUILD}/pyromaths_${VERSION}-?_all.deb ${DIST}

echo "#--------------------------------------------
#--------- CRÉATION DU PAQUET RPM -----------
#--------------------------------------------"
python setup.py bdist --formats=rpm -d $DIST
cp ${DIST}/pyromaths-${VERSION}*.noarch.rpm ${ARCHIVEPATH}
cd ${PYROPATH}

echo "#--------------------------------------------
#---------- CRÉATION DU DÉPÔT DEB -----------
#--------------------------------------------"
rm -r ${BUILD}/building_pyromaths
[ -d ${BUILD}/repo_debian ] && rm -r ${BUILD}/repo_debian
mkdir -p ${BUILD}/repo_debian/dists
cp ${DIST}/pyromaths_${VERSION}*.deb ${BUILD}/repo_debian/dists
cd ${BUILD}/repo_debian
sudo dpkg-scanpackages . /dev/null > Packages &&
sudo dpkg-scanpackages . /dev/null | gzip -c9 > Packages.gz &&
sudo dpkg-scanpackages . /dev/null | bzip2 -c9 > Packages.bz2 &&
apt-ftparchive release . > /tmp/Release.tmp &&
mv /tmp/Release.tmp Release &&
gpg --default-key "Jérôme Ortais" -bao Release.gpg Release &&
tar vjcf ${ARCHIVEPATH}/debs-${VERSION}.tar.bz2 dists/ Packages Packages.gz Packages.bz2 Release Release.gpg &&
cd ${PYROPATH} &&
rm -r ${BUILD}/repo_debian

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
