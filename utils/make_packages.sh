#!/bin/bash
DIR=$(cd `dirname $0` && pwd)
PYROPATH=$(cd `dirname $0` && cd .. && pwd)
# Install build dependencies (if needed)
if [ ! -f /usr/bin/debuild ];
then
    sudo apt-get install devscripts equivs
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
echo "*** Update pyromaths version..."
sed -i "s/VERSION ?= .*/VERSION ?= ${VERSION}/" ${PYROPATH}/Makefile

# Clean-up and create Documentation
cd $PYROPATH/Doc
make clean
make doctest
make html

# Prepare Changelog
cd $PYROPATH
head -20 NEWS
dch -v ${VERSION}-1
dch -r

# Clean-up and create packages
make clean
make all
make repo

echo "*** Create Windows binary..."
echo "Hit 'enter' when Windows package is ready."
read touche

echo "*** Tag git develop ***"
echo "Do you want to commit and tag the git develop branch (o/N)?"
read touche
case "$touche" in
  [oO] )
  git commit -am 'Pyromaths Release'
  git tag -u B39EE5B6 version-${VERSION} -m "Pyromaths ${VERSION}"
  #git push --tags:
  ;;
esac

echo "*** Update pyromaths web-site links..."
cat > ${PYROPATH}/pyrosite.txt << EOF

* !/media/img/debian.png(Linux)! "Pyromaths pour Linux - deb":/telecharger/pyromaths_${VERSION}-1_all.deb
* !/media/img/redhat.png(Linux)! "Pyromaths pour Linux - rpm":/telecharger/pyromaths-${VERSION}-1.noarch.rpm
* !/media/img/macosx.png(Mac OS X)! "Pyromaths pour Mac OS X":/telecharger/pyromaths-${VERSION}-macos.dmg
* !/media/img/winvista.png(Windows)! "Pyromaths pour Windows":/telecharger/pyromaths-${VERSION}-win32.exe
* !/media/img/source.png(Sources)! "Sources de Pyromaths":/telecharger/pyromaths-${VERSION}-sources.tar.bz2

<hr/>

h4. Nouveautés de cette version :

EOF
