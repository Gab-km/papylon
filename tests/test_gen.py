# -*- coding: utf-8 -*-
def test_gen_generate_returns_generated_value():
    from papylon.gen import Gen

    def gen():
        while True:
            yield 1
    sut = Gen(gen)
    actual = sut.generate()
    assert actual == 1


def test_Gen_such_that_returns_new_ranged_Gen_instance():
    from papylon.gen import choose
    gen = choose(-20, 20)
    new_gen = gen.such_that(lambda x: 0 <= x <= 20)
    actual = new_gen.generate()
    assert 0 <= actual <= 20


def test_Gen_such_that_returns_no_hitted_Gen_and_raise_StopGeneration_when_generate_called():
    from papylon.gen import choose, StopGeneration
    gen = choose(-30, 30)
    new_gen = gen.such_that(lambda x: 31 <= x)
    try:
        new_gen.generate()
    except StopGeneration:
        assert True
        return
    assert False


def test_when_one_of_takes_a_Gen_list_then_returns_one_of_the_Gen_instance_in_the_list():
    from papylon.gen import Gen, one_of

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
    from papylon.gen import choose
    try:
        choose("1", 2)
    except TypeError:
        assert True
        return
    assert False


def test_when_choose_takes_a_list_argument_as_max_value_then_raises_TypeError():
    from papylon.gen import choose
    try:
        choose(1, [2])
    except TypeError:
        assert True
        return
    assert False


def test_when_choose_takes_arguments_where_min_value_is_greater_than_max_value_then_raises_ValueError():
    from papylon.gen import choose
    try:
        choose(3, 2.0)
    except ValueError:
        assert True
        return
    assert False


def test_when_choose_takes_arguments_where_min_value_is_equal_to_max_value_then_raises_ValueError():
    from papylon.gen import choose
    try:
        choose(-1, -1)
    except ValueError:
        assert True
        return
    assert False


def test_when_choose_takes_arguments_where_min_value_is_float_then_returns_Gen_instance_which_generates_float_value():
    from papylon.gen import choose
    sut = choose(-2.0, 2)
    actual = sut.generate()
    assert type(actual) == float
    assert -2.0 <= actual <= 2.0


def test_when_choose_takes_arguments_where_max_value_is_float_then_returns_Gen_instance_which_generates_float_value():
    from papylon.gen import choose
    sut = choose(-5, 10.0)
    actual = sut.generate()
    assert type(actual) == float
    assert -5.0 <= actual <= 10.0


def test_when_choose_takes_arguments_both_of_which_are_int_then_returns_Gen_instance_which_generates_int_value():
    from papylon.gen import choose
    sut = choose(-50, 50)
    actual = sut.generate()
    assert type(actual) == int
    assert -50 <= actual <= 50


def test_when_frequency_runs_10000_times_then_its_choices_should_be_satisfied_with_accuracy_ge95_percents():
    from papylon.gen import Gen, frequency

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


def test_map_should_create_new_Gen_instance_with_mapper_function():
    from papylon.gen import choose, map
    gen = choose(1, 10)
    new_gen = map(lambda x: x * 2, gen)
    generated_by_new_gen = new_gen.generate()
    assert type(generated_by_new_gen) == int
    assert generated_by_new_gen in range(2, 21, 2)
    generated_by_gen = gen.generate()
    assert type(generated_by_gen) == int
    assert generated_by_gen in range(1, 11)
