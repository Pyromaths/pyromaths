#!/bin/bash
echo "*** Create DEB repository..."
source $(dirname $0)/default.sh
ARCHIVEPATH=${PYROPATH}/..

echo "***   Clean-up previous builds..."
BUILDIR=${BUILD}/repo_debian
[ -d $BUILDIR ] && rm -r $BUILDIR

echo "***   Create repository..."
mkdir -p ${BUILDIR}/dists
cp ${DIST}/pyromaths_${VERSION}*.deb ${BUILDIR}/dists
cd ${BUILDIR}
sudo dpkg-scanpackages . /dev/null > Packages &&
sudo dpkg-scanpackages . /dev/null | gzip -c9 > Packages.gz &&
sudo dpkg-scanpackages . /dev/null | bzip2 -c9 > Packages.bz2 &&
apt-ftparchive release . > /tmp/Release.tmp &&
echo "***   Sign repository..."
mv /tmp/Release.tmp Release &&
gpg --default-key "Jérôme Ortais" -bao Release.gpg Release &&
tar vjcf ${ARCHIVEPATH}/debs-${VERSION}.tar.bz2 dists/ Packages Packages.gz Packages.bz2 Release Release.gpg
