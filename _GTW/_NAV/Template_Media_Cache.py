# -*- coding: utf-8 -*-
# Copyright (C) 2011-2012 Martin Glueck All rights reserved
# Langstrasse 4, A--2244 Spannberg. martin@mangari.org
# #*** <License> ************************************************************#
# This module is part of the package GTW.NAV.
# 
# This module is licensed under the terms of the BSD 3-Clause License
# <http://www.c-tanzer.at/license/bsd_3c.html>.
# #*** </License> ***********************************************************#
#
#++
# Name
#    GTW.NAV.Template_Media_Cache
#
# Purpose
#    Handling of the caching of media fragments for templates
#
# Revision Dates
#    26-Sep-2011 (MG) Creation (factored from GTW.NAV.Base.load_css, store_css)
#    21-Oct-2011 (MG) `_create_css_cache` creating of directory added
#    21-Oct-2011 (CT) Esthetics
#    22-Nov-2011 (MG) Use `sos.mkdir_p` instead of `sos.mkdir`
#    25-Nov-2011 (CT) Use `root.template_iter` (major surgery)
#     5-Jan-2012 (CT) Add caching for `js`, call `t.get_cached_media` (SURGERY)
#     9-Jan-2012 (CT) Add `minifier`, cache `js` only `if not root.TEST`
#    19-Jan-2012 (CT) s/rank/cache_rank/
#    ««revision-date»»···
#--

from   _GTW                   import GTW
import _GTW._NAV
import _GTW.Media

from   _TFL                   import TFL
from   _TFL                   import sos
from   _TFL.predicate         import first

import _TFL._Meta.Object
import _TFL.multimap

import  hashlib
import  base64
from    posixpath import join as pjoin

class Template_Media_Cache (TFL.Meta.Object) :

    cache_rank = 1000

    def __init__ (self, media_dir, prefix, clear_dir = False) :
        if not prefix.startswith ("/") :
            prefix     = "/%s" % (prefix, )
        self.media_dir = media_dir
        self.prefix    = prefix
        self.clear_dir = clear_dir
    # end def __init__

    def as_pickle_cargo (self, root) :
        if self.clear_dir :
            self._clear_dir ()
        css_map = {}
        js_map  = {}
        TEST    = root.TEST
        TT      = root.Templateer.Template_Type
        for t in TFL.uniq (root.template_iter ()) :
            css_href = self._add_to_map (t, "CSS", css_map)
            js_href  = None if TEST else self._add_to_map (t, "js", js_map)
            TT.Media_Map [t.name] = t.get_cached_media (css_href, js_href)
        self._create_cache ("CSS", css_map, None if TEST else GTW.minified_css)
        if not TEST :
            self._create_cache ("js", js_map, GTW.minified_js)
        return dict (css_href_map = TT.css_href_map, Media_Map = TT.Media_Map)
    # end def as_pickle_cargo

    def _add_to_map (self, t, name, map) :
        try :
            attr = getattr (t, name)
        except Exception as exc :
            print name, "exception for template", t.path
            print "   ", exc
            if __debug__ :
                import traceback
                traceback.print_exc ()
        else :
            if attr :
                attr = attr.encode      (t.env.encoding)
                h    = hashlib.sha1     (attr).digest ()
                k    = base64.b64encode (h, "_-").rstrip ("=")
                if k not in map :
                    cn      = ".".join      ((k, name.lower ()))
                    href    = pjoin         (self.prefix,    cn)
                    fn      = sos.path.join (self.media_dir, cn)
                    map [k] = (href, fn, attr)
                else :
                    href = map [k] [0]
                return href
    # end def _add_to_map

    def _clear_dir (self) :
        for fod in sos.listdir_full (self.media_dir) :
            if sos.path.isdir (fod) :
                sos.rmdir  (fod, True)
            else :
                sos.unlink (fod)
    # end def _clear_dir

    def _create_cache (self, name, map, minifier = None) :
        media_dir = self.media_dir
        if not sos.path.isdir (media_dir) :
            sos.mkdir_p (media_dir)
        for k, (href, fn, attr) in map.iteritems () :
            with open (fn, "wb") as file :
                if minifier is not None :
                    attr = minifier (attr)
                file.write (attr)
    # end def _create_cache

    @classmethod
    def Media_Filenames (cls, root, include_templates = True) :
        result = set ()
        def _add (ts) :
            for t in ts :
                if include_templates and t.source_path is not None :
                    result.add (t.source_path)
                if t.media_path is not None :
                    result.add (t.media_path)
        for t in root.template_iter () :
            _add (t.templates)
        return result
    # end def Media_Filenames

    def from_pickle_cargo (self, root, cargo) :
        TT              = root.Templateer.Template_Type
        TT.css_href_map = cargo.get ("css_href_map", {})
        TT.Media_Map    = cargo.get ("Media_Map",    {})
    # end def from_pickle_cargo

    def __str__ (self) :
        return "Template_Media_Cache (%r, %r)" % (self.media_dir, self.prefix)
    # end def __str__

# end class Template_Media_Cache

if __name__ != "__main__" :
    GTW.NAV._Export ("*")
### __END__ GTW.NAV.Template_Media_Cache
