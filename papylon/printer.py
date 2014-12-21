# -*- coding: utf-8 -*-
import sys
import traceback


class SimplePrinter:
    def __init__(self, result):
        self.result = result

    def print_result(self):
        if self.result.has_passed():
            (count,) = self.result.get()
            print("OK, passed {0} tests.".format(count))
        elif self.result.has_falsified():
            run_count, inputs, error = self.result.get()
            text = "Falsified after {0} tests.\n> {1}".format(run_count, inputs)
            if error is not None:
                text += "\nwith exception:\n" + str(error)
            print(text)
        elif self.result.has_failed_to_generate():
            (run_count, count_generated) = self.result.get()
            text = "Gave up after only {0} tests. {1} arguments failed to be generated."
            print(text.format(run_count, count_generated))
        elif self.result.has_troubled():
            error, ex_traceback = self.result.get()
            text = "[Papylon] Some exception is raised.\n{0}".format(error.args[0])
            texts = traceback.format_tb(ex_traceback, limit=10)
            for t in texts:
                text = text + t
            print(text, file=sys.stderr)
        else:
            print("[Papylon] CheckResult doesn't have any known result types.", file=sys.stderr)