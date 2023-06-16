import logging.config

from urllib import parse

import requests


import settings
from client import oauth

logging.config.dictConfig(settings.LOGGER)
logger = logging.getLogger(__name__)

session = requests.Session()
session.auth = oauth


def test_connection() -> bool:
    try:
        response = session.get(ends_with_slash(settings.URL))
        response.raise_for_status()  # raise an exception if the status code is not 200
        logger.info('Connection succeeded.')
        return True
    except requests.exceptions.HTTPError as err:
        logger.error(f'Connection failed: {err}')
        return False


def ends_with_slash(url: str) -> str:
    return url if url.endswith('/') else url + '/'


def remove_leading_slash(s: str) -> str:
    return s[1:] if s.startswith('/') else s


def normalize_relative_url(relative_url: str) -> str:
    return remove_leading_slash(ends_with_slash(relative_url))


def make_request(method: str, relative_url: str, pk: str = None, params=None, **kwargs) -> requests.Response:
    if params is None:
        params = dict()
    url = parse.urljoin(ends_with_slash(settings.URL), normalize_relative_url(relative_url))
    if pk:
        url += ends_with_slash(pk.__str__())
    return session.request(method, url, params=params, **kwargs)


def get(relative_url, params=None) -> requests.Response:
    return make_request('GET', relative_url, params=params)


def post(relative_url, params=None, **kwargs) -> requests.Response:
    return make_request('POST', relative_url, params=params, **kwargs)


def patch(relative_url, pk: str, params=None, **kwargs) -> requests.Response:
    return make_request('PATCH', relative_url, pk=pk, params=params, **kwargs)


def delete(relative_url, pk, params=None, **kwargs)-> requests.Response:
    return make_request('DELETE', relative_url, pk=pk, params=params, **kwargs)