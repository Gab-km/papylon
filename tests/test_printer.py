# -*- coding: utf-8 -*-
from papylon.printer import SimplePrinter
from papylon.checker import CheckResult


def test_given_passed_result_when_print_result_then_report_OK(capsys):
    result = CheckResult.pass_all(10)
    sut = SimplePrinter()
    sut.print_result(result)
    out, _ = capsys.readouterr()
    assert out == "OK, passed 10 tests.\n"


def test_given_falsified_result_without_error_when_print_result_then_report_NOT_OK(capsys):
    result = CheckResult.falsify(5, ["test"])
    sut = SimplePrinter()
    sut.print_result(result)
    out, _ = capsys.readouterr()
    assert out == "Falsified after 5 tests.\n> ['test']\n"


def test_given_falsified_result_with_error_when_print_result_then_report_NOT_OK_FOR_ERROR(capsys):
    result = CheckResult.falsify(6, ["ham", "egg"], ValueError("SPAM!"))
    sut = SimplePrinter()
    sut.print_result(result)
    out, _ = capsys.readouterr()
    assert out == "Falsified after 6 tests.\n> ['ham', 'egg']\nwith exception:\nSPAM!\n"


def test_given_troubled_result_when_print_result_then_report_ERROR(capsys):
    result = CheckResult.trouble(ValueError("holy grail"), None)
    sut = SimplePrinter()
    sut.print_result(result)
    _, err = capsys.readouterr()
    assert err == "[Papylon] Some exception is raised.\nholy grail\n"


def test_given_unknown_result_when_print_result_then_report_UNKNOWN(capsys):
    result = CheckResult()
    sut = SimplePrinter()
    sut.print_result(result)
    _, err = capsys.readouterr()
    assert err == "[Papylon] CheckResult doesn't have any known result types.\n"