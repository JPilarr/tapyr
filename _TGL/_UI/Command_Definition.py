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
#    TGL.UI.Command_Definition
#
# Purpose
#    Simple way of defining commands for a command manager
#
# Revision Dates
#    13-Aug-2005 (MG) Creation (factored from PMA.UI.Office)
#    14-Aug-2005 (MG) `Command_Definition_Mixin`: Handling of
#                     `command_bindings` added 
#     3-Sep-2005 (MG) `command_bindings` handling changed
#    ««revision-date»»···
#--

class Command_Definition (object) :

    precondition = None
    batchable    = True
    icon         = None
    eventname    = None
    accelerator  = None
    underline    = None

    class Group (object) :
        def __init__ (self, name, ci = (), ev = ()) :
            self.name = name
            if not isinstance (ci, (list, tuple)) :
                ci = (ci, )
            if not isinstance (ev, (list, tuple)) :
                ev = (ev, )
            self.ci = ci
            self.ev = ev
        # end def __init__

        def command_interfacers (self, eventname = None) :
            if not eventname :
                return self.ci
            return self.ci + tuple ("%s:%s" % (ev, eventname) for ev in self.ev)
        # end def command_interfacers

    # end class Group

    def __init__ (self, name, callback, * group_spec, ** kw) :
        self.name         = name
        self.callback     = callback
        self.group_spec   = group_spec
        self.__dict__.update (kw)
    # end def __init__

    def __call__ (self, Cmd, cmd_mgr, obj = None) :
        callback = self.callback
        if not callable (callback) :
            callback = getattr (obj, callback)
        cmd_dict = dict \
            ( precondition = self.precondition
            , batchable    = self.batchable
            )
        for group in self.group_spec :
            acc = self.accelerator
            #if acc is not None :
            #    acc = getattr (obj.TNS.Eventname, acc)
            getattr (cmd_mgr.cmd, group.name).add_command \
                ( Cmd (self.name, callback, ** cmd_dict)
                , accelerator = acc
                , icon        = self.icon
                , if_names    = group.command_interfacers (self.eventname)
                , underline   = self.underline
                )
    # end def __call__

# end class Command_Definition

class Separator (object) :

    def __init__ (self, * group_spec) :
        self.group_spec = group_spec
    # end def __init__


    def __call__ (self, Cmd, cmd_mgr, obj = None) :
        for group in self.group_spec :
            getattr (cmd_mgr.cmd, group.name).add_separator \
                (if_names = group.command_interfacers ())
    # end def __call__

# end class Separator

class Command_Definition_Mixin (object) :
    """Mixin for handling the command definition."""

    command_bindings = {}
    commands         = ()
    deaf_commands    = ()
    
    def _setup_commands (self, cmd_mgr) :
        Cmd     = self.ANS.UI.Command
        Def_Cmd = self.ANS.UI.Deaf_Command
        for cmd in self.deaf_commands :
            cmd (Def_Cmd, cmd_mgr, self)
        for cd in self.commands :
            cd (Cmd, cmd_mgr, self)
        for widgets_attr_name, bindings in self.command_bindings.iteritems () :
            widgets = getattr (self, widgets_attr_name)
            if not isinstance (widgets, (list, tuple)) :
                widgets = (widgets, )
            for w in widgets :
                if "context_menu" in bindings :
                    i = self._interfacer (cmd_mgr, bindings ["context_menu"])
                    i.bind_to_widget     (w, "click_3")
                if "event_binder" in bindings :
                    i = self._interfacer (cmd_mgr, bindings ["event_binder"])
                    i.add_widget         (w)
    # end def _setup_commands

    def _interfacer (self, cmd_mgr, interfacer_name) :
        group, name = interfacer_name.split (".", 1)
        return cmd_mgr [group].interfacers [name]
    # end def _interfacer
    
# end class Command_Definition_Mixin

if __name__ != "__main__" :
    from   _TGL      import TGL
    import _TGL._UI
    TGL.UI._Export ("*")
### __END__ TGL.UI.Command_Definition
