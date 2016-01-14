// Copyright (C) 2016 Mag. Christian Tanzer All rights reserved
// Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
// #*** <License> ************************************************************#
// This module is licensed under the terms of the BSD 3-Clause License
// <http://www.c-tanzer.at/license/bsd_3c.html>.
// #*** </License> ***********************************************************#
//
//++
// Name
//    V5a/string_to_int_array.js
//
// Purpose
//    Vanilla javascript function converting a string to an array of ints
//
// Revision Dates
//    15-Jan-2016 (CT) Creation
//    ««revision-date»»···
//--

;
( function ($) {
    "use strict";

    $.string_to_int_array = function string_to_int_array (s) {
        var list   = s.split (",");
        var pat    = /^\s*\d+\s*([-+]\s*\d+)?\s*$/;
        var result = [];
        for (var i = 0, li = list.length, x; i < li; i+= 1) {
            x = list [i];
            if (x.match (pat)) {
                result.push (eval (x));
            };
        };
        return result;
    };
} ($V5a)
);

// __END__ V5a/string_to_int_array.js
