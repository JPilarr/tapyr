# -*- coding: iso-8859-1 -*-
# Copyright (C) 2004 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.cluster
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
#    TFL.SDG.C.Arg_List
#
# Purpose
#    Model C argument lists
#
# Revision Dates
#    28-Jul-2004 (CT) Creation
#    ��revision-date�����
#--

from   _TFL              import TFL
import _TFL._SDG._C.Node
import _TFL._SDG._C.Expression
import _TFL._SDG._C.Var

from   Regexp            import *

class Arg_List (TFL.SDG.C.Node) :
    """Model C argument lists"""


    children_group_names = (Decl, ) = range (1)

    h_format = c_format  = """%(:sep=%(base_indent)s, :*decl_children:)s"""

    arg_pat              = Regexp \
        ( r"^"
          r"(?: "
          r"  (?P<void> void)"
          r"| (?P<type> .+) \s+ (?P<name> [_a-z][_a-z0-9]*)"
          r")"
          r"$"
        , re.VERBOSE | re.IGNORECASE
        )

    def __init__ (self, * children, ** kw) :
        children = self._convert_children (children)
        self.__super.__init__ (* children, ** kw)
    # end def __init__

    def add (self, * children) :
        """Append all `children' to `self.children'"""
        print self.children_groups
        return self.__super.add (* children)
    # end def add

    def _convert_children (self, children) :
        if len (children) == 1 and isinstance (children [0], str) :
            children = [c.strip () for c in children [0].split (",")]
        result = []
        for c in children :
            if isinstance (c, str) :
                if self.arg_pat.match (c) :
                    if self.arg_pat.void :
                        c = TFL.SDG.C.Expression (self.arg_pat.void)
                    else :
                        c = TFL.SDG.C.Var \
                                (self.arg_pat.type, self.arg_pat.name)
                else :
                    raise TFL.SDG.C.Invalid_Node, (self, c)
            c.cgi     = self.Decl
            c.trailer = ""
            result.append (c)
        return result
    # end def _convert_children

# end class Arg_List

if __name__ != "__main__" :
    TFL.SDG.C._Export ("*")
### __END__ TFL.SDG.C.Arg_List
