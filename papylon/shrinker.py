"""Classes to shrink results with their counter-examples."""

import itertools
import math
import datetime


class AbstractShrinker:
    """An abstract class to shrink arguments."""

    def shrink(self, value):
        """
        Shrink arguments with a given value.

        :param value:
            The value of counter-example.

        :return:
        """

        raise NotImplementedError("AbstractShrinker#shrink")


def _interleave(xs, ys):
    _xs = xs
    _ys = ys
    result = []
    while True:
        if len(_xs) == 0:
            return itertools.chain(result, _ys)
        if len(_ys) == 0:
            return itertools.chain(result, _xs)
        x = _xs[0]
        _xs = _xs[1:]
        y = _ys[0]
        _ys = _ys[1:]
        result.append(x)
        result.append(y)


def _empty_iterable():
    return iter([])


class IntShrinker(AbstractShrinker):
    """A shrinker of integer."""

    def shrink(self, value):
        """
        Return an int iterator of shrunk result.

        :param value: int
            The int value of counter-example.

        :return:
            The int iterator which is shrunk with a given value.
        """

        def halfs(n):
            result = []
            if n != 0:
                v = n
                while v != 0:
                    result.append(v)
                    v = int(v / 2)
            return result

        if value == 0:
            return _empty_iterable()
        else:
            ns = list(map(lambda n: value - n, halfs(int(value / 2))))
            return itertools.chain([0], _interleave(ns, list(map(lambda n: (-1) * n, ns))))


class FloatShrinker(AbstractShrinker):
    """A shrinker of floating point number."""

    def shrink(self, value):
        """
        Return a float iterator of shrunk result.

        :param value: float
            The float value of counter-example.

        :return:
            The float iterator which is shrunk with a given value.
        """

        def halfs(n):
            result = []
            if n != 0:
                v = n
                # TODO: precision problem.
                # given too large float number, shrink treats too large iterable.
                while v < -0.001 or 0.001 < v:
                    result.append(v)
                    v /= 2
            return result

        if value == 0:
            return _empty_iterable()
        elif (abs(value) == float('inf')) or (math.isnan(value)):
            return iter([0.0])
        else:
            ns = list(map(lambda n: value - n, halfs(value / 2)))
            return itertools.chain([0], _interleave(ns, list(map(lambda n: (-1) * n, ns))))


class CharShrinker(AbstractShrinker):
    """A shrinker of character."""

    def shrink(self, value):
        """
        Return a char iterator of shrunk result.

        :param value: str
            The 1-length str value of counter-example.

        :return:
            The char iterator which is shrunk with a given value.
        """

        result = []
        for c in ['a', 'b', 'c']:
            if (ord(c) < ord(value)) or (not str.islower(value)):
                result.append(c)

        return iter(result)


class DateShrinker(AbstractShrinker):
    """A shrinker of date."""

    def shrink(self, value):
        """
        Return a date iterator of shrunk result.

        :param value: datetime.datetime
            The datetime value of counter-example.

        :return:
            The datetime iterator which is shrunk with a given value.
        """

        if value.second != 0:
            return iter([datetime.datetime(value.year, value.month, value.day, value.hour, value.minute)])
        elif value.minute != 0:
            return iter([datetime.datetime(value.year, value.month, value.day, value.hour)])
        elif value.hour != 0:
            return iter([datetime.datetime(value.year, value.month, value.day)])
        else:
            return _empty_iterable()


class ListShrinker(AbstractShrinker):
    """A shrinker of list."""

    def shrink(self, value):
        """
        Return a list iterator of shrunk result.

        :param value: list
            The list value of counter-example.

        :return:
            The list iterator which is shrunk with a given value.
        """

        def shrink_list(l):
            if not l:
                return []
            elif len(l) == 1:
                yield []
            else:
                x = l[0]
                xs = l[1:]
                yield xs
                for _xs in shrink_list(xs):
                    yield list(itertools.chain([x], _xs))
                # should elements be shrunk?
                # for _x in shrink_by_type(x):
                #     yield itertools.chain([_x], xs)

        return iter(shrink_list(value))


class StrShrinker(AbstractShrinker):
    """A shrinker of str."""

    def shrink(self, value):
        """
        Return a str iterator of shrunk result.

        :param value: str
            The str value of counter-example.

        :return:
            The str iterator which is shrunk with a given value.
        """

        shrinker = ListShrinker()
        return iter(map(lambda s: str.join("", s), shrinker.shrink(value)))
