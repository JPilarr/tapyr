# -*- coding: iso-8859-1 -*-
# Copyright (C) 2004 TTTech Computertechnik AG. All rights reserved
# Schönbrunnerstraße 7, A--1040 Wien, Austria. office@tttech.com
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
#    TFL.SDG.C._Test
#
# Purpose
#    Module test for the C-SDG.
#
# Revision Dates
#    10-Aug-2004 (MG) Creation
#    ««revision-date»»···
#--

"""
>>> NL = chr (10)
>>> v = C.Var ("int", "test", 2)
>>> print NL.join (v.as_c_code ())
int test = 2;
>>> v = C.Var (name = "test", type = "short", description = "desc")
>>> print NL.join (v.as_c_code ())
short test; /* desc                                                                   */

>>> c = C.Comment ("This is a comment", stars = 2)
>>> print NL.join (c.as_c_code ())
/** This is a comment                                                      **/
>>> c = C.Comment ("And now a multi line", "comment with 3 stars", stars = 3)
>>> print NL.join (c.as_c_code ())
/*** And now a multi line                                                   ***/
/*** comment with 3 stars                                                   ***/

>>> f = C.Function ("int", "func", "int foo, short bar")
>>> print NL.join (f.as_c_code ()).strip ()
int func
    ( int foo
    , short bar
    )
{
}

>>> f = C.Function ( "int", "func", "int foo, short bar"
...                , description = "A function description"
...                , explanation = "A function explanation"
...                )
>>> print NL.join (f.as_c_code ()).strip ()
int func
    ( int foo
    , short bar
    )
    /*** A function description                                                 ***/
{
    /*** A function explanation                                                 ***/
}

>>> f = C.Function ( "int", "func", "")
>>> f.add (C.For ("i = 0", "i++", "i < 10"))
>>> print NL.join (f.as_c_code ()).strip ()
int func (void)
{
    for (i = 0; i++; i < 10)
      {
      }
}

>>> print NL.join (f.as_h_code ()).strip ()
int func (void);

>>> f = C.Function ( "int", "func", "")
>>> f.add ("i = 0")
>>> f.add (C.While ("i < 10", "i++"))
>>> f.add (C.Do_While ("i > 0", "i--"))
>>> print NL.join (f.as_c_code ()).strip ()
int func (void)
{
    i = 0;
    while (i < 10)
      {
        i++;
      }
    do
      {
        i--;
      }
    while (i > 0)
}

>>> f = C.Function ( "int", "if_tests", "")
>>> f.add (C.If ("i > 0", '''error ("i has the wrong value")'''))
>>> if_s = C.If ("i < 0", "cont ()")
>>> f.add (if_s)
>>> if_s.then.add ('''next_call ("in then path")''')
>>> if_s.add (C.Else ('''error ("in else path")'''))
>>> if_e = C.If ("i < 0", "cont ()")
>>> f.add (if_e)
>>> if_e.add (C.Elseif ("y > 0", '''error ("in elseif path")'''))
>>> if_e.add (C.Else ('''error ("in else path")'''))
>>> print NL.join (f.as_c_code ()).strip ()
int if_tests (void)
{
    if (i > 0)
      {
        error ("i has the wrong value");
      }
    if (i < 0)
      {
        cont ();
        next_call ("in then path");
      }
    else
      {
        error ("in else path");
      }
    if (i < 0)
      {
        cont ();
      }
    else if (y > 0)
      {
        error ("in elseif path");
      }
    else
      {
        error ("in else path");
      }
}

>>> f = C.Function ( "void", "switch_test", "")
>>> f.add ( C.Switch ( "quuux"
...                  , C.Case ("1", "a = 0; b = 2")
...                  , C.Case ("2", "a = 10; b = 20")
...                  , C.Default_Case ("hugo ()")
...                  )
...       )
>>> print NL.join (f.as_c_code ()).strip ()
void switch_test (void)
{
    switch (quuux)
      {
        case 1 :
            a = 0;
            b = 2;
            break;
        case 2 :
            a = 10;
            b = 20;
            break;
        default :
            hugo ();
      }
}

>>> t = C.Typedef ("unsigend long", "ubyte4")
>>> print NL.join (t.as_c_code ()).strip ()
typedef unsigend long ubyte4;
>>> s = C.Struct ("my_struct")
>>> s.add ("ubyte4 field_1")
>>> s.add ("sbyte2 field_2_s")
>>> t = C.Typedef (s, "my_struct")
>>> print NL.join (t.as_c_code ()).strip ()
typedef struct _my_struct
  {
    ubyte4 field_1;
    sbyte2 field_2_s;
  } my_struct;

>>> s = C.Struct ("my_struct_stand", standalone = True)
>>> s.add ("ubyte4 field_1")
>>> s.add ("sbyte2 field_2_s")
>>> print NL.join (s.as_c_code ()).strip ()
struct _my_struct_stand
  {
    ubyte4 field_1;
    sbyte2 field_2_s;
  };

>>> s = C.Struct ( "TDFT_Sign_Mask"
...              , "unsigned long bit_mask    = 42 // mask for value"
...              , "unsigned long extend_mask // mask for sign extension"
...              )
>>> a1 = C.Array ("int", "ar", 2, init = (0, 1), static = True)
>>> a2 = C.Array ( "TDFT_Sign_Mask", "fubars", 2
...              , init = [ dict (bit_mask = 57, extend_mask = 137)
...                       , dict (bit_mask = 142, extend_mask = -1)
...                       ]
...              )
>>> print NL.join ([l.rstrip () for l in a1.as_c_code ()])
static int ar [2] =
  { 0 /* [0]                                                                    */
  , 1 /* [1]                                                                    */
  };
>>> print NL.join ([l.rstrip () for l in a2.as_c_code ()])
TDFT_Sign_Mask fubars [2] =
  {
    { 57 /* bit_mask                                                               */
    , 137 /* extend_mask                                                            */
    } /* [0]                                                                    */
  ,
    { 142 /* bit_mask                                                               */
    , -1 /* extend_mask                                                            */
    } /* [1]                                                                    */
  };

>>> d = dict (bit_mask = 42, extend_mask = 24)
>>> v = C.Var (name = "stuct_var", type = "TDFT_Sign_Mask", init_dict = d)
>>> print NL.join ([l.rstrip () for l in v.as_c_code ()])
TDFT_Sign_Mask stuct_var =
  { 42 /* bit_mask                                                               */
  , 24 /* extend_mask                                                            */
  };

>>> a = C.Array ("int", "int_array", bounds = 2)
>>> s = C.Struct ("test_struct", "ubyte1 field_1", "int field_2 [2]")
>>> t = C.Typedef (s, "my_type")
>>> print NL.join ([l.rstrip () for l in t.as_c_code ()])
typedef struct _test_struct
  {
    ubyte1 field_1;
    int field_2 [2];
  } my_type;
"""

### missing tests
###   - #Define
###   - #Macro
###   - #ifdef
###   - #ifndef
###   - Sys_Include/App_Include
###   - #else
###   - #elseif

import  U_Test
from   _TFL._SDG._C.import_C import C

def _unit_test () :
    class Test_Case (U_Test.Case) :
        ### Each test case is implemented by a method
        ### starting with `check_'

        def check_xxx (self) :
            pass
        # end def check_xxx

    # end class Test_Case

    ts = U_Test.make_suite (Test_Case, "check_")
    U_Test.Runner ().run (ts)
# end def _unit_test

def _doc_test () :
    return U_Test.run_module_doc_tests ("_TFL._SDG._C._Test")
# end def _doc_test

def _test () :
    _unit_test ()
    _doc_test  ()
# end def _test

if __name__ == "__main__" :
    _test ()
### __END__ TFL.SDG.C._Test
