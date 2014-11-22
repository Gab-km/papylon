# -*- coding: utf-8 -*-
import sys
import traceback


class SimplePrinter:
    def print_result(self, result):
        if result.has_passed():
            (count,) = result.passed
            print("OK, passed {0} tests.".format(count))
        elif result.has_falsified():
            run_count, inputs, error = result.falsified
            text = "Falsified after {0} tests.\n> {1}".format(run_count, inputs)
            if error is not None:
                text += "\nwith exception:\n" + str(error)
            print(text)
        elif result.has_troubled():
            error, ex_traceback = result.troubled
            print('[Papylon] Some exception is raised.\n{0}'.format(error.args[0]), file=sys.stderr)
            traceback.print_tb(ex_traceback, limit=10, file=sys.stderr)
        else:
            print('CheckResult has any known result types.', file=sys.stderr)