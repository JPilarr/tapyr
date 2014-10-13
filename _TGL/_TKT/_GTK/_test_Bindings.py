# -*- coding: utf-8 -*-
# Copyright (C) 2005 Martin Glück. All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. office@spannberg.com
# ****************************************************************************
#
# This module is licensed under the terms of the BSD 3-Clause License
# <http://www.c-tanzer.at/license/bsd_3c.html>.
# ****************************************************************************
#
#++
# Name
#    TGL.TKT.GTK._test_Bindings
#
# Purpose
#    Simple test of the event-binding
#
# Revision Dates
#    31-Mar-2005 (MG) Creation
#    ««revision-date»»···
#--

from   _TGL._TKT._GTK         import GTK
import _TGL._TKT._GTK.Eventname
import _TGL._TKT._GTK.Test_Window
import _TGL._TKT._GTK.Button
import _TGL._TKT._GTK.V_Box

w  = GTK.Test_Window ("Binding Rest")
bo = GTK.V_Box       ()
b1 = GTK.Button      (label = "Button 1")
b2 = GTK.Button      (label = "Button 2")
bo.add               (b1)
bo.add               (b2)
w .add               (bo)
w.show_all           ()

def cb (event, * args) :
    print event.widget, args
# end def cb

b1.bind_add          (GTK.Eventname.click_1,        cb, "sc1")
b1.bind_add          (GTK.Eventname.triple_click_3, cb, "tc1")
b2.bind_add          (GTK.Eventname.click_3,        cb, "sc3")
b2.bind_add          (GTK.Eventname.double_click_2, cb, "dc2")
b2.bind_add          (GTK.Eventname.cursor_home,    cb, "home")
GTK.main             ()
### __END__ TGL.TKT.GTK._test_Bindings


