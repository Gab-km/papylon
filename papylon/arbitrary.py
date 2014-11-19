# -*- coding: utf-8 -*-
import sys
import random

from papylon.gen import Gen


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


class ArbFloat(AbstractArbitrary):
    def __init__(self):
        def gen():
            min_float = -1.0 - sys.maxsize
            max_float = sys.maxsize
            while True:
                yield random.uniform(min_float, max_float)
        self.gen = Gen(gen)

    def arbitrary(self):
        return self.gen


class ArbList(AbstractArbitrary):
    def __init__(self, arb_type, max_length=100):
        def gen():
            min_length = 0
            length = random.randint(min_length, max_length)
            arb = arb_type.arbitrary()
            while True:
                yield [arb.generate() for i in range(length)]
        self.gen = Gen(gen)

    def arbitrary(self):
        return self.gen


def arb_int():
    return ArbInteger()


def arb_float():
    return ArbFloat()


def arb_list(arb_type, max_length):
    return ArbList(arb_type, max_length=max_length)