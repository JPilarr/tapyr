// Copyright (C) 2016 Mag. Christian Tanzer All rights reserved
// Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
// #*** <License> ************************************************************#
// This module is licensed under the terms of the BSD 3-Clause License
// <http://www.c-tanzer.at/license/bsd_3c.html>.
// #*** </License> ***********************************************************#
//
//++
// Name
//    V5a/wrapped_insert_html.js
//
// Purpose
//    Insert html contents adjacent to all elements of wrapped set.
//
// Revision Dates
//    25-Jan-2016 (CT) Creation
//    ««revision-date»»···
//--

// https://developer.mozilla.org/en-US/docs/Web/API/Element/insertAdjacentHTML

;
( function ($) {
    "use strict";

    $.$$._iah = function _iah (p, h) {
        return this.for_each (function (n) { n.insertAdjacentHTML (p, h); });
    };

    $.$$.after = function after (htm) {
        return this._iah ("afterend", htm);
    };

    $.$$.append = function append (htm) {
        return this._iah ("beforeend", htm);
    };

    $.$$.before = function before (htm) {
        return this._iah ("beforebegin", htm);
    };

    $.$$.prepend = function prepend (htm) {
        return this._iah ("afterbegin", htm);
    };

  } ($V5a)
);

// __END__ V5a/wrapped_insert_html.js
