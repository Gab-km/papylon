# -*- coding: utf-8 -*-


class PropResult:
    def __init__(self):
        self.done = None
        self.stopped = None

    @staticmethod
    def to_be_done(func_name, inputs, is_valid):
        result = PropResult()
        result.done = (func_name, inputs, is_valid)
        return result

    @staticmethod
    def to_be_stopped(func_name, inputs, error):
        result = PropResult()
        result.stopped = (func_name, inputs, error)
        return result


class Prop:
    def __init__(self, arbs, func, label="", exceptions=None):
        self.arbs = arbs
        self.func = func
        self.label = label
        self.exceptions = exceptions

    def execute(self):
        inputs = None
        try:
            inputs = []
            for arb in self.arbs:
                gen = arb.arbitrary()
                inputs.append(gen.generate())
            is_valid = self.func(*inputs)

            return PropResult.to_be_done(self.func.__name__, inputs, is_valid)

        except Exception as error:
            return PropResult.to_be_stopped(self.func.__name__, inputs, error)


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
