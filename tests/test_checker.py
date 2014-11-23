# -*- coding: utf-8 -*-
from papylon.checker import PropChecker, check
from papylon.prop import for_all
from papylon.arbitrary import arb_int


def test_given_count_as_100_when_PropChecker_check_a_propety_then_the_property_runs_100_times():
    sut = PropChecker(100)
    result = sut.check(for_all([arb_int()], lambda x: x + x == x * 2))
    assert result.has_passed()
    (count,) = result.passed
    assert count == 100


def test_given_falsifiable_property_when_PropChecker_check_the_property_then_return_faisified_report():
    sut = PropChecker(100)
    result = sut.check(for_all([arb_int()], lambda x: x != 0 and x == x * (-1)))
    assert result.has_falsified()
    run_count, inputs, error = result.falsified
    assert run_count == 1
    assert error is None


def test_given_exceptional_property_when_PropCheck_the_property_then_return_falsified_report_with_exception():
    sut = PropChecker(100)
    result = sut.check(for_all([arb_int()], lambda x: 0/x == x/0))
    assert result.has_falsified()
    run_count, inputs, error = result.falsified
    assert run_count == 1
    assert error is not None


def test_given_count_as_0_when_PropChecker_is_instantiated_then_occurs_ValueError():
    try:
        PropChecker(0)
        assert False
    except ValueError:
        assert True


def test_when_check_a_valid_property_then_it_should_run_well(capsys):
    check(for_all([arb_int()], lambda x: x + 1 > x))
    out, _ = capsys.readouterr()
    assert out == "OK, passed 100 tests.\n"