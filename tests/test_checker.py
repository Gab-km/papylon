# -*- coding: utf-8 -*-
def test_given_count_as_100_when_PropChecker_check_a_propety_then_the_property_runs_100_times():
    from papylon.checker import PropChecker
    from papylon.prop import for_all
    from papylon.arbitrary import arb_int

    sut = PropChecker(100)
    result = sut.check(for_all([arb_int()], lambda x: x + x == x * 2))
    assert result.has_passed()
    (count,) = result.get()
    assert count == 100


def test_given_property_which_fails_to_generate_when_PropChecker_check_it_then_returns_generation_failure_report():
    from papylon.checker import PropChecker
    from papylon.prop import for_all
    from papylon.arbitrary import from_gen
    from papylon.gen import choose

    gen = choose(-10, 20).such_that(lambda x: -20 <= x < -10)
    arb = from_gen(gen)
    sut = PropChecker(100)
    result = sut.check(for_all([arb], lambda x: x + 2 > x))
    assert result.has_failed_to_generate()
    (run_count, trial_to_generate) = result.get()
    assert run_count == 1
    assert trial_to_generate == 100


def test_given_falsifiable_property_when_PropChecker_check_the_property_then_returns_faisified_report():
    from papylon.checker import PropChecker
    from papylon.prop import for_all
    from papylon.arbitrary import arb_int

    sut = PropChecker(100)
    result = sut.check(for_all([arb_int()], lambda x: x != 0 and x == x * (-1)))
    assert result.has_falsified()
    run_count, inputs, error = result.get()
    assert run_count == 1
    assert error is None


def test_given_exceptional_property_when_check_the_property_then_returns_falsified_report_with_exception():
    from papylon.checker import PropChecker
    from papylon.prop import for_all
    from papylon.arbitrary import arb_int

    sut = PropChecker(100)
    result = sut.check(for_all([arb_int()], lambda x: 0/x == x/0))
    assert result.has_falsified()
    run_count, inputs, error = result.get()
    assert run_count == 1
    assert error is not None


def test_given_prop_execute_which_throws_error_when_PropChecker_check_the_property_then_returns_troubled_report():
    from papylon.checker import PropChecker

    class DummyProp:
        def __init__(self, msg):
            self.msg = msg

        def execute(self):
            raise ValueError(self.msg)
    msg = "Something has been occurred."
    prop = DummyProp(msg)
    sut = PropChecker(100)
    result = sut.check(prop)
    assert result.has_troubled()
    error, ex_traceback = result.get()
    assert type(error) == ValueError
    assert error.args[0] == msg
    assert ex_traceback is not None


def test_given_count_as_0_when_PropChecker_is_instantiated_then_occurs_ValueError():
    from papylon.checker import PropChecker

    try:
        PropChecker(0)
        assert False
    except ValueError:
        assert True


def test_when_check_a_valid_property_then_it_should_run_well(capsys):
    from papylon.checker import check
    from papylon.prop import for_all
    from papylon.arbitrary import arb_int

    check(for_all([arb_int()], lambda x: x + 1 > x))
    out, _ = capsys.readouterr()
    assert out == "OK, passed 100 tests.\n"