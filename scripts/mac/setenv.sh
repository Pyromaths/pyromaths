#!/bin/sh

# setenv.sh (Yves GESNEL)
# Un script pour éxécuter Pyromaths sur Mac OS X 
# en spécifiant des variables d'environnement.
# This file is part of Pyromaths.
#
# Pyromaths
# Un programme en Python qui permet de créer des fiches d'exercices types de
# mathématiques niveau collège ainsi que leur corrigé en LaTeX.
# Copyright © 2006 -- Jérôme Ortais (jerome.ortais@pyromaths.org)

# Pyromaths is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Pyromaths is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Pyromaths. if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301 USA. 

# Path to several LaTeX distributions
MACTEX="/usr/texbin:/usr/local/bin"
MACPORTS="/opt/local/bin:/opt/local/sbin"
FINK="/sw/bin"

# Launch Pyromaths with updated path
PWD=$(dirname "$0")
/usr/bin/env PATH="$PATH:$MACTEX:$MACPORTS:$FINK" $PWD/pyromaths
