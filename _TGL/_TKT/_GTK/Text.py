# -*- coding: iso-8859-1 -*-
# Copyright (C) 2005 Martin Gl�ck. All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. office@spannberg.com
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
#    TGL.TKT.GTK.Text
#
# Purpose
#    Text view widget used by UI.HTB und UI.HTD
#
# Revision Dates
#     2-Apr-2005 (MG) Creation
#    ��revision-date�����
#--

from   _TGL                     import TGL
import _TGL._TKT._GTK.Text_View
import _TGL._TKT._GTK.Text_Buffer
import  pango

GTK = TGL.TKT.GTK

class _GTK_Text_ (GTK.Text_View) :
    """Text view widget used by UI.HTB und UI.HTD"""

    _real_name = "Text"

    def see (self, pos_or_mark) :
        """Adjust view of `self` so that `pos_or_mark` is completely visible.
        """
        iter = self._buffer._iter_from_pom           (pos_or_mark)
        mark = self._buffer.wtk_object.create_mark   (None, iter)
        self.wtk_object.scroll_mark_onscreen         (mark)
        self._buffer.free_mark                       (mark)
    # end def see

    def set_tabs (self, * tabs) :
        length    = len (tabs)
        tab_array = pango.TabArray (len (tabs), True)
        for pos, tab in enumerate (tabs) :
            tab_array.set_tab (pos, pango.TAB_LEFT, tab)
        self.tabs = tab_array
    # end def set_tabs

    #### we must override tis function because we don't want the
    #### `apply_style` Function from the `Text_View` widget
    def apply_style (self, * args, ** kw) :
        return self._buffer.apply_style (* args, ** kw)
    # end def apply_style

    def __getattr__ (self, name) :
        if not name.startswith ("__") :
            return getattr (self._buffer, name)
        raise AttributeError, name
    # end def __getattr__

Text = _GTK_Text_ # end class _GTK_Text_

import _TGL._TKT.Text

def _doctest_AC () :
    ### Restricted to doctest use, only
    import _TGL._UI
    import _TGL._UI.App_Context
    return TGL.UI.App_Context (TGL)
# end def _doctest_AC

__test__ = dict (interface_test = TGL.TKT.Text._interface_test)

"""
from _TGL._TKT._GTK.Text import *
from _TGL._TKT._GTK.Text import _doctest_AC
from _TGL._UI.Style     import *
blue  = Style ("blue", background = "lightblue")
yell  = Style ("yell", background = "yellow", foreground = "red")
gray  = Style ("gray", background = "gray80")
hand  = Style ("hand", mouse_cursor = "hand")
defa  = Style ("hand", mouse_cursor = "default")
fleur = Style ("hand", mouse_cursor = "fleur")
w = Text (_doctest_AC ())
eot = w.eot_pos
cur = w.current_pos
w.push_style  (hand)
w.bot_pos, w.pos_at (eot), w.pos_at (cur), w.bol_pos (w.current_pos)
w.append ("Ha")
w.bot_pos, w.pos_at (eot), w.pos_at (cur), w.bol_pos (w.current_pos)
w.append ("Hum", blue)
w.insert (w.bot_pos, "Hi", yell)
w.insert (w.bot_pos, "Ho", delta = 2)
w.apply_style  (gray, w.bol_pos (w.current_pos), w.eol_pos (w.current_pos))
w.remove_style (gray, w.bot_pos, w.eot_pos)
for t in "Ha", "He", "Hi", "Ho", "Hu" :
    print t, w.find (t)

w.bot_pos, w.pos_at (eot), w.pos_at (cur), w.bol_pos (w.current_pos)
w.insert (w.eot_pos, '''\nDiddle Dum''')
w.apply_style (gray, w.bol_pos (w.current_pos), w.eol_pos (w.current_pos))
#w.remove_style (yell, w.bot_pos, w.eot_pos)
w.bot_pos, w.pos_at (eot), w.pos_at (cur), w.bol_pos (w.current_pos)
w.get ()
w.remove  (w.find ("Diddle"), delta = len ("Diddle"))
w.get ()

from _TGL._TKT._GTK.Test_Window import *
win = Test_Window ()
win.add           (w)
win.show_all      ()
GTK.main          ()
"""

if __name__ != "__main__" :
    GTK._Export ("Text")
### __END__ TGL.TKT.GTK.Text


