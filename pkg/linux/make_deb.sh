#!/bin/bash
echo "*** Make pyromaths DEB archive..."
source $(dirname $0)/default.sh

echo "***   Clean-up previous builds..."
BUILDIR=${BUILD}/pyromaths-${VERSION}
[ -d $BUILDIR ] && rm -r $BUILDIR
rm ${BUILD}/pyromaths_${VERSION}* ${DIST}/pyromaths_${VERSION}-*.deb

echo "***   Create stripped-down source archive..."
mkdir $BUILDIR
cd $BUILDIR
cp -r ${PYROPATH}/src ${PYROPATH}/data .
cp ${PYROPATH}/* . > $OUT
cp -r ${PYROPATH}/pkg/linux/debian .
# lightweight source archive in $BUILD
python setup.py sdist --formats=bztar -d $BUILD > $OUT
# Rename source archive according to debuild format
mv ${BUILD}/pyromaths-${VERSION}.tar.bz2 ${BUILD}/pyromaths_${VERSION}.orig.tar.bz2

echo "***   Create .deb archive..."
# Build deb archive
debuild clean > $OUT
debuild -kB39EE5B6 > $OUT
# Move it to $DIST/
mv ${BUILD}/pyromaths_${VERSION}-*_all.deb ${DIST} &&
echo "***   Done (file is in ${DIST})."
