// Copyright (C) 2016 Mag. Christian Tanzer All rights reserved
// Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
// #*** <License> ************************************************************#
// This module is licensed under the terms of the BSD 3-Clause License
// <http://www.c-tanzer.at/license/bsd_3c.html>.
// #*** </License> ***********************************************************#
//
//++
// Name
//    V5a/history_test.js
//
// Purpose
//    Vanilla javascript function testing history support
//
// Revision Dates
//    20-Jan-2016 (CT) Creation
//    ««revision-date»»···
//--

;
( function ($) {
    "use strict";

    function test () {
        // copied from Modernizr
        // filters buggy-as-hell stock browser of old Android
        var ua = navigator.userAgent;
        if (  (  ua.indexOf ('Android 2.')  !== -1
              || ua.indexOf ('Android 4.0') !== -1
              )
           && ua.indexOf('Mobile Safari') !== -1
           && ua.indexOf('Chrome')        === -1
           && ua.indexOf('Windows Phone') === -1
           ) {
            return false;
        };
        return (window.history && 'pushState' in window.history);
    };
    $.supports.history = test ();
  } ($V5a)
);

// __END__ V5a/history_test.js
