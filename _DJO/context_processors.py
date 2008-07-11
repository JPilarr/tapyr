# -*- coding: iso-8859-1 -*-
# Copyright (C) 2008 Mag. Christian Tanzer. All rights reserved
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
#    DJO.context_processors
#
# Purpose
#    Define context processors for Django
#
# Revision Dates
#    11-Jul-2008 (CT) Creation
#    ��revision-date�����
#--

from   _DJO            import DJO
from   _DJO.Navigation import Root

def navigation_root (request) :
    return dict (NAV = Root.top)
# end def navigation_root

if __name__ == "__main__" :
    DJO._Export_Module ()
### __END__ context_processors
