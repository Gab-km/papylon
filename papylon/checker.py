# -*- coding: utf-8 -*-
import sys
import traceback


class PropChecker:
    def __init__(self, count):
        self.count = count if count >= 1 else 100

    def check(self, prop):

        try:
            for i in range(self.count):
                prop_result = prop.execute()

                if prop_result.done:
                    _, inputs, is_valid = prop_result.done
                    if not is_valid:
                        return "Falsified after {0} tests.".format(i) + \
                            "\n> {0}".format(inputs)
                else:
                    _, inputs, error = prop_result.stopped
                    return "Falsified after {0} tests.".format(i) + \
                        "\n> {0}".format(inputs) + \
                        "\nwith exception:\n" + \
                        str(error)

            return "OK, passed {0} tests.".format(self.count)
        except Exception as error:
            print('[Papylon] Some exception is raised.', file=sys.stderr)
            print(error.args[0], file=sys.stderr)
            _, _, ex_traceback = sys.exc_info()
            traceback.print_tb(ex_traceback, limit=10, file=sys.stderr)
            return None
            #TODO: return some results?


def check(prop, count=100):
    checker = PropChecker(count=count)
    result = checker.check(prop)
    print(result)