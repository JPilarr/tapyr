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
#    TFL.Filename
#
# Purpose
#    Model filename
#
# Revision Dates
#    16-Apr-1998 (CT) Creation
#    20-Apr-1999 (CT) `__str__' and `__repr__' added
#    16-Jul-1999 (CT) `abs_directory' added
#    16-Jul-1999 (CT) `normpath' applied to `directory'
#    19-Jul-1999 (CT) Use `os.path.abspath' if available
#    17-Sep-1999 (MY) Complete documentation of the module
#    29-Sep-1999 (MY) Spellcheck the comments and put comment-endmarker in
#                     a separate line
#    28-Oct-1999 (CT) `base_ext' added
#     7-Dec-1999 (CT) Hack around bug in os.path.split of Win32 Python 1.5.1
#     7-Dec-1999 (CT) `abs_name' added
#     3-Feb-2000 (CT) `default_dir' added
#     3-May-2000 (CT) `__cmp__' and `__hash__' added
#    31-Jul-2000 (CT) `make_absolute' added
#    18-Dec-2000 (CT) `default_rel' added
#    19-Feb-2001 (CT) Stub for `relative_to' added
#    20-Feb-2001 (CT) `relative_to' added (as implemented by (ARU) and (MFE))
#    20-Feb-2001 (CT) Unit tests for `relative_to' added
#    26-Feb-2001 (ARU) Unit tests for 'Filename' constructor/selector axioms
#                      added
#    26-Feb-2001 (CT) `__init__' changed to apply `path.normpath' only to
#                     non-empty directories
#    26-Feb-2001 (CT) Unit tests corrected
#     3-May-2001 (CT) Doc-test added and style of test formatting changed
#    12-Nov-2001 (CT) `posixified` added
#    21-Feb-2001 (MSF) restored revision 1.21 (unittest is guarded by _debug_)
#     7-Mar-2003 (CT)  `relative_to` changed to include `.` for same
#                      directory
#     7-Mar-2003 (CT) 1.5.2 cruft removed from `relative_to`
#    29-Apr-2004 (MUZ) Corrected unittests
#     6-May-2004 (GWA) 'name_as_dir' added
#    24-May-2004 (CT)  `name_as_dir` removed
#    24-May-2004 (CT)  `Dirname` added
#    25-May-2004 (GWA) `Dirname` Doctests added
#    25-May-2004 (GWA) Bug fix in Dirname - `Dirname` Doctest with existing
#                      file added
#    28-May-2004 (GWA) `Dirname` pickles itself as `Filename`
#     7-Jun-2004 (GWA) `lower_lvl_dir` with Doctest added
#     7-Jun-2004 (GWA) `lower_lvl_dir` removed
#    15-Jul-2004 (CT)  `Function` replaced by staticmethod
#    15-Jul-2004 (CT)  Calls to `string` functions replaced by calls to `str`
#                      methods
#    18-Aug-2004 (CT)  `Filename.__nonzero__` changed to check `base` instead
#                      of `name`
#    30-Aug-2004 (GWA) `relative_to` corrected for win32 environment,
#                      `_cmp_file_str` introduced for posix and win32
#                      environment
#     6-Sep-2004 (GWA) `_cmp_file_str` -> reworked to `_is_file_str_equal`
#     6-Sep-2004 (GWA) `_is_file_str_equal` replaced with `normalized`
#     6-Sep-2004 (GWA) `normalized` changed in non Unix/Windows Environment
#     7-Sep-2004 (CT)  `_as_dir` and `_as_file` added and used
#     7-Sep-2004 (CT)  `as_dir` and `as_file` added
#     7-Sep-2004 (CT)  Methods defined in alphabetical order
#    28-Sep-2004 (CT)  Use `isinstance` instead of type comparison
#    24-Mar-2005 (CT)  Moved into package `TFL`
#    23-Mar-2006 (CED) `real_directory`, `real_name` added
#    23-Jul-2007 (CED) Activated absolute_import
#    06-Aug-2007 (CED) Future import removed again
#    ��revision-date�����
#--



"""Provides a class that represents a filename with its parts: path, base
   name, and file extension.
"""

from   _TFL           import TFL
from   _TFL.predicate import *

import _TFL._Meta.Object
import _TFL.Environment
import _TFL.sos

class Filename (TFL.Meta.Object):
    """Represents a filename with its parts: path, base name and file
       extension.

       The parts of the filename are provided by the attributes:

       base        basic file name
       ext         extension of the filename
       directory   path of the filename
       base_ext    `base' + `ext'
       name        complete filename including `directory', `base', and `ext'

       For example:

       >>> f=Filename ("/a/b/c/d/e.f")
       >>> f.name
       '/a/b/c/d/e.f'
       >>> f.base
       'e'
       >>> f.ext
       '.f'
       >>> f.directory
       '/a/b/c/d'
       >>> f.base_ext
       'e.f'
       >>>

    """

    as_dir  = property (lambda s : s._as_dir  (s.name))
    as_file = property (lambda s : s._as_file (s.name))

    def __init__ (self, name, * defaults, ** kw) :
        """Constructs the filename from the `name' and the optional `defaults'
           for `name', `directory', and `extension'. Default types that are
           already specified are ignored.

           name         name of the file specifying one or more of the
                        components `directory', `base', and `ext'

           defaults     arbitrary number of strings (or Filenames) with
                        defaults for `directory', `base', and `ext'

                        (if a default should just define a directory, it must
                        end with a directory separator -- otherwise its last
                        part will be interpreted as `base')

           default_dir  specify a default directory (this string can be
                        specified with or without trailing directory separator)

           absolute     force name to be absolute

           default_rel  Interpret relative name relative to
                        default_dir (instead of to current working directory)

           For example:

           >>> f=Filename ("spam.py")
           >>> f.name
           'spam.py'

           >>> f=Filename ("spam.py", "/usr/local/src")
           >>> f.name
           '/usr/local/spam.py'

           >>> f=Filename ("spam.py", "/usr/local/src/")
           >>> f.name
           '/usr/local/src/spam.py'

           >>> f=Filename (".pyo", "spam.py", "/usr/local/src/")
           >>> f.name
           '/usr/local/src/spam.pyo'

           >>> f=Filename ("../spam.py", "/usr/local/src/")
           >>> f.name
           '../spam.py'

           >>> f=Filename ("spam.py", default_dir = "/usr/local/src")
           >>> f.name
           '/usr/local/src/spam.py'

           >>> f=Filename ("spam.py")
           >>> f.directory == TFL.sos.getcwd ()
           0

           >>> f=Filename ("spam.py", absolute=1)
           >>> f.directory == TFL.sos.getcwd ()
           1

           >>> f=Filename ("../spam.py", "/usr/local/src/", default_rel=1)
           >>> f.name
           '/usr/local/spam.py'

        """
        if isinstance (name, Filename) :
            name = name.name
        path         = TFL.sos.path
        default_dir  = kw.get ("default_dir")
        absolute     = kw.get ("absolute")
        default_rel  = kw.get ("default_rel") and not path.isabs (name)
        (self.directory, bname) = path.split (name)
        if name.endswith (TFL.sos.sep) :
            ### fix bug in Win32 Python 1.5.1
            ### XXX is this still necessary ???
            self.directory = path.join (self.directory, bname)
            bname          = ""
        (self.base, self.ext) = path.splitext (bname)
        if default_dir :
            if isinstance (default_dir, (str, unicode)) :
                default_dir = self._as_dir (default_dir)
            defaults = (default_dir, ) + defaults
        for default in defaults :
            if isinstance (default, (str, unicode)) :
                default = Filename (default)
            defd = default.directory
            if defd :
                if not self.directory :
                    self.directory = defd
                elif default_rel :
                    self.directory = path.join (defd, self.directory)
                    default_rel    = 0
            if not self.base :
                self.base = default.base
            if not self.ext :
                self.ext  = default.ext
        self.base_ext = self.base + self.ext
        if absolute :
            self.make_absolute ()
        else :
            if self.directory :
                ### in Python 2.0, path.normpath ("") returns "."
                self.directory = path.normpath (self.directory)
            self.name = path.join (self.directory, self.base_ext)
    # end def __init__

    if    hasattr (TFL.sos.path, "abspath") :
        def abs_directory (self) :
            """Return the directory name converted to absolute path string."""
            result = TFL.sos.path.abspath (self.directory)
            if (not result) :
                result = TFL.sos.getcwd ()
            return result
        # end def abs_directory
    else :
        def abs_directory (self) :
            """Return the directory name converted to absolute path string."""
            result = self.directory
            if (not result) or (result == TFL.sos.curdir) :
                result = TFL.sos.getcwd ()
            return result
        # end def abs_directory
    # end if hasattr (TFL.sos.path, "abspath")

    def abs_name (self) :
        """Return the absolute filename corresponding to `self'."""
        return TFL.sos.path.join (self.abs_directory (), self.base_ext)
    # end def abs_name

    def _as_dir (cls, name) :
        path = TFL.sos.path
        for sep in (path.sep, path.altsep) :
            if sep and name.endswith (sep) :
                break
        else :
            name = "%s%s" % (name, path.sep)
        return name
    _as_dir = classmethod (_as_dir)

    def _as_file (cls, name) :
        path = TFL.sos.path
        for sep in (path.sep, path.altsep) :
            if sep and name.endswith (sep) :
                name = name [:-len (sep)]
                break
        return name
    _as_file = classmethod (_as_file)

    def directories (self) :
        return filter (None, self.directory.split (TFL.sos.sep))
    # end def directories

    def make_absolute (self) :
        """Make filename absolute"""
        self.directory = self.abs_directory ()
        self.name      = self.abs_name      ()
    # end def make_absolute

    def real_directory (self) :
        """Return the absolute directory name after resolving all
           symlinks.
        """
        result = self.abs_directory ()
        if hasattr (TFL.sos.path, "realpath") :
            result = TFL.sos.path.realpath (result)
        return result
    # end def real_directory

    def real_name (self) :
        """Return the absolute filename corresponding to `self'
           after resolving all symlinks.
        """
        return TFL.sos.path.join (self.real_directory (), self.base_ext)
    # end def real_name

    def relative_to (self, other) :
        """Returns `self' converted to a path relative to `other' (empty, if
           that's not possible)

           For example:

           >>> f=Filename ("/a/b/c/xxx.x")
           >>> g=Filename ("/a/b/d/yyy.y")
           >>> f.relative_to (g)
           '../c/xxx.x'
           >>> g.relative_to (f)
           '../d/yyy.y'
        """
        if not other :
            return ""
        self   = Filename (self,  absolute = 1)
        other  = Filename (other, absolute = 1)
        pairs  = paired (self.directories (), other.directories ())
        i      = 0
        for (s, o) in pairs :
            if (  s is None or o is None
               or self.normalized (s) != self.normalized (o)
               ) :
                break
            i = i + 1
        if not i :
            return ""
        differences = pairs  [i:]
        up          = [".." for (s, o) in differences if o]
        down        = [s    for (s, o) in differences if s]
        return "/".join (((up + down) or ["."]) + [self.base_ext])
    # end def relative_to

    def __cmp__ (self, other) :
        if isinstance (other, Filename) :
            return cmp (self.name, other.name)
        return cmp (self.name, other)
    # end def __cmp__

    def __hash__ (self) :
        return hash (self.name)
    # end def __hash__

    def __nonzero__ (self) :
        return len (self.base)
    # end def __nonzero__

    def __repr__ (self) :
        """Returns a string representation of the Filename object"""
        return "%s (%s)" % (self.__class__.__name__, self.name)
    # end def __repr__

    def __str__ (self) :
        """Returns the filename as string representation of the filename"""
        return "%s (%s, %s, %s)" % \
               (self.name, self.directory, self.base, self.ext)
    # end def __str__

    normalized = staticmethod (identity)

    if TFL.Environment.system == "posix" :
        posixified = staticmethod (identity)
    elif TFL.Environment.system == "win32" :
        normalized = staticmethod (str.lower)

        def posixified (filename) :
            """Return `filename` in posix syntax"""
            return filename.replace ("\\", "/")
        posixified = staticmethod (posixified)
    else :
        def posixified (filename) :
            raise NotImplementedError, \
              ( "Function Filename.posixified for system %s"
              % TFL.Environment.system
              )
        posixified = staticmethod (posixified)
    # end if TFL.Environment.system

# end class Filename

class Dirname (Filename) :
    """Represents a directory name.

       Examples :

        >>> g=Dirname ('p/xyz.ddb/')
        >>> g
        Dirname (p/xyz.ddb/)
        >>> g=Dirname ('p/xyz.ddb')
        >>> g
        Dirname (p/xyz.ddb/)
        >>> g.base_ext
        'xyz.ddb'
        >>> g.base
        'xyz.ddb'
        >>> g.ext
        ''
        >>> g = Dirname (__file__)
        >>> g.name.endswith ('lib/python/_TFL/')
        True
    """

    def __init__ (self, name, ** kw) :
        if isinstance (name, Filename) :
            name = name.name
        path = TFL.sos.path
        if path.isfile (name) and not path.isdir (name) :
            name, _ = path.split (name)
        self.__super.__init__ (self._as_dir (name), ** kw)
        if self.name :
            dirs = self.directories ()
            if dirs :
                self.base_ext = self.base = dirs [-1]
    # end def __init__

# end class Dirname

if __name__ != "__main__" :
    TFL._Export ("*")
### __END__ TFL.Filename
