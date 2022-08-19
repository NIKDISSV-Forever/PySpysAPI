from __future__ import annotations

from typing import Callable, Iterable, TypeVar

__all__ = ('BaseProxyView', 'ProxyViews')

TI = TypeVar('TI')
TO = TypeVar('TO')


class BaseProxyView:
    __slots__ = ('host', 'port', 'anonymity', 'country',
                 'more_info')
    host: str
    port: int | str
    anonymity: str
    country: str
    more_info: str | bool

    @staticmethod
    def _convert_to(to_type: Callable[[TI], TO], val: TI) -> TO | TI:
        try:
            return to_type(val)
        except ValueError:
            return val

    def __str__(self):
        return f'{self.host}:{self.port}'

    def __repr__(self) -> str:
        return (
            f"<{self.__class__.__qualname__}(ip='{self}', anm={self.anonymity!r}, country={self.country!r})"
            f" at {hex(id(self))}>")


ProxyViews = Iterable[BaseProxyView]
