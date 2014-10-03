#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2007-2014 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria.
# Web: http://www.c-tanzer.at/en/ Email: tanzer@swing.co.at
# All rights reserved
# ****************************************************************************
#
# This library is free software; you can redistribute it and/or modify
# it under the terms of the GNU Library General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Library General Public License for more details.
#
# You should have received a copy of the GNU Library General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
# ****************************************************************************
#
#++
# Name
#    _TFL.setup
#
# Purpose
#    Setup file for package namespace TFL
#
# Revision Dates
#    25-Oct-2007 (RS) Creation
#     7-Nov-2007 (CT) Add info, use `if` instead of `assert`
#    26-May-2011 (CT) Change file encoding to `iso-8859-15`
#    18-Nov-2013 (CT) Change file encoding to `utf-8`
#     3-Oct-2014 (CT) Replace `svn` by `git`
#     3-Oct-2014 (CT) Filter out `__pycache__` directories
#    ««revision-date»»···
#--

from   __future__               import print_function

import os
import sys
from   distutils.core           import setup

src_dir = os.path.dirname (__file__)
if src_dir :
    os.chdir (src_dir)

license = 'GNU Library or Lesser General Public License (LGPL)'

name    = "TFL"
p_name  = "_TFL"
v_name  = "TFL-version"

try :
    with open (v_name, "r") as f :
        version = f.read ().strip ()
except IOError :
    print ("No", v_name, "file found")
    raise SystemExit (1)

packages = []
for root, dirs, files in os.walk (os.path.join ('..', p_name)) :
    # ugly: need to modify dirs in place!
    dd = set (d for d in dirs if d.startswith ('_') and d != "__pycache__")
    for d in dirs :
        if d not in dd :
            dirs.remove (d)
    packages.append (root.replace ('/', '.').strip ("."))

setup \
    ( name                 = name
    , version              = version
    , description          =
        "Library with lots of useful stuff (says Ralf Schlatterbeck)"
    # long_description     =
    , license              = license
    , author               = "Christian Tanzer and others"
    , author_email         = "tanzer@swing.co.at"
    , url                  = "https://github.com/Tapyr/tapyr"
    , packages             = packages
    , package_dir          = {p_name : ""}
    , platforms            = 'Any'
    , classifiers          = \
        [ 'Development Status :: 6 - Mature'
        , 'License :: OSI Approved :: ' + license
        , 'Operating System :: OS Independent'
        , 'Programming Language :: Python :: 2'
        , 'Programming Language :: Python :: 3'
        , 'Intended Audience :: Developers'
        , 'Topic :: Software Development :: Libraries'
        , 'Topic :: Software Development :: Libraries :: '
            'Application Frameworks'
        , 'Topic :: Software Development :: Libraries :: Python Modules'
        ]
    )
