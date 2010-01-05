# -*- coding: iso-8859-1 -*-
# Copyright (C) 2009 Martin Glueck. All rights reserved
# Langstrasse 4, 2244 Spannberg, Austria. martin@mangari.org
# ****************************************************************************
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Affero General Public
# License as published by the Free Software Foundation; either
# version 3 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public
# License along with this library; if not, write to the Free
# Software Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
# ****************************************************************************
#
#++
# Name
#    MOM.DBW.SA.Type
#
# Purpose
#    Implement composite sort-key for list of sort criteria
#
# Revision Dates
#     2009-Oct-19 (MG) Creation
#     4-Nov-2009 (MG) Use `TFL.Add_To_Class`
#    31-Dec-2009 (MG) `_sa_numeric` added
#    ��revision-date�����
#--

from   _TFL               import TFL
import _TFL.Decorator
from   _MOM               import MOM
import _MOM._Attr.Type
import _MOM._Attr

Attr = MOM.Attr

from sqlalchemy     import types, schema # Table, Column, Integer, String, Boolean, MetaData, ForeignKey

@TFL.Add_To_Class ("_sa_column", Attr.A_Boolean)
def _sa_bool (self, kind, ** kw) :
    return schema.Column (self._sa_col_name, types.Boolean, ** kw)
# end def _sa_bool

@TFL.Add_To_Class ("_sa_column", Attr.A_String)
def _sa_string (self, kind, ** kw) :
    return schema.Column \
        (self._sa_col_name, types.String (self.max_length), ** kw)
# end def _sa_string

@TFL.Add_To_Class ("_sa_column", Attr.A_Int)
def _sa_int (self, kind, ** kw) :
    return schema.Column (self._sa_col_name, types.Integer, ** kw)
# end def _sa_int

@TFL.Add_To_Class ("_sa_column", Attr.A_Decimal)
def _sa_numeric (self, kind, ** kw) :
    return schema.Column \
        ( self._sa_col_name
        , types.Numeric (self.max_digits, self.decimal_places)
        , ** kw
        )
# end def _sa_numeric

@TFL.Add_To_Class ("_sa_column", Attr.A_Float)
def _sa_float (self, kind, ** kw) :
    return schema.Column (self._sa_col_name, types.Float, ** kw)
# end def _sa_float

@TFL.Add_To_Class ("_sa_column", Attr.A_Link_Role_EB)
def _sa_role_eb (self, kind, ** kw) :
    return schema.Column \
        ( self._sa_col_name
        , types.Integer
        , schema.ForeignKey
            ( "%s.%s"
            % (self.role_type._sa_table.name, self.role_type._sa_pk_name)
            )
        )
# end def _sa_role_eb

### __END__ MOM.DBW.SA.Type
