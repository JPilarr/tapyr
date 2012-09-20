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
#    MOM.Graph.SVG
#
# Purpose
#    SVG renderer for MOM graphs
#
# Revision Dates
#    29-Aug-2012 (CT) Creation
#    31-Aug-2012 (RS) Add kludge to appease inkscape
#    31-Aug-2012 (CT) Put lipstick on the kludge (use `no_alpha`)
#    31-Aug-2012 (RS) Store `link_markers` in lowercase, fixes missing markers
#     5-Sep-2012 (CT) Move `label` to second segment of link if first is short
#    19-Sep-2012 (RS) Fix `view_box`: x, y, width, heigth
#    19-Sep-2012 (RS) Use `Arrow_Head_A` for `MOM:AM` marker
#    20-Sep-2012 (RS) Use `marker_width` and `marker_width` for scaling
#    ��revision-date�����
#--

from   __future__ import absolute_import, division, print_function, unicode_literals

from   _MOM                   import MOM
from   _TFL                   import TFL

import _MOM._Graph._Renderer_
import _MOM._Graph.Entity
import _MOM._Graph.Relation

from   _TFL.predicate         import pairwise
from   _TFL._SDG._XML._SVG    import SVG
from   _TFL._D2               import D2, Cardinal_Direction as CD

import _TFL._SDG._XML._SVG.Document
import _TFL._D2.Point
import _TFL._D2.Rect

import _TFL._Meta.Object
import _TFL._Meta.Once_Property

class Renderer (MOM.Graph._Renderer_) :
    """SVG renderer for MOM.Graph"""

    default_grid_scale = D2.Point ( 2,  3)
    encoding           = "utf-8"
    link_markers       = dict \
        ( attr         = dict (start = "MOM:AM")
        , is_a         = dict (end   = "MOM:IM")
        , role         = dict (start = "MOM:RM")
        )
    node_size          = D2.Point (160, 100)

    _Parameters        = None

    def __init__ (self, graph, ** kw) :
        self.pop_to_self (kw, "encoding")
        self.pop_to_self (kw, "Parameters", prefix = "_")
        self.__super.__init__ (graph, ** kw)
    # end def __init__

    @property
    def Parameters (self) :
        result = self._Parameters
        if result is None :
            from _MOM._Graph.SVG_Parameters import SVG_Parameters
            result = self._Parameters = SVG_Parameters ()
        return result
    # end def Parameters

    def Canvas (self, min_x, min_y, max_x, max_y) :
        P      = self.Parameters
        w, h   = (max_x - min_x, max_y - min_y)
        root   = SVG.Root \
            ( view_box    = "%d %d %d %d" % (min_x, min_y, w, h)
            , width       = "100%"
            )
        result = SVG.Document \
            ( root
            , encoding    = self.encoding
            , standalone  = False
            )
        defs = SVG.Defs \
            ( SVG.Marker.Arrow_Head_A
                ( elid           = "MOM:AM"
                , ref_x          = P.attr_marker_ref_x
                , marker_width   = P.attr_marker_size
                , marker_height  = P.attr_marker_size
                , stroke         = P.color.attr_link.no_alpha
                , stroke_opacity = P.color.attr_link.alpha
                , fill           = P.color.link_bg.no_alpha
                , fill_opacity   = P.color.link_bg.alpha
                )
            , SVG.Marker.Arrow_Head
                ( elid           = "MOM:IM"
                , ref_x          = P.is_a_marker_ref_x
                , marker_width   = P.is_a_marker_size
                , marker_height  = P.is_a_marker_size
                , stroke         = P.color.is_a_link.no_alpha
                , stroke_opacity = P.color.is_a_link.alpha
                )
            , SVG.Marker.Plug
                ( elid           = "MOM:RM"
                , stroke         = P.color.role_link.no_alpha
                , stroke_opacity = P.color.role_link.alpha
                )
            )
        result.add (defs)
        return result
    # end def Canvas

    def render (self) :
        self.__super.render ()
        return "\n".join (self.canvas.as_xml ())
    # end def render

    def render_link (self, link, canvas) :
        P    = self.Parameters
        rel  = link.relation
        grp  = SVG.Group \
            ( elid         = rel.rid
            , opacity      = P.link_opacity
            )
        lkind = link.relation.kind.lower ()
        kw   = dict \
            (   ("marker_%s" % (k, ), "url(#%s)" % (v, ))
            for k, v in self.link_markers.get (lkind, {}).iteritems ()
            )
        colr = getattr (P.color, "%s_link" % lkind)
        paid = "%s::path" % (rel.rid, )
        p, q = link.points [:2]
        p_q  = p - q
        anchor, off = "start", 10
        if max (abs (p_q)) < 5 * P.font_char_width and len (link.points) > 2 :
            p, q = link.points [1:3]
            p_q  = p - q
            off  = 2
        if p_q.x > 0 :
            p, q = q, p
            anchor, off = "end", 90
        offset = "%d%%" % off
        path   = SVG.Path \
            ( d            = (p, q)
            , elid         = paid
            , fill         = "none"
            , stroke       = "none"
            )
        grp.add \
            ( SVG.Title (rel.title)
            , SVG.Desc  (rel.desc)
            , SVG.Polyline
                ( fill           = "none"
                , points         = link.points
                , stroke         = colr.no_alpha
                , stroke_width   = P.link_stroke_width
                , stroke_opacity = colr.alpha
                , ** kw
                )
            , path
            , SVG.Text
                ( SVG.Text_Path
                    ( SVG.Tspan
                        (rel.label, dy = - P.font_char_width * 3 // 4)
                    , start_offset       = offset
                    , text_anchor        = anchor
                    , xlink_href         = "#%s" % paid
                    )
                , fill         = colr.no_alpha
                , fill_opacity = colr.alpha
                , font_family  = P.font_family
                , font_size    = P.font_size
                )
            # rel.info
            )
        if rel.info :
            grp.add  \
                ( SVG.Text
                    ( SVG.Text_Path
                        ( SVG.Tspan
                            (rel.info, dy = P.font_size)
                        , start_offset       = offset
                        , text_anchor        = anchor
                        , xlink_href         = "#%s" % paid
                        )
                    , fill         = colr.no_alpha
                    , fill_opacity = colr.alpha
                    , font_family  = P.font_family
                    , font_size    = P.font_size
                    )
                )
        canvas.add (grp)
    # end def render_link

    def _render_node (self, node, canvas) :
        P   = self.Parameters
        box = node.box
        grp = SVG.Group \
            ( elid         = node.entity.type_name
            , fill         = P.color.node_bg
            , opacity      = P.node_opacity
            )
        grp.add \
            ( SVG.Title (node.entity.title)
            , SVG.Desc  (node.entity.desc)
            , SVG.Rect
                ( x            = box.ref_point.x
                , y            = box.ref_point.y
                , width        = box.size.x
                , height       = box.size.y
                , stroke       = P.color.node_border
                , stroke_width = P.node_border_width
                )
            )
        self._render_node_labels (node, grp)
        canvas.add (grp)
    # end def _render_node

    def _render_node_labels (self, node, grp) :
        P      = self.Parameters
        box    = node.box
        tp     = box.ref_point + D2.Point (P.font_size // 2, 0)
        width  = int ((box.size.x - P.font_size) / P.font_char_width)
        height = box.size.y / P.line_height - 1
        def _label_parts (parts, width, height) :
            i = 0
            l = len (parts)
            x = ""
            while i < l and height > 0:
                p  = x + parts [i]
                i += 1
                while i < l and len (p) < width :
                    if len (p) + len (parts [i]) < width :
                        p += parts [i]
                        i += 1
                    else :
                        break
                yield p
                height -= 1
        txt = SVG.Text \
            ( x           = tp.x
            , y           = tp.y
            , fill        = P.color.text
            , font_family = P.font_family
            , font_size   = P.font_size
            )
        dx = 0
        for lp in _label_parts (node.entity.label_parts, width, height) :
            txt.add (SVG.Tspan (lp, x = tp.x, dx = dx, dy = P.line_height))
            dx = P.font_size // 2
        grp.add (txt)
    # end def _render_node_labels

# end class Renderer

if __name__ != "__main__" :
    MOM.Graph._Export_Module ()
### __END__ MOM.Graph.SVG
