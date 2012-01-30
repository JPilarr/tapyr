# -*- coding: iso-8859-15 -*-
# Copyright (C) 2010-2012 Mag. Christian Tanzer All rights reserved
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
#    GTW.__test__.Boat
#
# Purpose
#    Test SRM.Boat creation and querying
#
# Revision Dates
#    27-Apr-2010 (CT) Creation
#    29-Mar-2011 (CT) Test for change of `Init_Only_Mixin` attribute added
#     9-Nov-2011 (CT) Add test for `sail_number_head` and `sail_number_tail`
#    10-Nov-2011 (CT) Add test for `Name_Clash`
#    ��revision-date�����
#--

_test_code = """
    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...
    >>> SRM = scope.SRM
    >>> SRM.Boat_Class ("Optimist", max_crew = 1)
    GTW.OMP.SRM.Boat_Class (u'Optimist')
    >>> print scope.SRM.Boat_Class.count ### 1
    1
    >>> laser = SRM.Boat_Class ("Laser", max_crew = 1)
    >>> print scope.SRM.Boat_Class.count ### 2
    2

    >>> scope.SRM.Boat_Class.query (name = u'Optimist').all ()
    [GTW.OMP.SRM.Boat_Class (u'Optimist')]
    >>> scope.SRM.Boat_Class.instance (u'Optimist')
    GTW.OMP.SRM.Boat_Class (u'Optimist')
    >>> SRM.Boat.instance_or_new (u'Optimist', u"AUT", u"1107", raw = True) ### 1
    GTW.OMP.SRM.Boat ((u'Optimist', ), u'AUT', 1107, u'')
    >>> print scope.SRM.Boat.count ### 3
    1
    >>> scope.SRM.Boat.query_s ().all ()
    [GTW.OMP.SRM.Boat ((u'Optimist', ), u'AUT', 1107, u'')]
    >>> scope.commit ()

    >>> SRM.Boat.instance_or_new (u'Optimist', u"AUT", u"1107", raw = True) ### 2
    GTW.OMP.SRM.Boat ((u'Optimist', ), u'AUT', 1107, u'')
    >>> print scope.SRM.Boat.count ### 4
    1
    >>> scope.SRM.Boat.query_s ().all ()
    [GTW.OMP.SRM.Boat ((u'Optimist', ), u'AUT', 1107, u'')]

    >>> b = SRM.Boat.instance_or_new (u'Optimist', u"AUT", u"1107", raw = True) ### 3
    >>> c = SRM.Boat (u"Optimist", None, "42", "OE", raw = True)

    >>> print scope.SRM.Boat.count ### 5
    2
    >>> scope.SRM.Boat.query_s ().all ()
    [GTW.OMP.SRM.Boat ((u'Optimist', ), '', 42, u'oe'), GTW.OMP.SRM.Boat ((u'Optimist', ), u'AUT', 1107, u'')]

    >>> print (c.sail_number, c.sail_number_head, c.sail_number_tail)
    (42, u'OE', u'42')
    >>> print (c.FO.sail_number, c.FO.sail_number_head, c.FO.sail_number_tail)
    ('42', u'OE', u'42')
    >>> print (b.sail_number, b.sail_number_head, b.sail_number_tail)
    (1107, u'', u'1107')

    >>> s1 = TFL.Sorted_By ("name")
    >>> s2 = TFL.Sorted_By ("-name")
    >>> SRM.Boat_Class.query ().order_by (s1).all ()
    [GTW.OMP.SRM.Boat_Class (u'Laser'), GTW.OMP.SRM.Boat_Class (u'Optimist')]
    >>> SRM.Boat_Class.query ().order_by (s1).order_by (s2).all ()
    [GTW.OMP.SRM.Boat_Class (u'Optimist'), GTW.OMP.SRM.Boat_Class (u'Laser')]

    >>> print SRM.Boat.sail_number.Q_Raw.EQ
    <Attr.Equal __raw_sail_number.EQ [==]>
    >>> rf = SRM.Boat.sail_number.Q_Raw.EQ ("1107")
    >>> print rf
    Q.__raw_sail_number == 1107

    >>> rf (b)
    True

    >>> getattr (b, "__raw_sail_number", "No raw value???")
    u'1107'

    >>> bq = SRM.Boat.query_s ()
    >>> bq.all ()
    [GTW.OMP.SRM.Boat ((u'Optimist', ), '', 42, u'oe'), GTW.OMP.SRM.Boat ((u'Optimist', ), u'AUT', 1107, u'')]
    >>> SRM.Boat.query_s (SRM.Boat.sail_number.Q_Raw.EQ ("1107")).all ()
    [GTW.OMP.SRM.Boat ((u'Optimist', ), u'AUT', 1107, u'')]
    >>> SRM.Boat.query_s (SRM.Boat.sail_number.Q_Raw.AC ("11")).all ()
    [GTW.OMP.SRM.Boat ((u'Optimist', ), u'AUT', 1107, u'')]

    >>> print scope.SRM.Boat.count ### 6
    2

    >>> b.set (left = laser)
    Traceback (most recent call last):
      ...
    AttributeError: Init-only attribute `GTW.OMP.SRM.Boat.left` cannot be changed from `(u'Optimist')` to `(u'Laser')` after object creation

    >>> print scope.SRM.Boat.count ### 7
    2

    >>> d = SRM.Boat (SRM.Boat_Class ("Optimist", max_crew = 1), "AUT", "1134")
    Traceback (most recent call last):
      ...
    Name_Clash: new definition of GTW.OMP.SRM.Boat_Class (u'Optimist') clashes with existing GTW.OMP.SRM.Boat_Class (u'Optimist')

    >>> scope.destroy ()

"""

from _GTW.__test__.model import *

__test__ = Scaffold.create_test_dict (_test_code)

### __END__ GTW.__test__.Boat
