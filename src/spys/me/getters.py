"""Functions to concisely get different proxies"""
from src.spys.me import *


def get_http_and_ssl_proxies() -> ProxyViews:
    return get_proxies('proxy')


def get_socks5_proxies() -> ProxyViews:
    return get_proxies('socks')


def get_all_proxies() -> ProxyViews:
    # noinspection PyUnresolvedReferences
    return get_http_and_ssl_proxies() + get_socks5_proxies()


def get_http_proxies() -> ProxyViews:
    return filter_proxies(get_proxies('proxy'), lambda x: not x.ssl_support)


def get_https_proxies() -> ProxyViews:
    return filter_proxies(get_proxies('proxy'), lambda x: x.ssl_support)


def get_ssl_proxies() -> ProxyViews:
    return filter_proxies(get_all_proxies(), lambda x: x.ssl_support)
