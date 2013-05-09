#!/bin/bash
echo "*** Make pyromaths python egg..."
source $(dirname $0)/default.sh

echo "***   Clean-up previous builds..."
rm ${DIST}/pyromaths-${VERSION}-*.egg

echo "***   Create python egg..."
cd $PYROPATH
python setup.py bdist_egg -d $DIST > $OUT &&
echo "***   Done (file is in ${DIST})."
