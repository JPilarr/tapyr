# -*- coding: utf-8 -*-
# Copyright (C) 2010-2014 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
# This module is part of the package MOM.DBW.HPS.
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
#    MOM.DBW.HPS.Change_Manager
#
# Purpose
#    HPS specific manager for change objects
#
# Revision Dates
#    18-May-2010 (CT) Creation
#     4-Aug-2012 (CT) Remove `uncommitted_changes` from `rollback`
#    22-Jan-2013 (MG) Don't reset `max_cid` in `rollback`
#    ««revision-date»»···
#--

from   _MOM                  import MOM
from   _TFL                  import TFL
from   _TFL.pyk              import pyk

import _MOM._DBW._HPS

import _TFL._Meta.Object

class Change_Manager (TFL.Meta.Object) :
    """HPS specific manager for change objects."""

    def __init__ (self) :
        self.max_cid = 0
        self.table   = {}
        self.to_load = []
    # end def __init__

    def add (self, change) :
        cid   = change.cid
        table = self.table
        if cid is None :
            self.max_cid += 1
            change.cid = cid = self.max_cid
        else :
            assert cid not in table
            self.max_cid = max (cid, self.max_cid)
        table [cid] = change
    # end def add

    def rollback (self, session) :
        info  = session.info
        table = self.table
        for cid in range (info.max_cid + 1, self.max_cid + 1) :
            table.pop (cid, None)
    # end def rollback

    def __iter__ (self) :
        return pyk.itervalues (self.table)
    # end def __iter__

# end class Change_Manager

if __name__ != "__main__" :
    MOM.DBW.HPS._Export ("*")
### __END__ MOM.DBW.HPS.Change_Manager
