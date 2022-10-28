from starlette.datastructures import URL
from secrets import choice
from string import ascii_lowercase, digits


def get_domain_name(url: str) -> str:
    domain_name = url.replace('http://', '').replace('https://', '')
    return domain_name


def build_short_postfix() -> str:
    symbols = ascii_lowercase + digits
    postfix = ''.join(choice(symbols) for _ in range(9))
    return postfix


def build_short_link(short_postfix: str, url: URL):
    return str(url) + short_postfix
