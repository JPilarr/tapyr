# -*- coding: utf-8 -*-
# Copyright (C) 2012-2013 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package GTW.RST.TOP.
# 
# This module is licensed under the terms of the BSD 3-Clause License
# <http://www.c-tanzer.at/license/bsd_3c.html>.
# #*** </License> ***********************************************************#
#
#++
# Name
#    GTW.RST.TOP.Response
#
# Purpose
#    Extend GTW.RST.Response with session handling
#
# Revision Dates
#    20-Jun-2012 (CT) Creation
#    23-Jul-2012 (CT) Add `username` to `_own_vars`
#     2-May-2013 (CT) Factor `clear_cookie`, `set_cookie`, and
#                     `set_secure_cookie` to `GTW.RST.Response`
#     9-Dec-2013 (CT) Adapt `_set_session_cookie` to signature change of
#                     `set_secure_cookie`
#     9-Dec-2013 (CT) Add `anti_csrf_token`
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division, print_function, unicode_literals

from   _GTW                     import GTW
from   _TFL                     import TFL

from   _TFL._Meta.Once_Property import Once_Property

import _GTW._RST._TOP
import _GTW._RST.Response
import _GTW._RST.Signed_Token

import base64
import time

class _RST_TOP_Response_ (GTW.RST.Response) :
    """Extend GTW.RST.Response with session handling."""

    _own_vars = ("username", )

    @Once_Property
    def anti_csrf_token (self) :
        return GTW.RST.Signed_Token.Anti_CSRF (self._request, "don't bug me")
    # end def anti_csrf_token

    @Once_Property
    def session (self) :
        return self._request.session
    # end def session

    @property
    def username (self) :
        return self.session.username
    # end def username

    @username.setter
    def username (self, value) :
        session = self.session
        if value != session.username :
            session.username = value
            self._set_session_cookie ()
    # end def username

    def add_notification (self, noti) :
        notifications = self.session.notifications
        if notifications is not None :
            if not isinstance (noti, GTW.Notification) :
                noti = GTW.Notification (noti)
            notifications.append (noti)
    # end def add_notification

    def _set_session_cookie (self) :
        request = self._request
        session = self.session
        name    = request.session_cookie_name
        value   = request.new_secure_cookie (session.sid)
        ttl     = self.resource.session_ttl
        cookie  = self.set_secure_cookie (name, value, max_age = ttl)
        GTW.Notification_Collection (session)
        return cookie
    # end def _set_session_cookie

Response = _RST_TOP_Response_ # end class

if __name__ != "__main__" :
    GTW.RST.TOP._Export ("Response")
### __END__ GTW.RST.TOP.Response
