# -*- coding: utf-8 -*-


class PropResult:
    def __init__(self):
        self.finished = None
        self.stopped = None

    @staticmethod
    def finish(func_name, inputs, is_valid):
        result = PropResult()
        result.finished = (func_name, inputs, is_valid)
        return result

    @staticmethod
    def stop(func_name, inputs, error):
        result = PropResult()
        result.stopped = (func_name, inputs, error)
        return result

    def has_finished(self):
        return self.finished is not None

    def has_stopped(self):
        return self.stopped is not None


class Prop:
    def __init__(self, arbs, func):
        self.arbs = arbs
        self.func = func

    def execute(self):
        inputs = None
        try:
            inputs = []
            for arb in self.arbs:
                gen = arb.arbitrary()
                inputs.append(gen.generate())
            is_valid = self.func(*inputs)

            return PropResult.finish(self.func.__name__, inputs, is_valid)

        except Exception as error:
            return PropResult.stop(self.func.__name__, inputs, error)


def for_all(arbs, func):
    return Prop(arbs, func)


# def for_all_as_method(arbitraries):
#     def make_prop(func_to_check):
#         def inner(target, *args):
#             def func_without_target(*a):
#                 return func_to_check(target, *a)
#             return Prop(arbitraries, func_without_target)
#         return inner
#     return make_prop


# def for_all(arbitraries):
#     def make_prop(func_to_check):
#         def inner(*args):
#             return Prop(arbitraries, func_to_check)
#         return inner
#     return make_prop
