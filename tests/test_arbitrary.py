# -*- coding: utf-8 -*-
import sys
from papylon.arbitrary import ArbInteger, ArbFloat, ArbStr, ArbList, arb_int, arb_float, arb_str, arb_list


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
    assert (-1.0 - sys.maxsize) <= actual <= 1.0 * sys.maxsize


def test_ArbStr_arbitrary_returns_generator_for_string():
    sut = ArbStr()
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


def test_arb_int_returns_ArbInteger_instance():
    actual = arb_int()
    assert isinstance(actual, ArbInteger)


def test_arb_float_returns_ArbFloat_instance():
    actual = arb_float()
    assert isinstance(actual, ArbFloat)


def test_arb_str_returns_ArbStr_instance():
    actual = arb_str()
    assert isinstance(actual, ArbStr)


def test_arb_list_returns_ArbList_instance():
    arb_type = ArbFloat()
    actual = arb_list(arb_type)
    assert isinstance(actual, ArbList)