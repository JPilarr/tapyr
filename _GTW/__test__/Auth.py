# -*- coding: iso-8859-15 -*-
# Copyright (C) 2012-2013 Martin Glueck All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. martin@mangari.org
# #*** <License> ************************************************************#
# This module is part of the package GTW.__test__.
#
# This module is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this module. If not, see <http://www.gnu.org/licenses/>.
# #*** </License> ***********************************************************#
#
#++
# Name
#    GTW.__test__.Auth
#
# Purpose
#    Tests for the GTW.RST.TOP.Auth classes
#
# Revision Dates
#    16-Aug-2012 (MG) Creation
#    25-Sep-2012 (CT) Fix `_register` errors
#     9-Oct-2012 (CT) Change "error" class, fix various errors
#     6-Dec-2012 (MG) Fix test executaion, new test for query attribute added
#     1-May-2013 (CT) Add `@foo.bar` to email addresses
#    26-May-2013 (CT) Add `_test_migration`
#    13-Jun-2013 (CT) Remove `PNS_Aliases`
#    ��revision-date�����
#--

from   __future__ import absolute_import, division, print_function, unicode_literals

_login_logout = r"""
    >>> root   = Scaffold (["wsgi", "-db_url=sqlite:///auth.sqlite"]) # doctest:+ELLIPSIS
    ...
    >>> print (root.top.Templateer.env.globals ["html_version"])
    html/5.jnj

    >>> scope  = root.scope
    >>> Auth   = scope.Auth
    >>> resp   = Scaffold.test_post ("/Auth/login.html")
    >>> errors = resp.PQ (b"li.Error-Message")
    >>> print ("".join (e.string for e in errors)) ### 1
    <li class="Error-Message">
              Please enter a username
            </li>
            <li class="Error-Message">
              A user name is required to login.
            </li>
            <li class="Error-Message">
              The password is required.
            </li>

    >>> data   = dict (username = "a1@foo.bar")
    >>> resp   = Scaffold.test_post ("/Auth/login.html", data = data)
    >>> errors = resp.PQ (b"li.Error-Message")
    >>> print ("".join (e.string for e in errors))
    <li class="Error-Message">
              Username or password incorrect
            </li>
            <li class="Error-Message">
              The password is required.
            </li>

    >>> data ["password"] = "p2"
    >>> resp   = Scaffold.test_post ("/Auth/login.html", data = data)
    >>> errors = resp.PQ (b"li.Error-Message")
    >>> print ("".join (e.string for e in errors))
    <li class="Error-Message">
          Username or password incorrect
        </li>

    >>> data ["password"] = "p1"
    >>> data ["next"]     = "/after/login"
    >>> resp   = Scaffold.test_post ("/Auth/login.html", data = data)
    >>> errors = resp.PQ (b"li.Error-Message")
    >>> print ("".join (e.string for e in errors))
    <BLANKLINE>
    >>> resp.headers ["Location"] ### login
    'http://localhost/after/login'

    >>> resp = Scaffold.test_post ("/Auth/logout.html", data = dict (next = "/after/logout"))
    >>> resp
    <Test_Response streamed [303 SEE OTHER]>
    >>> resp.headers ["Location"] ### logout
    'http://localhost/after/logout'

    >>> data ["username"] = "a3@foo.bar"
    >>> data ["password"] = "p3"
    >>> resp   = Scaffold.test_post ("/Auth/login.html", data = data)
    >>> errors = resp.PQ (b"li.Error-Message")
    >>> print ("".join (e.string for e in errors))
    <li class="Error-Message">
          This account is currently inactive
        </li>

    >>> a2 = Auth.Account.query (name = "a2@foo.bar").one ()
    >>> a2.password_change_required
    >>> data ["username"] = "a2@foo.bar"
    >>> data ["password"] = "p2"
    >>> resp   = Scaffold.test_post ("/Auth/login.html", data = data)
    >>> errors = resp.PQ (b"li.Error-Message")
    >>> print ("".join (e.string for e in errors))
    >>> resp.headers ["Location"] ### login a2
    'http://localhost/after/login'

    >>> Auth.Account.force_password_change (a2)
    >>> a2.password_change_required
    Auth.Account_Password_Change_Required ((u'a2@foo.bar', ))
    >>> resp   = Scaffold.test_post ("/Auth/login.html", data = data)
    >>> errors = resp.PQ (b"li.Error-Message")
    >>> print ("".join (e.string for e in errors))
    >>> resp.headers ["Location"] ### login a2 - redirect to change passwd
    'http://localhost/Auth/change_password?p=2'
"""

_activate        = r"""
    >>> root   = Scaffold (["wsgi", "-db_url=sqlite:///auth.sqlite", "-create"]) # doctest:+ELLIPSIS
    ...
    >>> scope  = root.scope
    >>> Auth   = scope.Auth
    >>> a2     = Auth.Account.query (name = "a2@foo.bar").one ()
    >>> passwd = a2.prepare_activation ()
    >>> scope.commit ()

    >>> resp   = Scaffold.test_get ("/Auth/activate.html", query_string = "p=%%d" %% (a2.pid, ))
    >>> print ("".join (t.string for t in resp.PQ (b"li.account-name")))
    <li class="account-name">a2@foo.bar</li>

    >>> data   = dict (username = a2.name)
    >>> resp   = Scaffold.test_post ("/Auth/activate.html", data = data)
    >>> errors = resp.PQ (b"li.Error-Message")
    >>> print ("".join (e.string for e in errors))
    <li class="Error-Message">
              Username or password incorrect
            </li>
          <li class="Error-Message">
              The password is required.
            </li>
          <li class="Error-Message">
              The password is required.
            </li>
          <li class="Error-Message">
              Repeat the password for verification.
            </li>
    <BLANKLINE>

    >>> data ["password"] = passwd
    >>> resp   = Scaffold.test_post ("/Auth/activate.html", data = data)
    >>> errors = resp.PQ (b"li.Error-Message")
    >>> print ("".join (e.string for e in errors))
    <li class="Error-Message">
              The password is required.
            </li>
          <li class="Error-Message">
              Repeat the password for verification.
            </li>
    <BLANKLINE>

    >>> data ["npassword"] = "P2"
    >>> resp   = Scaffold.test_post ("/Auth/activate.html", data = data)
    >>> errors = resp.PQ (b"li.Error-Message")
    >>> print ("".join (e.string for e in errors))
    <li class="Error-Message">
          Repeat the password for verification.
        </li>

    >>> data ["vpassword"] = "p2"
    >>> resp   = Scaffold.test_post ("/Auth/activate.html", data = data)
    >>> errors = resp.PQ (b"li.Error-Message")
    >>> print ("".join (e.string for e in errors))
    <li class="Error-Message">
          The passwords don't match.
        </li>

    >>> data ["vpassword"] = "P2"
    >>> resp   = Scaffold.test_post ("/Auth/activate.html", data = data)
    >>> errors = resp.PQ (b"li.Error-Message")
    >>> print ("".join (e.string for e in errors))
    <BLANKLINE>
"""

_register        = r"""
    >>> root   = Scaffold (["wsgi", "-db_url=sqlite:///auth.sqlite"]) # doctest:+ELLIPSIS
    ...
    >>> scope  = root.scope
    >>> Auth   = scope.Auth
    >>> resp   = Scaffold.test_get ("/Auth/register.html")
    >>> print ("\n".join (str (sorted (t.items ())) for t in resp.PQ (b"input")))
    [('id', 'F_username'), ('name', 'username'), ('type', 'text')]
    [('id', 'F_npassword'), ('name', 'npassword'), ('type', 'password')]
    [('id', 'F_vpassword'), ('name', 'vpassword'), ('type', 'password')]
    [('title', 'Update Email'), ('type', 'submit'), ('value', 'Update Email')]
    [('name', 'next'), ('type', 'hidden')]

    >>> data   = dict ()
    >>> resp   = Scaffold.test_post ("/Auth/register.html", data = data)
    >>> errors = resp.PQ (b"li.Error-Message")
    >>> print ("".join (e.string for e in errors))
    <li class="Error-Message">
              A user name is required to login.
            </li>
          <li class="Error-Message">
              The password is required.
            </li>
          <li class="Error-Message">
              Repeat the password for verification.
            </li>
    <BLANKLINE>

    >>> data ["username"] = "a2@foo.bar"
    >>> resp   = Scaffold.test_post ("/Auth/register.html", data = data)
    >>> errors = resp.PQ (b"li.Error-Message")
    >>> print ("".join (e.string for e in errors))
    <li class="Error-Message">
              Account with this Email address already registered
            </li>
          <li class="Error-Message">
              The password is required.
            </li>
          <li class="Error-Message">
              Repeat the password for verification.
            </li>
    <BLANKLINE>

    >>> data ["username"] = "new-account@foo.bar"
    >>> data ["npassword"] = "new-pass"
    >>> resp   = Scaffold.test_post ("/Auth/register.html", data = data)
    >>> errors = resp.PQ (b"li.Error-Message")
    >>> print ("".join (e.string for e in errors))
    <li class="Error-Message">
          Repeat the password for verification.
        </li>

    >>> data ["vpassword"] = "newpass"
    >>> resp   = Scaffold.test_post ("/Auth/register.html", data = data)
    >>> errors = resp.PQ (b"li.Error-Message")
    >>> print ("".join (e.string for e in errors))
    <li class="Error-Message">
          The passwords don't match.
        </li>

    >>> data ["vpassword"] = "new-pass"
    >>> resp   = Scaffold.test_post ("/Auth/register.html", data = data) # doctest:+ELLIPSIS
    Email via localhost from webmaster@ to ['new-account@foo.bar']
    Content-type: text/plain; charset=utf-8
    Date: ...
    Subject: Email confirmation for localhost
    To: new-account@foo.bar
    From: webmaster@
    <BLANKLINE>
    Confirm new email address new-account@foo.bar
    <BLANKLINE>
    To verify the new email address, please click the following link: http://localhost/Auth/action?...
    >>> errors = resp.PQ (b"li.Error-Message")
    >>> print ("".join (e.string for e in errors))
    <BLANKLINE>

    >>> a = Auth.Account.query (name = "new-account@foo.bar").one ()
    >>> links = Auth._Account_Token_Action_.query ().all ()
    >>> len (links)
    1
    >>> resp = Scaffold.test_get ("/Auth/action.html?p=%%d&t=%%s" %% (a.pid, links [0].token))
    >>> resp.headers ["Location"]
    'http://localhost/'

    >>> links = Auth._Account_Token_Action_.query ().all ()
    >>> len (links)
    0
"""

_change_email    = r"""
    >>> root   = Scaffold (["wsgi", "-db_url=sqlite:///auth.sqlite"]) # doctest:+ELLIPSIS
    ...
    >>> scope  = root.scope
    >>> Auth   = scope.Auth
    >>> a2     = Auth.Account.query (name = "a2@foo.bar").one ()
    >>> passwd = "p2"

    ### first, check if we can change the email without beeing logged in
    >>> resp   = Scaffold.test_get ("/Auth/change_email.html", query_string = "p=%%d" %% (a2.pid, ))
    >>> resp.status
    '400 BAD REQUEST'

    >>> login (Scaffold, a2, passwd)
    True
    >>> resp   = Scaffold.test_get ("/Auth/change_email.html", query_string = "p=%%d" %% (a2.pid, ))
    >>> print ("".join (t.string for t in resp.PQ (b"li#account-name")))
    <li id="account-name">a2@foo.bar</li>

    >>> data   = dict (username = a2.name)
    >>> resp   = Scaffold.test_post ("/Auth/change_email.html", data = data)
    >>> errors = resp.PQ (b"li.Error-Message")
    >>> print ("".join (e.string for e in errors))
    <li class="Error-Message">
              Username or password incorrect
            </li>
          <li class="Error-Message">
              The password is required.
            </li>
          <li class="Error-Message">
              The Email is required.
            </li>
          <li class="Error-Message">
              Repeat the EMail for verification.
            </li>
    <BLANKLINE>

    >>> data ["password"] = passwd
    >>> resp   = Scaffold.test_post ("/Auth/change_email.html", data = data)
    >>> errors = resp.PQ (b"li.Error-Message")
    >>> print ("".join (e.string for e in errors))
    <li class="Error-Message">
              The Email is required.
            </li>
          <li class="Error-Message">
              Repeat the EMail for verification.
            </li>
    <BLANKLINE>

    >>> data ["nemail"] = "new-email@foo.bar"
    >>> resp   = Scaffold.test_post ("/Auth/change_email.html", data = data)
    >>> errors = resp.PQ (b"li.Error-Message")
    >>> print ("".join (e.string for e in errors))
    <li class="Error-Message">
          Repeat the EMail for verification.
        </li>

    >>> data ["vemail"] = "newemail@foo.bar"
    >>> resp   = Scaffold.test_post ("/Auth/change_email.html", data = data)
    >>> errors = resp.PQ (b"li.Error-Message")
    >>> print ("".join (e.string for e in errors))
    <li class="Error-Message">
          The Email's don't match.
        </li>

    >>> data ["vemail"] = "new-email@foo.bar"
    >>> resp   = Scaffold.test_post ("/Auth/change_email.html", data = data) # doctest:+ELLIPSIS
    Email via localhost from webmaster@ to ['new-email@foo.bar']
    Content-type: text/plain; charset=utf-8
    ...
    Subject: Email confirmation for localhost
    To: new-email@foo.bar
    From: webmaster@
    <BLANKLINE>
    Confirm new email address new-email@foo.bar
    ...
    >>> errors = resp.PQ (b"li.Error-Message")
    >>> print ("".join (e.string for e in errors))
    <BLANKLINE>

    >>> links = Auth._Account_Token_Action_.query ().all ()
    >>> len (links)
    1
    >>> resp = Scaffold.test_get ("/Auth/action.html?p=2&t=%%s" %% links [0].token)
    >>> resp.headers ["Location"]
    'http://localhost/'

    >>> links = Auth._Account_Token_Action_.query ().all ()
    >>> len (links)
    0
"""

_change_password = r"""
    >>> root   = Scaffold (["wsgi", "-db_url=sqlite:///auth.sqlite"])
    >>> scope  = root.scope
    >>> Auth   = scope.Auth
    >>> a2     = Auth.Account.query (name = "a2@foo.bar").one ()
    >>> passwd = "p2"
    >>> scope.commit ()

    >>> login (Scaffold, a2, passwd)
    True
    >>> resp   = Scaffold.test_get ("/Auth/change_password.html", query_string = "p=%%d" %% (a2.pid, ))
    >>> print ("".join (t.string for t in resp.PQ (b"li.account-name")))
    <li class="account-name">a2@foo.bar</li>

    >>> data   = dict (username = a2.name)
    >>> resp   = Scaffold.test_post ("/Auth/change_password.html", data = data)
    >>> errors = resp.PQ (b"li.Error-Message")
    >>> print ("".join (e.string for e in errors))
    <li class="Error-Message">
              Username or password incorrect
            </li>
          <li class="Error-Message">
              The password is required.
            </li>
          <li class="Error-Message">
              The password is required.
            </li>
          <li class="Error-Message">
              Repeat the password for verification.
            </li>
    <BLANKLINE>

    >>> data ["password"] = passwd
    >>> resp   = Scaffold.test_post ("/Auth/change_password.html", data = data)
    >>> errors = resp.PQ (b"li.Error-Message")
    >>> print ("".join (e.string for e in errors))
    <li class="Error-Message">
              The password is required.
            </li>
          <li class="Error-Message">
              Repeat the password for verification.
            </li>
    <BLANKLINE>

    >>> data ["npassword"] = "P2"
    >>> resp   = Scaffold.test_post ("/Auth/change_password.html", data = data)
    >>> errors = resp.PQ (b"li.Error-Message")
    >>> print ("".join (e.string for e in errors))
    <li class="Error-Message">
          Repeat the password for verification.
        </li>

    >>> data ["vpassword"] = "p2"
    >>> resp   = Scaffold.test_post ("/Auth/change_password.html", data = data)
    >>> errors = resp.PQ (b"li.Error-Message")
    >>> print ("".join (e.string for e in errors))
    <li class="Error-Message">
          The passwords don't match.
        </li>

    >>> data ["vpassword"] = "P2"
    >>> resp   = Scaffold.test_post ("/Auth/change_password.html", data = data)
    >>> errors = resp.PQ (b"li.Error-Message")
    >>> print ("".join (e.string for e in errors))
    <BLANKLINE>
"""

_password_reset  = r"""
    >>> root   = Scaffold (["wsgi", "-db_url=sqlite:///auth.sqlite"]) # doctest:+ELLIPSIS
    ...
    >>> scope  = root.scope
    >>> Auth   = scope.Auth
    >>> data   = dict ()
    >>> resp   = Scaffold.test_post ("/Auth/request_reset_password.html", data = data)
    >>> errors = resp.PQ (b"li.Error-Message")
    >>> print ("".join (e.string for e in errors))
    <li class="Error-Message">
          A user name is required to login.
        </li>

    >>> data ["username"]= "a5@foo.bar"
    >>> resp   = Scaffold.test_post ("/Auth/request_reset_password.html", data = data)
    >>> errors = resp.PQ (b"li.Error-Message")
    >>> print ("".join (e.string for e in errors))
    <li class="Error-Message">
          Account could not be found
        </li>

    >>> data ["username"]= "a2@foo.bar"
    >>> resp   = Scaffold.test_post ("/Auth/request_reset_password.html", data = data)# doctest:+ELLIPSIS
    Email via localhost from webmaster@ to ['a2@foo.bar']
    Content-type: text/plain; charset=utf-8
    ...
    Subject: Password reset for user a2@foo.bar on website localhost
    To: a2@foo.bar
    From: webmaster@
    <BLANKLINE>
    Password of a2@foo.bar reset
    <BLANKLINE>
    Your password was reset to the temporary value:
    <BLANKLINE>
        ...
    <BLANKLINE>
    Please click the following link to change the temporary password to a new value:
    <BLANKLINE>
        ...
    >>> errors = resp.PQ (b"li.Error-Message")
    >>> print ("".join (e.string for e in errors))
"""

_test_migration     = r"""

    >>> root   = Scaffold (["wsgi", "-db_url=sqlite:///auth.sqlite", "-create"]) # doctest:+ELLIPSIS
    >>> scope  = root.scope
    >>> Auth   = scope.Auth
    >>> g1     = Auth.Group ("g1")
    >>> _      = Auth.Account_in_Group (("a1@foo.bar", ), ("g1", ), raw = True)
    >>> mig    = Auth.Account.migration ()
    >>> for k, d in sorted (pyk.iteritems (mig)) :
    ...     print (k)
    ...     for epk in sorted (d) :
    ...         print (" " * 2, epk)
    ...         print \
    ...             ( " " * 5
    ...             , (chr (10) + "      ").join
    ...                 (   "%%-10s : %%s"
    ...                       %% (k, v if k != "password" else "<password>")
    ...                 for k, v in sorted (pyk.iteritems (d [epk]))
    ...                 )
    ...             )
    Account
       (u'a1@foo.bar', 'Auth.Account')
          electric   : no
          enabled    : yes
          password   : <password>
          ph_name    : Bcrypt
          superuser  : yes
          suspended  : no
          x_locked   : no
       (u'a2@foo.bar', 'Auth.Account')
          electric   : no
          enabled    : yes
          password   : <password>
          ph_name    : Bcrypt
          superuser  : no
          suspended  : no
          x_locked   : no
       (u'a3@foo.bar', 'Auth.Account')
          electric   : no
          enabled    : yes
          password   : <password>
          ph_name    : Bcrypt
          superuser  : no
          suspended  : yes
          x_locked   : no
       (u'a4@foo.bar', 'Auth.Account')
          electric   : no
          enabled    : no
          password   : <password>
          ph_name    : Bcrypt
          superuser  : no
          suspended  : yes
          x_locked   : no
    Group
       (u'g1', 'Auth.Group')
          desc       :
          electric   : no
          x_locked   : no
    Person
    links
       ((u'a1@foo.bar', 'Auth.Account'), (u'g1', 'Auth.Group'), 'Auth.Account_in_Group')
          electric   : no
          x_locked   : no

"""

_test_query_attr    = r"""
    >>> root   = Scaffold (["wsgi", "-db_url=sqlite:///auth.sqlite", "-create"]) # doctest:+ELLIPSIS
    ...
    >>> scope  = root.scope
    >>> Auth   = scope.Auth

    >>> Auth.Account.query (Q.active == True).all ()
    [Auth.Account (u'a1@foo.bar'), Auth.Account (u'a2@foo.bar')]
"""

from   _GTW.__test__.Test_Command import *
from   _TFL.User_Config           import user_config
import _TFL.Password_Hasher
import _GTW._OMP._Auth.import_Auth

try :
    Bcrypt = TFL.Password_Hasher.Bcrypt
except AttributeError :
    pass
else :
    ### reduce CPU time necessary
    Bcrypt.default_rounds = 6

def fixtures (self, scope) :
    Auth  = scope.Auth
    a1    = Auth.Account.create_new_account_x \
        ("a1@foo.bar", "p1", enabled = True,  suspended = False, superuser = True)
    a2    = Auth.Account.create_new_account_x \
        ("a2@foo.bar", "p2", enabled = True,  suspended = False, superuser = False)
    a3    = Auth.Account.create_new_account_x \
        ("a3@foo.bar", "p3", enabled = True,  suspended = True,  superuser = False)
    a3    = Auth.Account.create_new_account_x \
        ("a4@foo.bar", "p4", enabled = False, suspended = True , superuser = False)
    scope.commit ()
# end def fixtures

user_config.time_zone                 = "Europe/Vienna"

Scaffold = GTW_Test_Command ()
Scaffold.__class__.fixtures = fixtures

def login (Scaffold, account, password) :
    data   = dict \
        ( username = getattr (account, "name", account)
        , password = password
        , next     = "/redirected-after-login"
        )
    ### print ("Login %s" % data.get ("username"))
    resp   = Scaffold.test_post ("/Auth/login.html", data = data)
    return resp.status_code == 303
# end def login

__test__ = Scaffold.create_test_dict \
    ( dict
        ( activate        = _activate
        , change_email    = _change_email
        , change_password = _change_password
        , login_logout    = _login_logout
        , register        = _register
        , reset_password  = _password_reset
        , test_migration  = _test_migration
        , test_query_attr = _test_query_attr
        )
    , backends = ("SQL", )
    )
### __END__ GTW.__test__.Auth
