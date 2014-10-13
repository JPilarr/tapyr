# -*- coding: utf-8 -*-
# Copyright (C) 2012-2013 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package GTW.OMP.Auth.
# 
# This module is licensed under the terms of the BSD 3-Clause License
# <http://www.c-tanzer.at/license/bsd_3c.html>.
# #*** </License> ***********************************************************#
#
#++
# Name
#    GTW.OMP.Auth.graph
#
# Purpose
#    Graph describing Auth (partial) object model
#
# Revision Dates
#    24-Sep-2012 (CT) Creation
#    26-Sep-2012 (CT) Fix typo in `_Export`
#     7-May-2013 (CT) Add `Person_has_Account`, remove `_Account_Action_`
#    13-Jun-2013 (CT) Remove `PNS_Aliases`
#    ««revision-date»»···
#--

from   __future__ import absolute_import, division, print_function, unicode_literals

from   _GTW                   import GTW
from   _MOM                   import MOM
from   _TFL                   import TFL

import _GTW._OMP._SRM

from   _MOM._Graph.Spec       import Attr, Child, ET, IS_A, Role, Skip

import _MOM._Graph.Command
import _MOM._Graph.Entity

from   _TFL._D2               import Cardinal_Direction as CD
from   _TFL.I18N              import _, _T

def graph (app_type) :
    result = MOM.Graph.Spec.Graph \
        ( app_type
        , ET.Auth.Account_in_Group
            ( Role.left
                ( offset = CD.W
                )
            , Role.right
                ( offset = CD.E
                )
            )
        , desc  = _T ("Graph displaying Auth partial object model")
        , title = _T ("Auth graph")
        )
    if hasattr (GTW.OMP, "PAP") and hasattr (GTW.OMP.PAP, "Person_has_Account"):
        result ["Auth.Account"]._add \
            ( ET.PAP.Person_has_Account
                ( Role.left
                    ( offset       = CD.S)
                , Role.right
                    ( guide_offset = 1.0
                    )
                , offset      = CD.S
                )
            )
    return result
# end def graph

class Command (MOM.Graph.Command) :

    @property
    def PNS (self) :
        return GTW.OMP.Auth
    # end def PNS

# end class Command

if __name__ != "__main__" :
    GTW.OMP.Auth._Export ("*")
else :
    import _GTW._OMP._Auth.import_Auth
    Command () ()
### __END__ GTW.OMP.Auth.graph
