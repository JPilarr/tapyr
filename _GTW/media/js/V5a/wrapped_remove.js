// Copyright (C) 2016 Mag. Christian Tanzer All rights reserved
// Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
// #*** <License> ************************************************************#
// This module is licensed under the terms of the BSD 3-Clause License
// <http://www.c-tanzer.at/license/bsd_3c.html>.
// #*** </License> ***********************************************************#
//
//++
// Name
//    V5a/wrapped_remove.js
//
// Purpose
//    Remove all nodes of wrapped set from document
//
// Revision Dates
//    25-Jan-2016 (CT) Creation
//    ««revision-date»»···
//--

;
( function ($) {
    "use strict";

    $.$$.prototype.remove = function remove () {
        return this.for_each (function (n) { n.parentNode.removeChild (n) }; );
    };
  } ($V5a)
);

// __END__ V5a/wrapped_remove.js
