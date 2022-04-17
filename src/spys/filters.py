"""Module for convenient presentation of input data fields (see spy.one.get_content)"""
import difflib
from typing import Callable

from spys.proxy_view import ProxyViews


class IntChoice:
    """
    Base class.
    The correct representation of the data can be obtained by passing the desired filter to the
    class constructor (__new__ method) or via getitem (__class_getitem__ method)
    """
    __slots__ = ()
    values = ()
    type = int

    def __new__(cls, item) -> type:
        if item in range(len(cls.values) + 1):
            return item
        if not isinstance(item, cls.type):
            item = cls.type(item)
        try:
            return cls.values.index(item)
        except ValueError:
            return cls.values.index(cls.about(item))

    def __class_getitem__(cls, item) -> type:
        return cls(item)

    @classmethod
    def about(cls, item):
        """If a value not from cls.values is passed, then the nearest value will be selected using this method"""
        return min(cls.values, key=lambda i: abs(i - item))


class Show(IntChoice):
    __slots__ = ()
    values = (30, 50, 100, 200, 300, 500)


class Port(IntChoice):
    __slots__ = ()
    values = (0, 3182, 8080, 80)


class StringChoice(IntChoice):
    __slots__ = ()
    type = str

    @classmethod
    def about(cls, item) -> type:
        return cm[0] if (cm := difflib.get_close_matches(item.upper(), cls.values)) else cls.values[0]


class Anm(StringChoice):
    __slots__ = ()
    values = ('ALL', 'A+H', 'NOA', 'ANM', 'HIA')


class SSL(StringChoice):
    __slots__ = ()
    values = ('ALL', 'SSL+', 'SSL-')


class Type(StringChoice):
    __slots__ = ()
    values = ('ALL', 'HTTP', 'SOCKS')


class Sort(StringChoice):
    __slots__ = ()
    values = ('DATE', 'SPEED')


def filter_proxies(proxies: ProxyViews, key: Callable = None) -> ProxyViews:
    return tuple(proxy for proxy in proxies if key(proxy))
