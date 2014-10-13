# -*- coding: utf-8 -*-
# Copyright (C) 2009-2010 Martin Glueck All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. martin@mangari.org
# ****************************************************************************
#
# This module is licensed under the terms of the BSD 3-Clause License
# <http://www.c-tanzer.at/license/bsd_3c.html>.
# ****************************************************************************
#
#++
# Name
#    GTW.Form.Field
#
# Purpose
#    A field of a form
#
# Revision Dates
#    30-Dec-2009 (MG) Creation
#    02-Feb-2010 (MG) `get_raw` paremeter form added
#    20-Feb-2010 (MG) Parameter `ui_name` added
#     3-May-2010 (MG) `default` method added to allow callable default values
#                     `_Field_` factored
#                     `Media` added
#     5-May-2010 (MG) `render_mode_description` added
#     6-May-2010 (MG) `needs_header` added
#    25-Jul-2010 (MG) Render mode `dl_seq` added
#    ««revision-date»»···
#--
from   _TFL               import TFL
import _TFL._Meta.Object
from   _GTW               import GTW
import _GTW._Form.Render_Mode_Description
from   _TFL.I18N          import _T

class _Field_ (TFL.Meta.Object) :
    """Base class for form fields."""

    electric                = False
    Media                   = None
    needs_header            = False

    render_mode_description = GTW.Form.Render_Mode_Description \
        ( div_seq = GTW.Form.Widget_Spec
            ( error        = "html/form.jnj,  field_error"
            , help         = "html/form.jnj,  field_help"
            , label        = "html/form.jnj,  field_label"
            , field        = "html/rform.jnj, fi_div_seq"
            )
        , dl_seq = GTW.Form.Widget_Spec
            ( error        = "html/form.jnj,  field_error"
            , help         = "html/rform.jnj, field_help_icon"
            , label        = "html/form.jnj,  field_label"
            , field        = "html/rform.jnj, fi_dl_seq"
            )
        , table   = GTW.Form.Widget_Spec
            ( error        = "html/form.jnj, field_error"
            , help         = "html/form.jnj, field_help"
            , label        = "html/form.jnj, field_label"
            , field_head   = "html/rform.jnj, fi_th"
            , field_header = "html/rform.jnj, fi_header"
            , field_body   = "html/rform.jnj, fi_td"
            )
        )
    def __init__ (self, name, default = u"") :
        self.name      = name
        self._default  = default
    # end def __init__

    def default (self, form, defaults) :
        if callable (self._default) :
            return self._default (form)
        return self._default
    # end def default

# end class _Field_

class Field (_Field_) :
    """A free field which should be part of a HTML form."""

    widget  = GTW.Form.Widget_Spec ("html/field.jnj, string")
    hidden  = False
    choices = ()

    def __init__ (self, name, default = u"", ui_name = None, ** kw) :
        self.__super.__init__ (name, default)
        self.html_name = name
        self.ui_name   = _T (ui_name or name.capitalize ())
        self.__dict__.update (kw)
    # end def __init__

    def get_raw (self, form, defaults) :
        return getattr (form.instance, self.name, self.default (form, defaults))
    # end def get_raw

# end class Field

if __name__ != "__main__" :
    GTW.Form._Export ("_Field_", "Field")
### __END__ GTW.Form.Field
