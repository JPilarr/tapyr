# -*- coding: utf-8 -*-
# Copyright (C) 2012-2014 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package TFL.
# 
# This module is licensed under the terms of the BSD 3-Clause License
# <http://www.c-tanzer.at/license/bsd_3c.html>.
# #*** </License> ***********************************************************#
#
#++
# Name
#    TFL.Command
#
# Purpose
#    Base class for an interactive command using CAO to define/process
#    arguments and options
#
# Revision Dates
#    17-May-2012 (CT) Creation
#    22-May-2012 (CT) Add `Sub_Command`, `app_dir`, and `app_path`
#    23-May-2012 (CT) Add `lib_dir`, `Sub_Command._handler_prefix`
#    24-May-2012 (CT) Add `_..._to_combine` to `_lists_to_combine`
#    25-May-2012 (CT) Add `sc_map` and `__getitem__`; add `_parent`
#    31-May-2012 (CT) Add `config_defaults`, define `Config` option in `opts`
#     1-Jun-2012 (CT) Fix `__doc__` in `_M_Command_.__new__`
#     1-Jun-2012 (CT) Add `Sub_Command_Combiner`
#     2-Jun-2012 (CT) Use `_TFL._Export_Module`, not `_TFL._Export`
#     2-Jun-2012 (CT) Factor `_Meta_Base_`, add `Option`
#     2-Jun-2012 (CT) Add `Config_Option`, remove `config_defaults`
#     3-Jun-2012 (CT) Sort `_opts_reified` by `rank`, fill `_opt_map`
#     3-Jun-2012 (CT) Factor `Rel_Path_Option`, add `Config_Dirs_Option`
#     3-Jun-2012 (CT) Add `Root_Command`
#     4-Jun-2012 (CT) Change `app_path` to use `root`
#    23-May-2013 (CT) Use `TFL.Meta.BaM` for Python-3 compatibility
#    16-Dec-2013 (CT) Factor `Rel_Path_Option._gen_base_dirs`
#    16-Dec-2013 (CT) Redefine `Config_Dirs_Option.base_dirs` to use
#                     `_defaults`, not `_base_dirs`
#    17-Dec-2013 (CT) Set `Config_Dirs_Option.type` to `False`
#    17-Dec-2013 (CT) Remove redefinition of `Config_Option.default`
#                     (resulted in double application of `base_dirs`)
#    17-Dec-2013 (CT) Improve $-expansion for `Rel_Path_Option.base_dirs`
#    18-Dec-2013 (CT) Add `abspath` to `app_dir`
#     2-Sep-2014 (CT) Change defaults to add `_init_kw` before
#                     `dynamic_defaults`
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division, print_function, unicode_literals

from   _TFL                   import TFL

from   _TFL.I18N              import _, _T, _Tn
from   _TFL.object_globals    import object_module
from   _TFL.predicate         import first, split_hst, uniq
from   _TFL.pyk               import pyk
from   _TFL                   import sos

import _TFL.Accessor
import _TFL.CAO
import _TFL._Meta.M_Auto_Combine
import _TFL._Meta.Object
import _TFL._Meta.Once_Property

from   itertools              import chain as ichain

class _Meta_Base_ (TFL.Meta.M_Auto_Combine) :

    def __new__ (mcls, name, bases, dct) :
        prefix = dct.get ("_rn_prefix") or first \
            (getattr (b, "_rn_prefix", None) for b in bases)
        if prefix and name.startswith (prefix) and "_real_name" not in dct :
            dct ["_real_name"] = name [len (prefix):]
        if "_name" not in dct :
            dct ["_name"] = dct.get ("_real_name", name).strip ("_").lower ()
        dct.setdefault ("is_partial", False)
        if not dct.get ("__doc__") :
            ### Find the right base to inherit doc-string from
            ### * must be an instance of `_Meta_Base_`
            ### * must contain a non-empty doc-string in its __dict__
            try :
                dct ["__doc__"] = first \
                    (  d for d in
                           (  b.__dict__.get ("__doc__") for b in bases
                           if isinstance (b, _Meta_Base_)
                           )
                    if d
                    )
            except LookupError :
                pass
        return mcls.__mc_super.__new__ (mcls, name, bases, dct)
    # end def __new__

# end class _Meta_Base_

class _M_Option_ (_Meta_Base_) :
    ### Meta class for `Option`.

    pass

# end class _M_Option_

class TFL_Option (TFL.Meta.BaM (TFL.Meta.Object, metaclass = _M_Option_)) :
    ### Base class for options of interactive commands.

    _real_name              = "Option"
    _rn_prefix              = "TFL_"

    cook              = None
    hide              = False
    max_number        = None
    range_delta       = 1
    rank              = 0
    type              = None

    _auto_split       = None
    _default          = None
    _defaults         = ()
    _name             = None

    _lists_to_combine = ("_defaults", )

    def __init__ (self, cmd) :
        if self.type is None :
            raise TypeError \
                ("%s::%s must define `type`" % (cmd, self.__class__.__name__))
        type = self.type
        if isinstance (type, pyk.string_types) :
            try :
                type = self.type = TFL.CAO.Opt.Table [type]
            except KeyError :
                type = self.type = getattr (TFL.CAO, type)
        self.cmd = cmd
    # end def __init__

    def __call__ (self) :
        result = self.type (** self.kw)
        return result
    # end def __call__

    @TFL.Meta.Once_Property
    def auto_split (self) :
        result = self._auto_split
        if result is None :
            result = self.type.auto_split
        return result
    # end def auto_split

    @TFL.Meta.Once_Property
    def default (self) :
        result = self._default
        if result is None and self._defaults :
            if self.auto_split :
                result = self.auto_split.join (self._defaults)
            else :
                raise TypeError \
                    ( "%s::%s has multiple defaults %s, but no `auto_split`"
                    % (cmd, self.__class__.__name__, self._defaults)
                    )
        return result
    # end def default

    @TFL.Meta.Once_Property
    def kw (self) :
        return dict \
            ( name            = self.name
            , default         = self.default
            , description     = self.__doc__
            , auto_split      = self.auto_split
            , max_number      = self.max_number
            , hide            = self.hide
            , range_delta     = self.range_delta
            , cook            = self.cook
            , rank            = self.rank
            )
    # end def kw

    @TFL.Meta.Once_Property
    def name (self) :
        return self._name or self.__class__.__name__.strip ("_").lower ()
    # end def name

Option = TFL_Option # end class

class TFL_Rel_Path_Option (Option) :

    auto_split              = ":"
    single_match            = False
    type                    = TFL.CAO.Rel_Path

    _base_dir               = None
    _base_dirs              = ("$app_dir", )

    @TFL.Meta.Once_Property
    def base_dirs (self) :
        result = tuple \
            (self._gen_base_dirs (self._base_dirs or (self._base_dir, )))
        return result
    # end def base_dirs

    @TFL.Meta.Once_Property
    def kw (self) :
        result = self.__super.kw
        if self.base_dirs :
            result ["_base_dirs"] = self.base_dirs
        result ["single_match"] = self.single_match
        return result
    # end def kw

    def _gen_base_dirs (self, bds) :
        for bd in bds :
            cwd = sos.getcwd ()
            if isinstance (bd, pyk.string_types) and bd.startswith ("$") :
                h, _, t = split_hst (bd, "/")
                h       = getattr (self.cmd, h [1:])
                if h == "" :
                    h   = cwd
                bd = "/".join ((h, t)) if t else h
            if bd is not None :
                yield bd
    # end def _gen_base_dirs

Rel_Path_Option = TFL_Rel_Path_Option # end class

class TFL_Config_Dirs_Option (Rel_Path_Option) :
    """Directories(s) considered for option files"""

    rank                    = -100
    type                    = False

    @TFL.Meta.Once_Property
    def base_dirs (self) :
        return tuple (self._gen_base_dirs (self._defaults or (self._default, )))
    # end def base_dirs

Config_Dirs_Option = TFL_Config_Dirs_Option # end class

class TFL_Config_Option (Rel_Path_Option) :
    """File(s) specifying defaults for options"""

    rank                    = -90

    type                    = TFL.CAO.Config

    _config_dirs_name       = "config_dirs"

    @TFL.Meta.Once_Property
    def base_dirs (self) :
        result  = self.__super.base_dirs
        opt_map = self.cmd._opt_map
        cdo     = opt_map.get (self._config_dirs_name)
        if cdo and cdo.base_dirs :
            result = cdo.base_dirs + result
        return tuple (uniq (result))
    # end def base_dirs

Config_Option = TFL_Config_Option # end class

class _M_Command_ (_Meta_Base_) :
    ### Meta class for `Command`

    def __new__ (mcls, name, bases, dct) :
        mcls._update_set (dct, _M_Command_, "_sub_commands")
        mcls._update_set (dct, _M_Option_,  "_opts_reified")
        return mcls.__mc_super.__new__ (mcls, name, bases, dct)
    # end def __new__

    @classmethod
    def _update_set (cls, dct, T, name) :
        dct [name] = _set = set (dct.get (name, ()))
        _set.update \
            (  v.__name__ for v in pyk.itervalues (dct)
            if isinstance (v, T) and not getattr (v, "is_partial", 0)
            )
    # end def _update_set

# end class _M_Command_

class TFL_Command (TFL.Meta.BaM (TFL.Meta.Object, metaclass = _M_Command_)) :
    ### Base class for interactive commands.

    _rn_prefix              = "TFL_"

    _dicts_to_combine       = ("_defaults", )
    _lists_to_combine       = \
        ( "_args", "_buns", "_opts"
        , "_dicts_to_combine", "_lists_to_combine", "_sets_to_combine"
        )
    _sets_to_combine        = ("_opts_reified", "_sub_commands")

    cmd_choice_name         = _ ("command")
    do_keywords             = False
    handler                 = None
    helper                  = None
    min_args                = 0
    max_args                = -1
    put_keywords            = False

    _args                   = ()
    _buns                   = ()
    _defaults               = {}
    _description            = ""
    _name                   = None
    _opts                   = ()
    _opts_reified           = set ()
    _root                   = None
    _sub_commands           = set ()

    def __init__ (self, _name = None, _parent = None, ** kw) :
        if _name is not None :
            self._name      = _name
        self._init_kw       = kw
        self._parent        = _parent
        if _parent is not None :
            self._root      = _parent._root or _parent
        self._cmd           = TFL.CAO.Cmd \
            ( args          = self.args
            , buns          = self.buns
            , defaults      = self.defaults
            , description   = self.description
            , do_keywords   = self.do_keywords
            , handler       = self.handler
            , helper        = self.helper
            , name          = self.name
            , max_args      = self.max_args
            , min_args      = self.min_args
            , opts          = self.opts
            , put_keywords  = self.put_keywords
            )
    # end def __init__

    def __call__ (self, _argv = None, ** _kw) :
        return self._cmd (_argv, ** _kw)
    # end def __call__

    @TFL.Meta.Once_Property
    def app_dir (self) :
        return sos.path.abspath (sos.path.dirname (self.app_path))
    # end def app_dir

    @TFL.Meta.Once_Property
    def app_path (self) :
        root = self._root or self
        return object_module (root).__file__
    # end def app_path

    @TFL.Meta.Once_Property
    def args (self) :
        if self._sub_commands :
            assert not self._args, \
                ( "Cannot specify both args %s and sub-commands %s"
                , (self._args, self._sub_commands)
                )
            name = _T (self.cmd_choice_name)
            scs  = tuple (sc._cmd for sc in self.sub_commands)
            return (TFL.CAO.Cmd_Choice (name, * scs), )
        else :
            return self._args
    # end def args

    @TFL.Meta.Once_Property
    def buns (self) :
        return self._buns
    # end def buns

    @TFL.Meta.Once_Property
    def defaults (self) :
        result = dict (self._defaults)
        result.update (self._init_kw)
        result.update (self.dynamic_defaults (result))
        return result
    # end def defaults

    @TFL.Meta.Once_Property
    def lib_dir (self) :
        return sos.path.dirname (sos.path.dirname (__file__))
    # end def lib_dir

    @TFL.Meta.Once_Property
    def description (self) :
        return self._description or self.__class__.__doc__
    # end def description

    @TFL.Meta.Once_Property
    def name (self) :
        if self._root :
            return self._name or self.__class__.__name__.strip ("_").lower ()
        else :
            return self.app_path
    # end def name

    @TFL.Meta.Once_Property
    def opts (self) :
        def _gen (self) :
            self._opt_map = map = {}
            for oc in sorted \
                    ( (  oc for oc in
                           (getattr (self, k) for k in self._opts_reified)
                      if oc is not None
                      )
                    , key = TFL.Getter.rank
                    ) :
                o = oc (self)
                map [o.name] = o
                if o.type :
                    yield o ()
        result = list (_gen (self))
        result.extend (self._opts)
        return tuple  (result)
    # end def opts

    @TFL.Meta.Once_Property
    def sc_map (self) :
        return dict ((sc.name, sc) for sc in self.sub_commands)
    # end def sc_map

    @TFL.Meta.Once_Property
    def sub_commands (self) :
        def _gen (self) :
            defaults = self.defaults
            for sc in self._sub_commands :
                if isinstance (sc, pyk.string_types) :
                    sc = getattr  (self, sc)
                if not isinstance (sc, TFL.CAO.Cmd) :
                    sc = sc (_parent = self, ** defaults)
                yield sc
        return tuple (_gen (self))
    # end def sub_commands

    def dynamic_defaults (self, defaults) :
        return {}
    # end def dynamic_defaults

    def __getitem__ (self, key) :
        if " " in key :
            result = self.sc_map
            for k in key.split (" ") :
                result = result [k]
        else :
            result = self.sc_map [key]
        return result
    # end def __getitem__

Command = TFL_Command # end class

class TFL_Sub_Command (Command) :
    ### Base class for sub-commands

    _real_name              = "Sub_Command"
    _handler_prefix         = ""

    def handler (self, cmd) :
        return self._handler (cmd)
    # end def handler

    @TFL.Meta.Once_Property
    def _handler (self) :
        handler_name = "".join (("_handle_", self._handler_prefix, self.name))
        return getattr (self._root, handler_name)
    # end def _handler

Sub_Command = TFL_Sub_Command # end class

class TFL_Sub_Command_Combiner (Command) :
    ### Base class for sub-commands that combine a number of other sub-commands

    _real_name              = "Sub_Command_Combiner"

    ### `_sub_command_seq` can't be auto-combined because a descendent might
    ### want a different sequence
    _sub_command_seq        = []

    @TFL.Meta.Once_Property
    def sub_command_seq (self) :
        def _gen (self) :
            for sc in self._sub_command_seq :
                if isinstance (sc, pyk.string_types) :
                    yield [sc]
                else :
                    yield sc
        return tuple (_gen (self))
    # end def sub_command_seq

    def handler (self, cmd) :
        opts   = self._std_opts (cmd)
        parent = self._parent
        for sc in self.sub_command_seq :
            parent (sc + opts)
    # end def handler

    def _std_opts (self, cmd) :
        result = []
        raws   = cmd._raw
        opts   = cmd._opt_dict
        for k, v in pyk.iteritems (cmd._map) :
            opt = opts.get (k)
            if opt :
                mk = "-" + k
                if k in raws :
                    result.extend ((mk, opt.auto_split.join (raws [k])))
                elif v and (not isinstance (v, list) or any (v)) :
                    result.append (mk)
        return result
    # end def _std_opts

Sub_Command_Combiner = TFL_Sub_Command_Combiner # end class

class TFL_Root_Command (Command) :
    ### Base class for root commands

    class TFL_Config_Dirs (Config_Dirs_Option) :
        """Directories(s) considered for option files."""

    Config_Dirs = TFL_Config_Dirs # end class

    class TFL_Config (Config_Option) :
        """File(s) specifying defaults for options."""

    Config = TFL_Config # end class

Root_Command = TFL_Root_Command # end class

if __name__ != "__main__" :
    TFL._Export_Module ()
### __END__ TFL.Command
