// Copyright (C) 2011-2014 Mag. Christian Tanzer All rights reserved
// Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
// #*** <License> ************************************************************#
// This software is licensed under the terms of either the
// MIT License or the GNU Affero General Public License (AGPL) Version 3.
// http://www.c-tanzer.at/license/mit_or_agpl.html
// #*** </License> ***********************************************************#
//
//++
// Name
//    GTW/jQ/hd_input.js
//
// Purpose
//    jQuery plugin to support input fields with display different from value
//
// Revision Dates
//    28-Nov-2011 (CT) Creation
//     7-Dec-2011 (CT) Change plugin name to `gtw_hd_input`
//     7-Mar-2012 (CT) Add `hidden`, set `disabled` of `hidden` to `false`, too
//    10-Apr-2013 (CT) Add and use `closing_flag`
//     3-May-2014 (CT) Add and use `trigger_event`, not hard-coded "focus"
//    ««revision-date»»···
//--

"use strict";

( function ($, undefined) {
    $.fn.gtw_hd_input = function (opts) {
        var self      = this;
        var selectors = $.extend
            ( { display       : ".value.display"
              , hidden        : ".value.hidden"
              }
            , opts && opts ["selectors"] || {}
            );
        var options   = $.extend
            ( { closing_flag  : "gtw_hd_input_closing"
              , trigger_event : "focus"
              }
            , opts || {}
            , { selectors     : selectors
              }
            );
        var display$ = $(selectors.display, this);
        var hidden$  = $(selectors.hidden,  this);
        if ("callback" in options) {
            display$.bind
                ( options.trigger_event
                , function hd_input_focus () {
                      var closing = self.data (options.closing_flag);
                      if (closing) {
                          return false;
                      } else {
                          return options.callback.apply (this, arguments);
                      };
                  }
                );
        }
        display$.prop ("disabled", false);
        hidden$.prop  ("disabled", false);
        return this;
    }
  } (jQuery)
);

// __END__ GTW/jQ/hd_input.js
