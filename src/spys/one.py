from __future__ import annotations

import urllib.parse
from array import array
from datetime import datetime
from typing import Generator

import bs4
from httpx import Client

from spys import filters
from spys.proxy_view import BaseProxyView, ProxyViews

__all__ = ('HOST', 'HTTP_PROXY_LIST_URL',
           'ProxyView',
           'get_content', 'get_proxies', 'parse_table')

HOST = 'https://spys.one/'
HTTP_PROXY_LIST_URL = urllib.parse.urljoin(HOST, 'en/http-proxy-list/')


class ProxyView(BaseProxyView):
    __slots__ = ('type', 'city', 'hostname', 'org', 'latency', 'uptime', 'checks',
                 'last_check_status', 'last_check_ago', 'check_date')

    def __init__(self,
                 host: str, port: str, type: str, anonymity: str, country_city: tuple[str, str], hostname_org: str,
                 latency: str, uptime: str, check_date: str):
        self.host = host
        self.port = self._convert_to(int, port)
        self.type = type
        self.anonymity = anonymity
        if len(country_city) < 2:
            country_city += '',
        country_city = (*country_city[0].split(),)
        while len(country_city) < 2:
            country_city += '',
        self.country = country_city[0]
        self.city = country_city[1].strip('()')
        self.more_info = country_city[1]
        hostname_org = hostname_org.split(' ', 1)
        while len(hostname_org) < 2:
            hostname_org.append('')
        self.hostname, self.org = hostname_org
        self.latency = self._convert_to(float, latency)
        _uptime = uptime.split(' ')
        while len(_uptime) < 3:
            _uptime.insert(0, '')
        self.uptime = self._convert_to(int, _uptime[0].rstrip('%'))
        self.checks = self._convert_to(int, _uptime[1].strip('()'))
        self.last_check_status = _uptime[2] == '+'
        _check_date = check_date.partition('(')
        self.last_check_ago = _check_date[2].rstrip(')')
        self.check_date: datetime | str = self._convert_to(lambda s: datetime.strptime(s, '%d-%b-%Y %H:%M'),
                                                           _check_date[0].strip())


def get_content(show: filters.ShowTypes = 0,
                anm: filters.AnmTypes = 0,
                ssl: filters.SSLTypes = 0,
                sort: filters.SortTypes = 0,
                port: filters.PortTypes | None = 0,
                type: filters.TypeTypes = 0
                ) -> Generator[array | str | None, int | str | None, None]:
    """
    Low-level function, parameters - input data fields see get_proxies parameter names.
    Will return the generator if the port is None (xf4),
        the first next (yield) will return a list (array.array('H')) of available ports,
        the second next will accept the port (Use the send method),
        and only the third next will return the response from the site (str).
    If the port is not None, the first next will return the response from the site.

    The answer must be passed to the parse_table function to get a list of proxies.
    """
    with Client() as client:
        xx0_soup = _best_bs4_future(client.post('https://spys.one/en/http-proxy-list/',
                                                headers={'User-Agent': 'Mozilla/5.0'}).text)
        token = xx0_soup.find_all('input', {'name': 'xx0'})[0]['value']
        if port is None:
            yield array('H', [opt.contents[0] for opt in xx0_soup.find_all(attrs={'id': 'xf4'})[0].find_all('option')])
            port = yield
            port = str(port)
        while True:
            yield client.post(HTTP_PROXY_LIST_URL,
                              headers={'referer': HTTP_PROXY_LIST_URL, 'User-Agent': 'Mozilla/5.0'},
                              data={'xx0': token,
                                    'xpp': show,
                                    'xf1': anm,
                                    'xf2': ssl,
                                    'xf3': sort,
                                    'xf4': port,
                                    'xf5': type}
                              ).text


def parse_table(content: str) -> ProxyViews:
    """
    Parse the response from the site and turn the data from the table into the ProxyView class.
    If lxml is installed (pip install lxml), it will be used.
    """
    soup = _best_bs4_future(content)
    exec(soup.find_all('script', {'type': 'text/javascript'})[0].text, obfuscated := {})
    try:
        del obfuscated['__builtins__']
    except KeyError:
        pass
    return (*(
        ProxyView(
            *((cols[0].text,
               eval(cols[0].find_all('script')[0].text[:-1].split('+', 1)[1].replace('(', 'str(', 5), obfuscated))
              + (*(col.text for col in cols[1:3]),)
              + ((cols[3].text, acronym.get('title')) if (acronym := cols[3].find('acronym')) else (cols[3].text,),)
              + (*(col.text for col in cols[4:] if col.text),)))
        for cols in (row.find_all('td') for row in soup.find_all('table')[2].find_all('tr')[2:-1]) if len(cols) > 1),)


def get_proxies(show: filters.ShowTypes = 0,
                anm: filters.AnmTypes = 0,
                ssl: filters.SSLTypes = 0,
                sort: filters.SortTypes = 0,
                port: filters.PortTypes = 0,
                type: filters.TypeTypes = 0) -> ProxyViews:
    port = filters.Port(port)
    return parse_table(next(get_content(
        filters.Show(show), filters.Anm(anm), filters.SSL(ssl), filters.Sort(sort),
        0 if port is None else port, filters.Type(type)))
    )


def _best_bs4_future(markup: str) -> bs4.BeautifulSoup:
    try:
        return bs4.BeautifulSoup(markup, 'lxml')
    except bs4.FeatureNotFound:
        return bs4.BeautifulSoup(markup, 'html.parser')
