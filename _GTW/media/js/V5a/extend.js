// Copyright (C) 2016 Mag. Christian Tanzer All rights reserved
// Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
// #*** <License> ************************************************************#
// This module is licensed under the terms of the BSD 3-Clause License
// <http://www.c-tanzer.at/license/bsd_3c.html>.
// #*** </License> ***********************************************************#
//
//++
// Name
//    V5a/extend.js
//
// Purpose
//    Function to extend an object with the properties of other objects.
//
// Revision Dates
//    14-Jan-2016 (CT) Creation
//    ««revision-date»»···
//--

;
( function ($) {
    "use strict";

    $.extend = function extend (target) {
        var desc;
        for (var i = 1, li = arguments.length, src; i < li; i++) {
            src = arguments [i];
            for (var k in src) {
                desc = Object.getOwnPropertyDescriptor (src, k);
                if (  desc
                   && (! (desc.writable && desc.configurable && desc.enumerable)
                      || desc.get
                      || desc.set
                      )
                   ) {
                    delete target [k];
                    Object.defineProperty (target, k, desc);
               } else {
                    target [k] = src [k];
               };
            };
        };
        return target;
    };
  } ($V5a)
);

// __END__ V5a/extend.js
