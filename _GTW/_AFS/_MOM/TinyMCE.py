# -*- coding: utf-8 -*-
# Copyright (C) 2013 Martin Glueck All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. martin@mangari.org
# #*** <License> ************************************************************#
# This module is part of the package GTW.AFS.MOM.
# 
# This module is licensed under the terms of the BSD 3-Clause License
# <http://www.c-tanzer.at/license/bsd_3c.html>.
# #*** </License> ***********************************************************#
#
#++
# Name
#    GTW.AFS.MOM.TinyMCE
#
# Purpose
#    Special field for adding support for the TinyMCE WYSIWYG editor.
#
# Revision Dates
#    29-Jan-2013 (MG) Creation
#--

from   __future__ import absolute_import, division, print_function, unicode_literals

from   _GTW                     import GTW
from   _GTW._AFS._MOM           import Element
from   _JNJ                     import JNJ
import _JNJ.Templateer
from   _TFL.I18N                import _T

JNJ.Template \
    ( "afs_tinymce"
    , "html/AFS/tinymce.jnj"
    , parent_name = "afs_div_seq"
    )

class TinyMCE_Field (Element.Field) :
    """A field which uses the tinymce WYSIWYG editor"""

    renderer                              = "afs_tinymce"
    settings                              = dict \
        ( tinymce                         = dict
            ( theme                       = "advanced"
            , theme_advanced_buttons1_add = "fontsizeselect,forecolor,backcolor"
            , theme_advanced_buttons3_add = "preview"
            , plugins                     =
                "pagebreak,style,table,advhr,advimage,advlink,"
                "emotions,inlinepopups,preview,searchreplace,print,"
                "contextmenu,paste,fullscreen,noneditable,visualchars,"
                "nonbreaking,xhtmlxtras,template"
            , theme_advanced_resizing     = True
            , relative_urls               = True
            )
        , file_browser                    = dict
            ( title                       = _T ("Image Selection")
            , width                       = 950
            , height                      = 450
            , url                         = "/elfinder/window.html"
            )
        )

    def __init__ (self, * args, ** kw) :
        kw ["tinymce"]      = dict \
            (self.settings ["tinymce"],      ** kw.get ("tinymce", {}))
        kw ["file_browser"] = dict \
            (self.settings ["file_browser"], ** kw.get ("file_browser", {}))
        self.__super.__init__ (* args,  ** kw)
    # end def __init__

# end class TinyMCE_Field

if __name__ != "__main__" :
    GTW.AFS.MOM._Export ("*")
### __END__ GTW.AFS.MOM.TinyMCE
