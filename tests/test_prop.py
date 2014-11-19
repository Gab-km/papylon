# -*- coding: utf-8 -*-
from unittest import TestCase
from papylon.prop import Prop
from papylon.arbitrary import arb_int


class PropTest(TestCase):
    def test_when_Prop_execute_runs_right_property_then_succeeds(self):
        sut = Prop([arb_int()], lambda x: x + x == x * 2)
        actual = sut.execute()
        assert actual.done is not None
        _, _, is_valid = actual.done
        assert is_valid
        assert actual.stopped is None

    def test_when_Prop_execute_runs_wrong_property_then_fails(self):
        sut = Prop([arb_int()], lambda x: x - 1 == 1 - x)
        actual = sut.execute()
        assert actual.done is not None
        _, _, is_valid = actual.done
        assert not is_valid
        assert actual.stopped is None

    def test_given_a_property_which_will_raise_exception_when_Prop_execute_runs_the_property_then_the_prop_will_be_stopped(self):
        sut = Prop([arb_int(), arb_int()], lambda x, y: x * y == (x + y) / 0)
        actual = sut.execute()
        assert actual.done is None
        assert actual.stopped is not None
        _, _, error = actual.stopped
        assert type(error) == ZeroDivisionError
