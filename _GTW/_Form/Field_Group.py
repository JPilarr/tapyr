# -*- coding: utf-8 -*-
# Copyright (C) 2010 Martin Glueck All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. martin@mangari.org
# ****************************************************************************
# This module is part of the package GTW.Form.
#
# This module is licensed under the terms of the BSD 3-Clause License
# <http://www.c-tanzer.at/license/bsd_3c.html>.
# ****************************************************************************
#
#++
# Name
#    GTW.Form.Field_Group
#
# Purpose
#    A field group which is bsaically a Field_Group_Description but with
#    field's which are `bound` to an object.
#
# Revision Dates
#    18-Jan-2010 (MG) Creation
#    29-Jan-2010 (MG) Reference to `field_group_description` added and
#                     `__getattr__` added to take undefined attrs from the
#                     `field_group_description`
#    15-Apr-2010 (MG) `Media` moved in here (was in
#                     `GTW.Form.Field_Group_Description`)
#     3-May-2010 (MG) `defaults` added
#    ««revision-date»»···
#--

from   _TFL                                 import TFL
import _TFL._Meta.Object
import _TFL._Meta.Once_Property
import _TFL.NO_List

from   _GTW                                 import GTW
import _GTW._Form._MOM

import  itertools

class Field_Group (TFL.Meta.Object) :
    """A group of form field."""

    action_list = ()

    def __init__ (self, fields, field_group_description) :
        self.fields                  = TFL.NO_List         (fields)
        self.field_group_description = field_group_description
    # end def __init__

    def defaults (self, form, instance, defaults) :
        ### possible hook for a field group to change the default values
        ### this hook is execture AFTER the default values of the fields have
        ### been added to the `defaults` dict
        pass
    # end def defaults

    @TFL.Meta.Once_Property
    def Media (self) :
        try :
            medias = itertools.chain \
                ((f.Media for f in self.fields), (self.media, ))
            return GTW.Media.from_list ([m for m in medias if m])
        except StandardError, e:
            import pdb; pdb.set_trace ()
            raise e
    # end def Media

    def setup_javascript (self, form) :
        if self.completer :
            self.completer.attach (form, multi_completer = form.completer)
    # end def setup_javascript

    def __getattr__ (self, name) :
        result = getattr (self.field_group_description, name)
        setattr (self, name, result)
        return result
    # end def __getattr__

# end class Field_Group

if __name__ != "__main__" :
    GTW.Form._Export ("*")
### __END__ GTW.Form.Field_Group
