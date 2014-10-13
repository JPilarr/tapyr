# -*- coding: utf-8 -*-
# Copyright (C) 2005-2007 Martin Glück. All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. office@spannberg.com
# ****************************************************************************
#
# This module is licensed under the terms of the BSD 3-Clause License
# <http://www.c-tanzer.at/license/bsd_3c.html>.
# ****************************************************************************
#
#++
# Name
#    TGL.TKT.GTK.Butcon
#
# Purpose
#    Model simple Button Control widget
#
# Revision Dates
#     3-Apr-2005 (MG) Creation
#     5-Apr-2005 (MG) Use `png` instead of `xbm` images
#     5-Apr-2005 (MG) Adapted to the changes of the `Image_Manager`
#    14-Dec-2007 (MG) Import fixed
#    ««revision-date»»···
#--

from   _TFL.predicate           import dict_from_list
from   _TGL                     import TGL
import _TGL._TKT
import _TGL._TKT._GTK.Event_Box ### do we realy need the event box????
import _TGL._TKT._GTK.Image_Manager
import _TGL._TKT._GTK.Image
import _TGL._TKT._GTK.Styler
import _TGL._TKT.Butcon

GTK = TGL.TKT.GTK

class _GTK_Butcon_ (GTK.Event_Box, TGL.TKT.Butcon) :
    """Model simple Button Control widget

       >>> from _TFL._UI.Style     import *
       >>> blue = Style ("blue", background = "lightblue")
       >>> yell = Style ("yell", background = "yellow", foreground = "red")
       >>> gray = Style ("gray", background = "gray80")
       >>> w = Butcon ()
       >>> w.apply_bitmap ('open_node')
       >>> w.apply_style (yell)
       >>> w.apply_bitmap ('closed_node')
       >>> w.apply_bitmap ('circle')
       >>> w.apply_style (gray)
    """

    class Styler (TGL.TKT.GTK.Styler) :
        Opts = dict_from_list (("foreground", "background"))
    # end class Styler

    _real_name = "Butcon"

    def __init__ (self, name = None, wc = None, bitmap = None, ** kw) :
        self.__super.__init__ (name = name, ** kw)
        # XXXX FIXME: bitmap_mgr add and caching of seen bitmaps should
        # probably be done by framework
        self.bitmaps = {}
        self._image  = GTK.Image ()
        self.add                 (self._image)
        self.apply_bitmap        (bitmap)
    # end def __init__

    # XXXX FIXME: bitmap_mgr add and caching of seen bitmaps should
    # probably be done by framework
    def _get_bitmap (self, bitmap) :
        if bitmap :
            if not self.bitmaps.has_key (bitmap) :
                GTK.image_mgr.add (bitmap + '.png')
                self.bitmaps [bitmap] = 1
            return GTK.image_mgr [bitmap]
        return None
    # end def _get_bitmap

    def apply_bitmap (self, bitmap) :
        self._image.pixbuf = self._get_bitmap (bitmap)
    # end def apply_bitmap

Butcon = _GTK_Butcon_ # end class _GTK_Butcon_

#__test__ = dict (interface_test = TGL.TKT.Butcon._interface_test)

"""
from _TGL._TKT._GTK.Butcon      import *
from _TGL._TKT._GTK.Test_Window import *
from _TGL._UI.Style             import *
blue = Style ("blue", background = "lightblue")
yell = Style ("yell", background = "yellow", foreground = "red")
gray = Style ("gray", background = "gray80")
w = Butcon ()
w.apply_bitmap ('open_node')
w.apply_style (yell)
w.apply_bitmap ('closed_node')
w.apply_bitmap ('circle')

win = GTK.Test_Window ()
win.add               (w)
win.show_all          ()
GTK.main              ()
"""

if __name__ != "__main__" :
    GTK._Export ("Butcon")
### __END__ TGL.TKT.GTK.Butcon
