# -*- coding: utf-8 -*-


class PropResult:
    FINISHED = 0
    STOPPED = 1

    def __init__(self, status):
        self.status = status
        self.result = None

    @staticmethod
    def finish(func_name, inputs, is_valid, shrunk_number):
        result = PropResult(PropResult.FINISHED)
        result.result = (func_name, inputs, is_valid, shrunk_number)
        return result

    @staticmethod
    def stop(func_name, inputs, error):
        result = PropResult(PropResult.STOPPED)
        result.result = (func_name, inputs, error)
        return result

    def has_finished(self):
        return self.status == PropResult.FINISHED

    def has_stopped(self):
        return self.status == PropResult.STOPPED

    def get(self):
        return self.result


class PropExecutor:
    def __init__(self, arbs, func, max_shrinks):
        self.arbs = arbs
        self.func = func
        self.max_shrinks = max_shrinks

    def execute(self):
        inputs = None
        try:
            inputs = []
            for arb in self.arbs:
                inputs.append(arb.arbitrary())
            is_valid = self.func(*inputs)

            if is_valid:
                return PropResult.finish(self.func.__name__, inputs, is_valid, 0)
            else:
                return self.execute_shrinker(inputs)

        except Exception as error:
            return PropResult.stop(self.func.__name__, inputs, error)

    def execute_shrinker(self, inputs):
        raise NotImplementedError("PropExecutor#execute_shrinker")


class PropExecutorWithShrink(PropExecutor):
    def __init__(self, arbs, func, max_shrinks):
        super().__init__(arbs, func, max_shrinks)

    def execute_shrinker(self, inputs):
        shrunk_number = 0
        last_inputs = inputs.copy()
        shrinkings = []
        new_inputs = []
        try:
            for _ in range(self.max_shrinks):
                zipped = zip(self.arbs, last_inputs)
                shrinkings.clear()
                for arb, v in zipped:
                    shrinkings.append(arb.shrink(v))
                stop_shrinking = False
                while True:
                    new_inputs.clear()
                    try:
                        for shrinking in shrinkings:
                            new_inputs.append(next(shrinking))
                    except TypeError:
                        break
                    except StopIteration:
                        break

                    if len(new_inputs) != len(self.arbs):
                        break

                    if new_inputs == last_inputs:
                        stop_shrinking = True
                        break

                    is_valid = self.func(*new_inputs)
                    if not is_valid:
                        last_inputs = new_inputs.copy()
                        shrunk_number += 1
                        break

                if stop_shrinking:
                    break
            return PropResult.finish(self.func.__name__, last_inputs, False, shrunk_number)
        except Exception as error:
            return PropResult.stop(self.func.__name__, new_inputs, error)


class PropExecutorWithoutShrink(PropExecutor):
    def __init__(self, arbs, func, max_shrinks):
        super().__init__(arbs, func, max_shrinks)

    def execute_shrinker(self, inputs):
        return PropResult.finish(self.func.__name__, inputs, False, 0)


class Prop:
    def __init__(self, arbs, func, executor_type):
        self.executor = executor_type(arbs, func, 100)

    def execute(self):
        return self.executor.execute()


def for_all_shrink(arbs, func):
    return Prop(arbs, func, executor_type=PropExecutorWithShrink)


def for_all_no_shrink(arbs, func):
    return Prop(arbs, func, executor_type=PropExecutorWithoutShrink)


def for_all(arbs, func):
    return for_all_shrink(arbs, func)


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
