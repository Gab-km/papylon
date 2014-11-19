# -*- coding: utf-8 -*-
import sys
from unittest import TestCase
from papylon.checker import PropChecker, check
from papylon.prop import for_all
from papylon.arbitrary import arb_int


class PropCheckerTest(TestCase):
    def test_given_count_as_100_when_PropChecker_check_a_propety_then_the_property_runs_100_times(self):
        sut = PropChecker(100)
        result = sut.check(for_all([arb_int()], lambda x: x + x == x * 2))
        assert result == "OK, passed 100 tests."

    def test_given_falsifiable_property_when_PropChecker_check_the_property_then_return_faisified_report(self):
        sut = PropChecker(100)
        result = sut.check(for_all([arb_int()], lambda x: x != 0 and x == x * (-1)))
        assert result.startswith("Falsified after 0 tests.")

    def test_given_exceptional_property_when_PropCheck_the_property_then_return_falsified_report_with_exception(self):
        sut = PropChecker(100)
        result = sut.check(for_all([arb_int()], lambda x: 0/x == x/0))
        assert result.startswith("Falsified after 0 tests.")
        assert "with exception:" in result

    def test_given_count_as_0_when_PropChecker_is_instantiated_then_occurs_ValueError(self):
        try:
            PropChecker(0)
            assert False
        except ValueError:
            assert True
