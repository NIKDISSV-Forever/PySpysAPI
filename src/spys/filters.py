"""Module for convenient presentation of input data fields (see spy.one.get_content)"""
from __future__ import annotations

from difflib import get_close_matches
from typing import Callable, Type as _TypingType, Union

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

    def __new__(cls, item_or_index) -> int:
        values_count = len(cls.values)
        if isinstance(item_or_index, int) and -values_count <= item_or_index < values_count:
            return item_or_index % values_count
        if not isinstance(item_or_index, cls.type):
            item_or_index = cls.type(item_or_index)
        try:
            return cls.values.index(item_or_index)
        except ValueError:
            return cls.values.index(cls.nearest(item_or_index))

    def __class_getitem__(cls, item_or_index) -> type:
        return cls(item_or_index)

    @classmethod
    def nearest(cls, item):
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
    def nearest(cls, item) -> type:
        return cm[0] if (cm := get_close_matches(item.upper(), cls.values)) else cls.values[0]


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
    return *(proxy for proxy in proxies if key(proxy)),


ShowTypes = Union[Show.type, Show, _TypingType[Show]]
PortTypes = Union[Port.type, Port, _TypingType[Port]]
AnmTypes = Union[Anm.type, Anm, _TypingType[Anm]]
SSLTypes = Union[SSL.type, SSL, _TypingType[SSL]]
TypeTypes = Union[Type.type, Type, _TypingType[Type]]
SortTypes = Union[Sort.type, Sort, _TypingType[Sort]]
