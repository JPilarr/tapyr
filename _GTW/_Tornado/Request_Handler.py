# -*- coding: iso-8859-1 -*-
# Copyright (C) 2007-2010 Martin Gl�ck. All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. martin@mangari.org
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
#    Tornado.Request_Handler
#
# Purpose
#    �text����
#
# Revision Dates
#    12-Sep-2009 (MG) Creation
#    ��revision-date�����
#--

from   _TFL                import TFL
import _TFL._Meta.Object

from    tornado            import web

class Request_Handler (web.RequestHandler) :
    """Base class for a request handler"""
# end class Request_Handler

if __name__ != "__main__" :
    from _GTW._Tornado import Tornado
    Tornado._Export ("*")
### __END__ Tornado.Request_Handler
