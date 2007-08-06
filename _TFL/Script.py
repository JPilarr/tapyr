# -*- coding: iso-8859-1 -*-
# Copyright (C) 2000-2006 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
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
#    TFL.Script
#
# Purpose
#    Model python script to be run from an application
#
# Revision Dates
#     8-Aug-2000 (CT)  Creation (factored from Script_Menu_Mgr)
#     8-Aug-2000 (CT)  `Script.__call__' changes sys.path temporarily to
#                      include the script's path
#     8-Aug-2000 (CT)  `add_to_python_path' and `reset_python_path' added
#    14-Sep-2000 (CT)  `error' added
#    22-Feb-2001 (CT)  Use `raise' instead of `raise exc' for re-raise
#     1-Jul-2002 (CT)  `__call__` changed to hide the mdodules `__builtin__`
#                      and `sys` from scripts
#     3-Jul-2002 (CT)  Change of 1-Jul revoked
#    29-Jan-2004 (CT)  `gauge` and `echo`-calls added
#    14-Jun-2004 (GWA) `\n` added to `gauge.echo` calls
#    14-Feb-2006 (CT)  Moved into package `TFL`
#     9-Aug-2006 (CT) `Script.__hash__` changed to return
#                     `hash (self.name)` instead of `id (self)`
#    23-Jul-2007 (CED) Activated absolute_import
#    06-Aug-2007 (CED) Future import removed again
#    ��revision-date�����
#--



from   _TFL              import TFL
from   _TFL.Filename     import *
from   _TFL.Functor      import Functor
from   _TFL.Gauge_Logger import Gauge_Logger
from   _TFL              import sos

import sys
import traceback

class Script :

    def __init__ (self, path, glob_dict = {}, local_dict = {}, name = None, doc = "") :
        fn             = Filename (path, absolute = 1)
        self.path      = fn.name
        self.name      = name or fn.base
        self.dir       = fn.directory
        self.gd        = glob_dict
        self.ld        = local_dict
        self.gauge     = local_dict.get ("gauge")
        if not self.gauge :
            self.gauge = Gauge_Logger ()
        self.old_path  = []
        self._sys_pth  = sys.path [:]
        self.__doc__   = \
            (  doc.replace ("script-name", self.name)
            or ("Run script `%s'" % self.name)
            )
        self.error     = None
    # end def __init__

    def __call__ (self, ld = {}) :
        self.error = None
        gd = self.gd.copy ()
        gd.update         (self.ld)
        gd.update         (ld)
        gd.update \
            ({ "add_to_python_path" : self.add_to_python_path
             , "reset_python_path"  : self.reset_python_path
             }
            )
        try :
            self.old_path = sys.path [:]
            try     :
                sys.path  [0:0] = [self.dir]
                self.gauge.echo   ("Running script %s\n" % self.path)
                execfile          (self.path, gd)
                self.gauge.echo   ("Finished execution of %s\n" % self.path)
            finally :
                sys.path  = self.old_path
        except KeyboardInterrupt, exc :
            raise
        except StandardError :
            print "Error during execution of", self.path
            traceback.print_exc ()
            self.error = sys.exc_info () [1]
    # end def __call__

    def add_to_python_path (self, path, index = -1) :
        """Add `path' to `sys.path'"""
        sys.path      [index+1 : index+1] = [path]
        self.old_path [index   : index] = [path]
    # end def add_to_python_path

    def reset_python_path (self) :
        """Reset `sys.path' to original value."""
        self.old_path = self._sys_pth [:]
        sys.path      = self._sys_pth [:]
    # end def reset_python_path

    def __cmp__ (self, other) :
        return cmp (self.name, other.name)
    # end def __cmp__

    def __hash__ (self) :
        return hash (self.name)
    # end def __hash__

# end class Script

if __name__ != "__main__" :
    TFL._Export ("*")
### __END__ TFL.Script
