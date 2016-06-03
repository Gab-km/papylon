"""Classes and functions to deal with generators."""

import random
import itertools
import bisect


class StopGeneration(StopIteration):
    """Signal the end from Gen.generate()."""
    def __init__(self, trial_to_generate, *args, **kwargs):
        StopIteration.__init__(self, *args, **kwargs)
        self.trial_to_generate = trial_to_generate


class Gen:
    """Generator of a random value."""

    DEFAULT_TRIAL = 100

    def __init__(self, gen, mapper=None, predicate=None, trial=DEFAULT_TRIAL):
        """
        Initialize a Gen instance.

        `self.mapper` is assigned an identity function if the argument
        `mapper` isn't set or is set None. `self.predicate` is also a
        function always returns True if the argument `predicate` isn't
        set or is set None.

        :param gen: function
            The generator function to yield a value.
        :param mapper: function
            The function to apply a generated value. Defaults to None.
        :param predicate: function
            The function to filter a generated value. Defaults to None.
        :param trial: int
            The trial number to generate values. Defaults to
            `DEFAULT_TRIAL`.
        """

        def _id(x):
            return x

        def _true(_):
            return True

        self.gen = gen()
        self.mapper = _id if mapper is None else mapper
        self.predicate = _true if predicate is None else predicate
        self.trial = trial

    def generate(self):
        """
        Generate a random value.

        Return a mapped value with `self.mapper` if the value satisfies
        `self.predicate`. If values don't satisfy the predicate and the
        number of trial is no less than `self.trial`, raise
        `StopGeneration`.

        :return:
            A random value which `self.gen` generates, `self.mapper`
            maps and `self.predicate` filters.
        """

        for i, value in enumerate(self.gen):
            mapped = self.mapper(value)
            if self.predicate(mapped):
                return mapped

            if i >= self.trial:
                raise StopGeneration(i)

    def map(self, f):
        """
        Return a Gen instance that applies f to every generated value.

        :param f: function
            The function to apply a generated value.

        :return: Gen
            The `Gen` instance derived from `self` and `self.mapper` is
            `f`.
        """

        return Gen(lambda: self.gen, f)

    def such_that(self, predicate, trial=DEFAULT_TRIAL):
        """
        Return a Gen which generates values filtered with predicate.

        :param predicate: function
            The function to filter a generated value.
        :param trial: int
            The trial number to generate values. Defaults to
            `DEFAULT_TRIAL`.

        :return: Gen
            The `Gen` instance derived from `self`, `self.mapper` is
            `predicate` and `self.trial` is `trial`.
        """

        return Gen(lambda: self.gen, predicate=predicate, trial=trial)


def one_of(gens):
    """
    Return a Gen instance from `gens` sequence.

    :param gens: list
        The list of `Gen` instance.

    :return: Gen
        The `Gen` instance from `gens` sequence.
    """

    return random.choice(gens)


def choose(min_value, max_value):
    """
    Return a Gen which generates between `min_value` and `max_value`.

    :param min_value: int | float
        The minimum value to generate.
    :param max_value: int | float
        The maximum value to generate.

    :return: Gen
        The `Gen` instance which generates a number between `min_value`
        and `max_value`. This generates a float value if `min_value` or
        `max_value` is float, otherwise a int value.
    """

    min_value_type = type(min_value)
    max_value_type = type(max_value)
    if min_value_type not in [int, float] or max_value_type not in [int, float]:
        raise TypeError("`gen.choose(min_value, max_value)` should take 2 arguments as `int` or `float`.")

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
    """
    Return a Gen instance from weighted Gen sequence `weighted_gens`.

    :ref:
        https://docs.python.org/3.4/library/random.html#examples-and-recipes

    :param weighted_gens: list
        The list of (int, Gen) sequence.

    :return: Gen
        The `Gen` instance from `weighted_gens` sequence, which is
        selected by.
    """

    weights, gens = zip(*weighted_gens)
    cumdist = list(itertools.accumulate(weights))
    x = random.random() * cumdist[-1]
    return gens[bisect.bisect(cumdist, x)]


def constant(value):
    """
    Return a Gen instance which generates a given value.

    :param value:
        The value to generate.

    :return: Gen
        The `Gen` instance generates a constant value which is given.
    """

    def gen():
        while True:
            yield value
    return Gen(gen)
