#!/bin/bash
#
# Linux build process: default values for environment variables.

# Pyromaths version
[ -z $VERSION ]  && VERSION=`date +%y.%m`

# Pyromaths project path
[ -z $PYROPATH ] && PYROPATH=$(cd `dirname $0` && cd ../.. && pwd)

# build and dist directories
[ -z $BUILD ]    && BUILD=${PYROPATH}/build
[ -z $DIST ]     && DIST=${PYROPATH}/dist

# Verbose mode
[ -z $OUT ]      && OUT=/dev/null
[ "${1}" = "-v" ] && OUT=/dev/stdout
