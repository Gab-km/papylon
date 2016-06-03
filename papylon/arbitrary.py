"""Classes and functions to generate arbitrary arguments."""

import sys
import random
import struct
import datetime

from papylon.gen import Gen, choose, frequency
from papylon.shrinker import (
    IntShrinker, FloatShrinker, CharShrinker,
    DateShrinker, ListShrinker, StrShrinker)


class AbstractArbitrary:
    """An abstract class to make arbitrary arguments."""

    def arbitrary(self):
        """
        Make arbitrary arguments.

        :return:
        """

        raise NotImplementedError("AbstractArbitrary#arbitrary")

    def shrink(self, value):
        """
        Shrink arguments with a given value.

        :param value:
            The value of counter-example.

        :return:
        """

        raise NotImplementedError("AbstractArbitrary#shrink")


class ArbInteger(AbstractArbitrary):
    """An arbitrary integer."""

    def __init__(self):
        self.gen = choose(-1-sys.maxsize, sys.maxsize)
        self.shrinker = IntShrinker()

    def arbitrary(self):
        """
        Return a generated int value.

        :return: int
            A generated value.
        """

        return self.gen.generate()

    def shrink(self, value):
        """
        Return an int iterator of shrunk result.

        :param value: int
            The int value of counter-example.

        :return:
            The int iterator which is shrunk with a given value.
        """

        return self.shrinker.shrink(value)


class ArbFloat(AbstractArbitrary):
    """An arbitrary floating point number."""

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
        """
        Return a generated float value.

        :return: float
            A generated value.
        """

        return self.gen.generate()

    def shrink(self, value):
        """
        Return a float iterator of shrunk result.

        :param value: float
            The float value of counter-example.

        :return:
            The float iterator which is shrunk with a given value.
        """

        return self.shrinker.shrink(value)


class ArbChar(AbstractArbitrary):
    """An arbitrary character."""

    def __init__(self):
        self.gen = frequency([(0xD800, choose(0, 0xD800-1).map(chr)),
                              (0xFFFF-0xDFFF, choose(0xdFFF+1, 0xFFFF).map(chr))])
        self.shrinker = CharShrinker()

    def arbitrary(self):
        """
        Return a generated char value.

        :return: str
            A generated value.
        """

        # self.gen generates a mapped Gen instance
        return self.gen.generate()

    def shrink(self, value):
        """
        Return a char iterator of shrunk result.

        :param value: str
            The 1-length str value of counter-example.

        :return:
            The char iterator which is shrunk with a given value.
        """

        return self.shrinker.shrink(value)


class ArbDate(AbstractArbitrary):
    """An arbitrary datetime."""

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
        """
        Return a generated datetime value.

        :return: datetime.datetime
            A generated value.
        """

        return self.gen.generate()

    def shrink(self, value):
        """
        Return a datetime iterator of shrunk result.

        :param value: datetime.datetime
            The datetime value of counter-example.

        :return:
            The datetime iterator which is shrunk with a given value.
        """

        return self.shrinker.shrink(value)


class ArbList(AbstractArbitrary):
    """A arbitrary list."""

    def __init__(self, arb_type, max_length):
        def gen():
            min_length = 0
            while True:
                length = random.randint(min_length, max_length)
                yield [arb_type.arbitrary() for _ in range(length)]
        self.gen = Gen(gen)
        self.shrinker = ListShrinker()

    def arbitrary(self):
        """
        Return a generated list value.

        :return: list
            A generated value.
        """

        return self.gen.generate()

    def shrink(self, value):
        """
        Return a list iterator of shrunk result.

        :param value: list
            The list value of counter-example.

        :return:
            The list iterator which is shrunk with a given value.
        """

        return self.shrinker.shrink(value)


class ArbStr(AbstractArbitrary):
    """A arbitrary string."""

    def __init__(self, max_length):
        def gen():
            min_length = 0
            while True:
                length = random.randint(min_length, max_length)
                yield "".join(arb_char().arbitrary() for _ in range(length))
        self.gen = Gen(gen)
        self.shrinker = StrShrinker()

    def arbitrary(self):
        """
        Return a generated str value.

        :return: str
            A generated value.
        """

        return self.gen.generate()

    def shrink(self, value):
        """
        Return a str iterator of shrunk result.

        :param value: str
            The str value of counter-example.

        :return:
            The str iterator which is shrunk with a given value.
        """

        return self.shrinker.shrink(value)


def arb_int():
    """
    Return an instance of ArbInteger.

    :return:
        An instance of ArbInteger.
    """

    return ArbInteger()


def arb_float():
    """
    Return an instance of ArbFloat.

    :return:
        An instance of ArbFloat.
    """

    return ArbFloat()


def arb_char():
    """
    Return an instance of ArbChar.

    :return: ArbChar
        An instance of ArbChar.
    """

    return ArbChar()


def arb_date():
    """
    Return an instance of ArbDate.

    :return:
        An instance of ArbDate.
    """

    return ArbDate()


def arb_list(arb_type, max_length=100):
    """
    Return an instance of ArbList.

    :param arb_type: type
        The type of arbitrary.
    :param max_length: int
        The length of an arbitrary lists. Defaults to 100.

    :return: list
        An instance of ArbList.
    """

    return ArbList(arb_type, max_length=max_length)


def arb_str(max_length=20):
    """
    Return an instance of ArbStr.

    :param max_length: int
        The length of an arbitrary string. Defaults to 20.

    :return: str
        An instance of ArbStr.
    """

    return ArbStr(max_length=max_length)


def from_gen(gen):
    """
    Return an instance of Arbitrary from a generator.

    :param gen: generator
        A generator.

    :return: AbstractArbitrary
        The instance of AbstractArbitrary.
    """

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
    """
    Return an instance of Arbitrary from a generator and a shrinker.

    :param gen: generator
        A generator.
    :param shrinker: AbstractShrinker
        A shrinker.

    :return: AbstractArbitrary
        The instance of AbstractArbitrary.
    """

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
