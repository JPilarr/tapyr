# -*- coding: iso-8859-15 -*-
# Copyright (C) 2010-2012 Martin Glueck All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. martin@mangari.org
# ****************************************************************************
# This module is part of the package GTW.Werkzeug.
#
# This module is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this module. If not, see <http://www.gnu.org/licenses/>.
# ****************************************************************************
#
#++
# Name
#    GTW.Werkzeug.Application
#
# Purpose
#    Basic application using the werkzeug WSGI utilities.
#
# Revision Dates
#    20-Mar-2010 (MG) Creation
#    24-Mar-2010 (CT) `__call__` changed to catch `GTW.Werkzeug.Status`
#                     instead of `Exception`
#    29-Apr-2010 (MG) Set `charset` of werkzeug reguest und response handlers
#     6-Mai-2010 (MG) Support for profiling added
#     6-May-2010 (MG) `url_charset` seperated from `charset` because `GET`
#                     parameters are by default `utf-8` encoded
#    25-Jun-2010 (MG) Changed to generate a common interface between Werkzeug
#                     and Tornado
#    25-Jun-2010 (CT) Bug fix (s/kw/hkw/ in `handlers` loop in `__init__`)
#    28-Jun-2010 (CT) `GTW._Application_` factored
#    29-Jun-2010 (CT) Import for all relevant modules of package added
#    11-Mar-2011 (CT) s/cookie_secret/cookie_salt/
#    11-Mar-2011 (CT) `edit_session_ttl` and `user_session_ttl` added to
#                     `default_settings`
#    21-Jun-2011 (MG) `reload_extra_files` added
#    17-Nov-2011 (MG) `run_development_server`: patch
#                     `werkzeug.serving.make_server` to run
#                     `GTW.NAV.Root.top.Run_on_Launch`
#     3-Jan-2012 (CT) Factor `Url_Handler`
#    ��revision-date�����
#--

from   _TFL               import TFL
from   _GTW               import GTW

import _GTW._Application_
import _GTW.File_Session
import _GTW.Static_File_Map

import _GTW._Werkzeug.Error
import _GTW._Werkzeug.Request_Data
import _GTW._Werkzeug.Request_Handler
import _GTW._Werkzeug.Static_File_Handler
import _GTW._Werkzeug.Upload_Handler
import _GTW._Werkzeug.Url_Handler

from    werkzeug          import ClosingIterator
from    werkzeug.wrappers import BaseRequest, BaseResponse

import  datetime
import  re
import  warnings

class _Werkzeug_Application_ (GTW._Application_) :
    """A WSGI Application"""

    default_settings = dict \
        ( Session_Class    = GTW.File_Session
        , cookie_salt      = "salt *MUST* be changed for every application"
        , edit_session_ttl = datetime.timedelta (hours =  6)
        , session_id       = "SESSION_ID"
        , user_session_ttl = datetime.timedelta (days  = 30)
        )

    _real_name = "Application"

    def __init__ (self, * handlers, ** kw) :
        if "cookie_salt" not in kw :
            warnings.warn \
                ( "Cookie salt should be specified for every application! "
                  "Using default `cookie_salt`!"
                , UserWarning
                )
        encoding                = kw.pop ("encoding", "utf-8")
        BaseRequest.charset     = BaseResponse.charset = encoding
        BaseRequest.url_charset = "utf-8"
        self.settings           = dict (self.default_settings, ** kw)
        self.handlers, self._server_opts = self._init_handlers (handlers, kw)
        self.__super.__init__ (** kw)
    # end def __init__

    def __call__ (self, environ, start_response) :
        path = environ ["PATH_INFO"]
        for uha in self.handlers :
            match = uha.pat.match (path)
            if match :
                return uha (environ, start_response, match)
    # end def __call__

    def run_development_server ( self
                               , port                 = 8080
                               , host                 = "localhost"
                               , use_profiler         = False
                               , profile_log_files    = ()
                               , profile_sort_by      = ('time', 'calls')
                               , profile_restrictions = ()
                               , profile_delete_logs  = False
                               , reload_extra_files   = None
                               ) :
        from werkzeug import run_simple
        from werkzeug import serving
        make_server = serving.make_server
        def _make_server (* msargs, ** mskw) :
            try :
                from _GTW._NAV.Base import Root
            except ImportError :
                pass
            else :
                while Root.top.Run_on_Launch :
                    fct, args = Root.top.Run_on_Launch.pop (0)
                    fct (args)
            return make_server (* msargs, ** mskw)
        # end def _make_server
        serving.make_server = _make_server
        app = self
        use_debugger = self._server_opts.get ("debug",       False)
        use_reloader = self._server_opts.get ("auto_reload", False)
        if use_profiler :
            from werkzeug.contrib.profiler import \
                ProfilerMiddleware, MergeStream
            import os, sys
            stream       = None
            file_handles = []
            for fn in profile_log_files :
                if hasattr (fn, "write") :
                    file_handles.append (fn)
                elif fn == "stderr" :
                    file_handles.append (sys.stderr)
                else :
                    if profile_delete_logs and os.path.isfile (fn) :
                        os.unlink (fn)
                    file_handles.append (open (fn, "w"))
            if file_handles :
                stream = MergeStream (* file_handles)
            app    = ProfilerMiddleware \
                (app, stream, profile_sort_by, profile_restrictions)
            use_reloader = use_debugger = False
        run_simple \
            ( host, port, app
            , use_reloader = use_reloader
            , use_debugger = use_debugger
            , extra_files  = reload_extra_files
            )
    # end def run_development_server

    def _handler_pattern (self, prefix) :
        return re.compile ("(%s)(/.*)$" % (prefix, ))
    # end def _handler_pattern

    def _init_handler (self, handler_spec) :
        return GTW.Werkzeug.Url_Handler \
            (self, * self.__super._init_handler (handler_spec))
    # end def _init_handler

    def _init_static_handler (self, handler_spec) :
        return self._init_handler (handler_spec)
    # end def _init_static_handler

Application = _Werkzeug_Application_ # end class

if __name__ != "__main__" :
    GTW.Werkzeug._Export ("*")
### __END__ GTW.Werkzeug.Application
