#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
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

from __future__ import unicode_literals
import math

def radians(alpha):
    """**radians**\ (*alpha*)

    Convertit un angle donné en degrés en radians

    :param alpha: angle en degrés
    :type alpha: float

    >>> from pyromaths.outils import Conversions
    >>> '%.2f' % Conversions.radians(30)
    0.52

    :rtype: float
    """
    return alpha * math.pi / 180

def degres(alpha):
    """**radians**\ (*alpha*)

    Convertit un angle donné en radians en degrés

    :param alpha: angle en radians
    :type alpha: float

    >>> from pyromaths.outils import Conversions
    >>> from math import pi
    >>> Conversions.degres(pi/2)
    90.0

    :rtype: float
    """
    return alpha * 180 / math.pi
