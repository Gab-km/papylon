# -*- coding: utf-8 -*-
from papylon.prop import for_all
from papylon.arbitrary import arb_list, arb_int
from papylon.checker import check

# reversed and reversed list is the same of the original list
p1 = for_all([arb_list(arb_int(), max_length=20)],
             lambda x: list(reversed(list(reversed(x)))) == x)
check(p1)
