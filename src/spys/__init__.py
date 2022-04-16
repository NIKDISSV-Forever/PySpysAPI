from typing import Callable

__all__ = ('HOST_ONE', 'HOST_ME', 'BaseProxyView')
HOST_ONE = 'https://spys.one/'
HOST_ME = 'https://spys.me/'


class BaseProxyView:
    __slots__ = ('host', 'port')

    @staticmethod
    def _convert_to(func: Callable, val):
        try:
            return func(val)
        except ValueError:
            return val

    def __str__(self):
        return f'{self.host}:{self.port}'

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__}({self}) at {hex(id(self)).upper()}>'
