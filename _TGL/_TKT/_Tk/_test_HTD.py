# -*- coding: utf-8 -*-
# Copyright (C) 2005 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
#
# This module is licensed under the terms of the BSD 3-Clause License
# <http://www.c-tanzer.at/license/bsd_3c.html>.
# ****************************************************************************
#
#++
# Name
#    TGL.TKT.Tk._test_HTD
#
# Purpose
#    Test TGL.UI.HTD used with Tk toolkit
#
# Revision Dates
#    31-Mar-2005 (CT) Creation
#    16-May-2005 (CT) Test for `Node_C` added to `t`
#    ««revision-date»»···
#--

import _TGL._TKT._Tk
import _TGL._TKT._Tk.Butcon
import _TGL._TKT._Tk.Eventname
import _TGL._TKT._Tk.Text

from _TGL._TKT._test_HTD import *

__test__ = dict (interface_test = HTD_interface_test)

from   _TGL._UI.HTD import *

def t () :
    from   _TFL._UI.App_Context import App_Context
    import _TGL._TKT._Tk
    import _TGL._TKT._Tk.Butcon
    import _TGL._TKT._Tk.Eventname
    import _TGL._TKT._Tk.Text

    def show (t) :
        x = t.get    ()
        y = x.rstrip ()
        print y
        print "%s characters with %s trailing whitespace" % \
              (len (x), len (x) - len (y))

    nl  = chr (10)
    ac  = App_Context (TGL)
    r   = Root (ac, nl.join (("R.line 1", "R.line 2")))
    s   = Root (ac)
    t   = r.tkt_text
    u   = s.tkt_text
    t.exposed_widget.pack (expand = "yes", fill = "both")
    u.exposed_widget.pack (expand = "yes", fill = "both")

    n1 = Node ( r
              , ( r.Style.T ("n1.line 1 ", "yellow")
                , nl, "n1 line 2"
                , Styled ("continued", r.Style.blue)
                ))

    n2 = Node_B  (r, nl.join (("n2 line 1", "n2 line 2")))
    n3 = Node_B2 ( r
                 , ( ["n3 closed line 1"]
                   , ["n3 open line 1", nl, "n3 open line 2"])
                 , r.Style.light_gray)
    k3 = Node_C  ( n3, s, "n3 closed line 1")
    n3.inc_state ()

    m1 = Node_B2 ( n3
                 , (["m1 closed line 1"], ["m1 open line 1\nm1 open line 2"]))
    l1 = Node_C  ( m1, k3, "m1 closed line 1")
    m2 = Node    ( n3, ("m2 line 1", nl, "m2 line 2"))
    n4 = Node_B2 ( r, ( ["n4 closed line 1"]
                      , ["n4 open line 1", nl, "n4 open line 2"])
                 , r.Style.light_blue)
    return t

if __name__ == "__main__" :
    t ().wtk_widget.mainloop ()
### __END__ TGL.TKT.Tk._test_HTD
