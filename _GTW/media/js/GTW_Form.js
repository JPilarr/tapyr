/*
** Copyright (C) 2010 Martin Glueck All rights reserved
** Langstrasse 4, A--2244 Spannberg, Austria. martin@mangari.org
** ****************************************************************************
** This file is part of the library GTW.
**
** This file is free software: you can redistribute it and/or modify
** it under the terms of the GNU Affero General Public License as published by
** the Free Software Foundation, either version 3 of the License, or
** (at your option) any later version.
**
** This file is distributed in the hope that it will be useful,
** but WITHOUT ANY WARRANTY; without even the implied warranty of
** MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
** GNU Affero General Public License for more details.
**
** You should have received a copy of the GNU Affero General Public License
** along with this file. If not, see <http://www.gnu.org/licenses/>.
** ****************************************************************************
**
**++
** Name
**    GTW_Form
**
** Purpose
**    Javascipt library form GTW form handling.
**
** Revision Dates
**    25-Feb-2010 (MG) Creation (based on model_edit_ui.js)
**    27-Feb-2010 (MG) `_form_submit` renumeration of forms added
      ��revision-date�����
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
  var form_buttons =
      [ { name           : "add"
        , title          : _("Add new form")
        , css_class      : "inline-form-add"
        , add_to_inline  : "false"
        , href           : "#add"
        , enabled        : "cur_count < max_count"
        , icon           : "ui-icon-plusthick"
        , callback       : "_add_new_inline"
        }
      , { name           : "delete"
        , add_to_inline  : "true"
        , href           : "#delete-recover"
        , default_state  : 0
        , states         :
            [ { name     : "delete"
              , title    : _("Delete")
              , enabled  : "cur_count > min_count"
              , icon     : "ui-icon-trash"
              , callback : "_delete_inline"
              }
            , { name     : "recover"
              , title    : _("Undelete")
              , enabled  : "cur_count < max_count"
              , icon     : "ui-icon-plus"
              , callback : "_undelete_inline"
              }
            ]
        }
      , { name           : "rename"
        , href           : "#rename"
        , add_to_inline  : "lid"
        , default_state  : 0
        , states         :
            [ { name     : "unlock"
              , title    : _("Rename")
              , enabled  : "true"
              , icon     : "ui-icon-pencil"
              , callback : "_unlock_inline"
              }
            , { name     : "lock"
              , title    : _("Undo")
              , enabled  : "true"
              , icon     : "ui-icon-arrowreturnthick-1-w"
              , callback : "_revert_inline"
              }
            ]
        }
      , { name           : "copy"
        , title          : _("Copy")
        , add_to_inline  : "lid"
        , href           : "#copy"
        , enabled        : "cur_count < max_count"
        , icon           : "ui-icon-copy"
        , callback       : "_copy_inline"
        }
      , { name           : "clear"
        , title          : _("Clear")
        , add_to_inline  : "lid"
        , href           : "#clear"
        , enabled        : "true"
        , icon           : "ui-icon-circle-close"
        , callback       : "_clear_inline"
        }
      ];

  var field_no_pat = /-M([\dP]+)_/;
  var GTW_Form =
    { _create : function ()
      {
        var i;
        var inlines    = this.options.inlines;
        for (i = 0; i < inlines.length; i++)
          {
            this._setup_inline (inlines [i]);
          }
        this._setup_completers (this.element);
        this.element.find (":submit").bind ("click", this, this._form_submit);
      }
    , _add_button : function ($element, button, prepend)
      {
        var icon      = button.icon;
        var title     = _T (button.title);
        var css_class = button.css_class;
        if (button.states)
          {
            icon      =     button.states [button.default_state].icon;
            title     = _T (button.states [button.default_state].title);
            css_class =     button.states [button.default_state].css_class;
          }
        if (css_class)
          {
            css_class = ' class="icon-link ' + css_class + '"';
          }
        else
          {
            css_class = ' class="icon-link"'
          }
        var html = '<a href="' + button.href + '"'
                 +   'title="' + title + '"' + css_class
                 + '>'
                 +   '<span class="ui-state-default ui-icon ' + icon + '">'
                 +      button.name
                 +   '</span>'
                 + '</a>'
        if (! prepend) $element.append  (html);
        else           $element.prepend (html);
      }
    , _add_new_inline : function (evt)
      {
        var $inline = $(evt.currentTarget).parents (".inline-root");
        evt.data._copy_form ($inline);
        evt.preventDefault  ();
      }
    , _clear_inline   : function (evt)
      {
        var  self   = evt.data;
        var $form   = $(evt.target).parents (".inline-instance");
        var $inputs = $form.find       (":input")
                           .attr       ("value", "")
                           .removeAttr ("disabled");
        /* set the state of ALL inlines to empty */
        $form.find ("input[name$=-instance_state]").attr ("value", "");
        /* set lid/state of ALL lines to New */
        $form.find ("input[name$=__lid_a_state_]").attr ("value", ":N");
        evt.preventDefault         ();
        evt.stopPropagation        ();
        $inputs.eq (0).focus       ();
      }
    , _copy_inline   : function (evt)
      {
        var  self   = evt.data;
        var $inline = $(evt.currentTarget).parents (".inline-root");
        var $source = $(evt.target).parents (".inline-instance");
        var  $new   = self._copy_form ($inline);
        self._restore_form_state ($new, self._save_form_state ($source));
        /* set the state of ALL inlines to empty */
        $new.find ("input[name$=-instance_state]").attr ("value", "");
        /* set lid/state of ALL lines to New */
        $new.find ("input[name$=__lid_a_state_]").attr ("value", ":N");
        self._update_button_states ($inline);
        evt.preventDefault         ();
        evt.stopPropagation        ();
      }
    , _copy_form     : function ($inline)
      {
        var state = {};
        var $prototype = $inline.data ("$prototype");
        var $new       = $prototype.clone ().removeClass ("inline-prototype");
        /* now that we have cloned the block, let's change the
        ** name/id/for attributes
        */
        $inline.data ("cur_count", $inline.data ("cur_count") + 1);
        var cur_number = $inline.data ("cur_number");
        $inline.data ("cur_number", cur_number + 1);
        var pattern    = /-MP_/;
        var new_no     = "-M" + cur_number + "_";
        var $labels    = $new.find     ("label")
        for (var i = 0; i < $labels.length; i++)
        {
            var $l = $labels.eq (i);
            $l.attr ("for", $l.attr ("for").replace (pattern, new_no));
        }
        var $edit_elements = $new.find (":input");
        var  edit_mod_list = ["id", "name"];
        for (var i = 0; i < $edit_elements.length; i++)
        {
            var $e = $edit_elements.eq (i);
            for (var j = 0; j < edit_mod_list.length; j++)
            {
                var n = edit_mod_list [j];
                $e.attr (n, $e.attr (n).replace (pattern, new_no));
            }
        }
        /* we are ready to add the new block at the end */
        this._setup_buttons        ($new, $inline.data ("buttons"), $inline);
        $prototype.parent          ().append ($new);
        this._update_button_states ($inline);
        this._setup_completers     ($inline);
        /* set lid/state of ALL lines to New */
        $new.find ("input[name$=__lid_a_state_]").attr ("value", ":N");
        return $new;
      }
    , _delete_inline : function (evt)
      {
        var  self   = evt.data;
        var $inline = $(evt.currentTarget).parents (".inline-root");
        var $proto  = $inline.data                 ("$prototype");
        var $form   = $(evt.target).parents (".inline-instance");
        if ($proto && self._forms_equal ($form, $proto))
        {
            $form.remove ();
        }
        else
        {
            var  button        = form_buttons [1];
            var $link          = $form.find  ("a[href=" + button.href + "]");
            var $button        = $link.find  ("span");
            var $elements      = $form.find  (":input:not([type=hidden])");
            var $l_a_s         = self._lid_for_inline ($inline, $form);
            var  lid           = $l_a_s.attr ("value").split (":") [0];
            $elements.attr        ("disabled","disabled")
                     .addClass    ("ui-state-disabled");
            $link.attr            ("title", _T (button.states [1].title));
            $button.removeClass   (button.states [0].icon)
                   .addClass      (button.states [1].icon);
            $l_a_s.attr ("value", [lid, "U"].join (":"));
        }
        $inline.data ("cur_count", $inline.data ("cur_count") - 1);
        self._update_button_states ($inline);
        evt.preventDefault         ();
        evt.stopPropagation        ();
      }
    , _forms_equal : function ($l, $r)
      {
        /* Returns whether the values of the two forms are equal */
        var $l_value_elements = $l.find ("[value]:not([type=hidden])");
        var $r_value_elements = $r.find ("[value]:not([type=hidden])");
        if ($l_value_elements.length != $r_value_elements.length)
            return false;
        for (var i = 0; i < $l_value_elements.length; i++)
        {
            if (  $l_value_elements.eq (i).attr ("value")
               != $r_value_elements.eq (i).attr ("value")
               )
                return false;
        }
        return true;
      }
    , _form_submit : function (evt)
      {
        var  self     = evt.data;
        var  pattern  = /M\d+_/;
        var $this     = $(this);
        /* re-enumerate the forms */
        /* first, let's renumerate the inline-instance's */
        self.element.find (".inline-form-table").each ( function ()
            {
                var $this  = $(this);
                var  no    = -1; /* the first is the prototype */
                $this.find (".inline-instance").each (function ()
                {
                    var $elements      = $(this).find (":input");
                    var  edit_mod_list = ["id", "name"];
                    var  new_no        = "M" + no + "_";
                    for (var i = 0; i < $elements.length; i++)
                    {
                        var $e = $elements.eq (i);
                        for (var j = 0; j < edit_mod_list.length; j++)
                        {
                            var n = edit_mod_list [j];
                            $e.attr
                              ( n
                              , $e.attr (n).replace (pattern, new_no)
                              );
                        }
                    }
                    no = no + 1;
                });
                var $m2m_range = $this.find (".many-2-many-range:first");
                var  m2m_range = $m2m_range.attr ("value").split (":");
                m2m_range [1]  = no;
                $m2m_range.attr ("value", m2m_range.join (":"));
            });
        /* re-enable all input elements so that all information is sent to the
        */
        self.element.find (":input").removeAttr ("disabled");
        /* prevent multiple submits use a solution found here:
        ** http://www.norio.be/blog/2008/09/preventing-multiple-form-submissions-revisited
        */
        $this.clone ().insertAfter ($this).attr ("disabled","disabled");
        $this.hide  ();
      }
    , _lid_for_inline : function ($inline, $form)
      {
        return $form.find
          ( "[name^=" + $inline.data ("options").prefix + "]"
          + "[name$=__lid_a_state_]"
          );
      }
    , _restore_form_state : function ($form, state)
      {
        var $elements = $form.find  (":input");
        var  form_no  = state ["_form_no_"];
        for (var i = 0; i < $elements.length; i++)
        {
            var $e  = $elements.eq (i);
            var key = $e.attr ("name").replace (field_no_pat, form_no);
            $e.attr ("value", state [key]);
        }
      }
    , _revert_inline   : function (evt)
      {
        var self           = evt.data;
        var $inline        = $(evt.currentTarget).parents (".inline-root");
        var $form          = $(evt.target).parents (".inline-instance");
        var  button        = form_buttons [2];
        var $link          = $form.find  ("a[href=" + button.href + "]");
        var $button        = $link.find  ("span");
        var $elements      = $form.find  (":input");
        self._restore_form_state   ($form, $form.data ("_state"));
        $elements.attr             ("disabled", "disabled");
        $link.attr                 ("title", _T (button.states [0].title));
        $button.removeClass        (button.states [1].icon)
               .addClass           (button.states [0].icon);
        self._update_button_states ($inline);
        evt.preventDefault         ();
        evt.stopPropagation        ();
      }
    , _save_form_state      : function ($form)
      {
        var $elements = $form.find (":input");
        var  match    = field_no_pat.exec ($elements.attr ("name"))
        var  state    = {_form_no_ :  (match || [""]) [0]};
        for (var i = 0; i < $elements.length; i++)
        {
            var $e = $elements.eq (i);
            state [$e.attr ("name")] = $e.attr ("value");
        }
        return state;
      }
    , _setup_buttons : function ($inline_instance, buttons, $inline)
      {
        $inline        = $inline || $inline_instance.parents (".inline-root");
        var $element   = $inline_instance;
        var $first_tag = $element.find (".inline-instance");
        if (! $first_tag.length)
            $first_tag = $element;
        var  first_tag = $first_tag.get (0).tagName.toLowerCase ();
        var $l_a_s     = this._lid_for_inline ($inline, $inline_instance);
        var  lid       = $l_a_s.attr ("value").split (":") [0];
        if (first_tag == "tr")
          {
            var css_class = 'class="width-' + buttons.length + '-icons"';
            var $temp  = $('<td><span ' + css_class + '</span></td>');
            $first_tag.append ($temp);
            $element = $temp.find ("span");
          }
        for (var i = 0; i < form_buttons.length; i++)
          {
            var button = form_buttons [i];
            if (  ($.inArray (button.name, buttons) >= 0)
               && eval (button.add_to_inline)
               )
              {
                this._add_button ($element, button);
              }
          }
      }
    , _setup_completers : function ($root)
    {
      var completers = this.options.completers;
      for (i = 0; i < completers.length; i++)
        {
          var completer = completers [i];
          var prefix    = "[name^=" + completer.field_prefix + "]";
          var middle    = "";
          if (completer.field_postfix)
              middle    = completer.field_postfix + "__";
          for (var field in completer.triggers)
            {
                var options = $.extend ({field : field}, completer);
                $root.find
                    ( prefix + "[name$=" + middle + field + "]"
                    ).MOM_Auto_Complete (options);
            }
        }
    }
    , _setup_inline : function (inline)
      {
        var $inline    = $("." + inline.prefix);
        var $prototype = $inline.find (".inline-prototype")
        var  buttons   = inline ["buttons"];
        $inline.data ("options", inline);
        /* if we have found a prototype we can have the add button */
        if ($prototype.length)
          {
            var $m2m_range = $inline.find ("input.many-2-many-range:first");
            var  m2m_range = $m2m_range.attr   ("value").split (":");
            var  cur_count = parseInt (m2m_range [1]);
            var  max_count = parseInt (m2m_range [2]);
            $inline.data ("$prototype", $prototype);
            $inline.data ("$m2m_range", $m2m_range);
            $inline.data ("min_count",  parseInt (m2m_range [0]));
            $inline.data ("cur_count",  cur_count);
            $inline.data ("cur_number", cur_count);
            $inline.data ("max_count",  max_count);
            this._add_button ($inline.find ("legend"), form_buttons [0], true);
          }
        else
          {
            $inline.data ("min_count",  0);
            $inline.data ("cur_count",  1);
            $inline.data ("cur_number", 0);
            $inline.data ("max_count",  1);
          }
        $inline.data     ("buttons", buttons);
        $inline.addClass ("inline-root");
        var self = this;
        $inline.find
          ("." + inline.instance_class + ":not(.inline-prototype)").each
            (function ()
              {
                var $this   = $(this);
                self._setup_buttons ($this, buttons);
                var $l_a_s = $this.find  ("input[name$=__lid_a_state_]");
                if (  inline.initial_disabled
                   && $l_a_s.attr ("value").split (":") [0]
                   )
                    $this.find (":input").attr ("disabled", "disabled");
              }
            );
        this._update_button_states ($inline);
      }
    , _undelete_inline : function (evt)
      {
        var self           = evt.data;
        var $inline        = $(evt.currentTarget).parents (".inline-root");
        var $proto         = $inline.data ("$prototype");
        var $form          = $(evt.target).parents (".inline-instance");
        var  button        = form_buttons [1];
        var $link          = $form.find  ("a[href=" + button.href + "]");
        var $button        = $link.find  ("span");
        var $elements      = $form.find  (":input:not([type=hidden])");
        var $l_a_s         = self._lid_for_inline ($inline, $form);
        var  lid           = $l_a_s.attr ("value").split (":") [0];
        var  new_state     = "L";
        if (! lid)
        {
            new_state      = "N";
            $elements.removeAttr ("disabled")
        }
        $elements.removeClass ("ui-state-disabled");
        $inline.data ("cur_count", $inline.data ("cur_count") + 1);
        $l_a_s.attr ("value", [lid, new_state].join (":"));
        $link.attr                 ("title", _T (button.states [0].title));
        $button.removeClass        (button.states [1].icon)
               .addClass           (button.states [0].icon);
        self._update_button_states ($inline);
        evt.preventDefault         ();
        evt.stopPropagation        ();
      }
    , _unlock_inline   : function (evt)
      {
        var self         = evt.data;
        var $inline      = $(evt.currentTarget).parents (".inline-root");
        var $form        = $(evt.target).parents (".inline-instance");
        var  button      = form_buttons [2];
        var $link        = $form.find    ("a[href=" + button.href + "]");
        var $button      = $link.find    ("span");
        var $elements    = $form.find    (":input");
        var  link_prefix = $inline.data ("options").prefix;
        var name         = $form.find  ("input[name$=__lid_a_state_]").each
          ( function () {
            var $this      = $(this);
            var lid        = $this.attr ("value").split (":") [0];
            var name       = $this.attr ("name");
            var new_state  = "r"
            if (name.split (field_no_pat) [0] == link_prefix)
            {
                /* this is the state field of the link */
                new_state     = "R";
            }
            $this.attr ("value", [lid, new_state].join (":"));
          }).attr ("name");
        $form.data                 ("_state", self._save_form_state ($form));
        $elements.removeAttr       ("disabled")
        $link.attr ("title", _T (button.states [1].title))
        $button.removeClass        (button.states [0].icon)
               .addClass           (button.states [1].icon);
        self._update_button_states ($inline);
        evt.preventDefault         ();
        evt.stopPropagation        ();
      }
    , _update_button_state  : function ( $root
                                       , cur_count, min_count, max_count
                                       , button, state
                                       )
    {
        var  href    = state.href || button.href;
        var $buttons = $root.find
            ('a[href=' + href + '] .' + state.icon.split (" ") [0])
        /* remove old handlers */
        $buttons.unbind ("click")
        if (eval (state.enabled))
        {
            var cb = this [state.callback];
            $buttons.bind   ("click", this, cb)
                    .parent ().removeClass ("ui-state-disabled");
        }
        else
        {
            $buttons.parent ().addClass ("ui-state-disabled");
        }
    }
    , _update_button_states : function ($root)
      {
        var  cur_count = $root.data ("cur_count");
        var  min_count = $root.data ("min_count");
        var  max_count = $root.data ("max_count");
        var $range     = $root.data ("$m2m_range");
        if ($range)
            $range.attr ("value", [min_count, cur_count, max_count].join (":"));
        for (var i = 0; i < form_buttons.length; i++)
        {
            var button        = form_buttons [i];
            if (button.states)
            {
                for (var si = 0; si < button.states.length; si++)
                {
                    this._update_button_state
                        ( $root, cur_count, min_count, max_count
                        , button, button.states [si]
                        );
                }
            }
            else
            {
                this._update_button_state
                    ($root, cur_count, min_count, max_count, button, button);
            }
        }
      }
    };
  $.widget ("ui.GTW_Form", GTW_Form);
  $.extend
      ( $.ui.GTW_Form
      , { "version"      : "0.1"
        , "defaults"     :
          {
          }
        }
      )
})(jQuery);
