# -*- coding: iso-8859-15 -*-
# Copyright (C) 2013 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package MOM.DBW.SAW.MY.
#
# This module is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this module. If not, see <http://www.gnu.org/licenses/>.
# #*** </License> ***********************************************************#
#
#++
# Name
#    MOM.DBW.SAW.MY.E_Type_Wrapper
#
# Purpose
#    SAW specific information about a E_Type, specialized for MySQL
#
# Revision Dates
#    27-Aug-2013 (CT) Creation
#    ��revision-date�����
#--

from   __future__ import division, print_function
from   __future__ import absolute_import, unicode_literals

from   _TFL                       import TFL
from   _TFL.pyk                   import pyk

from   _MOM.import_MOM            import MOM, Q
from   _MOM._DBW._SAW             import SA

import _MOM._DBW._SAW.E_Type_Wrapper

class MY_E_Type_Wrapper (MOM.DBW.SAW.E_Type_Wrapper) :
    """SAW specific information about a E_Type, specialized for MySQL"""

    _real_name          = "E_Type_Wrapper"

    def _exec_update (self, session, entity, values, ** xkw) :
        upd_stmt      = self.upd_stmt.values (values)
        last_cid_col  = self.last_cid_col
        reloaded_last = getattr (entity, "_reloaded_last_cid", None)
        if  last_cid_col is not None and reloaded_last :
            upd_stmt = upd_stmt.where (last_cid_col == reloaded_last)
        return session.connection.execute (upd_stmt, ** xkw)
    # end def _exec_update

E_Type_Wrapper = MY_E_Type_Wrapper # end class

if __name__ != "__main__" :
    MOM.DBW.SAW.MY._Export ("*")
### __END__ MOM.DBW.SAW.MY.E_Type_Wrapper
