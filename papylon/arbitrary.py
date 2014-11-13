# -*- coding: utf-8 -*-
import sys
import random

from papylon.gen import Gen

class NonNegativeInt:
    pass


class PositiveInt:
    pass


class NonZeroInt:
    pass


class NormalFloat:
    pass


class NonEmptyString:
    pass


class AbstractArbitrary:
    def arbitrary(self):
        raise NotImplementedError("AbstractArbitrary#arbitrary")


class ArbInteger(AbstractArbitrary):
    def __init__(self):
        def gen():
            min_int = - 1 - sys.maxsize
            max_int = sys.maxsize
            while True:
                yield random.randint(min_int, max_int)
        self.gen = Gen(gen)

    def arbitrary(self):
        return self.gen


def arb_int():
    return ArbInteger()