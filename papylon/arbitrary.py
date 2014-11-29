# -*- coding: utf-8 -*-
import sys
import random

from papylon.gen import Gen, choose, frequency, map


class AbstractArbitrary:
    def arbitrary(self):
        raise NotImplementedError("AbstractArbitrary#arbitrary")


class ArbInteger(AbstractArbitrary):
    def __init__(self):
        self.gen = choose(-1-sys.maxsize, sys.maxsize)

    def arbitrary(self):
        return self.gen


class ArbFloat(AbstractArbitrary):
    def __init__(self):
        self.gen = choose(-1.0-sys.maxsize, sys.maxsize)

    def arbitrary(self):
        return self.gen


class ArbStr(AbstractArbitrary):
    def __init__(self):
        self.gen = frequency([(0xD800, map(chr, choose(0, 0xD800-1))),
                              (0xFFFF-0xDFFF, map(chr, choose(0xdFFF+1, 0xFFFF)))])

    def arbitrary(self):
        return self.gen


class ArbList(AbstractArbitrary):
    def __init__(self, arb_type, max_length):
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


def arb_str():
    return ArbStr()


def arb_list(arb_type, max_length=100):
    return ArbList(arb_type, max_length=max_length)
