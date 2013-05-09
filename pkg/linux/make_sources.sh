#!/bin/bash
echo "*** Make pyromaths source archive..."
source $(dirname $0)/env.sh

echo "***   Clean-up previous builds..."
rm ${DIST}/pyromaths-${VERSION}.tar.*

echo "***   Create .tar.bz archive..."
cd $PYROPATH
python setup.py sdist --formats=bztar -d $DIST > $OUT &&
echo "***   Done (file is in ${DIST})."
