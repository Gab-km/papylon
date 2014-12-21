# -*- coding: utf-8 -*-
def test_when_Prop_execute_runs_right_property_then_succeeds():
    from papylon.prop import Prop
    from papylon.arbitrary import arb_int

    sut = Prop([arb_int()], lambda x: x + x == x * 2)
    actual = sut.execute()
    assert actual.has_finished()
    _, _, is_valid = actual.finished
    assert is_valid
    assert not actual.has_stopped()


def test_when_Prop_execute_runs_wrong_property_then_fails():
    from papylon.prop import Prop
    from papylon.arbitrary import arb_int

    sut = Prop([arb_int()], lambda x: x - 1 == 1 - x)
    actual = sut.execute()
    assert actual.has_finished()
    _, _, is_valid = actual.finished
    assert not is_valid
    assert not actual.has_stopped()


def test_given_a_property_which_fails_to_generate_when_Prop_execute_it_then_should_be_stopped_with_StopGeneration():
    from papylon.prop import Prop
    from papylon.arbitrary import from_gen
    from papylon.gen import choose, StopGeneration

    gen = choose(0, 100).such_that(lambda x: x > 100)
    arb = from_gen(gen)
    sut = Prop([arb], lambda x: 0 <= x * 2 <= 200)
    actual = sut.execute()
    assert not actual.has_finished()
    assert actual.has_stopped()
    _, _, error = actual.stopped
    assert type(error) == StopGeneration


def test_given_a_property_which_will_raise_exception_when_Prop_execute_runs_the_property_then_the_prop_should_be_stopped():
    from papylon.prop import Prop
    from papylon.arbitrary import arb_int

    sut = Prop([arb_int(), arb_int()], lambda x, y: x * y == (x + y) / 0)
    actual = sut.execute()
    assert not actual.has_finished()
    assert actual.has_stopped()
    _, _, error = actual.stopped
    assert type(error) == ZeroDivisionError


def test_when_Prop_from_for_all_function_act_as_a_property():
    from papylon.prop import for_all
    from papylon.arbitrary import arb_float

    sut = for_all([arb_float(), arb_float()], lambda x, y: x + y == y + x)
    actual = sut.execute()
    assert actual.has_finished()
    _, _, is_valid = actual.finished
    assert is_valid
    assert not actual.has_stopped()


def test_when_Prop_takes_Arbitrary_instance_with_from_gen_then_prop_can_execute_correctly():
    from papylon.prop import for_all
    from papylon.arbitrary import from_gen
    from papylon.gen import choose

    arb = from_gen(choose(0, 20))
    sut = for_all([arb], lambda x: 0 <= x <= 20)
    actual = sut.execute()
    assert actual.has_finished()
    _, _, is_valid = actual.finished
    assert is_valid
    assert not actual.has_stopped()
