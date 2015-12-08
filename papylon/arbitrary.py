# -*- coding: utf-8 -*-
import sys
import random
import struct
import datetime

from papylon.gen import Gen, choose, frequency, map
from papylon.shrinker import (
    IntShrinker, FloatShrinker, CharShrinker,
    DateShrinker, ListShrinker, StrShrinker)


class AbstractArbitrary:
    def arbitrary(self):
        raise NotImplementedError("AbstractArbitrary#arbitrary")

    def shrink(self, value):
        raise NotImplementedError("AbstractArbitrary#shrink")


class ArbInteger(AbstractArbitrary):
    def __init__(self):
        self.gen = choose(-1-sys.maxsize, sys.maxsize)
        self.shrinker = IntShrinker()

    def arbitrary(self):
        return self.gen.generate()

    def shrink(self, value):
        return self.shrinker.shrink(value)


class ArbFloat(AbstractArbitrary):
    def __init__(self):
        def gen():
            while True:
                s = random.randint(0, 1)                # sign
                e = random.randint(0, 0x7ff)            # exponent
                f = random.randint(0, 0xfffffffffffff)  # fraction
                yield struct.unpack('d', struct.pack('Q', (s << 63) | (e << 52) | f))[0]
        self.gen = Gen(gen)
        self.shrinker = FloatShrinker()

    def arbitrary(self):
        return self.gen.generate()

    def shrink(self, value):
        return self.shrinker.shrink(value)


class ArbChar(AbstractArbitrary):
    def __init__(self):
        self.gen = frequency([(0xD800, map(chr, choose(0, 0xD800-1))),
                              (0xFFFF-0xDFFF, map(chr, choose(0xdFFF+1, 0xFFFF)))])
        self.shrinker = CharShrinker()

    def arbitrary(self):
        # self.gen generates a mapped Gen instance
        return self.gen.generate()

    def shrink(self, value):
        return self.shrinker.shrink(value)


class ArbDate(AbstractArbitrary):
    def __init__(self):
        days_to_month_366 = [0, 31, 60, 91, 121, 152, 182, 213, 244, 274, 305, 335, 366]
        days_to_month_365 = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334, 365]

        def is_leap_year(year):
            assert 1 <= year <= 9999    # contract
            return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

        def days_in_month(year, month):
            assert 1 <= month <= 12     # contract
            days = days_to_month_366 if is_leap_year(year) else days_to_month_365
            return days[month] - days[month - 1]

        def gen():
            while True:
                year = random.randint(1, 9999)
                month = random.randint(1, 12)
                day = random.randint(1, days_in_month(year, month))
                hour = random.randint(0, 23)
                minute = random.randint(0, 59)
                second = random.randint(0, 59)
                yield datetime.datetime(year, month, day, hour, minute, second)
        self.gen = Gen(gen)
        self.shrinker = DateShrinker()

    def arbitrary(self):
        return self.gen.generate()

    def shrink(self, value):
        return self.shrinker.shrink(value)


class ArbList(AbstractArbitrary):
    def __init__(self, arb_type, max_length):
        def gen():
            min_length = 0
            while True:
                length = random.randint(min_length, max_length)
                yield [arb_type.arbitrary() for i in range(length)]
        self.gen = Gen(gen)
        self.shrinker = ListShrinker()

    def arbitrary(self):
        return self.gen.generate()

    def shrink(self, value):
        return self.shrinker.shrink(value)


class ArbStr(AbstractArbitrary):
    def __init__(self, max_length):
        def gen():
            min_length = 0
            while True:
                length = random.randint(min_length, max_length)
                yield "".join(arb_char().arbitrary() for i in range(length))
        self.gen = Gen(gen)
        self.shrinker = StrShrinker()

    def arbitrary(self):
        return self.gen.generate()

    def shrink(self, value):
        return self.shrinker.shrink(value)


def arb_int():
    return ArbInteger()


def arb_float():
    return ArbFloat()


def arb_char():
    return ArbChar()


def arb_date():
    return ArbDate()


def arb_list(arb_type, max_length=100):
    return ArbList(arb_type, max_length=max_length)


def arb_str(max_length=20):
    return ArbStr(max_length=max_length)


def from_gen(gen):
    arb = AbstractArbitrary()
    arb.gen = gen

    def new_arbitrary(this):
        return this.gen.generate()
    arb.arbitrary.__func__.__code__ = new_arbitrary.__code__

    def new_shrink(this, value):
        return iter([])
    arb.shrink.__func__.__code__ = new_shrink.__code__

    return arb


def from_gen_shrink(gen, shrinker):
    arb = AbstractArbitrary()
    arb.gen = gen
    arb.shrinker = shrinker

    def new_arbitrary(this):
        return this.gen.generate()
    arb.arbitrary.__func__.__code__ = new_arbitrary.__code__

    def new_shrink(this, value):
        return this.shrinker.shrink(value)
    arb.shrink.__func__.__code__ = new_shrink.__code__

    return arb
