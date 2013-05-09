# Pyromaths version
VERSION=13.05

# Logging
OUT=> /dev/null       # uncomment: quieter output
#OUT=>> log            # uncomment: log output to file

# Path
PYROPATH=$(PWD)/../..
ARCHIVEPATH=$(PYROPATH)/..
DIST=$(PYROPATH)/dist
BUILD=$(PYROPATH)/build
# Target specific build path
RPMBUILDIR=$(BUILD)/pyromaths-rpm
DEBUILDIR=$(BUILD)/pyromaths-$(VERSION)
REPOBUILDIR=$(BUILD)/repo_debian

help:
	#
	# Build pyromaths packages in several formats.
	#
	# Usage:
	#	$$ make tgz          # Make full-source .tar.gz archive
	#	$$ make tbz          # Make full-source .tar.bz2 archive
	#	$$ make source       # Alias for 'make tbz'
	#	$$ make egg          # Make python egg archive
	#	$$ make rpm          # Make RPM package
	#	$$ make deb          # Make DEB package
	#	$$ make all          # Make all previous archives/packages
	#
	# And also:
	#	$$ make version      # Print target version
	# 	$$ make clean        # Clean source tree
	#	$$ make purge        # Remove build/dist folders
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

purge: clean
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
	cp -r $(PYROPATH)/src $(PYROPATH)/data . $(RPMBUILDIR)
	cp -f $(PYROPATH)/* $(RPMBUILDIR) || exit 0
	# Create .rpm archive
	cd $(RPMBUILDIR) && python setup.py bdist --formats=rpm -b $(BUILD) -d $(DIST) $(OUT)

deb: clean
	# Make pyromaths DEB archive
	# ... Clean-up previous builds
	rm -rf $(DEBUILDIR)
	rm -f $(BUILD)/pyromaths_$(VERSION)* $(DIST)/pyromaths_$(VERSION)-*.deb
	# ... Create stripped-down source archive..."
	mkdir $(DEBUILDIR)
	cp -r ${PYROPATH}/src ${PYROPATH}/data $(DEBUILDIR)
	cp ${PYROPATH}/* $(DEBUILDIR) || exit 0
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

all: source egg rpm deb
