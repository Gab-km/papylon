# -*- coding: utf-8 -*-
from papylon.prop import for_all
from papylon.arbitrary import arb_int
from papylon.checker import check

import math

p2 = for_all([arb_int()], lambda n: math.sqrt(n*n) == n)
check(p2)
