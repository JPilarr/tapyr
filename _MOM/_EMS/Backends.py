# -*- coding: utf-8 -*-
# Copyright (C) 2010-2014 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
# This module is part of the package MOM.EMS.
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
#    MOM.EMS.Backends
#
# Purpose
#    Provide access to supported EMS/DBW backends
#
# Revision Dates
#    23-Jun-2010 (CT) Creation
#    19-Jun-2013 (CT) Add `SAW`
#    21-Jun-2013 (CT) Fix `SAW` entries of `Map` (DB-specific packages)
#     7-Jul-2013 (CT) Add `EMS.SAW`
#    23-Aug-2013 (CT) Remove `SAS` backends
#    ««revision-date»»···
#--

"""
    >>> print MOM.EMS.Backends.get ("hps:")
    (<class '_MOM._EMS.Hash.Manager'>, <class '_MOM._DBW._HPS.Manager.Manager'>, <class '_MOM._DBW._HPS.DBS.HPS'>)

    >>> print MOM.EMS.Backends.get ("postgresql:")
    (<class '_MOM._EMS.SAW.Manager'>, <class '_MOM._DBW._SAW._PG.Manager.Manager'>, <class '_MOM._DBW._SAW._PG.DBS.DBS'>)

    >>> print MOM.EMS.Backends.get ("sqlite:")
    (<class '_MOM._EMS.SAW.Manager'>, <class '_MOM._DBW._SAW._SQ.Manager.Manager'>, <class '_MOM._DBW._SAW._SQ.DBS.DBS'>)

"""

from   _MOM                   import MOM
import _MOM._EMS

_hps = ("Hash", "_HPS.Manager")

Map  = dict \
    ( { ""    : _hps
      , None  : _hps
      }
    , hps        = _hps
    , mysql      = ("SAW",  "_SAW._MY.Manager")
    , postgresql = ("SAW",  "_SAW._PG.Manager")
    , sqlite     = ("SAW",  "_SAW._SQ.Manager")
    )

def get (url) :
    """Return (`EMS`, `DBW`) for `scheme` of `url`."""
    import _MOM._DBW
    if ":" not in url :
        raise ValueError ("`%s` doesn't contain a scheme" % url)
    scheme = url.split (":", 1) [0]
    e, d   = Map [scheme]
    EMS    = MOM.EMS._Import_Module (e).Manager
    DBW    = MOM.DBW._Import_Module (d).Manager
    return (EMS, DBW, DBW.DBS_map [scheme])
# end def get

if __name__ != "__main__" :
    MOM.EMS._Export_Module ()
### __END__ MOM.EMS.Backends
