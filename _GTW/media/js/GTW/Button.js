/*
** Copyright (C) 2010 Martin Glueck All rights reserved
** Langstrasse 4, A--2244 Spannberg, Austria. martin@mangari.org
** ****************************************************************************
** This file is part of the library GTW.
**
** This module is licensed under the terms of the BSD 3-Clause License
** <http://www.c-tanzer.at/license/bsd_3c.html>.
** ****************************************************************************
**
**++
** Name
**    GTW_Button
**
** Purpose
**    Wrapper around the jQuery UI button to support two state buttons with
**    different icons for each state and some additional features.
**
** Revision Dates
**     9-May-2010 (MG) Creation
**    16-Jun-2010 (MG) Support for non icon buttons
**    ««revision-date»»···
**--
*/
(function ($)
{
  var _T;
  var _;
  var _Tn;

  if ($.I18N === undefined)
    {
      _T = _ = _Tn = function (t) { return t; }
    }
  else
    {
      _T = _ = $.I18N._T;
      _Tn    = $.I18N._Tn;
    }

  var GTW_Button =
    { _create : function ()
      {
        var O = this.options;
        if (O.states === undefined)
          {
            var state     = {};
            var attr_list = ["icon", "callback", "label"];
            for (var i = 0; i < attr_list.length; i++)
              state [attr_list [i]] = O [attr_list [i]];
            O.states        = [state];
            O.initial_state = 0;
          }
        O.state  = (O.initial_state || 0) - 1;
        if (O.state < 0) O.state = O.states.length - 1;
        this.element.data ("O", O);
        this.element.bind ("click", this, function (evt)
            {
              var self     = evt.data;
              self._update_icon (evt, true);
              return false;
            });
        this._update_icon (undefined, false);
      }
    , _update_icon : function (evt, trigger)
      {
          var O        = this.element.data ("O");
          var old_icon = O.states [O.state].icon;
          O.state     += 1;
          if (O.state >= O.states.length) O.state = 0;
          if (this.element.hasClass ("ui-icon"))
            {
              var new_icon = O.states [O.state].icon;
              this.element.removeClass (old_icon).addClass (new_icon);
            }
          if (trigger)
            {
              var callback = O.states [O.state].callback;
              callback (evt, O.data);
            }
      }
    };
  $.widget ("ui.GTW_Button", GTW_Button);
  $.extend
      ( $.ui.GTW_Form
      , { "version"      : "0.1"
        , "defaults"     :
          { group        : ""
          , states       : []
          }
        }
      )

})(jQuery);
