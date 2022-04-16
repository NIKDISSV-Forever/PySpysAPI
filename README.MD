spys - spys.me/spys.one Python API.

API для получения списка прокси с сайта spys.

> pip install -U [spys](https://pypi.org/project/spys/)

# Пакеты:

## spys

```python
__all__ = ('HOST_ONE', 'HOST_ME', 'BaseProxyView')
HOST_ONE = 'https://spys.one/'
HOST_ME = 'https://spys.me/'


class BaseProxyView: ...
```

## spys.me

```python
__all__ = ('DATA_REGEX', 'ProxyView', 'ProxiesList', 'ResultType', 'parse_proxies', 'get_proxies', 'filter_proxies')
DATA_REGEX = ...  # Регулярное выражение для парсинга ответа от API


class ProxyView(BaseProxyView):
    host: str
    port: int | str
    country_code: str
    anonymity: str
    ssl_support: bool
    more_info: str  # Имеется дополнительная информация о прокси (Получение только из spys.one)
    google_passed: str


ProxyViews = Iterable[ProxyView]
ResultType = tuple[str, ProxiesList, str]  # head, proxies, footer


def parse_proxies(data: str) -> ResultType:
    """Вернёт кортеж из доп. информации о API (str), списка прокси и доп. информации о списке прокси (str)"""
    ...


def get_proxies(protocol: str) -> ProxiesList:
    """Параметр protocol - либо proxy (http) либо socks"""
    ...


def filter_proxies(proxies: ProxiesList, key: Callable) -> ProxiesList:
    return tuple(filter(key, proxies))
```

## spys.me.getters

```python
"""Функции для краткой записи получения различных прокси"""
from spys import *


def get_http_and_ssl_proxies() -> ProxyViews:
    return get_proxies('proxy')


def get_socks5_proxies() -> ProxyViews:
    return get_proxies('socks')


def get_all_proxies() -> ProxyViews:
    return get_http_and_ssl_proxies() + get_socks5_proxies()


def get_http_proxies() -> ProxyViews:
    return filter_proxies(get_proxies('proxy'), lambda x: not x.ssl_support)


def get_https_proxies() -> ProxyViews:
    return filter_proxies(get_proxies('proxy'), lambda x: x.ssl_support)


def get_ssl_proxies() -> ProxyViews:
    return filter_proxies(get_all_proxies(), lambda x: x.ssl_support)

```

## spys.one

### Не злоупотребляйте методами из этого модуля, существует риск бана.

![risk_of_blocking.png](https://github.com/NIKDISSV-Forever/PySpysAPI/blob/main/resources/risk_of_blocking.png?raw=true)

```python

__all__ = ('ProxyView', 'ProxyViews', 'get_content', 'get_proxies', 'parse_table')

HTTP_PROXY_LIST_URL = urllib.parse.urljoin(HOST_ONE, 'http-proxy-list/')


class ProxyView(BaseProxyView):
    host: str
    port: int | str
    type: str
    anonymity: str
    country_city: list[str, str]  # ['Страна', '(Город)']
    country, city: str
    more_info: str  # Строка с доп. инфой о ПО прокси
    hostname_org: list[str, str]  # ['Хост', 'Организация']
    hostname, org: str
    latency: float | str
    uptime: int  # %
    checks: int
    last_check_status: bool
    last_check_ago: str  # Сколько секунд/минут/часов/... назад была проверка
    check_date: datetime.datetime | str


ProxyViews = tuple[ProxyView]


def get_content(xpp: int = 0, xf1: int = 0, xf2: int = 0, xf3: int = 0, xf4: Optional[int] = 0,
                xf5: int = 0) -> Generator[int | str | None, int | str | None, None]:
    """
    Низкоуровневая функция, параметры - input data поля см. get_proxies имена параметров.
    Вернёт генератор, если порт это None (xf4), 
        первый next (yield) вернёт список доступных портов,
        второй next примит порт (Воспользуйтесь методом send),
        и только третий next вернёт ответ от сайта (str).
    Если порт не None, первый next вернёт ответ от сайта.
    
    Ответ нужно передать в функцию parse_table, для получения списка прокси."""
    ...


def get_proxies(show: int = 0, anm: int = 0, ssl: int = 0, sort: int = 0, port: int = 0, type: int = 0) -> ProxyViews:
    return parse_table(next(get_content(show, anm, ssl, sort, 0 if port is None else port, type)))


def parse_table(content: str) -> ProxyViews:
    """Парсит ответ от сайта и превратит данные с таблицы в класс ProxyView"""
    ...
```

## spys.filters

```python
"""Модуль для удобного представления input data полей (см spys.one.get_content)"""


class IntChoice:
    """
    Базовый класс.
    Правильное представление данных можно получить передав желаемый фильтр в
    конструктор класса (метод __new__) или через getitem (__class_getitem__)
    """
    __slots__ = ()
    values = ()
    type = int

    def __new__(cls, item) -> type:
        ...

    def __class_getitem__(cls, item) -> type:
        ...

    @classmethod
    def about(cls):
        """
        Если передано значение не из cls.values, то с помощью этого метода будет выбранно близжаешее к тому значение
        """
        ...


class Show(IntChoice):
    values = (30, 50, 100, 200, 300, 500)


class Port(IntChoice):
    values = (0, 3182, 8080, 80)


class StringChoice(IntChoice):
    type = str


class Anm(StringChoice):
    values = ('ALL', 'A+H', 'NOA', 'ANM', 'HIA')


class SSL(StringChoice):
    values = ('ALL', 'SSL+', 'SSL-')


class Type(StringChoice):
    values = ('ALL', 'HTTP', 'SOCKS')


class Sort(StringChoice):
    values = ('DATE', 'SPEED')
```
