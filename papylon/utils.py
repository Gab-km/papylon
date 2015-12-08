import sys
import traceback


def pluralize(singular, plural, number):
    assert number >= 0   # contract
    return "{0} {1}".format(number, singular if number == 1 else plural)


def pluralize_test(number):
    return pluralize("test", "tests", number)


def convert_to_outputs(result):
    if result.has_passed():
        (count,) = result.get()
        return "OK, passed {0}.".format(pluralize_test(count)), True, sys.stdout
    elif result.has_falsified():
        run_count, inputs, shrunk_number = result.get()
        text = "Falsified after {0} ({1}):\n> {2}".format(
            pluralize_test(run_count), pluralize("shrink", "shrinks", shrunk_number), inputs)
        return text, False, sys.stdout
    elif result.has_error_occurred():
        run_count, inputs, error = result.get()
        text = "Falsified after {0}:\n> {1}\nwith exception:\n{2}".format(
            pluralize_test(run_count), inputs, error)
        return text, False, sys.stdout
    elif result.has_failed_to_generate():
        run_count, count_generated = result.get()
        text = "Gave up after only {0}. {1} failed to be generated.".format(
            pluralize_test(run_count), pluralize("argument", "arguments", count_generated))
        return text, False, sys.stdout
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


def print_result_in_group(result, group_name, prop_name):
    text, _, file_object = convert_to_outputs(result)
    print(group_name + '.' + prop_name + ' -> ' + text, file=file_object)


def assert_result(result):
    text, is_proved, _ = convert_to_outputs(result)
    if not is_proved:
        raise AssertionError(text)
