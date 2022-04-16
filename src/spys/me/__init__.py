import re
import urllib.parse
import urllib.request
from typing import Iterable, Callable

from spys import HOST_ME, BaseProxyView

__all__ = ('DATA_REGEX', 'ProxyView', 'ProxyViews', 'ResultType', 'parse_proxies', 'get_proxies', 'filter_proxies')
DATA_REGEX = re.compile(r'(\d+\.\d+\.\d+\.\d+):(\d+)\s+(..)-(.)-(S)?(!*)-?\s+([+-])?')


class ProxyView(BaseProxyView):
    def __init__(self, host: str, port: str,
                 country_code: str, anonymity: str, ssl_support: str, proxy_software: str, google_passed: str):
        self.host = host
        self.port = self._convert_to(int, port)
        self.country_code = country_code
        self.anonymity = anonymity
        self.ssl_support = ssl_support == 'S'
        self.more_info = proxy_software == '!'
        self.google_passed = google_passed == '+'


ProxyViews = Iterable[ProxyView]
ResultType = tuple[str, ProxyViews, str]


def parse_proxies(data: str) -> ResultType:
    """Returns a tuple from the
     additional information about API (str), list of proxies and additional proxy list information (str)"""
    header, proxies_lines, footer = data.replace('\r', '').split('\n\n')
    return (header,
            tuple(ProxyView(*data) for data in DATA_REGEX.findall(proxies_lines)),
            footer)


def get_proxies(protocol: str) -> ProxyViews:
    """protocol parameter - either proxy (http) or socks"""
    return parse_proxies(urllib.request.urlopen(
        urllib.request.Request(urllib.parse.urljoin(HOST_ME, f'{protocol}.txt'),
                               headers={'User-Agent': 'Mozilla/5.0'})).read().decode('utf-8'))[1]


def filter_proxies(proxies: ProxyViews, key: Callable) -> ProxyViews:
    return tuple(filter(key, proxies))
