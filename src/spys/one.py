import urllib.parse
from datetime import datetime
from typing import Optional, Generator, Union

import requests
from bs4 import BeautifulSoup

from spys import HOST_ONE, BaseProxyView

__all__ = ('ProxyView', 'ProxyViews', 'get_content', 'get_proxies', 'parse_table')

HTTP_PROXY_LIST_URL = urllib.parse.urljoin(HOST_ONE, 'http-proxy-list/')


class ProxyView(BaseProxyView):

    def __init__(self,
                 host: str, port: str, type: str, anonymity: str, country_city: tuple[str, str], hostname_org: str,
                 latency: str, uptime: str, check_date: str):
        self.host = host
        self.port = self._convert_to(int, port)
        self.type = type
        self.anonymity = anonymity
        if len(country_city) < 2:
            country_city += '',
        self.country_city = country_city[0].split()
        while len(self.country_city) < 2:
            self.country_city += '',
        self.country, self.city = self.country_city[0], self.country_city[1].strip('()')
        self.more_info = country_city[1]
        self.hostname_org = hostname_org.split(' ', 1)
        self.hostname, self.org = self.hostname_org
        self.latency = self._convert_to(float, latency)
        self._uptime = uptime.split(' ')
        while len(self._uptime) < 3:
            self._uptime.insert(0, '')
        self.uptime = self._convert_to(int, self._uptime[0].rstrip('%'))
        self.checks = self._convert_to(int, self._uptime[1].strip('()'))
        self.last_check_status = self._uptime[2] == '+'
        _check_date = check_date.partition('(')
        self.last_check_ago = _check_date[2].rstrip(')')
        self.check_date: Union[datetime, str] = self._convert_to(lambda s: datetime.strptime(s, '%d-%b-%Y %H:%M'),
                                                                 _check_date[0].strip())


ProxyViews = tuple[ProxyView]


def get_content(xpp: int = 0, xf1: int = 0, xf2: int = 0, xf3: int = 0, xf4: Optional[int] = 0,
                xf5: int = 0) -> Generator[Union[int, str, None], Union[int, str, None], None]:
    """
    Low-level function, parameters - input data fields see get_proxies parameter names.
    Will return the generator if the port is None (xf4),
        the first next (yield) will return a list of available ports,
        the second next will accept the port (Use the send method),
        and only the third next will return the response from the site (str).
    If the port is not None, the first next will return the response from the site.

    The answer must be passed to the parse_table function to get a list of proxies.
    """
    with requests.session() as ses:
        xx0_soup = BeautifulSoup(ses.post('https://spys.one/en/http-proxy-list/',
                                          headers={
                                              'User-Agent': 'Mozilla/5.0'}).text,
                                 'html.parser')
        xx0 = xx0_soup.find('input', {'name': 'xx0'})['value']
        if xf4 is None:
            yield [opt.contents[0] for opt in xx0_soup.find(attrs={'id': 'xf4'}).find_all('option')]
            xf4 = yield
            xf4 = str(xf4)
        while True:
            yield ses.post(HTTP_PROXY_LIST_URL,
                           headers={'referer': HTTP_PROXY_LIST_URL, 'User-Agent': 'Mozilla/5.0'},
                           data={
                               'xx0': xx0, 'xpp': xpp, 'xf1': xf1, 'xf2': xf2, 'xf3': xf3, 'xf4': xf4, 'xf5': xf5}).text


def get_proxies(show: int = 0, anm: int = 0, ssl: int = 0, sort: int = 0, port: int = 0, type: int = 0) -> ProxyViews:
    return parse_table(next(get_content(show, anm, ssl, sort, 0 if port is None else port, type)))


def parse_table(content: str) -> ProxyViews:
    """Parse the response from the site and turn the data from the table into the ProxyView class"""
    soup = BeautifulSoup(content, 'html.parser')
    exec(soup.find('script', {'type': 'text/javascript'}).text, obfuscated := {})
    try:
        del obfuscated['__builtins__']
    except KeyError:
        pass
    return tuple(
        ProxyView(
            *((cols[0].text,
               eval(cols[0].find('script').text[:-1].split('+', 1)[1].replace('(', 'str(', 5), obfuscated))
              + tuple(col.text for col in cols[1:3])
              + ((cols[3].text, acronym.get('title')) if (acronym := cols[3].find('acronym')) else (cols[3].text,),)
              + tuple(col.text for col in cols[4:] if col.text)))
        for cols in (row.find_all('td') for row in soup.find_all('table')[2].find_all('tr')[2:-1]) if len(cols) > 1)
