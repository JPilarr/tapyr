# -*- coding: iso-8859-15 -*-
# Copyright (C) 2009-2012 Mag. Christian Tanzer All rights reserved
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
#    ��revision-date�����
#--

from   __future__            import unicode_literals

from   _MOM.import_MOM        import *
from   _GTW                   import GTW
from   _GTW._OMP._PAP         import PAP
from   _TFL.I18N              import _

import _GTW._OMP._PAP.Entity
from   _GTW._OMP._PAP.Subject_has_Property   import Subject_has_Property
from   _GTW._OMP._PAP.Phone                  import Phone

_Ancestor_Essence = Subject_has_Property

class Subject_has_Phone (_Ancestor_Essence) :
    """Model the link between a subject and a phone number"""

    is_partial = True

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        class right (_Ancestor.right) :
            """Phone number of subject"""

            role_type     = Phone
            auto_cache    = True

        # end class right

    # end class _Attributes

# end class Subject_has_Phone

if __name__ != "__main__" :
    GTW.OMP.PAP._Export ("*")
### __END__ GTW.OMP.PAP.Subject_has_Phone