# -*- coding: utf-8 -*-
import sys
import traceback


def convert_to_outputs(result):
    if result.has_passed():
        (count,) = result.get()
        return "OK, passed {0} tests.".format(count), True, sys.stdout
    elif result.has_falsified():
        run_count, inputs, shrunk_number = result.get()
        text = "Falsified after {0} tests ({1} shrinks):\n> {2}".format(run_count, shrunk_number, inputs)
        return text, False, sys.stdout
    elif result.has_error_occurred():
        run_count, inputs, error = result.get()
        text = "Falsified after {0} tests:\n> {1}\nwith exception:\n{2}".format(run_count, inputs, error)
        return text, False, sys.stdout
    elif result.has_failed_to_generate():
        run_count, count_generated = result.get()
        text = "Gave up after only {0} tests. {1} arguments failed to be generated."
        return text.format(run_count, count_generated), False, sys.stdout
    elif result.has_troubled():
        error, ex_traceback = result.get()
        text = "[Papylon] Some exception is raised:\n{0}".format(error.args[0])
        texts = traceback.format_tb(ex_traceback, limit=10)
        for t in texts:
            text = text + t
        return text, False, sys.stderr
    else:
        return "[Papylon] CheckResult doesn't have any known result types.", False, sys.stderr


def print_result(result):
    text, _, file_object = convert_to_outputs(result)
    print(text, file=file_object)


def assert_result(result):
    text, is_proved, _ = convert_to_outputs(result)
    if not is_proved:
        raise AssertionError(text)
