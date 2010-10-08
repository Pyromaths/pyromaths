#!/bin/sh

# standalone.sh
# Automatise la réalisation de Pyromaths.app.
# Copyright (C) 2010 Yves Gesnel
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

mac=`/usr/bin/dirname $0`
cd $mac/../..
pyromaths=$PWD

# Utiliser py2app:
cd $mac
python setup.py py2app --packages=lxml

# Supprimer les fichiers debug des frameworks
rm $mac/dist/Pyromaths.app/Contents/Frameworks/*.framework/Versions/4/*_debug
rm $mac/dist/Pyromaths.app/Contents/Frameworks/*.framework/*_debug

# Copier les dossiers modele et img
cp -R $pyromaths/modeles $mac/dist/Pyromaths.app/Contents/MacOS
mkdir $mac/dist/Pyromaths.app/Contents/MacOS/img/
cp $pyromaths/img/pyromaths.png $mac/dist/Pyromaths.app/Contents/MacOS/img/
cp -R $pyromaths/img/vignettes $mac/dist/Pyromaths.app/Contents/MacOS/img/

# copier le script setenv.sh et le rendre exécutable
cp $mac/setenv.sh $mac/dist/Pyromaths.app/Contents/MacOS/
chmod +x $mac/dist/Pyromaths.app/Contents/MacOS/setenv.sh

# Remplacer le CFBundleExecutable pyromaths par le script setenv.sh dans Info.plist
sed -i '' '23s/pyromaths/setenv.sh/' $mac/dist/Pyromaths.app/Contents/Info.plist

# Suppression du code PowerPC et déplacement de Pyromaths finalisé sur le bureau
ditto --rsrc --arch i386 $mac/dist/Pyromaths.app ~/Desktop/Pyromaths.app

# nettoyage
rm -rf $mac/dist/
rm -rf $mac/build