# -*- coding: iso-8859-1 -*-
# Copyright (C) 1998-2005 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Library General Public
# License as published by the Free Software Foundation; either
# version 2 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Library General Public License for more details.
#
# You should have received a copy of the GNU Library General Public
# License along with this library; if not, write to the Free
# Software Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
# ****************************************************************************
#
#++
# Name
#    TFL.sos
#
# Purpose
#    Provide shell around module `os' and make some functions more portable
#
# Revision Dates
#    20-Apr-1998 (CT) Creation
#    19-Apr-1999 (CT) Don't cancel exceptions -- check existence of `dst'
#                     before trying to `remove' instead
#     1-Jul-1999 (CT) Fix `samefile' for MS operating systems
#    16-Jul-1999 (CT) `tempfile_name' added
#    12-Oct-1999 (CT) `isdir' hacked
#    12-Oct-1999 (CT) `forced_unlink' added
#     2-Dec-1999 (CT) `isdir' hack corrected
#    13-Dec-1999 (CT) `listdir_full' and `listdir_ext' added
#    13-Jan-2000 (CT) `expanded_glob' added
#    17-Jan-2000 (CT) `expanded_path' added
#    19-Jan-2000 (CT) Error in `expanded_path' removed
#                     (spurious `self' argument)
#    13-Jun-2000 (CT) `listdir_exts' added
#     9-Aug-2000 (CT) `system_info_env' added
#    14-Aug-2000 (RM) Added 'rmdir'
#    18-Sep-2000 (MG) Allow `*' as extension in `listdir_ext*'
#    18-Dec-2000 (CT) `isabs' hacked
#    22-Feb-2001 (CT) Use `raise' instead of `raise exc' for re-raise
#     7-Mar-2001 (CT) Comment added to `forced_unlink'
#    21-Sep-2001 (CT) `rmdir` fixed to recursively removed subdirectories if
#                     necessary
#    18-Jun-2004 (CT) `mkdir_p` added
#    20-Jun-2004 (CT) `mkdir_p` redefined to be just an alias for
#                     `os.makedirs` instead of home grown code
#    25-Jan-2005 (CT) `expanded_globs` added
#    24-Mar-2005 (CT)  Moved into package `TFL`
#    29-Jul-2005 (CT) Optional argument `create_dir` added to `tempfile_name`
#    30-Aug-2005 (CT) Use `in` or `startswith` instead of `find`
#    ��revision-date�����
#--

from   _TFL import TFL
from   os   import *

mkdir_p = makedirs

if (name == "nt") or (name == "win32") :
    _os_rename = rename
    def rename (src, dst) :
        if path.exists (dst) :
            remove (dst)
        _os_rename (src, dst)
    # end def rename

    _os_path_isdir = path.isdir
    def _hacked_isdir (path) :
        try :
            if path [- len (sep):] == sep and path [- len (sep) - 1] != ":" :
                path = path [: - len (sep)]
        except (SystemExit, KeyboardInterrupt), exc :
            raise
        except :
            pass
        return _os_path_isdir (path)
    # end def _hacked_isdir
    path.isdir = _hacked_isdir

    _os_path_isabs = path.isabs
    def _isabs (path) :
        return (  ":" in path
               or path.startswith ("/")
               or path.startswith ("\\")
                    ### strictly speaking this isn't an absolute filename (it
                    ### is relative to the current drive) but it isn't a
                    ### relative filename, either
               )
    # end def _isabs
    path.isabs = _isabs

    if not hasattr (path, "samefile") :
        def __samefile (p, q) :
            p = path.normcase (path.normpath (p))
            q = path.normcase (path.normpath (q))
            return p == q
        # end def __samefile
        path.samefile = __samefile
    # end if not hasattr (path, "samefile")
# end if (name == "nt") or (name == "win32")

def tempfile_name (in_dir = None, create_dir = False) :
    """Return a unqiue temporary filename. If `in_dir' is specified, the
       filename returned resides in the directory `in_dir'.
    """
    import tempfile
    try :
        if in_dir :
            tempdir, tempfile.tempdir = tempfile.tempdir, in_dir
            if create_dir and not path.isdir (in_dir) :
                mkdir (in_dir)
        result = tempfile.mktemp ()
    finally :
        if in_dir :
            tempfile.tempdir = tempdir
    return result
# end def tempfile_name

def filesize (path) :
    """Return size of file `path' in bytes."""
    import os
    import stat
    return os.stat (path) [stat.ST_SIZE]
# end def filesize

def forced_unlink (* file) :
    """Delete all `file's passed as arguments without raising exceptions for
       non-existing files.
    """
    for f in file :
        if path.exists (f) :
            unlink (f)
# end def forced_unlink

def listdir_full (in_dir) :
    """Returns the result of `listdir (in_dir)' augmented by `in_dir'
       (i.e., each element in the result is a full path).
    """
    if in_dir and in_dir != curdir :
        return [path.join (in_dir, f) for f in listdir (in_dir)]
    else :
        return listdir (".")
# end def listdir_full

def listdir_ext  (in_dir, ext) :
    """Returns a list of all files with extension `ext' contained in
       directory `in_dir'.

       Unlike the result of `listdir', the files returned by this function
       are full-blown pathes (i.e., they include `in_dir').
    """
    result = listdir_full (in_dir)
    if "*" not in ext :
        result = [f for f in result if path.isfile (f) and f.endswith (ext)]
    return result
# end def listdir_ext

__extension_dict = {}

def _ext_filter (f) :
    if path.isfile (f) :
        n, e = path.splitext (f)
        return __extension_dict.has_key (e)
    return 0
# end def _ext_filter

def listdir_exts (in_dir, * extensions) :
    """Returns a list of all files with one of the extensions specified by
       `extensions' contained in directory `in_dir'.

       Unlike the result of `listdir', the files returned by this function
       are full-blown pathes (i.e., they include `in_dir').
    """
    from _TFL.predicate import un_nested
    extensions = un_nested (extensions)
    if extensions and ("*" not in extensions) :
        global __extension_dict
        __extension_dict = {}
        for e in extensions :
            __extension_dict [e] = 1
        return filter (_ext_filter, listdir_full (in_dir))
    else :
        return [f for f in listdir_full (in_dir) if not path.isdir (f)]
# end def listdir_exts

def expanded_path (pathname) :
    """Return `pathname' with tilde and shell variables expanded."""
    return path.expandvars (path.expanduser (pathname))
# end def expanded_path

def expanded_glob (pathname) :
    """Return a list of file names matching `expanded_path (pathname)'."""
    from glob import glob
    return glob (expanded_path (pathname))
# end def expanded_glob

def expanded_globs (* pathnames) :
    """Generate all file names to which the `pathnames` expand"""
    for p in pathnames :
        for r in expanded_glob (p) :
            yield r
# end def expanded_globs

def rmdir (dir, deletefiles = 0) :
    """ Extension to the standard rmdir function. It takes an additional
        argument 'deletefiles' which can be true or false.

        If 'deletefiles' is false (default) rmdir is like the standard
        os.rmdir. Otherwise it first deletes all files in the specified
        diretory.
    """
    if deletefiles :
        files = listdir_full (dir)
        for f in files :
            if path.isdir (f) :
                rmdir  (f, deletefiles)
            else :
                remove (f)
    import os
    os.rmdir (dir)
# end def rmdir

def system_info_env () :
    """Returns a dictionary containing the subset of `os.environ' providing
       information about the system.
    """
    import re
    import sys
    patterns = \
        [ re.compile (k)
        for k in ("NAME$", "^OS", "PROCESSOR", "^(PYTHON)?PATH$", "TYPE$")
        ]
    result = dict \
        ( program  = sys.executable
        , platform = sys.platform
        )
    for k, v in environ.iteritems () :
        for p in patterns :
            if p.search (k) :
                result [k] = v
                break
    return result
# end def system_info_env

if __name__ != "__main__" :
    TFL._Export_Module ()
### __END__ TFL.sos
