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
#    TGL.TKT.Application
#
# Purpose
#    Generic application framework root
#
# Revision Dates
#    12-Aug-2005 (MG) Creation
#    ««revision-date»»···
#--
#

from   _TGL               import TGL
import _TGL._TKT
import _TGL._TKT.Mixin

class _Application_ (TGL.TKT.Mixin) :

    cmd                   = property (lambda s : s.model.cmd)
    verbose               = property (lambda s : s.model.verbose)

    def __init__ (self, model, ** kw) :
        self.__super.__init__ (model.AC, ** kw)
        self.message               = model.AC.ui_state.message = None
        self.gauge                 = model.AC.ui_state.gauge   = None
        self.State                 = model.AC.memory
        self.model                 = model
        self.queued_stdout         = None
    # end def __init__

    def echo (self, * msg, ** kw) :
        verbose = kw.get ("verbose", self.default_verbosity)
        if self.verbose >= verbose :
            for m in msg :
                print m,
            if msg :
                print
    # end def echo

    def _destroy (self) :
        if self.queued_stdout :
            self.queued_stdout.destroy ()
    # end def _destroy

    def _kill_interact (self, event = None) :
        model = self.model
        if model.ipreter :
            model.ipreter.destroy ()
            model.ipreter = None
    # end def _kill_interact

    def _setup_clipboard (self) : ### XXX ???
        self.clipboard = self.AC.ui_state.clipboard = self.ANS.UI.Clipboard \
            (AC = self.AC)
    # end def _setup_clipboard

    def _setup_context_menu (self) :
        pass
    # end def _setup_context_menu

    def _setup_stdout_redirect (self) :
        self.queued_stdout = self.TNS.Queued_Stdout \
            (self.message, redirect_stderr = True)
    # end def _setup_stdout_redirect

    def _write_bug_info (self, file) :
        if self.message :
            sep   = "\n" + ("-" * 79) + "\n"
            write = file.write
            write (sep)
            write ("Contents of message window")
            write (sep)
            write (self.message.get ())
            write ("\n")
    # end def _write_bug_info

Application = _Application_

if __name__ != "__main__" :
    TGL.TKT._Export ("Application")
### __END__ TGL.TKT.Application
