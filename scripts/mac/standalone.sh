#!/bin/sh

# standalone.sh
# Automatise la réalisation de Pyromaths.app.
# Copyright (C) 2010 Yves Gesnel
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

cd $(dirname $0)
DIST="$PWD/dist"
APP="$DIST/Pyromaths.app/Contents"

echo "*** Remove previous builds..."
rm -rf dist/Pyromaths*.app build/bdist.macosx*

echo "*** Build stand-alone application..."
# L'option -v permet d'afficher le détail de la compilation
if [ "$1" == "-v" ]; then
	python setup.py py2app
else
	python setup.py py2app > /dev/null
fi

echo "*** Apply setenv.sh hack..."
# Copier le script setenv.sh
cp -a setenv.sh $APP/MacOS/
# Remplacer le CFBundleExecutable pyromaths par setenv.sh
sed -i '' '23s/pyromaths/setenv.sh/' $APP/Info.plist

echo "*** Clean-up unnecessary files/folders..."
# /: Supprimer le fichier PkgInfo (codes type & creator codes déjà indiqués dans Info.plist)
rm $APP/PkgInfo
# /Resources: Supprimer les fichiers inutiles
cd $APP/Resources
rm -rf include lib/python2.*/config lib/python2.*/site.pyc
# /Resources/data: Supprimer le dossier linux et les images inutiles
cd $APP/Resources/data
rm -rf linux/ images/pyromaths-banniere.png images/pyromaths.ico
# /Resources/lib: Supprimer les fichiers .so inutiles
cd $APP/Resources/lib/python2.*/lib-dynload
rm _AE.so _codecs_cn.so _codecs_hk.so _codecs_iso2022.so _codecs_jp.so    \
	_codecs_kr.so _codecs_tw.so _Evt.so _File.so _hashlib.so _heapq.so       \
	_locale.so _multibytecodec.so _Res.so _ssl.so array.so bz2.so cPickle.so \
	datetime.so gestalt.so MacOS.so pyexpat.so resource.so strop.so          \
	unicodedata.so PyQt4/Qt.so
# /Frameworks: Supprimer les fichiers inutiles
cd $APP/Frameworks
rm -rf *.framework/Contents *.framework/Versions/4.0 \
	*.framework/Versions/Current *.framework/*.prl    \
	QtCore.framework/QtCore QtGui.framework/QtGui
cd $APP/Frameworks/Python.framework/Versions/2.*
rm -rf include lib Resources

echo "*** Improve french localization..."
# Extract strings from qt_menu.nib
cd $DIST
ibtool --generate-strings-file qt_menu.strings $APP/Frameworks/QtGui.framework/Versions/4/Resources/qt_menu.nib
# Convert qt_menu.strings from UTF-16 to UTF-8
iconv -f utf-16 -t utf-8 qt_menu.strings > qt_menu_tmp.strings
mv -f qt_menu_tmp.strings qt_menu.strings
# Replace the english strings with the french string
sed -i '' 's/Hide/Masquer/g' qt_menu.strings
sed -i '' 's/Others/les autres/g' qt_menu.strings
sed -i '' 's/Show All/Tout afficher/g' qt_menu.strings
sed -i '' 's/Quit/Quitter/g' qt_menu.strings
# Import french strings
cd $APP/Frameworks/QtGui.framework/Versions/4/Resources
ibtool --strings-file $DIST/qt_menu.strings --write qt_menu_french.nib qt_menu.nib
# Clean-up
rm -rf qt_menu.nib
mv qt_menu_french.nib qt_menu.nib
rm $DIST/qt_menu.strings

echo "*** Remove all architectures but x86_64..."
ditto --rsrc --arch x86_64 --hfsCompression $DIST/Pyromaths.app $DIST/Pyromaths-x86_64.app

echo "*** Done."
