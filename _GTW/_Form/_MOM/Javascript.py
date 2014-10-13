# -*- coding: utf-8 -*-
# Copyright (C) 2010-2011 Martin Glueck All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. martin@mangari.org
# ****************************************************************************
# This module is part of the package GTW.Form.MOM.
#
# This module is licensed under the terms of the BSD 3-Clause License
# <http://www.c-tanzer.at/license/bsd_3c.html>.
# ****************************************************************************
#
#++
# Name
#    GTW.Form.MOM.Javascript
#
# Purpose
#    MOM specific javascript code generation
#
# Revision Dates
#    26-Feb-2010 (MG) Creation
#    27-Feb-2010 (MG) `Field_Completer` added, `_MOM_Completer_` factored
#    28-Feb-2010 (MG) `_send_suggestions` factored and `uniq_p` used for
#                     `Field_Completer._send_suggestions`
#    02-Mar-2010 (MG) `Field_Completer.js_on_ready` suuport for top level
#                     field completion added
#     2-Mar-2010 (MG) `Multi_Completer` moved into `GTW.Form.Javascript`
#     3-May-2010 (MG) New form handling implemented
#     6-May-2010 (MG) `Field_Completer.js_on_ready` urls fixed
#    12-May-2010 (CT) Use `pid`, not `lid`
#    15-May-2010 (MG) `_form_as_dict` factored
#    23-Jun-2010 (MG) `Completer._send_result` changed to not send `_state_`
#    24-Jun-2010 (CT) 3-compatibility
#    11-Jan-2011 (CT) s/handler.json/handler.write_json/
#    ««revision-date»»···
#--

from   _TFL               import TFL

from   _TFL.predicate     import uniq_p

import _TFL._Meta.Object
import _TFL._Meta.M_Unique_If_Named
import _TFL.Accessor

from   _GTW                       import GTW

import _GTW._Form.Javascript      as     Javascript
import _GTW._Form._MOM
from   _MOM.import_MOM            import Q

class _MOM_Completer_ (GTW.Form.Javascript._Completer_) :
    """Base class for the MOM Completers"""

    def complete (self, form, handler, pid) :
        et_man   = form.et_man
        try :
            obj  = et_man.pid_query (pid)
        except IndexError, exc :
            error = (_T("%s `%s` does not exist!") % (_T(et_man.ui_name), id))
            raise self.top.HTTP.Error_404 (request.path, error)
        return self._send_result (form, handler, obj)
    # end def complete

    def suggestions (self, form, handler, args) :
        et_man   = form.et_man
        trigger  = getattr (et_man._etype, args.pop ("TRIGGER_FIELD"))
        filter   = tuple \
            (    getattr (Q, k).STARTSWITH (v)
            for (k, v) in et_man.cooked_attrs (args).iteritems ()
            )
        return self._send_suggestions \
            (handler, trigger, et_man.query ().filter (* filter).distinct ())
    # end def suggestions

# end class _MOM_Completer_

class Field_Completer (_MOM_Completer_) :
    """Complete parts of a form."""

    options = dict \
        ( min_chars = 2
        )

    def __init__ ( self, trigger, fields
                 , prefix       = "/Admin"
                 , separator    = ", "
                 , ** kw
                 ) :
        self.trigger     = trigger
        self.prefix    = prefix
        self.separator = separator
        self.options   = dict (self.options, ** kw)
        if not isinstance (fields, (tuple, list)) :
            fields     = (fields, )
        self.fields    = fields
    # end def __init__

    def _send_result (self, form_cls, handler, obj) :
        attributes = obj.attributes
        result     = dict \
            ((f, attributes [f].get_raw (obj)) for f in self.fields)
        return handler.write_json (result)
    # end def _send_result

    def _send_suggestions (self, handler, trigger, query) :
        result = uniq_p \
            (((self.ui_display (c), c) for c in query), TFL.Getter [0])
        return handler.write_json \
            ( [ dict
                  ( pid   = str (c.pid)
                  , value = trigger.get_raw (c)
                  , label = d
                  )
                  for d, c in result
              ]
            )
    # end def _send_suggestions

    def js_on_ready (self, form, role_name) :
        form_name    = prefix = form.form_name
        postfix      = ""
        if role_name and form_name.endswith (role_name) :
            prefix   = form_name [: -len(role_name) - 2]
            postfix  = role_name
        parts        = form_name.split ("__", 1)
        if len (parts) == 2 :
            bname, fname = parts [0], "/" + parts [1] + "__"
        else :
            bname, fname = parts [0], "/"
        url_format   = "%s/%s/%%s%s%s" \
            % (self.prefix, bname, fname, self.trigger)
        result = \
            ( dict
                ( field_prefix  = prefix
                , field_postfix = postfix
                , triggers      =
                    {self.trigger : dict (self.options, fields = self.fields)}
                , type          = self.__class__.__name__
                , suggest_url   = url_format % ("complete", )
                , complete_url  = url_format % ("completed", )
                )
            ,
            )
        return result
    # end def js_on_ready

    def ui_display (self, obj) :
        attributes = obj.attributes
        result     = [attributes [f].get_raw (obj) for f in self.fields]
        return self.separator.join (p for p in result if p)
    # end def ui_display

# end class Field_Completer

class Completer (_MOM_Completer_) :
    """Completion for the whole form for an MOM entity."""

    ### Can be overriden by `__init__` arguments
    options   = dict \
        ( fields       = ()
        , min_chars    = 3
        , prefix       = "/Admin"
        )
    _ignore_options = set (("name", "prefix"))

    def __init__ (self, triggers, ** kw) :
        self._triggers = triggers
        self.options   = dict (self.options, ** kw)
    # end def __init__

    def js_on_ready (self, form, role_name) :
        form_name    = prefix = form.form_name
        postfix      = ""
        bname, fname = form_name.split ("__", 1)
        url_format   = "%s/%s/%%s/%s"  % (self.options ["prefix"], bname, fname)
        if form_name.endswith (role_name) :
            prefix   = form_name [: -len(role_name) - 2]
            postfix  = role_name
        return \
            ( dict
                ( field_prefix  = prefix
                , field_postfix = postfix
                , triggers      = self.triggers
                , type          = self.__class__.__name__
                , suggest_url   = url_format % ("complete", )
                , complete_url  = url_format % ("completed", )
                )
            ,
            )
    # end def js_on_ready

    def _send_suggestions (self, handler, trigger, query) :
        return handler.write_json \
            ( [ dict
                  ( pid   = str (c.pid)
                  , value = trigger.get_raw (c)
                  , label = self.ui_display (c)
                  )
                for c in query
              ]
            )
    # end def _send_suggestions

    @TFL.Meta.Class_and_Instance_Method
    def _send_result (self, form_cls, handler, obj) :
        data                = self.form_as_dict (form_cls (obj))
        data ["ui_display"] = getattr (obj, "ui_display", u"")
        return handler.write_json (data)
    # end def _send_result

    @classmethod
    def form_as_dict (cls, form) :
        data = dict ((f.name, form.get_raw (f)) for f in form.fields)
        for ai in form.inline_fields :
            data [ai.link_name] = cls.form_as_dict (ai.form)
        ###data.pop ("_state_", None)
        return data
    # end def form_as_dict

    @property
    def triggers (self) :
        result = {}
        for k, v in self._triggers.iteritems () :
            result [k] = d = v.copy ()
            for k, v in self.options.iteritems () :
                if k not in self._ignore_options :
                    d.setdefault (k, v)
            if not isinstance (d ["fields"], (list, tuple)) :
                d ["fields"] = (d ["fields"], )
        return result
    # end def triggers

    def ui_display (self, obj) :
        return obj.ui_display
    # end def ui_display

# end class Completer

if __name__ != "__main__" :
    GTW.Form.MOM._Export_Module ()
### __END__ GTW.Form.MOM.Javascript
