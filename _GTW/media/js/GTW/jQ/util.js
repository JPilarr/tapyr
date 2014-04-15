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
//    util
//
// Purpose
//    Utility functions for jQuery use
//
// Revision Dates
//    27-Jul-2011 (CT) Creation
//    18-Apr-2013 (CT) Add `alert` to `options.error`
//    29-Apr-2013 (CT) Move `gtw_externalize` and `fix_a_nospam` in here
//    20-Jan-2014 (CT) Pass `xhr_instance.responseText` to `show_message`;
//                     remove call of `alert` from `options.error`
//    15-Apr-2014 (CT) Put request info into `options.error` of `gtw_ajax_2json`
//    ««revision-date»»···
//--


( function ($) {
    "use strict";
    $.gtw_ajax_2json = function (opts, name) {
        var options  = $.extend
            ( { async       : false                  // defaults settings
              , timeout     : 30000
              , type        : "POST"
              }
            , opts                                   // arguments
            , { contentType : "application/json"     // mandatory settings
              , dataType    : "json"
              , processData : false
              }
            );
        var data = options.data;
        if (typeof data !== "string") {
            options.data = $GTW.jsonify (data);
        };
        if (! ("error" in options)) {
            options.error = function (xhr_instance, status, exc) {
                var msg = (name || "Ajax request") + " failed: ";
                $GTW.show_message
                    ( msg, status, exc
                    , "\n\nRequest:", options.type, options.url
                    , "\n\nResponse:", xhr_instance.responseText
                    );
            };
        };
        $.ajax (options);
    };
    $.fn.gtw_externalize = function () {
        this.click
            ( function (event) {
                  window.open (this.href).focus ();
                  if (event && "preventDefault" in event) {
                      event.preventDefault ();
                  };
              }
            ).addClass ("external");
        return this;
    };
    $GTW.update
        ( { fix_a_nospam   : function ($) {
                $("a.nospam").each (
                    function () {
                        var data = $(this).next ("b.nospam").attr ("title");
                        if (data != null) {
                            var aia = $GTW.as_int_array (data);
                            $(this).replaceWith
                                (String.fromCharCode.apply (null, aia));
                        };
                    }
                );
            }
          }
        );
  } (jQuery)
);

// __END__ util.js
