# -*- coding: utf-8 -*-
from unittest import TestCase
from papylon.checker import PropChecker
from papylon.prop import Prop
from papylon.arbitrary import arb_int


class PropCheckerTest(TestCase):
    def test_given_count_as_10_when_PropChecker_check_a_propety_then_the_property_runs_10_times(self):
        sut = PropChecker(10)
        result = sut.check(Prop([arb_int()], lambda x: x + x == x * 2))
        assert result.success + result.failure == 10
        assert result.success == 10
        assert result.failure == 0

    def test_given_no_argument_for_instantiation_of_PropCheck_when_PropChecker_check_a_property_then_the_property_runs_100_times(self):
        sut = PropChecker()
        result = sut.check(Prop([arb_int(), arb_int()], lambda x, y: x + y == y + x))
        assert result.success + result.failure == 100
        assert result.success == 100
        assert result.failure == 0

    def test_given_exceptional_property_when_PropCheck_the_property_then_CheckResult_has_no_None_exceptions(self):
        sut = PropChecker()
        result = sut.check(Prop([arb_int()], lambda x: 0/x == x/0))
        assert result.success == 0
        assert result.failure == 0
        assert len(result.exceptions) == 1
        assert result.exceptions['ZeroDivisionError'] == 100