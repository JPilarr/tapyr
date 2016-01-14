// Copyright (C) 2016 Mag. Christian Tanzer All rights reserved
// Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
// #*** <License> ************************************************************#
// This module is licensed under the terms of the BSD 3-Clause License
// <http://www.c-tanzer.at/license/bsd_3c.html>.
// #*** </License> ***********************************************************#
//
//++
// Name
//    V5a/page_notifications.js
//
// Purpose
//    Vanilla javascript function supporting page notifications
//
// Revision Dates
//    17-Jan-2016 (CT) Creation
//    ««revision-date»»···
//--

;
( function ($) {
    "use strict";

    $.page_notifications = $.merge
        ( function page_notifications (opts) {
            var O = $.merge ({}, opts);
            var S = $.merge ({}, page_notifications.selectors, O ["selectors"]);
            var pn_els = $.query  (S.container);
            $.for_each
                ( pn_els
                , function (pn) {
                    var els = $.query (S.active_element, pn);
                    $.bind
                        ( els, "click"
                        , function pn_hide (ev) {
                            pn.style.display = "none";
                            $.prevent_default (ev);
                          }
                        );
                  }
                );
          }
        , { selectors :
              { active_element         : "label"
              , container              : ".page-notifications"
              }
          }
        );
  } ($V5a)
);

// __END__ V5a/page_notifications.js
