# -*- coding: utf-8 -*-
# Copyright (C) 2009-2013 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
# This module is part of the package GTW.OMP.PAP.
#
# This module is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this module. If not, see <http://www.gnu.org/licenses/>.
# ****************************************************************************
#
#++
# Name
#    GTW.OMP.PAP.Subject_has_Phone
#
# Purpose
#    Model the link between a subject and a phone number
#
# Revision Dates
#    30-Dec-2009 (CT) Creation
#     3-Feb-2010 (CT) `_Person_has_Property_` factored
#    19-Feb-2010 (MG) `left.auto_cache` added
#    28-Feb-2010 (CT) `extension` is a `A_Numeric_String` (instead of `A_Int`)
#    18-Nov-2011 (CT) Import `unicode_literals` from `__future__`
#    22-Mar-2012 (CT) Change from `Person_has_Phone` to `Subject_has_Phone`
#    12-Sep-2012 (CT) Add `extension`
#    16-Apr-2013 (CT) Update `auto_derive_np_kw` instead of explicit class
#    ««revision-date»»···
#--

from   __future__             import unicode_literals

from   _MOM.import_MOM        import *

from   _GTW._OMP._PAP.Subject_has_Property   import Subject_has_Property

class extension (A_Numeric_String) :
    """Extension number used in PBX"""

    kind            = Attr.Primary_Optional
    example         = "99"
    max_length      = 5

# end class extension

_kw = Subject_has_Property.auto_derive_np_kw ["Subject_has_Phone"]

_kw ["extra_attributes"].update \
    ( extension = extension
    )

_kw ["properties"].update \
    ( __doc__ = """Link a %(left.role_name)s to a phone number"""
    )

_kw ["right"].update \
    ( __doc__    = """Phone number of %(left.role_name)s"""
    , is_partial = True
    )

del extension

### __END__ GTW.OMP.PAP.Subject_has_Phone
