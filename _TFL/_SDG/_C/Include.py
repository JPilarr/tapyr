# -*- coding: iso-8859-15 -*-
# Copyright (C) 2004-2011 TTTech Computertechnik AG. All rights reserved
# Schönbrunnerstraße 7, A--1040 Wien, Austria. office@tttech.com
# ****************************************************************************
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Library General Public
# License as published by the Free Software Foundation; either
# version 2 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Library General Public License for more details.
#
# You should have received a copy of the GNU Library General Public
# License along with this library; if not, write to the Free
# Software Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
# ****************************************************************************
#
#++
# Name
#    TFL.SDG.C.Include
#
# Purpose
#    C-include statements
#
# Revision Dates
#    11-Aug-2004 (MG)  Creation
#    12-Aug-2004 (MG)  `cgi` set to `Decl`
#    13-Aug-2004 (CT)  `Include.c_format` simplified
#                      (`%(filename)s` instead of `%(::.filename:)s`)
#    24-Aug-2004 (CT)  `fn_head` and `fn_tail` added
#    24-Aug-2004 (CT)  Append `.h` if necessary (using `Filename`)
#    11-Sep-2006 (MZO) [21459] searchpath fixed
#    23-Jul-2007 (CED) Activated absolute_import
#    06-Aug-2007 (CED) Future import removed again
#    31-Oct-2011 (MG)  imports corrected
#    26-Feb-2012 (MG) `__future__` imports added
#    ««revision-date»»···
#--



from   __future__  import absolute_import, division, print_function, unicode_literals
from   _TFL              import TFL
from   _TFL.Filename     import Filename
import _TFL._SDG._C.Node
from   _TFL              import sos
import sys

class Include (TFL.SDG.Leaf, TFL.SDG.C.Node) :
    """C-include statements"""

    cgi                    = TFL.SDG.C.Node.Decl
    init_arg_defaults      = dict \
        ( filename         = ""
        )
    front_args             = ("filename", )
    _autoconvert           = dict \
        ( filename         = lambda s, k, v : s._convert_filename (v)
        )

    h_format = c_format    = \
        """#include %(fn_head)s%(filename)s%(fn_tail)s"""

    fn_head                = '<'
    fn_tail                = '>'

    def _convert_filename (self, value) :
        fname = Filename (value, ".h").name
        if sys.platform == "win32" :
            fname = fname.replace (sos.sep, "/")
        return fname
    # end def _convert_filename

# end class Include

Sys_Include = Include

class App_Include (Include) :
    """C-app-include statement"""

    fn_head = '"'
    fn_tail = '"'

# end class App_Include

if __name__ != "__main__" :
    TFL.SDG.C._Export ("*", "Sys_Include")
### __END__ TFL.SDG.C.Include