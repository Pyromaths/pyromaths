# Pyromaths Makefile.
#
# See 'make help' for available targets and usage details.

### CONFIG
#
# Pyromaths version
VERSION ?= 14.05
# Archive format(s) produced by 'make src' (bztar,gztar,zip...)
FORMATS ?= bztar,zip
# Verbosity and logging
OUT     ?= > /dev/null       # uncomment: quieter output
#OUT     ?= >> log            # uncomment: log output to file

### ENVIRONMENT VARIABLES
#
# Path
PYRO    := $(PWD)
DIST    := $(PYRO)/dist
BUILD   := $(PYRO)/build
ARCHIVE := $(PYRO)/..
# Target-specific build dir (if needed)
BUILDIR  = $(BUILD)/$@
# Mac app folder
APP     := $(DIST)/Pyromaths.app/Contents
# Project files
FILES   := AUTHORS COPYING NEWS pyromaths README setup.py MANIFEST.in src data

### MANIFESTS
#
# Base manifest (README, src/ and test/ auto-included):
MANIFEST :=                                     \
    include AUTHORS COPYING NEWS                \n\
    exclude MANIFEST.in                         \n\
    global-include src/pyromaths/ex/*/img/*.png \n\
    graft data                                  \n
# Minimal install (i.e. without test/ dir):
MANIFEST-min := $(MANIFEST)                     \
    prune test                                  \n
# Full project sources:
MANIFEST-all := $(MANIFEST)                     \
    graft debian                                \n\
    graft utils                                 \n\
    include Makefile                            \n
# Unix:
MANIFEST-unix := $(MANIFEST-min)                \
    exclude data/qtmac_fr.qm                    \n\
    exclude data/images/pyromaths.icns          \n\
    exclude data/images/pyromaths.ico           \n
# Mac app:
MANIFEST-mac := $(MANIFEST-min)                 \
    prune data/linux                            \n\
    exclude data/images/pyromaths.ico           \n\
    exclude data/images/pyromaths-banniere.png  \n
# Win app:
MANIFEST-win := $(MANIFEST-min)                 \
    prune data/linux                            \n\
    exclude data/qtmac_fr.qm                    \n\
    exclude data/images/pyromaths.icns          \n

### SHORTCUTS & COMPATIBILITY
#
ifeq ($(OS),Windows_NT)
	# Windows
	PYTHON ?= c:/Python27/python.exe
else
	# Unix
	PYTHON ?= python
	ifeq ($(shell uname -s),Darwin)
		# Mac/BSD
		sed-i := sed -i ''
	else
		# GNU
		sed-i := sed -i
	endif
endif
setup := $(PYTHON) setup.py

### MACROS
#
# Remove manifest file, egg-info dir and target build dir, clean-up sources.
clean = rm -f MANIFEST.in && rm -rf src/*.egg-info && rm -rf $(BUILDIR) &&\
        find . -name '*~' | xargs rm -f && find . -iname '*.pyc' | xargs rm -f


# src must be after rpm, otherwise rpm produces a .tar.gz file that replaces the
# .tar.gz source file (should $$FORMATS include gztar).
all: egg rpm deb src

help:
	#
	# Build pyromaths packages in several formats.
	#
	# Usage (Unix):
	#	$$ make src          # Make full-source archive(s)
	#	$$ make egg          # Make python egg
	#	$$ make rpm          # Make RPM package
	#	$$ make deb          # Make DEB package
	#	$$ make [all]        # Make all previous archives/packages
	#
	# Usage (Mac):
	#	$$ make app          # Make standalone application
	#
	# Usage (Windows):
	#	$$ make exe          # Make standalone executable (experimental)
	#
	# And also:
	#	$$ make version      # Apply target $$VERSION [$(VERSION)] to sources
	# 	$$ make clean        # Clean-up build/dist folders and source tree
	#	$$ make repo         # Make debian repository
	#
	# Notes:
	#	- Notice the source achive $$FORMATS produced [$(FORMATS)].
	#	- Mangle with $$OUT to make it quieter/verbose/log to output file.

clean:
	# Clean
	rm -r $(BUILD)/* || mkdir -p $(BUILD)
	rm -r $(DIST)/*  || mkdir -p $(DIST)
	rmdir $(BUILD)
	rmdir $(DIST)
	$(clean)

version:
	# Apply target version ($(VERSION)) to sources
	$(sed-i) "s/VERSION\s*=\s*'.*'/VERSION = '$(VERSION)'/" src/pyromaths/Values.py

src: version
	# Make full-source archive(s) (formats=$(FORMATS))
	$(clean)
	echo "$(MANIFEST-all)" > MANIFEST.in
	$(setup) sdist --formats=$(FORMATS) -d $(DIST) $(OUT)

egg: version
	# Make python egg
	$(clean)
	echo "$(MANIFEST-unix)" > MANIFEST.in
	$(setup) bdist_egg -d $(DIST) $(OUT)

rpm: version
	# Make RPM package
	$(clean)
	echo "$(MANIFEST-unix)" > MANIFEST.in
	$(setup) bdist --formats=rpm -b $(BUILD) -d $(DIST) $(OUT)
	rm $(DIST)/pyromaths-$(VERSION).tar.gz

min: version
	# Make minimalist .tar.bz source archive in $(BUILD)
	$(clean)
	echo "$(MANIFEST-unix)" > MANIFEST.in
	$(setup) sdist --formats=bztar -d $(BUILD) $(OUT)

deb: min
	# Make DEB archive
	$(clean)
	cd $(BUILD) && tar -xjf pyromaths-$(VERSION).tar.bz2              &&\
	    mv pyromaths-$(VERSION) $(BUILDIR)                            &&\
	    mv pyromaths-$(VERSION).tar.bz2 pyromaths_$(VERSION).orig.tar.bz2
	cp -r debian $(BUILDIR)
	cd $(BUILDIR) && debuild clean $(OUT)
	cd $(BUILDIR) && debuild -kB39EE5B6 $(OUT) || exit 0
	mkdir -p $(DIST)
	mv $(BUILD)/pyromaths_$(VERSION)-*_all.deb $(DIST)

repo: deb
	# Create DEB repository
	$(clean)
	mkdir -p $(BUILDIR)/dists
	cp $(DIST)/pyromaths_$(VERSION)*.deb $(BUILDIR)/dists
	cd $(BUILDIR)                                                     &&\
	    sudo dpkg-scanpackages . /dev/null > Packages                 &&\
	    sudo dpkg-scanpackages . /dev/null | gzip -c9 > Packages.gz   &&\
	    sudo dpkg-scanpackages . /dev/null | bzip2 -c9 > Packages.bz2 &&\
	    apt-ftparchive release . > /tmp/Release.tmp                   &&\
	    mv /tmp/Release.tmp Release                                   &&\
	    gpg --default-key "Jérôme Ortais" -bao Release.gpg Release    &&\
	    tar vjcf $(ARCHIVE)/debs-$(VERSION).tar.bz2 dists/ Packages Packages.gz Packages.bz2 Release Release.gpg

data/%.qm: data/%.ts
	# Translate new/updated language files
	lrelease $< -qm $@

app: version data/qtmac_fr.qm
	# Make standalone Mac application
	$(setup) py2app -O2 -b $(BUILD) -d $(DIST) $(OUT)
	# ..Clean-up unnecessary files/folders
	rm -f $(APP)/PkgInfo
	cd $(APP)/Resources && rm -rf site.pyc include lib/python2.*/config lib/python2.*/site.pyc
	cd $(APP)/Frameworks                                     &&\
	    rm -rf *.framework/Contents *.framework/Versions/4.0   \
	           *.framework/Versions/Current *.framework/*.prl  \
	           QtCore.framework/QtCore QtGui.framework/QtGui
	cd $(APP)/Frameworks/Python.framework/Versions/2.*       &&\
	    rm -rf include lib Resources
	rm -rf $(APP)/Resources/lib/python2.7/pyromaths.ex/examples
	find $(APP)/Resources/lib/python2.7/pyromaths.ex \( -name '*.pyc' \) -delete
	rm -rf $(APP)/Frameworks/pyromaths
	# ..Remove all architectures but x86_64..."
	ditto --rsrc --arch x86_64 --hfsCompression $(DIST)/Pyromaths.app $(DIST)/Pyromaths-x86_64.app

exe:
	# Make standalone Windows executable
	# ..Remove previous builds
	rmdir /s /q $(BUILDIR)
	rm $(DIST)/Pyromaths-*-win32.exe
	# ..Create stripped-down sources
	md $(BUILDIR)
	xcopy data $(BUILDIR)/data /i /s
	xcopy src $(BUILDIR)/src /i /s
	copy $(FILES) $(BUILDIR)
	move $(BUILDIR)/pyromaths $(BUILDIR)/Pyromaths.py
	# ..Create standalone exe
	cd $(BUILDIR) && $(setup) innosetup -b $(BUILD) -d $(DIST)
