# -*- coding: iso-8859-1 -*-
# Copyright (C) 2005 Mag. Christian Tanzer. All rights reserved
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
#    TFL.TKT.Mixin
#
# Purpose
#    Mixin for TFL.TKT classes
#
# Revision Dates
#    18-Jan-2005 (CT) Creation
#    ��revision-date�����
#--

from   _TFL           import TFL
import _TFL._Meta.Object
import _TFL._TKT

class Mixin (TFL.Meta.Object) :
    """Mixin for TFL.TKT classes

       This mixin supplies two symbolic names for package name spaces:
       - ANS specifies the application specific PNS
       - TNS specifies the toolkit specific PNS

       Descendents should always use these attributes to refer to classes
       instead of using literal names for the package name spaces.
    """

    ANS      = TFL
    TNS_name = None

    def __init__ (self, AC = None, ** kw) :
        if AC is not None :
            self.ANS = AC.ANS
            if self.TNS_name is not None :
                tns = AC.ANS
                for p in ["TKT"] + self.TNS_name.split (".") :
                    tns = getattr (tns, p)
                self.TNS = tns
        self.__super.__init__ (AC = AC, ** kw)
    # end def __init__

# end class Mixin

if __name__ != "__main__" :
    TFL.TKT._Export ("*")
### __END__ TFL.TKT.Mixin
