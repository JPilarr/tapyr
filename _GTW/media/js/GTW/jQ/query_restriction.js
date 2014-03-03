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
//    GTW/jQ/uery_restriction.js
//
// Purpose
//    jQuery plugin for a query restriction form
//
// Revision Dates
//    22-Nov-2011 (CT) Creation
//    23-Nov-2011 (CT) Creation continued (new_attr_filter, op_map_by_sym, ...)
//    24-Nov-2011 (CT) Creation continued (disabler_cb, submit_cb)
//    26-Nov-2011 (CT) Creation continued
//                     (setup_obj_list, GTW_buttonify, fix_buttons)
//    28-Nov-2011 (CT) Creation continued (order_by_cb, ...)
//    29-Nov-2011 (CT) Creation continued (order_by...)
//    30-Nov-2011 (CT) Creation continued (ev.delegateTarget)
//     5-Dec-2011 (CT) Creation continued (s/input/:input/ for selectors)
//     6-Dec-2011 (CT) Creation continued (use `gtw_ajax_2json`
//                     [qx_af_html_url, qx_obf_url],
//                     `active_menu_but_class`, `adjust_op_menu`)
//     7-Dec-2011 (CT) Creation continued (`response.callbacks`)
//     7-Dec-2011 (CT) Creation continued (reorganize `options`)
//    12-Dec-2011 (CT) Creation continued (start `setup_completer`)
//    13-Dec-2011 (CT) Creation continued (continue `setup_completer`)
//    15-Dec-2011 (CT) Creation continued (use `$GTW.UI_Icon_Map`,
//                     `.toggleClass`)
//    16-Dec-2011 (CT) Creation continued (factor e_type_selector.js)
//    22-Dec-2011 (CT) s/children/attrs/ (in `attr_filters`)
//    16-Jan-2012 (CT) Creation continued (`attr_select`)
//    17-Jan-2012 (CT) Creation continued (add `focus` to `op_select_cb`)
//    23-Feb-2012 (CT) Use `{ html: XXX }` as argument to `L`
//     8-Mar-2012 (CT) Add `options.completer_position`, `.dialog_position`,
//                     `.menu_position`, adjust positions of various popups
//    19-Mar-2012 (CT) Use `.ui-state-default` in parent of `.ui-icon`
//     5-Apr-2013 (CT) Adapt to API changes of jQueryUI 1.9+
//     5-Apr-2013 (CT) Add gtw-specific prefix to .`data` keys
//     9-Apr-2013 (CT) Add and use `new_menu_nested` for `attr_filters`
//     9-Apr-2013 (CT) Fix dialogs ("gtw_dialog_is_closing")
//    10-Apr-2013 (CT) Bind `beforeClose`, `close` events of `obf$.dialog` to
//                     `order_by.cb.before_close_cb`, `.cb.close_cb`;
//                     bind `cancel_button` to `ob_widget$.dialog("close")`
//    11-Apr-2013 (CT) Add `pred` to `new_menu_nested`
//    11-Apr-2013 (CT) DRY `toggle_disabled_state`, fix it for nested entries;
//                     fix `attr_select.prefill` call of `toggle` (`af.label`)
//    11-Apr-2013 (CT) Add polymorphic attributes to attribute filter menu
//    29-Apr-2013 (CT) Use `$GTW.show_message`, not `console.error`
//     2-Mar-2014 (CT) Protect recursion in `attr_filters.add`
//    ««revision-date»»···
//--

"use strict";

( function ($, undefined) {
    var L = $GTW.L;
    $.fn.gtw_query_restriction = function (qrs, opts) {
        var completer_position = $.extend
            ( { my         : "left top"
              , at         : "left bottom"
              }
            , opts && opts ["completer_position"] || {}
            );
        var dialog_position = $.extend
            ( { my         : "right top"
              , at         : "right bottom"
              }
            , opts && opts ["dialog_position"] || {}
            );
        var icons = new $GTW.UI_Icon_Map (opts && opts ["icon_map"] || {});
        var menu_position  = $.extend
            ( { my         : "right top"
              , at         : "left bottom"
              , collision  : "fit"
              }
            , opts && opts ["menu_position"] || {}
            );
        var selectors = $.extend
            ( { ascending                : ".asc"
              , attr_filter_container    : "tr"
              , attr_filter_disabler     : "td.disabler"
              , attr_filter_label        : "td.name label"
              , attr_filter_op           : "td.op a.button"
              , attr_filter_value        : "td :input.value"
              , attr_filter_value_entity : "td.value.Entity"
              , attrs_container          : "table.attrs"
              , descending               : ".desc"
              , disabled_button          : "button[class=disabled]"
              , disabler                 : ".disabler"
              , head_line                : "h1.headline"
              , limit                    : ":input[name=limit]"
              , object_container         : "table.Object-List"
              , offset                   : ":input[name=offset]"
              , order_by_criteria        : "ul.attributes"
              , order_by_criterion       : "li"
              , order_by_direction       : ".direction"
              , order_by_display         : ":input.value.display[id=QR-order_by]"
              , order_by_value           : ":input.value.hidden[name=order_by]"
              , prototype                : "ul.prototype li"
              , select_attr_attributes   : "ul.attributes"
              , select_attr_item         : "li"
              , select_attr_value        : ":input.value.hidden[name=fields]"
              , submit                   : "[type=submit]"
              }
            , icons.selectors
            , opts && opts ["selectors"] || {}
            );
        var ui_class = $.extend
            ( { active_menu_button    : "active-menu-button"
              , disable               : icons.ui_class ["DISABLE"]
              , enable                : icons.ui_class ["ENABLE"]
              , sort_asc              : icons.ui_class ["SORT_ASC"]
              , sort_desc             : icons.ui_class ["SORT_DESC"]
              }
            , opts && opts ["ui_class"] || {}
            );
        var options  = $.extend
            ( { obf_closing_flag    : "gtw_obf_dialog_closing"
              , treshold            : 0
              }
            , opts || {}
            , { completer_position  : completer_position
              , dialog_position     : dialog_position
              , icon_map            : icons
              , menu_position       : menu_position
              , selectors           : selectors
              , ui_class            : ui_class
              }
            );
        var qr$    = $(this);
        var body$  = $("body").last ();
        var af_map = {};
        var as_widget$, ob_widget$;
        var attr_filters =
            ( function () {
                var result = [];
                var name_sep = new RegExp (qrs.name_sep, "g");
                var add = function add (filters, prefix, ui_prefix) {
                    for (var i = 0, li = filters.length, f; i < li; i++) {
                        f = filters [i];
                        if (prefix) {
                            f.key   = prefix    + qrs.name_sep + f.name;
                            f.label = ui_prefix + qrs.ui_sep   + f.ui_name;
                        } else {
                            f.key   = f.name;
                            f.label = f.ui_name;
                        };
                        f.q_name          = f.key.replace (name_sep, ".");
                        f.ops_selected    = [];
                        af_map [f.label]  = f;
                        af_map [f.q_name] = f;
                        result.push (f);
                        if ("attrs" in f && f.attrs) {
                            add (f.attrs, f.key, f.label);
                        } else if ("children_np" in f) {
                            for ( var j = 0, lj = f.children_np.length, c
                                ; j < lj
                                ; j++
                                ) {
                                c = f.children_np [j];
                                if ("attrs" in c && c.attrs) {
                                    add ( c.attrs
                                        , f.key   + "[" + c.type_name    + "]"
                                        , f.label + "[" + c.ui_type_name + "]"
                                        );
                                };
                            };
                        };
                    };
                };
                if (qrs.filters) {
                    add (qrs.filters);
                };
                return result;
              } ()
            );
        var op_map_by_sym =
            ( function () {
                var result = {}, k, v, label;
                for (k in qrs.op_map) {
                    if (qrs.op_map.hasOwnProperty (k)) {
                        v              = qrs.op_map [k];
                        v.key          = k;
                        // if label contains stuff like `&ge;` we need to
                        // run it through `html` because we'll later want
                        // to look up `but$.html ()` in `op_map_by_sym`
                        //     Can't use `L`, because that keeps html-quotes
                        label          = $("<a>").append (v.label).html ();
                        result [v.sym] = v;
                        result [label] = v;
                    };
                };
                return result;
              } ()
            );
        var sig_map =
            ( function () {
                var result = {}, k, v;
                for (k in qrs.sig_map) {
                    if (qrs.sig_map.hasOwnProperty (k)) {
                        v = qrs.sig_map [k];
                        result [k] = $.map
                            ( v
                            , function (value) {
                                return qrs.op_map [value];
                              }
                            );
                    };
                };
                return result;
              } ()
            );
        var toggle_disabled_state = function toggle_disabled_state (menu$, choice, state) {
            var cl = choice.length;
            menu$.find ("a.button").each
                ( function () {
                    var a$         = $(this);
                    var c          = a$.data ("gtw_qr_choice");
                    var label      = c ? c.label : a$.html ();
                    var label_head = label.slice (0, cl);
                    var label_sep  = label [cl];
                    var match      =
                        (  (cl <= label.length)
                        && (!label_sep)
                        || (label_sep === "/")
                        );
                    if (match && (choice === label_head)) {
                        a$.toggleClass ("ui-state-disabled", state);
                    };
                  }
                );
        };
        var add_attr_filter_cb = function add_attr_filter_cb (ev) {
            var S       = options.selectors;
            var target$ = $(ev.delegateTarget);
            var choice  = target$.data ("gtw_qr_choice");
            var afs$    = $(S.attr_filter_container, qr$);
            var head$   = afs$.filter
                ( function () {
                    return $(this).attr ("title") <= choice.label;
                  }
                );
            var nf$ = new_attr_filter (choice);
            if (head$.length) {
                head$.last ().after  (nf$);
            } else if (afs$.length) {
                afs$.first ().before (nf$);
            } else {
                $(S.attrs_container).append (nf$);
            };
            $(S.attr_filter_value, nf$).focus ();
            setup_esf (nf$);
        };
        var adjust_op_menu = function adjust_op_menu (afs) {
            var menu$ = afs.ops_menu$;
            menu$.element.find ("a.button").each
                ( function () {
                    var a$    = $(this);
                    var label = a$.html ();
                    var map   = afs.ops_selected;
                    var op    = op_map_by_sym [label];
                    if (op) {
                        a$.toggleClass ("ui-state-disabled", !! map [op.sym]);
                    };
                  }
                );
        };
        var attach_menu = function attach_menu (but$, menu) {
            but$.click (menu_click_cb)
                .data  ("gtw_qr_menu$", menu);
        };
        var attr_select =
            { cb              :
                { add         : function add (ev) {
                      var S       = options.selectors;
                      var target$ = $(ev.delegateTarget);
                      var choice  = target$.data ("gtw_qr_choice").label;
                      var c$      = attr_select.new_attr (choice);
                      var but$    = as_widget$.find (S.add_button);
                      var menu$   = but$.data ("gtw_qr_menu$").element;
                      as_widget$.find    (S.select_attr_attributes).append (c$);
                      attr_select.toggle (menu$, choice, true);
                      as_widget$.find    (S.apply_button).focus ();
                  }
                , apply       : function apply (ev) {
                      var S      = options.selectors;
                      var attrs$ = as_widget$.find
                          (S.select_attr_attributes + " " + S.select_attr_item);
                      var values = [];
                      attrs$.each
                          ( function () {
                                var a$ = $(this);
                                var v$ = a$.find ("b");
                                if (! a$.hasClass ("disabled")) {
                                    var label = v$.html ();
                                    if (label) {
                                        var af = af_map [label];
                                        values.push (af.q_name);
                                    };
                                };
                            }
                          )
                      $(S.select_attr_value).val (values.join (", "));
                      attr_select.cb.close ();
                      qr$.find (S.apply_button).focus ();
                  }
                , clear       : function clear (ev, ui) {
                      var S = options.selectors;
                      var but$    = as_widget$.find (S.add_button);
                      var menu$   = but$.data ("gtw_qr_menu$").element;
                      as_widget$.find (S.select_attr_attributes).empty ();
                      menu$.find ("a.button").removeClass ("ui-state-disabled");
                  }
                , close       : function close (ev) {
                      as_widget$.dialog ("close");
                      attr_select.cb.clear ();
                  }
                , disabler    : function disabler (ev) {
                      var S        = options.selectors;
                      var target$  = $(ev.target);
                      var attr$    = target$.closest (S.select_attr_item);
                      var disabled = attr$.hasClass  ("disabled");
                      var but$     = as_widget$.find (S.add_button);
                      var menu$    = but$.data ("gtw_qr_menu$").element;
                      var choice   = attr$.find ("b").html ();
                      var title    = disabled ?
                          options.title.disabler : options.title.enabler;
                      attr$.toggleClass ("disabled", !disabled);
                      target$
                          .attr        ("title", title)
                          .toggleClass (options.ui_class.enable,  !disabled)
                          .toggleClass (options.ui_class.disable,  disabled);
                      attr_select.toggle (menu$, choice, disabled);
                      return false;
                  }
                , open        : function open (ev) {
                      var S       = options.selectors;
                      var target$ = $(ev.delegateTarget);
                      var li$     = target$.closest ("li");
                      var value$  = $(S.select_attr_value);
                      var val     = value$.val ();
                      var width   = qr$.width  ();
                      var dialog;
                      if (as_widget$ == null) {
                          as_widget$ = attr_select.setup_widget (target$);
                      };
                      attr_select.cb.clear ();
                      attr_select.prefill  (val ? val.split (",") : []);
                      as_widget$
                          .dialog
                              ( "option"
                              , { dialogClass : "no-close"
                                , width       : "auto"
                                }
                              )
                          .dialog ("open")
                          .dialog ("widget")
                              .position
                                  ( $.extend
                                      ( {}
                                      , options.dialog_position
                                      , { of : target$ }
                                      )
                                  );
                  }
                }
            , new_attr          : function new_attr (label) {
                  var S      = options.selectors;
                  var result = as_widget$.find (S.prototype).clone (true);
                  var dir$;
                  result.find ("b").html (label);
                  return result;
              }
            , prefill           : function prefill (choices) {
                  var S       = options.selectors;
                  var attrs$  = as_widget$.find (S.select_attr_attributes);
                  var but$    = as_widget$.find (S.add_button);
                  var menu$   = but$.data ("gtw_qr_menu$").element;
                  var af, a$;
                  for (var i = 0, li = choices.length, choice; i < li; i++) {
                      choice = $.trim (choices [i]);
                      if (choice.length) {
                          af = af_map [choice];
                          a$ = attr_select.new_attr (af.label);
                          attrs$.append (a$);
                          attr_select.toggle (menu$, af.label, true);
                      };
                  };
              }
            , setup             : function setup () {
                  $(this).click (attr_select.cb.open);
              }
            , setup_widget      : function setup_widget (but$) {
                  var S      = options.selectors;
                  var saf$   = options ["select_attr_form_html"];
                  var result;
                  if (! saf$) {
                      $.gtw_ajax_2json
                          ( { async       : false
                            , success     : function (response, status) {
                                if (! response ["error"]) {
                                    if ("html" in response) {
                                        saf$ = $(response.html);
                                        options.select_attr_form_html = saf$;
                                    } else {
                                        $GTW.show_message
                                            ("Ajax Error", response);
                                    };
                                } else {
                                  $GTW.show_message
                                      ("Ajax Error", response.error);
                                }
                              }
                            , url         : options.url.qx_asf
                            }
                          );
                      if (! saf$) {
                          return;
                      };
                  };
                  result = saf$.dialog
                      ( { dialogClass : "no-close"
                        , autoOpen    : false
                        , title       : saf$.attr ("title")
                        , width       : "auto"
                        }
                      );
                  result.find (S.prototype)
                      .attr ("title", options.title.select_attr_sortable);
                  result.find (S.select_attr_attributes).sortable
                      ( { close       : attr_select.cb.clear
                        , distance    : 5
                        , placeholder : "ui-state-highlight"
                        }
                      );
                  result.find (S.button)
                      .gtw_buttonify (icons, options.buttonify_options);
                  result.find (S.add_button)
                      .each
                          ( function () {
                              var but$ = $(this);
                              attach_menu
                                ( but$
                                , new_menu_nested
                                    (qrs.filters, attr_select.cb.add)
                                );
                            }
                          );
                  result.find (S.apply_button).click  (attr_select.cb.apply);
                  result.find (S.cancel_button).click (attr_select.cb.close);
                  result.find (S.clear_button).click  (attr_select.cb.clear);
                  result.find (S.disabler)
                      .addClass ("ui-icon " + options.ui_class.disable)
                      .attr     ("title", options.title.disabler)
                      .click    (attr_select.cb.disabler)
                      .parent   ().addClass ("ui-state-default");
                  return result;
              }
            , toggle         : toggle_disabled_state
            };
        var disabler_cb = function disabler_cb (ev) {
            var S        = options.selectors;
            var afc$     = $(ev.target).closest (S.attr_filter_container);
            var dis$     = $(S.attr_filter_disabler, afc$);
            var but$     = dis$.find (".button");
            var val$     = $(S.attr_filter_value, afc$);
            var disabled = val$.prop ("disabled");
            var title    = disabled ?
                options.title.disabler : options.title.enabler;
            afc$.toggleClass ("ui-state-disabled",     !disabled);
            but$.toggleClass (options.ui_class.enable, !disabled)
                .toggleClass (options.ui_class.disable, disabled);
            dis$.attr    ("title", title);
            val$.prop    ("disabled", !disabled);
            return false;
        };
        var fix_buttons = function fix_buttons (buttons) {
            var S = options.selectors;
            var name, sel, value, old$, new$;
            for (name in buttons) {
                if (buttons.hasOwnProperty (name)) {
                    value = buttons [name];
                    sel   = S.add_button.replace ("ADD", name);
                    old$  = $(sel);
                    new$  = $(value);
                    old$.replaceWith (new$);
                };
            };
            $(S.button).gtw_buttonify (icons, options.buttonify_options);
        };
        var hide_menu_cb = function hide_menu_cb (ev) {
            var menu$ = $(".drop-menu"), tc;
            if (menu$.is (":visible")) {
                tc = $(ev.target).closest (".drop-menu");
                if (ev.keyCode === $.ui.keyCode.ESCAPE || ! tc.length) {
                    menu$.hide ();
                    $("." + options.ui_class.active_menu_button)
                        .removeClass (options.ui_class.active_menu_button);
                };
            };
        };
        var menu_click_cb = function menu_click_cb (ev) {
            var but$ = $(ev.delegateTarget);
            var menu = but$.data ("gtw_qr_menu$");
            var opts = menu.element.data ("gtw_qr_options");
            if (menu.element.is (":visible")) {
                menu.element.hide ();
                but$.removeClass (options.ui_class.active_menu_button);
            } else {
                hide_menu_cb (ev); // hide other open menus, if any
                if (opts && "open" in opts) {
                    opts.open (ev, menu);
                };
                menu.element
                    .show ()
                    .position
                      ( $.extend
                          ( options.menu_position
                          , opts && opts ["position"] || {}
                          , { of : but$ }
                          )
                      )
                    .zIndex (but$.zIndex () + 1)
                    .focus  ();
                but$.addClass (options.ui_class.active_menu_button);
                if (ev && "stopPropagation" in ev) {
                    ev.stopPropagation ();
                };
            };
        };
        var menu_select_cb = function menu_select_cb (ev) {
            var target$ = $(ev.delegateTarget);
            var menu$   = target$.closest (".cmd-menu");
            target$.data ("gtw_qr_callback") (ev);
            $("."+options.ui_class.active_menu_button)
                .removeClass (options.ui_class.active_menu_button);
            menu$.hide ();
        };
        var new_attr_filter = function new_attr_filter (choice) {
            var S = options.selectors;
            var op  = op_map_by_sym ["=="] ; // last-op ???
            var key = choice.key + qrs.op_sep + op.key;
            var ajx = false;
            if (! ("attr_filter_html" in choice)) {
                $.gtw_ajax_2json
                    ( { async       : false
                      , data        :
                          { key     : key
                          }
                      , success     : function (response, status) {
                            if (! response ["error"]) {
                                if ("html" in response) {
                                  choice.attr_filter_html = $(response.html);
                                  choice.attr_filter_html
                                      .find (S.attr_filter_disabler)
                                          .each (setup_disabler);
                                  ajx = true;
                                } else {
                                  $GTW.show_message ("Ajax Error", response);
                                }
                            } else {
                                $GTW.show_message
                                    ("Ajax Error", response.error);
                            };
                        }
                      , url         : options.url.qx_af_html
                      }
                    , "Attribute filter"
                    );
                if (!ajx) {
                  return;
                };
            };
            var result = choice.attr_filter_html
                .clone (true)
                .data ("gtw_qr_choice", choice);
            update_attr_filter_op (result, op, key);
            $(S.attr_filter_op, result).each (setup_op_button);
            return result;
        };
        var new_menu__add = function new_menu__add (choice, menu, cb, off) {
            var label  = choice.label.substr (off || 0);
            var entry  = $(L ("a.button", { html : label }));
            var result = $(L ("li"));
            entry
                .click (menu_select_cb)
                .data  ({ gtw_qr_callback : cb, gtw_qr_choice : choice});
            result.append (entry);
            menu.append (result);
            return result;
        };
        var new_menu__add_nested = function new_menu__add_nested (choice, menu, cb, off, pred, icnp) {
            var label  = choice.label.substr (off || 0);
            var offs   = choice.label.length + qrs.ui_sep.length;
            var sub, tail = "", treshold = 2;
            if (pred (choice)) {
                new_menu__add (choice, menu, cb, off);
                tail     = "/...";
                treshold = 3;
            };
            if ("attrs" in choice) {
                if (choice.attrs.length > treshold) {
                    sub = $(L ("li")).append
                        ( $(L ("a.button", { html : label + tail })));
                    menu.append (sub);
                    new_menu__add_sub (choice.attrs, sub, cb, offs, pred, icnp);
                } else {
                    for (var j = 0, lj = choice.attrs.length; j < lj; j++) {
                        new_menu__add_nested
                            (choice.attrs [j], menu, cb, off, pred, icnp);
                    };
                };
            } else if (icnp && "children_np" in choice) {
                sub = $(L ("li")).append
                    ( $(L ("a.button", { html : label + tail })));
                menu.append (sub);
                new_menu__add_sub_cnp
                        (choice.children_np, sub, cb, offs, pred);
            };
        };
        var new_menu__add_sub = function new_menu__add_sub (choices, menu, cb, off, pred, icnp) {
            var sub_menu = $(L ("ul"));
            menu.append (sub_menu);
            for (var i = 0, li = choices.length; i < li; i++) {
                new_menu__add_nested
                    (choices [i], sub_menu, cb, off, pred, icnp);
            };
        };
        var new_menu__add_sub_cnp = function new_menu__add_sub_cnp (children_np, menu, cb, off, pred) {
            var sub_menu = $(L ("ul"));
            var etn, offs, typ_menu, typ;
            menu.append (sub_menu);
            for (var i = 0, li = children_np.length; i < li; i++) {
                typ  = children_np [i];
                etn  = "[" + typ.ui_type_name + "]";
                offs = off + etn.length;
                typ_menu = $(L ("li")).append
                    ( $(L ("a.button", { html : etn })));
                sub_menu.append (typ_menu);
                new_menu__add_sub (typ.attrs, typ_menu, cb, offs, pred, true);
            };
        };
        var new_menu__create = function new_menu__create (options) {
            var result = $(L ("ul.drop-menu.cmd-menu"));
            result.data ({ gtw_qr_options : options });
            return result;
        };
        var new_menu__finish = function new_menu__finish (menu) {
            var result = menu
                .menu     ({})
                .appendTo (body$)
                .css      ({ top: 0, left: 0, position : "absolute" })
                .hide     ()
                .data     ("ui-menu");
            return result;
        };
        var new_menu = function new_menu (choices, cb, kw) {
            var opts = (kw && "opts" in kw) ? kw.opts : {};
            var menu = new_menu__create (opts);
            for (var i = 0, li = choices.length; i < li; i++) {
                new_menu__add (choices [i], menu, cb, 0);
            };
            return new_menu__finish (menu);
        };
        var new_menu_nested = function new_menu_nested (choices, cb, kw) {
            var pred = (kw && "pred" in kw) ? kw.pred
                         : function () { return true; };
            var icnp = (kw && "icnp" in kw) ? kw.icnp : false;
            var opts = (kw && "opts" in kw) ? kw.opts : {};
            var menu = new_menu__create (opts);
            menu.addClass ("nested");
            for (var i = 0, li = choices.length; i < li; i++) {
                new_menu__add_nested (choices [i], menu, cb, 0, pred, icnp);
            };
            return new_menu__finish (menu);
        };
        var op_select_cb = function op_select_cb (ev) {
            var S       = options.selectors;
            var target$ = $(ev.delegateTarget);
            var choice  = target$.data ("gtw_qr_choice");
            var but$    = $("."+options.ui_class.active_menu_button).first ();
            var afc$    = but$.closest (S.attr_filter_container);
            var val$  = $(S.attr_filter_value, afc$);
            var name    = val$.attr ("name");
            var prefix  = name.split  (qrs.op_sep) [0];
            var key     = prefix + qrs.op_sep + choice.key;
            update_attr_filter_op (afc$, choice, key);
            setTimeout
                ( function () {
                    $(S.attr_filter_value, afc$).focus ();
                  }
                , 1
                );
        };
        var order_by =
            { cb              :
                { add_criterion : function add_criterion (ev) {
                      var S       = options.selectors;
                      var target$ = $(ev.delegateTarget);
                      var choice  = target$.data ("gtw_qr_choice").label;
                      var c$      = order_by.new_criterion (choice);
                      var but$    = ob_widget$.find (S.add_button);
                      var menu$   = but$.data ("gtw_qr_menu$").element;
                      ob_widget$.find (S.order_by_criteria).append (c$);
                      order_by.toggle_criteria (menu$, choice, true);
                      ob_widget$.find (S.apply_button).focus ();
                  }
                , apply         : function apply (ev) {
                      var S     = options.selectors;
                      var crit$ = ob_widget$.find
                          (S.order_by_criteria + " " + S.order_by_criterion);
                      var displays = [], values = [];
                      crit$.each
                          ( function () {
                                var c$ = $(this);
                                var v$ = c$.find ("b");
                                if (! c$.hasClass ("disabled")) {
                                    var dir$  = c$.find (S.order_by_direction);
                                    var label = v$.html ();
                                    if (label) {
                                        var desc  = dir$.hasClass
                                            (options.ui_class.sort_desc);
                                        var sign  = desc ? "-" : "";
                                        var af    = af_map [label];
                                        displays.push (sign + label);
                                        values.push   (sign + af.q_name);
                                    };
                                };
                            }
                          )
                      $(S.order_by_display).val (displays.join (", "));
                      $(S.order_by_value)  .val (values.join   (", "));
                      ob_widget$.dialog ("close");
                      qr$.find (S.apply_button).focus ();
                  }
                , before_close  : function before_close (ev) {
                      var hdi$ = order_by.hd_input$;
                      if (hdi$) {
                          hdi$.data (options.obf_closing_flag, true);
                      };
                  }
                , clear         : function clear (ev, ui) {
                      var S = options.selectors;
                      var but$    = ob_widget$.find (S.add_button);
                      var menu$   = but$.data ("gtw_qr_menu$").element;
                      ob_widget$.find (S.order_by_criteria).empty ();
                      menu$.find ("a.button").removeClass ("ui-state-disabled");
                  }
                , close         : function close (ev) {
                      var hdi$ = order_by.hd_input$;
                      if (hdi$) {
                          hdi$.removeData (options.obf_closing_flag);
                      };
                  }
                , dir           : function dir (ev) {
                      var S        = options.selectors;
                      var target$  = $(ev.target);
                      var crit$    = target$.closest (S.order_by_criterion);
                      var dir$     = crit$.find (S.order_by_direction);
                      order_by.toggle_dir (dir$);
                  }
                , disabler      : function disabler (ev) {
                      var S        = options.selectors;
                      var target$  = $(ev.target);
                      var crit$    = target$.closest (S.order_by_criterion);
                      var disabled = crit$.hasClass ("disabled");
                      var but$     = ob_widget$.find (S.add_button);
                      var menu$    = but$.data ("gtw_qr_menu$").element;
                      var choice   = crit$.find ("b").html ();
                      var title    = disabled ?
                          options.title.disabler : options.title.enabler;
                      crit$.toggleClass ("disabled", !disabled);
                      target$
                          .attr        ("title", title)
                          .toggleClass (options.ui_class.enable,  !disabled)
                          .toggleClass (options.ui_class.disable,  disabled);
                      order_by.toggle_criteria (menu$, choice, disabled);
                      return false;
                  }
                , open          : function open (ev) {
                      var S       = options.selectors;
                      var target$ = $(ev.delegateTarget);
                      var li$     = target$.closest ("li");
                      var obw$    = ob_widget$;
                      var width   = qr$.width ();
                      if (obw$ == null) {
                          ob_widget$ = obw$ = order_by.setup_widget (target$);
                      };
                      order_by.cb.clear ();
                      order_by.prefill  (target$.val ().split (","));
                      obw$.dialog ("option", "width", "auto")
                          .dialog ("open")
                          .dialog ("widget")
                              .position
                                  ( $.extend
                                      ( {}
                                      , options.dialog_position
                                      , { of : target$ }
                                      )
                                  );
                  }
                }
            , new_criterion     : function new_criterion (label, desc) {
                  var S      = options.selectors;
                  var result = ob_widget$.find (S.prototype).clone (true);
                  var dir$;
                  result.find ("b").html (label);
                  if (desc) {
                      dir$ = result.find (S.order_by_direction);
                      order_by.toggle_dir (dir$);
                  };
                  return result;
              }
            , prefill           : function prefill (choices) {
                  var S       = options.selectors;
                  var crits$  = ob_widget$.find (S.order_by_criteria);
                  var but$    = ob_widget$.find (S.add_button);
                  var menu$   = but$.data ("gtw_qr_menu$").element;
                  var c$, desc;
                  for (var i = 0, li = choices.length, choice; i < li; i++) {
                      choice = $.trim (choices [i]);
                      if (choice.length) {
                          desc = false;
                          if (choice [0] === "-") {
                              desc = true;
                              choice = choice.slice (1);
                          }
                          c$ = order_by.new_criterion (choice, desc);
                          crits$.append (c$);
                          order_by.toggle_criteria (menu$, choice, true);
                      };
                  };
              }
            , setup             : function setup () {
                  var li$ = $(this).closest ("li");
                  order_by.hd_input$ = li$;
                  li$.gtw_hd_input
                      ( { callback     : order_by.cb.open
                        , closing_flag : options.obf_closing_flag
                        }
                      );
              }
            , setup_widget      : function setup_widget (but$) {
                  var S      = options.selectors;
                  var obf$   = options ["order_by_form_html"];
                  var result;
                  if (! obf$) {
                      $.gtw_ajax_2json
                          ( { async       : false
                            , success     : function (response, status) {
                                if (! response ["error"]) {
                                    if ("html" in response) {
                                        obf$ = $(response.html);
                                        options.order_by_form_html = obf$;
                                    } else {
                                        $GTW.show_message
                                            ("Ajax Error", response);
                                    };
                                } else {
                                  $GTW.show_message
                                      ("Ajax Error", response.error);
                                }
                              }
                            , url         : options.url.qx_obf
                            }
                          );
                      if (! obf$) {
                          return;
                      };
                  };
                  result = obf$.dialog
                      ( { autoOpen    : false
                        , beforeClose : order_by.cb.before_close
                        , close       : order_by.cb.close
                        , title       : obf$.attr ("title")
                        }
                      );
                  result.find (S.prototype)
                      .attr ("title", options.title.order_by_sortable);
                  result.find (S.order_by_criteria).sortable
                      ( { close       : order_by.cb.clear
                        , distance    : 5
                        , placeholder : "ui-state-highlight"
                        }
                      );
                  result.find (S.button)
                      .gtw_buttonify (icons, options.buttonify_options);
                  result.find (S.add_button)
                      .each
                          ( function () {
                              var but$ = $(this);
                              attach_menu
                                ( but$
                                , new_menu_nested
                                    (qrs.filters, order_by.cb.add_criterion)
                                );
                            }
                          );
                  result.find (S.apply_button).click  (order_by.cb.apply);
                  result.find (S.cancel_button).click
                    ( function () {
                          return ob_widget$.dialog ("close");
                      }
                    );
                  result.find (S.clear_button).click  (order_by.cb.clear);
                  result.find (S.order_by_direction)
                      .addClass ("ui-icon " + options.ui_class.sort_asc)
                      .attr     ("title", options.title.order_by_asc)
                      .parent   ().addClass ("ui-state-default");
                  result.find (S.disabler)
                      .addClass ("ui-icon " + options.ui_class.disable)
                      .attr     ("title", options.title.disabler)
                      .click    (order_by.cb.disabler)
                      .parent   ().addClass ("ui-state-default");
                  result.delegate
                      (S.order_by_criterion, "click", order_by.cb.dir);
                  return result;
              }
            , toggle_criteria   : toggle_disabled_state
            , toggle_dir        : function toggle_dir (dir$) {
                  var asc   = dir$.hasClass (options.ui_class.sort_asc);
                  var title = asc ?
                      options.title.order_by_desc : options.title.order_by_asc;
                  dir$.toggleClass (options.ui_class.sort_asc, !asc)
                      .toggleClass (options.ui_class.sort_desc, asc)
                      .attr        ("title", title);
              }
            };
        var setup_disabler = function setup_disabler () {
            var dis$ = $(this);
            dis$.append
                    ($(L ("a.button", {name : "DISABLE"})).gtw_iconify (icons))
                .attr    ("title", options.title.disabler)
                .parent  ().addClass ("ui-state-default");
        };
        var setup_esf = function setup_esf (context) {
            var S = options.selectors;
            $(S.attr_filter_value_entity, context).gtw_e_type_selector_hd
                (options);
        };
        var setup_op_button = function setup_op_button () {
            var but$   = $(this);
            var afc$   = but$.closest (options.selectors.attr_filter_container);
            var afs    = af_map [afc$.attr ("title")];
            var label  = but$.html ();
            var op     = op_map_by_sym [label];
            if (! ("ops_menu$" in afs)) {
                afs.ops_menu$ = new_menu
                    ( sig_map [afs.sig_key]
                    , op_select_cb
                    , { opts :
                          { open     : function (ev, menu) {
                                adjust_op_menu (afs);
                            }
                          , position : { my : "left top" }
                          }
                      }
                    );
            };
            attach_menu (but$, afs.ops_menu$);
            afs.ops_selected [op.sym] = true;
        };
        var submit_ajax_cb = function submit_ajax_cb (response) {
            var S = options.selectors;
            var of$ = $(S.offset);
            if ("object_container" in response) {
                $(S.object_container).last ().replaceWith
                    (response.object_container);
            };
            if ("head_line" in response) {
                $(S.head_line).html (response.head_line);
            };
            if ("limit" in response) {
                $(S.limit).val (response.limit);
            };
            if ("offset" in response) {
                $(S.offset).val (response.offset);
            };
            if ("buttons" in response) {
                fix_buttons (response.buttons);
            };
            if ("callbacks" in response) {
                for ( var i = 0, li = response.callbacks.length, cb, cbn
                    ; i < li
                    ; i++
                    ) {
                    cbn = response.callbacks [i];
                    cb  = options.callback [cbn];
                    if (cb) {
                        cb ();
                    };
                };
            };
            $GTW.push_history (qr$.attr ("action") + "?" + qr$.serialize ());
        };
        var submit_cb = function submit_cb (ev) {
            var S = options.selectors;
            var target$ = $(ev.target);
            var form$   = target$.closest ($("form"));
            var args    = form$.serialize ()
                + "&" + this.name + "=" + this.value;
            $.getJSON (form$.attr ("action"), args, submit_ajax_cb);
            return false;
        };
        var tr_selector = function tr_selector (label) {
            var head = options.selectors.attr_filter_container, tail;
            if (label.length) {
                tail = "[title^='"+label+"']";
            } else {
                tail = "[title]";
            };
            return head + tail;
        };
        var update_attr_filter_op = function update_attr_filter_op (afc$, op, key) {
            var S     = options.selectors;
            var afm   = af_map;
            var title = afc$.attr ("title");
            var afs   = afm [title];
            var but$  = $(S.attr_filter_op, afc$);
            var oop   = op_map_by_sym [but$.html ()];
            if (oop) {
                afs.ops_selected [oop.sym] = false;
            };
            $(S.attr_filter_label, afc$).attr ("for", key);
            $(S.attr_filter_value, afc$)
                .not (".hidden")
                    .prop ("id", key)
                    .end ()
                .not (".display")
                    .prop ("name", key);
            $(S.attr_filter_op,    afc$)
                .attr ("title", op.desc)
                .html (op.label);
            afs.ops_selected [op.sym] = true;
        };
        options.esf_focusee = qr$.find (selectors.apply_button);
        $(document).bind ("click.menuhide keyup.menuhide", hide_menu_cb);
        $(selectors.button).gtw_buttonify (icons, options.buttonify_options);
        $(selectors.add_button, qr$)
            .each
                ( function () {
                    attach_menu
                        ( $(this)
                        , new_menu_nested
                            ( qrs.filters, add_attr_filter_cb
                            , { pred : function (choice) {
                                    return "sig_key" in choice;
                                }
                              , icnp : true
                              }
                            )
                        );
                  }
                );
        $(selectors.attr_filter_op).each (setup_op_button);
        $(selectors.attr_filter_disabler).each (setup_disabler);
        setup_esf ();
        $(selectors.attrs_container)
            .delegate (selectors.attr_filter_disabler, "click", disabler_cb);
        $(selectors.order_by_display).each (order_by.setup);
        $(selectors.config_button).each    (attr_select.setup);
        qr$.delegate (selectors.submit, "click", submit_cb);
        return this;
    }
  } (jQuery)
);

// __END__ GTW/jQ/query_restriction.js
