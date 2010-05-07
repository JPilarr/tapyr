# -*- coding: iso-8859-1 -*-
# Copyright (C) 2010 Martin Glueck All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. martin@mangari.org
# ****************************************************************************
# This module is part of the package GTW.__test__.
#
# This module is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this module. If not, see <http://www.gnu.org/licenses/>.
# ****************************************************************************
#
#++
# Name
#    GTW.__test__.model
#
# Purpose
#    Helper function to create the App-Type for other tests
#
# Revision Dates
#    21-Apr-2010 (MG) Creation
#    27-Apr-2010 (CT) `MOM.Scaffold` factored
#    ��revision-date�����
#--

from   _GTW                   import GTW
from   _MOM                   import MOM
from   _TFL                   import TFL

from   _MOM.Product_Version   import Product_Version, IV_Number
from   _TFL                   import sos

import _GTW._OMP._Auth.import_Auth
import _GTW._OMP._EVT.import_EVT
import _GTW._OMP._PAP.import_PAP
import _GTW._OMP._SRM.import_SRM
import _GTW._OMP._SWP.import_SWP
import _MOM.Scaffold
import _TFL.Filename

GTW.Version = Product_Version \
    ( productid           = u"MOM/GTW Test Cases"
    , productnick         = u"MOM-Test"
    , productdesc         = u"Test application for the regressiontest"
    , date                = "21-Apr-2010 "
    , major               = 0
    , minor               = 1
    , patchlevel          = 2
    , author              = u"Martin Glueck/Christian Tanzer"
    , copyright_start     = 2010
    , db_version          = IV_Number
        ( "db_version"
        , ("MOMT", )
        , ("MOMT", )
        , program_version = 1
        , comp_min        = 0
        , db_extension    = ".momt"
        )
    )

class Scaffold (MOM.Scaffold) :

    ANS         = GTW
    nick        = u"MOMT"
    PNS_Aliases = dict \
        ( Auth  = GTW.OMP.Auth
        , EVT   = GTW.OMP.EVT
        , PAP   = GTW.OMP.PAP
        , SRM   = GTW.OMP.SRM
        , SWP   = GTW.OMP.SWP
        )

# end class Scaffold

Scope = Scaffold.scope

if __name__ == "__main__" :
    TFL.Environment.exec_python_startup ()
    db_prefix = sos.environ.get ("GTW_DB_prefix", None)
    scope = Scope (db_prefix)
### __END__ GTW.__test__.model
