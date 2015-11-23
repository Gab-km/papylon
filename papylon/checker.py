# -*- coding: utf-8 -*-
import sys
from papylon.gen import StopGeneration
from papylon.utils import print_result, print_result_in_group, assert_result


class CheckResult:
    PASSED = 0
    FALSIFIED = 1
    ERROR = 2
    FAIL_TO_GENERATE = 3
    TROUBLED = 4

    def __init__(self, status):
        self.status = status
        self.result = None

    @staticmethod
    def pass_all(count):
        result = CheckResult(CheckResult.PASSED)
        result.result = (count,)
        return result

    @staticmethod
    def falsify(run_count, inputs, shrunk_number):
        result = CheckResult(CheckResult.FALSIFIED)
        result.result = (run_count, inputs, shrunk_number)
        return result

    @staticmethod
    def error(run_count, inputs, error):
        result = CheckResult(CheckResult.ERROR)
        result.result = (run_count, inputs, error)
        return result

    @staticmethod
    def fail_to_generate(run_count, trial_to_generate):
        result = CheckResult(CheckResult.FAIL_TO_GENERATE)
        result.result = (run_count, trial_to_generate)
        return result

    @staticmethod
    def trouble(error, ex_traceback):
        result = CheckResult(CheckResult.TROUBLED)
        result.result = (error, ex_traceback)
        return result

    def has_passed(self):
        return self.status == CheckResult.PASSED

    def has_falsified(self):
        return self.status == CheckResult.FALSIFIED

    def has_error_occurred(self):
        return self.status == CheckResult.ERROR

    def has_failed_to_generate(self):
        return self.status == CheckResult.FAIL_TO_GENERATE

    def has_troubled(self):
        return self.status == CheckResult.TROUBLED

    def get(self):
        return self.result


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
                    _, inputs, is_valid, shrunk_number = prop_result.get()
                    if not is_valid:
                        return CheckResult.falsify(i+1, inputs, shrunk_number)
                else:
                    _, inputs, error = prop_result.get()

                    # failed to generate?
                    if type(error) == StopGeneration:
                        return CheckResult.fail_to_generate(i+1, error.trial_to_generate)
                    else:
                        return CheckResult.error(i+1, inputs, error)

            return CheckResult.pass_all(self.count)
        except Exception as error:
            _, _, ex_traceback = sys.exc_info()
            return CheckResult.trouble(error, ex_traceback)


def check(prop, count=100, printer=print_result):
    checker = PropChecker(count=count)
    result = checker.check(prop)
    printer(result)


def check_and_assert(prop, count=100, asserter=assert_result):
    checker = PropChecker(count=count)
    result = checker.check(prop)
    asserter(result)


def check_all(properties, count=100, printer=print_result_in_group):
    checker = PropChecker(count=count)
    group_name = properties.group_name
    for prop_name, prop in properties.properties():
        result = checker.check(prop)
        printer(result, group_name, prop_name)
