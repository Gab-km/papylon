# -*- coding: utf-8 -*-
import sys
from papylon.printer import SimplePrinter


class CheckResult:
    def __init__(self):
        self.passed = None
        self.falsified = None
        self.troubled = None

    @staticmethod
    def pass_all(count):
        result = CheckResult()
        result.passed = (count,)
        return result

    @staticmethod
    def falsify(run_count, inputs, error=None):
        result = CheckResult()
        result.falsified = (run_count, inputs, error)
        return result

    @staticmethod
    def trouble(error, ex_traceback):
        result = CheckResult()
        result.troubled = (error, ex_traceback)
        return result

    def has_passed(self):
        return self.passed is not None

    def has_falsified(self):
        return self.falsified is not None

    def has_troubled(self):
        return self.troubled is not None


class PropChecker:
    def __init__(self, count):
        if count < 1:
            raise ValueError("Argument `count` should be a integer greater than or equal to 1.")
        self.count = count

    def check(self, prop):
        try:
            for i in range(self.count):
                prop_result = prop.execute()

                if prop_result.has_finished():
                    _, inputs, is_valid = prop_result.finished
                    if not is_valid:
                        return CheckResult.falsify(i+1, inputs)
                else:
                    _, inputs, error = prop_result.stopped
                    return CheckResult.falsify(i+1, inputs, error)

            return CheckResult.pass_all(self.count)
        except Exception as error:
            _, _, ex_traceback = sys.exc_info()
            return CheckResult.trouble(error.args[0], ex_traceback)


def check(prop, count=100, printer_class=SimplePrinter):
    checker = PropChecker(count=count)
    result = checker.check(prop)
    printer = printer_class()
    printer.print_result(result)