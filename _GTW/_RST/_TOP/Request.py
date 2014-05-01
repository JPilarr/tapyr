# -*- coding: utf-8 -*-
# Copyright (C) 2012-2014 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package GTW.RST.TOP.
#
# This module is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this module. If not, see <http://www.gnu.org/licenses/>.
# #*** </License> ***********************************************************#
#
#++
# Name
#    GTW.RST.TOP.Request
#
# Purpose
#    Extend GTW.RST.Request with session handling
#
# Revision Dates
#    20-Jun-2012 (CT) Creation
#    16-Jul-2012 (CT) Pass `bytes ("~@")` to `b64decode`
#    24-Jul-2012 (CT) Fix `locale_codes`
#    24-Jul-2012 (CT) Add `use_language`
#     4-Aug-2012 (MG) Don't save session on language change
#     4-Aug-2012 (MG) Allow setting of `username`
#    16-Jan-2013 (CT) Consider `ssl_authorized_user` in `username` methods
#     2-May-2013 (CT) Factor `cookie_encoding`, `cookie`, `secure_cookie`,
#                     `_cookie_signature`, to `GTW.RST.Request`
#     4-May-2013 (CT) Change `username` to use `__super.username`
#     4-May-2013 (CT) Redefine `apache_authorized_user` to disable it
#    26-Nov-2013 (CT) Take `user_locale_codes` from cookie `language`,
#                     not from session; remove `use_language`
#     9-Dec-2013 (CT) Add `allow_login`, `csrf_safe`
#    11-Dec-2013 (CT) Factor `csrf_token`
#    11-Feb-2014 (CT) Remove `username.setter` (redundant to `Response...`)
#    29-Apr-2014 (CT) Add `getattr_safe` to property `username`
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division, print_function, unicode_literals

from   _GTW                     import GTW
from   _TFL                     import TFL

from   _TFL.Decorator           import getattr_safe
from   _TFL._Meta.Once_Property import Once_Property

import _GTW.File_Session
import _GTW._RST._TOP
import _GTW._RST.Request

class _RST_TOP_Request_ (GTW.RST.Request) :
    """Extend GTW.RST.Request with session handling."""

    _real_name        = "Request"

    @Once_Property
    def allow_login (self) :
        resource = self._resource
        return resource.login_url and \
            (resource.TEST or resource.s_domain or self.is_secure)
    # end def allow_login

    @Once_Property
    def apache_authorized_user (self) :
        ### Don't want to support this in TOP context
        pass
    # end def apache_authorized_user

    @Once_Property
    def csrf_safe (self) :
        return self.same_origin and self.csrf_token
    # end def csrf_safe

    @Once_Property
    def csrf_token (self) :
        value = self.req_data.get ("F_ACT", "")
        csrf_token = GTW.RST.Signed_Token.Anti_CSRF.recover (self, value)
        return csrf_token
    # end def csrf_token

    @Once_Property
    def locale_codes (self) :
        """The locale-code for the current session."""
        codes = self.get_user_locale_codes ()
        if not codes :
            codes = self.__super.locale_codes
        return codes
    # end def locale_codes

    @Once_Property
    def session (self) :
        cookie_name = self.session_cookie_name
        S_Class     = self.settings.get  ("Session_Class", GTW.File_Session)
        sid         = self.secure_cookie (cookie_name)
        session     = S_Class (sid, self.settings, self._session_hasher)
        return session
    # end def session

    @Once_Property
    def session_cookie_name (self) :
        return self.settings.get ("session_id",  "SESSION_ID")
    # end def session_cookie_name

    @property
    @getattr_safe
    def username (self) :
        result = self.__super._auth_user_name
        if result is None :
            ### `session.username` can change (due to login/logout)
            ### cannot cache by defining as `Once_Property`
            result = self.session.username
        return result
    # end def username

    def get_user_locale_codes (self) :
        cookie = self.cookie ("language")
        result = ()
        if cookie :
            languages  = getattr (self.root, "languages", set ())
            if cookie in languages :
                result = (cookie, )
        return result
    # end def get_user_locale_codes

    def _session_hash (self, sig) :
        root   = self.root
        hash   = root.hash_fct     (str (sig)).digest ()
        result = root.b64_encoded  (hash, altchars = "~@")
        return result
    # end def _session_hash

    def _session_hasher (self, username) :
        sig    = self._session_sig  (username)
        result = self._session_hash (sig)
        return result
    # end def _session_hash

    def _session_sig (self, user) :
        root  = self.root
        scope = root.scope
        if isinstance (user, basestring) :
            user = root._get_user (user)
        return \
            ( getattr (user, "password", user)
            , scope.db_meta_data.dbid
                  if scope is not None else self.settings ["cookie_salt"]
            )
    # end def _session_sig

Request = _RST_TOP_Request_ # end class

if __name__ != "__main__" :
    GTW.RST.TOP._Export ("Request")
### __END__ GTW.RST.TOP.Request
