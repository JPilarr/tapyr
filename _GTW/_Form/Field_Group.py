# -*- coding: iso-8859-1 -*-
# Copyright (C) 2009-2010 Martin Glueck All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. martin@mangari.org
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
#    GTW.Form.Field_Group
#
# Purpose
#    A group of field which are part of a form
#
# Revision Dates
#    30-Dec-2009 (MG) Creation
#    ��revision-date�����
#--
from   _TFL               import TFL
import _TFL.NO_List
import _TFL._Meta.Object
import _TFL._Meta.Once_Property

from   _GTW               import GTW
import _GTW._Form.Field
import _GTW._Form._Field_Group_

class Field_Group (GTW.Form._Field_Group_) :
    """A group of field's which are part of a form."""

    widget = "html/form.jnj, fg_div_seq"

    def __init__ (self, parent, * fields, ** kw) :
        self.__super.__init__ ()
        self.parent       = parent
        self.fields       = TFL.NO_List (fields)
    # end def __init__

    def _collect_changes (self, request_data) :
        result = {}
        for f in self.fields :
            name = self.parent.get_id (f)
            if name in request_data :
                result [f.name] = request_data [name]
        return result
    # end def _collect_changes

    @property
    def instance (self) :
        return self.parent.instance
    # end def instance

    @TFL.Meta.Once_Property
    def visible_fields (self) :
        return [f for f in self if not f.hidden]
    # end def visible_fields

    def __iter__ (self) :
        return iter (self.fields)
    # end def __iter__

# end class Field_Group


if __name__ != "__main__" :
    GTW.Form._Export ("*")
### __END__ GTW.Form.Field_Group
