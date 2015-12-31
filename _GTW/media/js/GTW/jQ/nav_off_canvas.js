// Copyright (C) 2014-2015 Mag. Christian Tanzer All rights reserved
// Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
// #*** <License> ************************************************************#
// This script is licensed under the terms of the BSD 3-Clause License
// <http://www.c-tanzer.at/license/bsd_3c.html>.
// #*** </License> ***********************************************************#
//
//++
// Name
//    GTW/jQ/nav_off_canvas.js
//
// Purpose
//    jQuery plugin supporting off-canvas navigation
//
// Revision Dates
//    20-Feb-2014 (CT) Creation
//    31-Dec-2015 (CT) Use `nav_show$.children` to find nav-button
//    ««revision-date»»···
//--

;( function ($, undefined) {
    "use strict";

    $.fn.gtw_nav_off_canvas = function (opts) {
        var selectors = $.extend
            ( { button                   : "a"
              , container                : "[id=main]"
              }
            , opts && opts ["selectors"] || {}
            );
        var options  = $.extend
            ( { nav_off_class            : "nav-off-canvas"
              , nav_on_class             : "nav-on-canvas"
              }
            , opts || {}
            , { selectors : selectors
              }
            );
        $(this).each
            ( function () {
                  var S         = options.selectors;
                  var nav_show$ = $(this);
                  var b$, c$;
                  if (nav_show$.is (":visible")) {
                      b$ = nav_show$.children (S.button);
                      c$ = nav_show$.closest  (S.container);
                      b$.click
                        ( function nav_show_click (ev) {
                            var is_off = c$.hasClass (options.nav_off_class);
                            c$.toggleClass (options.nav_off_class, ! is_off);
                            c$.toggleClass (options.nav_on_class,    is_off);
                            return false;
                          }
                        )
                      c$.addClass    (options.nav_off_class);
                      c$.removeClass (options.nav_on_class);
                  };
              }
            );
        return this;
    }
  } (jQuery)
);

// __END__ GTW/jQ/nav_off_canvas.js
