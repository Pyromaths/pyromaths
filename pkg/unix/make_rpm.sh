#!/bin/bash
echo "*** Make pyromaths RPM archive..."
source $(dirname $0)/default.sh

echo "***   Clean-up previous builds..."
BUILDIR=${BUILD}/pyromaths-rpm
[ -d $BUILDIR ] && rm -r $BUILDIR
rm ${DIST}/pyromaths_${VERSION}-*.rpm

echo "***   Create stripped-down sources..."
mkdir $BUILDIR
cd $BUILDIR
cp -r ${PYROPATH}/src ${PYROPATH}/data .
cp ${PYROPATH}/* .

echo "***   Create .rpm archive..."
python setup.py bdist --formats=rpm -b $BUILD -d $DIST > $OUT &&
echo "***   Done (file is in ${DIST})."
