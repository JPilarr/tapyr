# -*- coding: utf-8 -*-
# Copyright (C) 2005-2009 Martin Glück. All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. office@spannberg.com
# ****************************************************************************
#
# This module is licensed under the terms of the BSD 3-Clause License
# <http://www.c-tanzer.at/license/bsd_3c.html>.
# ****************************************************************************
#
#++
# Name
#    TGL.TKT.GTK.Model
#
# Purpose
#    Tree/List data models required by the Tree_View widget
#
# Revision Dates
#    27-Mar-2005 (MG) Creation
#    16-May-2005 (MG) `Sort_Model` added
#    16-May-2005 (MG) `iter_to_object` added
#     5-Jun-2005 (MG) `iter_to_object` removed, `ui_object` added
#     5-Jun-2005 (MG) `Dict_Mapper` and `Model_Proxy_Mapper` removed
#     5-Jun-2005 (MG) `add_empty` added
#     5-Jun-2005 (MG) `Filter_Model` and friends added
#     5-Jun-2005 (MG) `Sort_Model` streamlined
#     6-Jun-2005 (MG) `AC` added to `Sort_Model` and `Filter_Model`
#     7-Jun-2005 (MG) `clear` added and `remove` fixed
#    11-Jun-2005 (MG) `update` added
#    17-Jun-2005 (MG) `List_Model._add` allow `parent` as parameter
#    26-Jul-2005 (MG) Internal dict `iter` renamed to `_iter` and method
#                     `iter` added
#    28-Jul-2005 (MG) `_Iter_Mixin_` added
#    29-Jul-2005 (MG) `_Proxy_Model_`: `add` and `remove` added
#    13-Aug-2005 (MG) `Sort_Model.ui_object` and `Filter_Model.ui_object`
#                     changed to handle `path` arguments as well as `iter`
#                     arguments
#    16-Sep-2005 (MG) `add`: debug code added
#    30-Dec-2005 (MG) `Filter_Model.iter` added
#    17-Jul-2009 (CT) `_check_MRO` and `__init__` added t o`_Proxy_Model_`
#    ««revision-date»»···
#--

from   _TFL                   import TFL
from   _TGL._TKT._GTK         import GTK
import _TGL._TKT._GTK.Object
import _TGL._TKT._GTK.Constants

class _Iter_Mixin_ (object) :

    def iter_delta (self, iter, delta) :
        model = self.wtk_object
        if delta < 0 :
            path = model.get_path (iter)
            new  = path [-1] + delta
            if new < 0 :
                return None
            return model.get_iter (path [:-1] + (new, ))
        else :
            while delta and iter:
                iter   = model.iter_next (iter)
                delta -= 1
            return iter
    # end def iter_delta

# end class _Iter_Mixin_

class _Model_ (GTK.Object, _Iter_Mixin_) :
    """Root class for all `Model` (Tree/List Model, FilterModel, SortModel)"""

    GTK_Class        = None

    __gtk_properties = \
       ( GTK.SG_Property
             ("columns", get_fct_name = "get_n_columns", set = None)
       ,
       )

    def __init__ (self, * column_types, ** kw) :
        self.ui_column = kw.get ("ui_column", None)
        if "ui_column" in kw :
            del kw ["ui_column"]
        self.__super.__init__        (* column_types, ** kw)
        self._iter      = {}
    # end def __init__

    def add (self, row, after = None, ** kw) :
        try :
            iter = self._add \
                (row, after_iter = self._iter.get (after, after), ** kw)
        except :
            print "Error in adding a new row"
            for i, data in enumerate (row) :
                print "Col: %2d, value [%s] src_type [%s] gtk_type [%s]" % \
                    (i, data, data.__class__, self.wtk_object.get_column_type (i))
            raise
        if self.ui_column is not None :
            self._iter [row [self.ui_column]] = iter
        return iter
    # end def add

    def add_empty (self, reference = None, after = None, ** kw) :
        iter = self._add \
            (None, after_iter = self._iter.get (after, after), ** kw)
        if reference and self.ui_column is not None :
            self.wtk_object.set (iter, self.ui_column, reference)
        return iter
    # end def add_empty

    def clear (self) :
        for row in self.wtk_object :
            self.remove (row.iter)
    # end def clear

    def iter (self, obj) :
        return self._iter.get (obj)
    # end def iter

    def remove (self, node) :
        iter  = self._iter.get (node, node)
        child = self.wtk_object.iter_children (iter)
        while child :
            n_child = self.wtk_object.iter_next (child)
            self.remove (child)
            child = n_child
        if (   isinstance (node, GTK.gtk.TreeIter)
           and (self.ui_column is not None)
           ) :
            node = self.wtk_object.get_value (iter, self.ui_column)
        if node in self._iter :
            del self._iter    [node]
        self.wtk_object.remove (iter)
    # end def remove

    def ui_object (self, iter) :
        if self.ui_column is not None :
            try :
                return self.wtk_object [iter] [self.ui_column]
            except TypeError :
                print "==>", iter, self.ui_column
        return iter
    # end def ui_object

    def update (self, ui, row) :
        iter = self._iter.get (ui, ui)
        for index, value in enumerate (row) :
            self.wtk_object.set_value (iter, index, value)
    # end def update

    def __getitem__ (self, key) :
        return self.wtk_object [key]
    # end def __getitem__

    def __setitem__ (self, key, value) :
        self.wtk_object [key] = value
    # end def __setitem__

    def __delitem__ (self, key) :
        self.remove (self.wtk_object [key].iter)
    # end def __delitem__

    def pprint (self, sep = ":") :
        for row in self.wtk_object :
            print "\n".join (self._format_row (row, sep))
    # end def pprint

    def _format_row (self, row, sep = ":", intend = 0) :
        result = ["%s%s" % (" " * intend, sep.join (str (c) for c in row))]
        for r in row.iterchildren () :
            result.extend (self._format_row (r, sep, intend + 2))
        return result
    # end def _format_row

# end class _Model_

class List_Model (_Model_) :
    """Wrapper for the gtk.ListStore class
       >>> l = List_Model (str,int)
       >>> r0 = l.add (("Row_1", 0))
       >>> r1 = l.add (("Row_2", 1))
       >>> l.pprint ()
       Row_1:0
       Row_2:1
       >>> r1_5 = l.add (("Row_1_5", 15), after = r0)
       >>> l.pprint ()
       Row_1:0
       Row_1_5:15
       Row_2:1
       >>> del l [1]
       >>> l.pprint ()
       Row_1:0
       Row_2:1
    """

    GTK_Class    = GTK.gtk.ListStore

    def _add (self, row, after_iter, parent = None) :
        if after_iter :
            return self.wtk_object.insert_after (after_iter, row)
        else :
            return self.wtk_object.append       (row)
    # end def _add

    def has_children (self, * args, ** kw) :
        return False
    # end def has_children

# end class List_Model

class Tree_Model (_Model_) :
    """Wrapper for the gtk.TreeStore class

       >>> from _TGL._TKT._GTK.Model import *
       >>> t = Tree_Model (str,int)
       >>> p = t.add (("Test_1",     1))
       >>> c = t.add (("Test_1_1",   2), parent = p)
       >>> d = t.add (("Test_1_1_1", 3), parent = c)
       >>> t [0] [0]
       'Test_1'
       >>> t [0] [1]
       1
       >>> t [0] [1] = 2
       >>> t [0] [1]
       2
       >>> t.pprint ()
       Test_1:2
         Test_1_1:2
           Test_1_1_1:3
    """

    GTK_Class    = GTK.gtk.TreeStore

    def _add (self, row, after_iter, parent = None) :
        par_iter = self._iter.get  (parent, parent)
        if after_iter :
            return self.wtk_object.insert_after (par_iter, after_iter, row)
        else :
            return self.wtk_object.append       (par_iter, row)
    # end def _add

    def has_children (self, node) :
        iter = self._iter.get (node, node)
        return self.wtk_object.iter_has_child (iter)
    # end def has_children

# end class Tree_Model

class _Proxy_Model_ (TFL.Meta.Object, _Iter_Mixin_) :
    """Root class for all kinds of `proxy` models (sort, filter, ...)"""

    ui_column = property ( lambda s : s.model.ui_column)

    def __init__ (self, * args, ** kw) :
        self.__super.__init__  (* args, ** kw)
        _Iter_Mixin_.__init__  (self)
    # end def __init__

    @classmethod
    def _check_MRO (cls, args, kw) :
        """We know what we're doing and explicitly call
           `_Iter_Mixin_.__init__`.
        """
    # end def _check_MRO

    def add (self, * args, ** kw) :
        return self.model.add (* args, ** kw)
    # end def add

    def remove (self, * args, ** kw) :
        return self.model.remove (* args, ** kw)
    # end def remove

# end class _Proxy_Model_

class Sort_Model (_Proxy_Model_, GTK.Object) :
    """Sorts a child model"""

    GTK_Class = GTK.gtk.TreeModelSort

    def __init__ (self, child_model, AC = None) :
        self.__super.__init__ (child_model.wtk_object, AC = AC)
        self.model      = child_model
        self._functions = {}
    # end def __init__

    def set_sort_funcion (self, id, fct, data = None, destroy = None) :
        """The sort function must accept the following parameter:
             treemodel, iter1, iter2, user_data
        """
        if fct is None :
            if id in self._functions :
                del self._functions [id]
        else :
            self._functions [id] = (fct, data, destroy)
        self.wtk_object.set_sort_func (id, fct, data, destroy)
    # end def set_sort_funcion

    def sort_function (self, id) :
        return self._functions [id]
    # end def sort_function

    def ui_object (self, iter) :
        """Converts `iter` from the an tree iter of the sort model to
           an iter of the proxied model.
        """
        if not isinstance (iter, GTK.gtk.TreeIter) :
            iter = self.wtk_object.get_iter (iter)
        return self.model.ui_object \
            (self.wtk_object.convert_iter_to_child_iter (None, iter))
    # end def ui_object

    def iter (self, iter) :
        """Converts `iter` from the an tree iter of the sort model to
           an iter of the sort model.
        """
        return self.wtk_object.convert_child_iter_to_iter \
            (None, self.model.iter (iter))
    # end def iter

# end class Sort_Model

class Filter_Model (_Proxy_Model_, GTK.Object_Wrapper) :
    """Apply a filter function on the proxied model."""

    GTK_Class       = GTK.gtk.TreeModelFilter

    _wtk_delegation = GTK.Delegation \
        ( GTK.Delegator ("refilter")
        )
    def __init__ ( self
                 , child_model
                 , filter_function
                 , root       = None
                 , row_filter = False
                 , AC         = None
                 ) :
        wtk_object = child_model.wtk_object.filter_new (root)
        self.model = child_model
        self.__super.__init__ (wtk_object, AC = AC)
        self.filter_function = filter_function
        row_filter           = row_filter or self.ui_column is None
        filter_fct           = \
            (self._filter_ui, self._filter_row) [row_filter]
        self.wtk_object.set_visible_func (filter_fct)
    # end def __init__

    def _filter_row (self, wtk_model, iter, data = None) :
        row = [col for col in wtk_model [iter]]
        return self.filter_function (row)
    # end def _filter_row

    def _filter_ui (self, wtk_model, iter, data = None) :
        model = wtk_model.get_data ("ktw_object")
        ui    = model.ui_object (iter)
        if ui is None :
            ### I don't know how this is possible, but it is !
            return False
        return self.filter_function (ui)
    # end def _filter_ui

    def ui_object (self, iter) :
        if not isinstance (iter, GTK.gtk.TreeIter) :
            iter = self.wtk_object.get_iter (iter)
        return self.model.ui_object \
            (self.wtk_object.convert_iter_to_child_iter (iter))
    # end def ui_object

    def iter (self, iter) :
        """Converts `iter` from the an tree iter of the filter model to
           an iter of the sort model.
        """
        return self.wtk_object.convert_child_iter_to_iter \
            (self.model.iter (iter))
    # end def iter

# end class Filter_Model

if __name__ != "__main__" :
    GTK._Export ("*")
### __END__ TGL.TKT.GTK.Model
