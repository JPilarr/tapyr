# -*- coding: utf-8 -*-
# Copyright (C) 2011-2012 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************
# This module is part of the package LNX.
#
# This module is licensed under the terms of the BSD 3-Clause License
# <http://www.c-tanzer.at/license/bsd_3c.html>.
# #*** </License> ***********************************************************#
#
#++
# Name
#    LNX.VCS_Typer
#
# Purpose
#    Identify repository type of a version control system
#
# Revision Dates
#    13-May-2011 (CT) Creation
#    ««revision-date»»···
#--

from   __future__  import unicode_literals

from   _LNX import LNX
from   _TFL import TFL
from   _TFL import sos

import _TFL.CAO
import _TFL._Meta.Object

path     = sos.path

class VCS_Typer (TFL.Meta.Object) :

    def __init__ (self, ** kw) :
        self.type_map = kw
    # end def __init__

    def __call__ (self, p) :
        """Return type of repository `p`, if any."""
        for type, rdn in self.type_map.iteritems () :
            if path.isdir (path.join (p, rdn)) :
                return type
    # end def __call__

    def add_type (self, name, repo_dir_name) :
        self.type_map [name] = repo_dir_name
    # end def add_type

# end class VCS_Typer

vcs_typer = VCS_Typer \
    ( cvs      = "CVS"
    , git      = ".git"
    , hg       = ".hg"
    , svn      = ".svn"
    )

def _main (cmd) :
    result = vcs_typer (cmd.arg)
    if result :
        print result
    else :
        raise SystemExit (9)
# end def _main

_Command = TFL.CAO.Cmd \
    ( handler       = _main
    , args          =
        ( "arg:P?Path to repository", )
    , min_args      = 1
    , max_args      = 1
    , description   = "Identify type of repository"
    )

if __name__ != "__main__" :
    LNX._Export ("*", "vcs_typer")
if __name__ == "__main__" :
    _Command ()
### __END__ LNX.VCS_Typer
