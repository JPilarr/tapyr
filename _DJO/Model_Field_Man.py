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
#    DJO.Model_Field_Man
#
# Purpose
#    Manager for the fields of a model
#
# Revision Dates
#    28-May-2009 (CT) Creation
#    29-May-2009 (CT) Creation continued
#    29-May-2009 (MG) `__getitem__` added
#     1-Jun-2009 (CT) `get` added
#     1-Jun-2009 (CT) Support for `real_name` added
#     1-Jun-2009 (MG) Special save handling added if `ledom` is created
#                     automatically
#     2-Jun-2009 (MG) `Own_O2O` added, setting of `_%_owned` added
#    ««revision-date»»···
#--

from   _TFL                               import TFL
import _TFL._Meta.M_Class
import _TFL.NO_List

from   _DJO                               import DJO
import _DJO.Model_Field                   as     MF

import itertools

def _sort_key (x) :
    return getattr (x, "sort_key", x.creation_counter)
# end def _sort_key

class Model_Field_Man (TFL.Meta.Object) :
    """Manager for the fields of a model.

       Allows convenient access to fields of related models, too.
    """

    _finalized = False
    _extension = []

    def __init__ (self, model) :
        self._extension.append     (self)
        self.All     = TFL.NO_List ()
        self.Own     = TFL.NO_List ()
        self.Own_O2O = TFL.NO_List ()
        self.model   = model
        self._rn_map = {}
    # end def __init__

    def finalize (self) :
        if self._finalized :
            return
        self._finalized = True
        All             = self.All
        Own             = self.Own
        model           = self.model
        fields          = itertools.chain \
            (model._meta.fields + model._meta.many_to_many)
        for f in sorted (fields, key = _sort_key) :
            if hasattr (f, "real_name") :
                self._rn_map [f.real_name] = f.name
            Own.append (f)
        for f in self.Own :
            if isinstance (f, MF.One_to_One) :
                self.Own_O2O.append (f)
                ledom = f.rel.to
                if not hasattr (ledom, "_F") :
                    DJO.M_Model.assimilate (ledom)
                else :
                    ledom._F.finalize  ()
                for g in ledom._F :
                    if g.name not in Own :
                        if hasattr (g, "real_name") :
                            self._rn_map [g.real_name] = g.name
                        All.append (g)
                        self._setup_delegated_field (model, ledom, f, g)
            else :
                All.append (f)
    # end def finalize

    @classmethod
    def finalize_all (cls, ** kw) :
        for mfm in cls._extension :
            mfm.finalize ()
    # end def finalize_all

    def get (self, key, default = None) :
        try :
            return self [key]
        except KeyError :
            return default
    # end def get

    def _setup_delegated_field (self, model, ledom, field, dleif) :
        def _get (this) :
            l = getattr (this, field.name, None)
            if l is not None :
                return getattr (l, dleif.name)
        def _set (this, value) :
            created = False
            try :
                l   = getattr (this, field.name, None)
            except ledom.DoesNotExist :
                l   = None
            if l is None :
                created = True
                l       = ledom ()
                setattr (this, field.name, l)
            if _get (this) != value :
                setattr (l, dleif.name, value)
                if created :
                    ### save the information that the `ledom` was created
                    ### automatically so that we can delete it automatically
                    ### as well
                    setattr (this, "_%s_owned" % (field.name, ), True)
                    def save () :
                        l.save ()
                        setattr (this, field.name, l)
                    # end def save
                else :
                    save = l.save
                if l not in this._save_callbacks :
                    this._save_callbacks [l] = save
        def _del (this) :
            l = getattr (this, field.name, None)
            if l is not None :
                setattr (l, dleif.name, dleif.Null)
        setattr \
            (model, dleif.name, property (_get, _set, _del, dleif.help_text))
    # end def _setup_delegated_field

    def __contains__ (self, key) :
        key = self._rn_map.get (key, key)
        return key in self.All
    # end def __contains__

    def __getattr__ (self, name) :
        try :
            return self [name]
        except KeyError :
            raise AttributeError, name
    # end def __getattr__

    def __getitem__ (self, key) :
        key = self._rn_map.get (key, key)
        try :
            return self.All [key]
        except KeyError :
            return self.Own [key]
    # end def __getitem__

    def __iter__ (self) :
        return iter (self.All)
    # end def __iter__

# end class Model_Field_Man

DJO.models_loaded_signal.connect (Model_Field_Man.finalize_all)

if __name__ != "__main__" :
    DJO._Export ("*")
### __END__ DJO.Model_Field_Man
