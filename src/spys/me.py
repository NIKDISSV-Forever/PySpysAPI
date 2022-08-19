from __future__ import annotations

import urllib.parse
import urllib.request
from re import compile as re_compile

from spys import filters
from spys.proxy_view import BaseProxyView, ProxyViews

__all__ = ('DATA_REGEX', 'HOST',
           'Getters',
           'ProxyView',
           'parse_proxies', 'get_proxies')

HOST = 'https://spys.me/'
DATA_REGEX = re_compile(r'(\d+\.\d+\.\d+\.\d+):(\d+)\s+(..)-(.)-?(S?)(!?)\s+([+-]?)')


class UnknownProtocol(ValueError):
    __slots__ = ()


class ProxyView(BaseProxyView):
    __slots__ = ('ssl_support', 'google_passed')

    def __init__(self, host: str, port: str,
                 country: str, anonymity: str, ssl_support: str, more_info: str, google_passed: str):
        self.host = host
        self.port = self._convert_to(int, port)
        self.country = country
        self.anonymity = anonymity
        self.ssl_support = ssl_support == 'S'
        self.more_info = more_info == '!'
        self.google_passed = google_passed == '+'


def parse_proxies(data: str) -> tuple[str, ProxyViews, str]:
    """
    Returns a tuple from the additional information about API (str),
    list of proxies and additional proxy list information (str)
    """
    header, proxies_lines, footer = data.replace('\r', '').split('\n\n')
    return (header,
            (*(ProxyView(*data) for data in DATA_REGEX.findall(proxies_lines)),),
            footer)


def get_content(protocol: str) -> str:
    """Send a request to the host, return the parsed information (see parse_proxies)"""
    with urllib.request.urlopen(
            urllib.request.Request(urllib.parse.urljoin(HOST, f'{protocol}.txt'),
                                   headers={'User-Agent': 'Mozilla/5.0'})) as resp:
        return resp.read().decode()


def _get_proxies(protocol: str) -> ProxyViews:
    """
    Protocol parameter - either "proxy" or "socks".
    """
    return parse_proxies(get_content(protocol))[1]


def get_proxies(protocol: str = 'proxy') -> ProxyViews:
    """
    Protocol parameter - either proxy (http) or socks (socks5).
    Allowed protocols: proxy, socks | socks5, all, http, https, ssl (https & socks ssl)
    """
    protocol = protocol.lower().removesuffix('5')
    return {'all': Getters.get_all_proxies,
            'http': Getters.get_http_proxies, 'https': Getters.get_https_proxies,
            'ssl': Getters.get_ssl_proxies}.get(protocol, lambda: _get_proxies(protocol))()


class Getters:
    """Functions to concisely get different proxies"""
    __slots__ = ()

    @staticmethod
    def get_http_s_proxies() -> ProxyViews:  # http | https
        return get_proxies('proxy')

    @staticmethod
    def get_http_proxies() -> ProxyViews:
        return filters.filter_proxies(get_proxies('proxy'), lambda x: not x.ssl_support)

    @staticmethod
    def get_https_proxies() -> ProxyViews:
        return filters.filter_proxies(get_proxies('proxy'), lambda x: x.ssl_support)

    @staticmethod
    def get_socks5_proxies() -> ProxyViews:
        return get_proxies('socks')

    @classmethod
    def get_all_proxies(cls) -> ProxyViews:
        # noinspection PyUnresolvedReferences
        return cls.get_http_s_proxies() + cls.get_socks5_proxies()

    @classmethod
    def get_ssl_proxies(cls, from_proxies: ProxyViews = None) -> ProxyViews:  # socks with ssl and https
        return filters.filter_proxies(cls.get_all_proxies() if from_proxies is None else from_proxies,
                                      lambda x: x.ssl_support)
