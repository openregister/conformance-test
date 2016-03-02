import pytest
import requests
from urllib.parse import urljoin


class TestRegisterResourceJson(object):
    @pytest.fixture
    def response(self, endpoint):
        return requests.get(urljoin(endpoint, 'register.json'))

    def test_content_type(self, response):
        assert response.headers['content-type'] == 'application/json'
