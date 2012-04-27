# -*- coding: iso-8859-15 -*-
# Copyright (C) 2010-2012 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
# This module is part of the package GTW.OMP.SRM.
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
#    GTW.OMP.SRM.Boat_in_Regatta
#
# Purpose
#    Boat racing in a regatta
#
# Revision Dates
#    19-Apr-2010 (CT) Creation
#    10-May-2010 (CT) `place` added
#     6-Sep-2010 (CT) `race_results` removed (now implemented as `Link1`)
#    20-Sep-2010 (CT) `rank` added
#    14-Oct-2010 (CT) `Init_Only_Mixin` added to `registration_date`
#     1-Dec-2010 (CT) `crew` added
#    22-Sep-2011 (CT) s/A_Entity/A_Id_Entity/
#    22-Sep-2011 (CT) s/Class/P_Type/ for _A_Id_Entity_ attributes
#    18-Nov-2011 (CT) Import `unicode_literals` from `__future__`
#    26-Jan-2012 (CT) Set `Boat_in_Regatta.left.ui_allow_new`
#    27-Apr-2012 (CT) Add predicate `skipper_not_multiplexed`
#    ��revision-date�����
#--

from   __future__            import unicode_literals

from   _GTW                     import GTW
from   _MOM.import_MOM          import *

import _GTW._OMP._SRM.Boat
import _GTW._OMP._SRM.Entity
import _GTW._OMP._SRM.Regatta
import _GTW._OMP._SRM.Sailor

from   _TFL.I18N                import _, _T, _Tn

_Ancestor_Essence = GTW.OMP.SRM.Link2

class Boat_in_Regatta (_Ancestor_Essence) :
    """Boat racing in a regatta."""

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        ### Primary attributes

        class left (_Ancestor.left) :
            """Boat racing in a regatta."""

            role_type          = GTW.OMP.SRM.Boat
            ui_allow_new       = True
            auto_cache         = True

        # end class left

        class right (_Ancestor.right) :
            """Regatta a boat races in."""

            role_type          = GTW.OMP.SRM.Regatta

        # end class right

        ### Non-primary attributes

        class crew (A_Blob) :

            kind               = Attr.Cached
            Kind_Mixins        = (Attr.Computed_Set_Mixin, )
            auto_up_depends    = ("_crew", )

            def computed (self, obj) :
                scope = obj.home_scope
                return \
                    [ cm.sailor for cm in scope.SRM.Crew_Member.r_query
                        ( left = obj
                        , sort_key = TFL.Sorted_By ("key", "pid")
                        )
                    ]
            # end def computed

        # end class crew

        class place (A_Int) :
            """Place of boat in this regatta."""

            kind               = Attr.Optional
            min_value          = 1

        # end class place

        class points (A_Int) :
            """Total points of boat in this regatta."""

            kind               = Attr.Optional
            min_value          = 1

        # end class points

        class rank (A_Int) :
            """Rank of registration of boat in regatta."""

            kind               = Attr.Internal
            default            = 0

        # end class rank

        class registration_date (A_Date) :
            """Date of registration."""

            kind               = Attr.Internal
            Kind_Mixins        = (Attr.Init_Only_Mixin, )
            computed_default   = A_Date.now

        # end class registration_date

        class skipper (A_Id_Entity) :
            """Skipper of boat."""

            P_Type             = GTW.OMP.SRM.Sailor
            kind               = Attr.Required

        # end class skipper

        class other_boots_skippered (A_Blob) :
            """Other links of this `skipper` to a boat in this `regatta.event`.
            """

            kind               = Attr.Computed

            def computed (self, obj) :
                if obj is not None :
                    ETM = obj.home_scope [obj.type_name]
                    return ETM.query_s \
                        ( Q.pid           != obj.pid
                        , Q.regatta.event == obj.regatta.event
                        , Q.skipper       == obj.skipper
                        )
            # end def computed

        # end class other_boots_skippered

    # end class _Attributes

    class _Predicates (_Ancestor_Essence._Predicates) :

        _Ancestor = _Ancestor_Essence._Predicates

        class skipper_not_multiplexed (Pred.Condition) :
            """A sailor can't be skipper of more than one boat in a single
               regatta event.
            """

            kind               = Pred.Region
            assertion          = "other_boots_skippered_count == 0"
            attributes         = ("boat", "regatta", "skipper")
            bindings           = dict \
                ( other_boots_skippered_count =
                    "this.other_boots_skippered.count ()"
                )
            _xtra_added        = False

            def _add_entities_to_extra_links (self, obj, lst) :
                self.__super._add_entities_to_extra_links (obj, lst)
                if not self._xtra_added :
                    self._extra_links_d.extend \
                        (obj.other_boots_skippered.all () or ())
                    self._xtra_added = True
            # end def _add_entities_to_extra_links

        # end class skipper_not_multiplexed

    # end class _Predicates

# end class Boat_in_Regatta

if __name__ != "__main__" :
    GTW.OMP.SRM._Export ("*")
### __END__ GTW.OMP.SRM.Boat_in_Regatta
