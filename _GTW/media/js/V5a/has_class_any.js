// Copyright (C) 2016 Mag. Christian Tanzer All rights reserved
// Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
// #*** <License> ************************************************************#
// This module is licensed under the terms of the BSD 3-Clause License
// <http://www.c-tanzer.at/license/bsd_3c.html>.
// #*** </License> ***********************************************************#
//
//++
// Name
//    V5a/has_class_any.js
//
// Purpose
//    Vanilla javascript functions testing if an element has any of classes
//
// Revision Dates
//    18-Jan-2016 (CT) Creation
//    ««revision-date»»···
//--

;
( function ($) {
    "use strict";

    $.has_class_any = function has_class_any (el, class_spec) {
        var classes    = $.arg_to_array (class_spec);
        var el_classes = el.classList;
        var result     = classes.some
            (function (name) { return el_classes.contains (name); });
        return result;
    };
  } ($V5a)
);

// __END__ V5a/has_class_any.js
