# Pyromaths version
VERSION=13.05

# Logging
OUT=> /dev/null       # uncomment: quieter output
#OUT=>> log            # uncomment: log output to file

# Path
PYROPATH=$(PWD)
ARCHIVEPATH=$(PYROPATH)/..
DIST=$(PYROPATH)/dist
BUILD=$(PYROPATH)/build

# Build process
# Target specific build path
RPMBUILDIR=$(BUILD)/pyromaths-rpm
DEBUILDIR=$(BUILD)/pyromaths-$(VERSION)
REPOBUILDIR=$(BUILD)/repo_debian
# Build files in root folder
FILES=AUTHORS COPYING NEWS pyromaths README setup.py
# Mac app folder
APP=$(DIST)/Pyromaths.app/Contents

help:
	#
	# Build pyromaths packages in several formats.
	#
	# Usage (Unix):
	#	$$ make tgz          # Make full-source .tar.gz archive
	#	$$ make tbz          # Make full-source .tar.bz2 archive
	#	$$ make source       # Alias for 'make tbz'
	#	$$ make egg          # Make python egg archive
	#	$$ make rpm          # Make RPM package
	#	$$ make deb          # Make DEB package
	#	$$ make all          # Make all previous archives/packages
	#
	# Usage (Mac):
	#	$$ make app          # Make standalone application
	#
	# And also:
	#	$$ make version      # Print target version
	# 	$$ make clean        # Clean source tree
	#	$$ make purge        # Clean-up build/dist folders
	#	$$ make deb_repo     # Make debian repository for DEB packages
	#
	# Notes:
	#	- Check $$VERSION is up-to-date before running.
	#	- Mangle with $$OUT to make it quieter/verbose/log to output file.

version:
	# Target version: pyromaths-$(VERSION)

clean:
	# Remove backup and compiled files
	find $(PYROPATH) -iname '*~'    | xargs rm -f
	find $(PYROPATH) -iname '*.pyc' | xargs rm -f
	mkdir -p $(BUILD)
	mkdir -p $(DIST)

purge:
	# Remove $$BUILD and $$DIST folders
	rm -rf $(BUILD) $(DIST)

tbz: clean
	# Make pyromaths full-source BZ archive
	# ... Clean-up previous builds
	rm -f $(DIST)/pyromaths-$(VERSION).tar.bz2
	# ... Create .tar.bz archive
	cd $(PYROPATH) && python setup.py sdist --formats=bztar -d $(DIST) $(OUT)

tgz: clean
	# Make pyromaths full-source GZ archive
	# ... Clean-up previous builds
	rm -f $(DIST)/pyromaths-$(VERSION).tar.gz
	# ... Create .tar.gz archive
	cd $(PYROPATH) && python setup.py sdist --formats=gztar -d $(DIST) $(OUT)

source: tbz

egg: clean
	# Make pyromaths python egg
	# ... Clean-up previous builds
	rm -f $(DIST)/pyromaths-$(VERSION)-*.egg
	# ... Create python egg
	cd $(PYROPATH) && python setup.py bdist_egg -d $(DIST) $(OUT)

rpm: clean
	# Make pyromaths RPM archive
	# ... Clean-up previous builds
	rm -rf $(RPMBUILDIR)
	rm -f $(DIST)/pyromaths_$(VERSION)-*.rpm
	# ... Create stripped-down sources
	mkdir $(RPMBUILDIR)
	cp -r $(PYROPATH)/src $(PYROPATH)/data $(RPMBUILDIR)
	cd $(PYROPATH) && cp $(FILES) $(RPMBUILDIR)
	# Create .rpm archive
	cd $(RPMBUILDIR) && python setup.py bdist --formats=rpm -b $(BUILD) -d $(DIST) $(OUT)

deb: clean
	# Make pyromaths DEB archive
	# ... Clean-up previous builds
	rm -rf $(DEBUILDIR)
	rm -f $(BUILD)/pyromaths_$(VERSION)* $(DIST)/pyromaths_$(VERSION)-*.deb
	# ... Create stripped-down source archive..."
	mkdir $(DEBUILDIR)
	cp -r $(PYROPATH)/src $(PYROPATH)/data $(DEBUILDIR)
	cd $(PYROPATH) && cp $(FILES) $(DEBUILDIR)
	cp -r ${PYROPATH}/pkg/unix/debian $(DEBUILDIR)
	cd $(DEBUILDIR) && python setup.py sdist --formats=bztar -d $(BUILD) $(OUT)
	# ... Rename source archive according to debuild format
	mv $(BUILD)/pyromaths-$(VERSION).tar.bz2 $(BUILD)/pyromaths_$(VERSION).orig.tar.bz2
	# ... Create .deb archive
	# ... WARNING: code signing failure will not stop build process
	cd $(DEBUILDIR) && debuild clean $(OUT)
	cd $(DEBUILDIR) && debuild -kB39EE5B6 $(OUT) || exit 0
	# ... Move it to $$DIST
	mv $(BUILD)/pyromaths_$(VERSION)-*_all.deb $(DIST)

deb_repo: deb
	# Create DEB repository
	# ... Clean-up previous builds
	rm -rf $(REPOBUILDIR)
	# ... Create repository
	mkdir -p $(REPOBUILDIR)/dists
	cp $(DIST)/pyromaths_$(VERSION)*.deb $(REPOBUILDIR)/dists
	cd $(REPOBUILDIR) && \
	sudo dpkg-scanpackages . /dev/null > Packages && \
	sudo dpkg-scanpackages . /dev/null | gzip -c9 > Packages.gz && \
	sudo dpkg-scanpackages . /dev/null | bzip2 -c9 > Packages.bz2 && \
	apt-ftparchive release . > /tmp/Release.tmp && \
	mv /tmp/Release.tmp Release && \
	gpg --default-key "Jérôme Ortais" -bao Release.gpg Release && \
	tar vjcf $(ARCHIVEPATH)/debs-$(VERSION).tar.bz2 dists/ Packages Packages.gz Packages.bz2 Release Release.gpg

app: clean
	# Make standalone Mac application
	# ... Remove previous builds
	rm -rf $(DIST)/Pyromaths*.app $(BUILD)/bdist.macosx*
	# ... Build standalone app
	cd $(PYROPATH) && python setup.py py2app -b $(BUILD) -d $(DIST) $(OUT)
	# ... Improve french localization..."
	#     Extract strings from qt_menu.nib
	cd $(DIST) && \
	ibtool --generate-strings-file qt_menu.strings $APP/Frameworks/QtGui.framework/Versions/4/Resources/qt_menu.nib && \
	#     Convert qt_menu.strings from UTF-16 to UTF-8
	iconv -f utf-16 -t utf-8 qt_menu.strings > qt_menu_tmp.strings && \
	mv -f qt_menu_tmp.strings qt_menu.strings &&                      \
	#     Replace the english strings with the french string
	sed -i '' 's/Hide/Masquer/g' qt_menu.strings &&                   \
	sed -i '' 's/Others/les autres/g' qt_menu.strings &&              \
	sed -i '' 's/Show All/Tout afficher/g' qt_menu.strings &&         \
	sed -i '' 's/Quit/Quitter/g' qt_menu.strings
	#     Import french strings
	cd $(APP)/Frameworks/QtGui.framework/Versions/4/Resources && \
	ibtool --strings-file $DIST/qt_menu.strings --write qt_menu_french.nib qt_menu.nib && \
	#     Clean-up
	rm -rf qt_menu.nib && mv qt_menu_french.nib qt_menu.nib
	rm $(DIST)/qt_menu.strings
	# ... Clean-up unnecessary files/folders
	rm -f $(APP)/PkgInfo
	cd $(APP)/Resources && rm -rf include lib/python2.*/config lib/python2.*/site.pyc
	cd $(APP)/Resources/lib/python2.*/lib-dynload && \
	rm -f _AE.so _codecs_cn.so _codecs_hk.so _codecs_iso2022.so _codecs_jp.so   \
		_codecs_kr.so _codecs_tw.so _Evt.so _File.so _hashlib.so _heapq.so      \
		_locale.so _multibytecodec.so _Res.so _ssl.so array.so bz2.so cPickle.so\
		datetime.so gestalt.so MacOS.so pyexpat.so resource.so strop.so         \
		unicodedata.so PyQt4/Qt.so
	cd $(APP)/Frameworks &&                               \
	rm -rf *.framework/Contents *.framework/Versions/4.0  \
		*.framework/Versions/Current *.framework/*.prl    \
		QtCore.framework/QtCore QtGui.framework/QtGui
	cd $(APP)/Frameworks/Python.framework/Versions/2.* && \
	rm -rf include lib Resources
	# ... Remove all architectures but x86_64..."
	ditto --rsrc --arch x86_64 --hfsCompression $(DIST)/Pyromaths.app $(DIST)/Pyromaths-x86_64.app


all: tbz tgz egg rpm deb
