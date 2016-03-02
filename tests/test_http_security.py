import pytest
from urllib.parse import urlparse


def test_endpoint_is_https_url(endpoint):
    o = urlparse(endpoint)
    assert o.scheme == 'https'
