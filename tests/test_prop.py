# -*- coding: utf-8 -*-
from papylon.prop import Prop, for_all
from papylon.arbitrary import arb_int, arb_float


def test_when_Prop_execute_runs_right_property_then_succeeds():
    sut = Prop([arb_int()], lambda x: x + x == x * 2)
    actual = sut.execute()
    assert actual.has_finished()
    _, _, is_valid = actual.finished
    assert is_valid
    assert not actual.has_stopped()


def test_when_Prop_execute_runs_wrong_property_then_fails():
    sut = Prop([arb_int()], lambda x: x - 1 == 1 - x)
    actual = sut.execute()
    assert actual.has_finished()
    _, _, is_valid = actual.finished
    assert not is_valid
    assert not actual.has_stopped()


def test_given_a_property_which_will_raise_exception_when_Prop_execute_runs_the_property_then_the_prop_should_be_stopped():
    sut = Prop([arb_int(), arb_int()], lambda x, y: x * y == (x + y) / 0)
    actual = sut.execute()
    assert not actual.has_finished()
    assert actual.has_stopped()
    _, _, error = actual.stopped
    assert type(error) == ZeroDivisionError


def test_when_Prop_from_for_all_function_act_as_a_property():
    sut = for_all([arb_float(), arb_float()], lambda x, y: x + y == y + x)
    actual = sut.execute()
    assert actual.has_finished()
    _, _, is_valid = actual.finished
    assert is_valid
    assert not actual.has_stopped()