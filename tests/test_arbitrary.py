# -*- coding: utf-8 -*-
import sys
from papylon.arbitrary import (
    AbstractArbitrary,
    ArbInteger, ArbFloat, ArbChar, ArbList, ArbStr,
    arb_int, arb_float, arb_char, arb_list, arb_str,
    from_gen
)
from papylon.gen import choose


def test_ArbInteger_arbitrary_returns_generator_for_integer():
    sut = ArbInteger()
    gen = sut.arbitrary()
    actual = gen.generate()
    assert type(actual) == int
    assert (-1 - sys.maxsize) <= actual <= sys.maxsize


def test_ArbFloat_arbitrary_returns_generator_for_float():
    sut = ArbFloat()
    gen = sut.arbitrary()
    actual = gen.generate()
    assert type(actual) == float
    assert (-sys.float_info.max <= actual <= sys.float_info.max) or (abs(actual) == float('inf')) or (actual != actual)


def test_ArbChar_arbitrary_returns_generator_for_1_char_string():
    sut = ArbChar()
    gen = sut.arbitrary()
    actual = gen.generate()
    assert type(actual) == str
    orded = ord(actual)
    assert 0 <= orded < 0xD800 or 0xDFFF < orded <= 0xFFFF


def test_ArbList_arbitrary_returns_generator_for_list():
    arb_type = ArbInteger()
    sut = ArbList(arb_type, max_length=100)
    gen = sut.arbitrary()
    actual = gen.generate()
    assert type(actual) == list
    assert len(actual) <= 100


def test_ArbStr_arbitrary_returns_generator_for_string():
    sut = ArbStr(max_length=20)
    gen = sut.arbitrary()
    actual = gen.generate()
    assert type(actual) == str
    assert len(actual) <= 20


def test_arb_int_returns_ArbInteger_instance():
    actual = arb_int()
    assert isinstance(actual, ArbInteger)


def test_arb_float_returns_ArbFloat_instance():
    actual = arb_float()
    assert isinstance(actual, ArbFloat)


def test_arb_char_returns_ArbChar_instance():
    actual = arb_char()
    assert isinstance(actual, ArbChar)


def test_arb_list_returns_ArbList_instance():
    arb_type = ArbFloat()
    actual = arb_list(arb_type)
    assert isinstance(actual, ArbList)


def test_arb_str_returns_ArbStr_instance():
    actual = arb_str()
    assert isinstance(actual, ArbStr)


def test_from_gen_returns_AbstractArbitrary_instance_whose_arbitrary_returns_given_Gen_instance():
    sut1 = from_gen(choose(0, 9))
    assert isinstance(sut1, AbstractArbitrary)
    sut2 = from_gen(choose(10, 99))
    assert isinstance(sut2, AbstractArbitrary)

    gen1 = sut1.arbitrary()
    actual1 = gen1.generate()
    assert 0 <= actual1 <= 9
    gen2 = sut2.arbitrary()
    actual2 = gen2.generate()
    assert 10 <= actual2 <= 99
