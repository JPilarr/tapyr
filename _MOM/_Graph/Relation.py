# -*- coding: iso-8859-15 -*-
# Copyright (C) 2012 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package MOM.Graph.
#
# This module is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this module. If not, see <http://www.gnu.org/licenses/>.
# #*** </License> ***********************************************************#
#
#++
# Name
#    MOM.Graph.Relation
#
# Purpose
#    Model relations between MOM entities as displayed in a MOM.Graph
#
# Revision Dates
#    18-Aug-2012 (CT) Creation
#    21-Aug-2012 (CT) Add `info` and `label`
#    22-Aug-2012 (CT) Add `delta`, `reverse`, `set_connector`
#    26-Aug-2012 (CT) Add `add_guides`
#    29-Aug-2012 (CT) Add `desc` and `title`
#     3-Sep-2012 (CT) Add `side`, `source_side`, and `target_side`
#     3-Sep-2012 (CT) Add same-side support to `add_guides`
#     3-Sep-2012 (CT) Reify `Connector`, factor in `points_gen`, add `points`
#     5-Sep-2012 (CT) Add `shift_guide`, rename `add_guides` to `set_guides`
#    19-Sep-2012 (CT) Use `generic_role_name`, not `role_name`, for `Role.rid`
#    ��revision-date�����
#--

from   __future__  import absolute_import, division, print_function, unicode_literals

from   _MOM                   import MOM
from   _TFL                   import TFL

import _MOM.import_MOM
import _MOM._Graph

from   _TFL._D2               import D2, Cardinal_Direction as CD
from   _TFL.Math_Func         import sign

import _TFL.Decorator
import _TFL._Meta.Object
import _TFL._Meta.Once_Property

class Connector (TFL.Meta.Object) :
    """Connector of a relation to a node."""

    def __init__ (self, side, offset = None) :
        self.side   = side
        self.offset = offset
    # end def __init__

    def __getitem__ (self, index) :
        return (self.side, self.offset) [index]
    # end def __getitem__

    def __iter__ (self) :
        yield self.side
        yield self.offset
    # end def __iter__

    def __len__ (self) :
        return 2
    # end def __len__

    def __repr__ (self) :
        return "%s %s" % (self.__class__.__name__, tuple (self))
    # end def __repr__

    def __str__  (self) :
        return "%s" % (tuple (self), )
    # end def __str__

# end class Connector

class _R_Base_ (TFL.Meta.Object) :

    @TFL.Meta.Once_Property
    def guide_sort_key (self) :
        points = self.points
        p0     = points [ 0].free
        p      = points [ 1].free
        q      = points [-1].free
        p0_q   = p0 - q
        p_q    = p  - q
        side   = self.connector.side
        p0_q_y = getattr (p0_q, side.other_dim)
        p_q_x  = getattr (p_q,  side.dim)
        p_q_y  = getattr (p_q,  side.other_dim)
        result = (side.sort_sign * p0_q_y, abs (p_q_y), - p_q_x)
        return result
    # end def guide_sort

# end class _R_Base_

class _Reverse_ (_R_Base_) :
    """Reverse relation"""

    is_reverse        = True
    reverse           = None

    def __init__ (self, relation) :
        self.reverse = relation
    # end def __init__

    @TFL.Meta.Once_Property
    def delta (self) :
        return - self.reverse.delta
    # end def delta

    @property
    def connector (self) :
        return self.target_connector
    # end def connector

    @property
    def other_connector (self) :
        return self.reverse.source_connector
    # end def other_connector

    @property
    def points (self) :
        return self.reverse.points [::-1]
    # end def points

    @property
    def ref (self) :
        return self.reverse.target
    # end def pos

    @property
    def side (self) :
        return self.reverse.target_side
    # end def side

    def set_connector (self, connector) :
        assert self.reverse.target_connector is None
        self.reverse.target_connector = connector
    # end def set_connector

    def shift_guide (self, factor) :
        self.reverse.shift_guide (factor)
    # end def shift_guide

    def __getattr__ (self, name) :
        return getattr (self.reverse, name)
    # end def __getattr__

    def __repr__ (self) :
        return "<Graph.Reverse_Relation.%s %s.%s <- %s>" % \
            (self.kind, self.source.type_name, self.name, self.target.type_name)
    # end def __repr__

# end class _Reverse_

class _Relation_ (_R_Base_) :
    """Base class for relations between MOM entities."""

    guide_offset      = 0.25
    guides            = None
    info              = None
    is_reverse        = False
    source_connector  = None
    source_side       = None
    target_connector  = None
    target_side       = None

    _points           = None

    def __init__ (self, source, target, * args, ** kw) :
        self.pop_to_self (kw, "guide_offset", "source_side", "target_side")
        if kw :
            raise TypeError \
                ("Unknown arguments %s" % (sorted (kw.iteritems ())))
        self.source   = source
        self.target   = target
    # end def __init__

    @TFL.Meta.Once_Property
    def delta (self) :
        return self.source.pos - self.target.pos
    # end def delta

    @TFL.Meta.Once_Property
    def kind (self) :
        return self.__class__.__name__
    # end def kind

    @TFL.Meta.Once_Property
    def label (self) :
        return self.name
    # end def label

    @property
    def connector (self) :
        return self.source_connector
    # end def connector

    @property
    def other_connector (self) :
        return self.target_connector
    # end def other_connector

    @property
    def points (self) :
        if self.guides is not None :
            result = self._points
            if result is None :
                result = self._points = tuple (self.points_gen ())
            return result
    # end def points

    @property
    def ref (self) :
        return self.source
    # end def pos

    @TFL.Meta.Once_Property
    def reverse (self) :
        return _Reverse_ (self)
    # end def reverse

    @property
    def side (self) :
        return self.source_side
    # end def side

    def points_gen (self, head = None, tail = None, off_scale = 1) :
        if head is None :
            head = self.source.pos
        if tail is None :
            tail = self.target.pos
        guides = self.guides
        zero   = D2.Point (0, 0)
        yield head
        if guides :
            for g in guides :
                if len (g) == 3 :
                    wh, wt = g [:2]
                    offset = off_scale * g [-1]
                else :
                    wh, wt = g
                    offset = zero
                yield head * wh + tail * wt + offset
        yield tail
    # end def points_gen

    def set_connector (self, connector) :
        assert self.source_connector is None
        self.source_connector = connector
    # end def set_connector

    def set_guides (self) :
        src_c, trg_c = self.source_connector.side, self.target_connector.side
        dim          = src_c.dim
        delta        = self.delta
        guides       = self.guides = []
        g_offset     = self.guide_offset
        add          = guides.append
        self._points = None
        if src_c.is_opposite (trg_c) :
            if getattr (delta, src_c.other_dim) != 0 :
                p2_a = D2.Point (** {dim : 1})
                p2_b = D2.Point (* reversed (p2_a))
                off  = src_c.guide_offset (g_offset)
                add ((D2.Point (1, 1), D2.Point (0, 0), off))
                add ((p2_a,            p2_b,            off))
        elif src_c.side == trg_c.side :
            if getattr (delta, dim) == 0 :
                off  = src_c.guide_offset (g_offset)
                add ((D2.Point (1, 1), D2.Point (0, 0), off))
                add ((D2.Point (0, 0), D2.Point (1, 1), off))
        else :
            p2_a = src_c.guide_point (0)
            p2_b = D2.Point (* reversed (p2_a))
            add ((p2_a, p2_b))
    # end def set_guides

    def shift_guide (self, factor) :
        self.guide_offset = self.__class__.guide_offset * (factor + 1)
        self.set_guides ()
    # end def shift_guide

# end class _Relation_

class Attr (_Relation_) :
    """Model an attribute relation between MOM entities."""

    def __init__ (self, source, target, attr, ** kw) :
        self.attr   = attr
        self.name   = attr.name
        self.__super.__init__ (source, target, ** kw)
    # end def __init__

    @TFL.Meta.Once_Property
    def desc (self) :
        return self.attr.description
    # end def desc

    @TFL.Meta.Once_Property
    def info (self) :
        result = self.attr.kind
        if result :
            return "[%s]" % (result, )
    # end def info

    @TFL.Meta.Once_Property
    def rid (self) :
        return "%s.%s:%s" % \
            (self.source.type_name, self.name, self.target.type_name)
    # end def rid

    @TFL.Meta.Once_Property
    def title (self) :
        return "%s attribute %s" % (self.source.type_name, self.name)
    # end def title

    def __repr__ (self) :
        return "<Graph.Relation.%s %s.%s -> %s>" % \
            (self.kind, self.source.type_name, self.name, self.target.type_name)
    # end def __repr__

# end class Attr

class IS_A (_Relation_) :
    """Model an inheritance relation between MOM entities."""

    name = "IS_A"

    @TFL.Meta.Once_Property
    def desc (self) :
        return "%s is derived from %s" % \
            (self.source.type_name, self.target.type_name)
    # end def desc

    @TFL.Meta.Once_Property
    def rid (self) :
        return "%s:is_a:%s" % (self.source.type_name, self.target.type_name)
    # end def rid

    @TFL.Meta.Once_Property
    def title (self) :
        return "%s is-a %s" % (self.source.type_name, self.target.type_name)
    # end def desc

    def __repr__ (self) :
        return "<Graph.Relation %s IS A %s>" % \
            (self.source.type_name, self.target.type_name)
    # end def __repr__

# end class IS_A

class Role (Attr) :
    """Model a link role relation between MOM entities."""

    @TFL.Meta.Once_Property
    def info (self) :
        result = self.attr.max_links
        if result and result > 0 :
            return "0 .. %s" % (result, )
    # end def info

    @TFL.Meta.Once_Property
    def label (self) :
        return self.attr.generic_role_name
    # end def label

    @TFL.Meta.Once_Property
    def rid (self) :
        return "%s.%s:%s" % \
            ( self.source.type_name
            , self.attr.generic_role_name
            , self.target.type_name
            )
    # end def rid

    @TFL.Meta.Once_Property
    def title (self) :
        return "%s role %s" % (self.source.type_name, self.attr.role_name)
    # end def title

# end class Role

if __name__ != "__main__" :
    MOM.Graph._Export_Module ()
### __END__ MOM.Graph.Relation
