# -*- coding: utf-8 -*-
# Copyright (C) 2012-2014 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package GTW.Werkzeug.
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
#    GTW.Werkzeug.Response
#
# Purpose
#    Extend werkzeug's Response class
#
# Revision Dates
#    20-Jun-2012 (CT) Creation
#     2-Mar-2013 (CT) Add `add_header` and `set_header` (both encode `key`)
#    14-Mar-2014 (CT) Add `encoded_url`
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division, print_function, unicode_literals

from   _GTW                       import GTW
from   _TFL                       import TFL

import _GTW._Werkzeug

from   _TFL._Meta.Once_Property   import Once_Property

import _TFL._Meta.M_Class

from   werkzeug.wrappers             import Response
from   werkzeug.contrib.wrappers     import DynamicCharsetResponseMixin
from   werkzeug.urls                 import Href

class _WZG_Response_ (DynamicCharsetResponseMixin, Response) :
    """Extend werkzeug's Response class."""

    __metaclass__        = TFL.Meta.M_Class
    _real_name           = "Response"

    default_charset      = "utf-8"

    def add_header (self, key, value, ** kw) :
        if isinstance (key, unicode) :
            key = key.encode ("ascii")
        return self.headers.add (key, value, ** kw)
    # end def add_header

    def clear (self) :
        self.headers.clear ()
        self.response = []
        self.status   = self.default_status
    # end def clear

    def encoded_url (self, * args, ** kw) :
        if args :
            result = Href (args [0])
            return result (* args [1:], ** kw)
        else :
            result = Href ()
            return result (** kw) [2:]
    # end def encoded_url

    def write (self, data) :
        self.response.append (data)
    # end def write

    def set_header (self, key, value, ** kw) :
        if isinstance (key, unicode) :
            key = key.encode ("ascii")
        return self.headers.set (key, value, ** kw)
    # end def set_header

    def write_json (self, __data = None, ** kw) :
        data = dict (kw)
        if __data is not None :
            data.update (__data)
        self.set_header ("Content-Type", "text/javascript; charset=UTF-8")
        self.write      (json.dumps (data))
    # end def write_json

Response = _WZG_Response_ # end class

if __name__ != "__main__" :
    GTW.Werkzeug._Export ("Response")
### __END__ GTW.Werkzeug.Response
