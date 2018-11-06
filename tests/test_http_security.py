import pytest

from urllib.parse import urlparse

@pytest.mark.v1
@pytest.mark.v2
@pytest.mark.https
def test_endpoint_is_https_url(endpoint):
    o = urlparse(endpoint)
    assert o.scheme == 'https'
