# -*- coding: utf-8 -*-
# Copyright (C) 2009-2013 Martin Glück. All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. martin@mangari.org
# ****************************************************************************
#
# This module is licensed under the terms of the BSD 3-Clause License
# <http://www.c-tanzer.at/license/bsd_3c.html>.
# ****************************************************************************
#
#++
# Name
#    GTW.NAV.example.hello_world
#
# Purpose
#    Simple hello world using the GTW.NAV and tornado frameworks
#
# Revision Dates
#    13-Sep-2009 (MG) Creation
#    14-Jan-2010 (MG) Use `TFL.CAO`
#    14-Jan-2010 (CT) `PNS_Aliases` added and `Account_P` creation enabled
#    17-Aug-2010 (CT) Switch from `title/desc` to `short_title/title`
#    11-Mar-2011 (CT) s/cookie_secret/cookie_salt/
#    ««revision-date»»···
#--

from   _TFL                      import TFL
from   _GTW                      import GTW
import _GTW._NAV.Request_Handler
import _GTW._Tornado.Application
import _GTW.File_Session
import  os

import _GTW._NAV.Base
import _GTW._NAV.ReST
import _GTW._NAV._E_Type.Admin
import _GTW._NAV.E_Type.Site_Admin
import _GTW._OMP._PAP.Nav
import _GTW._OMP._SWP.Nav
from   _JNJ.Templateer import Templateer
import _JNJ

from   _MOM            import MOM
from    app_import     import app_type as apt

import _GTW._Form._MOM.Instance
import _GTW._Form._MOM.Inline_Description
import _GTW._Form._MOM.Field_Group_Description

import _GTW._NAV.Auth

from Nav_Pages import Redirect, Error, E_Type_Form, I18N_Test

from   _MOM                      import MOM
from   _MOM.Product_Version      import Product_Version, IV_Number

import _TFL.I18N
TFL.I18N.load ("de_AT", "en_US", domains = ("messages", ), use = "en_US")

GTW.Version = Product_Version \
    ( productid           = u"GTW Test"
    , productnick         = u"GTW"
    , productdesc         = u"Example web application "
    , date                = "20-Jan-2010"
    , major               = 0
    , minor               = 5
    , patchlevel          = 42
    , author              = u"Christian Tanzer, Martin Glück"
    , copyright_start     = 2010
    , db_version          = IV_Number
        ( "db_version"
        , ("Hello World", )
        , ("Hello World", )
        , program_version = 1
        , comp_min        = 0
        , db_extension    = ".how"
        )
    )

### define the command line and parse it to get the `port` from the command
### line needed for the `site_url`
import _TFL.CAO
import  sys
cmd = TFL.CAO.Cmd \
    ( opts = ( "port:I=8080?Server port"
             , "tornado_reload:B?Use the tornado reload feature"
             )
    ) (sys.argv [1:])

scope  = MOM.Scope.new (apt, None)

anonymous = scope.Auth.Account_Anonymous ("anonymous")
scope.Auth.Account_P ("user1", password = "passwd1", active = True)
scope.Auth.Account_P \
    ("user2", password = "passwd2", active = True, superuser = True)

base_template_dir = os.path.dirname (_JNJ.__file__)
ROOT_DIR          = os.path.dirname (__file__)
template_dirs     = [os.path.join (ROOT_DIR, "templates"), base_template_dir]

NAV               = GTW.NAV.Root \
    ( src_dir           = "."
    , copyright_start   = 2008
    , encoding          = "utf-8"
    , input_encoding    = "utf-8"
    , template          = "static.jnj"
    , account_manager   = scope.Auth.Account
    , anonymous         = anonymous
    , scope             = scope
    , HTTP              = GTW.Tornado
    , Templateer        = Templateer
          ( load_path   = template_dirs
          , trim_blocks = True
          , i18n        = True
          , encoding    = "utf-8"
          , globals     = dict (site_base = "base.jnj")
          , version     = "html/x.jnj"
          )
    )
NAV.add_entries \
    ( ( dict
          ( name           = "index.html"
          , short_title    = u"Home"
          , Type           = GTW.NAV.Page_ReST_F
          )
      , dict
          ( name           = "test.html"
          , short_title    = u"Test"
          , Type           = GTW.NAV.Page_ReST_F
          , login_required = True
          )
      , dict
          ( name           = "sitemap.html"
          , template       = "sitemap.jnj"
          , short_title    = u"Sitemap"
          , Type           = GTW.NAV.Page
          , login_required = True
          )
      , dict
          ( name            = "login.html"
          , template        = "login.jnj"
          , short_title     = u"Login"
          , Type            = GTW.NAV.Auth.Login
          , hidden          = True
          )
      , dict
          ( name            = "logout.html"
          , short_title     = u"Logout"
          , Type            = GTW.NAV.Auth.Logout
          , hidden          = True
          )
      , dict
          ( name            = "I18N.html"
          , short_title     = "I18N Test"
          , template        = "i18n.jnj"
          , Type            = I18N_Test
          )
      , dict
          ( name           = "redirect_301.html"
          , short_title    = u"Redirect 301 (index)"
          , Type           = Redirect
          , redirect_to    = "index.html"
          , code           = 301
          )
      , dict
          ( name           = "redirect_302.html"
          , short_title    = u"Redirect 302 (test)"
          , Type           = Redirect
          , redirect_to    = "test.html"
          , code           = 302
          )
      , dict
          ( sub_dir         = "Admin"
          , short_title     = "Admin"
          , title           = u"Verwaltung der Homepage"
          , head_line       = u"Administration der Homepage"
          , login_required  = False # True
          , etypes          =
              [ GTW.OMP.PAP.Nav.Admin.Person
              , GTW.OMP.SWP.Nav.Admin.Page
              ]
          , Type            = GTW.NAV.E_Type.Site_Admin
          )
      )
    , Dir_Type = GTW.NAV.Dir
    )
NAV.add_entries \
    ( ( dict
          ( name           = "error_%s.html" % c
          , short_title          = u"Display a HTTP error %s" % c
          , Type           = Error
          , code           = c
          )
        for c in (401, 403, 404, 500)
      )
    , Dir_Type = GTW.NAV.Dir
    )
if __name__ == "__main__" :
    print "Start server on port %d" % (cmd.port, )
    if cmd.tornado_reload :
        print "Use Tornado buildin autorelaod feature"
    app = GTW.Tornado.Application \
        ( ((".*$", GTW.NAV.Request_Handler), )
        , cookie_salt   = "sdf756!764/785'H7858&)=8766/&%$rw2?g56476W§+@"
        , debug         = cmd.tornado_reload
        , Session_Class = GTW.File_Session
        , session_id    = "SESSION_ID"
        , i18n          = True
        )
    GTW.Tornado.start_server (app, cmd.port)
### __END__ GTW.NAV.example.hello_world
