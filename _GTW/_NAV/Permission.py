# -*- coding: utf-8 -*-
# Copyright (C) 2009-2012 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
# This module is part of the package GTW.NAV.
#
# This module is licensed under the terms of the BSD 3-Clause License
# <http://www.c-tanzer.at/license/bsd_3c.html>.
# ****************************************************************************
#
#++
# Name
#    GTW.NAV.Permission
#
# Purpose
#    Classes modelling permissions for accessing Navigation objects
#
# Revision Dates
#    16-Jan-2010 (CT) Creation
#    18-Jan-2010 (CT) `In_Page_Group` removed
#    26-Feb-2010 (CT) `Is_Superuser` added
#     8-Jun-2012 (CT) Add `Login_Required`, add guards for `user`
#    11-Jun-2012 (CT) Add `rank`
#    20-Jun-2012 (CT) Remove dependency on `GTW.NAV.Root.top`
#    ««revision-date»»···
#--

from   _TFL                     import TFL
from   _GTW                     import GTW

import _GTW._NAV

from   _TFL._Meta.Once_Property import Once_Property

import _TFL.Filter

class _Permission_ (TFL._.Filter._Filter_S_) :

    rank = 0

# end class _Permission_

class In_Group (_Permission_) :
    """Permission if user is member of group"""

    def __init__ (self, name) :
        self.name = name
    # end def __init__

    def group (self, page) :
        scope = page.top.scope
        Group = scope ["Auth.Group"]
        return Group.instance (self.name)
    # end def group

    def predicate (self, user, page, * args, ** kw) :
        if user :
            group = self.group (page)
            return group in user.groups
    # end def predicate

# end class In_Group

class Is_Creator (_Permission_) :

    def __init__ (self, attr_name = "creator") :
        self.attr_name = attr_name
    # end def __init__

    def predicate (self, user, page, * args, ** kw) :
        return user and user == getattr (page.obj, self.attr_name, None)
    # end def predicate

# end class Is_Creator

class Is_Superuser (_Permission_) :

    def predicate (self, user, page, * args, ** kw) :
        return user and user.superuser
    # end def predicate

# end class Is_Superuser

class Login_Required (_Permission_) :

    rank = -100

    def predicate (self, user, page, * args, ** kw) :
        return user and user.authenticated and user.active
    # end def predicate

# end class Login_Required

if __name__ != "__main__":
    GTW.NAV._Export ("*")
### __END__ GTW.NAV.Permission
