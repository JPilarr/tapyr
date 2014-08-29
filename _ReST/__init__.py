# -*- coding: utf-8 -*-
# Copyright (C) 2010-2014 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
# This file is part of the package _ReST.
#
# This file is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This file is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this file. If not, see <http://www.gnu.org/licenses/>.
# ****************************************************************************
#
#++
# Name
#    ReST.__init__
#
# Purpose
#    Package augmenting reStructuredText
#
# Revision Dates
#    15-Feb-2010 (CT) Creation
#    29-Aug-2014 (CT) Filter warnings from `PIL`
#    ««revision-date»»···
#--

from _TFL.Package_Namespace import Package_Namespace

ReST = Package_Namespace ()

del Package_Namespace

### Filter PIL warnings to avoid crap like this::
# /usr/lib/python2.7/site-packages/PIL/Image.py:44:
#     DeprecationWarning: classic int division
#   MAX_IMAGE_PIXELS = int(1024 * 1024 * 1024 / 4 / 3)

import warnings
warnings.filterwarnings ("ignore", module = "^PIL.*")
del warnings

### __END__ ReST.__init__
