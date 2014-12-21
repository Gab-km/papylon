# -*- coding: utf-8 -*-
import random
import itertools
import bisect


class StopGeneration(StopIteration):
    def __init__(self, trial_to_generate, *args, **kwargs):
        StopIteration.__init__(self, *args, **kwargs)
        self.trial_to_generate = trial_to_generate


class Gen:
    DEFAULT_TRIAL = 100

    def __init__(self, gen, mapper=lambda x: x, pred=lambda x: True, trial=DEFAULT_TRIAL):
        self.gen = gen()
        self.mapper = mapper
        self.pred = pred
        self.trial = trial

    def generate(self):
        for i, value in enumerate(self.gen):
            mapped = self.mapper(value)
            if self.pred(mapped):
                return mapped

            if i >= self.trial:
                raise StopGeneration(i)

    def such_that(self, pred, trial=DEFAULT_TRIAL):
        return Gen(lambda: self.gen, pred=pred, trial=trial)


def one_of(gens):
    return random.choice(gens)


def choose(min_value, max_value):
    min_value_type = type(min_value)
    max_value_type = type(max_value)
    if min_value_type not in [int, float] or max_value_type not in [int, float]:
        raise TypeError("`gen.choose(min_value, max_value)` should take 2 arguments" + "as `int` or `float`.")

    if min_value >= max_value:
        raise ValueError("`gen.choose(min_value, max_value)` should take 2 arguments" +
                         " such as `min_value` < `max_value`.")

    if float in [min_value_type, max_value_type]:
        def gen():
            while True:
                yield random.uniform(min_value, max_value)
        return Gen(gen)
    else:
        def gen():
            while True:
                yield random.randint(min_value, max_value)
        return Gen(gen)


def frequency(weighted_gens):
    """ref: https://docs.python.org/3.4/library/random.html#examples-and-recipes"""

    weights, gens = zip(*weighted_gens)
    cumdist = list(itertools.accumulate(weights))
    x = random.random() * cumdist[-1]
    return gens[bisect.bisect(cumdist, x)]


def map(f, gen):
    return Gen(lambda: gen.gen, f)
