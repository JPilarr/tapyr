# -*- coding: utf-8 -*-
# Copyright (C) 2005 Martin Glück. All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. office@spannberg.com
# ****************************************************************************
#
# This module is licensed under the terms of the BSD 3-Clause License
# <http://www.c-tanzer.at/license/bsd_3c.html>.
# ****************************************************************************
#
#++
# Name
#    TGL.TKT.GTK.File_Chooser_Dialog
#
# Purpose
#    Wrapper for the GTK widget FileChooserDialog
#
# Revision Dates
#    03-Jun-2005 (MG) Automated creation
#     3-Jun-2005 (MG) Creation continued
#    14-Aug-2005 (MG) `_ask_dialog` fixed
#     3-Sep-2005 (MG) `select_multiple` added
#     4-Sep-2005 (CT) `reduce` monstrosity replaced by call to `any_true_p`
#     4-Sep-2005 (CT) `run` streamlined
#     5-Sep-2005 (MG) `overwrite_warning` removed from `Folder_Create_Dialog`
#    ««revision-date»»···
#--

from   _TGL._TKT._GTK         import GTK
import _TGL._TKT._GTK.Dialog
import _TGL._TKT._GTK.File_Filter
import _TGL._TKT._GTK.Message_Dialog
import _TFL.sos               as os

from   _TFL.predicate         import any_true_p

class File_Chooser_Dialog (GTK.Dialog.Dialog) :
    """Wrapper for the GTK widget FileChooserDialog"""

    GTK_Class        = GTK.gtk.FileChooserDialog
    __gtk_properties = \
        ( GTK.SG_Property
            ("selection", set = False, get_fct_name = "get_filenames")
        , GTK.SG_Property ("select_multiple")
        )

# end class File_Chooser_Dialog

class File_Open_Dialog (File_Chooser_Dialog) :
    """Select an existing file."""

    action         = GTK.gtk.FILE_CHOOSER_ACTION_OPEN
    action_buttons = \
        ( "gtk-cancel", GTK.RESPONSE_CANCEL
        , "gtk-open",   GTK.RESPONSE_OK
        )

    _wtk_delegation = GTK.Delegation \
        ( GTK.Delegator_O ("add_filter")
        )

    def __init__ ( self
                 , parent      = None
                 , title       = None
                 , filetypes   = ()
                 , init_val    = None
                 , multiselect = False
                 , AC          = None
                 ) :
        self.__super.__init__ \
            ( title   = title
            , parent  = parent
            , action  = self.action
            , buttons = self.action_buttons
            , AC      = AC
            )
        for name, pattern in filetypes :
            filter = self.TNS.File_Filter (name, pattern, AC = self.AC)
            self.add_filter               (filter)
        if init_val :
            self.wtk_object.set_filename  (init_val)
        self.select_multiple = multiselect
    # end def __init__

# end class File_Open_Dialog

class _Save_Dialog_ (File_Open_Dialog) :
    """Select a new file name."""

    action         = GTK.gtk.FILE_CHOOSER_ACTION_SAVE
    action_buttons = \
        ( "gtk-cancel", GTK.RESPONSE_CANCEL
        , "gtk-save",   GTK.RESPONSE_OK
        )
    exist_check    = staticmethod (os.path.isfile)
    kind           = "file"

    def __init__ (self, * args, ** kw) :
        self.__super.__init__ (* args, ** kw)
        initialdir, initialfile = os.path.split (kw.get ("init_val", ""))
        if initialfile :
            self.wtk_object.set_current_name (initialfile)
    # end def __init__

# end class _Save_Dialog_

class File_Save_Dialog (_Save_Dialog_) :
    """Select a new file name."""

    def run (self, overwrite_warning = True) :
        response = self.wtk_object.run ()
        if overwrite_warning and response == GTK.RESPONSE_OK :
            selected = self.selection
            if any_true_p (selected, self.exist_check) :
                d = self.TNS.Yes_No_Cancel_Question \
                    ( title   = self.title
                    , message =
                        ( "The %s `%s` already exists!\n\n"
                          "Do you realy want to overwrite it?"
                        ) % (self.kind, selected)
                    , AC      = self.AC
                    )
                over = d.run ()
                d.destroy    ()
                if over == GTK.RESPONSE_CANCEL :
                    return over
                elif over == GTK.RESPONSE_YES :
                    return GTK.RESPONSE_OK
        return response
    # end def run

# end class File_Save_Dialog

class Folder_Select_Dialog (File_Open_Dialog) :
    """Select a new file name."""

    action         = GTK.gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER

# end class Folder_Select_Dialog

class Folder_Create_Dialog (_Save_Dialog_) :
    """Select a new file name."""

    action         = GTK.gtk.FILE_CHOOSER_ACTION_CREATE_FOLDER
    exist_check    = staticmethod (os.path.isdir)
    kind           = "directory"

# end class Folder_Create_Dialog

def _ask_dialog (cls, args = (), kw = {}) :
    d = cls (* args, ** kw)
    if d.run () == GTK.RESPONSE_CANCEL :
        result = None
    else :
        result = d.selection
        if len (result) == 1 :
            result = result [0]
    d.destroy ()
    return result
# end def _ask_dialog

def ask_open_file_name (* args, ** kw) :
    return _ask_dialog (File_Open_Dialog, args, kw)
# end def ask_open_file_name

def ask_save_file_name (* args, ** kw) :
    return _ask_dialog (File_Save_Dialog, args, kw)
# end def ask_save_file_name

def ask_dir_name (* args, ** kw) :
    return _ask_dialog (Folder_Select_Dialog, args, kw)
# end def ask_dir_name

def ask_open_dir_name (* args, ** kw) :
    return _ask_dialog (Folder_Select_Dialog, args, kw)
# end def ask_open_dir_name

def ask_save_dir_name (* args, ** kw) :
    return _ask_dialog (Folder_Create_Dialog, args, kw)
# end def ask_save_dir_name

if __name__ != "__main__" :
    GTK._Export ("*")
else :
    from _TGL import TGL
    from _TGL._UI.App_Context   import App_Context
    AC = App_Context (TGL)
    fo = File_Save_Dialog \
        ( title     = "Test file save"
        , filetypes = (("All Files", "*"), ("Python Files", "*.py"))
        , init_val  = ("/home/lucky/x.py")
        , AC        = AC
        )
    print fo.run ()
    print fo.selection
### __END__ TGL.TKT.GTK.File_Chooser_Dialog
