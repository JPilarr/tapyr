# -*- coding: utf-8 -*-
# Copyright (C) 2012-2014 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package GTW.AFS.MOM.
# 
# This module is licensed under the terms of the BSD 3-Clause License
# <http://www.c-tanzer.at/license/bsd_3c.html>.
# #*** </License> ***********************************************************#
#
#++
# Name
#    GTW.AFS.MOM.Form_Cache
#
# Purpose
#    Handling of AFS form caching
#
# Revision Dates
#     1-Feb-2012 (CT) Creation (factored from GTW.AFS.MOM.Element.Form)
#     1-Feb-2012 (CT) Add `Extra`
#     6-Sep-2012 (CT) Add `verbose`
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division, print_function, unicode_literals

from   _GTW                   import GTW
from   _TFL                   import TFL

from   _GTW._AFS._MOM.Element import Form

from   _TFL.pyk               import pyk

import _TFL._Meta.Object

class Extra (TFL.Meta.Object) :
    """Specification for an extra, i.e., non-automatically generated, AFS
       form.
    """

    def __init__ (self, fid, * entities) :
        assert entities, "Need at least one entity for Extra"
        self.fid      = fid
        self.entities = entities
    # end def __init__

    def __call__ (self, app_type) :
        return Form (self.fid, children = list (self._gen_children (app_type)))
    # end def __call__

    def _gen_children (self, app_type) :
        for e in self.entities :
            if isinstance (e, pyk.string_types) :
                name = e
                spec = None
                kw   = {}
            elif isinstance (e, dict) :
                name = e ["name"]
                spec = e.get ("spec")
                kw   = e.get ("kw", {})
            else :
                name = e.name
                spec = getattr (e, "spec")
                kw   = getattr (e, "kw", {})
            T = app_type [name]
            S = spec or T.GTW.afs_spec
            yield S (T, ** kw)
    # end def _gen_children

# end class Extra

class _Form_Cache_ (TFL.Meta.Object) :
    """Handle cache for AFS forms"""

    cache_rank = -500
    verbose    = False

    def __init__ (self) :
        self._extras = []
    # end def __init__

    def __call__ (self, * args, ** kw) :
        """Just for compatibility with other cachers"""
        self.pop_to_self (kw, "verbose")
        return self
    # end def __call__

    def add (self, * extras) :
        self._extras.extend (extras)
    # end def add

    def as_pickle_cargo (self, root) :
        if not Form.Table :
            ### mustn't do this more than once
            app_type = root.App_Type
            self._create_auto_forms  (app_type)
            self._create_extra_forms (app_type)
        return dict (AFS_Form_Table = Form.Table)
    # end def as_pickle_cargo

    def from_pickle_cargo (self, root, cargo) :
        table = cargo.get ("AFS_Form_Table", {})
        table.update      (Form.Table)
        ### We want to set `Table` for `GTW.AFS.Element.Form`, not for a
        ### possible descendent class
        GTW.AFS.Element.Form.Table = table
    # end def from_pickle_cargo

    def _create_auto_forms (self, app_type) :
        verbose = self.verbose
        for T in app_type._T_Extension :
            if T.GTW.afs_id is not None and T.GTW.afs_spec is not None :
                f = Form (T.GTW.afs_id, children = [T.GTW.afs_spec (T)])
                if verbose :
                    print \
                        ("Created form %s for E_Type %s" % (f.id, T.type_name))
    # end def _create_auto_forms

    def _create_extra_forms (self, app_type) :
        for e in self._extras :
            e (app_type)
    # end def _create_extra_forms

# end class _Form_Cache_

Form_Cache = _Form_Cache_ ()

if __name__ != "__main__" :
    GTW.AFS.MOM._Export ("*")
### __END__ GTW.AFS.MOM.Form_Cache
