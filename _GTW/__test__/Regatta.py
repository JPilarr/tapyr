# -*- coding: utf-8 -*-
# Copyright (C) 2010-2014 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
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
#    GTW.__test__.Regatta
#
# Purpose
#    Test Regatta creation and querying
#
# Revision Dates
#    30-Apr-2010 (CT) Creation
#     9-Sep-2011 (CT) Test for `Q.RAW.left.date.start` added
#    15-Nov-2011 (CT) Add tests for `sorted_by` and `sort_key`
#    19-Mar-2012 (CT) Adapt to `Boat_Class.name.ignore_case` now being `True`
#    19-Mar-2012 (CT) Adapt to reification of `SRM.Handicap`
#    29-Mar-2012 (CT) Add test for cached role `regattas`
#    12-Oct-2012 (CT) Adapt to repr change of `An_Entity`
#    ««revision-date»»···
#--

_test_code = """
    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...
    >>> SRM = scope.SRM
    >>> PAP = scope.PAP
    >>> p = PAP.Person ("Tanzer", "Christian")
    >>> bc  = SRM.Boat_Class (u"Optimist", max_crew = 1)
    >>> ys  = SRM.Handicap ("Yardstick")
    >>> rev = SRM.Regatta_Event (u"Himmelfahrt", ("20080501", ), raw = True)
    >>> rev.epk_raw
    (u'Himmelfahrt', (('finish', u'2008/05/01'), ('start', u'2008/05/01')), 'SRM.Regatta_Event')
    >>> SRM.Regatta_Event.instance (* rev.epk_raw, raw = True)
    SRM.Regatta_Event (u'himmelfahrt', (u'2008/05/01', u'2008/05/01'))
    >>> SRM.Regatta_Event.instance (* rev.epk)
    SRM.Regatta_Event (u'himmelfahrt', (u'2008/05/01', u'2008/05/01'))
    >>> reg = SRM.Regatta_C (rev.epk_raw, boat_class = bc.epk_raw, result = ("2008/05/01 17:21", ), raw = True)
    >>> reg.epk_raw
    ((u'Himmelfahrt', (('finish', u'2008/05/01'), ('start', u'2008/05/01')), 'SRM.Regatta_Event'), (u'Optimist', 'SRM.Boat_Class'), 'SRM.Regatta_C')
    >>> SRM.Regatta_C.instance (* reg.epk_raw, raw = True)
    SRM.Regatta_C ((u'himmelfahrt', (u'2008/05/01', u'2008/05/01')), (u'optimist', ))
    >>> SRM.Regatta_C.instance (* reg.epk)
    SRM.Regatta_C ((u'himmelfahrt', (u'2008/05/01', u'2008/05/01')), (u'optimist', ))
    >>> reh = SRM.Regatta_H (rev.epk_raw, ys,  raw = True)
    >>> reh.epk_raw
    ((u'Himmelfahrt', (('finish', u'2008/05/01'), ('start', u'2008/05/01')), 'SRM.Regatta_Event'), (u'Yardstick', 'SRM.Handicap'), 'SRM.Regatta_H')
    >>> SRM.Regatta_H.instance (* reh.epk_raw, raw = True)
    SRM.Regatta_H ((u'himmelfahrt', (u'2008/05/01', u'2008/05/01')), (u'yardstick', ))
    >>> SRM.Regatta_H.instance (* reh.epk)
    SRM.Regatta_H ((u'himmelfahrt', (u'2008/05/01', u'2008/05/01')), (u'yardstick', ))

    >>> reg.result
    SRM.Regatta_Result ('2008/05/01 17:21:00')

    >>> TFL.user_config.time_zone = None
    >>> reg.__class__.result.E_Type.date.as_rest_cargo_ckd (reg.result)
    '2008-05-01T17:21:00+00:00'
    >>> reg.__class__.result.E_Type.date.as_rest_cargo_raw (reg.result)
    '2008/05/01 17:21:00'

    >>> TFL.user_config.time_zone = "Europe/Vienna"
    >>> reg.__class__.result.E_Type.date.as_rest_cargo_ckd (reg.result)
    '2008-05-01T19:21:00+02:00'
    >>> reg.__class__.result.E_Type.date.as_rest_cargo_raw (reg.result)
    '2008/05/01 19:21:00'

    >>> TFL.user_config.time_zone = "America/New_York"
    >>> reg.__class__.result.E_Type.date.as_rest_cargo_ckd (reg.result)
    '2008-05-01T13:21:00-04:00'
    >>> reg.__class__.result.E_Type.date.as_rest_cargo_raw (reg.result)
    '2008/05/01 13:21:00'

    >>> SRM.Regatta.query_s (Q.RAW.left.date.start == "2008/05/01").all ()
    [SRM.Regatta_C ((u'himmelfahrt', (u'2008/05/01', u'2008/05/01')), (u'optimist', )), SRM.Regatta_H ((u'himmelfahrt', (u'2008/05/01', u'2008/05/01')), (u'yardstick', ))]

    >>> print reg.sorted_by
    <Sorted_By: Getter function for `.left.name`, Getter function for `.left.date.start`, Getter function for `.left.date.finish`, Getter function for `.boat_class.name`>
    >>> print reh.sorted_by
    <Sorted_By: Getter function for `.left.name`, Getter function for `.left.date.start`, Getter function for `.left.date.finish`, Getter function for `.boat_class.name`>

    >>> sk = TFL.Sorted_By (scope.MOM.Id_Entity.sort_key)
    >>> print sk (reg)
    (('tuple', (('unicode', u'himmelfahrt'), ('date', datetime.date(2008, 5, 1)), ('date', datetime.date(2008, 5, 1)), ('unicode', u'optimist'))),)
    >>> print sk (reh)
    (('tuple', (('unicode', u'himmelfahrt'), ('date', datetime.date(2008, 5, 1)), ('date', datetime.date(2008, 5, 1)), ('unicode', u'yardstick'))),)

    >>> SRM.Regatta.query_s (Q.RAW.left.date.start == "2008/05/01").order_by (sk).all ()
    [SRM.Regatta_C ((u'himmelfahrt', (u'2008/05/01', u'2008/05/01')), (u'optimist', )), SRM.Regatta_H ((u'himmelfahrt', (u'2008/05/01', u'2008/05/01')), (u'yardstick', ))]

    >>> scope.MOM.Id_Entity.query_s ().order_by (sk).all ()
    [SRM.Regatta_Event (u'himmelfahrt', (u'2008/05/01', u'2008/05/01')), SRM.Regatta_C ((u'himmelfahrt', (u'2008/05/01', u'2008/05/01')), (u'optimist', )), SRM.Regatta_H ((u'himmelfahrt', (u'2008/05/01', u'2008/05/01')), (u'yardstick', )), SRM.Boat_Class (u'optimist'), PAP.Person (u'tanzer', u'christian', u'', u''), SRM.Handicap (u'yardstick')]

    >>> for x in scope.MOM.Id_Entity.query_s ().order_by (sk) :
    ...    print x, NL, "   ", sk (x)
    (u'himmelfahrt', (u'2008/05/01', u'2008/05/01'))
        (('tuple', (('unicode', u'himmelfahrt'), ('date', datetime.date(2008, 5, 1)), ('date', datetime.date(2008, 5, 1)))),)
    ((u'himmelfahrt', (u'2008/05/01', u'2008/05/01')), (u'optimist', ))
        (('tuple', (('unicode', u'himmelfahrt'), ('date', datetime.date(2008, 5, 1)), ('date', datetime.date(2008, 5, 1)), ('unicode', u'optimist'))),)
    ((u'himmelfahrt', (u'2008/05/01', u'2008/05/01')), (u'yardstick', ))
        (('tuple', (('unicode', u'himmelfahrt'), ('date', datetime.date(2008, 5, 1)), ('date', datetime.date(2008, 5, 1)), ('unicode', u'yardstick'))),)
    (u'optimist')
        (('tuple', (('unicode', u'optimist'),)),)
    (u'tanzer', u'christian', u'', u'')
        (('tuple', (('unicode', u'tanzer'), ('unicode', u'christian'), ('unicode', u''), ('unicode', u''))),)
    (u'yardstick')
        (('tuple', (('unicode', u'yardstick'),)),)

#    ### XXX auto cached roles are currently not supported
#    ### XXX * either remove tests or re-add auto-cached roles and fix tests
#    >>> sorted (SRM.Regatta.acr_map.values ())
#    [<Link_Cacher_n (GTW.OMP.SRM.Regatta) event --> regattas>]
#    >>> sorted (SRM.Regatta_C.acr_map.values ())
#    [<Link_Cacher_n (GTW.OMP.SRM.Regatta_C) event --> regattas>]
#    >>> sorted (SRM.Regatta_H.acr_map.values ())
#    [<Link_Cacher_n (GTW.OMP.SRM.Regatta_H) event --> regattas>]

    >>> crs = SRM.Regatta_Event.regattas
    >>> print crs, ":", crs.Ref_Type.type_name
    Link_Ref_List `regattas` : SRM.Regatta

    >>> sorted (rev.regattas)
    [SRM.Regatta_C ((u'himmelfahrt', (u'2008/05/01', u'2008/05/01')), (u'optimist', )), SRM.Regatta_H ((u'himmelfahrt', (u'2008/05/01', u'2008/05/01')), (u'yardstick', ))]

"""

from _GTW.__test__.model import *
NL = chr (10)

import _TFL.User_Config

__test__ = Scaffold.create_test_dict (_test_code)

### __END__ GTW.__test__.Regatta
