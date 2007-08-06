# -*- coding: iso-8859-1 -*-
# Copyright (C) 2003-2005 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
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
#    Ival_Map
#
# Purpose
#    Map intervals to values
#
# Revision Dates
#     5-Jul-2003 (CT) Creation
#    23-Jul-2007 (CED) Activated absolute_import
#    06-Aug-2007 (CED) Future import removed again
#    ��revision-date�����
#--



from   _TFL               import TFL
from   _TFL._Meta         import Meta
import _TFL._Meta.Object
import _TFL.predicate

class Ival_Map (Meta.Object) :
    """Mapping of intervals to values.

       >>> ivm = Ival_Map ((500, 65), (1500, 85), (100000, 95), (1000, 75))
       >>> ivm
       [(500, 65), (1000, 75), (1500, 85), (100000, 95)]
       >>> ivm [100]
       65
       >>> ivm [499]
       65
       >>> ivm [500]
       75
       >>> ivm [1600]
       95
       >>> ivm [160000]
       95
       >>> ivm [2**31]
       95
       >>> ivm [-2**31]
       65
    """

    def __init__ (self, * iv_list) :
        self.iv_map = TFL.sorted (iv_list)
    # end def __init__

    def __getitem__ (self, key) :
        for i, result in self.iv_map :
            if key < i :
                break
        return result
    # end def __getitem__

    def __str__ (self) :
        return str (self.iv_map)
    # end def __str__

    def __repr__ (self) :
        return repr (self.iv_map)
    # end def __repr__

# end class Ival_Map

if __name__ != "__main__" :
    TFL._Export ("*")
### __END__ Ival_Map
