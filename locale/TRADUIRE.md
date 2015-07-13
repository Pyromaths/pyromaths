## Conditions préalables pour traduire:
 - gettext
 - msgfmt

### OS X:
Vous devez d'abord installer [brew](http://brew.sh). Après, éxecutez

```
brew install gettext
```

### Unix:
Tout les distributions des systèmes Unix fournissent Gettext et Msgfmt par défaut.

### Windows:
Gettext est [là](http://gnuwin32.sourceforge.net/packages/gettext.htm).


## Géneration des fichiers à traduire
Pour obtenir le fichier `.po`, lancez
```
xgettext -L Python -d pyromaths --from-code utf-8 -o locale/pyromaths.pot -f locale/traductibles
```
depuis répertoire racine du code source.

Créez le répertoire de nom de votre [code de langue](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes) dans '/locale/'.
Dedans, il faut qu'un nouveau répertoire existe: `LC_MESSAGES`.

Copiez le fichier `.pot` dans le répertoire crée sous le nom de `.po`, (exemple pour Italien):
```
cp pyromaths.pot it/LC_MESSAGES/pyromaths.po
```
Pour copiage le fichier `.pot` vers tout les répertoires de langue, lancez depuis `/locale/`:
```
find . -name "LC_MESSAGES" -exec cp pyromaths.pot {}/pyromaths.po \;
```

## Traduction

Dans le fichier `pyromaths.po`, modifiez chaque couple de `msgid` et `msgstr`, comme dans exemple (anglais):
```
msgid "Quitter"
msgstr "Quit"
```

## Finir

Après avoir traduit ce que vous voulez, mettez à jour les fichiers binaires `.mo` depuis votre répertoire de langue (p. ex. `/locale/it/LC_MESSAGES`) pour voir les résultats:
```
msgfmt -o pyromaths.mo pyromaths.po
```
