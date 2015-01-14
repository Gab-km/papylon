# -*- coding: utf-8 -*-
def test_given_passed_result_when_print_result_then_report_ok(capsys):
    from papylon.printer import SimplePrinter
    from papylon.checker import CheckResult

    result = CheckResult.pass_all(10)
    sut = SimplePrinter(result)
    sut.print_result()
    out, err = capsys.readouterr()
    assert out == "OK, passed 10 tests.\n"
    assert err == ""


def test_given_falsified_result_without_error_when_print_result_then_report_not_ok(capsys):
    from papylon.printer import SimplePrinter
    from papylon.checker import CheckResult

    result = CheckResult.falsify(5, ["test"], 0)
    sut = SimplePrinter(result)
    sut.print_result()
    out, err = capsys.readouterr()
    assert out == "Falsified after 5 tests (0 shrinks):\n> ['test']\n"
    assert err == ""


def test_given_falsified_result_with_error_when_print_result_then_report_not_ok_for_error(capsys):
    from papylon.printer import SimplePrinter
    from papylon.checker import CheckResult

    result = CheckResult.error(6, ["ham", "egg"], ValueError("SPAM!"))
    sut = SimplePrinter(result)
    sut.print_result()
    out, err = capsys.readouterr()
    assert out == "Falsified after 6 tests:\n> ['ham', 'egg']\nwith exception:\nSPAM!\n"
    assert err == ""


def test_given_argument_failed_to_be_generated_result_when_print_result_then_report_failed_to_generate(capsys):
    from papylon.printer import SimplePrinter
    from papylon.checker import CheckResult

    result = CheckResult.fail_to_generate(66, 100)
    sut = SimplePrinter(result)
    sut.print_result()
    out, err = capsys.readouterr()
    assert out == "Gave up after only 66 tests. 100 arguments failed to be generated.\n"
    assert err == ""


def test_given_troubled_result_when_print_result_then_report_error(capsys):
    from papylon.printer import SimplePrinter
    from papylon.checker import CheckResult

    result = CheckResult.trouble(ValueError("holy grail"), None)
    sut = SimplePrinter(result)
    sut.print_result()
    out, err = capsys.readouterr()
    assert out == ""
    assert err == "[Papylon] Some exception is raised:\nholy grail\n"


def test_given_unknown_result_when_print_result_then_report_unknown(capsys):
    from papylon.printer import SimplePrinter
    from papylon.checker import CheckResult

    result = CheckResult(-1)
    sut = SimplePrinter(result)
    sut.print_result()
    out, err = capsys.readouterr()
    assert out == ""
    assert err == "[Papylon] CheckResult doesn't have any known result types.\n"