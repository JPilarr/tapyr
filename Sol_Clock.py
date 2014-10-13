# -*- coding: utf-8 -*-
# Copyright (C) 2007-2014 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
#
# This module is licensed under the terms of the BSD 3-Clause License
# <http://www.c-tanzer.at/license/bsd_3c.html>.
# ****************************************************************************
#
#++
# Name
#    Sol_Clock
#
# Purpose
#    Display 24-hour clock showing sunrise, transit, sunset, and twilight
#
# Revision Dates
#    13-Nov-2007 (CT) Creation
#    14-Nov-2007 (CT) Creation continued
#    15-Nov-2007 (CT) Creation continued...
#    16-Nov-2007 (CT) Creation continued....
#    18-Nov-2007 (CT) `close_balloon` added
#     1-Jan-2008 (CT) `_balloon_show` changed to show length of day and
#                     transit height
#    16-Jun-2013 (CT) Use `TFL.CAO`, not `TFL.Command_Line`
#    ««revision-date»»···
#--

"""
Sol_Clock displays an analog clock (with a 24-hour face) showing the current
time, the times of sunrise, the sun's transit, and sunset, and the begin and
end of the civil, nautic, and astronomical twilight.
"""

from   _TFL                  import TFL
from   _CAL                  import CAL

from   _TFL.predicate        import pairwise
from   _TFL.Angle            import Angle_D, Angle_R
from   _TFL.pyk              import pyk

from   _TGL._TKT._Tk.CTK     import *

import _CAL.Date
import _CAL.Time
import _CAL._Sky.Location
import _CAL._Sky.Sun

import _TFL._Meta.Object
import _TFL.CAO
import _TFL.defaultdict

class Display (TFL.Meta.Object) :
    """Solar clock."""

    tag_colors   = dict \
        ( astro  = "#086FFF"
        , civil  = "#9CD8FC"
        , day    = "#D3F0FE"
        , grid   = "grey65"
        , hand   = "red"
        , nautic = "#5BC2FE"
        , night  = "#0005B1"
        )
    background   = "#BEBEBE"
    font_grid    = ("Arial",  8)
    font_time    = ("Arial", 13)
    label_color  = "white" # "grey30"
    pad_x        = 0
    pad_y        = 0
    period       = 1000 * 60 ### specified in milliseconds --> 1 minute

    def __init__ (self, master, date, location, size = 64, border = 5) :
        self.date     = date
        self.location = location
        self.balloon  = balloon = CTK.Balloon (master, arrow = False)
        balloon.body.configure (font = ("Arial", 8))
        self.canvas   = canvas  = CTK.Canvas \
            ( master
            , background         = self.background
            , highlightthickness = 0
            , name               = "clock"
            )
        b             = self.border = border
        bi            = size // 4
        self.size     = size
        self.rect     = rect = border, border, size - border, size - border
        self.rect2           = bi, bi, size - bi, size - bi
        CTK.Oval \
            ( canvas, rect
            , fill    = self.tag_colors ["night"]
            , outline = ""
            , width   = 0
            , tags    = "night"
            )
        self._setup_grid  (canvas, size, border, rect)
        self._display_rts (date, location, canvas, rect)
        canvas.configure  (height = size, width = size)
        CTK.Widget.bind   (canvas, "<Enter>",           self._balloon_show)
        CTK.Widget.bind   (canvas, "<Leave>",           self._balloon_hide)
        canvas.after      (self.period, self.update)
    # end def __init__

    def pack (self) :
        self.canvas.pack (padx = self.pad_x, pady = self.pad_y)
    # end def pack

    def update (self, event = None) :
        canvas = self.canvas
        date   = CAL.Date ()
        if date != self.date :
            self.date = date
            self._display_rts (date, self.location, canvas, self.rect)
        self._hand    (canvas)
        canvas.after  (self.period, self.update)
    # end def update

    def _arc (self, start, extent, tag, rect = None, tags = ("sol", )) :
        CTK.Arc \
            ( self.canvas, rect or self.rect
            , start              = start
            , extent             = extent
            , fill               = self.tag_colors [tag]
            , outline            = ""
            , width              = 0
            , tags               = (tag, ) + tags
            )
    # end def _arc

    def _balloon_show (self, event = None) :
        if event :
            widget  = event.widget
            r       = self.rts
            alt     = r.transit.altitude
            message = "\n".join \
                ( ( "%s %s %s        [%02d:%02d]"
                    % ( (self.location.name, self.date, self.time)
                      + (r.day_length).hh_mm
                      )
                  , ", ".join
                      ( ( "Sunrise : %s" % r.rise
                        , "transit : %s" % r.transit
                        , "sunset : %s"  % r.set
                        )
                      )
                  , "Rise    azimuth : %6.2f degrees" % r.rise.azimuth.degrees
                  , "Transit height  : %6.2f degrees" % alt.degrees
                  , "Set     azimuth : %6.2f degrees" % r.set.azimuth.degrees
                  , "Civil  twilight starts %s, ends %s"
                    % (r.civil_twilight_start, r.civil_twilight_finis)
                  , "Nautic twilight starts %s, ends %s"
                    % (r.nautic_twilight_start, r.nautic_twilight_finis)
                  , "Astro  twilight starts %s, ends %s"
                    % (r.astro_twilight_start, r.astro_twilight_finis)
                  )
                )
            x    = event.x_root - event.x
            y    = event.y_root - event.y
            offx = 0
            offy = 5
            if event.x_root > 200 :
                offx = -200
            if event.y_root > 100 :
                offy = -25
            self.balloon.activate \
                (widget, message, x = x, y = y, offx = offx, offy = offy)
    # end def _balloon_show

    def _balloon_hide (self, event = None) :
        self.balloon.deactivate ()
    # end def _balloon_hide

    def _display_rts (self, date, location, canvas, rect) :
        self.rts = rts = CAL.Sky.RTS_Sun.On_Day (date, location)
        canvas.delete ("sol")
        events = \
            [ rts.astro_twilight_start
            , rts.nautic_twilight_start
            , rts.civil_twilight_start
            , rts.rise
            , rts.set
            , rts.civil_twilight_finis
            , rts.nautic_twilight_finis
            , rts.astro_twilight_finis
            ]
        for (a, b), tag in zip \
            ( pairwise (events)
            , ("astro", "nautic", "civil", "day", "civil", "nautic", "astro")
            ) :
            x = 270 - a.time.as_degrees
            y = 270 - b.time.as_degrees
            self._arc (x, y - x, tag)
        self._raise_grid ()
        self._hand       (canvas)
    # end def _display_rts

    def _hand (self, canvas) :
        canvas.delete ("hand")
        hh, mm    = CAL.Time ().hh_mm
        hours     = 270 - (hh + mm / 60.) * 15
        minutes   =  90 - (mm * 6)
        self.time = time = "%02d:%02d" % (hh, mm)
        p         = self.size // 2
        self._arc (hours   - 5, + 10, "hand", self.rect2)
        self._arc (minutes - 2, +  5, "hand", self.rect)
        CTK.CanvasText \
            ( canvas, (p, p + 2)
            , anchor = N
            , fill   = self.label_color
            , font   = self.font_time
            , tags   = ("hand", )
            , text   = time
            )
    # end def _hand

    def _raise_grid (self) :
        self.canvas.tkraise ("grid")
    # end def _raise_grid

    def _setup_grid (self, canvas, size, border, rect) :
        a_size = size - 2 * border
        for i in range (0, 360, 90) :
            self._arc (i - 1, +2, "grid",  rect, ())
        self._setup_ticks \
            (canvas, size, border, pyk.range (0, 360, 45), a_size / 10., 25)
        self._setup_ticks \
            ( canvas, size, border
            , (i for i in pyk.range (0, 360, 15) if (i % 45) != 0)
            , a_size / 16., 20
            )
        if border >= 10 :
            self._setup_labels (canvas, size, border)
    # end def _setup_grid

    def _setup_labels (self, canvas, size, border) :
        r  = (size - border) / 2.0 + 3
        x0 = y0 = size / 2.0
        x_off   = TFL.defaultdict \
            (int, {0 :  2, 15 : 5, 18 : 4, 21 :  5})
        y_off   = TFL.defaultdict \
            (int, {0 : -4, 12 : 3, 15 : 2, 21 : -1})
        for i, anchor in zip \
                (range (0, 360, 45), (E, E, None, W, W, W, None, E)) :
            t   = Angle_D (i)
            h   = ((270 - i) // 15) % 24
            x   = x0 + r * t.cos + x_off [h]
            y   = y0 - r * t.sin + y_off [h]
            CTK.CanvasText \
                ( canvas, (x, y)
                , anchor = anchor
                , fill   = self.label_color
                , font   = ("Arial", 8)
                , text   = "%d" % (h, )
                )
    # end def _setup_labels

    def _setup_ticks (self, canvas, size, border, angles, arr_r, arr_t) :
        r  = (size - 2 * border) / 2.0 - arr_r
        x0 = y0 = size / 2.0
        for i in angles :
            t   = Angle_D (i)
            x   = x0 + r * t.cos
            y   = y0 + r * t.sin
            box = x - arr_r, y - arr_r, x + arr_r, y + arr_r
            self._arc (- i - arr_t, 2 * arr_t + 1, "grid", box, ())
    # end def _setup_ticks

# end class Display

class Toplevel (TFL.Meta.Object) :
    """Toplevel for solor clock."""

    background   = "grey70"
    relief       = CTK.RAISED

    class _TL_ (CTK.C_Toplevel) :
        widget_class = "Sol_Clock"

    def __init__ (self, date, location, size, border) :
        self.toplevel = toplevel = self._TL_ \
            ( bg                 = self.background
            , close_cmd          = self.close_balloon
            , destroy_cmd        = self.destroy
            , relief             = self.relief
            , title              = "Sol-Clock"
            )
        self.display  = display  = Display \
            (toplevel, date, location, size, border)
        display.pack ()
    # end def __init__

    def close_balloon (self, event = None) :
        self.display.balloon.deactivate ()
    # end def close_balloon

    def destroy (self, event = None) :
        self.toplevel.destroy ()
        try :
            CTK.root.destroy  ()
        except Exception as exc :
            pass
    # end def destroy

    def mainloop (self) :
        try :
            self.toplevel.mainloop ()
        except KeyboardInterrupt :
            pass
    # end def mainloop

# end class Toplevel

def _main (cmd) :
    date = CAL.Date.from_string (cmd.date)
    if cmd.latitude and cmd.longitude :
        location = CAL.Sky.Location \
            (cmd.latitude, cmd.longitude, cmd.location or None)
    else :
        location = CAL.Sky.Location.Table [cmd.location]
    Display.font_grid = (cmd.font, cmd.font_grid_size)
    Display.font_time = (cmd.font, cmd.font_time_size)
    a = Toplevel (date, location, cmd.size, cmd.border)
    if cmd.pos :
        a.toplevel.geometry (cmd.pos)
    CTK.root.withdraw ()
    a.mainloop ()
# end def _main

_Command = TFL.CAO.Cmd \
    ( handler       = _main
    , args          =
        ( "date:S=%s" % CAL.Date ()
        ,
        )
    , opts          =
        ( "border:I=14?Border around clock"
        , "font:S=Arial"
        , "font_grid_size:I=8"
        , "font_time_size:I=13"
        , "latitude:F?Latitude (north is positive)"
        , "location:S=Vienna?Location of observer"
        , "longitude:F?Longitude (negative is east of Greenwich)"
        , "pos:S?Position of display in geometry-format"
        , "size:I=100?Size of clock (square)"
        )
    , max_args      = 1
    )

if __name__ == "__main__":
    _Command ()
### __END__ Sol_Clock
