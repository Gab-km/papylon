# -*- coding: utf-8 -*-
import sys
from unittest import TestCase
from papylon.arbitrary import ArbInteger, ArbFloat, ArbList, arb_int, arb_float, arb_list


class ArbitraryTest(TestCase):
    def test_ArbInteger_arbitrary_returns_generator_for_integer(self):
        sut = ArbInteger()
        gen = sut.arbitrary()
        actual = gen.generate()
        assert type(actual) == int
        assert (-1 - sys.maxsize) <= actual <= sys.maxsize

    def test_ArbFloat_arbitrary_returns_generator_for_float(self):
        sut = ArbFloat()
        gen = sut.arbitrary()
        actual = gen.generate()
        assert type(actual) == float
        assert (-1.0 - sys.maxsize) <= actual <= 1.0 * sys.maxsize

    def test_ArbList_arbitrary_returns_generator_for_list(self):
        arb_type = ArbInteger()
        sut = ArbList(arb_type, max_length=100)
        gen = sut.arbitrary()
        actual = gen.generate()
        assert type(actual) == list
        assert len(actual) <= 100

    def test_arb_int_returns_ArbInteger_instance(self):
        actual = arb_int()
        assert isinstance(actual, ArbInteger)

    def test_arb_float_returns_ArbFloat_instance(self):
        actual = arb_float()
        assert isinstance(actual, ArbFloat)

    def test_arb_list_returns_ArbList_instance(self):
        arb_type = ArbFloat()
        actual = arb_list(arb_type)
        assert isinstance(actual, ArbList)