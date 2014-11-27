# -*- coding: utf-8 -*-
from papylon.gen import Gen, one_of, choose, frequency


def test_gen_generate_returns_generated_value():
    def gen():
        while True:
            yield 1
    sut = Gen(gen)
    actual = sut.generate()
    assert actual == 1


def test_when_one_of_takes_a_Gen_list_then_returns_one_of_the_Gen_instance_in_the_list():
    def generate_1():
        while True:
            yield 1
    gen_1 = Gen(generate_1)
    def generate_2():
        while True:
            yield 2
    gen_2 = Gen(generate_2)
    def generate_3():
        while True:
            yield 3
    gen_3 = Gen(generate_3)
    sut = one_of([gen_1, gen_2, gen_3])
    actual = sut.generate()
    assert actual in [1, 2, 3]


def test_when_choose_takes_a_string_argument_as_min_value_then_raises_TypeError():
    try:
        choose("1", 2)
    except TypeError:
        assert True
        return
    assert False


def test_when_choose_takes_a_list_argument_as_max_value_then_raises_TypeError():
    try:
        choose(1, [2])
    except TypeError:
        assert True
        return
    assert False


def test_when_choose_takes_arguments_where_min_value_is_greater_than_max_value_then_raises_ValueError():
    try:
        choose(3, 2.0)
    except ValueError:
        assert True
        return
    assert False


def test_when_choose_takes_arguments_where_min_value_is_equal_to_max_value_then_raises_ValueError():
    try:
        choose(-1, -1)
    except ValueError:
        assert True
        return
    assert False


def test_when_choose_takes_arguments_where_min_value_is_float_then_returns_Gen_instance_which_generates_float_value():
    sut = choose(-2.0, 2)
    actual = sut.generate()
    assert type(actual) == float
    assert -2.0 <= actual <= 2.0


def test_when_choose_takes_arguments_where_max_value_is_float_then_returns_Gen_instance_which_generates_float_value():
    sut = choose(-5, 10.0)
    actual = sut.generate()
    assert type(actual) == float
    assert -5.0 <= actual <= 10.0


def test_when_choose_takes_arguments_both_of_which_are_int_then_returns_Gen_instance_which_generates_int_value():
    sut = choose(-50, 50)
    actual = sut.generate()
    assert type(actual) == int
    assert -50 <= actual <= 50


def test_when_frequency_runs_10000_times_then_its_choices_should_be_satisfied_with_accuracy_ge95_percents():
    def generate_1():
        while True:
            yield 1
    gen_1 = Gen(generate_1)

    def generate_10():
        while True:
            yield 10
    gen_10 = Gen(generate_10)

    def generate_100():
        while True:
            yield 100
    gen_100 = Gen(generate_100)

    weighted_gens = [(5, gen_1), (3, gen_10), (2, gen_100)]
    count_1, count_10, count_100 = 0, 0, 0
    parameter = 10000
    for i in range(parameter):
        sut = frequency(weighted_gens)
        value = sut.generate()
        if value == 1:
            count_1 += 1
        elif value == 10:
            count_10 += 1
        elif value == 100:
            count_100 += 1
        else:
            assert False

    def assert_frequency(actual, param, weight, accuracy):
        return actual >= param * weight * accuracy
    assert assert_frequency(count_1, parameter, 0.5, 0.95)
    assert assert_frequency(count_10, parameter, 0.3, 0.95)
    assert assert_frequency(count_100, parameter, 0.2, 0.95)
