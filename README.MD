spys - spys.me/spys.one Python API.

API для получения списка прокси с сайта spys.

> pip install -U [spys](https://pypi.org/project/spys/)

# Пакеты:

## spys

```python
from spys import me, one, filters, proxy_view

__all__ = ('me', 'one', 'filters', 'proxy_view')
```

## spys.me

```python
__all__ = ('DATA_REGEX', 'HOST',
           'Getters',
           'ProxyView', 'ResultType',
           'parse_proxies', 'get_proxies')

ResultType = tuple[str, ProxyViews, str]
HOST = 'https://spys.me/'
DATA_REGEX = ...  # Регулярное выражение для парсинга ответа от API


class ProxyView(BaseProxyView):
    def __init__(self, host: str, port: str,
                 country: str, anonymity: str, ssl_support: str, more_info: str, google_passed: str):
        ...

    more_info: bool  # Имеется ли дополнительная информация о прокси (Получение самой информации только из spys.one)
    google_passed: bool


def parse_proxies(data: str) -> ResultType:
    """Вернёт кортеж из доп. информации о API (str), списка прокси и доп. информации о списке прокси (str)"""
    ...


def get_content(protocol: str) -> str:
    """Отправит запрос на хост, вернёт спаршенную информацию (см. parse_proxies)"""
    ...


def get_proxies(protocol: str) -> ProxiesList:
    """
    Параметр protocol - либо proxy (http) либо socks
    Разрешённые протоколы: proxy, socks | socks5, all, http, https, ssl (https & socks ssl)
    :raise ValueError: если протокол не поддерживается
    """
    ...


class Getters:
    """Functions to concisely get different proxies"""

    @staticmethod
    def get_http_s_proxies() -> ProxyViews:  # http | https
        return get_proxies('proxy')

    @staticmethod
    def get_socks5_proxies() -> ProxyViews:
        return get_proxies('socks')

    @staticmethod
    def get_http_proxies() -> ProxyViews:
        return filter_proxies(get_proxies('proxy'), lambda x: not x.ssl_support)

    @staticmethod
    def get_https_proxies() -> ProxyViews:
        return filter_proxies(get_proxies('proxy'), lambda x: x.ssl_support)

    @classmethod
    def get_all_proxies(cls) -> ProxyViews:
        return cls.get_http_and_ssl_proxies() + cls.get_socks5_proxies()

    @classmethod
    def get_ssl_proxies(cls, from_proxies: ProxyViews = None) -> ProxyViews:
        return filter_proxies(cls.get_all_proxies() if from_proxies is None else from_proxies, lambda x: x.ssl_support)
```

## spys.one

### Не злоупотребляйте методами из этого модуля, существует риск бана.

![risk_of_blocking.png](https://github.com/NIKDISSV-Forever/PySpysAPI/blob/main/resources/risk_of_blocking.png?raw=true)

```python
__all__ = ('HOST', 'HTTP_PROXY_LIST_URL',
           'ProxyView',
           'get_content', 'get_proxies', 'parse_table')

HOST = 'https://spys.one/'
HTTP_PROXY_LIST_URL = urllib.parse.urljoin(HOST, 'http-proxy-list/')


class ProxyView(BaseProxyView):
    def __init__(self,
                 host: str, port: str, type: str, anonymity: str, country_city: tuple[str, str], hostname_org: str,
                 latency: str, uptime: str, check_date: str):
        ...

    type: str
    city: str
    hostname: str
    org: str
    latency: float | str
    uptime: int | str
    checks: int | str
    last_check_status: bool
    last_check_ago: str
    check_date: datetime.datetime | str


def get_content(show: int = 0, anm: int = 0, ssl: int = 0, sort: int = 0, port: int | None = 0, type: int = 0
                ) -> Generator[array.array | str | None, int | str | None, None]:
    """
    Низкоуровневая функция, параметры - input data поля см. get_proxies имена параметров.
    Вернёт генератор, если порт это None (xf4), 
        первый next (yield) вернёт список (array.array('H')) доступных портов,
        второй next примит порт (Воспользуйтесь методом send),
        и только третий next вернёт ответ от сайта (str).
    Если порт не None, первый next вернёт ответ от сайта.
    
    Ответ нужно передать в функцию parse_table, для получения списка прокси."""
    ...


def get_proxies(show: int = 0, anm: int = 0, ssl: int = 0, sort: int = 0, port: int = 0, type: int = 0) -> ProxyViews:
    ...


def parse_table(content: str) -> ProxyViews:
    """
    Парсит ответ от сайта и превратит данные с таблицы в класс ProxyView.
    Если установлен lxml (pip install lxml), будет использован он.
    """
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

## spys.proxy_view

```python
__all__ = ('BaseProxyView', 'ProxyViews')


class BaseProxyView:
    host: str
    port: int | str
    anonymity: str
    country: str
    more_info: str | bool

    def __str__(self):
        return f'{self.host}:{self.port}'


ProxyViews: Type[Iterable[BaseProxyView]] = Iterable[BaseProxyView]
```

### For English documentation use pydoc

> python -m pydoc -p 8081 [spys](http://localhost:8081/spys)
