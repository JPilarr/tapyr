# -*- coding: utf-8 -*-
# Copyright (C) 2009 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
#
# This module is licensed under the terms of the BSD 3-Clause License
# <http://www.c-tanzer.at/license/bsd_3c.html>.
# ****************************************************************************
#
#++
# Name
#    DJO.Nested_Form_Completer
#
# Purpose
#    Helper class for completion in nested forms
#
# Revision Dates
#    19-Aug-2009 (CT) Creation
#    20-Aug-2009 (CT) `template` added
#    20-Aug-2009 (CT) `jsor_form` and `js_on_ready` changed to include `triggers`
#    21-Aug-2009 (CT) `options` factored
#    21-Aug-2009 (CT) `min_chars` added to `options`
#    21-Aug-2009 (CT) Use meta class `M_Unique_If_Named`
#    21-Aug-2009 (CT) `_ignore_options` added and used
#    ««revision-date»»···
#--

from   _TFL                               import TFL
from   _DJO                               import DJO

import _TFL._Meta.Object
import _TFL._Meta.M_Unique_If_Named
import _TFL.Caller

class Nested_Form_Completer (TFL.Meta.Object) :
    """Helper class for completion in nested forms."""

    __metaclass__ = TFL.Meta.M_Unique_If_Named

    jsor_form = "\n".join \
        ( ("""$(".%(mname)s").completer"""
          , """  ({ "list_url" : "%(list_url)s" """
          , """   , "obj_url"  : "%(obj_url)s" """
          , """   , "prefix"   : "%(mname)s" """
          , """   , "triggers" :  %(triggers)s """
          , """  }); """
          , ""
          )
        )

    ### Can be overriden by `__init__` arguments
    options   = dict \
        ( fields    = ()
        , min_chars = 3
        , prefix    = "/Admin"
        , template  = "model_completion_list.html"
        )
    _ignore_options = set (["name", "prefix", "template"])

    def __init__ (self, triggers, ** kw) :
        self._triggers = triggers
        self.options   = dict (self.options, ** kw)
    # end def __init__

    def js_on_ready (self, nested_form_group) :
        from django.utils import simplejson
        model    = nested_form_group.model
        fname    = nested_form_group.field_name
        mname    = nested_form_group.Name
        list_url = "%s/%s/complete/%s"  % (self.prefix, model.__name__, fname)
        obj_url  = "%s/%s/completed/%s" % (self.prefix, model.__name__, fname)
        triggers = simplejson.dumps (self.triggers)
        result   = self.jsor_form % TFL.Caller.Object_Scope (self)
        return (result, )
    # end def js_on_ready

    @property
    def triggers (self) :
        result = {}
        for k, v in self._triggers.iteritems () :
            result [k] = d = v.copy ()
            for k, v in self.options.iteritems () :
                if k not in self._ignore_options :
                    d.setdefault (k, v)
        return result
    # end def triggers

    def __getattr__ (self, name) :
        try :
            return self.options [name]
        except KeyError :
            raise AttributeError, name
    # end def __getattr__

# end class Nested_Form_Completer

if __name__ != "__main__":
    DJO._Export ("*")
### __END__ DJO.Nested_Form_Completer
