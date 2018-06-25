#!/usr/bin/env python3

# Pyromaths
# Un programme en Python qui permet de créer des fiches d'exercices types de
# mathématiques niveau collège ainsi que leur corrigé en LaTeX.
# Copyright (C) 2006 -- Jérôme Ortais (jerome.ortais@pyromaths.org)
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301 USA
#

from __future__ import unicode_literals
from builtins import str
import re

def suppr0(nombre):
    """Supprime le zéro inutile après la virgule d'un float, si c'est possible."""
    if round(nombre, 0) == nombre:
        return int(nombre)
    else:
        return nombre

#---------------------------------------------------------------------
# Affichages des nombres décimaux
#---------------------------------------------------------------------
def decimaux(nb, mathenv=0):
    """nb est un float ou une str"""
    pattern = re.compile(r"^(-?\d+)\.*(\d*)e?([\+\-]?\d*)$")
    entiere, decimale, exposant = pattern.search(format(float(nb), ".15g")).groups() #arrondit les floats
    if exposant:
        if int(exposant) > 0:
            if int(exposant) < len(decimale):
                entiere = entiere + decimale[:int(exposant)]
                decimale = decimale[int(exposant):]
            else:
                entiere = entiere + decimale + "0"*(int(exposant) - len(decimale))
                decimale = ''
        else:
            if -int(exposant) < len(entiere):
                decimale = entiere[len(entiere) + int(exposant):] + decimale
                entiere = entiere[:len(entiere) + int(exposant)]
            else:
                decimale = "0"*(-int(exposant) - len(entiere)) + str(abs(int(entiere))) + decimale.rstrip("0")
                if entiere[0] == "-": entiere = "-0"
                else: entiere = "0"

    pattern = re.compile(r"^(-?\d{1,3}?)" + "(\d{3})" * \
                         ((len(entiere) - 1 - (entiere[0] == '-')) // 3) + "$")
    partie_entiere = pattern.search(entiere).groups()
    if decimale and int(decimale):
        """Vérifie si la partie décimale existe et si elle est différente de
        zéro"""
        pattern = re.compile(r"^" + "(\d{3})" * ((len(decimale) - 1) // 3) + \
                             "(\d{1,3})?$")
        partie_decimale = pattern.search(decimale).groups()
        if mathenv:
            return "{,}".join(("\,".join(partie_entiere),
                               "\,".join(partie_decimale)))
        else:
            return ",".join(("\,".join(partie_entiere),
                             "\,".join(partie_decimale)))
    else:
        return "\,".join(partie_entiere)
