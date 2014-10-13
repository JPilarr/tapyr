# -*- coding: utf-8 -*-
# Copyright (C) 2010-2014 Martin Glueck All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. martin@mangari.org
# ****************************************************************************
# This module is part of the package GTW.
#
# This module is licensed under the terms of the BSD 3-Clause License
# <http://www.c-tanzer.at/license/bsd_3c.html>.
# ****************************************************************************
#
#++
# Name
#    GTW.Notification
#
# Purpose
#    A framework for user notification in a web application
#
# Revision Dates
#    20-Feb-2010 (MG) Creation
#    17-Aug-2012 (MG) Add new `Cached` property and adapt pickle behavior
#    18-Aug-2012 (MG) Fix `discarge` to avoid `empty` head/tail result
#    ««revision-date»»···
#--
"""
Short test for the notification framework
    >>> from _GTW.File_Session import File_Session
    >>> time1   = datetime.datetime (2010, 2, 20, 11, 42, 00)
    >>> time2   = datetime.datetime (2010, 2, 20, 11, 42, 42)
    >>> session = File_Session ()
    >>> sid     = session.sid

    >>> nc = Notification_Collection (session)
    >>> nc.append (Notification ("Password reset mail has been sent", time2))
    >>> nc.append (Notification ("User has been logged out",          time1))
    >>> nc
    [Notification ('Password reset mail has been sent', datetime.datetime(2010, 2, 20, 11, 42, 42)), Notification ('User has been logged out', datetime.datetime(2010, 2, 20, 11, 42))]
    >>> session.save                 ()

    >>> session2 = File_Session (sid)
    >>> session != session2
    True
    >>> session2.notifications
    [Notification ('Password reset mail has been sent', datetime.datetime(2010, 2, 20, 11, 42, 42)), Notification ('User has been logged out', datetime.datetime(2010, 2, 20, 11, 42))]
    >>> print (session2.notifications.discarge ())
    User has been logged out
    Password reset mail has been sent
    >>> print (session2.notifications.discarge ())
    <BLANKLINE>
    >>> session.remove ()
"""

from   __future__          import print_function

from   _GTW                import GTW
from   _TFL                import TFL
from   _TFL.pyk            import pyk

import _TFL._Meta.Object

import  datetime

class M_Notification_Collection (TFL.Meta.Object.__class__) :
    """Meta class implementing a singleton pattern"""

    session_key = "notifications"

    def __call__ (cls, session, * args) :
        if cls.session_key not in session :
            session [cls.session_key] = super \
                (M_Notification_Collection, cls).__call__ (* args)
        return session [cls.session_key]
    # end def __call__

# end class M_Notification_Collection

class Notification_Collection \
          ( TFL.Meta.BaM
              (TFL.Meta.Object, metaclass = M_Notification_Collection)
          ) :
    """Collection of all notifications for a session."""

    def __init__ (self) :
        self._notifications = []
    # end def __init__

    def append (self, arg) :
        self._notifications.append (arg)
    # end def append

    def __iter__ (self) :
        return iter (self._notifications)
    # end def __iter__

    def __getstate__ (self) :
        self.__dict__.pop ("Cached", ())
        return self.__dict__
    # end def __getstate__

    @TFL.Meta.Once_Property
    def Cached (self) :
        return tuple (self)
    # end def Cached

    def discarge (self, head = "", joiner = "\n", tail = "") :
        self.Cached = items = tuple (self._notifications)
        result      = []
        if items :
            result.append (head)
            result.append \
                ( joiner.join
                    (  pyk.text_type (s)
                    for s in sorted (items, key = lambda n : n.time)
                    )
                )
            result.append (tail)
            self._notifications = []
        return "".join (result)
    # end def discarge

# end class Notification_Collection

@pyk.adapt__str__
class Notification (TFL.Meta.Object) :
    """A notification based on plain text."""

    def __init__ (self, message, time = None) :
        self.message = message
        self.time    = time or datetime.datetime.now ()
    # end def __init__

    def __str__ (self) :
        return self.message
    # end def __str__

    def __repr__ (self) :
        return pyk.reprify \
            ("%s (%r, %r)" % (self.__class__.__name__, self.message, self.time))
    # end def __repr__

# end class Notification

if __name__ != "__main__" :
    GTW._Export ("*")
### __END__ GTW.Notification
