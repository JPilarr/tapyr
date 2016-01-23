// Copyright (C) 2016 Mag. Christian Tanzer All rights reserved
// Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
// #*** <License> ************************************************************#
// This module is licensed under the terms of the BSD 3-Clause License
// <http://www.c-tanzer.at/license/bsd_3c.html>.
// #*** </License> ***********************************************************#
//
//++
// Name
//    V5a/wrapped_remove_class.js
//
// Purpose
//    Vanilla javascript wrapper function removing a class
//    from all wrapped nodes
//
// Revision Dates
//    24-Jan-2016 (CT) Creation
//    ««revision-date»»···
//--

;
( function ($) {
    "use strict";

    $.$$.prototype.remove_class = function remove_class (class_spec) {
        this.for_each_arg
            (class_spec, function (el, name) { el.classList.remove (name); });
        return this;
    };
  } ($V5a)
);

// __END__ V5a/wrapped_remove_class.js
