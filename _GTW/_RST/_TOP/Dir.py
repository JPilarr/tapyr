# -*- coding: iso-8859-15 -*-
# Copyright (C) 2012 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package GTW.RST.TOP.
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
#    GTW.RST.TOP.Dir
#
# Purpose
#    Model a directory in a tree of pages
#
# Revision Dates
#     6-Jul-2012 (CT) Creation (based on GTW.NAV.Base)
#    18-Jul-2012 (CT) Redefine `add_entries` to set `Index`
#    18-Jul-2012 (CT) Move `add_entries` from `_Dir_` to `_Dir_Base_`
#    18-Jul-2012 (CT) Redefine `_Dir_._get_child` to handle "index"
#    20-Jul-2012 (CT) Factor `_add_index`
#    23-Jul-2012 (CT) Redefine `Dir_V.has_children`
#     3-Aug-2012 (CT) Change `is_current_dir` to use `href`, not `prefix`
#     6-Aug-2012 (MG) Consider `hidden` in  `is_current_dir`
#     7-Aug-2012 (CT) Factor `own_links` to `RST.Base`
#     8-Aug-2012 (MG) Consider `hidden` in `_effective`
#     9-Aug-2012 (CT) Fix `is_current_dir` (test for "/" after `startswith`)
#    17-Sep-2012 (CT) Ignore `TypeError` in `_effective`
#    26-Sep-2012 (CT) Factor `_effective_entry`
#    ��revision-date�����
#--

from   __future__  import absolute_import, division, print_function, unicode_literals

from   _GTW                     import GTW
from   _TFL                     import TFL

import _GTW._RST.Resource
import _GTW._RST._TOP.Base

from   _TFL._Meta.Once_Property import Once_Property
from   _TFL.Decorator           import getattr_safe
from   _TFL.predicate           import enumerate_slice, first

class _TOP_Dir_Base_ (GTW.RST.TOP._Base_, GTW.RST._Dir_Base_) :

    _real_name                 = "_Dir_Base_"

    def add_entries (self, * entries) :
        l = len (self._entries)
        self.__super.add_entries (* entries)
        self._add_index (l)
    # end def add_entries

    def is_current_dir (self, page) :
        if not self.hidden :
            p = page.href
            s = self.href
            return p == s or (p.startswith (s) and p [len (s)] == "/")
    # end def is_current_dir

    def _add_index (self, l) :
        Index = self.Index_Type
        for i, e in enumerate_slice (self._entries, l) :
            e._index = (Index (i))
    # end def _add_index

_Dir_Base_ = _TOP_Dir_Base_ # end class

_Ancestor = _Dir_Base_

class _TOP_Dir_ (_Ancestor, GTW.RST._Dir_) :

    _real_name                 = "_Dir_"

    @property
    @getattr_safe
    def has_children (self) :
        try :
            first (self.own_links)
        except IndexError :
            return False
        else :
            return True
    # end def has_children

    @property
    @getattr_safe
    def _effective (self) :
        dt = self.dir_template
        if dt is None :
            try :
                return self._effective_entry
            except (IndexError, TypeError) :
                pass
        return self
    # end def _effective

    @property
    @getattr_safe
    def _effective_entry (self) :
        page = first (e for e in self.entries if not e.hidden)
        return page._effective
    # end def _effective_entry

    def _get_child (self, child, * grandchildren) :
        result = self.__super._get_child (child, * grandchildren)
        if result is None and child == "index" and not grandchildren :
            return self
        return result
    # end def _get_child

_Dir_ = _TOP_Dir_ # end class

class TOP_Dir (_Dir_, GTW.RST.Dir) :
    """Directory of tree of pages."""

    _real_name                 = "Dir"

Dir = TOP_Dir # end class

class TOP_Dir_V (_Dir_Base_, GTW.RST.Dir_V) :
    """Volatile directory of tree of pages (directory with children,
       without permanent `_entries`).
    """

    _real_name                 = "Dir_V"

    @property
    @getattr_safe
    def has_children (self) :
        return False
    # end def has_children

Dir_V = TOP_Dir_V # end class

if __name__ != "__main__" :
    GTW.RST.TOP._Export ("*", "_Dir_Base_", "_Dir_")
### __END__ GTW.RST.TOP.Dir
