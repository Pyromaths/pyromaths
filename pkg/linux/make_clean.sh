#!/bin/bash
echo "*** Clean-up pyromaths source tree..."
source $(dirname $0)/env.sh

find ${PYROPATH} -iname '*~' | xargs rm
find ${PYROPATH} -iname '*.pyc' | xargs rm
