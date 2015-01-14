# -*- coding: utf-8 -*-
def test_when_IntShrinker_shrink_takes_positive_value_then_returns_a_iterable_with_values_smaller_than_arg():
    from papylon.shrinker import IntShrinker

    sut = IntShrinker()
    actual = list(sut.shrink(10))
    expected = [0, 5, -5, 8, -8, 9, -9]
    assert actual == expected


def test_when_IntShrinker_shrink_takes_negative_value_then_returns_a_iterable_with_values_smaller_than_arg():
    from papylon.shrinker import IntShrinker

    sut = IntShrinker()
    actual = list(sut.shrink(-10))
    expected = [0, -5, 5, -8, 8, -9, 9]
    assert actual == expected


def test_when_IntShrinker_shrink_takes_zero_then_returns_empty_list():
    from papylon.shrinker import IntShrinker

    sut = IntShrinker()
    actual = list(sut.shrink(0))
    assert actual == []


def test_when_FloatShrinker_shrink_takes_positive_value_then_returns_a_iterable_with_values_smaller_than_arg():
    from papylon.shrinker import FloatShrinker

    sut = FloatShrinker()
    actual = list(sut.shrink(10.0))
    expected = [0.0, 5.0, -5.0, 7.5, -7.5, 8.75, -8.75, 9.375, -9.375, 9.6875, -9.6875, 9.84375, -9.84375,
                9.921875, -9.921875, 9.9609375, -9.9609375, 9.98046875, -9.98046875, 9.990234375, -9.990234375,
                9.9951171875, -9.9951171875, 9.99755859375, -9.99755859375, 9.998779296875, -9.998779296875]
    assert actual == expected


def test_when_FloatShrinker_shrink_takes_negative_value_then_returns_a_iterable_with_values_smaller_than_arg():
    from papylon.shrinker import FloatShrinker

    sut = FloatShrinker()
    actual = list(sut.shrink(-10.0))
    expected = [0.0, -5.0, 5.0, -7.5, 7.5, -8.75, 8.75, -9.375, 9.375, -9.6875, 9.6875, -9.84375, 9.84375,
                -9.921875, 9.921875, -9.9609375, 9.9609375, -9.98046875, 9.98046875, -9.990234375, 9.990234375,
                -9.9951171875, 9.9951171875, -9.99755859375, 9.99755859375, -9.998779296875, 9.998779296875]
    assert actual == expected


def test_when_FloatShrinker_shrink_takes_zero_then_returns_empty_list():
    from papylon.shrinker import FloatShrinker

    sut = FloatShrinker()
    actual = list(sut.shrink(0.0))
    assert actual == []


def test_when_FloatShrinker_shrink_takes_positive_infinity_value_then_returns_a_list_of_zero():
    from papylon.shrinker import FloatShrinker

    sut = FloatShrinker()
    actual = list(sut.shrink(float('inf')))
    assert actual == [0.0]


def test_when_FloatShrinker_shrink_takes_negative_infinity_value_then_returns_a_list_of_zero():
    from papylon.shrinker import FloatShrinker

    sut = FloatShrinker()
    actual = list(sut.shrink(float('-inf')))
    assert actual == [0.0]


def test_when_FloatShrinker_shrink_takes_Nan_value_then_returns_a_list_of_zero():
    from papylon.shrinker import FloatShrinker

    sut = FloatShrinker()
    actual = list(sut.shrink(float('nan')))
    assert actual == [0.0]


def test_when_CharShrinker_shrink_takes_upper_charactor_then_returns_a_list_with_a_b_c():
    from papylon.shrinker import CharShrinker

    sut = CharShrinker()
    actual = list(sut.shrink('P'))
    assert actual == ['a', 'b', 'c']


def test_when_CharShrinker_shrink_takes_lower_charactor_except_for_a_b_c_then_returns_a_list_with_a_b_c():
    from papylon.shrinker import CharShrinker

    sut = CharShrinker()
    actual = list(sut.shrink('d'))
    assert actual == ['a', 'b', 'c']


def test_when_CharShrinker_shrink_takes_lower_c_then_returns_a_list_with_a_b():
    from papylon.shrinker import CharShrinker

    sut = CharShrinker()
    actual = list(sut.shrink('c'))
    assert actual == ['a', 'b']


def test_when_CharShrinker_shrink_takes_lower_a_then_returns_an_empty_list():
    from papylon.shrinker import CharShrinker

    sut = CharShrinker()
    actual = list(sut.shrink('a'))
    assert actual == []


def test_when_DateShrinker_shrink_takes_2012_02_29_01_23_45_then_returns_a_list_with_2012_02_29_01_23_00():
    from papylon.shrinker import DateShrinker
    import datetime

    sut = DateShrinker()
    actual = list(sut.shrink(datetime.datetime(2012, 2, 29, 1, 23, 45)))
    expected = [datetime.datetime(2012, 2, 29, 1, 23)]
    assert actual == expected


def test_when_DateShrinker_shrink_takes_2013_03_01_12_34_00_then_returns_a_list_with_2013_03_01_12_00_00():
    from papylon.shrinker import DateShrinker
    import datetime

    sut = DateShrinker()
    actual = list(sut.shrink(datetime.datetime(2013, 3, 1, 12, 34)))
    expected = [datetime.datetime(2013, 3, 1, 12)]
    assert actual == expected


def test_when_DateShrinker_shrink_takes_2014_11_22_23_00_00_then_returns_a_list_with_2014_11_22_00_00_00():
    from papylon.shrinker import DateShrinker
    import datetime

    sut = DateShrinker()
    actual = list(sut.shrink(datetime.datetime(2014, 11, 22, 23)))
    expected = [datetime.datetime(2014, 11, 22)]
    assert actual == expected


def test_when_DateShrinker_shrink_takes_2015_01_09_00_00_00_then_returns_an_empty_list():
    from papylon.shrinker import DateShrinker
    import datetime

    sut = DateShrinker()
    actual = list(sut.shrink(datetime.datetime(2015, 1, 9)))
    assert actual == []


def test_when_ListShrinker_shrink_takes_a_3_elements_list_then_returns_a_list_with_lists_which_are_smaller_than_origin():
    from papylon.shrinker import ListShrinker

    sut = ListShrinker()
    actual = list(sut.shrink([1, 2, 3]))
    expected = [[2, 3], [1, 3], [1, 2]]
    assert actual == expected


def test_when_ListShrinker_shrink_takes_a_1_element_list_then_returns_a_list_contains_an_empty_list():
    from papylon.shrinker import ListShrinker

    sut = ListShrinker()
    actual = list(sut.shrink([3.5]))
    assert actual == [[]]


def test_when_ListShrinker_shrink_takes_an_empty_list_then_returns_an_empty_list():
    from papylon.shrinker import ListShrinker

    sut = ListShrinker()
    actual = list(sut.shrink([]))
    assert actual == []


def test_when_StrShrinker_shrink_takes_a_string_then_returns_a_iterable_with_new_smaller_strings():
    from papylon.shrinker import StrShrinker

    sut = StrShrinker()
    actual = list(sut.shrink('Spam'))
    expected = ['pam', 'Sam', 'Spm', 'Spa']
    assert actual == expected


def test_when_StrShrinker_shrink_takes_a_empty_string_then_returns_a_empty_list():
    from papylon.shrinker import StrShrinker

    sut = StrShrinker()
    actual = list(sut.shrink(''))
    assert actual == []
