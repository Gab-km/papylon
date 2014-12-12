# -*- coding: utf-8 -*-
import sys
import random
import struct
import datetime

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
        def gen():
            while True:
                s = random.randint(0, 1)                # sign
                e = random.randint(0, 0x7ff)            # exponent
                f = random.randint(0, 0xfffffffffffff)  # fraction
                yield struct.unpack('d', struct.pack('Q', (s << 63) | (e << 52) | f))[0]
        self.gen = Gen(gen)

    def arbitrary(self):
        return self.gen


class ArbChar(AbstractArbitrary):
    def __init__(self):
        self.gen = frequency([(0xD800, map(chr, choose(0, 0xD800-1))),
                              (0xFFFF-0xDFFF, map(chr, choose(0xdFFF+1, 0xFFFF)))])

    def arbitrary(self):
        return self.gen


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

    def arbitrary(self):
        return self.gen


class ArbList(AbstractArbitrary):
    def __init__(self, arb_type, max_length):
        def gen():
            min_length = 0
            while True:
                length = random.randint(min_length, max_length)
                arb = arb_type.arbitrary()
                yield [arb.generate() for i in range(length)]
        self.gen = Gen(gen)

    def arbitrary(self):
        return self.gen


class ArbStr(AbstractArbitrary):
    def __init__(self, max_length):
        def gen():
            min_length = 0
            while True:
                length = random.randint(min_length, max_length)
                arb = arb_char().arbitrary()
                yield "".join(arb.generate() for i in range(length))
        self.gen = Gen(gen)

    def arbitrary(self):
        return self.gen


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
        return this.gen
    arb.arbitrary.__func__.__code__ = new_arbitrary.__code__
    return arb
