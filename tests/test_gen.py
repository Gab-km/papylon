# -*- coding: utf-8 -*-
from unittest import TestCase
from papylon.gen import Gen


class GenTest(TestCase):
    def test_gen_generate_returns_generated_value(self):
        def gen():
            while True:
                yield 1
        sut = Gen(gen)
        actual = sut.generate()
        assert actual == 1