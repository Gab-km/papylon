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
            #inputs = [gen.generate() for gen in self.arb.arbitrary()]
            inputs = []
            for arb in self.arbs:
                gen = arb.arbitrary()
                inputs.append(gen.generate())
            is_valid = self.func(*inputs)

            return PropResult.to_be_done(self.func.__name__, inputs, is_valid)
        #except self.exceptions as error:
        except Exception as error:
            return PropResult.to_be_stopped(self.func.__name__, inputs, error)
