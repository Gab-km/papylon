# -*- coding: utf-8 -*-
from papylon.gen import Gen


def test_gen_generate_returns_generated_value():
    def gen():
        while True:
            yield 1
    sut = Gen(gen)
    actual = sut.generate()
    assert actual == 1