#!/bin/bash
DIR=$(cd `dirname $0` && pwd)
PYROPATH=$(cd `dirname $0` && cd .. && pwd)
ARCHIVEPATH=$(cd `dirname $0` && cd ../.. && pwd)

# Install build dependencies (if needed)
if [ ! -f /usr/bin/debuild ];
then
    sudo apt-get install devscripts
fi
if [ ! -f /usr/bin/rpm ];
then
    sudo apt-get install rpm
fi

# Update pyromaths version
VERSION=`date +%y.%m`
echo "What is the current version number? (Default: ${VERSION})"
read touche
case "$touche" in
  "" )
  ;;
  * )
  VERSION="$touche"
  ;;
esac
echo "*** Update pyromaths version in sources..."
sed -i "s/VERSION = '.*/VERSION = '${VERSION}'/" ${PYROPATH}/src/pyromaths/Values.py

# Clean-up and create packages
UNIX=$DIR/unix
env VERSION=$VERSION $UNIX/make_clean.sh
env VERSION=$VERSION $UNIX/make_sources.sh $1
env VERSION=$VERSION $UNIX/make_egg.sh $1
env VERSION=$VERSION $UNIX/make_rpm.sh $1
env VERSION=$VERSION $UNIX/make_deb.sh $1 &&
env VERSION=$VERSION $UNIX/make_deb_repo.sh $1

echo "*** Create Windows binary..."
echo "Hit 'enter' when Windows package is ready."
read touche

echo "*** Update pyromaths web-site links..."
cat > ${ARCHIVEPATH}/pyrosite.txt << EOF

* !/media/img/debian.png(Linux)! "Pyromaths pour Linux - deb":/telecharger/pyromaths_${VERSION}_all.deb
* !/media/img/redhat.png(Linux)! "Pyromaths pour Linux - rpm":/telecharger/pyromaths-${VERSION}-1.noarch.rpm
* !/media/img/macosx.png(Mac OS X)! "Pyromaths pour Mac OS X":/telecharger/pyromaths-${VERSION}-macos.dmg
* !/media/img/winvista.png(Windows)! "Pyromaths pour Windows":/telecharger/pyromaths-${VERSION}-win32.exe
* !/media/img/source.png(Sources)! "Sources de Pyromaths":/telecharger/pyromaths-${VERSION}-sources.tar.bz2

<hr/>

h4. Nouveautés de cette version :

EOF
