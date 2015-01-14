# -*- coding: utf-8 -*-
def test_when_Prop_execute_runs_right_property_then_succeeds():
    from papylon.prop import Prop, PropExecutorWithoutShrink
    from papylon.arbitrary import arb_int

    sut = Prop([arb_int()], lambda x: x + x == x * 2, executor_type=PropExecutorWithoutShrink)
    actual = sut.execute()
    assert actual.has_finished()
    _, _, is_valid, _ = actual.get()
    assert is_valid
    assert not actual.has_stopped()


def test_given_PropExecutorWithShrink_then_execute_shrink_runs_wrong_property_then_finishes_in_1_second():
    from papylon.prop import PropExecutorWithShrink
    from papylon.arbitrary import arb_int
    import time

    sut = PropExecutorWithShrink([arb_int()], lambda x: x + x == x * 2 + 1, 100)
    start = time.time()
    actual = sut.execute_shrinker([1, 3])
    elapsed = time.time() - start
    assert actual.has_finished()
    _, _, is_valid, shrunk_number = actual.get()
    assert not is_valid
    assert shrunk_number >= 1
    assert not actual.has_stopped()
    assert elapsed <= 1.0


def test_given_PropExecutorWithShrink_then_execute_shrink_runs_wrong_property_then_shrinks_10_times():
    from papylon.prop import PropExecutorWithShrink
    from papylon.arbitrary import arb_int

    sut = PropExecutorWithShrink([arb_int()], lambda x: x >= 2000 or x == 0, 10)
    actual = sut.execute_shrinker([1000])
    assert actual.has_finished()
    _, _, is_valid, shrunk_number = actual.get()
    assert not is_valid
    assert shrunk_number == 10
    assert not actual.has_stopped()


def test_when_Prop_execute_runs_wrong_property_then_fails():
    from papylon.prop import Prop, PropExecutorWithoutShrink
    from papylon.arbitrary import arb_int

    sut = Prop([arb_int()], lambda x: x - 1 == 1 - x, executor_type=PropExecutorWithoutShrink)
    actual = sut.execute()
    assert actual.has_finished()
    _, _, is_valid, shrunk_number = actual.get()
    assert not is_valid
    assert shrunk_number >= 0
    assert not actual.has_stopped()


def test_given_a_property_which_fails_to_generate_when_Prop_execute_it_then_should_be_stopped_with_StopGeneration():
    from papylon.prop import Prop, PropExecutorWithoutShrink
    from papylon.arbitrary import from_gen
    from papylon.gen import choose, StopGeneration

    gen = choose(0, 100).such_that(lambda x: x > 100)
    arb = from_gen(gen)
    sut = Prop([arb], lambda x: 0 <= x * 2 <= 200, executor_type=PropExecutorWithoutShrink)
    actual = sut.execute()
    assert not actual.has_finished()
    assert actual.has_stopped()
    _, _, error = actual.get()
    assert type(error) == StopGeneration


def test_given_a_property_which_will_raise_exception_when_Prop_execute_runs_the_property_then_the_prop_should_be_stopped():
    from papylon.prop import Prop, PropExecutorWithoutShrink
    from papylon.arbitrary import arb_int

    sut = Prop([arb_int(), arb_int()], lambda x, y: x * y == (x + y) / 0, executor_type=PropExecutorWithoutShrink)
    actual = sut.execute()
    assert not actual.has_finished()
    assert actual.has_stopped()
    _, _, error = actual.get()
    assert type(error) == ZeroDivisionError


def test_when_Prop_from_for_all_function_act_as_a_property():
    from papylon.prop import for_all
    from papylon.arbitrary import arb_float

    sut = for_all([arb_float(), arb_float()], lambda x, y: x + y == y + x)
    actual = sut.execute()
    assert actual.has_finished()
    _, _, is_valid, _ = actual.get()
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
    _, _, is_valid, _ = actual.get()
    assert is_valid
    assert not actual.has_stopped()
