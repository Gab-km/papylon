def test_when_pluralize_takes_0_as_number_then_returns_plural_form():
    from papylon.utils import pluralize

    actual = pluralize("test", "tests", 0)
    expected = "0 tests"
    assert actual == expected


def test_when_pluralize_takes_1_as_number_then_returns_singular_form():
    from papylon.utils import pluralize

    actual = pluralize("egg", "eggs", 1)
    expected = "1 egg"
    assert actual == expected


def test_when_pluralize_takes_2_as_number_then_returns_plural_form():
    from papylon.utils import pluralize

    actual = pluralize("city", "cities", 2)
    expected = "2 cities"
    assert actual == expected


def test_given_passed_result_with_count_10_when_convert_to_output_then_return_ok_message_as_plural_form():
    from papylon.utils import convert_to_outputs
    from papylon.checker import CheckResult

    result = CheckResult.pass_all(10)
    message, is_ok, _ = convert_to_outputs(result)
    expected = "OK, passed 10 tests."
    assert message == expected
    assert is_ok


def test_given_passed_result_with_count_1_when_convert_to_output_then_return_ok_message_as_singular_form():
    from papylon.utils import convert_to_outputs
    from papylon.checker import CheckResult

    result = CheckResult.pass_all(1)
    message, is_ok, _ = convert_to_outputs(result)
    expected = "OK, passed 1 test."
    assert message == expected
    assert is_ok


def test_given_falsified_result_with_1_shrink_when_convert_to_output_then_return_falsified_message_with_single_shrink():
    from papylon.utils import convert_to_outputs
    from papylon.checker import CheckResult

    result = CheckResult.falsify(5, ["test"], 1)
    message, is_ok, _ = convert_to_outputs(result)
    expected = "Falsified after 5 tests (1 shrink):\n> ['test']"
    assert message == expected
    assert not is_ok


def test_given_falsified_result_with_count_1_when_convert_to_output_then_return_falsified_message_with_single_test():
    from papylon.utils import convert_to_outputs
    from papylon.checker import CheckResult

    result = CheckResult.falsify(1, ["ham"], 0)
    message, is_ok, _ = convert_to_outputs(result)
    expected = "Falsified after 1 test (0 shrinks):\n> ['ham']"
    assert message == expected
    assert not is_ok


def test_given_error_result_with_count_6_when_convert_to_output_then_return_error_message_as_plural_form():
    from papylon.utils import convert_to_outputs
    from papylon.checker import CheckResult

    result = CheckResult.error(6, ["ham", "egg"], ValueError("SPAM!"))
    message, is_ok, _ = convert_to_outputs(result)
    expected = "Falsified after 6 tests:\n> ['ham', 'egg']\nwith exception:\nSPAM!"
    assert message == expected
    assert not is_ok


def test_given_error_result_with_count_1_when_convert_to_output_then_return_error_message_as_singular_form():
    from papylon.utils import convert_to_outputs
    from papylon.checker import CheckResult

    result = CheckResult.error(1, [2, 3], ValueError("one!"))
    message, is_ok, _ = convert_to_outputs(result)
    expected = "Falsified after 1 test:\n> [2, 3]\nwith exception:\none!"
    assert message == expected
    assert not is_ok


class TestGivenGenerationFailureResult:
    def test_with_1_argument_when_convert_to_output_then_returns_generation_failure_message_with_single_argument(self):
        from papylon.utils import convert_to_outputs
        from papylon.checker import CheckResult

        result = CheckResult.fail_to_generate(66, 1)
        message, is_ok, _ = convert_to_outputs(result)
        expected = "Gave up after only 66 tests. 1 argument failed to be generated."
        assert message == expected
        assert not is_ok

    def test_with_count_1_when_convert_to_output_then_returns_generation_failure_message_with_single_count(self):
        from papylon.utils import convert_to_outputs
        from papylon.checker import CheckResult

        result = CheckResult.fail_to_generate(1, 100)
        message, is_ok, _ = convert_to_outputs(result)
        expected = "Gave up after only 1 test. 100 arguments failed to be generated."
        assert message == expected
        assert not is_ok


def test_given_troubled_result_when_convert_to_output_then_returns_troubled_message():
    from papylon.utils import convert_to_outputs
    from papylon.checker import CheckResult

    result = CheckResult.trouble(ValueError("holy grail"), None)
    message, is_ok, _ = convert_to_outputs(result)
    expected = "[Papylon] Some exception is raised:\nholy grail"
    assert message == expected
    assert not is_ok


def test_given_unknown_result_when_convert_to_output_then_returns_unknown_message():
    from papylon.utils import convert_to_outputs
    from papylon.checker import CheckResult

    result = CheckResult(-1)
    message, is_ok, _ = convert_to_outputs(result)
    expected = "[Papylon] CheckResult doesn't have any known result types."
    assert message == expected
    assert not is_ok


def test_when_print_result_then_print_the_result(capsys):
    from papylon.utils import print_result
    from papylon.checker import CheckResult

    result = CheckResult.pass_all(10)
    print_result(result)
    out, err = capsys.readouterr()
    expected = "OK, passed 10 tests.\n"
    assert out == expected
    assert err == ""


def test_given_passed_result_when_assert_result_then_does_not_raise_errors():
    from papylon.utils import assert_result
    from papylon.checker import CheckResult

    result = CheckResult.pass_all(10)
    try:
        assert_result(result)
        assert True
    except AssertionError:
        assert False


def test_given_falsified_result_without_error_when_assert_result_then_raise_assertion_error():
    from papylon.utils import assert_result
    from papylon.checker import CheckResult

    result = CheckResult.falsify(5, ["test"], 0)
    try:
        assert_result(result)
        assert False
    except AssertionError as aes:
        assert str(aes) == "Falsified after 5 tests (0 shrinks):\n> ['test']"


def test_given_falsified_result_with_error_when_assert_result_then_raise_assertion_error():
    from papylon.utils import assert_result
    from papylon.checker import CheckResult

    result = CheckResult.error(6, ["ham", "egg"], ValueError("SPAM!"))
    try:
        assert_result(result)
        assert False
    except AssertionError as aes:
        assert str(aes) == "Falsified after 6 tests:\n> ['ham', 'egg']\nwith exception:\nSPAM!"


def test_given_argument_failed_to_be_generated_result_when_assert_result_then_raise_assertion_error():
    from papylon.utils import assert_result
    from papylon.checker import CheckResult

    result = CheckResult.fail_to_generate(66, 100)
    try:
        assert_result(result)
        assert False
    except AssertionError as aes:
        assert str(aes) == "Gave up after only 66 tests. 100 arguments failed to be generated."


def test_given_troubled_result_when_assert_result_then_raise_assertion_error():
    from papylon.utils import assert_result
    from papylon.checker import CheckResult

    result = CheckResult.trouble(ValueError("holy grail"), None)
    try:
        assert_result(result)
        assert False
    except AssertionError as aes:
        assert str(aes) == "[Papylon] Some exception is raised:\nholy grail"


def test_given_unknown_result_when_assert_result_then_raise_assertion_error():
    from papylon.utils import assert_result
    from papylon.checker import CheckResult

    result = CheckResult(-1)
    try:
        assert_result(result)
        assert False
    except AssertionError as aes:
        assert str(aes) == "[Papylon] CheckResult doesn't have any known result types."
