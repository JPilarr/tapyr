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
#    TFL.SDG.XML.Decl
#
# Purpose
#    Model declarations of a XML document
#
# Revision Dates
#    27-Aug-2004 (CT) Creation
#    23-Jul-2007 (CED) Activated absolute_import
#    06-Aug-2007 (CED) Future import removed again
#    ��revision-date�����
#--



from   _TFL                   import TFL
import _TFL._SDG._XML.Element

class _Decl_ (TFL.SDG.XML.Leaf) :

    front_args           = ("name", "value")

    init_arg_defaults    = dict \
        ( name           = None
        , value          = None
        )

    percent_head         = ""

    _xml_format_body     = \
        """%(elem_type)s %(percent_head)s%(name)s %(::>.value:)s"""
    xml_format           = "".join (("<", _xml_format_body, " >"))

    _autoconvert         = dict \
        ( name           = lambda s, k, v : s._checked_xml_name (v)
        )

# end class _Decl_

class Attlist (_Decl_) :
    """Model an attribute list declaration of a XML document"""

    elem_type            = "!ATTLIST"
    front_args           = ("name", )
    rest_args            = "value"

# end class Attlist

class Element (_Decl_) :
    """Model an element type declaration of a XML document"""

    elem_type            = "!ELEMENT"

# end class Element

class Entity (_Decl_) :
    """Model an entity declaration of a XML document"""

    elem_type            = "!ENTITY"

# end class Entity

class Notation (_Decl_) :
    """Model a notation declaration of a XML document"""

    elem_type            = "!NOTATION"

# end class Notation

class Parameter_Entity (Entity) :
    """Model a parameter entity declaration of a XML document"""

    percent_head         = "%% "

# end class Parameter_Entity

class Unparsed_Entity (Entity) :
    """Model an unparsed entity declaration of a XML document"""

    Ancestor             = Entity

    front_args           = ("name", "value", "notation")

    init_arg_defaults    = dict \
        ( notation       = None
        )

    xml_format           = "".join \
        ( ("<", Ancestor._xml_format_body, " NDATA %(notation)s >")
        )

    _autoconvert         = dict \
        ( notation       = lambda s, k, v : s._checked_xml_name (v)
        )

# end class Unparsed_Entity

Parameter = Parameter_Entity
Unparsed  = Unparsed_Entity

if __name__ != "__main__" :
    TFL.SDG.XML._Export_Module ()
### __END__ TFL.SDG.XML.Decl
