# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function
import time
import uuid
import copy
from json import dumps
from urllib import urlencode, unquote
from urlparse import urlparse, parse_qsl, ParseResult


def timestamp():
    """
    Returns a unix timestamp
    :return:
    """
    return int(time.time())


def uuid_or_string(data):
    """
    Convenience method
    :param data:
    :return:
    """
    if isinstance(data, uuid.UUID):
        return str(data)
    elif isinstance(data, basestring):
        return data
    raise ValueError('Expected string or UUID')


def filter_api_struct(api_struct, filter_dict):
    result = copy.copy(api_struct)

    keys_to_remove = []

    for key in filter_dict:
        if result[key] == filter_dict[key]:
            keys_to_remove.append(key)

    for key in keys_to_remove:
        del result[key]

    return result


def filter_dict_list(list_of_dicts, **field_filter):
    def _filter(_dicts, key, value):
        return [d for d in _dicts if d[key] == value]

    list_of_dicts = copy.copy(list_of_dicts)
    for key in field_filter:
        list_of_dicts = _filter(list_of_dicts, key, field_filter[key])

    return list_of_dicts


def add_url_params(url, params):
    """ Add GET params to provided URL being aware of existing.

    :param url: string of target URL
    :param params: dict containing requested params to be added
    :return: string with updated URL

    >> url = 'http://stackoverflow.com/test?answers=true'
    >> new_params = {'answers': False, 'data': ['some','values']}
    >> add_url_params(url, new_params)
    'http://stackoverflow.com/test?data=some&data=values&answers=false'

    Source: http://stackoverflow.com/a/25580545/591217
    """
    # Unquoting URL first so we don't loose existing args
    url = unquote(url)
    # Extracting url info
    parsed_url = urlparse(url)
    # Extracting URL arguments from parsed URL
    get_args = parsed_url.query
    # Converting URL arguments to dict
    parsed_get_args = dict(parse_qsl(get_args))
    # Merging URL arguments dict with new params
    parsed_get_args.update(params)

    # Bool and Dict values should be converted to json-friendly values
    # you may throw this part away if you don't like it :)
    parsed_get_args.update(
        {k: dumps(v) for k, v in parsed_get_args.items()
         if isinstance(v, (bool, dict))}
    )

    # Converting URL argument to proper query string
    encoded_get_args = urlencode(parsed_get_args, doseq=True)
    # Creating new parsed result object based on provided with new
    # URL arguments. Same thing happens inside of urlparse.
    new_url = ParseResult(
        parsed_url.scheme, parsed_url.netloc, parsed_url.path,
        parsed_url.params, encoded_get_args, parsed_url.fragment
    ).geturl()

    return new_url


def assert_dict_keys_in(d, allowed_keys):
    for key in d:
        assert key in allowed_keys


def ensure_trailing_slash(url):
    if not url.endswith('/'):
        url = '%s/' % url
    return url