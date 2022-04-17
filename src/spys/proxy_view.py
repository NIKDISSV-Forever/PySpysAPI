from typing import Callable, TypeVar, Union, Type, Iterable

__all__ = ('BaseProxyView', 'ProxyViews')

TI = TypeVar('TI')
TO = TypeVar('TO')


class BaseProxyView:
    __slots__ = ('host', 'port', 'anonymity', 'country',
                 'more_info')
    host: str
    port: Union[int, str]
    anonymity: str
    country: str
    more_info: Union[str, bool]

    @staticmethod
    def _convert_to(to_type: Callable[[TI], TO], val: TI) -> Union[TO, TI]:
        try:
            return to_type(val)
        except ValueError:
            return val

    def __str__(self):
        return f'{self.host}:{self.port}'

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__}({self}) at {hex(id(self)).upper()}>'


ProxyViews: Type[Iterable[BaseProxyView]] = Iterable[BaseProxyView]
