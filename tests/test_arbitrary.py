class TestArbInteger:
    def test_arbitrary_should_return_integer(self):
        from papylon.arbitrary import ArbInteger
        import sys

        sut = ArbInteger()
        actual = sut.arbitrary()
        assert type(actual) == int
        assert (-1 - sys.maxsize) <= actual <= sys.maxsize

    def test_when_shrink_takes_non_zero_integer_then_returns_a_iterable_with_smaller_integers(self):
        from papylon.arbitrary import ArbInteger

        sut = ArbInteger()
        actual = list(sut.shrink(5))
        expected = [0, 3, -3, 4, -4]
        assert actual == expected


class TestArbFloat:
    def test_arbitrary_should_return_float(self):
        from papylon.arbitrary import ArbFloat
        import sys
        import math

        sut = ArbFloat()
        actual = sut.arbitrary()
        assert type(actual) == float
        assert (-sys.float_info.max <= actual <= sys.float_info.max) or\
               (abs(actual) == float('inf')) or\
               (math.isnan(actual))

    def test_when_shrink_takes_non_zero_float_then_returns_a_iterable_with_smaller_floats(self):
        from papylon.arbitrary import ArbFloat

        sut = ArbFloat()
        actual = list(sut.shrink(4.0))
        expected = [0.0, 2.0, -2.0, 3.0, -3.0, 3.5, -3.5, 3.75, -3.75, 3.875, -3.875, 3.9375, -3.9375, 3.96875,
                    -3.96875, 3.984375, -3.984375, 3.9921875, -3.9921875, 3.99609375, -3.99609375, 3.998046875,
                    -3.998046875]
        assert actual == expected


class TestArbChar:
    def test_arbitrary_should_return_1_char_string(self):
        from papylon.arbitrary import ArbChar

        sut = ArbChar()
        actual = sut.arbitrary()
        assert type(actual) == str
        orded = ord(actual)
        assert 0 <= orded < 0xD800 or 0xDFFF < orded <= 0xFFFF

    def test_when_shrink_takes_char_p_then_returns_a_iterable_with_a_b_c(self):
        from papylon.arbitrary import ArbChar

        sut = ArbChar()
        actual = list(sut.shrink('p'))
        expected = ['a', 'b', 'c']
        assert actual == expected


class TestArbDate:
    def test_arbitrary_should_return_datetime_instance(self):
        from papylon.arbitrary import ArbDate
        import datetime

        sut = ArbDate()
        actual = sut.arbitrary()
        assert type(actual) == datetime.datetime
        assert datetime.datetime.min <= actual <= datetime.datetime.max

    def test_when_shrink_takes_1987_06_05_04_32_10_then_returns_a_iterable_with_1987_06_05_04_32_00(self):
        from papylon.arbitrary import ArbDate
        import datetime

        sut = ArbDate()
        actual = list(sut.shrink(datetime.datetime(1987, 6, 5, 4, 32, 10)))
        expected = [datetime.datetime(1987, 6, 5, 4, 32)]
        assert actual == expected


class TestArbList:
    def test_arbitrary_should_return_list(self):
        from papylon.arbitrary import ArbInteger, ArbList

        arb_type = ArbInteger()
        sut = ArbList(arb_type, max_length=100)
        actual = sut.arbitrary()
        assert type(actual) == list
        assert len(actual) <= 100

    def test_when_shrink_takes_a_list_then_returns_another_list_smaller_than_the_original(self):
        from papylon.arbitrary import ArbFloat, ArbList

        arb_type = ArbFloat()
        sut = ArbList(arb_type, max_length=100)
        actual = list(sut.shrink([3, 3.1, 3.14, 3.141]))
        expected = [[3.1, 3.14, 3.141], [3, 3.14, 3.141], [3, 3.1, 3.141], [3, 3.1, 3.14]]
        assert actual == expected


class TestArbStr:
    def test_arbitrary_should_return_generator_for_string(self):
        from papylon.arbitrary import ArbStr

        sut = ArbStr(max_length=20)
        actual = sut.arbitrary()
        assert type(actual) == str
        assert len(actual) <= 20

    def test_when_shrink_takes_a_string_python_then_returns_a_iterable_with_strings_smaller_than_the_original(self):
        from papylon.arbitrary import ArbStr

        sut = ArbStr(max_length=20)
        actual = list(sut.shrink('Python'))
        expected = ['ython', 'Pthon', 'Pyhon', 'Pyton', 'Pythn', 'Pytho']
        assert actual == expected


def test_arb_int_returns_arb_integer_instance():
    from papylon.arbitrary import arb_int, ArbInteger

    actual = arb_int()
    assert isinstance(actual, ArbInteger)


def test_arb_float_returns_arb_float_instance():
    from papylon.arbitrary import arb_float, ArbFloat

    actual = arb_float()
    assert isinstance(actual, ArbFloat)


def test_arb_char_returns_arb_char_instance():
    from papylon.arbitrary import arb_char, ArbChar

    actual = arb_char()
    assert isinstance(actual, ArbChar)


def test_arb_date_returns_arb_date_instance():
    from papylon.arbitrary import arb_date, ArbDate

    actual = arb_date()
    assert isinstance(actual, ArbDate)


def test_arb_list_returns_arb_list_instance():
    from papylon.arbitrary import arb_list, ArbFloat, ArbList
    arb_type = ArbFloat()
    actual = arb_list(arb_type)
    assert isinstance(actual, ArbList)


def test_arb_str_returns_arb_str_instance():
    from papylon.arbitrary import arb_str, ArbStr

    actual = arb_str()
    assert isinstance(actual, ArbStr)


def test_from_gen_returns_abstract_arbitrary_instance_with_given_gen_instance():
    from papylon.gen import choose
    from papylon.arbitrary import from_gen, AbstractArbitrary

    sut1 = from_gen(choose(0, 9))
    assert isinstance(sut1, AbstractArbitrary)
    sut2 = from_gen(choose(10, 99))
    assert isinstance(sut2, AbstractArbitrary)

    generated1 = sut1.arbitrary()
    assert 0 <= generated1 <= 9
    shrunk1 = list(sut1.shrink(5))
    assert shrunk1 == []
    generated1 = sut2.arbitrary()
    assert 10 <= generated1 <= 99
    shrunk2 = list(sut2.shrink(50))
    assert shrunk2 == []


def test_from_gen_shrink_returns_abstract_arbitrary_instance_with_given_gen_instance_and_shrinker():
    from papylon.gen import choose
    from papylon.shrinker import AbstractShrinker
    from papylon.arbitrary import from_gen_shrink, AbstractArbitrary

    class OriginalShrinker(AbstractShrinker):
        def shrink(self, value):
            return iter([0, 1, -1])
    shrinker = OriginalShrinker()
    sut = from_gen_shrink(choose(0, 9), shrinker)
    assert isinstance(sut, AbstractArbitrary)

    generated = sut.arbitrary()
    assert 0 <= generated <= 9
    shrunk = list(sut.shrink(5))
    assert shrunk == [0, 1, -1]
