# -*- coding: utf-8 -*-
import re
import sys
import traceback


class CheckResult:
    def __init__(self, func_name, label, success, failure, exceptions, results):
        self.func_name = func_name
        self.label = label
        self.success = success
        self.failure = failure
        self.exceptions = exceptions
        self.results = results


class PropChecker:
    def __init__(self, count=100):
        self.count = count if count >= 1 else 100

    def check(self, prop):
        success, failure = 0, 0
        exceptions = {}
        results = []

        try:
            for i in range(self.count):
                prop_result = prop.execute()

                if prop_result.done:
                    _, _, is_valid = prop_result.done
                    if is_valid:
                        success += 1
                    else:
                        failure += 1
                    results.append(prop_result)
                else:
                    _, _, error = prop_result.stopped
                    exception_key = re.match('^([a-zA-Z]+)\(.*$', repr(error)).group(1)
                    exceptions.setdefault(exception_key, 0)
                    exceptions[exception_key] += 1

                    results.append(prop_result)

            return CheckResult(
                prop.func.__name__,
                prop.label,
                success,
                failure,
                exceptions,
                results
            )
        except Exception as error:
            print('Exception is raised', file=sys.stderr)
            print(error.args[0], file=sys.stderr)
            _, _, ex_traceback = sys.exc_info()
            traceback.print_tb(ex_traceback, limit=10, file=sys.stderr)

            #TODO: return subinstance of TestResult