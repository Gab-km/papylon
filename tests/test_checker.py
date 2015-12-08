def test_given_count_as_100_when_prop_checker_check_a_property_then_the_property_runs_100_times():
    from papylon.checker import PropChecker
    from papylon.prop import for_all
    from papylon.arbitrary import arb_int

    sut = PropChecker(100)
    result = sut.check(for_all([arb_int()], lambda x: x + x == x * 2))
    assert result.has_passed()
    (count,) = result.get()
    assert count == 100


def test_given_property_which_fails_to_generate_when_prop_checker_check_it_then_returns_generation_failure_report():
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


def test_given_falsifiable_property_when_prop_checker_check_the_property_then_returns_falsified_report():
    from papylon.checker import PropChecker
    from papylon.prop import for_all
    from papylon.arbitrary import arb_int

    sut = PropChecker(100)
    result = sut.check(for_all([arb_int()], lambda x: x != 0 and x == x * (-1)))
    assert result.has_falsified()
    run_count, inputs, shrunk_number = result.get()
    assert run_count == 1
    assert shrunk_number >= 0


def test_given_exceptional_property_when_check_the_property_then_returns_falsified_report_with_exception():
    from papylon.checker import PropChecker
    from papylon.prop import for_all
    from papylon.arbitrary import arb_int

    sut = PropChecker(100)
    result = sut.check(for_all([arb_int()], lambda x: 0/x == x/0))
    assert result.has_error_occurred()
    run_count, inputs, error = result.get()
    assert run_count == 1
    assert error is not None


def test_given_prop_execute_which_throws_error_when_prop_checker_check_the_property_then_returns_troubled_report():
    from papylon.checker import PropChecker

    class DummyProp:
        def __init__(self, msg):
            self.msg = msg

        def execute(self):
            raise ValueError(self.msg)
    message = "Something has been occurred."
    prop = DummyProp(message)
    sut = PropChecker(100)
    result = sut.check(prop)
    assert result.has_troubled()
    error, ex_traceback = result.get()
    assert type(error) == ValueError
    assert error.args[0] == message
    assert ex_traceback is not None


def test_given_count_as_0_when_prop_checker_is_instantiated_then_occurs_value_error():
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


def test_when_check_and_assert_an_invalid_property_then_raise_assertion_error():
    from papylon.checker import check_and_assert
    from papylon.prop import for_all
    from papylon.arbitrary import arb_float

    try:
        check_and_assert(for_all([arb_float()], lambda x: x + 1.0 == x))
        assert False
    except AssertionError:
        assert True


def test_when_check_all_a_properties_instance_then_check_all_properties(capsys):
    from papylon.checker import check_all
    from papylon.prop import for_all, Properties
    from papylon.arbitrary import arb_int, arb_list

    p1 = for_all([arb_list(arb_int(), max_length=20), arb_list(arb_int(), max_length=20)],
                 lambda xs, ys: len(xs) + len(ys) == len(xs + ys))
    props = Properties("List propositions")
    props.add("length proposition", p1)
    props.add("wrong proposition",
              for_all([arb_list(arb_int(), max_length=20)], lambda xs: len(xs) < 0))
    check_all(props)
    out, _ = capsys.readouterr()
    out_lines = out.splitlines()
    assert len(out_lines) == 3
    assert out_lines[0] == "List propositions.length proposition -> OK, passed 100 tests."
    expected_failing = "List propositions.wrong proposition -> Falsified after 1 test "
    assert out_lines[1][:len(expected_failing)] == expected_failing
    assert out_lines[2] == "> [[]]"  # Is this assertion fragile?


def test_when_check_all_properties_then_checks_it_not_in_lexical_order_but_of_registration(capsys):
    from papylon.checker import check_all
    from papylon.prop import for_all, Properties
    from papylon.arbitrary import arb_int, arb_list

    p1 = for_all([arb_list(arb_int(), max_length=20)],
                 lambda x: list(reversed(list(reversed(x)))) == x)
    props = Properties("List propositions")
    props.add("reverse cyclic proposition", p1)
    p2 = for_all([arb_list(arb_int(), max_length=20), arb_list(arb_int(), max_length=20)],
                 lambda xs, ys: len(xs) + len(ys) == len(xs + ys))
    props.add("length proposition", p2)
    check_all(props)
    out, _ = capsys.readouterr()
    out_lines = out.splitlines()
    assert len(out_lines) == 2
    assert out_lines[0] == "List propositions.reverse cyclic proposition -> OK, passed 100 tests."
    assert out_lines[1] == "List propositions.length proposition -> OK, passed 100 tests."
