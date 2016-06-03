"""Classes and functions to check properties and for checked results."""

import sys
from papylon.gen import StopGeneration
from papylon.utils import print_result, print_result_in_group, assert_result


class CheckResult:
    """A result of checking properties."""

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
        """
        Create a CheckResult as passed.

        :param count: int
            The number of checking count.

        :return: CheckResult
            The passed result of checking properties.
        """

        result = CheckResult(CheckResult.PASSED)
        result.result = (count,)
        return result

    @staticmethod
    def falsify(run_count, inputs, shrunk_number):
        """
        Create a CheckResult as falsified.

        :param run_count: int
            The number of running count.

        :param inputs: list
            The list of passed arguments.

        :param shrunk_number:
            The number of shrinking.

        :return: CheckResult
            The falsified result of checking properties.
        """

        result = CheckResult(CheckResult.FALSIFIED)
        result.result = (run_count, inputs, shrunk_number)
        return result

    @staticmethod
    def error(run_count, inputs, error):
        """
        Create a CheckResult as error.

        :param run_count: int
            The number of running count.

        :param inputs: list
            The list of passed arguments.

        :param error: Exception
            The occured exception.

        :return: CheckResult
            The error result of checking properties.
        """

        result = CheckResult(CheckResult.ERROR)
        result.result = (run_count, inputs, error)
        return result

    @staticmethod
    def fail_to_generate(run_count, trial_to_generate):
        """
        Create a CheckResult as failure to generate.

        :param run_count: int
            The number of running count.

        :param trial_to_generate: int
            The number of trial to generate.

        :return: CheckResult
            The failure to generate arbitraries in checking properties.
        """

        result = CheckResult(CheckResult.FAIL_TO_GENERATE)
        result.result = (run_count, trial_to_generate)
        return result

    @staticmethod
    def trouble(error, ex_traceback):
        """
        Create a CheckResult as trouble.

        :param error: Exception
            The occured exception.

        :param ex_traceback: ex_traceback
            The traceback object.

        :return: CheckResult
            The error result out of checking properties.
        """

        result = CheckResult(CheckResult.TROUBLED)
        result.result = (error, ex_traceback)
        return result

    def has_passed(self):
        """
        Return whether the CheckResult is passed or not.

        :return: bool
            True if the status is PASSED, otherwise False.
        """

        return self.status == CheckResult.PASSED

    def has_falsified(self):
        """
        Return whether the CheckResult is falsified or not.

        :return: bool
            True if the status is FALSIFIED, otherwise False.
        """

        return self.status == CheckResult.FALSIFIED

    def has_error_occurred(self):
        """
        Return whether the CheckResult is error or not.

        :return: bool
            True if the status is ERROR, otherwise False.
        """

        return self.status == CheckResult.ERROR

    def has_failed_to_generate(self):
        """
        Return whether the CheckResult failed to generate or not.

        :return: bool
            True if the status is FAILE_TO_GENERATE, otherwise False.
        """

        return self.status == CheckResult.FAIL_TO_GENERATE

    def has_troubled(self):
        """
        Return whether the CheckResult has some troubles.

        :return: bool
            True if the status is TROUBLED, otherwise False.
        """

        return self.status == CheckResult.TROUBLED

    def get(self):
        """
        Return the result.

        :return: tuple
            A tuple which represents the result.
        """
        return self.result


class PropChecker:
    """A checker of properties."""

    def __init__(self, count):
        if count < 1:
            raise ValueError("Argument `count` should be a integer greater than or equal to 1.")
        self.count = count

    def check(self, prop):
        """
        Check the given property.

        :param prop: Prop
            The property to check.

        :return: CheckResult
            The result of checking the property.
        """

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
    """
    Check the property in the count of times using the printer.

    :param prop: Prop
        The property to check.

    :param count: int
        The number of times to check. Default value is 100.

    :param printer: function
        The function to print the checking result. Default value is print_result.
    """

    checker = PropChecker(count=count)
    result = checker.check(prop)
    printer(result)


def check_and_assert(prop, count=100, asserter=assert_result):
    """
    Check the property and assert it.

    :param prop: Prop
        The property to check.

    :param count: int
        The number of times to check. Default value is 100.

    :param asserter: function
        The function to assert the checking result. Default value is assert_result.
    """

    checker = PropChecker(count=count)
    result = checker.check(prop)
    asserter(result)


def check_all(properties, count=100, printer=print_result_in_group):
    """
    Check all the properties.

    :param properties: Properties
        The properties that has a bunch of properties to check.

    :param count: int
        The number of times to check. Default value is 100.

    :param printer: function
        The function to print the checking result. Default value is print_result.
    """
    checker = PropChecker(count=count)
    group_name = properties.group_name
    ps = properties.properties()
    for prop_name, prop in ps:
        result = checker.check(prop)
        printer(result, group_name, prop_name)
