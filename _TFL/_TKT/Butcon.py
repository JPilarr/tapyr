# -*- coding: iso-8859-15 -*-
# Copyright (C) 2005-2013 Mag. Christian Tanzer. All rights reserved
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
#    TFL.TKT.Butcon
#
# Purpose
#    Model simple Button Control widget
#
# Revision Dates
#    17-Feb-2005 (RSC) Creation
#    25-Feb-2005 (ABR) Fixed doctest (uses png's instead of xbm's)
#    25-Feb-2005 (RSC) Re-added bitmaps that fail TGW doctest
#    25-Feb-2005 (RSC) Removed bitmaps for which no xbm exists -- Tk
#                      can't read PNG. Now left one xbm to document
#                      failing doctest of TGW.
#    25-Feb-2005 (RSC) Added style-related doctests
#    23-May-2013 (CT)  Fix bitmap-names in tests
#    28-May-2013 (CT) Use `@subclass_responsibility` instead of home-grown code
#    ��revision-date�����
#--

from   _TFL                 import TFL
from   _TFL.Decorator       import subclass_responsibility

import _TFL._TKT.Mixin

class Butcon (TFL.TKT.Mixin) :
    """Model simple Button Control widget."""

    _interface_test   = """
        >>> from _TFL._UI.Style import *
        >>> w = Butcon ()
        >>> w.apply_bitmap ('node_open')
        >>> w.apply_bitmap ('node_closed')
        >>> blue = Style ("blue", background = "lightblue")
        >>> w.apply_style (blue)
        >>> w.push_style  (blue)
        >>> w.pop_style   ()
        >>> w.pop_style   ()
        Traceback (most recent call last):
        ...
        IndexError: pop from empty list
    """

    @subclass_responsibility
    def apply_bitmap (self, bitmap) :
        """Apply `bitmap` to our widget, replacing existing bitmap."""
    # end def apply_bitmap

    @subclass_responsibility
    def apply_style (self, style) :
        """Apply `style` to our widget."""
    # end def apply_style

    @subclass_responsibility
    def remove_style (self, style) :
        """Remove `style` from our widget."""
    # end def apply_style

# end class Butcon

if __name__ != "__main__" :
    TFL.TKT._Export ("*")
### __END__ TFL.TKT.Tk.Text
