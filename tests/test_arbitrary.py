# -*- coding: utf-8 -*-
import sys
from unittest import TestCase
from papylon.arbitrary import ArbInteger


class ArbitraryTest(TestCase):
    def test_ArbInteger_arbitrary_returns_generator_for_integer(self):
        sut = ArbInteger()
        gen = sut.arbitrary()
        actual = gen.generate()
        assert (-1 - sys.maxsize) <= actual <= sys.maxsize
