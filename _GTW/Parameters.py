# -*- coding: utf-8 -*-
# Copyright (C) 2011-2014 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
# This module is part of the package GTW.
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
#    GTW.Parameters
#
# Purpose
#    Support definition of parameters for media, i.e., CSS and JS, fragments
#
# Revision Dates
#    14-Jan-2011 (CT) Creation
#    13-Sep-2011 (CT) `Script_File` and `Style_File` added
#    13-Sep-2011 (MG) doctest added
#    27-Sep-2011 (MG) `Include`, `Eval`, and `_eval_file` added
#     3-Jan-2012 (CT) Add and use `_Media`, change `_MOB_.__call__` to not
#                     unnecessarily wrap media objects
#     8-Apr-2013 (CT) Add `chdir (base_dir)` to `__doc__`
#     8-Apr-2013 (CT) Add `Rule` and its children, `Rule_Definition`,
#                     factor `_Parameter_`
#    19-Sep-2013 (CT) Pass `AttributeError` to `TFL.Attr_Query`
#    20-Feb-2014 (CT) Add `Rule._resolved_children`
#     4-Apr-2014 (CT) Use `TFL.Q_Exp.Base`, not `TFL.Attr_Query ()`
#     9-Apr-2014 (CT) Pass `static_handler` to `GTW.CSS.Style_File`
#    15-Apr-2014 (CT) Fix `Script_File`, `script_files`
#    ««revision-date»»···
#--

from   __future__                 import print_function, unicode_literals

from   _GTW                       import GTW
from   _TFL                       import TFL

from   _TFL._Meta.Property        import Lazy_Property
from   _TFL._Meta.Once_Property   import Once_Property
from   _TFL.pyk                   import pyk
from   _TFL                       import sos

import _TFL._Meta.Object
import _TFL.Caller
import _TFL.Q_Exp

P = TFL.Q_Exp.Base (Ignore_Exception = AttributeError)

def ddict (* ds) :
    result = {}
    for d in ds :
        result.update (d)
    return result
# end def ddict

class _Parameter_ (TFL.Q_Exp.Q_Root) :

    def __init__ (self, * args, ** kw) :
        self.args = args
        self.kw   = kw
    # end def __init__

    def _resolved_args (self, P, args) :
        Q_Root = TFL.Q_Exp.Q_Root
        for a in args :
            if isinstance (a, Q_Root) :
                a = a (P)
            yield a
    # end def _resolved_args

    def _resolved_kw (self, P, kw) :
        Q_Root = TFL.Q_Exp.Q_Root
        for k, v in pyk.iteritems (kw) :
            if isinstance (v, Q_Root) :
                v = v (P)
            yield k, v
    # end def _resolved_kw

# end class P_dict

class P_dict (_Parameter_) :
    """Parameter dict: supports lazy evaluation of dict arguments."""

    def __call__ (self, P) :
        return dict \
            (  * tuple (self._resolved_args (P, self.args))
            , ** dict  (self._resolved_kw   (P, self.kw))
            )
    # end def __call__

# end class P_dict

class Rule (_Parameter_) :
    """Parameterized CSS rule"""

    def __call__ (self, P) :
        from _GTW._CSS import Rule as CSS_Rule
        RT       = getattr (CSS_Rule, self.__class__.__name__)
        args     = tuple (self._resolved_args (P, self.args))
        children = list  \
            (self._resolved_children (P, self.kw.pop ("children", [])))
        kw       = dict  (self._resolved_kw   (P, self.kw))
        return RT (* args, children = children, ** kw)
    # end def __call__

    def _resolved_children (self, P, children) :
        Q_Root = TFL.Q_Exp.Q_Root
        for c in children :
            if isinstance (c, Q_Root) :
                c = c (P)
            if isinstance (c, Rule) :
                c = c (P)
            yield c
    # end def _resolved_children

# end class Rule

class Rule_Attr    (Rule) : pass
class Rule_Child   (Rule) : pass
class Rule_Class   (Rule) : pass
class Rule_Pseudo  (Rule) : pass
class Rule_Sibling (Rule) : pass

class M_Definition (TFL.Meta.Object.__class__) :
    """Meta class for `Definition`."""

    def __init__ (cls, name, bases, dct) :
        cls.__m_super.__init__ (name, bases, dct)
        bn = tuple (reversed ([getattr (b, "_nested_", {}) for b in bases]))
        cls._nested_ = _nested_ = ddict (* bn)
        Q_Root = TFL.Q_Exp.Q_Root
        for k, v in pyk.iteritems (dct) :
            if isinstance (v, Q_Root) :
                setattr (cls, k, Lazy_Property (k, v))
            elif isinstance (v, M_Definition) :
                _nested_ [k] = v
    # end def __init__

    def __call__ (cls, * args, ** kw) :
        result = cls.__m_super.__call__ (* args, ** kw)
        for k, v in pyk.iteritems (cls._nested_) :
            setattr (result, k, v (R = result))
        return result
    # end def __call__

# end class M_Definition

class Definition (TFL.Meta.BaM (TFL.Meta.Object, metaclass = M_Definition)) :
    """Definition of parameters for media, i.e., CSS and JS, fragments.

    >>> class Defaults (Definition) :
    ...   foo = 1
    ...   bar = P.foo * 2
    ...   class nav_col (Definition) :
    ...     bar = 42
    ...     baz = 0
    ...     class own_links (Definition) :
    ...       qux = P.R.bar * 2
    ...       quy = P.T.bar * 2
    ...       quz = P.T.foo * 0.5
    ...     spec = P_dict (a = P.bar, border = "solid")
    ...
    >>> class App (Defaults) :
    ...   foo = 2
    ...   class nav_col (Defaults.nav_col) :
    ...     bar = 137
    ...
    >>> D = Defaults ()
    >>> E = App ()
    >>> D.foo, E.foo
    (1, 2)
    >>> D.bar, E.bar
    (2, 4)
    >>> D.nav_col.own_links.qux, E.nav_col.own_links.qux
    (84, 274)
    >>> D.nav_col.own_links.quy, E.nav_col.own_links.quy
    (4, 8)
    >>> D.nav_col.own_links.quz, E.nav_col.own_links.quz
    (0.5, 1.0)
    >>> sorted (D.nav_col.spec.items ()), sorted (E.nav_col.spec.items ())
    ([('a', 42), ('border', u'solid')], [('a', 137), ('border', u'solid')])
    """

    def __init__ (self, R = None) :
        self.R = R
    # end def __init__

    @Once_Property
    def T (self) :
        R = self.R
        if R is not None :
            return R.T
        else :
            return self
    # end def T

# end class Definition

class Rule_Definition (Definition) :
    """Definition of parameterized CSS rules"""

# end class Rule_Definition

class _Parameters_Scope_ (TFL.Caller.Object_Scope_Mutable) :
    """Encapsulate media parameters so that it is usable as context for
       `exec` of a file containing media fragments.
    """

    _real_name = "Scope"

    class _MOB_ (TFL.Meta.Object) :
        """Wrapper for media object class"""

        def __init__ (self, cls, ext = None, ** kw) :
            self._cls = cls
            self._    = self
            self._ext = ext if ext is not None else []
            self._kw  = kw
        # end def __init__

        def __call__ (self, * args, ** kw) :
            cls = self._cls
            ckw = dict (self._kw, ** kw)
            if len (args) == 1 and (isinstance (args [0], cls)) and not ckw :
                result = args [0]
            else :
                result = cls (* args, ** ckw)
            self._ext.append (result)
            return result
        # end def __call__

        def __getattr__ (self, name) :
            return getattr (self._cls, name)
        # end def __getattr__

    # end class _MOB_

    class _Script_File_ (TFL.Meta.Object) :
        """Wrapper for a javascript `Script_File` referenced in a media fragment."""

        cache_p       = True
        requires      = ()
        may_cache     = True

        def __init__ (self, file_name, body = None, rank = 0) :
            self.file_name = file_name
            self._body     = body
            self.rank      = 0
        # end def __init__

        @property
        def body (self) :
            result = self._body
            if result is None :
                fn = self.file_name
                with open (fn, "rb") as f :
                    result = self._body = f.read ().strip ()
            return result
        # end def body

        def __str__ (self) :
            return self.body
        # end def __str__

    # end class _Script_File_

    css_links            = property (lambda s : s._Media.css_links)
    js_on_ready          = property (lambda s : s._Media.js_on_ready)
    rel_links            = property (lambda s : s._Media.rel_links)
    scripts              = property (lambda s : s._Media.scripts)
    style_sheets         = property (lambda s : s.Style_Sheet._ext)

    def __init__ (self, parameters, env = None) :
        from _GTW._CSS  import import_CSS
        from _GTW.Media import CSS_Link, JS_On_Ready, Rel_Link, Script
        self.P                = parameters
        self.CSS_Link         = self._MOB_ (CSS_Link)
        self.JS_On_Ready      = self._MOB_ (JS_On_Ready)
        self.Rel_Link         = self._MOB_ (Rel_Link)
        self.Script           = self._MOB_ (Script)
        self.Style_Sheet = SS = self._MOB_ (import_CSS.Style_Sheet)
        self.Style_File       = self._MOB_ \
            ( import_CSS.Style_File, SS._ext
            , static_handler = env.static_handler
            )
        self.env              = env
        self.script_files     = []
        self.__super.__init__ \
            ( object = import_CSS
            , locls  = dict (Include = self.Include)
            )
        self._setup_media ()
    # end def __init__

    def Eval (self, * fragments) :
        self.globs = {}
        for f in fragments :
            self._eval_file (f)
        self._setup_media ()
        return self
    # end def Eval

    def Include (self, * includes, ** kw) :
        ignore_missing = kw.pop ("ignore_missing", False)
        assert not kw, kw
        env            = self.env
        get_source     = env.loader.get_source
        for fn in includes :
            if not fn.endswith (".media") :
                fn = "%s.media" % (fn, )
            source, path, _ = get_source (env, fn)
            self._eval_file (path)
    # end def Include

    def Script_File (self, src, ** kw) :
        env  = self.env
        body = None
        if sos.path.isfile (src) :
            fn      = src
        else :
            handler = env.static_handler
            fn      = handler.get_path (src) if handler else None
            if fn is None :
                body, fn, _ = env.loader.get_source (env, src)
        sf   = self._Script_File_ (fn, body, ** kw)
        self.script_files.append  (sf)
    # end def Script_File

    def _eval_file (self, filename) :
        with open (filename, "rt") as file :
            self.globs ["__name__"] = filename
            exec (file.read (), self.globs, self)
    # end def _eval_file

    def _setup_media (self) :
        from _GTW.Media import Media
        self._Media = Media \
            ( self.CSS_Link._ext
            , self.Script._ext
            , self.JS_On_Ready._ext
            , self.Rel_Link._ext
            )
    # end def _setup_media

    def __getitem__ (self, index) :
        try :
            if (   isinstance (index, pyk.string_types)
               and not index.startswith ("_")
               ) :
                return getattr (self, index)
        except AttributeError :
            return self.__super.__getitem__ (index)
    # end def __getitem__

Scope = _Parameters_Scope_ # end class

__doc__ = r"""
>>> from _JNJ.Media_Defaults import Media_Defaults
>>> from _JNJ.Environment    import HTML
>>> import _GTW.jQuery
>>> import os
>>> base_dir        = os.path.abspath \
...    (os.path.join (os.path.dirname (__file__), "..", "_GTW", "__test__"))
>>> env             = HTML (load_path = base_dir)
>>> base_media      = os.path.join (base_dir, "_test.media")
>>> os.chdir (base_dir)

>>> def as_string (fragments) :
...     return "\n\n".join \
...         (str (s) for s in sorted (fragments, key = TFL.Getter.rank))

>>> scope = Scope (Media_Defaults, env).Eval (base_media)
>>> print (as_string (scope.style_sheets))
a, abbr, acronym, address, article, aside, audio
  { border         : 0
  ; font           : inherit
  ; font-size      : 100%
  ; margin         : 0
  ; outline        : 0
  ; padding        : 0
  ; vertical-align : baseline
  }
<BLANKLINE>
/* --> rules from a existing CSS file `/
a.hide
{
    display:          none
}
/* <-- */
>>> print (as_string (scope.script_files))
/* a test javascript file directly included */

>>> list (scope.scripts)
[/media/GTW/js/modernizr.custom.js: text/javascript, /media/GTW/js/jquery.min.js: text/javascript, /media/GTW/js/jquery-ui.min.js: text/javascript, /media/GTW/js/GTW.js: text/javascript, /media/GTW/js/GTW/UI_Icon_Map.js: text/javascript, /media/GTW/js/GTW/jQ/buttonify.js: text/javascript, /media/GTW/js/GTW/util.js: text/javascript, /media/GTW/js/GTW/jsonify.js: text/javascript, /media/GTW/js/GTW/jQ/util.js: text/javascript, /media/GTW/js/GTW/jQ/autocomplete.js: text/javascript, /media/GTW/js/GTW/jQ/e_type_selector.js: text/javascript, /media/GTW/js/GTW/L.js: text/javascript, /media/GTW/js/GTW/jQ/mf3.js: text/javascript]

>>> list (scope.css_links)
[all: /media/GTW/css/jquery.gritter.css]

>>> list (scope.rel_links)
[href="/media/GTW/css/jquery.gritter.rel.css"]

>>> print (as_string (scope.js_on_ready))
/* this is a JS on ready code */

"""

if __name__ != "__main__" :
    GTW._Export_Module ()
### __END__ GTW.Parameters
